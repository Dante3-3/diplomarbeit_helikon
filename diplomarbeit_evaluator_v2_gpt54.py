#!/usr/bin/env python3
"""
Evaluator V2: Evaluates results from results_v2_structural.jsonl
Uses 'final_response' field (post-structural-review output).
Output: diplomarbeit_output/diplomarbeit_report_v2.md
"""

import json, sys, os, subprocess, time, argparse

CONFIG_PATH = "diplomarbeit_config_v2.json"
OUTPUT_DIR = "diplomarbeit_output"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results_v2_structural.jsonl")
REPORT_FILE = os.path.join(OUTPUT_DIR, "diplomarbeit_report_v2_gpt54.md")
EVAL_MODEL = "gpt-5.4"

CATEGORY_CRITERIA = {
    "Vocabulary": ["Definition Quality (no self-reference, context-accurate)",
                   "Randomization of definition order",
                   "Subject-specific relevance of chosen vocabulary"],
    "Multiple Choice": ["Exactly ONE correct answer per question",
                        "Distractor gradation (CA > MPD > LPD > WPD)",
                        "Letter randomization (no letter > 40%)",
                        "Questions follow text order"],
    "Sentence Completion": ["Strategic placement of gaps",
                             "Compliance with max word count per answer",
                             "Unambiguity of answers"],
    "Grammar": ["Clear target structure (tests intended grammar topic)",
                "Unambiguity of solutions",
                "Contextual embedding"],
    "True/False": ["Balanced T/F ratio (~50/50)",
                   "Paraphrasing (no direct quoting from text)",
                   "Cognitive demand appropriate for CEFR level"],
    "Gap-Fill": ["Word bank / bracketed forms correct and appropriate",
                 "Strategic gap placement",
                 "Unambiguity of solutions"],
    "German Orthography": ["Rule correctness (amtliche Regeln)",
                           "Quality of rule explanations",
                           "Coverage of sub-rules"],
}

MAX_POINTS = {
    "Vocabulary": 40, "Multiple Choice": 45, "Sentence Completion": 40,
    "Grammar": 40, "True/False": 40, "Gap-Fill": 40, "German Orthography": 40
}


def call_copilot(prompt, timeout=120):
    try:
        proc = subprocess.run(["copilot", "--model", EVAL_MODEL, "-p", prompt, "--yolo"],
                              capture_output=True, text=True, timeout=timeout,
                              cwd=OUTPUT_DIR)
        return proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[ERROR] Copilot timed out"
    except Exception as e:
        return f"[ERROR] {e}"


def evaluate_model_teil(teil_key, teil_name, kategorie, model, outputs, config):
    specific_criteria = CATEGORY_CRITERIA.get(kategorie, [])
    max_pts = MAX_POINTS.get(kategorie, 40)

    outputs_text = ""
    for i, o in enumerate(outputs, 1):
        outputs_text += f"\n--- Output {i} (Test: {o['test_id']}, Rep: {o['rep']}) ---\n"
        response_field = o.get("final_response", o.get("response", ""))
        outputs_text += response_field[:3000]
        outputs_text += "\n"

    eval_prompt = f"""You are an expert evaluator for AI-generated educational materials (CLIL context).

Evaluate these {len(outputs)} outputs from the LLM "{model}" for the category "{kategorie}" ({teil_name}).

Category-specific criteria (1-5 points each):
{chr(10).join('- ' + c for c in specific_criteria)}

General criteria (1-5 points each):
- Formatting
- CEFR Appropriateness
- Content Accuracy
- Instruction Adherence
- Language Quality

Maximum points: {max_pts}

{outputs_text}

Provide:
1. Overall SCORE out of {max_pts}
2. RANGE (min-max) across outputs
3. Brief 2-3 sentence SUMMARY

Format EXACTLY:
SCORE: X/{max_pts}
RANGE: X-Y/{max_pts}
SUMMARY: Your summary here."""

    print(f"  Evaluating {model}...", end=" ", flush=True)
    result = call_copilot(eval_prompt)
    print("Done")
    return result


def generate_report():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    all_results = []
    with open(RESULTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                all_results.append(json.loads(line))

    print(f"Loaded {len(all_results)} results from {RESULTS_FILE}")

    teil_keys = sorted(set(r["teil"] for r in all_results))
    report_lines = ["# Diplomarbeit V2 – Structural Feedback Loop Results\n",
                    f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
                    f"Reviewer model: qwen2.5:3b (structural checks)\n",
                    "---\n"]

    for teil_key in teil_keys:
        teil_results = [r for r in all_results if r["teil"] == teil_key]
        if not teil_results:
            continue

        teil_name = teil_results[0]["teil_name"]
        kategorie = teil_results[0]["kategorie"]
        max_pts = MAX_POINTS.get(kategorie, 40)

        report_lines.append(f"\n## {teil_key.upper()}: {teil_name}\n")
        report_lines.append(f"**Kategorie:** {kategorie} | **Max. Punkte:** {max_pts}\n")

        models = {}
        for r in teil_results:
            models.setdefault(r["model"], []).append(r)

        # Write outputs + review info
        for model, outputs in models.items():
            outputs.sort(key=lambda x: (x["test_id"], x["rep"]))
            report_lines.append(f"\n### Model: {model}\n")
            for o in outputs:
                report_lines.append(f"\n#### {o['test_id']} – Rep {o['rep']}\n")
                report_lines.append(f"*Generation: {o.get('elapsed_seconds','?'):.1f}s | "
                                    f"Structural review: {'PASS' if o['structural_pass'] else 'FAIL'} | "
                                    f"Revised: {'Yes' if o['was_revised'] else 'No'}*\n")
                if not o["structural_pass"] and o.get("structural_issues"):
                    report_lines.append(f"**Issues found:** {', '.join(o['structural_issues'])}\n")
                report_lines.append(f"\n{o['final_response']}\n\n---\n")

        # Evaluate
        report_lines.append(f"\n### Bewertung\n")
        report_lines.append("| Modell | Punkte | Range | Zusammenfassung |")
        report_lines.append("|--------|--------|-------|-----------------|")

        evaluations = {}
        for model, outputs in models.items():
            eval_result = evaluate_model_teil(teil_key, teil_name, kategorie, model, outputs, config)
            evaluations[model] = eval_result
            score, score_range, summary = "?", "?", eval_result[:200]
            for line in eval_result.split("\n"):
                if line.strip().startswith("SCORE:"):
                    score = line.split("SCORE:")[1].strip()
                elif line.strip().startswith("RANGE:"):
                    score_range = line.split("RANGE:")[1].strip()
                elif line.strip().startswith("SUMMARY:"):
                    summary = line.split("SUMMARY:")[1].strip()
            report_lines.append(f"| {model} | {score} | {score_range} | {summary} |")

        report_lines.append("\n\n#### Detaillierte Bewertungen\n")
        for model, eval_text in evaluations.items():
            report_lines.append(f"\n**{model}:**\n```\n{eval_text}\n```\n")

        report_lines.append("\n---\n")

    # Statistics summary
    total = len(all_results)
    failed = sum(1 for r in all_results if not r["structural_pass"])
    revised = sum(1 for r in all_results if r["was_revised"])
    report_lines.append(f"\n## Feedback Loop Statistics\n")
    report_lines.append(f"- Total outputs: {total}\n")
    report_lines.append(f"- Structural review FAIL: {failed} ({100*failed//total}%)\n")
    report_lines.append(f"- Successfully revised: {revised} ({100*revised//total}%)\n")

    report_content = "\n".join(report_lines)
    with open(REPORT_FILE, "w") as f:
        f.write(report_content)
    print(f"\nReport written to: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
