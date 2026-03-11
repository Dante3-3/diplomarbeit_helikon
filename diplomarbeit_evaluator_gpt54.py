#!/usr/bin/env python3
"""
Diplomarbeit Evaluator
Reads results from JSONL, generates markdown report, calls Copilot for evaluation.
Usage: python3 diplomarbeit_evaluator.py [--teil teil2] [--all]
"""

import json
import sys
import os
import subprocess
import time
import argparse

CONFIG_PATH = "/tmp/diplomarbeit_config_orig.json"
OUTPUT_DIR = "/Users/dstoilovski/Documents/Helikon/diplomarbeit_output"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results_original.jsonl")
REPORT_FILE = os.path.join(OUTPUT_DIR, "diplomarbeit_report_gpt54_run2.md")
EVAL_MODEL = "gpt-5.4"

# Category-specific criteria for the evaluation prompt
CATEGORY_CRITERIA = {
    "Vocabulary": [
        "Definition Quality (no self-reference, context-accurate)",
        "Randomization of definition order",
        "Subject-specific relevance of chosen vocabulary"
    ],
    "Multiple Choice": [
        "Exactly ONE correct answer per question",
        "Distractor gradation (CA > MPD > LPD > WPD)",
        "Letter randomization (no letter > 40%)",
        "Questions follow text order"
    ],
    "Sentence Completion": [
        "Strategic placement of gaps",
        "Compliance with max word count per answer",
        "Unambiguity of answers"
    ],
    "Grammar": [
        "Clear target structure (tests intended grammar topic)",
        "Unambiguity of solutions",
        "Contextual embedding"
    ],
    "True/False": [
        "Balanced T/F ratio (~50/50)",
        "Paraphrasing (no direct quoting from text)",
        "Cognitive demand appropriate for CEFR level"
    ],
    "Gap-Fill": [
        "Word bank / bracketed forms correct and appropriate",
        "Strategic gap placement",
        "Unambiguity of solutions"
    ],
    "German Orthography": [
        "Rule correctness (amtliche Regeln)",
        "Quality of rule explanations",
        "Coverage of sub-rules"
    ]
}

MAX_POINTS = {
    "Vocabulary": 40,
    "Multiple Choice": 45,
    "Sentence Completion": 40,
    "Grammar": 40,
    "True/False": 40,
    "Gap-Fill": 40,
    "German Orthography": 40
}


def load_results(teil_filter=None):
    """Load results from JSONL file, optionally filtered by teil."""
    results = []
    if not os.path.exists(RESULTS_FILE):
        print(f"ERROR: Results file not found: {RESULTS_FILE}")
        sys.exit(1)

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if teil_filter is None or r["teil"] == teil_filter:
                results.append(r)
    return results


def call_copilot(prompt, timeout=120):
    """Call GitHub Copilot CLI for evaluation using GPT-5.4."""
    try:
        proc = subprocess.run(
            ["copilot", "--model", EVAL_MODEL, "-p", prompt, "--yolo"],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=OUTPUT_DIR
        )
        return proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[ERROR] Copilot timed out"
    except Exception as e:
        return f"[ERROR] {str(e)}"


def evaluate_model_teil(teil_key, teil_name, kategorie, model, outputs, config):
    """Evaluate all outputs of one model for one teil using Copilot."""
    eval_system = config["evaluation"]["system_prompt"]
    specific_criteria = CATEGORY_CRITERIA.get(kategorie, [])
    max_pts = MAX_POINTS.get(kategorie, 40)

    # Build the evaluation prompt
    outputs_text = ""
    for i, o in enumerate(outputs, 1):
        outputs_text += f"\n--- Output {i} (Test: {o['test_id']}, Repetition: {o['rep']}) ---\n"
        outputs_text += o["response"][:3000]  # Truncate very long outputs
        outputs_text += "\n"

    eval_prompt = f"""You are an expert evaluator for AI-generated educational materials (CLIL context).

Evaluate these {len(outputs)} outputs from the LLM "{model}" for the category "{kategorie}" ({teil_name}).

The outputs were generated with the same system prompt but different user prompts (3 prompts, 3 repetitions each = 9 outputs).

Category-specific criteria (1-5 points each):
{chr(10).join('- ' + c for c in specific_criteria)}

General criteria (1-5 points each):
- Formatting
- CEFR Appropriateness
- Content Accuracy
- Instruction Adherence
- Language Quality

Maximum points for this category: {max_pts}

{outputs_text}

Please provide:
1. An OVERALL score for this model (sum of all criteria averages) out of {max_pts}
2. The range of quality across the 9 outputs (min-max score)
3. A brief 2-3 sentence summary
4. Format your response EXACTLY like this:
SCORE: X/{max_pts}
RANGE: X-Y/{max_pts}
SUMMARY: Your summary here."""

    print(f"  Evaluating {model}... ", end="", flush=True)
    result = call_copilot(eval_prompt)
    print("Done")
    return result


def generate_report(teil_keys=None):
    """Generate the full markdown report with evaluations."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    all_results = load_results()

    if teil_keys is None:
        teil_keys = sorted(set(r["teil"] for r in all_results))

    report_lines = ["# Diplomarbeit - LLM Test Results & Evaluation\n"]
    report_lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    report_lines.append(f"Evaluator model: {EVAL_MODEL} (via GitHub Copilot CLI)\n")
    report_lines.append("---\n")

    for teil_key in teil_keys:
        teil_results = [r for r in all_results if r["teil"] == teil_key]
        if not teil_results:
            print(f"No results for {teil_key}, skipping...")
            continue

        teil_name = teil_results[0]["teil_name"]
        kategorie = teil_results[0]["kategorie"]
        max_pts = MAX_POINTS.get(kategorie, 40)

        report_lines.append(f"\n## {teil_key.upper()}: {teil_name}\n")
        report_lines.append(f"**Kategorie:** {kategorie} | **Max. Punkte:** {max_pts}\n")

        # Group by model
        models = {}
        for r in teil_results:
            if r["model"] not in models:
                models[r["model"]] = []
            models[r["model"]].append(r)

        # Write all outputs
        for model, outputs in models.items():
            report_lines.append(f"\n### Model: {model}\n")
            # Sort by test_id then rep
            outputs.sort(key=lambda x: (x["test_id"], x["rep"]))
            for o in outputs:
                report_lines.append(f"\n#### {o['test_id']} - Wiederholung {o['rep']}\n")
                report_lines.append(f"*Dauer: {o.get('elapsed_seconds', '?')}s*\n")
                report_lines.append(f"\n{o['response']}\n")
                report_lines.append("\n---\n")

        # Evaluation section
        report_lines.append(f"\n### Bewertung - {teil_key.upper()}: {teil_name}\n")
        report_lines.append(f"\n| Modell | Punkte | Range | Zusammenfassung |")
        report_lines.append(f"\n|--------|--------|-------|-----------------|")

        evaluations = {}
        for model, outputs in models.items():
            eval_result = evaluate_model_teil(
                teil_key, teil_name, kategorie, model, outputs, config
            )
            evaluations[model] = eval_result

            # Parse the evaluation result
            score = "?"
            score_range = "?"
            summary = eval_result[:200] if eval_result else "No evaluation"

            for line in eval_result.split("\n"):
                if line.strip().startswith("SCORE:"):
                    score = line.split("SCORE:")[1].strip()
                elif line.strip().startswith("RANGE:"):
                    score_range = line.split("RANGE:")[1].strip()
                elif line.strip().startswith("SUMMARY:"):
                    summary = line.split("SUMMARY:")[1].strip()

            report_lines.append(f"\n| {model} | {score} | ({score_range}) | {summary} |")

        # Write full evaluation details
        report_lines.append(f"\n\n#### Detaillierte Bewertungen\n")
        for model, eval_text in evaluations.items():
            report_lines.append(f"\n**{model}:**\n")
            report_lines.append(f"```\n{eval_text}\n```\n")

        report_lines.append("\n---\n")

    # Write report
    report_content = "\n".join(report_lines)
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"\nReport written to: {REPORT_FILE}")
    print(f"Total results processed: {len(all_results)}")
    return REPORT_FILE


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate LLM test results")
    parser.add_argument("--teil", help="Evaluate specific teil (e.g. teil2)")
    parser.add_argument("--all", action="store_true", help="Evaluate all teile")
    args = parser.parse_args()

    if args.teil:
        generate_report([args.teil])
    elif args.all:
        generate_report()
    else:
        print("Usage: python3 diplomarbeit_evaluator.py --teil teil2  OR  --all")
        sys.exit(1)
