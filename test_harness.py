#!/usr/bin/env python3
"""CLIL Benchmark — Evaluates local Ollama LLMs on CLIL educational content generation.

Usage:
    python test_harness.py            # Fresh run (overwrites previous results)
    python test_harness.py --resume   # Resume an interrupted run

Required folder structure:
    .
    ├── test_harness.py
    ├── CLIL_Prompts.md
    └── material/
        ├── Material1.txt
        ├── Material2.txt
        └── Material3.txt
"""

import csv
import json
import re
import shutil
import sys
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import ollama

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

TEST_MODELS = [
    "jobautomation/OpenEuroLLM-German:latest",
    "mistral-nemo:latest",
    "deepseek-r1:14b",
    "gemma3:12b",
]

TRANSLATOR_MODEL = "translategemma:12b"
JUDGE_MODEL = "deepseek-r1:14b"

MATERIAL_DIR = Path("material")
PROMPTS_FILE = Path("CLIL_Prompts.md")
RESULTS_CSV = Path("benchmark_results.csv")
SUMMARY_MD = Path("summary.md")
OUTPUTS_DIR = Path("outputs")
GRADING_DIR = Path("grading")
REPORT_HTML = Path("report.html")
REPORT_TEMPLATE = Path("report_template.html")

# Text placeholder in user prompts — replaced with material content
PLACEHOLDER = "[Text hier einfügen]"

# Default values for other prompt placeholders
DEFAULTS = {
    "[A1 bis C2]": "B2",
    "[A1-C2]": "B2",
    "[Anzahl]": "10",
    "[Anzahl einfügen]": "10",
}

# Ollama context window size (increase if your materials are long)
NUM_CTX = 8192


# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════


@dataclass
class PromptSection:
    name: str
    system_prompt: str
    user_prompts: dict  # {"level1": str, "level2": str}


@dataclass
class GenResult:
    content: str
    wall_time_s: float
    eval_count: int
    eval_duration_ns: int
    tokens_per_sec: float


@dataclass
class BenchmarkRow:
    model: str
    material: str
    prompt_section: str
    level: str
    workflow: str
    gen_time_s: float
    trans_time_s: float
    total_time_s: float
    tokens_per_sec: float
    score: int
    reasoning: str


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════


def short_name(model: str) -> str:
    """Extract a short display name from a model identifier."""
    return model.split("/")[-1].split(":")[0][:30]


def strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks (e.g. deepseek-r1 reasoning traces)."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def log(msg: str):
    print(f"  [{time.strftime('%H:%M:%S')}] {msg}")


def _run_path(base_dir: Path, model: str, material: str, section_name: str,
              level: str, workflow: str) -> Path:
    """Build an output file path like base_dir/<short_model>/<mat>_<sec>_<lvl>_<wf>.md"""
    model_dir = base_dir / short_name(model)
    sec_safe = re.sub(r'[^\w\-]', '_', section_name.split(":")[-1].strip())[:30]
    filename = f"{material}_{sec_safe}_{level}_{workflow}.md"
    return model_dir / filename


def save_output(model: str, material: str, section_name: str, level: str,
                workflow: str, content: str):
    """Save LLM-generated content to outputs/<model>/....md"""
    path = _run_path(OUTPUTS_DIR, model, material, section_name, level, workflow)
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# Output: {short_name(model)}\n\n"
        f"- **Material**: {material}\n"
        f"- **Section**: {section_name}\n"
        f"- **Level**: {level}\n"
        f"- **Workflow**: {workflow}\n"
        f"- **Generated**: {time.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"---\n\n"
    )
    path.write_text(header + content, encoding="utf-8")


def save_grading(model: str, material: str, section_name: str, level: str,
                 workflow: str, score: int, reasoning: str):
    """Save judge evaluation to grading/<model>/....md"""
    path = _run_path(GRADING_DIR, model, material, section_name, level, workflow)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        f"# Grading: {short_name(model)}\n\n"
        f"- **Material**: {material}\n"
        f"- **Section**: {section_name}\n"
        f"- **Level**: {level}\n"
        f"- **Workflow**: {workflow}\n"
        f"- **Judge Model**: {JUDGE_MODEL}\n"
        f"- **Evaluated**: {time.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"## Score: {score}/5\n\n"
        f"## Reasoning\n\n{reasoning}\n"
    )
    path.write_text(text, encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPT PARSING
# ═══════════════════════════════════════════════════════════════════════════════


def parse_prompts(filepath: Path) -> list[PromptSection]:
    """Parse CLIL_Prompts.md into structured PromptSection objects.

    Only sections whose user prompts contain PLACEHOLDER are returned.
    """
    text = filepath.read_text(encoding="utf-8")

    # Split at each "## X.Y Training Prompt:" header
    parts = re.split(
        r"(?=^## \d+\.\d+ Training Prompt:)", text, flags=re.MULTILINE
    )

    sections: list[PromptSection] = []
    for part in parts:
        header = re.match(r"^## (.+)", part)
        if not header or "### User Prompt" not in part:
            continue

        name = header.group(1).strip()
        sys_block, user_block = part.split("### User Prompt", 1)

        # System prompt = everything after the header line
        system_prompt = "\n".join(sys_block.split("\n")[1:]).strip()

        # Extract Level 1 / Level 2 user prompts
        user_prompts: dict[str, str] = {}

        m1 = re.search(
            r"\*\*Variant A \(Level 1\)\*\*\s*\n(.*?)(?=\*\*Variant B|\Z)",
            user_block,
            re.DOTALL,
        )
        if m1:
            user_prompts["level1"] = m1.group(1).strip()

        m2 = re.search(
            r"\*\*Variant B \(Level 2\)\*\*\s*\n(.*?)(?=\n## |\Z)",
            user_block,
            re.DOTALL,
        )
        if m2:
            user_prompts["level2"] = m2.group(1).strip()

        # Only keep sections whose user prompts use the text placeholder
        if user_prompts and any(PLACEHOLDER in v for v in user_prompts.values()):
            sections.append(
                PromptSection(
                    name=name,
                    system_prompt=system_prompt,
                    user_prompts=user_prompts,
                )
            )

    return sections


def prepare_prompt(template: str, material: str, language: str) -> str:
    """Fill placeholders and set the output-language instruction."""
    prompt = template.replace(PLACEHOLDER, material)
    for ph, default in DEFAULTS.items():
        prompt = prompt.replace(ph, default)

    if language == "de":
        prompt = prompt.replace(
            "Der Output soll auf Deutsch sein.",
            "Output strictly in German. Antworten Sie ausschließlich auf Deutsch.",
        )
    elif language == "en":
        prompt = prompt.replace(
            "Der Output soll auf Deutsch sein.",
            "Output strictly in English.",
        )
    return prompt


# ═══════════════════════════════════════════════════════════════════════════════
# OLLAMA INTERACTION
# ═══════════════════════════════════════════════════════════════════════════════


def call_model(model: str, system_prompt: str, user_prompt: str) -> GenResult:
    """Send a chat request to an Ollama model and return result with metrics."""
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})

    start = time.perf_counter()
    response = ollama.chat(
        model=model, messages=messages, options={"num_ctx": NUM_CTX}
    )
    wall_time = time.perf_counter() - start

    content = response["message"]["content"]
    eval_count = response.get("eval_count", 0) or 0
    eval_duration = response.get("eval_duration", 0) or 0  # nanoseconds

    if eval_duration and eval_duration > 0:
        tps = eval_count / (eval_duration / 1e9)
    elif wall_time > 0:
        tps = eval_count / wall_time
    else:
        tps = 0.0

    return GenResult(
        content=content,
        wall_time_s=wall_time,
        eval_count=eval_count,
        eval_duration_ns=eval_duration,
        tokens_per_sec=tps,
    )


def translate_to_german(english_text: str) -> GenResult:
    """Translate English text to German via the translator utility model."""
    prompt = (
        "Translate the following educational text into natural German:\n\n"
        + english_text
    )
    return call_model(TRANSLATOR_MODEL, "", prompt)


def judge_content(content: str, level_key: str) -> tuple[int, str]:
    """Evaluate German CLIL material with the judge model. Returns (score, reasoning)."""
    level_desc = (
        "Recall — explicit facts and factual accuracy"
        if level_key == "level1"
        else "Synthesis — deep understanding, connections, Why/How reasoning"
    )

    prompt = (
        "Evaluate the following German CLIL educational material on a 1-5 scale.\n\n"
        "Criteria:\n"
        f"  1. Adherence to cognitive level: {level_desc}\n"
        "  2. Language Naturalness (fluent, idiomatic German)\n"
        "  3. Educational Quality\n\n"
        'Return ONLY valid JSON: {"score": <1-5>, "reasoning": "<brief explanation>"}\n\n'
        "--- CONTENT ---\n"
        + content[:4000]
    )

    result = call_model(JUDGE_MODEL, "", prompt)
    raw = strip_think_tags(result.content)

    try:
        start_idx = raw.index("{")
        end_idx = raw.rindex("}") + 1
        data = json.loads(raw[start_idx:end_idx])
        score = max(0, min(5, int(data.get("score", 0))))
        reasoning = str(data.get("reasoning", ""))
        return score, reasoning
    except (ValueError, json.JSONDecodeError):
        return 0, f"JSON parse error: {raw[:200]}"


# ═══════════════════════════════════════════════════════════════════════════════
# CSV I/O
# ═══════════════════════════════════════════════════════════════════════════════

CSV_FIELDS = [
    "Model",
    "Material",
    "Prompt_Section",
    "Level",
    "Workflow",
    "Gen_Time_s",
    "Trans_Time_s",
    "Total_Time_s",
    "Tokens_per_sec",
    "Score",
    "Reasoning",
]


def load_completed(csv_path: Path) -> set[tuple]:
    """Load already-completed run keys from an existing CSV."""
    done: set[tuple] = set()
    if not csv_path.exists():
        return done
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            done.add(
                (
                    row["Model"],
                    row["Material"],
                    row["Prompt_Section"],
                    row["Level"],
                    row["Workflow"],
                )
            )
    return done


def append_row(row: BenchmarkRow):
    """Append a single result row to the CSV (creates header if needed)."""
    needs_header = not RESULTS_CSV.exists() or RESULTS_CSV.stat().st_size == 0
    with open(RESULTS_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if needs_header:
            w.writerow(CSV_FIELDS)
        w.writerow(
            [
                row.model,
                row.material,
                row.prompt_section,
                row.level,
                row.workflow,
                row.gen_time_s,
                row.trans_time_s,
                row.total_time_s,
                row.tokens_per_sec,
                row.score,
                row.reasoning,
            ]
        )


def load_all_rows(csv_path: Path) -> list[BenchmarkRow]:
    """Load every result row from CSV."""
    rows: list[BenchmarkRow] = []
    if not csv_path.exists():
        return rows
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(
                BenchmarkRow(
                    model=r["Model"],
                    material=r["Material"],
                    prompt_section=r["Prompt_Section"],
                    level=r["Level"],
                    workflow=r["Workflow"],
                    gen_time_s=float(r["Gen_Time_s"]),
                    trans_time_s=float(r["Trans_Time_s"]),
                    total_time_s=float(r["Total_Time_s"]),
                    tokens_per_sec=float(r["Tokens_per_sec"]),
                    score=int(r["Score"]),
                    reasoning=r["Reasoning"],
                )
            )
    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# MODEL VERIFICATION
# ═══════════════════════════════════════════════════════════════════════════════


def verify_models():
    """Check that all required models are pulled in Ollama."""
    try:
        response = ollama.list()
        # Handle both dict and object API styles
        if isinstance(response, dict):
            models_raw = response.get("models", [])
        else:
            models_raw = getattr(response, "models", [])

        available: set[str] = set()
        for m in models_raw:
            if isinstance(m, dict):
                available.add(m.get("name", ""))
                available.add(m.get("model", ""))
            else:
                available.add(getattr(m, "name", ""))
                available.add(getattr(m, "model", ""))
    except Exception as e:
        print(f"\n  WARNING: Cannot connect to Ollama: {e}")
        print("  Make sure Ollama is running (ollama serve).")
        return

    all_needed = sorted(set(TEST_MODELS) | {TRANSLATOR_MODEL, JUDGE_MODEL})
    missing = [m for m in all_needed if m not in available]
    if missing:
        print(f"\n  WARNING: {len(missing)} model(s) not found locally:")
        for m in missing:
            print(f"    - {m}")
        print("  Pull them with:  ollama pull <model-name>")


# ═══════════════════════════════════════════════════════════════════════════════
# SUMMARY GENERATION
# ═══════════════════════════════════════════════════════════════════════════════


def write_summary(rows: list[BenchmarkRow]):
    """Generate summary.md from all benchmark results."""

    def avg(lst):
        return sum(lst) / len(lst) if lst else 0

    lines = [
        "# CLIL Benchmark — Summary",
        "",
        f"*Generated: {time.strftime('%Y-%m-%d %H:%M')}*  ",
        f"*Total runs: {len(rows)}*",
        "",
    ]

    valid = [r for r in rows if r.score > 0]
    if not valid:
        lines.append("No valid results to summarise.")
        SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")
        return

    # Aggregate by (model, workflow)
    agg: dict[tuple, dict] = defaultdict(
        lambda: {"scores": [], "speeds": [], "times": []}
    )
    for r in valid:
        k = (r.model, r.workflow)
        agg[k]["scores"].append(r.score)
        agg[k]["speeds"].append(r.tokens_per_sec)
        agg[k]["times"].append(r.total_time_s)

    # ── Overall leaderboard ──────────────────────────────────────────────
    lines += [
        "## Overall Leaderboard",
        "",
        "| Rank | Model | Workflow | Avg Score | Avg t/s | Avg Time (s) | Runs |",
        "|------|-------|----------|-----------|---------|--------------|------|",
    ]

    ranked = sorted(agg.keys(), key=lambda k: -avg(agg[k]["scores"]))
    for rank, k in enumerate(ranked, 1):
        d = agg[k]
        lines.append(
            f"| {rank} | {short_name(k[0])} | {k[1]} | "
            f"{avg(d['scores']):.2f} | {avg(d['speeds']):.1f} | "
            f"{avg(d['times']):.1f} | {len(d['scores'])} |"
        )

    # ── Winner per category ──────────────────────────────────────────────
    for wf, title in [
        ("Direct-DE", "Best Direct Model"),
        ("Translated", "Best Translated Pipeline"),
    ]:
        lines.append(f"\n## {title}\n")
        cands = {k: d for k, d in agg.items() if k[1] == wf}
        if cands:
            best = max(cands.keys(), key=lambda k: avg(cands[k]["scores"]))
            d = cands[best]
            lines.append(
                f"**{short_name(best[0])}** — "
                f"Avg Score: {avg(d['scores']):.2f}/5, "
                f"Avg Speed: {avg(d['speeds']):.1f} t/s"
            )

    # ── Per-level breakdown ──────────────────────────────────────────────
    for level in ("L1-Recall", "L2-Synthesis"):
        lines += [
            f"\n## {level} Breakdown",
            "",
            "| Model | Workflow | Avg Score | Avg t/s |",
            "|-------|----------|-----------|---------|",
        ]
        lv: dict[tuple, dict] = defaultdict(lambda: {"scores": [], "speeds": []})
        for r in valid:
            if r.level == level:
                k = (r.model, r.workflow)
                lv[k]["scores"].append(r.score)
                lv[k]["speeds"].append(r.tokens_per_sec)

        for k in sorted(lv.keys(), key=lambda k: -avg(lv[k]["scores"])):
            d = lv[k]
            lines.append(
                f"| {short_name(k[0])} | {k[1]} | "
                f"{avg(d['scores']):.2f} | {avg(d['speeds']):.1f} |"
            )

    # ── Per-section breakdown ────────────────────────────────────────────
    section_names = sorted(set(r.prompt_section for r in valid))
    if len(section_names) > 1:
        lines.append("\n## Per-Section Breakdown")
        for sec in section_names:
            sec_short = sec.split(":")[-1].strip()
            lines += [
                f"\n### {sec_short}",
                "",
                "| Model | Workflow | Avg Score |",
                "|-------|----------|-----------|",
            ]
            sec_data: dict[tuple, list] = defaultdict(list)
            for r in valid:
                if r.prompt_section == sec:
                    sec_data[(r.model, r.workflow)].append(r.score)
            for k in sorted(sec_data, key=lambda k: -avg(sec_data[k])):
                lines.append(
                    f"| {short_name(k[0])} | {k[1]} | {avg(sec_data[k]):.2f} |"
                )

    SUMMARY_MD.write_text("\n".join(lines), encoding="utf-8")


def write_report(rows: list[BenchmarkRow]):
    """Generate an interactive HTML report with Chart.js visualizations."""

    valid = [r for r in rows if r.score > 0]
    if not valid:
        REPORT_HTML.write_text(
            "<html><body><h1>No valid results</h1></body></html>",
            encoding="utf-8",
        )
        return

    models = sorted(set(r.model for r in valid))
    model_labels = [short_name(m) for m in models]
    workflows = ["Direct-DE", "Translated"]
    levels = ["L1-Recall", "L2-Synthesis"]
    materials = sorted(set(r.material for r in valid))
    sections = sorted(set(r.prompt_section for r in valid))
    section_labels = [s.split(":")[-1].strip() for s in sections]

    table_data = []
    for r in valid:
        table_data.append({
            "model": short_name(r.model),
            "fullModel": r.model,
            "material": r.material,
            "section": r.prompt_section.split(":")[-1].strip(),
            "level": r.level,
            "workflow": r.workflow,
            "gen_time": r.gen_time_s,
            "trans_time": r.trans_time_s,
            "total_time": r.total_time_s,
            "tps": r.tokens_per_sec,
            "score": r.score,
            "reasoning": r.reasoning,
        })

    data_json = json.dumps(table_data)
    models_json = json.dumps(model_labels)
    workflows_json = json.dumps(workflows)
    levels_json = json.dumps(levels)
    materials_json = json.dumps(materials)
    sections_json = json.dumps(section_labels)

    mat_options = "".join(f'<option value="{m}">{m}</option>' for m in materials)
    lvl_options = "".join(f'<option value="{l}">{l}</option>' for l in levels)
    sec_options = "".join(
        f'<option value="{s.split(":")[-1].strip()}">{s.split(":")[-1].strip()}</option>'
        for s in sections
    )
    wf_options = "".join(f'<option value="{w}">{w}</option>' for w in workflows)
    model_options = "".join(
        f'<option value="{short_name(m)}">{short_name(m)}</option>' for m in models
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CLIL Benchmark Report</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #0f1117;
    --surface: #1a1d27;
    --surface2: #232733;
    --border: #2e3347;
    --text: #e4e6f0;
    --text-muted: #8b8fa3;
    --accent: #6c8aff;
    --accent2: #ff9f43;
    --green: #2ed573;
    --yellow: #ffa502;
    --red: #ff4757;
    --purple: #a55eea;
    --cyan: #18dcff;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    min-height: 100vh;
  }}

  .container {{
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }}

  .header {{
    text-align: center;
    padding: 3rem 0 2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
  }}
  .header h1 {{
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--accent), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
  }}
  .header .subtitle {{
    color: var(--text-muted);
    font-size: 0.95rem;
  }}

  .stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
  }}
  .stat-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
  }}
  .stat-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
  }}
  .stat-card .value {{
    font-size: 2rem;
    font-weight: 700;
    color: var(--accent);
  }}
  .stat-card .label {{
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
  }}

  .tabs {{
    display: flex;
    gap: 0.25rem;
    margin-bottom: 2rem;
    border-bottom: 2px solid var(--border);
    overflow-x: auto;
  }}
  .tab {{
    padding: 0.75rem 1.25rem;
    cursor: pointer;
    border: none;
    background: transparent;
    color: var(--text-muted);
    font-size: 0.9rem;
    font-weight: 500;
    border-bottom: 2px solid transparent;
    margin-bottom: -2px;
    transition: all 0.2s;
    white-space: nowrap;
  }}
  .tab:hover {{ color: var(--text); }}
  .tab.active {{
    color: var(--accent);
    border-bottom-color: var(--accent);
  }}
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}

  .chart-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-bottom: 2rem;
  }}
  @media (max-width: 900px) {{
    .chart-grid {{ grid-template-columns: 1fr; }}
  }}
  .chart-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
  }}
  .chart-card h3 {{
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--text-muted);
  }}
  .chart-card canvas {{
    max-height: 380px;
  }}
  .chart-card.full-width {{
    grid-column: 1 / -1;
  }}

  .leaderboard {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }}
  .leaderboard h3 {{
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }}
  .podium {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-bottom: 1.5rem;
  }}
  .podium-item {{
    background: var(--surface2);
    border-radius: 10px;
    padding: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    border-left: 4px solid var(--accent);
    transition: transform 0.15s;
  }}
  .podium-item:hover {{ transform: scale(1.02); }}
  .podium-item.gold {{ border-left-color: #ffd700; }}
  .podium-item.silver {{ border-left-color: #c0c0c0; }}
  .podium-item.bronze {{ border-left-color: #cd7f32; }}
  .podium-rank {{
    font-size: 1.8rem;
    font-weight: 800;
    min-width: 2.5rem;
    text-align: center;
  }}
  .podium-item.gold .podium-rank {{ color: #ffd700; }}
  .podium-item.silver .podium-rank {{ color: #c0c0c0; }}
  .podium-item.bronze .podium-rank {{ color: #cd7f32; }}
  .podium-info {{ flex: 1; }}
  .podium-model {{ font-weight: 600; font-size: 1rem; }}
  .podium-detail {{ font-size: 0.8rem; color: var(--text-muted); }}
  .podium-score {{
    font-size: 1.6rem;
    font-weight: 700;
  }}

  .filters {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    align-items: center;
  }}
  .filters label {{
    font-size: 0.85rem;
    color: var(--text-muted);
  }}
  .filters select {{
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--text);
    font-size: 0.9rem;
    cursor: pointer;
    outline: none;
    transition: border-color 0.2s;
  }}
  .filters select:focus {{ border-color: var(--accent); }}

  .table-wrap {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: auto;
    max-height: 600px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
  }}
  th {{
    background: var(--surface2);
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 600;
    color: var(--text-muted);
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
    position: sticky;
    top: 0;
    z-index: 1;
  }}
  th:hover {{ color: var(--text); }}
  th .sort-arrow {{ margin-left: 4px; opacity: 0.4; }}
  th.sorted .sort-arrow {{ opacity: 1; color: var(--accent); }}
  td {{
    padding: 0.6rem 1rem;
    border-top: 1px solid var(--border);
    white-space: nowrap;
  }}
  tr:hover td {{ background: rgba(108, 138, 255, 0.05); }}
  td.reasoning-cell {{
    white-space: normal;
    max-width: 350px;
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.4;
  }}

  .score-badge {{
    display: inline-block;
    padding: 0.2rem 0.65rem;
    border-radius: 6px;
    font-weight: 700;
    font-size: 0.85rem;
  }}
  .score-1 {{ background: rgba(255,71,87,0.2); color: var(--red); }}
  .score-2 {{ background: rgba(255,71,87,0.15); color: #ff6b7a; }}
  .score-3 {{ background: rgba(255,165,2,0.2); color: var(--yellow); }}
  .score-4 {{ background: rgba(46,213,115,0.15); color: #5adc8f; }}
  .score-5 {{ background: rgba(46,213,115,0.25); color: var(--green); }}

  .model-cards {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }}
  .model-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    transition: transform 0.2s;
  }}
  .model-card:hover {{ transform: translateY(-2px); }}
  .model-card h4 {{
    font-size: 1.1rem;
    margin-bottom: 1rem;
    color: var(--accent);
  }}
  .model-stat-row {{
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
  }}
  .model-stat-row:last-child {{ border-bottom: none; }}
  .model-stat-label {{ color: var(--text-muted); }}
  .model-stat-value {{ font-weight: 600; }}

  .heatmap-wrap {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    overflow-x: auto;
  }}
  .heatmap-wrap h3 {{
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }}
  .heatmap {{
    display: grid;
    gap: 3px;
    font-size: 0.8rem;
  }}
  .heatmap-cell {{
    padding: 0.5rem;
    text-align: center;
    border-radius: 4px;
    font-weight: 600;
    transition: transform 0.1s;
  }}
  .heatmap-cell:hover {{ transform: scale(1.1); z-index: 1; }}
  .heatmap-header {{
    background: var(--surface2);
    color: var(--text-muted);
    font-weight: 600;
    padding: 0.5rem;
    text-align: center;
    border-radius: 4px;
    font-size: 0.75rem;
  }}

  /* ── Radar / Skill Chart ─────────────────────────────────── */
  .radar-section {{
    margin-bottom: 2rem;
  }}
  .radar-controls {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }}
  .radar-toggle {{
    padding: 0.5rem 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--surface2);
    color: var(--text-muted);
    cursor: pointer;
    font-size: 0.85rem;
    transition: all 0.2s;
  }}
  .radar-toggle.active {{
    border-color: var(--accent);
    color: var(--text);
    background: rgba(108,138,255,0.15);
  }}
  .radar-toggle:hover {{ border-color: var(--accent); color: var(--text); }}

  /* ── Head-to-Head ────────────────────────────────────────── */
  .h2h-grid {{
    display: grid;
    grid-template-columns: 1fr auto 1fr;
    gap: 2rem;
    align-items: start;
  }}
  @media (max-width: 900px) {{
    .h2h-grid {{ grid-template-columns: 1fr; }}
  }}
  .h2h-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
  }}
  .h2h-vs {{
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 800;
    color: var(--text-muted);
    padding-top: 3rem;
  }}
  .h2h-bar {{
    display: flex;
    height: 28px;
    border-radius: 6px;
    overflow: hidden;
    margin: 0.4rem 0;
  }}
  .h2h-bar-left {{
    transition: width 0.4s ease;
  }}
  .h2h-bar-right {{
    transition: width 0.4s ease;
  }}
  .h2h-metric {{
    display: flex;
    justify-content: space-between;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
  }}
  .h2h-metric:last-child {{ border-bottom: none; }}
  .h2h-metric .winner {{ color: var(--green); font-weight: 700; }}
  .h2h-metric .loser {{ color: var(--text-muted); }}

  .footer {{
    text-align: center;
    padding: 2rem 0;
    color: var(--text-muted);
    font-size: 0.8rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
  }}

  .row-count {{
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
  }}

  .section-title {{
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
  }}

  .donut-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }}
  .donut-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
  }}
  .donut-card h4 {{
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
  }}
  .donut-card canvas {{ max-height: 200px; }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>CLIL Benchmark Report</h1>
    <div class="subtitle">
      Generated: {time.strftime('%Y-%m-%d %H:%M')} &middot;
      {len(valid)} valid runs across {len(models)} models &middot;
      {len(materials)} materials &middot; {len(sections)} exercise types
    </div>
  </div>

  <div class="stats-grid" id="statsGrid"></div>

  <div class="tabs">
    <button class="tab active" onclick="showTab('overview',this)">Overview</button>
    <button class="tab" onclick="showTab('radar',this)">Skill Radar</button>
    <button class="tab" onclick="showTab('h2h',this)">Head-to-Head</button>
    <button class="tab" onclick="showTab('comparison',this)">Model Cards</button>
    <button class="tab" onclick="showTab('heatmap',this)">Heatmap</button>
    <button class="tab" onclick="showTab('charts',this)">Detailed Charts</button>
    <button class="tab" onclick="showTab('details',this)">All Results</button>
  </div>

  <!-- ══ TAB: Overview ════════════════════════════════════════ -->
  <div id="overview" class="tab-content active">
    <div class="leaderboard">
      <h3>Leaderboard &mdash; Overall Average Score</h3>
      <div class="podium" id="podium"></div>
    </div>
    <div class="chart-grid">
      <div class="chart-card">
        <h3>Average Score by Model &amp; Workflow</h3>
        <canvas id="scoreChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Average Total Time by Model &amp; Workflow</h3>
        <canvas id="timeChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Tokens/sec by Model</h3>
        <canvas id="tpsChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Score by Cognitive Level</h3>
        <canvas id="levelChart"></canvas>
      </div>
    </div>
    <div class="section-title">Score Distribution per Model</div>
    <div class="donut-grid" id="donutGrid"></div>
    <div class="chart-grid">
      <div class="chart-card full-width">
        <h3>Workflow Advantage &mdash; Direct-DE vs Translated (per model)</h3>
        <canvas id="wfAdvChart"></canvas>
      </div>
    </div>
  </div>

  <!-- ══ TAB: Skill Radar ═════════════════════════════════════ -->
  <div id="radar" class="tab-content">
    <div class="radar-section">
      <div class="section-title">Model Skill Radar &mdash; click models to toggle</div>
      <div class="radar-controls" id="radarToggles"></div>
      <div class="chart-grid">
        <div class="chart-card full-width">
          <h3>Skills by Exercise Type (avg score per section)</h3>
          <canvas id="radarSections"></canvas>
        </div>
      </div>
      <div class="chart-grid">
        <div class="chart-card">
          <h3>Overall Attributes Radar</h3>
          <canvas id="radarOverall"></canvas>
        </div>
        <div class="chart-card">
          <h3>Per-Material Proficiency</h3>
          <canvas id="radarMaterials"></canvas>
        </div>
      </div>
      <div class="chart-grid">
        <div class="chart-card">
          <h3>Workflow Comparison Radar</h3>
          <canvas id="radarWorkflow"></canvas>
        </div>
        <div class="chart-card">
          <h3>Cognitive Level Radar</h3>
          <canvas id="radarLevels"></canvas>
        </div>
      </div>
    </div>
  </div>

  <!-- ══ TAB: Head-to-Head ════════════════════════════════════ -->
  <div id="h2h" class="tab-content">
    <div class="section-title">Head-to-Head Comparison</div>
    <div class="filters">
      <label>Model A:</label>
      <select id="h2hA" onchange="buildH2H()">
        {model_options}
      </select>
      <label>Model B:</label>
      <select id="h2hB" onchange="buildH2H()">
        {model_options}
      </select>
    </div>
    <div class="chart-grid">
      <div class="chart-card full-width">
        <canvas id="h2hRadar"></canvas>
      </div>
    </div>
    <div class="h2h-grid" id="h2hDetails"></div>
    <div class="chart-grid">
      <div class="chart-card">
        <h3>Score Comparison by Section</h3>
        <canvas id="h2hSections"></canvas>
      </div>
      <div class="chart-card">
        <h3>Speed Comparison by Section</h3>
        <canvas id="h2hSpeed"></canvas>
      </div>
    </div>
  </div>

  <!-- ══ TAB: Model Cards ═════════════════════════════════════ -->
  <div id="comparison" class="tab-content">
    <div class="model-cards" id="modelCards"></div>
  </div>

  <!-- ══ TAB: Heatmap ═════════════════════════════════════════ -->
  <div id="heatmap" class="tab-content">
    <div class="filters">
      <label>Workflow:</label>
      <select id="heatmapWf" onchange="buildHeatmap()">
        <option value="">All</option>
        {wf_options}
      </select>
      <label>Level:</label>
      <select id="heatmapLvl" onchange="buildHeatmap()">
        <option value="">All</option>
        {lvl_options}
      </select>
    </div>
    <div class="heatmap-wrap">
      <h3>Score Heatmap &mdash; Model vs Material &times; Section</h3>
      <div class="heatmap" id="heatmapGrid"></div>
    </div>
  </div>

  <!-- ══ TAB: Detailed Charts ═════════════════════════════════ -->
  <div id="charts" class="tab-content">
    <div class="chart-grid">
      <div class="chart-card full-width">
        <h3>Score Distribution (histogram)</h3>
        <canvas id="boxChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Scores by Material</h3>
        <canvas id="matChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Scores by Section</h3>
        <canvas id="secChart"></canvas>
      </div>
      <div class="chart-card full-width">
        <h3>Time vs Score (scatter)</h3>
        <canvas id="scatterChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Average Score Trend by Material (line)</h3>
        <canvas id="trendChart"></canvas>
      </div>
      <div class="chart-card">
        <h3>Generation vs Translation Time (stacked)</h3>
        <canvas id="stackedTimeChart"></canvas>
      </div>
    </div>
  </div>

  <!-- ══ TAB: All Results ═════════════════════════════════════ -->
  <div id="details" class="tab-content">
    <div class="filters">
      <label>Model:</label>
      <select id="filterModel" onchange="filterTable()">
        <option value="">All</option>
        {model_options}
      </select>
      <label>Material:</label>
      <select id="filterMaterial" onchange="filterTable()">
        <option value="">All</option>
        {mat_options}
      </select>
      <label>Level:</label>
      <select id="filterLevel" onchange="filterTable()">
        <option value="">All</option>
        {lvl_options}
      </select>
      <label>Section:</label>
      <select id="filterSection" onchange="filterTable()">
        <option value="">All</option>
        {sec_options}
      </select>
      <label>Workflow:</label>
      <select id="filterWorkflow" onchange="filterTable()">
        <option value="">All</option>
        {wf_options}
      </select>
      <label>Min Score:</label>
      <select id="filterMinScore" onchange="filterTable()">
        <option value="0">Any</option>
        <option value="1">1+</option><option value="2">2+</option>
        <option value="3">3+</option><option value="4">4+</option><option value="5">5</option>
      </select>
    </div>
    <div class="row-count" id="rowCount"></div>
    <div class="table-wrap">
      <table>
        <thead><tr>
          <th onclick="sortTable(0)">Model <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(1)">Material <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(2)">Section <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(3)">Level <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(4)">Workflow <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(5)">Gen (s) <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(6)">Trans (s) <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(7)">Total (s) <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(8)">t/s <span class="sort-arrow">&#9650;</span></th>
          <th onclick="sortTable(9)">Score <span class="sort-arrow">&#9650;</span></th>
          <th>Reasoning</th>
        </tr></thead>
        <tbody id="tableBody"></tbody>
      </table>
    </div>
  </div>

  <div class="footer">
    CLIL Benchmark Report &middot; Generated {time.strftime('%Y-%m-%d %H:%M')} &middot;
    {len(valid)} runs &middot; {len(models)} models
  </div>
</div>

<script>
// ═══════════════════════════════════════════════════════════════
// DATA
// ═══════════════════════════════════════════════════════════════
const DATA = {data_json};
const MODELS = {models_json};
const WORKFLOWS = {workflows_json};
const LEVELS = {levels_json};
const MATERIALS = {materials_json};
const SECTIONS = {sections_json};

const COLORS = {{
  'Direct-DE': '#6c8aff',
  'Translated': '#ff9f43',
  'L1-Recall': '#2ed573',
  'L2-Synthesis': '#a55eea',
}};
const MODEL_COLORS = ['#6c8aff','#ff9f43','#2ed573','#ff4757','#a55eea','#18dcff','#ffd700','#ff6b7a'];
const MODEL_COLORS_ALPHA = MODEL_COLORS.map(c => c + '33');

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════
function avg(arr) {{ return arr.length ? arr.reduce((a,b)=>a+b,0)/arr.length : 0; }}
function stdev(arr) {{
  if (arr.length < 2) return 0;
  const m = avg(arr);
  return Math.sqrt(arr.reduce((s,v) => s + (v-m)**2, 0) / (arr.length-1));
}}
function scoreColor(s) {{
  if (s >= 4.5) return 'var(--green)';
  if (s >= 3.5) return '#5adc8f';
  if (s >= 2.5) return 'var(--yellow)';
  return 'var(--red)';
}}
function heatColor(score) {{
  if (score === 0) return 'var(--surface2)';
  const colors = ['','rgba(255,71,87,0.35)','rgba(255,71,87,0.2)','rgba(255,165,2,0.25)','rgba(46,213,115,0.2)','rgba(46,213,115,0.4)'];
  return colors[Math.round(score)] || 'var(--surface2)';
}}
function normalize(val, min, max) {{ return max === min ? 0.5 : (val - min) / (max - min); }}

Chart.defaults.color = '#8b8fa3';
Chart.defaults.borderColor = '#2e3347';
Chart.defaults.font.family = "'Inter', system-ui, sans-serif";

// ═══════════════════════════════════════════════════════════════
// TAB SWITCHING
// ═══════════════════════════════════════════════════════════════
function showTab(id, btn) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}}

// ═══════════════════════════════════════════════════════════════
// STATS CARDS
// ═══════════════════════════════════════════════════════════════
(function buildStats() {{
  const grid = document.getElementById('statsGrid');
  const avgScore = avg(DATA.map(r=>r.score));
  const avgTime = avg(DATA.map(r=>r.total_time));
  const avgTps = avg(DATA.map(r=>r.tps));
  const maxScore = Math.max(...DATA.map(r=>r.score));
  const bestModel = MODELS.reduce((best,m) => {{
    const s = avg(DATA.filter(r=>r.model===m).map(r=>r.score));
    return s > best.s ? {{m, s}} : best;
  }}, {{m:'', s:0}});
  const fastestModel = MODELS.reduce((best,m) => {{
    const s = avg(DATA.filter(r=>r.model===m).map(r=>r.tps));
    return s > best.s ? {{m, s}} : best;
  }}, {{m:'', s:0}});

  const stats = [
    {{ value: DATA.length, label: 'Total Runs' }},
    {{ value: MODELS.length, label: 'Models Tested' }},
    {{ value: SECTIONS.length, label: 'Exercise Types' }},
    {{ value: avgScore.toFixed(2) + '/5', label: 'Avg Score' }},
    {{ value: avgTime.toFixed(1) + 's', label: 'Avg Time' }},
    {{ value: avgTps.toFixed(1), label: 'Avg Tokens/sec' }},
    {{ value: bestModel.m, label: 'Highest Quality' }},
    {{ value: fastestModel.m, label: 'Fastest Model' }},
  ];
  grid.innerHTML = stats.map(s =>
    `<div class="stat-card"><div class="value">${{s.value}}</div><div class="label">${{s.label}}</div></div>`
  ).join('');
}})();

// ═══════════════════════════════════════════════════════════════
// PODIUM / LEADERBOARD
// ═══════════════════════════════════════════════════════════════
(function buildPodium() {{
  const ranked = MODELS.map(m => ({{
    model: m,
    score: avg(DATA.filter(r=>r.model===m).map(r=>r.score)),
    speed: avg(DATA.filter(r=>r.model===m).map(r=>r.tps)),
    time:  avg(DATA.filter(r=>r.model===m).map(r=>r.total_time)),
    runs:  DATA.filter(r=>r.model===m).length,
    consistency: 5 - stdev(DATA.filter(r=>r.model===m).map(r=>r.score)),
  }})).sort((a,b) => b.score - a.score);

  const medals = ['gold','silver','bronze'];
  document.getElementById('podium').innerHTML = ranked.map((r, i) =>
    `<div class="podium-item ${{medals[i]||''}}">
      <div class="podium-rank">#${{i+1}}</div>
      <div class="podium-info">
        <div class="podium-model">${{r.model}}</div>
        <div class="podium-detail">${{r.runs}} runs &middot; ${{r.speed.toFixed(1)}} t/s &middot; ${{r.time.toFixed(1)}}s avg</div>
      </div>
      <div class="podium-score" style="color:${{scoreColor(r.score)}}">${{r.score.toFixed(2)}}</div>
    </div>`
  ).join('');
}})();

// ═══════════════════════════════════════════════════════════════
// OVERVIEW CHARTS
// ═══════════════════════════════════════════════════════════════
function avgByMW(workflow, field) {{
  return MODELS.map(m => {{
    const rows = DATA.filter(r => r.model===m && r.workflow===workflow);
    return rows.length ? avg(rows.map(r=>r[field])) : 0;
  }});
}}

new Chart(document.getElementById('scoreChart'), {{
  type: 'bar',
  data: {{
    labels: MODELS,
    datasets: WORKFLOWS.map(wf => ({{
      label: wf, data: avgByMW(wf,'score'),
      backgroundColor: COLORS[wf], borderRadius: 4,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }}, tooltip: {{ mode: 'index' }} }},
    scales: {{ y: {{ beginAtZero: true, max: 5, title: {{ display: true, text: 'Avg Score (1-5)' }} }} }}
  }}
}});

new Chart(document.getElementById('timeChart'), {{
  type: 'bar',
  data: {{
    labels: MODELS,
    datasets: WORKFLOWS.map(wf => ({{
      label: wf, data: avgByMW(wf,'total_time'),
      backgroundColor: COLORS[wf], borderRadius: 4,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Avg Time (s)' }} }} }}
  }}
}});

new Chart(document.getElementById('tpsChart'), {{
  type: 'bar',
  data: {{
    labels: MODELS,
    datasets: [{{
      label: 'Tokens/sec',
      data: MODELS.map(m => avg(DATA.filter(r=>r.model===m).map(r=>r.tps))),
      backgroundColor: MODEL_COLORS.slice(0, MODELS.length),
      borderRadius: 4,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Tokens/sec' }} }} }}
  }}
}});

new Chart(document.getElementById('levelChart'), {{
  type: 'bar',
  data: {{
    labels: MODELS,
    datasets: LEVELS.map(lvl => ({{
      label: lvl,
      data: MODELS.map(m => avg(DATA.filter(r=>r.model===m && r.level===lvl).map(r=>r.score))),
      backgroundColor: COLORS[lvl], borderRadius: 4,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ y: {{ beginAtZero: true, max: 5, title: {{ display: true, text: 'Avg Score' }} }} }}
  }}
}});

// Donut charts per model (score distribution)
(function buildDonuts() {{
  const grid = document.getElementById('donutGrid');
  MODELS.forEach((m, i) => {{
    const card = document.createElement('div');
    card.className = 'donut-card';
    card.innerHTML = `<h4 style="color:${{MODEL_COLORS[i]}}">${{m}}</h4><canvas id="donut${{i}}"></canvas>`;
    grid.appendChild(card);
  }});
  MODELS.forEach((m, i) => {{
    const counts = [1,2,3,4,5].map(s => DATA.filter(r=>r.model===m && r.score===s).length);
    new Chart(document.getElementById('donut'+i), {{
      type: 'doughnut',
      data: {{
        labels: ['1/5','2/5','3/5','4/5','5/5'],
        datasets: [{{ data: counts, backgroundColor: ['#ff4757','#ff6b7a','#ffa502','#5adc8f','#2ed573'], borderWidth: 0 }}]
      }},
      options: {{
        responsive: true,
        cutout: '55%',
        plugins: {{
          legend: {{ position: 'bottom', labels: {{ boxWidth: 12, padding: 8, font: {{ size: 11 }} }} }},
          tooltip: {{ callbacks: {{ label: ctx => ctx.label + ': ' + ctx.raw + ' runs' }} }}
        }}
      }}
    }});
  }});
}})();

// Workflow advantage chart
new Chart(document.getElementById('wfAdvChart'), {{
  type: 'bar',
  data: {{
    labels: MODELS,
    datasets: [{{
      label: 'Direct-DE advantage (positive = Direct-DE better)',
      data: MODELS.map(m => {{
        const de = avg(DATA.filter(r=>r.model===m && r.workflow==='Direct-DE').map(r=>r.score));
        const tr = avg(DATA.filter(r=>r.model===m && r.workflow==='Translated').map(r=>r.score));
        return +(de - tr).toFixed(3);
      }}),
      backgroundColor: MODELS.map(m => {{
        const de = avg(DATA.filter(r=>r.model===m && r.workflow==='Direct-DE').map(r=>r.score));
        const tr = avg(DATA.filter(r=>r.model===m && r.workflow==='Translated').map(r=>r.score));
        return de >= tr ? 'rgba(108,138,255,0.6)' : 'rgba(255,159,67,0.6)';
      }}),
      borderRadius: 4,
    }}]
  }},
  options: {{
    responsive: true,
    indexAxis: 'y',
    plugins: {{ legend: {{ display: false }},
      tooltip: {{ callbacks: {{ label: ctx => {{
        const v = ctx.raw;
        return v >= 0 ? `Direct-DE better by ${{v.toFixed(2)}}` : `Translated better by ${{Math.abs(v).toFixed(2)}}`;
      }} }} }}
    }},
    scales: {{ x: {{ title: {{ display: true, text: 'Score difference' }} }} }}
  }}
}});

// ═══════════════════════════════════════════════════════════════
// RADAR / SKILL CHARTS
// ═══════════════════════════════════════════════════════════════
const radarState = {{}};
MODELS.forEach((m,i) => radarState[m] = i < 3);

const radarCharts = {{}};

function buildRadarToggles() {{
  const container = document.getElementById('radarToggles');
  container.innerHTML = MODELS.map((m, i) =>
    `<button class="radar-toggle ${{radarState[m]?'active':''}}" style="border-color:${{radarState[m]?MODEL_COLORS[i]:''}}"
      onclick="toggleRadarModel('${{m}}',${{i}},this)">${{m}}</button>`
  ).join('');
}}

function toggleRadarModel(m, i, btn) {{
  radarState[m] = !radarState[m];
  btn.classList.toggle('active');
  btn.style.borderColor = radarState[m] ? MODEL_COLORS[i] : '';
  updateRadars();
}}

function getActiveModels() {{ return MODELS.filter(m => radarState[m]); }}

function radarDatasets(labelsArr, dataFn) {{
  return getActiveModels().map(m => {{
    const i = MODELS.indexOf(m);
    return {{
      label: m,
      data: labelsArr.map(l => dataFn(m, l)),
      borderColor: MODEL_COLORS[i],
      backgroundColor: MODEL_COLORS_ALPHA[i],
      pointBackgroundColor: MODEL_COLORS[i],
      pointRadius: 4,
      pointHoverRadius: 7,
      borderWidth: 2,
      fill: true,
    }};
  }});
}}

const radarOpts = {{
  responsive: true,
  plugins: {{ legend: {{ position: 'top', labels: {{ boxWidth: 14 }} }} }},
  scales: {{ r: {{
    beginAtZero: true, max: 5,
    ticks: {{ stepSize: 1, color: '#8b8fa3', backdropColor: 'transparent' }},
    grid: {{ color: '#2e3347' }},
    pointLabels: {{ color: '#e4e6f0', font: {{ size: 12 }} }},
    angleLines: {{ color: '#2e3347' }}
  }} }},
  animation: {{ duration: 400 }}
}};

function buildRadar(canvasId, labels, dataFn) {{
  const ctx = document.getElementById(canvasId);
  if (radarCharts[canvasId]) radarCharts[canvasId].destroy();
  radarCharts[canvasId] = new Chart(ctx, {{
    type: 'radar',
    data: {{ labels, datasets: radarDatasets(labels, dataFn) }},
    options: radarOpts
  }});
}}

function updateRadars() {{
  // Section skills
  buildRadar('radarSections', SECTIONS, (m, sec) =>
    avg(DATA.filter(r=>r.model===m && r.section===sec).map(r=>r.score))
  );

  // Overall attributes
  const allTps = DATA.map(r=>r.tps);
  const maxTps = Math.max(...allTps);
  const allTimes = DATA.map(r=>r.total_time);
  const maxTime = Math.max(...allTimes);
  const attrLabels = ['Quality', 'Speed', 'Efficiency', 'L1-Recall', 'L2-Synthesis', 'Consistency'];
  buildRadar('radarOverall', attrLabels, (m, attr) => {{
    const rows = DATA.filter(r=>r.model===m);
    switch(attr) {{
      case 'Quality': return avg(rows.map(r=>r.score));
      case 'Speed': return normalize(avg(rows.map(r=>r.tps)), 0, maxTps) * 5;
      case 'Efficiency': return (1 - normalize(avg(rows.map(r=>r.total_time)), 0, maxTime)) * 5;
      case 'L1-Recall': return avg(rows.filter(r=>r.level==='L1-Recall').map(r=>r.score));
      case 'L2-Synthesis': return avg(rows.filter(r=>r.level==='L2-Synthesis').map(r=>r.score));
      case 'Consistency': return Math.max(0, 5 - stdev(rows.map(r=>r.score)) * 2);
      default: return 0;
    }}
  }});

  // Materials
  buildRadar('radarMaterials', MATERIALS, (m, mat) =>
    avg(DATA.filter(r=>r.model===m && r.material===mat).map(r=>r.score))
  );

  // Workflow
  buildRadar('radarWorkflow', ['Direct-DE Quality','Translated Quality','Direct-DE Speed','Translated Speed'], (m, lbl) => {{
    const parts = lbl.split(' ');
    const wf = parts[0]; const metric = parts[1];
    const rows = DATA.filter(r=>r.model===m && r.workflow===(wf==='Direct-DE'?'Direct-DE':'Translated'));
    if (metric === 'Quality') return avg(rows.map(r=>r.score));
    return normalize(avg(rows.map(r=>r.tps)), 0, Math.max(...DATA.map(r=>r.tps))) * 5;
  }});

  // Cognitive levels detailed
  const lvlLabels = [];
  LEVELS.forEach(l => WORKFLOWS.forEach(w => lvlLabels.push(l + ' / ' + w)));
  buildRadar('radarLevels', lvlLabels, (m, lbl) => {{
    const [lvl, wf] = lbl.split(' / ');
    return avg(DATA.filter(r=>r.model===m && r.level===lvl && r.workflow===wf).map(r=>r.score));
  }});
}}

buildRadarToggles();
updateRadars();

// ═══════════════════════════════════════════════════════════════
// HEAD-TO-HEAD COMPARISON
// ═══════════════════════════════════════════════════════════════
let h2hRadarChart = null, h2hSecChart = null, h2hSpdChart = null;

// Select second model by default if available
if (MODELS.length > 1) document.getElementById('h2hB').selectedIndex = 1;

function buildH2H() {{
  const mA = document.getElementById('h2hA').value;
  const mB = document.getElementById('h2hB').value;
  const rowsA = DATA.filter(r=>r.model===mA);
  const rowsB = DATA.filter(r=>r.model===mB);
  const iA = MODELS.indexOf(mA), iB = MODELS.indexOf(mB);

  // Radar overlay
  const attrs = ['Quality','Speed','L1-Recall','L2-Synthesis','Direct-DE','Translated','Consistency'];
  const maxTps = Math.max(...DATA.map(r=>r.tps));
  function attrVal(rows, attr) {{
    switch(attr) {{
      case 'Quality': return avg(rows.map(r=>r.score));
      case 'Speed': return normalize(avg(rows.map(r=>r.tps)), 0, maxTps) * 5;
      case 'L1-Recall': return avg(rows.filter(r=>r.level==='L1-Recall').map(r=>r.score));
      case 'L2-Synthesis': return avg(rows.filter(r=>r.level==='L2-Synthesis').map(r=>r.score));
      case 'Direct-DE': return avg(rows.filter(r=>r.workflow==='Direct-DE').map(r=>r.score));
      case 'Translated': return avg(rows.filter(r=>r.workflow==='Translated').map(r=>r.score));
      case 'Consistency': return Math.max(0, 5 - stdev(rows.map(r=>r.score)) * 2);
      default: return 0;
    }}
  }}

  const ctx = document.getElementById('h2hRadar');
  if (h2hRadarChart) h2hRadarChart.destroy();
  h2hRadarChart = new Chart(ctx, {{
    type: 'radar',
    data: {{
      labels: attrs,
      datasets: [
        {{ label: mA, data: attrs.map(a=>attrVal(rowsA,a)), borderColor: MODEL_COLORS[iA], backgroundColor: MODEL_COLORS_ALPHA[iA], pointBackgroundColor: MODEL_COLORS[iA], fill: true, borderWidth: 2, pointRadius: 4 }},
        {{ label: mB, data: attrs.map(a=>attrVal(rowsB,a)), borderColor: MODEL_COLORS[iB], backgroundColor: MODEL_COLORS_ALPHA[iB], pointBackgroundColor: MODEL_COLORS[iB], fill: true, borderWidth: 2, pointRadius: 4 }}
      ]
    }},
    options: {{ ...radarOpts, plugins: {{ ...radarOpts.plugins, title: {{ display: true, text: mA + ' vs ' + mB, font: {{ size: 16 }}, color: '#e4e6f0' }} }} }}
  }});

  // Metric detail cards
  const metrics = [
    ['Avg Score', avg(rowsA.map(r=>r.score)).toFixed(2), avg(rowsB.map(r=>r.score)).toFixed(2), true],
    ['Avg Tokens/sec', avg(rowsA.map(r=>r.tps)).toFixed(1), avg(rowsB.map(r=>r.tps)).toFixed(1), true],
    ['Avg Time (s)', avg(rowsA.map(r=>r.total_time)).toFixed(1), avg(rowsB.map(r=>r.total_time)).toFixed(1), false],
    ['L1-Recall Score', avg(rowsA.filter(r=>r.level==='L1-Recall').map(r=>r.score)).toFixed(2), avg(rowsB.filter(r=>r.level==='L1-Recall').map(r=>r.score)).toFixed(2), true],
    ['L2-Synthesis Score', avg(rowsA.filter(r=>r.level==='L2-Synthesis').map(r=>r.score)).toFixed(2), avg(rowsB.filter(r=>r.level==='L2-Synthesis').map(r=>r.score)).toFixed(2), true],
    ['Direct-DE Score', avg(rowsA.filter(r=>r.workflow==='Direct-DE').map(r=>r.score)).toFixed(2), avg(rowsB.filter(r=>r.workflow==='Direct-DE').map(r=>r.score)).toFixed(2), true],
    ['Translated Score', avg(rowsA.filter(r=>r.workflow==='Translated').map(r=>r.score)).toFixed(2), avg(rowsB.filter(r=>r.workflow==='Translated').map(r=>r.score)).toFixed(2), true],
    ['Consistency', (5-stdev(rowsA.map(r=>r.score))*2).toFixed(2), (5-stdev(rowsB.map(r=>r.score))*2).toFixed(2), true],
  ];

  let winsA = 0, winsB = 0;
  metrics.forEach(([_,a,b,higher]) => {{
    const va = parseFloat(a), vb = parseFloat(b);
    if (higher ? va > vb : va < vb) winsA++;
    else if (higher ? vb > va : vb < va) winsB++;
  }});

  const detailsEl = document.getElementById('h2hDetails');
  detailsEl.innerHTML = `
    <div class="h2h-card">
      <h4 style="color:${{MODEL_COLORS[iA]}}">${{mA}}</h4>
      <div style="font-size:2.5rem;font-weight:800;color:var(--green);margin:0.5rem 0">${{winsA}}</div>
      <div style="color:var(--text-muted)">categories won</div>
      ${{metrics.map(([label,a,b,higher]) => {{
        const va = parseFloat(a), vb = parseFloat(b);
        const aWins = higher ? va > vb : va < vb;
        return `<div class="h2h-metric"><span>${{label}}</span><span class="${{aWins?'winner':'loser'}}">${{a}}</span></div>`;
      }}).join('')}}
    </div>
    <div class="h2h-vs">VS</div>
    <div class="h2h-card">
      <h4 style="color:${{MODEL_COLORS[iB]}}">${{mB}}</h4>
      <div style="font-size:2.5rem;font-weight:800;color:var(--green);margin:0.5rem 0">${{winsB}}</div>
      <div style="color:var(--text-muted)">categories won</div>
      ${{metrics.map(([label,a,b,higher]) => {{
        const va = parseFloat(a), vb = parseFloat(b);
        const bWins = higher ? vb > va : vb < va;
        return `<div class="h2h-metric"><span>${{label}}</span><span class="${{bWins?'winner':'loser'}}">${{b}}</span></div>`;
      }}).join('')}}
    </div>`;

  // Section comparison bars
  const ctxSec = document.getElementById('h2hSections');
  if (h2hSecChart) h2hSecChart.destroy();
  h2hSecChart = new Chart(ctxSec, {{
    type: 'bar',
    data: {{
      labels: SECTIONS,
      datasets: [
        {{ label: mA, data: SECTIONS.map(s=>avg(rowsA.filter(r=>r.section===s).map(r=>r.score))), backgroundColor: MODEL_COLORS[iA], borderRadius: 4 }},
        {{ label: mB, data: SECTIONS.map(s=>avg(rowsB.filter(r=>r.section===s).map(r=>r.score))), backgroundColor: MODEL_COLORS[iB], borderRadius: 4 }}
      ]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true, max: 5 }} }} }}
  }});

  const ctxSpd = document.getElementById('h2hSpeed');
  if (h2hSpdChart) h2hSpdChart.destroy();
  h2hSpdChart = new Chart(ctxSpd, {{
    type: 'bar',
    data: {{
      labels: SECTIONS,
      datasets: [
        {{ label: mA, data: SECTIONS.map(s=>avg(rowsA.filter(r=>r.section===s).map(r=>r.tps))), backgroundColor: MODEL_COLORS[iA], borderRadius: 4 }},
        {{ label: mB, data: SECTIONS.map(s=>avg(rowsB.filter(r=>r.section===s).map(r=>r.tps))), backgroundColor: MODEL_COLORS[iB], borderRadius: 4 }}
      ]
    }},
    options: {{ responsive: true, scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 't/s' }} }} }} }}
  }});
}}
buildH2H();

// ═══════════════════════════════════════════════════════════════
// MODEL COMPARISON CARDS
// ═══════════════════════════════════════════════════════════════
(function buildModelCards() {{
  const cards = document.getElementById('modelCards');
  cards.innerHTML = MODELS.map((m, i) => {{
    const rows = DATA.filter(r=>r.model===m);
    const de = rows.filter(r=>r.workflow==='Direct-DE');
    const tr = rows.filter(r=>r.workflow==='Translated');
    const l1 = rows.filter(r=>r.level==='L1-Recall');
    const l2 = rows.filter(r=>r.level==='L2-Synthesis');
    const con = Math.max(0, 5 - stdev(rows.map(r=>r.score)) * 2);
    return `<div class="model-card">
      <h4 style="color:${{MODEL_COLORS[i]}}">${{m}}</h4>
      <div class="model-stat-row"><span class="model-stat-label">Total Runs</span><span class="model-stat-value">${{rows.length}}</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Overall Avg Score</span><span class="model-stat-value" style="color:${{scoreColor(avg(rows.map(r=>r.score)))}}">${{avg(rows.map(r=>r.score)).toFixed(2)}}/5</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Direct-DE Score</span><span class="model-stat-value">${{de.length ? avg(de.map(r=>r.score)).toFixed(2) : 'N/A'}}</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Translated Score</span><span class="model-stat-value">${{tr.length ? avg(tr.map(r=>r.score)).toFixed(2) : 'N/A'}}</span></div>
      <div class="model-stat-row"><span class="model-stat-label">L1-Recall Avg</span><span class="model-stat-value">${{l1.length ? avg(l1.map(r=>r.score)).toFixed(2) : 'N/A'}}</span></div>
      <div class="model-stat-row"><span class="model-stat-label">L2-Synthesis Avg</span><span class="model-stat-value">${{l2.length ? avg(l2.map(r=>r.score)).toFixed(2) : 'N/A'}}</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Consistency</span><span class="model-stat-value">${{con.toFixed(2)}}/5</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Avg Tokens/sec</span><span class="model-stat-value">${{avg(rows.map(r=>r.tps)).toFixed(1)}}</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Avg Total Time</span><span class="model-stat-value">${{avg(rows.map(r=>r.total_time)).toFixed(1)}}s</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Best Score</span><span class="model-stat-value">${{Math.max(...rows.map(r=>r.score))}}/5</span></div>
      <div class="model-stat-row"><span class="model-stat-label">Worst Score</span><span class="model-stat-value">${{Math.min(...rows.map(r=>r.score))}}/5</span></div>
    </div>`;
  }}).join('');
}})();

// ═══════════════════════════════════════════════════════════════
// HEATMAP
// ═══════════════════════════════════════════════════════════════
function buildHeatmap() {{
  const wfFilter = document.getElementById('heatmapWf').value;
  const lvlFilter = document.getElementById('heatmapLvl').value;
  let filtered = DATA;
  if (wfFilter) filtered = filtered.filter(r=>r.workflow===wfFilter);
  if (lvlFilter) filtered = filtered.filter(r=>r.level===lvlFilter);

  const combos = [];
  MATERIALS.forEach(mat => SECTIONS.forEach(sec => combos.push(mat + ' / ' + sec)));

  const grid = document.getElementById('heatmapGrid');
  grid.style.gridTemplateColumns = `150px repeat(${{combos.length}}, 1fr)`;

  let html = '<div class="heatmap-header">Model</div>';
  combos.forEach(c => {{ html += `<div class="heatmap-header">${{c}}</div>`; }});

  MODELS.forEach(m => {{
    html += `<div class="heatmap-header">${{m}}</div>`;
    combos.forEach(c => {{
      const [mat, sec] = c.split(' / ');
      const rows = filtered.filter(r => r.model===m && r.material===mat && r.section===sec);
      const s = rows.length ? avg(rows.map(r=>r.score)) : 0;
      html += `<div class="heatmap-cell" title="${{m}} | ${{c}} | ${{s.toFixed(2)}}" style="background:${{heatColor(s)}}">${{s ? s.toFixed(1) : '-'}}</div>`;
    }});
  }});

  grid.innerHTML = html;
}}
buildHeatmap();

// ═══════════════════════════════════════════════════════════════
// DETAILED CHARTS
// ═══════════════════════════════════════════════════════════════

new Chart(document.getElementById('boxChart'), {{
  type: 'bar',
  data: {{
    labels: [1,2,3,4,5],
    datasets: MODELS.map((m,i) => ({{
      label: m,
      data: [1,2,3,4,5].map(s => DATA.filter(r=>r.model===m && r.score===s).length),
      backgroundColor: MODEL_COLORS[i],
      borderRadius: 3,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{
      x: {{ title: {{ display: true, text: 'Score' }} }},
      y: {{ beginAtZero: true, title: {{ display: true, text: 'Count' }}, ticks: {{ stepSize: 1 }} }}
    }}
  }}
}});

new Chart(document.getElementById('matChart'), {{
  type: 'bar',
  data: {{
    labels: MATERIALS,
    datasets: MODELS.map((m,i) => ({{
      label: m,
      data: MATERIALS.map(mat => avg(DATA.filter(r=>r.model===m && r.material===mat).map(r=>r.score))),
      backgroundColor: MODEL_COLORS[i], borderRadius: 4,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ y: {{ beginAtZero: true, max: 5 }} }}
  }}
}});

new Chart(document.getElementById('secChart'), {{
  type: 'bar',
  data: {{
    labels: SECTIONS,
    datasets: MODELS.map((m,i) => ({{
      label: m,
      data: SECTIONS.map(sec => avg(DATA.filter(r=>r.model===m && r.section===sec).map(r=>r.score))),
      backgroundColor: MODEL_COLORS[i], borderRadius: 4,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ y: {{ beginAtZero: true, max: 5 }} }}
  }}
}});

new Chart(document.getElementById('scatterChart'), {{
  type: 'scatter',
  data: {{
    datasets: MODELS.map((m,i) => ({{
      label: m,
      data: DATA.filter(r=>r.model===m).map(r => ({{ x: r.total_time, y: r.score }})),
      backgroundColor: MODEL_COLORS[i],
      pointRadius: 5,
      pointHoverRadius: 8,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }},
      tooltip: {{ callbacks: {{ label: ctx => ctx.dataset.label + ': ' + ctx.raw.y + '/5 in ' + ctx.raw.x.toFixed(1) + 's' }} }}
    }},
    scales: {{
      x: {{ title: {{ display: true, text: 'Total Time (s)' }} }},
      y: {{ beginAtZero: true, max: 5, title: {{ display: true, text: 'Score' }} }}
    }}
  }}
}});

// Line chart: avg score per material
new Chart(document.getElementById('trendChart'), {{
  type: 'line',
  data: {{
    labels: MATERIALS,
    datasets: MODELS.map((m,i) => ({{
      label: m,
      data: MATERIALS.map(mat => avg(DATA.filter(r=>r.model===m && r.material===mat).map(r=>r.score))),
      borderColor: MODEL_COLORS[i],
      backgroundColor: MODEL_COLORS_ALPHA[i],
      pointBackgroundColor: MODEL_COLORS[i],
      tension: 0.3,
      fill: false,
      pointRadius: 5,
      pointHoverRadius: 8,
      borderWidth: 2,
    }}))
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ y: {{ beginAtZero: true, max: 5, title: {{ display: true, text: 'Avg Score' }} }} }}
  }}
}});

// Stacked time chart
new Chart(document.getElementById('stackedTimeChart'), {{
  type: 'bar',
  data: {{
    labels: MODELS,
    datasets: [
      {{ label: 'Generation', data: MODELS.map(m => avg(DATA.filter(r=>r.model===m).map(r=>r.gen_time))), backgroundColor: '#6c8aff', borderRadius: 0 }},
      {{ label: 'Translation', data: MODELS.map(m => avg(DATA.filter(r=>r.model===m && r.workflow==='Translated').map(r=>r.trans_time))), backgroundColor: '#ff9f43', borderRadius: 0 }}
    ]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, beginAtZero: true, title: {{ display: true, text: 'Time (s)' }} }} }}
  }}
}});

// ═══════════════════════════════════════════════════════════════
// RESULTS TABLE
// ═══════════════════════════════════════════════════════════════
let sortCol = -1, sortAsc = true;
const fields = ['model','material','section','level','workflow','gen_time','trans_time','total_time','tps','score'];

function getFiltered() {{
  const fm = document.getElementById('filterModel').value;
  const fmat = document.getElementById('filterMaterial').value;
  const fl = document.getElementById('filterLevel').value;
  const fs = document.getElementById('filterSection').value;
  const fw = document.getElementById('filterWorkflow').value;
  const fms = parseInt(document.getElementById('filterMinScore').value) || 0;
  let d = DATA;
  if (fm)  d = d.filter(r=>r.model===fm);
  if (fmat) d = d.filter(r=>r.material===fmat);
  if (fl)  d = d.filter(r=>r.level===fl);
  if (fs)  d = d.filter(r=>r.section===fs);
  if (fw)  d = d.filter(r=>r.workflow===fw);
  if (fms > 0) d = d.filter(r=>r.score>=fms);
  return d;
}}

function renderTable(data) {{
  document.getElementById('rowCount').textContent = `Showing ${{data.length}} of ${{DATA.length}} results`;
  document.getElementById('tableBody').innerHTML = data.map(r =>
    `<tr>
      <td>${{r.model}}</td><td>${{r.material}}</td><td>${{r.section}}</td>
      <td>${{r.level}}</td><td>${{r.workflow}}</td>
      <td>${{r.gen_time.toFixed(1)}}</td><td>${{r.trans_time.toFixed(1)}}</td>
      <td>${{r.total_time.toFixed(1)}}</td><td>${{r.tps.toFixed(1)}}</td>
      <td><span class="score-badge score-${{r.score}}">${{r.score}}/5</span></td>
      <td class="reasoning-cell">${{r.reasoning}}</td>
    </tr>`
  ).join('');
}}

function filterTable() {{
  const data = getFiltered();
  if (sortCol >= 0) sortData(data);
  renderTable(data);
}}

function sortData(data) {{
  const f = fields[sortCol];
  data.sort((a,b) => {{
    const va = typeof a[f] === 'number' ? a[f] : a[f].toLowerCase();
    const vb = typeof b[f] === 'number' ? b[f] : b[f].toLowerCase();
    return sortAsc ? (va > vb ? 1 : -1) : (va < vb ? 1 : -1);
  }});
}}

function sortTable(col) {{
  if (sortCol === col) sortAsc = !sortAsc;
  else {{ sortCol = col; sortAsc = true; }}
  document.querySelectorAll('th').forEach((th,i) => {{
    th.classList.toggle('sorted', i===col);
    const arrow = th.querySelector('.sort-arrow');
    if (arrow) arrow.innerHTML = (i===col && !sortAsc) ? '&#9660;' : '&#9650;';
  }});
  filterTable();
}}

renderTable(DATA);
</script>
</body>
</html>"""

    REPORT_HTML.write_text(html, encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN BENCHMARK
# ═══════════════════════════════════════════════════════════════════════════════


def run_benchmark(resume: bool = False):
    # ── Validate inputs ──────────────────────────────────────────────────
    if not PROMPTS_FILE.exists():
        print(f"ERROR: {PROMPTS_FILE} not found.")
        sys.exit(1)
    if not MATERIAL_DIR.exists() or not list(MATERIAL_DIR.glob("*.txt")):
        print(f"ERROR: {MATERIAL_DIR}/ must exist and contain .txt files.")
        sys.exit(1)

    material_files = sorted(MATERIAL_DIR.glob("*.txt"))
    sections = parse_prompts(PROMPTS_FILE)

    if not sections:
        print("ERROR: No usable prompt sections found in CLIL_Prompts.md")
        sys.exit(1)

    # ── Print configuration ──────────────────────────────────────────────
    print("=" * 65)
    print("  CLIL BENCHMARK")
    print("=" * 65)
    print(f"\n  Prompt sections ({len(sections)}):")
    for s in sections:
        levels = ", ".join(s.user_prompts.keys())
        print(f"    - {s.name}  [{levels}]")
    print(f"\n  Materials: {[f.name for f in material_files]}")
    print(f"\n  Test models ({len(TEST_MODELS)}):")
    for m in TEST_MODELS:
        print(f"    - {m}")
    print(f"  Translator: {TRANSLATOR_MODEL}")
    print(f"  Judge:      {JUDGE_MODEL}")

    verify_models()

    # ── Build the full run list ──────────────────────────────────────────
    runs: list[tuple] = []
    for model in TEST_MODELS:
        for mat_file in material_files:
            for section in sections:
                for level_key in sorted(section.user_prompts):
                    for workflow in ("Direct-DE", "Translated"):
                        level_label = (
                            "L1-Recall"
                            if level_key == "level1"
                            else "L2-Synthesis"
                        )
                        runs.append(
                            (model, mat_file, section, level_key, level_label, workflow)
                        )

    # ── Resume handling ──────────────────────────────────────────────────
    completed: set[tuple] = set()
    if resume:
        completed = load_completed(RESULTS_CSV)
        print(f"\n  Resuming: {len(completed)} runs already done")
    elif RESULTS_CSV.exists():
        RESULTS_CSV.unlink()
        if OUTPUTS_DIR.exists():
            shutil.rmtree(OUTPUTS_DIR)
        if GRADING_DIR.exists():
            shutil.rmtree(GRADING_DIR)

    pending = [
        r
        for r in runs
        if (r[0], r[1].stem, r[2].name, r[4], r[5]) not in completed
    ]

    total = len(runs)
    done_count = total - len(pending)
    print(f"\n  Total: {total} | Done: {done_count} | Remaining: {len(pending)}")
    print("=" * 65)

    if not pending:
        print("\n  All runs completed. Regenerating summary & report...")
        all_rows = load_all_rows(RESULTS_CSV)
        write_summary(all_rows)
        write_report(all_rows)
        return

    # ── Main loop ────────────────────────────────────────────────────────
    for idx, (model, mat_file, section, level_key, level_label, workflow) in enumerate(
        pending, 1
    ):
        mat_content = mat_file.read_text(encoding="utf-8")
        mat_name = mat_file.stem
        sec_short = section.name.split(":")[-1].strip()[:25]

        print(
            f"\n[{done_count + idx}/{total}] "
            f"{short_name(model)} | {mat_name} | {sec_short} | "
            f"{level_label} | {workflow}"
        )

        try:
            if workflow == "Direct-DE":
                # ── Variant A: Direct German generation ───────────────
                prompt = prepare_prompt(
                    section.user_prompts[level_key], mat_content, "de"
                )
                gen = call_model(model, section.system_prompt, prompt)

                final_content = strip_think_tags(gen.content)
                gen_time = gen.wall_time_s
                trans_time = 0.0
                tps = gen.tokens_per_sec

                log(f"Generated: {gen.eval_count} tok | {tps:.1f} t/s | {gen_time:.1f}s")

            else:
                # ── Variant B: English generation + translation ───────
                prompt = prepare_prompt(
                    section.user_prompts[level_key], mat_content, "en"
                )
                gen = call_model(model, section.system_prompt, prompt)
                gen_time = gen.wall_time_s

                log(
                    f"EN output: {gen.eval_count} tok | "
                    f"{gen.tokens_per_sec:.1f} t/s | {gen_time:.1f}s"
                )

                english_output = strip_think_tags(gen.content)
                trans = translate_to_german(english_output)
                trans_time = trans.wall_time_s
                final_content = trans.content

                combined_tok = gen.eval_count + trans.eval_count
                combined_time = gen_time + trans_time
                tps = combined_tok / combined_time if combined_time > 0 else 0

                log(f"Translated: {trans.eval_count} tok | {trans_time:.1f}s")

            total_time = gen_time + trans_time

            # ── Judge ────────────────────────────────────────────────
            score, reasoning = judge_content(final_content, level_key)
            log(f"Score: {score}/5 | Total: {total_time:.1f}s")

            save_output(model, mat_name, section.name, level_label, workflow, final_content)
            save_grading(model, mat_name, section.name, level_label, workflow, score, reasoning)

            row = BenchmarkRow(
                model=model,
                material=mat_name,
                prompt_section=section.name,
                level=level_label,
                workflow=workflow,
                gen_time_s=round(gen_time, 2),
                trans_time_s=round(trans_time, 2),
                total_time_s=round(total_time, 2),
                tokens_per_sec=round(tps, 1),
                score=score,
                reasoning=reasoning,
            )

        except Exception as e:
            print(f"  ERROR: {e}")
            row = BenchmarkRow(
                model=model,
                material=mat_name,
                prompt_section=section.name,
                level=level_label,
                workflow=workflow,
                gen_time_s=0,
                trans_time_s=0,
                total_time_s=0,
                tokens_per_sec=0,
                score=0,
                reasoning=f"Error: {e}",
            )

        append_row(row)

    # ── Generate summary ─────────────────────────────────────────────────
    all_rows = load_all_rows(RESULTS_CSV)
    write_summary(all_rows)
    write_report(all_rows)

    print(f"\n{'=' * 65}")
    print(f"  COMPLETE — {len(all_rows)} results")
    print(f"  CSV:     {RESULTS_CSV.resolve()}")
    print(f"  Summary: {SUMMARY_MD.resolve()}")
    print(f"  Report:  {REPORT_HTML.resolve()}")
    print(f"  Outputs: {OUTPUTS_DIR.resolve()}/")
    print(f"  Grading: {GRADING_DIR.resolve()}/")
    print(f"{'=' * 65}")


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_benchmark(resume="--resume" in sys.argv)
