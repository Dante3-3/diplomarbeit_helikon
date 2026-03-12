# Grammar-Split Evaluation (GPT-5.4)

Generated: 2026-03-12 01:08:54

Evaluator model: gpt-5.4 (via GitHub Copilot CLI)

Split prompts: Gap-Fill / Error Correction / Sentence Transformation (each tested separately)

---


## TEIL5A: Grammar Gap-Fill

**Max. Punkte:** 40


### Bewertung

| Modell | Punkte | Range | Zusammenfassung |
|--------|--------|-------|-----------------|
| mistral:latest | 16/40 | 11-23/40 | Mistral performs weakly on split Grammar Gap-Fill prompts because it repeatedly violates the format, mixing in error-correction and sentence-transformation items instead of producing pure gap-fills. The main problems are faulty or mismatched answer keys, ambiguous solutions, and poorly targeted gap placement, although a few passive-voice outputs show acceptable contextual embedding and cleaner formatting. |
| gemma2:9b | 25/40 | 16-36/40 | `gemma2:9b` shows uneven quality on split Grammar Gap-Fill tasks: the passive voice items are mostly strong, contextualized, and grammatically accurate, but the present perfect/past simple set has repeated answer-key/table mismatches and one clearly wrong form (`has gone` instead of `has been`). The conditional outputs are more coherent than the G1a set, yet they still contain a wrong key (`invested` instead of `invest`) and slight prompt drift because one item tests the zero conditional rather than only Type I/II. |
| deepseek-r1:8b | 27/40 | 14-38/40 | The model shows highly uneven quality: the conditional and simpler passive-voice sets are often usable, but the present perfect/past simple outputs are badly damaged by missing answers, malformed gap design, and answer-key mismatches. Overall, `deepseek-r1:8b` can sometimes produce solid contextualized grammar gap-fills, but its reliability is too inconsistent for dependable classroom use without careful teacher correction. |


#### Detaillierte Bewertungen


**mistral:latest:**
```
SCORE: 16/40

RANGE: 11-23/40

SUMMARY: Mistral performs weakly on split Grammar Gap-Fill prompts because it repeatedly violates the format, mixing in error-correction and sentence-transformation items instead of producing pure gap-fills. The main problems are faulty or mismatched answer keys, ambiguous solutions, and poorly targeted gap placement, although a few passive-voice outputs show acceptable contextual embedding and cleaner formatting.
```


**gemma2:9b:**
```
● Todo added: Evaluate gemma2 grammar gap-fill outputs

I’ve finished scoring the set and am just recording completion before I hand over the final verdict.

● Todo completed: evaluate-gemma2-gapfill

SCORE: 25/40

RANGE: 16-36/40

SUMMARY: `gemma2:9b` shows uneven quality on split Grammar Gap-Fill tasks: the passive voice items are mostly strong, contextualized, and grammatically accurate, but the present perfect/past simple set has repeated answer-key/table mismatches and one clearly wrong form (`has gone` instead of `has been`). The conditional outputs are more coherent than the G1a set, yet they still contain a wrong key (`invested` instead of `invest`) and slight prompt drift because one item tests the zero conditional rather than only Type I/II.
```


**deepseek-r1:8b:**
```
SCORE: 27/40
RANGE: 14-38/40
SUMMARY: The model shows highly uneven quality: the conditional and simpler passive-voice sets are often usable, but the present perfect/past simple outputs are badly damaged by missing answers, malformed gap design, and answer-key mismatches. Overall, `deepseek-r1:8b` can sometimes produce solid contextualized grammar gap-fills, but its reliability is too inconsistent for dependable classroom use without careful teacher correction.
```


---


## TEIL5B: Grammar Error Correction

**Max. Punkte:** 40


### Bewertung

| Modell | Punkte | Range | Zusammenfassung |
|--------|--------|-------|-----------------|
| mistral:latest | 11/40 | 5-18/40 | Mistral performs poorly on this split Grammar Error Correction task: many outputs are not true error-correction exercises at all, but drift into gap-fill, sentence rewriting, or tense labeling, and the answer keys are frequently wrong or internally inconsistent. The stronger outputs provide usable context and mostly understandable language, but even these often contain ambiguous corrections, target-grammar drift, or teacher keys that introduce new errors. |
| gemma2:9b | 15/40 | 6-28/40 | Gemma 2 9b performs poorly on split Grammar Error Correction prompts because many “errors” are actually correct forms, bolding often marks the wrong word, and answer keys are frequently inaccurate or misaligned with the task. The Present Perfect/Past Simple and Conditional outputs are especially weak on instruction adherence and unambiguity, while the Passive Voice set is somewhat stronger but still inconsistent. |
| deepseek-r1:8b | 19/40 | 8-36/40 | The model is highly inconsistent on Grammar Error Correction: a few outputs, especially some conditional and passive-voice sets, are workable, but several others fail badly because correct phrases are marked as errors, multiple errors appear in one sentence, or the answer keys are plainly wrong. Overall, formatting and contextual embedding are often acceptable, but reliability is too low for dependable classroom use without heavy teacher correction. |


#### Detaillierte Bewertungen


**mistral:latest:**
```
● Todo added: Evaluate Mistral GEC outputs

● Create session plan
  $ cat > /Users/dstoilovski/.copilot/session-state/6048bc12-c68d-4977-938c-06f32e943cea/plan.md
  <<'EOF'
  1. Review all 9 outputs for Grammar Error Correction quality.
  2. Estimate per-output scores using the provided criteria and derive overall score/range.
  3. Return the requested 3-line summary in the exact format....
  └ 2 lines...

I’ve finished the scoring pass. I’m just marking the evaluation task complete and then I’ll return the requested three-line verdict.

● Todo completed: evaluate-mistral-gec

SCORE: 11/40

RANGE: 5-18/40

SUMMARY: Mistral performs poorly on this split Grammar Error Correction task: many outputs are not true error-correction exercises at all, but drift into gap-fill, sentence rewriting, or tense labeling, and the answer keys are frequently wrong or internally inconsistent. The stronger outputs provide usable context and mostly understandable language, but even these often contain ambiguous corrections, target-grammar drift, or teacher keys that introduce new errors.
```


**gemma2:9b:**
```
● SQL: Create evaluation todos
  └ 2 row(s) inserted. Last inserted row ID: 2.

● Todo completed: assess-gemma-g3b, summarize-findings

SCORE: 15/40
RANGE: 6-28/40
SUMMARY: Gemma 2 9b performs poorly on split Grammar Error Correction prompts because many “errors” are actually correct forms, bolding often marks the wrong word, and answer keys are frequently inaccurate or misaligned with the task. The Present Perfect/Past Simple and Conditional outputs are especially weak on instruction adherence and unambiguity, while the Passive Voice set is somewhat stronger but still inconsistent.
```


**deepseek-r1:8b:**
```
● Todo added: Review DeepSeek GEC outputs

I’ve finished the per-output judgments and am just calculating a consistent overall score and range. The pattern is very uneven: a few solid conditional/passive exercises, but several severe failures where correct text is marked as wrong or keys are unusable.

● Todo started: review-deepseek-gec

● Todo completed: finalize-deepseek-gec

SCORE: 19/40

RANGE: 8-36/40

SUMMARY: The model is highly inconsistent on Grammar Error Correction: a few outputs, especially some conditional and passive-voice sets, are workable, but several others fail badly because correct phrases are marked as errors, multiple errors appear in one sentence, or the answer keys are plainly wrong. Overall, formatting and contextual embedding are often acceptable, but reliability is too low for dependable classroom use without heavy teacher correction.
```


---


## TEIL5C: Grammar Sentence Transformation

**Max. Punkte:** 40


### Bewertung

| Modell | Punkte | Range | Zusammenfassung |
|--------|--------|-------|-----------------|
| mistral:latest | 25/40 | 20-29/40 | Mistral shows uneven quality on Grammar Sentence Transformation: the conditional-sentence sets and one passive-voice set are moderately usable, but most outputs contain meaning shifts, tense/aspect errors, incomplete answer keys, or awkward rewrites that stop being true transformations. Its biggest weaknesses are instruction adherence and grammatical reliability, especially in the Present Perfect/Past Simple and Passive Voice tasks, where prompts and keys often become fragments, paraphrases, or ungrammatical sentences. |
| gemma2:9b | 21/40 | 9-35/40 | `gemma2:9b` shows very uneven quality on Grammar Sentence Transformation. Its best outputs are clear, well-formatted, and contextually embedded, especially for straightforward conditional rewrites, but many items fail on core transformation validity: unchanged sentences, wrong tense shifts, ungrammatical answer keys, and meaning changes are frequent. Overall, the model is usable only with careful human review, because reliability across outputs is low. |
| deepseek-r1:8b | 11/40 | 5-34/40 | Overall, `deepseek-r1:8b` performs poorly on Grammar Sentence Transformation with SPLIT prompts. Most outputs suffer from truncation, missing or invalid answer keys, and transformations that fail to preserve meaning or produce a correct grammatical reformulation; only Output 9 is genuinely strong. The model shows it can generate contextualized material, but reliability is far too inconsistent for dependable classroom use in this category. |


#### Detaillierte Bewertungen


**mistral:latest:**
```
SCORE: 25/40
RANGE: 20-29/40
SUMMARY: Mistral shows uneven quality on Grammar Sentence Transformation: the conditional-sentence sets and one passive-voice set are moderately usable, but most outputs contain meaning shifts, tense/aspect errors, incomplete answer keys, or awkward rewrites that stop being true transformations. Its biggest weaknesses are instruction adherence and grammatical reliability, especially in the Present Perfect/Past Simple and Passive Voice tasks, where prompts and keys often become fragments, paraphrases, or ungrammatical sentences.
```


**gemma2:9b:**
```
SCORE: 21/40
RANGE: 9-35/40
SUMMARY: `gemma2:9b` shows very uneven quality on Grammar Sentence Transformation. Its best outputs are clear, well-formatted, and contextually embedded, especially for straightforward conditional rewrites, but many items fail on core transformation validity: unchanged sentences, wrong tense shifts, ungrammatical answer keys, and meaning changes are frequent. Overall, the model is usable only with careful human review, because reliability across outputs is low.
```


**deepseek-r1:8b:**
```
● Todo added: Score nine outputs

Quick pass done: most failures are instruction/answer-key integrity issues rather than isolated grammar slips. I’m turning that into a conservative averaged model score and a min-max range now.

● SQL: Compute score average
  └ Executed 4 statement(s)

● Todo started: score-outputs

I’ve got the final numbers: one clearly good passive-voice set, but the rest are dragged down by truncation, missing/invalid keys, and transformations that often stop preserving meaning. I’m closing out the tracking and handing you the condensed verdict next.

● Todo completed: draft-summary

SCORE: 11/40
RANGE: 5-34/40
SUMMARY: Overall, `deepseek-r1:8b` performs poorly on Grammar Sentence Transformation with SPLIT prompts. Most outputs suffer from truncation, missing or invalid answer keys, and transformations that fail to preserve meaning or produce a correct grammatical reformulation; only Output 9 is genuinely strong. The model shows it can generate contextualized material, but reliability is far too inconsistent for dependable classroom use in this category.
```


---
