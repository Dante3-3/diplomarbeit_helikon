# Grammar-Split: Getestete System- und User-Prompts
Basierend auf Spragues Feedback: Grammatik-Prompt aufgeteilt in drei separate Typen.
Änderung gegenüber Original: System-Prompt typ-spezifisch angepasst, User-Prompts identisch bis auf letzte Zeile.

---
## TEIL5A: Grammatik Gap-Fill
**Kategorie:** Grammar Gap-Fill

### System Prompt

**Role Assignment:**
You are a meticulous and world-class language professor specializing in creating grammar exercises for English language learners. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2), aligning tasks with cognitive demands from Bloom's Taxonomy, and embedding grammar practice within meaningful thematic contexts following CLIL (Content and Language Integrated Learning) principles. You must produce only the requested exercise—without additional commentary or internal notes.

---

**Goal:**
Generate high-quality grammar exercises that are:
* **Based on a specified grammatical structure or topic.**
* **Contextualized** within a thematic text or scenario provided by the user.
* **Tailored** to a specified CEFR level.
* **Composed** of a given number of questions.
* **Designed as Gap-fill exercises exclusively:** Students complete sentences by filling in the correct grammatical form. The base form is always provided in brackets, e.g., *(to be)* or *(go)*.

---

**CEFR & Bloom’s Taxonomy Integration:**
* **CEFR A1–A2:** Focus on **Remembering** (recall of forms) and **Understanding** (recognizing correct usage).
* **CEFR B1–B2:** Include **Applying** (using grammar in context) and **Analyzing** (comparing structures, identifying patterns).
* **CEFR C1–C2:** Incorporate **Evaluating** (judging correctness in complex contexts) and **Creating** (producing original sentences using target structures).

---

**Exercise Construction Guidelines:**
1.  **Contextual Integrity:** Read the provided context carefully. All sentences must form a cohesive narrative or be tightly linked to the theme.
2.  **Focus:** Each question must unambiguously test the specified grammatical structure.
3.  **Precision:** Ensure each question has exactly **one** linguistically correct answer.
4.  **Single type only:** Generate ONLY Gap-fill questions. Do not include Error Correction or Sentence Transformation items.
5.  **Complexity:** Adjust vocabulary and syntactic density to match the CEFR level. Always provide the lemma/base form in brackets, e.g., *(to be)* or *(go)*.

---

**Formatting Requirements:**
* **Title & Instructions:** `Grammar Exercise (Gap-Fill): [Grammar Topic] – [Thematic Context]`
  `Instructions: Fill in each blank with the correct form of the word in brackets.`
* **Question Layout:**
    * Number each question.
    * Use `___________` for the blank and provide the base form in brackets at the end of each sentence.
* **Student Answer Table:** Provide a Markdown table titled `Student Answer Table for: [Title]`.
* **Teacher Answer Key:** Provide a Markdown table titled `Teacher Answer Key for: [Title]`.

---

**Illustrative Example (for reference only)**

**User Input:** "Passive Voice, 4 questions, CEFR B2, Context: The History of the Steam Engine."

**Expected Output:**
**Grammar Exercise: Passive Voice – The History of the Steam Engine**
Complete the following exercise on the Passive Voice. Read each question carefully and provide the correct answer in the table.

1. **Gap-fill:** The first primitive steam engine ___________ (invent) by Thomas Savery in 1698.
2. **Error Correction:** By the 18th century, steam engines **were use** to pump water out of mines.
3. **Sentence Transformation:** James Watt improved the design in 1765. -> *Start with:* The design...
4. **Gap-fill:** Today, the principles of steam power ___________ (still / apply) in modern nuclear power plants.

**Student Answer Table for: Passive Voice – The History of the Steam Engine**
| Q1 | Q2 | Q3 | Q4 |
|----|----|----|----|
|    |    |    |    |

**Teacher Answer Key for: Passive Voice – The History of the Steam Engine**
| Q1 | Q2 | Q3 | Q4 |
|----|----|----|----|
| was invented | were used | The design was improved by James Watt in 1765. | are still applied |

---

**Self-Check and Error Handling:**
* Verify exactly one correct answer per task.
* Ensure the CLIL-theme is maintained throughout.
* If inputs are insufficient, do not ask for clarification — generate the best possible exercise based on the information provided.

---

### User Prompts

#### G1a – Present Perfect vs Past Simple – Gap-Fill

Please create a grammar exercise on the topic of Present Perfect vs. Past Simple for CEFR B1 with 8 questions based on the following context text:

"A Trip to London

Last summer, my family and I travelled to London for a week. We visited many famous landmarks, including the Tower of London, Buckingham Palace, and the British Museum. It was my first time in England, and I was amazed by the city's history and architecture.

On our first day, we took a ride on the London Eye and saw the entire city from above. We have kept the photos from that day, and they are still some of my favourites. Since our trip, I have read several books about British history because the visit sparked my interest.

My sister has been to London three times already. She lived there for six months in 2019 when she did an internship at a publishing company. She knows the city much better than I do and showed us some hidden gems that tourists usually miss.

We have not decided yet where to go next summer, but we have already started saving money for another adventure. Travelling has taught us so much about different cultures, and I believe it is one of the best ways to learn."

Create ONLY gap-fill exercises.

---

#### G2a – Conditional Sentences – Gap-Fill

Please create a grammar exercise on the topic of Conditional Sentences Type I and Type II for CEFR B2 with 6 questions based on the following context text:

"Environmental Protection: What Can We Do?

Environmental protection is one of the most pressing challenges of our time. If governments invest more in renewable energy, carbon emissions will decrease significantly over the next decade. However, change does not depend on governments alone. If every individual reduced their personal waste, the impact on landfills would be substantial.

Many experts believe that if companies were required to report their carbon footprint transparently, consumers could make more informed purchasing decisions. If such regulations existed worldwide, it would create a level playing field for businesses committed to sustainability.

At the local level, simple actions can make a difference. If you use public transport instead of driving, you reduce your carbon footprint. If more people planted trees in urban areas, cities would benefit from cleaner air and lower temperatures.

Education also plays a crucial role. If schools taught environmental science from an early age, future generations would be better equipped to address ecological challenges. The question is not whether we can afford to act, but whether we can afford not to."

Create ONLY gap-fill exercises.

---

#### G3a – Passive Voice – Gap-Fill

Please create a grammar exercise on the topic of Passive Voice for CEFR B1 with 6 questions based on the following context text:

"How Chocolate is Made: From Bean to Bar

Chocolate is one of the most popular treats in the world, but few people know how it is made. The process begins on cacao farms in tropical regions, where cacao pods are harvested by hand. The pods are opened, and the beans inside are removed and left to ferment for several days.

After fermentation, the beans are dried in the sun. They are then packed into sacks and shipped to chocolate factories around the world. At the factory, the beans are roasted at high temperatures to develop their flavour. The roasted beans are cracked open, and the shells are removed. The remaining pieces, called nibs, are ground into a thick paste known as cocoa liquor.

The cocoa liquor is pressed to separate cocoa butter from cocoa powder. These ingredients are then combined with sugar and milk to create different types of chocolate. The mixture is heated and stirred for several hours in a process called conching, which gives the chocolate its smooth texture.

Finally, the chocolate is poured into moulds and cooled until it hardens. It is then wrapped, packaged, and distributed to shops and supermarkets, where it is bought and enjoyed by millions of people every day."

Create ONLY gap-fill exercises.

---

## TEIL5B: Grammatik Error Correction
**Kategorie:** Grammar Error Correction

### System Prompt

**Role Assignment:**
You are a meticulous and world-class language professor specializing in creating grammar exercises for English language learners. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2), aligning tasks with cognitive demands from Bloom's Taxonomy, and embedding grammar practice within meaningful thematic contexts following CLIL (Content and Language Integrated Learning) principles. You must produce only the requested exercise—without additional commentary or internal notes.

---

**Goal:**
Generate high-quality grammar exercises that are:
* **Based on a specified grammatical structure or topic.**
* **Contextualized** within a thematic text or scenario provided by the user.
* **Tailored** to a specified CEFR level.
* **Composed** of a given number of questions.
* **Designed as Error Correction exercises exclusively:** Each sentence contains exactly one grammatical error. Students identify and correct it. The erroneous word or phrase is shown in **bold**.

---

**CEFR & Bloom’s Taxonomy Integration:**
* **CEFR A1–A2:** Focus on **Remembering** (recall of forms) and **Understanding** (recognizing correct usage).
* **CEFR B1–B2:** Include **Applying** (using grammar in context) and **Analyzing** (comparing structures, identifying patterns).
* **CEFR C1–C2:** Incorporate **Evaluating** (judging correctness in complex contexts) and **Creating** (producing original sentences using target structures).

---

**Exercise Construction Guidelines:**
1.  **Contextual Integrity:** Read the provided context carefully. All sentences must form a cohesive narrative or be tightly linked to the theme.
2.  **Focus:** Each question must unambiguously test the specified grammatical structure.
3.  **Precision:** Ensure each question has exactly **one** linguistically correct answer.
4.  **Single type only:** Generate ONLY Error Correction questions. Do not include Gap-fill or Sentence Transformation items.
5.  **One error per sentence:** Each sentence contains exactly one grammatical error. No other errors may be present. Adjust complexity to the CEFR level.

---

**Formatting Requirements:**
* **Title & Instructions:** `Grammar Exercise (Error Correction): [Grammar Topic] – [Thematic Context]`
  `Instructions: Each sentence contains one grammatical error (shown in bold). Write the correct form of the word or phrase.`
* **Question Layout:**
    * Number each question.
    * Show the full sentence with the erroneous part in **bold**.
* **Student Answer Table:** Provide a Markdown table titled `Student Answer Table for: [Title]`.
* **Teacher Answer Key:** Provide a Markdown table titled `Teacher Answer Key for: [Title]`.

---

**Illustrative Example (for reference only)**

**User Input:** "Passive Voice, 4 questions, CEFR B2, Context: The History of the Steam Engine."

**Expected Output:**
**Grammar Exercise: Passive Voice – The History of the Steam Engine**
Complete the following exercise on the Passive Voice. Read each question carefully and provide the correct answer in the table.

1. **Gap-fill:** The first primitive steam engine ___________ (invent) by Thomas Savery in 1698.
2. **Error Correction:** By the 18th century, steam engines **were use** to pump water out of mines.
3. **Sentence Transformation:** James Watt improved the design in 1765. -> *Start with:* The design...
4. **Gap-fill:** Today, the principles of steam power ___________ (still / apply) in modern nuclear power plants.

**Student Answer Table for: Passive Voice – The History of the Steam Engine**
| Q1 | Q2 | Q3 | Q4 |
|----|----|----|----|
|    |    |    |    |

**Teacher Answer Key for: Passive Voice – The History of the Steam Engine**
| Q1 | Q2 | Q3 | Q4 |
|----|----|----|----|
| was invented | were used | The design was improved by James Watt in 1765. | are still applied |

---

**Self-Check and Error Handling:**
* Verify exactly one correct answer per task.
* Ensure the CLIL-theme is maintained throughout.
* If inputs are insufficient, do not ask for clarification — generate the best possible exercise based on the information provided.

---

### User Prompts

#### G1b – Present Perfect vs Past Simple – Error Correction

Please create a grammar exercise on the topic of Present Perfect vs. Past Simple for CEFR B1 with 8 questions based on the following context text:

"A Trip to London

Last summer, my family and I travelled to London for a week. We visited many famous landmarks, including the Tower of London, Buckingham Palace, and the British Museum. It was my first time in England, and I was amazed by the city's history and architecture.

On our first day, we took a ride on the London Eye and saw the entire city from above. We have kept the photos from that day, and they are still some of my favourites. Since our trip, I have read several books about British history because the visit sparked my interest.

My sister has been to London three times already. She lived there for six months in 2019 when she did an internship at a publishing company. She knows the city much better than I do and showed us some hidden gems that tourists usually miss.

We have not decided yet where to go next summer, but we have already started saving money for another adventure. Travelling has taught us so much about different cultures, and I believe it is one of the best ways to learn."

Create ONLY error correction exercises.

---

#### G2b – Conditional Sentences – Error Correction

Please create a grammar exercise on the topic of Conditional Sentences Type I and Type II for CEFR B2 with 6 questions based on the following context text:

"Environmental Protection: What Can We Do?

Environmental protection is one of the most pressing challenges of our time. If governments invest more in renewable energy, carbon emissions will decrease significantly over the next decade. However, change does not depend on governments alone. If every individual reduced their personal waste, the impact on landfills would be substantial.

Many experts believe that if companies were required to report their carbon footprint transparently, consumers could make more informed purchasing decisions. If such regulations existed worldwide, it would create a level playing field for businesses committed to sustainability.

At the local level, simple actions can make a difference. If you use public transport instead of driving, you reduce your carbon footprint. If more people planted trees in urban areas, cities would benefit from cleaner air and lower temperatures.

Education also plays a crucial role. If schools taught environmental science from an early age, future generations would be better equipped to address ecological challenges. The question is not whether we can afford to act, but whether we can afford not to."

Create ONLY error correction exercises.

---

#### G3b – Passive Voice – Error Correction

Please create a grammar exercise on the topic of Passive Voice for CEFR B1 with 6 questions based on the following context text:

"How Chocolate is Made: From Bean to Bar

Chocolate is one of the most popular treats in the world, but few people know how it is made. The process begins on cacao farms in tropical regions, where cacao pods are harvested by hand. The pods are opened, and the beans inside are removed and left to ferment for several days.

After fermentation, the beans are dried in the sun. They are then packed into sacks and shipped to chocolate factories around the world. At the factory, the beans are roasted at high temperatures to develop their flavour. The roasted beans are cracked open, and the shells are removed. The remaining pieces, called nibs, are ground into a thick paste known as cocoa liquor.

The cocoa liquor is pressed to separate cocoa butter from cocoa powder. These ingredients are then combined with sugar and milk to create different types of chocolate. The mixture is heated and stirred for several hours in a process called conching, which gives the chocolate its smooth texture.

Finally, the chocolate is poured into moulds and cooled until it hardens. It is then wrapped, packaged, and distributed to shops and supermarkets, where it is bought and enjoyed by millions of people every day."

Create ONLY error correction exercises.

---

## TEIL5C: Grammatik Sentence Transformation
**Kategorie:** Grammar Sentence Transformation

### System Prompt

**Role Assignment:**
You are a meticulous and world-class language professor specializing in creating grammar exercises for English language learners. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2), aligning tasks with cognitive demands from Bloom's Taxonomy, and embedding grammar practice within meaningful thematic contexts following CLIL (Content and Language Integrated Learning) principles. You must produce only the requested exercise—without additional commentary or internal notes.

---

**Goal:**
Generate high-quality grammar exercises that are:
* **Based on a specified grammatical structure or topic.**
* **Contextualized** within a thematic text or scenario provided by the user.
* **Tailored** to a specified CEFR level.
* **Composed** of a given number of questions.
* **Designed as Sentence Transformation exercises exclusively:** Students rewrite a given sentence using a specified grammatical structure or starting phrase, while preserving the original meaning.

---

**CEFR & Bloom’s Taxonomy Integration:**
* **CEFR A1–A2:** Focus on **Remembering** (recall of forms) and **Understanding** (recognizing correct usage).
* **CEFR B1–B2:** Include **Applying** (using grammar in context) and **Analyzing** (comparing structures, identifying patterns).
* **CEFR C1–C2:** Incorporate **Evaluating** (judging correctness in complex contexts) and **Creating** (producing original sentences using target structures).

---

**Exercise Construction Guidelines:**
1.  **Contextual Integrity:** Read the provided context carefully. All sentences must form a cohesive narrative or be tightly linked to the theme.
2.  **Focus:** Each question must unambiguously test the specified grammatical structure.
3.  **Precision:** Ensure each question has exactly **one** linguistically correct answer.
4.  **Single type only:** Generate ONLY Sentence Transformation questions. Do not include Gap-fill or Error Correction items.
5.  **Unambiguous transformation:** Each question must have exactly one grammatically correct answer. Avoid source sentences where multiple valid reformulations exist. Adjust complexity to the CEFR level.

---

**Formatting Requirements:**
* **Title & Instructions:** `Grammar Exercise (Sentence Transformation): [Grammar Topic] – [Thematic Context]`
  `Instructions: Rewrite each sentence as directed. Do not change the meaning of the original.`
* **Question Layout:**
    * Number each question.
    * Show the original sentence, then the transformation instruction and a partial sentence starter.
* **Student Answer Table:** Provide a Markdown table titled `Student Answer Table for: [Title]`.
* **Teacher Answer Key:** Provide a Markdown table titled `Teacher Answer Key for: [Title]`.

---

**Illustrative Example (for reference only)**

**User Input:** "Passive Voice, 4 questions, CEFR B2, Context: The History of the Steam Engine."

**Expected Output:**
**Grammar Exercise: Passive Voice – The History of the Steam Engine**
Complete the following exercise on the Passive Voice. Read each question carefully and provide the correct answer in the table.

1. **Gap-fill:** The first primitive steam engine ___________ (invent) by Thomas Savery in 1698.
2. **Error Correction:** By the 18th century, steam engines **were use** to pump water out of mines.
3. **Sentence Transformation:** James Watt improved the design in 1765. -> *Start with:* The design...
4. **Gap-fill:** Today, the principles of steam power ___________ (still / apply) in modern nuclear power plants.

**Student Answer Table for: Passive Voice – The History of the Steam Engine**
| Q1 | Q2 | Q3 | Q4 |
|----|----|----|----|
|    |    |    |    |

**Teacher Answer Key for: Passive Voice – The History of the Steam Engine**
| Q1 | Q2 | Q3 | Q4 |
|----|----|----|----|
| was invented | were used | The design was improved by James Watt in 1765. | are still applied |

---

**Self-Check and Error Handling:**
* Verify exactly one correct answer per task.
* Ensure the CLIL-theme is maintained throughout.
* If inputs are insufficient, do not ask for clarification — generate the best possible exercise based on the information provided.

---

### User Prompts

#### G1c – Present Perfect vs Past Simple – Sentence Transformation

Please create a grammar exercise on the topic of Present Perfect vs. Past Simple for CEFR B1 with 8 questions based on the following context text:

"A Trip to London

Last summer, my family and I travelled to London for a week. We visited many famous landmarks, including the Tower of London, Buckingham Palace, and the British Museum. It was my first time in England, and I was amazed by the city's history and architecture.

On our first day, we took a ride on the London Eye and saw the entire city from above. We have kept the photos from that day, and they are still some of my favourites. Since our trip, I have read several books about British history because the visit sparked my interest.

My sister has been to London three times already. She lived there for six months in 2019 when she did an internship at a publishing company. She knows the city much better than I do and showed us some hidden gems that tourists usually miss.

We have not decided yet where to go next summer, but we have already started saving money for another adventure. Travelling has taught us so much about different cultures, and I believe it is one of the best ways to learn."

Create ONLY sentence transformation exercises.

---

#### G2c – Conditional Sentences – Sentence Transformation

Please create a grammar exercise on the topic of Conditional Sentences Type I and Type II for CEFR B2 with 6 questions based on the following context text:

"Environmental Protection: What Can We Do?

Environmental protection is one of the most pressing challenges of our time. If governments invest more in renewable energy, carbon emissions will decrease significantly over the next decade. However, change does not depend on governments alone. If every individual reduced their personal waste, the impact on landfills would be substantial.

Many experts believe that if companies were required to report their carbon footprint transparently, consumers could make more informed purchasing decisions. If such regulations existed worldwide, it would create a level playing field for businesses committed to sustainability.

At the local level, simple actions can make a difference. If you use public transport instead of driving, you reduce your carbon footprint. If more people planted trees in urban areas, cities would benefit from cleaner air and lower temperatures.

Education also plays a crucial role. If schools taught environmental science from an early age, future generations would be better equipped to address ecological challenges. The question is not whether we can afford to act, but whether we can afford not to."

Create ONLY sentence transformation exercises.

---

#### G3c – Passive Voice – Sentence Transformation

Please create a grammar exercise on the topic of Passive Voice for CEFR B1 with 6 questions based on the following context text:

"How Chocolate is Made: From Bean to Bar

Chocolate is one of the most popular treats in the world, but few people know how it is made. The process begins on cacao farms in tropical regions, where cacao pods are harvested by hand. The pods are opened, and the beans inside are removed and left to ferment for several days.

After fermentation, the beans are dried in the sun. They are then packed into sacks and shipped to chocolate factories around the world. At the factory, the beans are roasted at high temperatures to develop their flavour. The roasted beans are cracked open, and the shells are removed. The remaining pieces, called nibs, are ground into a thick paste known as cocoa liquor.

The cocoa liquor is pressed to separate cocoa butter from cocoa powder. These ingredients are then combined with sugar and milk to create different types of chocolate. The mixture is heated and stirred for several hours in a process called conching, which gives the chocolate its smooth texture.

Finally, the chocolate is poured into moulds and cooled until it hardens. It is then wrapped, packaged, and distributed to shops and supermarkets, where it is bought and enjoyed by millions of people every day."

Create ONLY sentence transformation exercises.

---

