#!/usr/bin/env python3
"""
Evaluator Grammar-Split: Evaluates results_grammar_split.jsonl
Compares split grammar prompts (Gap-Fill / Error Correction / Sentence Transformation)
vs. original unified Grammar category.
Uses GPT-5.4 via GitHub Copilot CLI.
Output: diplomarbeit_output/diplomarbeit_report_grammarsplit_gpt54.md
"""

import json, os, subprocess, time

OUTPUT_DIR = "diplomarbeit_output"
RESULTS_FILE = os.path.join(OUTPUT_DIR, "results_grammar_split.jsonl")
REPORT_FILE = os.path.join(OUTPUT_DIR, "diplomarbeit_report_grammarsplit_gpt54.md")
EVAL_MODEL = "gpt-5.4"

CATEGORY_CRITERIA = {
    "Grammar Gap-Fill": [
        "Correct grammatical forms in answer key",
        "Unambiguity of solutions",
        "Contextual embedding",
        "Strategic gap placement",
    ],
    "Grammar Error Correction": [
        "Errors are clearly marked and correctable",
        "Correct answer key (grammatically sound corrections)",
        "Unambiguity of corrections",
        "Contextual embedding",
    ],
    "Grammar Sentence Transformation": [
        "Transformation preserves original meaning",
        "Correct grammar structure in answer key",
        "Unambiguity of solutions",
        "Contextual embedding",
    ],
}

MAX_POINTS = {
    "Grammar Gap-Fill": 40,
    "Grammar Error Correction": 40,
    "Grammar Sentence Transformation": 40,
}

TEIL_NAMES = {
    "teil5a": "Grammar Gap-Fill",
    "teil5b": "Grammar Error Correction",
    "teil5c": "Grammar Sentence Transformation",
}


def call_copilot(prompt, timeout=120):
    try:
        proc = subprocess.run(
            ["copilot", "--model", EVAL_MODEL, "-p", prompt, "--yolo"],
            capture_output=True, text=True, timeout=timeout, cwd=OUTPUT_DIR
        )
        return proc.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[ERROR] Copilot timed out"
    except Exception as e:
        return f"[ERROR] {e}"


def evaluate_model_teil(teil_key, kategorie, model, outputs):
    specific_criteria = CATEGORY_CRITERIA.get(kategorie, [])
    max_pts = MAX_POINTS.get(kategorie, 40)

    outputs_text = ""
    for i, o in enumerate(outputs, 1):
        outputs_text += f"\n--- Output {i} (Test: {o['test_id']}, Rep: {o['rep']}) ---\n"
        outputs_text += o.get("response", "")[:3000]
        outputs_text += "\n"

    eval_prompt = f"""You are an expert evaluator for AI-generated educational materials (CLIL context).

Evaluate these {len(outputs)} outputs from the LLM "{model}" for the category "{kategorie}".

The outputs were generated with SPLIT grammar prompts — each prompt tests ONLY ONE grammar sub-type ({kategorie}), not a mix.

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

Please provide:
1. An OVERALL score for this model out of {max_pts}
2. The range of quality across the outputs (min-max score)
3. A brief 2-3 sentence summary
4. Format your response EXACTLY like this:
SCORE: X/{max_pts}
RANGE: X-Y/{max_pts}
SUMMARY: Your summary here."""

    print(f"  Evaluating {model}...", end=" ", flush=True)
    result = call_copilot(eval_prompt)
    print("Done")
    return result


def generate_report():
    all_results = []
    with open(RESULTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                all_results.append(json.loads(line))

    print(f"Loaded {len(all_results)} results")

    report_lines = [
        "# Grammar-Split Evaluation (GPT-5.4)\n",
        f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"Evaluator model: {EVAL_MODEL} (via GitHub Copilot CLI)\n",
        "Split prompts: Gap-Fill / Error Correction / Sentence Transformation (each tested separately)\n",
        "---\n"
    ]

    for teil_key in ["teil5a", "teil5b", "teil5c"]:
        kategorie = TEIL_NAMES[teil_key]
        max_pts = MAX_POINTS.get(kategorie, 40)
        teil_results = [r for r in all_results if r["teil"] == teil_key]
        if not teil_results:
            continue

        report_lines.append(f"\n## {teil_key.upper()}: {kategorie}\n")
        report_lines.append(f"**Max. Punkte:** {max_pts}\n")

        models = {}
        for r in teil_results:
            models.setdefault(r["model"], []).append(r)

        report_lines.append("\n### Bewertung\n")
        report_lines.append("| Modell | Punkte | Range | Zusammenfassung |")
        report_lines.append("|--------|--------|-------|-----------------|")

        evaluations = {}
        for model, outputs in models.items():
            outputs.sort(key=lambda x: (x["test_id"], x["rep"]))
            eval_result = evaluate_model_teil(teil_key, kategorie, model, outputs)
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

    with open(REPORT_FILE, "w") as f:
        f.write("\n".join(report_lines))
    print(f"\nReport written to: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
