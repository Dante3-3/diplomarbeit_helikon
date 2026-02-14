# Diplomarbeit: LLM-Evaluation fur CLIL-Materialerstellung

Vergleichende Analyse von Open-Source Large Language Models (LLMs) bei der automatisierten Erstellung von englischsprachigen CLIL-Unterrichtsmaterialien auf B2-Niveau.

## Worum geht es?

Diese Diplomarbeit untersucht, wie gut lokale Open-Source-LLMs CLIL-Materialien (Content and Language Integrated Learning) generieren koennen. Drei Modelle — **Mistral 7B**, **Gemma2 9B** und **DeepSeek-R1 8B** — werden ueber 7 Aufgabenkategorien systematisch getestet. Fuer die Kategorie Deutsche Rechtschreibung wird zusaetzlich **EuroLLM** einbezogen.

### Getestete Kategorien

| Teil | Kategorie |
|------|-----------|
| Teil 2 | Vocabulary (Knowledge Activation) |
| Teil 3 | Multiple Choice |
| Teil 4 | Sentence Completion |
| Teil 5 | Grammatik |
| Teil 6 | True/False |
| Teil 7 | Gap-Fill |
| Teil 8 | Deutsche Rechtschreibung |

## Erster Testlauf

Ein erster vollstaendiger Testlauf mit **198 Outputs** (3 Modelle x 7 Teile x 3 Prompts x 3 Wiederholungen + EuroLLM fuer Teil 8) wurde durchgefuehrt. Alle Outputs wurden anschliessend mit GitHub Copilot bewertet.

Die Ergebnisse sind im interaktiven Dashboard visualisiert:

**[`diplomarbeit_dashboard.html`](diplomarbeit_dashboard.html)** (auf dem `languages`-Branch)

Das Dashboard zeigt Radar-Charts, Heatmap-Tabellen, Balkendiagramme, Antwortzeiten- und Output-Laengen-Analysen sowie die wichtigsten Erkenntnisse auf einen Blick.

## Projektstruktur

- `diplomarbeit_output/` — Alle generierten LLM-Outputs und Evaluierungen
- `diplomarbeit_dashboard.html` — Interaktives React-Dashboard (auf `languages`-Branch)
- `clil-main/` — CLIL-Plattform (Frontend)
