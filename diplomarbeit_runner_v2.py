#!/usr/bin/env python3
"""
Runner V2: Generation + Structural Feedback Loop (qwen2.5:3b reviewer)
- Generates outputs with mistral, gemma2, qwen3.5:9b (no thinking mode)
- After each output: structural reviewer checks formatting/structure
- If review FAILS: regenerate ONCE with feedback included
- Saves: initial_response, structural_feedback, structural_pass, final_response
- Output: diplomarbeit_output/results_v2_structural.jsonl
"""

import json
import subprocess
import time
import os
import sys
from datetime import datetime

CONFIG_PATH = "diplomarbeit_config_v2.json"
RESULTS_FILE = "diplomarbeit_output/results_v2_structural.jsonl"
REVIEWER_MODEL = "qwen2.5:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"
TIMEOUT = 900

# ── Category-specific structural check prompts ──────────────────────────────

REVIEWER_SYSTEM_PROMPT = """You are a strict quality-control checker for AI-generated educational exercises.
Your sole task is to detect critical structural and formatting errors — NOT to evaluate style or content quality.

You will receive the exercise category, the original prompts, and the generated output.
Respond with ONLY valid JSON in this exact format:
{
  "pass": true or false,
  "issues": ["short description of issue 1", "short description of issue 2"]
}

Rules:
- "pass": true ONLY if NO critical issues are found
- "issues": empty array [] if pass is true
- Be strict but mechanical — only flag clear, verifiable violations
- Do NOT comment on style, creativity, or minor wording preferences
- Do NOT rewrite or improve the exercise — only identify problems"""

REVIEWER_USER_PROMPTS = {
    "Vocabulary": """Category: Vocabulary (Knowledge Activation)
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. INCOMPLETE OUTPUT: Is the output cut off or missing the Student Answer Table or Teacher Answer Key?
2. WRONG COUNT: Does the vocabulary list have exactly 10 words AND exactly 10 definitions (A–J)?
3. SEQUENTIAL ORDER: Are definitions in sequential A=1, B=2, C=3... order? (This defeats the matching exercise — flag if ALL or nearly ALL are sequential)
4. SELF-REFERENCE: Does any definition contain the vocabulary word itself or a direct derivation of it?
5. MISSING SECTIONS: Are all three parts present — Speaking questions, Vocabulary Matching, AND Student/Teacher tables?

Respond with JSON only.""",

    "Multiple Choice": """Category: Multiple Choice Reading Comprehension
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. INCOMPLETE OUTPUT: Is the output cut off or missing the answer key?
2. MULTIPLE CORRECT ANSWERS: Does any question say "select all that apply" or have more than one marked correct answer?
3. LETTER BIAS: In the answer key, does any single letter (A, B, C, or D) appear as the correct answer for more than 60% of questions?
4. MISSING ANSWER KEY: Is the answer key absent or incomplete?
5. QUESTION COUNT MISMATCH: Does the number of questions in the answer key match the number in the exercise?

Respond with JSON only.""",

    "Sentence Completion": """Category: Sentence Completion
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. INCOMPLETE OUTPUT: Is the output cut off or missing the Student Answer Table or Teacher Answer Key?
2. WORD COUNT VIOLATION: Do any answers in the Teacher Answer Key exceed the maximum word count specified in the user prompt? Count words carefully.
3. MISSING GAPS: Are there actual sentence completion gaps (blanks) in the exercise questions?
4. COUNT MISMATCH: Does the number of answers in the key match the number of gaps in the exercise?

Respond with JSON only.""",

    "Grammar": """Category: Grammar (mixed: gap-fill, error correction, sentence transformation)
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. INCOMPLETE OUTPUT: Is the output cut off or missing the Student Answer Table or Teacher Answer Key?
2. COUNT MISMATCH: Does the number of answers in the Teacher Answer Key match the number of questions in the exercise?
3. MISSING ANSWER KEY: Is the Teacher Answer Key absent or completely empty?
4. EMPTY ANSWERS: Are any answer key cells blank or contain only "..." placeholders?

Respond with JSON only.""",

    "True/False": """Category: True/False Reading Comprehension
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. INCOMPLETE OUTPUT: Is the output cut off or missing the answer key?
2. NO QUESTIONS GENERATED: Did the model fail to generate any True/False questions (e.g., only responded with a meta-message asking for more input)?
3. ALL SAME ANSWER: Are all answers either all True or all False (no balance at all)?
4. MISSING ANSWER KEY: Is the answer key absent?
5. COUNT MISMATCH: Does the number of T/F answers in the key match the number of statements in the exercise?

Respond with JSON only.""",

    "Gap-Fill": """Category: Gap-Fill (Klassischer Lückentext)
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. NO GAPS: Are there actual blank gaps (___) in the exercise text? If the text is fully written out with no blanks, this is a critical failure.
2. WORD BANK MISMATCH: If a word bank is present, do all words in the Teacher Answer Key also appear in the word bank? List any missing words.
3. COUNT MISMATCH: Does the number of answers in the Teacher Answer Key match the number of gaps in the text?
4. INCOMPLETE OUTPUT: Is the output cut off or missing the Student Answer Table or Teacher Answer Key?
5. ANSWERS PRE-FILLED: Are the answers already filled into the text (making it not a gap-fill exercise)?

Respond with JSON only.""",

    "German Orthography": """Category: German Orthography (Deutsche Rechtschreibung & Grammatik)
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. INCOMPLETE OUTPUT: Is the output cut off mid-sentence or missing the answer key?
2. NO EXERCISES: Did the model fail to generate actual exercises (e.g., only responded with a preamble)?
3. MISSING ANSWER KEY: Is the Lösungsschlüssel/answer key absent?
4. COUNT MISMATCH: Does the number of answers in the key match the number of exercise items?

Note: Do NOT check for correctness of German grammar rules — only check structure.
Respond with JSON only.""",

    "Grammar Gap-Fill": """Category: Grammar Gap-Fill
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. TYPE VIOLATION: Does the output contain Error Correction or Sentence Transformation items? (should be Gap-Fill only)
2. NO GAPS: Are there actual blanks (___) in the exercise text?
3. COUNT MISMATCH: Does the Teacher Answer Key have the same number of answers as there are gaps?
4. WORD BANK MISMATCH: If a word bank is present, do all answer key words appear in the word bank?
5. INCOMPLETE OUTPUT: Is the output cut off or missing Student Table or Answer Key?

Respond with JSON only.""",

    "Grammar Error Correction": """Category: Grammar Error Correction
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. TYPE VIOLATION: Does the output contain Gap-Fill or Sentence Transformation items? (should be Error Correction only)
2. NO ERRORS MARKED: Are errors shown in bold or otherwise marked in each sentence?
3. COUNT MISMATCH: Does the Teacher Answer Key have the same number of answers as there are questions?
4. INCOMPLETE OUTPUT: Is the output cut off or missing Student Table or Answer Key?

Respond with JSON only.""",

    "Grammar Sentence Transformation": """Category: Grammar Sentence Transformation
Exercise output to check:
---
{output}
---

Check ONLY for these critical structural issues:
1. TYPE VIOLATION: Does the output contain Gap-Fill or Error Correction items? (should be Sentence Transformation only)
2. NO STARTER PROVIDED: Does each transformation question provide a sentence starter or transformation instruction?
3. COUNT MISMATCH: Does the Teacher Answer Key have the same number of answers as there are questions?
4. INCOMPLETE OUTPUT: Is the output cut off or missing Student Table or Answer Key?

Respond with JSON only."""
}


def call_ollama(model, system_prompt, user_prompt, timeout=TIMEOUT):
    """Call Ollama API, returns (response_text, elapsed_seconds) or raises."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"num_ctx": 16384}
    }
    # Disable thinking mode for qwen3 models
    if "qwen3" in model.lower():
        payload["think"] = False

    payload_str = json.dumps(payload)
    start = time.time()
    result = subprocess.run(
        ["curl", "-s", "-X", "POST", OLLAMA_URL,
         "-H", "Content-Type: application/json",
         "-d", payload_str],
        capture_output=True, text=True, timeout=timeout
    )
    elapsed = time.time() - start

    if result.returncode != 0:
        raise RuntimeError(f"curl failed: {result.stderr}")

    data = json.loads(result.stdout)
    if "error" in data:
        raise RuntimeError(f"Ollama error: {data['error']}")

    text = data["message"]["content"].strip()
    return text, elapsed


def structural_review(output_text, kategorie):
    """Run structural review via qwen2.5:3b. Returns (pass_bool, issues_list, feedback_text)."""
    template = REVIEWER_USER_PROMPTS.get(kategorie, REVIEWER_USER_PROMPTS["Grammar"])
    user_prompt = template.format(output=output_text[:4000])  # limit to avoid context overflow

    try:
        response, _ = call_ollama(REVIEWER_MODEL, REVIEWER_SYSTEM_PROMPT, user_prompt, timeout=120)
        # Extract JSON from response (may have extra text)
        import re
        json_match = re.search(r'\{[^{}]*"pass"[^{}]*\}', response, re.DOTALL)
        if json_match:
            review_data = json.loads(json_match.group())
            return review_data.get("pass", True), review_data.get("issues", []), response
        else:
            # Try parsing the whole response
            review_data = json.loads(response)
            return review_data.get("pass", True), review_data.get("issues", []), response
    except Exception as e:
        print(f"    [REVIEWER ERROR] {e} — treating as PASS")
        return True, [], f"Reviewer error: {e}"


def build_retry_prompt(original_user_prompt, original_output, issues):
    """Build a retry user prompt that includes the reviewer feedback."""
    issues_text = "\n".join(f"- {issue}" for issue in issues)
    return f"""{original_user_prompt}

---
IMPORTANT: A quality reviewer found the following critical issues in a previous attempt. Please fix ALL of these in your new output:

{issues_text}

Generate a completely corrected version that addresses all issues above."""


def load_existing(results_file):
    """Load already completed entries to allow resuming."""
    done = set()
    if os.path.exists(results_file):
        with open(results_file) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    key = (entry["teil"], entry["model"], entry["test_id"], entry["rep"])
                    done.add(key)
                except:
                    pass
    return done


def is_problematic(text):
    """Check if output is clearly a failure."""
    if len(text) < 50:
        return True
    fail_phrases = [
        "please provide", "i need more information", "could you please",
        "i'm ready to", "i am ready to", "please give me"
    ]
    lower = text.lower()
    return any(p in lower for p in fail_phrases)


def main():
    os.makedirs("diplomarbeit_output", exist_ok=True)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    models = config["models"]
    reps = config["repetitions"]
    teile = config["teile"]

    done = load_existing(RESULTS_FILE)
    print(f"Already completed: {len(done)} entries")

    total = sum(len(v["user_prompts"]) * len(models) * reps for v in teile.values())
    completed = 0

    with open(RESULTS_FILE, "a") as out_f:
        for teil_key, teil_val in teile.items():
            system_prompt = teil_val["system_prompt"]
            kategorie = teil_val["kategorie"]

            for prompt_data in teil_val["user_prompts"]:
                test_id = prompt_data["id"]
                test_title = prompt_data["title"]
                user_prompt = prompt_data["prompt"]

                for model in models:
                    for rep in range(1, reps + 1):
                        key = (teil_key, model, test_id, rep)
                        if key in done:
                            completed += 1
                            continue

                        print(f"\n[{completed+1}/{total}] {teil_key} | {model} | {test_id} | Rep {rep}")

                        # ── Step 1: Generate initial output ──
                        try:
                            initial_response, elapsed = call_ollama(model, system_prompt, user_prompt)
                        except Exception as e:
                            print(f"  ERROR generating: {e}")
                            continue

                        if is_problematic(initial_response):
                            print(f"  PROBLEMATIC initial output — skipping")
                            continue

                        print(f"  Generated ({elapsed:.1f}s, {len(initial_response)} chars)")

                        # ── Step 2: Structural review ──
                        print(f"  Running structural review ({REVIEWER_MODEL})...")
                        review_pass, review_issues, review_raw = structural_review(initial_response, kategorie)

                        final_response = initial_response
                        revised = False
                        revision_elapsed = 0.0

                        if not review_pass:
                            print(f"  REVIEW FAILED: {review_issues}")
                            print(f"  Regenerating with feedback...")

                            retry_prompt = build_retry_prompt(user_prompt, initial_response, review_issues)
                            try:
                                revised_response, revision_elapsed = call_ollama(model, system_prompt, retry_prompt)
                                if not is_problematic(revised_response):
                                    final_response = revised_response
                                    revised = True
                                    print(f"  Revised ({revision_elapsed:.1f}s)")
                                else:
                                    print(f"  Revision was problematic — keeping original")
                            except Exception as e:
                                print(f"  Revision error: {e} — keeping original")
                        else:
                            print(f"  REVIEW PASSED")

                        # ── Step 3: Save result ──
                        entry = {
                            "teil": teil_key,
                            "teil_name": teil_val["name"],
                            "kategorie": kategorie,
                            "model": model,
                            "test_id": test_id,
                            "test_title": test_title,
                            "rep": rep,
                            "initial_response": initial_response,
                            "structural_pass": review_pass,
                            "structural_issues": review_issues,
                            "structural_feedback_raw": review_raw,
                            "was_revised": revised,
                            "final_response": final_response,
                            "elapsed_seconds": elapsed,
                            "revision_elapsed_seconds": revision_elapsed,
                            "timestamp": datetime.now().isoformat()
                        }
                        out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                        out_f.flush()
                        done.add(key)
                        completed += 1

    print(f"\nDone! {completed} entries saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
