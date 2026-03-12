# Diplomarbeit: LLM-Evaluation für CLIL-Materialerstellung

Vergleichende Analyse von Open-Source Large Language Models (LLMs) bei der automatisierten Erstellung von englischsprachigen CLIL-Unterrichtsmaterialien auf B2-Niveau.

---

## Master Dashboard

**[`master_dashboard.html`](master_dashboard.html)** — Gesamtübersicht aller Ergebnisse (dieser Branch, `main`)

Das Dashboard enthält 4 Tabs und fasst alle Testergebnisse zusammen. **Alle Scores wurden einheitlich mit GPT-5.4 (GitHub Copilot) bewertet**, um Vergleichbarkeit sicherzustellen.

### Tab 1 – Gesamtübersicht
Alle 5 getesteten Modelle (Mistral, Gemma2, DeepSeek-R1, Qwen3.5, EuroLLM) im Vergleich über alle 7 Kategorien. Enthält eine farbcodierte Heatmap-Tabelle, ein Radar-Chart sowie ein Balkendiagramm (normalisiert auf %).

> **Hinweis:** Mistral, Gemma2 und DeepSeek wurden im Original-Run mit Prompts 1–3 getestet. Qwen3.5 wurde im Feedback-Loop-Run mit Prompts 4–5 getestet (kein direkter 1:1-Vergleich möglich, aber als Orientierung brauchbar).

### Tab 2 – Original Run
Ergebnisse des ersten vollständigen Testlaufs: **198 Outputs** (3 Modelle × 7 Kategorien × 3 Prompts × 3 Wiederholungen + EuroLLM für Orthography). Enthält Score-Tabelle, Balkendiagramm und Modell-Zusammenfassungskarten.

### Tab 3 – Grammar Split
Vergleich zwischen dem einheitlichen Grammar-Prompt und aufgeteilten Subtypen (Gap-Fill / Error Correction / Sentence Transformation). Ergebnis: Das Splitting hat sich nicht gelohnt — alle Modelle schneiden im Split schlechter ab als im einheitlichen Format.

### Tab 4 – Feedback Loop
Ergebnisse des automatischen zweistufigen Feedback-Systems:
- **V2:** Strukturcheck durch qwen2.5:3b (96% FAIL-Rate → Überarbeitung)
- **V3:** Inhaltscheck durch qwen2.5:7b (79% FAIL-Rate → Überarbeitung)

Zeigt den tatsächlichen Effekt beider Feedback-Stufen pro Modell und Kategorie, inklusive "Scores nach Kategorie" Vergleich (V2i → V2 → V3) für jedes Modell.

---

## Getestete Kategorien

| Teil | Kategorie | Max. Punkte |
|------|-----------|-------------|
| Teil 2 | Vocabulary (Knowledge Activation) | 40 |
| Teil 3 | Multiple Choice | 45 |
| Teil 4 | Sentence Completion | 40 |
| Teil 5 | Grammatik | 40 |
| Teil 6 | True/False | 40 |
| Teil 7 | Gap-Fill | 40 |
| Teil 8 | Deutsche Rechtschreibung | 40 |

---

## Branches & was dort zu finden ist

### `languages` — Erster Testlauf
Der vollständige erste Testlauf mit 198 Outputs.

- [`AnweisungenMaterialErstellung.md`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/languages/AnweisungenMaterialErstellung.md) — **Alle Testangaben, System-Prompts, User-Prompts und die vollständige Bewertungsskala** (Teil 9). Wichtigstes Referenzdokument für die Methodik.
- [`diplomarbeit_config.json`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/languages/diplomarbeit_config.json) — Konfiguration: alle Prompts, Modelle, Wiederholungen
- [`diplomarbeit_runner.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/languages/diplomarbeit_runner.py) — Script zur Generierung aller Outputs via Ollama
- [`diplomarbeit_evaluator.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/languages/diplomarbeit_evaluator.py) — Evaluator (ursprünglich ohne fixe Modellversion)
- [`diplomarbeit_dashboard.html`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/languages/diplomarbeit_dashboard.html) — Interaktives Dashboard des ersten Runs (alte Copilot-Scores)
- `diplomarbeit_output/results.jsonl` — 198 generierte Outputs (JSON Lines)

### `grammar-split` — Grammar-Splitting Experiment
Test ob das Aufteilen des einheitlichen Grammar-Prompts in 3 Subtypen bessere Ergebnisse liefert.

- [`grammar_comparison_dashboard.html`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/grammar-split/grammar_comparison_dashboard.html) — Dashboard: Unified vs. Split Vergleich
- `diplomarbeit_output/results_grammar_split.jsonl` — 81 Outputs (3 Subtypen × 3 Modelle × 9 Outputs)
- **Ergebnis:** Split schlechter als Unified für alle Modelle

### `feedback-structural` — Feedback Loop Implementierung
Entwicklung und erster Teil des automatischen Feedback-Loop-Systems.

- [`diplomarbeit_runner_v2.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-structural/diplomarbeit_runner_v2.py) — Generator mit Strukturcheck (qwen2.5:3b als Reviewer)
- [`diplomarbeit_config_v2.json`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-structural/diplomarbeit_config_v2.json) — Konfiguration V2: Prompts 4–5, Modelle mistral/gemma2/qwen3.5
- `diplomarbeit_output/results_v2_structural.jsonl` — 126 Outputs inkl. `initial_response` und `final_response`

### `feedback-content` — Vollständiger Feedback Loop + GPT-5.4 Bewertung
Alle finalen Ergebnisse, GPT-5.4 Evaluatoren und der Feedback-Vergleichs-Dashboard.

- [`diplomarbeit_runner_v3.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/diplomarbeit_runner_v3.py) — Generator mit Inhaltscheck (qwen2.5:7b als Reviewer)
- [`feedback_comparison_dashboard.html`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/feedback_comparison_dashboard.html) — Dashboard: Orig → V2i → V2 → V3 Vergleich (GPT-5.4 Scores)
- [`diplomarbeit_evaluator_gpt54.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/diplomarbeit_evaluator_gpt54.py) — GPT-5.4 Evaluator für den Original-Run (2 Runs für Reproduzierbarkeit)
- [`diplomarbeit_evaluator_v2_gpt54.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/diplomarbeit_evaluator_v2_gpt54.py) — GPT-5.4 Evaluator für V2 (post-structural)
- [`diplomarbeit_evaluator_v2initial_gpt54.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/diplomarbeit_evaluator_v2initial_gpt54.py) — GPT-5.4 Evaluator für V2-initial (vor Feedback)
- [`diplomarbeit_evaluator_v3_gpt54.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/diplomarbeit_evaluator_v3_gpt54.py) — GPT-5.4 Evaluator für V3 (post-content)
- [`diplomarbeit_evaluator_grammarsplit_gpt54.py`](https://github.com/Dante3-3/diplomarbeit_helikon/blob/feedback-content/diplomarbeit_evaluator_grammarsplit_gpt54.py) — GPT-5.4 Evaluator für Grammar Split
- `diplomarbeit_output/results_v3_content.jsonl` — 126 finale Outputs (post-content-feedback)

---

## Wichtige Designentscheidungen

### Evaluator: GPT-5.4 statt Copilot (default)
Der ursprüngliche Evaluator nutzte GitHub Copilot ohne festgelegte Modellversion. Nachträgliche Tests zeigten Schwankungen von bis zu ±20 Punkten auf denselben Outputs. Alle im Master Dashboard verwendeten Scores wurden daher einheitlich mit `copilot --model gpt-5.4` neu bewertet — 2 Runs für den Original-Run (zur Überprüfung der Reproduzierbarkeit), je 1 Run für V2/V3/Grammar-Split.

### Feedback Loop
- **V2 (Strukturcheck):** qwen2.5:3b prüft mechanisch auf strukturelle Fehler (fehlende Gaps, falsche Anzahl Antworten, etc.). Bei FAIL: ein Überarbeitungsversuch mit dem Feedback im Prompt.
- **V3 (Inhaltscheck):** qwen2.5:7b prüft inhaltliche Fehler (falsche Zeiten, falsches Answer Key, etc.). Deutsche Rechtschreibung ausgenommen (`human_review_required`).
- **Ergebnis:** Strukturcheck verschlechtert Mistral in 5/7 Kategorien. Gemma2 profitiert am meisten. Inhaltscheck hilft kaum bis schadet.

### Grammar Split
Der einheitliche Grammar-Prompt ließ die Modelle alle drei Typen kombiniert generieren. Das Splitting in separate Prompts erbrachte schlechtere Ergebnisse — Error Correction erwies sich als besonders schwierig für alle Modelle (11–19/40).

---

## Projektstruktur (main branch)

```
diplomarbeit_helikon/
├── master_dashboard.html     # Gesamtübersicht aller Ergebnisse
└── README.md                 # Diese Datei
```

Alle weiteren Dateien (Outputs, Runner, Evaluatoren, Branch-Dashboards) befinden sich auf den jeweiligen Branches (siehe oben).

---

*Diplomarbeit Helikon – CLIL LLM-Evaluation – bewertet mit GPT-5.4 (GitHub Copilot)*
