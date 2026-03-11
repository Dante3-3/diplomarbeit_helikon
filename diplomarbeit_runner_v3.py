#!/usr/bin/env python3
"""
Runner V3: Content Feedback Loop (qwen2.5:7b reviewer)
- Reads final_response from results_v2_structural.jsonl
- Content reviewer (qwen2.5:7b) checks for substantive errors per category
- If review FAILS: regenerate ONCE with content feedback
- Saves: content_feedback, content_pass, final_response_v3
- Output: diplomarbeit_output/results_v3_content.jsonl
"""

import json
import subprocess
import time
import os
import re
from datetime import datetime

INPUT_FILE = "diplomarbeit_output/results_v2_structural.jsonl"
RESULTS_FILE = "diplomarbeit_output/results_v3_content.jsonl"
REVIEWER_MODEL = "qwen2.5:7b"
CONFIG_PATH = "diplomarbeit_config_v2.json"
OLLAMA_URL = "http://localhost:11434/api/chat"
TIMEOUT = 900

# ── Content reviewer prompts (deeper, semantic checks) ──────────────────────

CONTENT_REVIEWER_SYSTEM = """You are an expert reviewer of AI-generated educational language exercises.
Your task is to detect substantive content errors — not formatting or structure (those were already checked).

Focus only on:
- Incorrect answers in the answer key
- Grammatically wrong solutions
- Answers that do not fit the gap or question context
- Factually wrong information

Respond with ONLY valid JSON:
{
  "pass": true or false,
  "issues": ["specific description of error in question X: what is wrong and what would be correct"]
}

Rules:
- "pass": true only if NO content errors are found
- Be specific — name the question number and explain the error
- Do NOT flag style preferences — only factual/grammatical errors
- If unsure, lean towards pass=true (do not over-flag)"""

CONTENT_REVIEWER_PROMPTS = {
    "Vocabulary": """Category: Vocabulary Matching Exercise
Original User Prompt: {user_prompt}
Exercise Output:
---
{output}
---

Check ONLY for these content issues:
1. WRONG DEFINITION: Does any definition factually mismatch its vocabulary word?
2. SELF-REFERENCE: Does any definition contain the word itself or a direct cognate?
3. ANSWER KEY ERROR: In the Teacher Answer Key, do the letter-number pairings actually correspond to correct matches between words and definitions?

List each error as: "Word [X] / Definition [Y]: [what is wrong]"
Respond with JSON only.""",

    "Multiple Choice": """Category: Multiple Choice Reading Comprehension
Original User Prompt: {user_prompt}
Exercise Output:
---
{output}
---

Check ONLY for these content issues:
1. WRONG CORRECT ANSWER: Is the marked correct answer actually incorrect based on the text provided?
2. MULTIPLE VALID ANSWERS: Are there questions where more than one answer option is factually correct?
3. TRICK QUESTIONS: Are there questions that use double negatives or misleading phrasing that makes the correct answer ambiguous?

For each issue: "Question [X]: [what is wrong, what the correct answer should be]"
Respond with JSON only.""",

    "Sentence Completion": """Category: Sentence Completion
Original User Prompt: {user_prompt}
Exercise Output:
---
{output}
---

Check ONLY for these content issues:
1. WRONG ANSWER: Does the Teacher Answer Key provide an answer that does not grammatically or factually complete the sentence correctly?
2. AMBIGUOUS GAP: Is there a gap where multiple very different answers could be correct (making the answer key arbitrary)?
3. FACTUAL ERROR: Does any answer contain factually incorrect information based on the provided text?

For each issue: "Question [X]: [what is wrong]"
Respond with JSON only.""",

    "Grammar": """Category: Grammar Exercise (mix of gap-fill, error correction, sentence transformation)
Original User Prompt: {user_prompt}
Exercise Output:
---
{output}
---

Check ONLY for these content issues:
1. WRONG TENSE/FORM: Does any gap-fill answer use the wrong grammatical tense or form for the context?
2. ERROR CORRECTION KEY WRONG: In error correction questions, is the provided correction grammatically wrong?
3. TRANSFORMATION ANSWER WRONG: Does a sentence transformation answer fail to preserve the original meaning, or use the wrong grammar structure?
4. ANSWER DOES NOT FIT: Does any answer key entry not grammatically fit into the sentence?

For each issue: "Question [X]: [what is wrong, what would be correct]"
Respond with JSON only.""",

    "True/False": """Category: True/False Reading Comprehension
Original User Prompt: {user_prompt}
Exercise Output:
---
{output}
---

Check ONLY for these content issues:
1. WRONG T/F ANSWER: Is any True/False answer in the key actually incorrect based on the provided text?
2. STATEMENT NOT IN TEXT: Does any statement ask about information that is not present in the provided text at all?

For each issue: "Statement [X]: [what is wrong — it says X but text says Y]"
Respond with JSON only.""",

    "Gap-Fill": """Category: Gap-Fill Exercise
Original User Prompt: {user_prompt}
Exercise Output:
---
{output}
---

Check ONLY for these content issues:
1. WRONG ANSWER: Does the Teacher Answer Key provide a word/phrase that does not grammatically fit the gap in the sentence?
2. FACTUAL ERROR: Is any answer factually wrong in context (e.g., wrong verb for the action described)?
3. BRACKET MISMATCH: For word-form gaps (base form in brackets), does the answer represent the wrong transformation of the given base word?

For each issue: "Gap [X]: given answer '[Y]' — [what is wrong, what would be correct]"
Respond with JSON only.""",

    "German Orthography": None  # Skip content check — flag for human review only
}


def unload_model(model):
    """Unload model from RAM via Ollama API."""
    payload = json.dumps({"model": model, "keep_alive": 0})
    subprocess.run(
        ["curl", "-s", "-X", "POST", "http://localhost:11434/api/generate",
         "-H", "Content-Type: application/json", "-d", payload],
        capture_output=True, timeout=10
    )
    print(f"  [RAM] Unloaded {model}")


def call_ollama(model, system_prompt, user_prompt, timeout=TIMEOUT):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,
        "options": {"num_ctx": 16384}
    }
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

    return data["message"]["content"].strip(), elapsed


def content_review(output_text, kategorie, user_prompt_text):
    """Run content review via qwen2.5:7b."""
    template = CONTENT_REVIEWER_PROMPTS.get(kategorie)

    if template is None:
        # German Orthography — skip, flag for human
        return True, [], "human_review_required", True

    review_prompt = template.format(
        output=output_text[:5000],
        user_prompt=user_prompt_text[:1000]
    )

    try:
        response, _ = call_ollama(REVIEWER_MODEL, CONTENT_REVIEWER_SYSTEM, review_prompt, timeout=180)
        json_match = re.search(r'\{[^{}]*"pass"[^{}]*\}', response, re.DOTALL)
        if json_match:
            review_data = json.loads(json_match.group())
        else:
            review_data = json.loads(response)
        return review_data.get("pass", True), review_data.get("issues", []), response, False
    except Exception as e:
        print(f"    [CONTENT REVIEWER ERROR] {e} — treating as PASS")
        return True, [], f"Reviewer error: {e}", False


def build_content_retry_prompt(original_user_prompt, issues):
    issues_text = "\n".join(f"- {issue}" for issue in issues)
    return f"""{original_user_prompt}

---
IMPORTANT: A content reviewer found the following errors in a previous attempt. Please fix ALL of these:

{issues_text}

Generate a completely corrected version that addresses all content errors above."""


def load_existing(results_file):
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


def main():
    os.makedirs("diplomarbeit_output", exist_ok=True)

    with open(CONFIG_PATH) as f:
        config = json.load(f)

    # Build lookup: (teil, test_id) -> (system_prompt, user_prompt, kategorie)
    prompt_lookup = {}
    for teil_key, teil_val in config["teile"].items():
        for p in teil_val["user_prompts"]:
            prompt_lookup[(teil_key, p["id"])] = {
                "system_prompt": teil_val["system_prompt"],
                "user_prompt": p["prompt"],
                "kategorie": teil_val["kategorie"]
            }

    # Load v2 results
    v2_entries = []
    with open(INPUT_FILE) as f:
        for line in f:
            try:
                v2_entries.append(json.loads(line))
            except:
                pass

    print(f"Loaded {len(v2_entries)} entries from {INPUT_FILE}")
    done = load_existing(RESULTS_FILE)
    print(f"Already completed: {len(done)} entries")

    total = len(v2_entries)
    current_generation_model = None
    current_reviewer_loaded = False

    with open(RESULTS_FILE, "a") as out_f:
        for i, v2_entry in enumerate(v2_entries):
            teil_key = v2_entry["teil"]
            model = v2_entry["model"]
            test_id = v2_entry["test_id"]
            rep = v2_entry["rep"]
            key = (teil_key, model, test_id, rep)

            if key in done:
                continue

            print(f"\n[{i+1}/{total}] {teil_key} | {model} | {test_id} | Rep {rep}")

            # Unload previous generation model if switching to a new one
            if current_generation_model and current_generation_model != model:
                unload_model(current_generation_model)
                time.sleep(2)
            current_generation_model = model

            lookup = prompt_lookup.get((teil_key, test_id))
            if not lookup:
                print(f"  WARNING: no prompt found for {teil_key}/{test_id} — skipping")
                continue

            system_prompt = lookup["system_prompt"]
            user_prompt = lookup["user_prompt"]
            kategorie = v2_entry["kategorie"]
            input_text = v2_entry["final_response"]  # Take v2's final output

            # ── Content review ──
            print(f"  Running content review ({REVIEWER_MODEL})...")
            content_pass, content_issues, content_raw, human_flag = content_review(
                input_text, kategorie, user_prompt
            )

            final_response_v3 = input_text
            revised = False
            revision_elapsed = 0.0

            if human_flag:
                print(f"  → Human review required (German Orthography)")
            elif not content_pass:
                print(f"  CONTENT REVIEW FAILED: {content_issues}")
                print(f"  Regenerating with content feedback...")
                # Unload reviewer before loading generation model
                unload_model(REVIEWER_MODEL)
                time.sleep(2)
                retry_prompt = build_content_retry_prompt(user_prompt, content_issues)
                try:
                    revised_response, revision_elapsed = call_ollama(
                        model, system_prompt, retry_prompt
                    )
                    if len(revised_response) > 50:
                        final_response_v3 = revised_response
                        revised = True
                        print(f"  Content-revised ({revision_elapsed:.1f}s)")
                    else:
                        print(f"  Revision too short — keeping v2 output")
                except Exception as e:
                    print(f"  Revision error: {e} — keeping v2 output")
            else:
                print(f"  CONTENT REVIEW PASSED")

            entry = {
                "teil": teil_key,
                "teil_name": v2_entry["teil_name"],
                "kategorie": kategorie,
                "model": model,
                "test_id": test_id,
                "test_title": v2_entry["test_title"],
                "rep": rep,
                # V2 fields carried over
                "v2_final_response": input_text,
                "v2_structural_pass": v2_entry["structural_pass"],
                "v2_was_revised": v2_entry["was_revised"],
                # V3 content review
                "content_pass": content_pass,
                "content_issues": content_issues,
                "content_feedback_raw": content_raw,
                "human_review_required": human_flag,
                "was_content_revised": revised,
                "final_response": final_response_v3,
                "revision_elapsed_seconds": revision_elapsed,
                "timestamp": datetime.now().isoformat()
            }
            out_f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            out_f.flush()
            done.add(key)

    print(f"\nDone! Results saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
