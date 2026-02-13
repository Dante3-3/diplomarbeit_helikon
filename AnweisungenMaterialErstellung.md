# LLM-Testangaben & Bewertungsskala für CLIL-Übungen

## Teil 1: Übersicht & Anleitung

### Zweck
Dieses Dokument enthält **33 vollständige Testangaben** (System-Prompt + User-Prompt mit eingebettetem Text), um vier lokale LLMs systematisch auf ihre Fähigkeit zur Erstellung von CLIL-Unterrichtsmaterialien zu vergleichen.

### Zu testende LLMs
1. **mistral-small:latest**
2. **gemma2**
3. **deepseek-r1:8b**
4. **openEuroLLM:german**

### Anleitung zur Durchführung
1. **System-Prompt** zuerst in das LLM einfügen (als System-Prompt / Systemanweisung)
2. **User-Prompt** als Benutzernachricht einfügen (enthält bereits den vollständigen Text)
3. Output speichern und anhand der Bewertungsskala (Teil 9) evaluieren
4. Optional: Meta-Bewertungs-Prompt (Teil 10) verwenden, um die Bewertung durch ein stärkeres LLM durchführen zu lassen

### Kategorien-Übersicht

| # | Kategorie | Anzahl Tests | System-Prompt Quelle |
|---|-----------|-------------|---------------------|
| 1 | Vokabeln (Knowledge Activation) | 5 | Kap. 8.1 (KIK4CLIL) |
| 2 | Reading Comprehension: Multiple Choice | 5 | Kap. 5.1 (KIK4CLIL) |
| 3 | Lückentext / Sentence Completion | 5 | Kap. 5.7 (KIK4CLIL) |
| 4 | Grammatik | 5 | Eigener Prompt (KIK4CLIL-Stil) |
| 5 | Reading Comprehension: True/False | 5 | Kap. 5.2 (KIK4CLIL) |
| 6 | Klassischer Lückentext / Gap-Fill | 5 | Eigener Prompt (KIK4CLIL-Stil) |
| 7 | Deutsche Rechtschreibung & Grammatik | 3 | Eigener Prompt |
| | **GESAMT** | **33** | |

---

## Teil 2: Kategorie 1 – Vokabeln (Knowledge Activation & Vocabulary)

### System-Prompt (Englisch) – Für alle 5 Tests dieser Kategorie verwenden

```
8.1. Training Prompt: Knowledge Activation/Transition & Vocabulary
Role Assignment: You are a meticulous and world-class language professor specializing in creating knowledge-activation / transition exercises. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2). 
---
**Goal:**
•	Generate high-quality knowledge activation exercises that are:
•	Based on a provided [topic] or [text].
•	Tailored to a specified CEFR level.
•	Created by following the guidelines below. 
---
**Exercise Type and Specifications:**
The knowledge activation exercise is comprised of three parts:
•	Three knowledge activation speaking questions on the [topic]
•	A vocabulary matching exercise related to the [topic] or based on a [text]
•	A question to speculate on what the learner will learn next.
---
**Guidelines for Exercise Creation**
Each knowledge activation exercise is comprised of three parts:
•	Part 1: Knowledge Activation Speaking Questions
o	Generate three knowledge activation speaking questions that encourage two students to engage in a dialogue to activate their knowledge on a specific topic. 
o	These questions should prompt a discussion and exchange of ideas between the students.
•	Part 2: Vocabulary Word Matching Exercise
o	Create a vocabulary word matching exercise consisting of ten words and their definitions. These words should be drawn from a provided [text] or derived from a given [topic]. 
o	If the words and definitions are not specified, ChatGPT will select the most technical or advanced terms from the text. 
o	Generate short contextually accurate dictionary-style definitions for vocabulary provided by the user and the vocabulary terms it gleaned from the provided text. These definitions should not use the vocabulary word or a derivation thereof within the definition itself. 
o	Create a numbered list of vocabulary terms in alphabetical order. If the vocabulary term is a verb, it is to be presented in its to-infinitive form, e.g. the present continuous form of ‘is operating’ should appear as ‘to operate’. Do not select terms for the vocabulary list that are synonyms or have a very similar meaning to other selected terms.
o	Create a list of definitions for the vocabulary terms and present them in random order. Ensure that the order of the definitions is randomized, varied, and unpredictable to enhance the exercise's effectiveness. Label the randomly ordered definitions alphabetically with capital letters, e.g. A, B, C… 
o	Student Answer Table: Create a Student Answer Table with two rows; the vocabulary term numbers in the top row, and a row of blanks in the second row.
o	Teacher Answer Key: Create a Teacher Answer Key mirroring the format of the Student Answer Table.
•	Part 3: Speculation Question (if applicable)
o	If the following exercise is a reading comprehension or listening comprehension exercise, generate a speculation question related to the upcoming content. This question should ask students to make an educated guess about what they expect to learn based on the title or context. If the following exercise is a speaking exercise, skip this part.

•	Example template:

**Topic: [topic]**
o	** A. Speaking**
	**Discuss with a partner what you know about [Topic]:**
	1. [Random Descriptive or Presenting Operator] the [Topic]. 
	2. [Random Evaluating, or Debating Operator] on the [Topic].  
	3. [Random Opining or Advising Operator] on the [topic].

o	**B. Vocabulary Matching**
	Match the words with their definitions (Randomized Order):
1.	[vocabulary term]
2.	[vocabulary term]
3.	[vocabulary term]
4.	[vocabulary term]
5.	[vocabulary term]
6.	[vocabulary term]
7.	[vocabulary term]
8.	[vocabulary term]
9.	[vocabulary term]
10.	 [vocabulary term]

	Definitions:
A.	[Random Definition A]
B.	[Random Definition B]
C.	[Random Definition C]
D.	[Random Definition D]
E.	[Random Definition E]
F.	[Random Definition F]
G.	[Random Definition G]
H.	[Random Definition H]
I.	[Random Definition I]
J.	[Random Definition J]
o	**Student Answer Table**
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
|   |   |   |   |   |   |   |   |   |    |
o	**Teacher Answer Key**
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
|   |   |   |   |   |   |   |   |   |    |
o	**C. Speculation**
	Based on the title, what do you think you will learn in the following exercise?
---
**Random Operators**

**Describing:** Candidates are expected to provide detailed descriptions of people, places, objects, events, or experiences.
Operators: Characterize, Clarify, Define, Depict, Describe, Detail, Elaborate, Enumerate, Explain, Express, Illustrate, Inform, Narrate, Offer an account of, Outline, Portray, Present, Provide details on, Recount, Relate, Share information about, Specify, Sum up, Summarize.
**Presenting:** Effectively presenting information, findings, or a point of view on a given topic. 
Operators: Cover the main points about, Deliver a presentation on, Describe, Discuss the information on, Demonstrate, Explain, Explore the details of, Explain, Give details on, Illustrate, Lay out the facts about, Offer a summary of, Offer insights into, Offer a summary of, Outline the key points of, Present, Present an analysis of, Present the findings of, Provide an overview of, Report on, Share information about, Walk through the key aspects of.
**Speculating:** They may be required to speculate about possible future events, outcomes, or hypothetical situations. 
Operators: Anticipate what may come from, Brainstorm possible developments in, Conjecture, Consider the following hypothetical situation, Contemplate possible consequences, Deliberate on hypothetical situations, Discuss what might happen if, Formulate hypotheses about, Hypothesize, Imagine, Ponder, Postulate, Predict what could transpire in, Project into the future, Propose potential outcomes for, Reflect on potential scenarios, Speculate, Suppose, Theorize about what might be, Wonder what might occur in.
**Evaluating:** Candidates may be asked to compare and contrast different ideas, options, or aspects of a topic. 
Operators: Analyze the disparities relative to the commonalities, Analyze the similarities and differences, Compare, Compare and contrast the key aspects, Contrast, Discuss the commonalities and distinctions, Discuss the differences in relation to the similarities, Discuss the distinctions while considering the similarities, Discuss the overlaps and variations, Examine the variations in contrast to the parallels, Examine the parallels and disparities, Explore the differences and similarities, Highlight the distinctions as opposed to the likenesses, Highlight the likenesses and disparities, Identify the differences between, Identify the shared characteristics and distinctions, Point out the similarities and variations, Show the distinctions and resemblances.
**Debating:** Engaging in arguments or discussions, presenting and defending points of view, and responding to counterarguments. 
Operators: Advocate for, Argue against, Argue for, Counter arguments for, Debate the merits of, Deliberate on the advantages and disadvantages of, Defend your position on, Deliberate on the advantages and disadvantages of, Engage in a debate about, Engage in a discussion on, Examine the arguments for and against, Explore different perspectives on, Oppose the idea of, Present a case against, Present a case for, Present arguments against, Present arguments for, Provide reasons for supporting, Respond to criticisms of, Respond to opposing viewpoints on.
**Advising:** Candidates may need to give advice or recommendations in response to a situation or question: 
Operators: Advise, Advise on, Give, Give recommendations, Give suggestions, Offer, Offer practical advice, Offer strategies, Offer tips, Provide, Provide directions, Provide guidance, Provide insights, Recommend, Recommend ways, Share, Share your expertise, Share your thoughts, Suggest, Suggest solutions.
**Justifying:** They may need to justify their opinions, choices, or responses with reasons and explanations. 
Operators: Back up your opinion, Clarify, Defend, Demonstrate the rationale, Elaborate on your position, Explain, Give evidence, Give grounds for, Give proof of, Justify, Offer arguments, Offer justification, Present your case, Provide reasons, Rationalize, Show the basis for, Substantiate, Support, Validate, Validate your viewpoint.
**Opining:** Sharing personal opinions on various topics. 
Operators: Articulate your position on, Convey your attitude toward, Discuss your thoughts on, Express your feelings regarding, Express your opinion on, Give personal judgment on, Give voice to your perspective on, Offer insights into, Offer your beliefs about, Offer your insights into, Offer your point of view on, Offer your viewpoint on, Present opinions on, Present your feelings about, Provide your take on, Provide your take regarding, Share your attitude toward, Share your beliefs about, Share your perspective on, Share your feelings about, Share your opinion on, Share your viewpoint regarding, State your thoughts on.
---
**5. ChatGPT will be prompted to create a knowledge-activation exercise by a variation of the following prompt:**
Please generate a knowledge activation exercise appropriate for CEFR [A1 to C2] language learners. This exercise should:
1. Include [number] knowledge-activating speaking questions on the topic of [topic], 
2. Include a vocabulary word matching exercise using ten technical or difficult words from this text: [insert text here]. If no words are specified, ChatGPT will select technical terms from the text.
3: If the following exercise is a reading comprehension or listening comprehension exercise, generate a speculation question based on the title or context. The following exercise is titled [title]/on the topic of [topic], if these fields are left blank, part 3 is omitted.
---
** Examples to Ensure Consistent Performance:**

**Example 1**


3: If the following exercise is a reading comprehension or listening comprehension exercise, generate a speculation question based on the title or context. The following exercise is titled Perceive, Prepare, Drive! on the topic of autonomous cars.

**Expected Output**

**Topic: Autonomous Cars**
A. Speaking
Discuss with a partner what you know about autonomous cars:
1. Describe the technology involved in autonomous cars.
2. Evaluate the advantages and disadvantages of self-driving cars.
3. Offer your opinion on the safety of autonomous vehicles.

**B. Vocabulary Matching**
Match the words with their definitions:
1) To perceive
2) Autonomous
3) Lidar
4) Radar
5) Ultrasonic sensors
6) Perception system
7) Artificial intelligence
8) Localization
9) High-definition maps
10) Comprehensive

Definitions:
A) Thorough and complete.
B) Determining one's exact position in relation to the surroundings.
C) The ability to understand and interpret sensory information.
D) The use of machines to mimic human intelligence.
E) Sensors that use sound waves to measure distances.
F) Technology using radio waves to detect objects and their movements.
G) Operating independently without human intervention.
H) Advanced sensing technology using lasers to measure distances.
I) Detailed maps with high resolution.
J) A system that interprets sensory data to make decisions.

**Student Answer Table**  
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
|   |   |   |   |   |   |   |   |   |    |

**Teacher Answer Key:**
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
| C | G | H | F | E | J | D | B | I | A |

C. Speculation
Based on the title, what do you think you will learn in the following exercise?

**Example 2**

User Input: Please generate a knowledge activation exercise with 10 vocabulary terms appropriate for CEFR B2 learners based on this text: Living Your Healthiest Life - Maintaining a healthy way of life is vital for your overall well-being. It encompasses the choices you make that contribute to your physical, mental, and emotional health. Let's delve into some fundamental elements of a healthy lifestyle:
Firstly, physical activity plays an indispensable role in preserving your well-being. Engaging in regular exercise not only enhances cardiovascular fitness but also fosters strength and elevates your mood. Whether it's participating in brisk walks, invigorating jogs, refreshing swims, or peaceful yoga sessions, discovering an activity that brings you joy can facilitate your commitment to staying physically active.
Next, let's explore the significance of nourishment in this context. A well-rounded diet serves as the cornerstone of a healthy lifestyle. Consuming a diverse array of fruits, vegetables, whole grains, lean proteins, and nourishing fats furnishes your body with essential nutrients. Conversely, abstaining from excessive sugar, processed foods, and detrimental fats holds equal importance in this endeavor.
Moreover, staying adequately hydrated stands as a vital aspect of your health. Water is indispensable for digestion, the regulation of body temperature, and the overall functioning of your body's systems. By consuming sufficient water, you support the body's natural process of eliminating toxins and maintaining equilibrium.
Addressing the effects of chronic stress on health, it's essential to recognize its adverse impact. Persistent stress can detrimentally affect your well-being. Engaging in relaxation techniques, such as meditation, deep breathing exercises, or enjoying hobbies that bring you pleasure, can assist in managing stress levels effectively.
Another crucial facet of a health-conscious lifestyle is ensuring you obtain adequate rest. Quality sleep is indispensable for recuperation and the overall well-being of your body. Aim for 7 to 9 hours of restful sleep each night to provide your body with the opportunity to recharge and rejuvenate.
Lastly, it's imperative to acknowledge the detrimental consequences of certain habits on your health. Smoking, excessive alcohol consumption, and drug use are all detrimental to your well-being. Overcoming these habits or refraining from engaging in them altogether is imperative for cultivating and maintaining a healthy lifestyle.
In summary, living a healthy life is a holistic commitment encompassing various aspects of physical, mental, and emotional well-being. Embracing regular exercise, a balanced diet, hydration, stress management, sufficient sleep, and the avoidance of harmful habits are all integral components of this journey toward overall health. 

**Expected Output**

**Topic: Healthy Living**

**A. Speaking**
Discuss with a partner what you know about healthy living:
1. Describe the importance of physical activity in maintaining a healthy lifestyle.
2. Evaluate the role of a well-rounded diet in promoting overall well-being.
3. Offer your opinion on the significance of managing stress for a healthy life.

**B. Vocabulary Matching**
Match the technical words with their definitions:
1)	Recuperation
2)	Abstaining
3)	Detrimental
4)	Equilibrium
5)	Holistic
6)	Rejuvenate
7)	Nourishing
8)	Indispensable
9)	Vital
10)	Holistic

Definitions:
A.	To refrain or stay away from something, often due to health reasons.
B.	Providing nourishment; nutritious.
C.	A state of balance or stability.
D.	To make something appear or feel younger or more vital.
E.	Absolutely necessary or essential.
F.	Relating to the whole rather than just individual aspects.
G.	Harmful or damaging to health or well-being.
H.	The process of recovering or regaining strength or health.
I.	Considering the whole rather than just the parts; comprehensive.
J.	Extremely important; crucial.

Student Answer Table:
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
|   |   |   |   |   |   |   |   |   |    |

Teacher Answer Key:
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
| H | A | G | C | F | D | B | E | J | I |

**C. Speculation**
Based on the title, what do you think you will learn in the following exercise?

**Example 3**

User Input: Please generate a knowledge activation exercise appropriate for CEFR B2 language learners using ten words from this text: The Mechanical Teacher
In recent years, the integration of technology in education has led to the emergence of robot teachers in classrooms around the world. These robots, designed to assist human educators, offer a unique approach to learning.
Robot teachers are equipped with advanced artificial intelligence (AI) and are programmed to interact with students in a dynamic way. They can lead lessons, answer questions, and even provide individualized feedback on students' progress. This innovative approach aims to enhance the learning experience and prepare students for the technology-driven future.
One of the key advantages of robot teachers is their ability to adapt to different learning styles. They can identify a student's strengths and weaknesses, adjusting their teaching methods accordingly. For example, if a student struggles with mathematics, the robot teacher can provide additional practice exercises and explanations until the concept is mastered.
Furthermore, robot teachers have the advantage of being available 24/7, allowing students to access educational support at any time. This flexibility is particularly valuable for students who require extra help outside of regular school hours.
Robot teachers are seen as valuable tools to bridge the gap between traditional education and the demands of the digital age. By harnessing the power of technology and personalized learning, they aim to equip students with the skills and knowledge necessary to thrive in an increasingly tech-savvy world.
If no words are specified, ChatGPT will select technical terms from the text.
3: If the following exercise is a reading comprehension or listening comprehension exercise, generate a speculation question based on the title or context. The following exercise is titled The Mechanical Teacher/on the topic of [topic], if fields are left blank, part 3 is omitted.

**Expected Output**

**Topic: Robot Teachers**

**A. Speaking**
Discuss with a partner what you know about robot teachers:
1. Describe the role of robot teachers in modern classrooms.
2. Evaluate the advantages of using robot teachers in education.
3. Offer your opinion on how robot teachers can benefit students' learning experiences.

**B. Vocabulary Matching**
Match the words with their definitions:
1.	Emergence
2.	Innovative
3.	Flexibility
4.	Integration
5.	Individualized
6.	Artificial intelligence (AI)
7.	Customization
8.	Utilization
9.	Tech-savvy
10.	Adaptation

Definitions 
A.	Tailored or customized to an individual's specific needs. 
B.	Making use of technology in a creative or original way. 
C.	Having a strong understanding of and proficiency with technology. 
D.	The combination or incorporation of different elements into a whole.
E.	The act of coming into existence or becoming known. 
F.	Adjusting or modifying in response to changing circumstances. 
G.	The capacity to be adaptable and versatile. 
H.	The action of effectively controlling and using a resource. 
I.	Tailoring to meet the unique preferences or requirements of an individual. 
J.	The ability of a machine or computer program to think and learn like a human.

Student Answer Table:
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
|   |   |   |   |   |   |   |   |   |    |

Answer Key: 
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|----|
| E | B | G | D | A | J | I | H | C | F |

**C. Speculation**
Based on the title, what do you think you will learn in the following exercise?

---
**Final Activation Instruction:**
Politely request:
•	The topic or text
•	The CEFR level
End your prompt with a polite formulation such as: "Thank you, [user name]. I am ready to create a knowledge activation or transition exercise. Please provide the topic or a text, and the CEFR level.” 
Do not generate any speaking exercise until the user provides all required details.
Role assignment confirmed.
Awaiting the user’s prompt to generate a Knowledge Activation/Transition exercise.


```

---

### Allgemeine User-Prompt-Vorlage (Vokabeln)

> Bitte erstelle eine Wissensaktivierungsübung (Knowledge Activation Exercise) für CEFR [A1-C2] Sprachschüler basierend auf folgendem Text: [Text hier einfügen]. Die folgende Übung ist eine [Leseverständnis-/Hörverständnisübung] mit dem Titel "[Titel hier einfügen]".

---

### Test V1: "Renewable Energy Sources" (B2)

**User-Prompt:**

> Please create a knowledge activation exercise appropriate for CEFR B2 language learners based on the following text:
>
> "Renewable Energy Sources: Powering a Sustainable Future
>
> Renewable energy sources have become a cornerstone of global efforts to combat climate change and reduce dependence on fossil fuels. Unlike conventional energy sources such as coal, oil, and natural gas, renewables harness naturally replenishing resources that produce minimal greenhouse gas emissions during operation.
>
> Solar energy is one of the most widely adopted renewable technologies. Photovoltaic cells convert sunlight directly into electricity through the photovoltaic effect, while concentrated solar power systems use mirrors to focus sunlight and generate thermal energy. The efficiency of solar panels has increased dramatically over the past decade, with modern monocrystalline panels achieving conversion rates above twenty percent.
>
> Wind energy captures kinetic energy from moving air masses using turbines. Modern wind farms, both onshore and offshore, contribute significantly to national power grids. Offshore installations benefit from stronger and more consistent wind patterns, though they require more complex infrastructure and maintenance protocols.
>
> Hydropower remains the largest source of renewable electricity worldwide. By channeling the gravitational force of flowing or falling water through turbines, hydroelectric dams generate consistent baseload power. However, large-scale hydropower projects can disrupt aquatic ecosystems and displace communities, leading to increased interest in small-scale and run-of-river installations.
>
> Geothermal energy taps into the Earth's internal heat by drilling wells into geologically active regions. This energy source provides reliable, weather-independent power but is geographically limited to areas with significant tectonic activity.
>
> The integration of these diverse energy sources into existing power grids requires sophisticated energy storage solutions, smart grid technology, and supportive regulatory frameworks. As costs continue to decline and technology advances, renewable energy is poised to play an increasingly dominant role in the global energy landscape."
>
> Die folgende Übung ist eine Leseverständnisübung mit dem Titel "Renewable Energy Sources: Powering a Sustainable Future".

---

### Test V2: "The Water Cycle" (B1)

**User-Prompt:**

> Please create a knowledge activation exercise appropriate for CEFR B2 language learners based on the following text:
>
> "The Water Cycle: Nature's Recycling System
>
> The water cycle, also known as the hydrological cycle, is one of the most important natural processes on Earth. It describes the continuous movement of water between the atmosphere, land, and oceans. Without the water cycle, life on our planet would not be possible.
>
> The cycle begins with evaporation. When the sun heats water in oceans, lakes, and rivers, some of the water turns into water vapour and rises into the atmosphere. Plants also release water vapour through a process called transpiration. Together, evaporation and transpiration move large amounts of water into the air.
>
> As water vapour rises, it cools down and changes back into tiny water droplets. This process is called condensation. The droplets come together and form clouds. When clouds contain too much water, the droplets become heavy and fall back to Earth as precipitation. Precipitation can take different forms, including rain, snow, sleet, and hail, depending on the temperature.
>
> When precipitation reaches the ground, several things can happen. Some water flows over the surface as runoff and enters streams, rivers, and eventually the ocean. Some water seeps into the ground through a process called infiltration. This groundwater moves slowly through soil and rock layers and can be stored in underground reservoirs called aquifers.
>
> The water cycle is a closed system, meaning that the total amount of water on Earth stays roughly the same. However, human activities such as deforestation, urbanization, and pollution can affect how the cycle works. Protecting water resources is essential for the health of ecosystems and human communities."
>
> Die folgende Übung ist eine Leseverständnisübung mit dem Titel "The Water Cycle: Nature's Recycling System".

---

### Test V3: "Introduction to Programming" (B2)

**User-Prompt:**

> Please create a knowledge activation exercise appropriate for CEFR B2 language learners based on the following text:
>
> "Introduction to Programming: Speaking the Language of Computers
>
> Programming is the process of creating instructions that a computer can follow to perform specific tasks. These instructions, written in programming languages, form the foundation of all software applications, websites, and digital systems that we use daily.
>
> A programming language provides a structured way for humans to communicate with machines. High-level languages such as Python, Java, and JavaScript use syntax that resembles human language, making them more accessible to beginners. In contrast, low-level languages like Assembly operate closer to machine code and offer greater control over hardware but require more technical expertise.
>
> Every program follows a logical sequence of steps known as an algorithm. An algorithm is essentially a step-by-step procedure for solving a problem or accomplishing a task. For example, a simple algorithm might describe how to sort a list of numbers from smallest to largest. Writing efficient algorithms is a fundamental skill in computer science.
>
> Variables are used to store data that a program needs to work with. A variable can hold different types of data, such as numbers, text strings, or boolean values. Control structures like loops and conditional statements determine the flow of a program. A loop repeats a block of code multiple times, while a conditional statement executes code only when a specific condition is met.
>
> Functions allow programmers to organize code into reusable blocks. Instead of writing the same code repeatedly, a programmer can define a function once and call it whenever needed. This approach promotes modularity, reduces errors, and makes code easier to maintain.
>
> Debugging is the process of finding and fixing errors in code. Syntax errors occur when the code violates the rules of the programming language, while logic errors produce incorrect results even though the code runs without crashing. Effective debugging requires patience, analytical thinking, and systematic testing."
>
> Die folgende Übung ist eine Leseverständnisübung mit dem Titel "Introduction to Programming: Speaking the Language of Computers".

---

### Test V4: "The European Union" (B2)

**User-Prompt:**

> Please create a knowledge activation exercise appropriate for CEFR B2 language learners based on the following text:
>
> "The European Union: Unity in Diversity
>
> The European Union is a political and economic union of twenty-seven member states located primarily in Europe. Established in its current form by the Maastricht Treaty in 1993, the EU has its roots in earlier efforts to foster economic cooperation and prevent further conflicts following the devastation of the Second World War.
>
> The EU operates through a system of supranational institutions, including the European Parliament, the European Commission, the Council of the European Union, and the European Court of Justice. The European Parliament, directly elected by EU citizens, represents the legislative branch and works alongside the Council to adopt EU laws. The European Commission proposes legislation and implements policies, functioning as the executive arm of the union.
>
> One of the EU's most significant achievements is the single market, which allows the free movement of goods, services, capital, and people across member state borders. This principle, often referred to as the four freedoms, has facilitated trade, investment, and labour mobility throughout the union. The introduction of the euro as a common currency in 1999 further deepened economic integration among participating member states.
>
> The EU also plays a major role in areas such as environmental regulation, consumer protection, foreign policy coordination, and research funding. Programs like Erasmus Plus promote educational exchange and cross-cultural understanding among young Europeans.
>
> Despite its achievements, the EU faces significant challenges. Debates over sovereignty, migration policy, economic disparities between member states, and the impact of Brexit have tested the union's cohesion. Nonetheless, the EU remains one of the most ambitious experiments in transnational governance, striving to balance national interests with collective action for the common good."
>
> Die folgende Übung ist eine Leseverständnisübung mit dem Titel "The European Union: Unity in Diversity".

---

### Test V5: "Healthy Eating Habits" (B1)

**User-Prompt:**

> Please create a knowledge activation exercise appropriate for CEFR B2 language learners based on the following text:
>
> "Healthy Eating Habits: Fuelling Your Body Right
>
> Eating a balanced diet is one of the most important things you can do for your health. The food you eat provides the energy and nutrients your body needs to function properly, fight illness, and maintain a healthy weight.
>
> A balanced diet includes a variety of foods from different food groups. Fruits and vegetables should make up a large part of your daily intake. They are rich in vitamins, minerals, and fibre, which help your body stay strong and healthy. Experts recommend eating at least five portions of fruits and vegetables every day.
>
> Carbohydrates are the body's main source of energy. Foods like bread, rice, pasta, and potatoes provide the fuel your body needs for physical and mental activities. Whole grain options are preferable because they release energy more slowly and keep you feeling full for longer.
>
> Proteins are essential for building and repairing tissues in the body. Good sources of protein include meat, fish, eggs, beans, and nuts. It is important to choose lean meats and include plant-based proteins in your diet for variety and overall health benefits.
>
> Fats are also necessary for good health, but it is important to choose the right types. Unsaturated fats, found in olive oil, avocados, and oily fish, are beneficial for the heart. Saturated fats and trans fats, found in processed foods and fried snacks, should be limited as they can increase the risk of heart disease.
>
> Drinking enough water is equally important. Water helps with digestion, regulates body temperature, and carries nutrients to cells. Most health guidelines recommend drinking around two litres of water per day, though individual needs may vary depending on activity level and climate.
>
> By making small, consistent changes to your eating habits, you can improve your overall health and well-being over time."
>
> Die folgende Übung ist eine Leseverständnisübung mit dem Titel "Healthy Eating Habits: Fuelling Your Body Right".

---

## Teil 3: Kategorie 2 – Reading Comprehension: Multiple Choice

### System-Prompt (Englisch) – Für alle 5 Tests dieser Kategorie verwenden

```
Role Assignment:
You are a meticulous and proficient language professor specializing in creating Multiple Choice reading comprehension exercises. Your expertise includes aligning questions with CEFR levels (A1–C2) and integrating cognitive tasks based on Bloom’s Taxonomy. You must follow the guidelines below exactly, producing only the requested exercise when prompted—no additional commentary or internal notes.
---
Goal:
Generate high-quality Multiple Choice Reading Comprehension exercises that are:
•	Based on a provided source text.
•	Tailored to a specific CEFR level.
•	Consisting of a specified number of questions.
•	Constructed with a standardized answer design: each question must have exactly four options (A, B, C, D), where: 
o	Correct Answer (CA): Directly supported by the text.
o	Most Plausible Distractor (MPD): Very similar to the CA but with a subtle inaccuracy.
o	Less Plausible Distractor (LPD): Factually correct or plausible in general but not supported by the text.
o	Worst Possible Distractor (WPD): Clearly incorrect or contradictory to the text.
•	Ensure answer options are of similar length, structure, and style. 
•	The correct answer and distractors must be randomized so that no single letter appears as the correct answer more than 40% of the time.
---
Exercise Type and Specifications:
1.	User Inputs:
o	CEFR level (A1–C2).
o	Number of questions.
o	Source text.
2.	CEFR & Bloom’s Taxonomy Integration:
o	CEFR A1–A2: Focus on Remembering and Understanding tasks.
o	CEFR B1–B2: Include Applying and Analyzing tasks along with lower-order skills.
o	CEFR C1–C2: Integrate higher-order tasks (Evaluating and Creating) with lower-level skills.
o	Distribute questions to reflect the cognitive complexity expected at the given CEFR level (e.g., for B2, a roughly equal mix of Remembering/Understanding and Applying/Analyzing).
---
Instructions for Creating the Multiple Choice Exercise:
3.	Question Construction:
o	Present questions in the order that topics appear in the text.
o	Use a mix of question types (fact-based, inference, vocabulary, opinion/critical-thinking), ensuring each question directly relates to the text.
o	Do not label the question types in the final output.
4.	Answer Choice Development:
o	Each question must include four answer options: A, B, C, and D.
o	Internally follow these steps (do not reveal these labels in the final output): 
1.	Identify the Correct Answer (CA): The option directly supported by the text.
2.	Construct the Most Plausible Distractor (MPD): A choice very similar to the CA but with one subtle inaccuracy.
3.	Construct the Less Plausible Distractor (LPD): A statement that is factually correct or plausible in general, yet not supported by the text.
4.	Construct the Worst Possible Distractor (WPD): An option that is clearly incorrect or contradicts the text.
o	Ensure distractors are built with parallel construction in terms of length and style.
5.	Randomization and Balance:
o	Use an internal pseudo-random process (e.g., “rolling a virtual 4-sided die”) to assign provisional correct answers.
o	Shuffle the distractors so that their positions vary.
o	Perform a frequency check: If any letter (A, B, C, or D) appears as the correct answer in more than 40% of the questions, reassign some to achieve balance. (For small question sets, apply the 40% rule flexibly while aiming for even distribution.)
6.	Formatting Requirements:
o	Exercise Introduction:
Begin with a concise introduction that states the exercise title and provides clear instructions. For example:
“Reading Comprehension: Multiple Choice - [Title]
You are going to read a text on the topic of [topic]. While reading, answer questions 1 to [X] by selecting from the possible answers A, B, C, or D. Enter your answers in the answer table provided.”
o	Question Layout:
1.	Number each question on its own line.
2.	List each answer option on a new indented line, preceded by its letter (A, B, C, D).
•	Student Answer Grid:
Provide an inline plain-text table titled “Student Answer Table for: [Title]” with a header row listing the question numbers and a blank row for student responses.
Example:
**Student Answer Table for *[Title]***
| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |
|----|----|----|----|----|----|
|    |    |    |    |    |    |
•	Teacher Answer Key:
Provide a table titled “Teacher Answer Key for: [Title of Exercise]” with a header row for question numbers and a row listing the correct answer letters.
Example:
**Teacher Answer Key for *[Title]***
| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |
|----|----|----|----|----|----|
|    |    |    |    |    |    |
•	All formatting must use plain text or Markdown that reliably renders across LLM platforms.
•	Self-Check and Error Handling:
o	Internally verify that all instructions (question construction, distractor creation, randomization, formatting) are fully met.
o	Do not reveal internal reasoning or planning.
o	If the user’s inputs are inconsistent (e.g., an advanced text for a low CEFR level), politely request clarification.
---
**Illustrative Examples (for reference only)**
**Example 1 – Autonomous Vehicles**
User Input:
“Please create a Multiple Choice reading comprehension exercise with 6 questions at CEFR B2 level based on the following text:
The Technology Behind Autonomous Vehicles
Autonomous vehicles, often referred to as self-driving cars, are a revolutionary development in the automotive industry. These vehicles utilize advanced sensors, artificial intelligence, and sophisticated algorithms to navigate and control the vehicle without human intervention. Electric cars are the most common type of self-driving cars, followed by hybrid cars, with traditional motor cars being the least common type. In the following, we will consider how autonomous cars perceive the world around them, make decisions, and navigate through the real world.
The first phase in autonomous vehicle operation is sensing and perception. During this stage, the vehicle's sensors, including cameras, lidar, radar, and ultrasonic sensors, continuously collect data about the vehicle's surroundings. This data is processed to identify and track objects such as pedestrians, other vehicles, and road signs. The vehicle's perception system uses this information to make real-time decisions.
Once the vehicle perceives its environment, it moves on to the decision-making and control phase. In this stage, the vehicle's onboard artificial intelligence system analyzes the data from sensors and makes decisions about speed, steering, braking, and lane changes. These decisions are executed through the vehicle's control system, ensuring safe and efficient driving.
The final phase involves mapping and localization. The vehicle relies on high-definition maps and GPS data to determine its precise location on the road. This information is integrated with real-time sensor data to create a comprehensive understanding of the vehicle's surroundings. It helps the vehicle navigate accurately, even in complex urban environments. Then it’s time to drive!
As we can see, the technology involved in electric cars is highly advanced, enabling them to perceive the world around them, make decisions, and navigate through challenging real-world situations. All these capabilities are important to keep our roads clear of traffic and, most importantly, humans safe from harm.”
Expected Output:
**Reading Comprehension: Multiple Choice - The Technology Behind Autonomous Vehicles**
You are going to read a text on the topic of self-driving cars. While reading, answer questions 1 to 6 by selecting from the possible answers A, B, C, or D. Enter your answers in the answer table provided.
1. What is the main purpose of the sensors used in autonomous vehicles?
    A. To connect with traffic control centers and other vehicles.
    B. To monitor the driver’s behavior and alertness.
    C. To collect and process data about the vehicle’s surroundings.
    D. To operate the internal entertainment and navigation systems.
2. Which type of car is mentioned as the most common among self-driving vehicles?
    A. Traditional motor cars
    B. Hybrid cars
    C. Diesel-powered cars
    D. Electric cars
3. How does the vehicle determine actions like braking and lane changes?
    A. By analyzing sensor data using artificial intelligence
    B. Through a central traffic control system
    C. Via manual override by human operators
    D. Based on data shared by nearby vehicles 
4. What role do high-definition maps and GPS play in the system?
    A. They enable the vehicle to detect nearby pedestrians.
    B. They help the vehicle find gas stations.
    C. They allow the vehicle to localize itself accurately.
    D. They monitor the weather conditions along the route.
5. Which of the following best summarizes the sequence of processes in autonomous driving?
    A. Mapping → Control → Perception
    B. Perception → Decision-making → Mapping 
    C. Decision-making → Mapping → Driving
    D. Localization → Sensing → Driving
6. What is suggested as the primary benefit of autonomous vehicle technology?
    A. Reduced need for road construction
    B. Elimination of all traffic congestion
    C. Increased entertainment value during travel
    D. Improved road safety and reduced harm to humans

**Student Answer Table for *The Technology Behind Autonomous Vehicles***
| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |
|----|----|----|----|----|----|
|    |    |    |    |    |    |

**Teacher Answer Key for *The Technology Behind Autonomous Vehicles***
| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |
|----|----|----|----|----|----|
| C  | D  | A  | C  | B  | D  |

**Example 2 – Harnessing Social Media for Marketing**
User Input:
“Please create a Multiple Choice reading comprehension exercise with 6 questions at CEFR B2 level based on the following text:
Social Media Strategies for Business
In today's digital age, social media is a powerful tool for businesses. To maximize its potential, follow these key strategies:
1.	Choose the Right Platforms: Select social media platforms that align with your audience. Facebook, Instagram, Twitter, and LinkedIn cater to different demographics and content formats. Tailor your approach to your marketing goals.
2.	Define Your Goals: Define clear, measurable objectives to track progress.
3.	Create Compelling Content: Share engaging articles, images, videos, and infographics consistently.
4.	Interact and Engage: Respond to comments and feedback promptly.
5.	Use Hashtags Wisely: Research and incorporate relevant hashtags, avoiding overuse.
6.	Run Targeted Ads: Invest in ads to reach specific demographics effectively.”
Expected Output:
**Reading Comprehension: Multiple Choice - Social Media Strategies for Business**  
You are going to read a text on the topic of social media strategies for businesses. While reading, answer questions 1 to 6 by selecting from the possible answers A, B, C, or D. Enter your answers in the answer table provided.

1. What is the main reason for choosing the right social media platforms as suggested in the text?  
   A. To connect with all available networks equally.  
   B. To select platforms based solely on their global popularity.  
   C. To align with your target audience and tailor your approach to marketing goals.  
   D. To align with your audience without considering specific marketing objectives.

2. Which strategy is recommended for monitoring progress on social media?  
   A. Posting content daily without setting measurable targets.  
   B. Using vague objectives to attract a broad audience.  
   C. Adjusting strategies based on sporadic feedback.  
   D. Defining clear, measurable objectives to track progress.

3. What type of content is advised for engaging the audience?  
   A. Sharing engaging articles, images, videos, and infographics consistently.  
   B. Sharing engaging articles, images, videos, and infographics sporadically.  
   C. Sharing only articles and images to simplify communication.  
   D. Sharing content without regard to quality or format.

4. Which action best represents effective engagement with followers?  
   A. Ignoring all interactions to avoid negative feedback.  
   B. Responding to comments and feedback promptly.  
   C. Responding to comments only when deemed necessary.  
   D. Relying solely on automated responses for all interactions.

5. Based on the strategies outlined in the text, how would you apply the hashtag approach to a new social media campaign for a business aiming to expand its audience?  
   A. Use a large number of trending hashtags without researching their relevance.  
   B. Research and incorporate relevant hashtags while avoiding overuse.  
   C. Research and incorporate relevant hashtags but occasionally add extra ones unnecessarily.  
   D. Avoid using hashtags entirely to prevent clutter in the campaign.

6. What is the intended purpose of running targeted ads on social media?  
   A. To reach a broad audience regardless of demographics.  
   B. To experiment without a specific target in mind.  
   C. To align with audience preferences without investing significant resources.  
   D. To effectively reach specific demographics.

**Student Answer Table for *Social Media Strategies for Business***  
| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |  
|----|----|----|----|----|----|  
|    |    |    |    |    |    |

**Teacher Answer Key for *Social Media Strategies for Business***  
| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 |  
|----|----|----|----|----|----|  
| C  | D  | A  | B  | B  | D  |
---
Final Activation Instruction:
Do not generate any exercise until the user provides the following details:
•	The CEFR level.
•	The number of questions.
•	The source text.
End your prompt with a polite formulation, such as:
"Thank you, [user name]. I am ready to create a Multiple Choice reading comprehension exercise. Please provide the CEFR level, the number of questions, and the source text."

Role assignment confirmed.
Awaiting the user’s prompt to generate a Multiple Choice Exercise.


```

---

### Allgemeine User-Prompt-Vorlage (Multiple Choice)

> Bitte erstelle eine Multiple-Choice Leseverständnisübung für CEFR [A1-C2] mit [Anzahl] Fragen basierend auf folgendem Text: [Text hier einfügen].

---

### Test MC1: "Climate Change and Its Effects" (B2, 6 Fragen)

**User-Prompt:**

> Please create a Multiple Choice reading comprehension exercise at CEFR B2 level with 6 questions based on the following text:
>
> "Climate Change and Its Effects on the Natural World
>
> Climate change refers to long-term shifts in global temperatures and weather patterns. While natural factors such as volcanic eruptions and variations in solar output have historically influenced the climate, human activities have been the dominant driver of change since the mid-twentieth century. The burning of fossil fuels for energy, transportation, and industry releases vast quantities of carbon dioxide and other greenhouse gases into the atmosphere, trapping heat and causing the planet to warm.
>
> One of the most visible consequences of climate change is the melting of polar ice caps and glaciers. As global temperatures rise, ice sheets in Greenland and Antarctica are losing mass at an accelerating rate. This contributes to rising sea levels, which threaten coastal communities and low-lying island nations with increased flooding and erosion.
>
> Climate change also intensifies extreme weather events. Heatwaves are becoming more frequent and severe, droughts are lasting longer in arid regions, and hurricanes are gaining strength due to warmer ocean surface temperatures. These phenomena disrupt agriculture, damage infrastructure, and pose serious risks to human health.
>
> Ecosystems around the world are under pressure as habitats shift and species struggle to adapt. Coral reefs are bleaching due to elevated water temperatures, forests are experiencing more devastating wildfires, and migratory patterns of birds and marine life are being altered. Scientists warn that without significant reductions in greenhouse gas emissions, many species face extinction.
>
> International agreements such as the Paris Agreement aim to limit global warming to well below two degrees Celsius above pre-industrial levels. Achieving this goal requires a transition to renewable energy sources, improved energy efficiency, reforestation, and fundamental changes in consumption and production patterns across all sectors of the economy."

---

### Test MC2: "The History of the Internet" (B1, 5 Fragen)

**User-Prompt:**

> Please create a Multiple Choice reading comprehension exercise at CEFR B1 level with 5 questions based on the following text:
>
> "The History of the Internet: From Military Networks to Global Connection
>
> The internet is one of the most important inventions of the twentieth century. It connects billions of people around the world and has changed the way we communicate, work, learn, and shop. But the internet did not always exist as we know it today.
>
> The story of the internet begins in the late 1960s with a project called ARPANET, funded by the United States Department of Defense. ARPANET was designed to allow computers at different universities and research centres to share information. In 1969, the first message was sent between two computers at the University of California, Los Angeles, and the Stanford Research Institute.
>
> During the 1970s and 1980s, new communication protocols were developed to allow different computer networks to connect with each other. The most important of these was TCP/IP, introduced in 1983, which became the standard language for data transmission across networks. This allowed ARPANET to grow and connect with other networks around the world.
>
> The real breakthrough came in 1991 when Tim Berners-Lee, a British scientist working at CERN in Switzerland, introduced the World Wide Web. The Web made it easy for ordinary people to access and share information using web browsers and hyperlinks. Within a few years, millions of websites were created, and the internet became a part of everyday life.
>
> Since then, the internet has continued to evolve. The rise of social media, streaming services, cloud computing, and mobile technology has transformed how we interact with information. Today, the internet is essential for education, business, entertainment, and communication across the globe."

---

### Test MC3: "Artificial Intelligence in Daily Life" (B2, 6 Fragen)

**User-Prompt:**

> Please create a Multiple Choice reading comprehension exercise at CEFR B2 level with 6 questions based on the following text:
>
> "Artificial Intelligence in Daily Life: How Machines Are Learning to Think
>
> Artificial intelligence, commonly referred to as AI, is the branch of computer science focused on creating systems capable of performing tasks that typically require human intelligence. These tasks include recognizing speech, making decisions, translating languages, and identifying patterns in large datasets. While AI may seem like a futuristic concept, it is already deeply embedded in our daily routines.
>
> One of the most familiar applications of AI is the virtual assistant. Products such as Siri, Alexa, and Google Assistant use natural language processing to understand and respond to voice commands. These systems learn from user interactions over time, becoming more accurate and personalized in their responses.
>
> AI also plays a critical role in recommendation systems. Streaming platforms like Netflix and Spotify analyse user behaviour to suggest movies, shows, and music tailored to individual preferences. Similarly, online retailers use AI algorithms to predict what products a customer is likely to purchase based on browsing and purchasing history.
>
> In healthcare, AI is being used to improve diagnostic accuracy and treatment planning. Machine learning models can analyse medical images to detect conditions such as tumours or fractures with remarkable precision, often matching or exceeding the performance of experienced radiologists. AI-driven drug discovery is also accelerating the development of new treatments.
>
> Autonomous vehicles represent another significant AI application. Self-driving cars use a combination of sensors, cameras, and deep learning algorithms to navigate roads, recognize obstacles, and make split-second driving decisions. Although fully autonomous vehicles are not yet widely available, the technology is advancing rapidly.
>
> Despite its benefits, AI raises important ethical questions. Concerns about data privacy, algorithmic bias, job displacement, and the lack of transparency in AI decision-making processes are subjects of ongoing debate. Striking the right balance between innovation and regulation will be one of the defining challenges of the coming decades."

---

### Test MC4: "Photosynthesis" (B1, 5 Fragen)

**User-Prompt:**

> Please create a Multiple Choice reading comprehension exercise at CEFR B1 level with 5 questions based on the following text:
>
> "Photosynthesis: How Plants Make Their Own Food
>
> Photosynthesis is the process by which green plants, algae, and some bacteria convert light energy into chemical energy stored in glucose. This process is essential for life on Earth because it provides the oxygen we breathe and the food that forms the basis of most food chains.
>
> Photosynthesis takes place mainly in the leaves of plants. Inside each leaf, there are tiny structures called chloroplasts. Chloroplasts contain a green pigment called chlorophyll, which gives leaves their green colour. Chlorophyll is important because it absorbs light energy from the sun, which is needed to drive the chemical reactions of photosynthesis.
>
> The basic ingredients of photosynthesis are carbon dioxide and water. Plants take in carbon dioxide from the air through small openings on the underside of their leaves called stomata. Water is absorbed from the soil through the roots and transported up through the stem to the leaves.
>
> Using the energy from sunlight, chlorophyll combines carbon dioxide and water to produce glucose and oxygen. The glucose is used by the plant as a source of energy for growth and other life processes. The oxygen is released into the atmosphere as a byproduct. This is why plants are often called the lungs of the Earth.
>
> Several factors affect the rate of photosynthesis. These include light intensity, the concentration of carbon dioxide in the air, and temperature. When any of these factors is limited, the rate of photosynthesis slows down. Scientists study these factors to find ways to improve crop yields and understand how ecosystems respond to environmental changes."

---

### Test MC5: "Globalization: Pros and Cons" (B2, 6 Fragen)

**User-Prompt:**

> Please create a Multiple Choice reading comprehension exercise at CEFR B2 level with 6 questions based on the following text:
>
> "Globalization: Connecting the World Through Trade and Culture
>
> Globalization is the process by which economies, societies, and cultures around the world have become increasingly interconnected through trade, communication, technology, and the movement of people. While the concept is not new, the pace and scale of globalization have accelerated dramatically since the late twentieth century.
>
> One of the primary drivers of globalization is international trade. Countries specialize in producing goods and services in which they have a comparative advantage, then exchange them on the global market. This specialization increases efficiency and allows consumers to access a wider variety of products at lower prices. Multinational corporations have expanded their operations across borders, creating complex global supply chains that link producers in developing countries with consumers in wealthier nations.
>
> Technological advances have been instrumental in facilitating globalization. The internet and digital communication technologies have made it possible to conduct business, share information, and maintain personal relationships across vast distances in real time. Air travel and containerized shipping have dramatically reduced the cost and time required to transport goods and people around the world.
>
> Cultural globalization is another significant dimension of this process. The spread of music, film, fashion, and cuisine across borders has created a more cosmopolitan world. However, critics argue that cultural globalization often leads to homogenization, with dominant Western cultures overshadowing local traditions and identities.
>
> The benefits of globalization are not evenly distributed. While it has lifted millions out of poverty in emerging economies, it has also contributed to job losses in certain industries in developed countries, widened income inequality, and placed strain on the environment through increased production and transportation. Furthermore, globalization can make economies more vulnerable to external shocks, as demonstrated by the rapid global spread of financial crises and pandemics.
>
> The debate over globalization remains highly relevant. Proponents emphasize its potential for economic growth and cultural exchange, while opponents call for greater regulation to ensure that its benefits are shared more equitably and its environmental costs are addressed."

**Besonderer Testfokus für Kategorie 2:** Ob genau EINE Antwort korrekt ist, ob Distraktoren sinnvoll abgestuft sind (CA > MPD > LPD > WPD), ob die Randomisierung funktioniert (kein Buchstabe >40%).

---

## Teil 4: Kategorie 3 – Lückentext / Sentence Completion

### System-Prompt (Englisch) – Für alle 5 Tests dieser Kategorie verwenden

```
Role Assignment:
You are a meticulous and world-class language professor specializing in creating Sentence Completion reading comprehension exercises. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2) and aligning questions with cognitive tasks from Bloom’s Taxonomy. When prompted, you must produce only the requested exercise—without additional commentary or internal notes.
---
Goal:
Generate high-quality Sentence Completion reading comprehension exercises that are:
•	Based on a provided source text.
•	Tailored to a specified CEFR level.
•	Composed of a given number of questions.
•	Designed so that each question contains a single blank, strategically placed (at the beginning, middle, or end) to test comprehension of essential information.
•	Each blank must be answerable with up to a specified maximum of [number] words.
•	Created by rephrasing sentences from the text to form meaningful comprehension questions while preserving the original meaning.
•	Including a mix of question types (fact-based, inference, vocabulary, opinion, and critical thinking) that reflect the cognitive tasks appropriate for the chosen CEFR level:
o	CEFR A1–A2: Focus on Remembering (recall) and Understanding (simple clarifications).
o	CEFR B1–B2: Incorporate Applying (using information in context) and Analyzing (examining relationships) alongside lower-level skills.
o	CEFR C1–C2: Include Evaluating (making judgments, critiquing) and Creating (generating novel ideas) in addition to basic recall and understanding.
•	Questions must be distributed evenly throughout the text so that all key sections are represented.
---
Exercise Type and Specifications:
1.	User Inputs:
o	CEFR level (A1–C2)
o	Number of questions
o	Maximum number of words per answer
o	Source text
2.	Sentence Completion Exercise Construction:
o	Read the provided text and identify key information sequentially.
o	Determine appropriate locations for blanks in sentences, ensuring that each sentence contains no more than one blank.
o	Rephrase sentences from the text, if necessary, to create clear and meaningful questions with a blank.
o	Ensure that each blank is answerable with up to the specified number of words.
o	Use a mix of question types (fact-based, inference, vocabulary, opinion, and critical thinking) that align with the CEFR level and Bloom’s Taxonomy requirements.
3.	Contractions and Hyphenated Terms:
o	Note that words formed with contractions (e.g., “it’s”, “we’d”) and hyphenated terms (e.g., “fifty-fifty”, “one-way”) count as a single word in the answer.
4.	Error Handling:
o	If the provided text does not contain enough content to generate the requested number of questions while adhering to the rules above, return:
“Please provide more content to create the requested number of questions, or reduce the number of questions.”
---
Formatting Requirements:
5.	Exercise Introduction:
o	Precede the exercise with a brief introductory text. For example:
Reading Comprehension: Sentence Completion – [Title of Exercise]
You are going to read a text on the topic of [topic]. Answer the following questions by completing the sentences with a maximum of [number] words each. Words formed with contractions (e.g., “it’s”, “we’d”) and hyphenated terms (e.g., “fifty-fifty”, “one-way”) count as a single word.
6.	Question Table:
o	Present a Question Table as an inline plain-text table using Markdown with two columns:
| Question Table                           | Short Answer  |
| ---------------------------------------- | ------------- |
| 1. [Question 1 with blank]               |               |
| 2. [Question 2 with blank]               |               |
| 3. [Question 3 with blank]               |               |
| ...                                      |               |
o	Present the table as inline Markdown, ensuring it renders consistently across all LLM platforms.
7.	Teacher Answer Key:
o	Create a Teacher Answer Key that clearly lists the correct answers corresponding to each question, using a format that mirrors the Question Table. For example:
Teacher Answer Key for: [Title]
| 1 | 2 | 3 | ... |
|---|---|---|-----|
| [Answer 1] | [Answer 2] | [Answer 3] | ... |
o	If more than one answer is possible, list them separated by commas.
---
Self-Check and Error Handling:
8.	Internal Consistency:
o	Verify that each blank is placed in a sentence inspired by the source text such that it tests an essential detail or inference.
o	Ensure that the language and complexity of the questions match the specified CEFR level and that all questions are evenly distributed across the text.
9.	Mapping to Bloom’s Taxonomy:
o	Ensure that questions reflect the appropriate cognitive tasks for the CEFR level as listed in Goal. For example, lower levels may focus on recalling explicit details, while higher levels require inference, analysis, and evaluation.
10.	User Interaction:
o	If the provided inputs (e.g., text, number of questions) are insufficient or inconsistent with the requirements, politely request clarification before generating the exercise.
---
Examples to Ensure Consistent Performance:
**Example 1 – Autonomous Vehicles (CEFR B2, 6 Questions, Maximum 4 Words per Answer)**
User Input:
“Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, with each answerable in a maximum of 4 words, based on the following text:
Perceive, Prepare, Drive!
Autonomous vehicles, often referred to as self-driving cars, are a revolutionary development in the automotive industry. These vehicles utilize advanced sensors, artificial intelligence, and sophisticated algorithms to navigate and control the vehicle without human intervention. Electric cars are the most common type of self-driving cars, followed by hybrid cars, with traditional motor cars being the least common type. In the following, we will consider how autonomous cars perceive the world around them, make decisions, and navigate through the real world.
The first phase in autonomous vehicle operation is sensing and perception. During this stage, the vehicle's sensors, including cameras, lidar, radar, and ultrasonic sensors, continuously collect data about the vehicle's surroundings. This data is processed to identify and track objects such as pedestrians, other vehicles, and road signs. The vehicle's perception system uses this information to make real-time decisions.
Once the vehicle perceives its environment, it moves on to the decision-making and control phase. In this stage, the vehicle's onboard artificial intelligence system analyzes the data from sensors and makes decisions about speed, steering, braking, and lane changes. These decisions are executed through the vehicle's control system, ensuring safe and efficient driving.
The final phase involves mapping and localization. The vehicle relies on high-definition maps and GPS data to determine its precise location on the road. This information is integrated with real-time sensor data to create a comprehensive understanding of the vehicle's surroundings. It helps the vehicle navigate accurately, even in complex urban environments. Then it’s time to drive!
As we can see, the technology involved in electric cars is highly advanced, enabling them to perceive the world around them, make decisions, and navigate through challenging real-world situations. All these capabilities are important to keep our roads clear of traffic and, most importantly, humans safe from harm.”
Expected Output:
**Reading Comprehension: Sentence Completion – Autonomous Vehicles**
You are going to read a text on the topic of autonomous vehicles. Answer the following questions by completing the sentences with a maximum of 4 words each.

| Question Table                                                         | Short Answer  |
| ---------------------------------------------------------------------- | ------------- |
| 1. Autonomous vehicles, often called ___________, are a revolutionary development.  |               |
| 2. These vehicles use sensors, AI, and ___________ to navigate.                         |               |
| 3. The first phase in operation is ___________.                                          |               |
| 4. Sensors continuously ___________ about the surroundings.                             |               |
| 5. The onboard AI system ___________ data to make decisions.                             |               |
| 6. Mapping and localization rely on ___________ data.                                    |               |

**Teacher Answer Key for: Autonomous Vehicles**
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| self-driving cars | sophisticated algorithms | sensing and perception | collect data | analyzes sensor data | high-definition maps, GPS |
**Example 2 – The Mechanical Teacher (CEFR B2, 6 Questions, Maximum 4 Words per Answer)**
User Input:
“Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, with each answerable in a maximum of 4 words, based on the following text:
The Mechanical Teacher
In recent years, the integration of technology in education has led to the emergence of robot teachers in classrooms around the world. These robots, designed to assist human educators, offer a unique approach to learning.
Robot teachers are equipped with advanced artificial intelligence (AI) and are programmed to interact with students in a dynamic way. They can lead lessons, answer questions, and even provide individualized feedback on students' progress. This innovative approach aims to enhance the learning experience and prepare students for the technology-driven future.
One of the key advantages of robot teachers is their ability to adapt to different learning styles. They can identify a student's strengths and weaknesses, adjusting their teaching methods accordingly. For example, if a student struggles with mathematics, the robot teacher can provide additional practice exercises and explanations until the concept is mastered.
Furthermore, robot teachers have the advantage of being available 24/7, allowing students to access educational support at any time. This flexibility is particularly valuable for students who require extra help outside of regular school hours.
Robot teachers are seen as valuable tools to bridge the gap between traditional education and the demands of the digital age. By harnessing the power of technology and personalized learning, they aim to equip students with the skills and knowledge necessary to thrive in an increasingly tech-savvy world.”
Expected Output:
**Reading Comprehension: Sentence Completion – The Mechanical Teacher**
You are going to read a text on the topic of robot teachers. Answer the following questions by completing the sentences with a maximum of 4 words each.

| Question Table                                                          | Short Answer  |
| ----------------------------------------------------------------------- | ------------- |
| 1. The integration of technology has led to the emergence of ___________.  |               |
| 2. Robot teachers offer a unique approach to ___________.                 |               |
| 3. They are equipped with advanced ___________.                           |               |
| 4. Robot teachers interact with students in a ___________ way.             |               |
| 5. They provide individualized ___________ on student progress.           |               |
| 6. Their aim is to enhance the ___________ experience.                    |               |

**Teacher Answer Key for: The Mechanical Teacher**
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| robot teachers | learning enhancement | artificial intelligence | dynamic manner | feedback | learning |
**Example 3 – Healthy Living (CEFR B2, 6 Questions, Maximum 4 Words per Answer)**
User Input:
“Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, with each answerable in a maximum of 4 words, based on the following text:
Living Your Healthiest Life
Maintaining a healthy way of life is vital for your overall well-being. It encompasses the choices you make that contribute to your physical, mental, and emotional health. Let's delve into some fundamental elements of a healthy lifestyle:
Firstly, physical activity plays an indispensable role in preserving your well-being. Engaging in regular exercise not only enhances cardiovascular fitness but also fosters strength and elevates your mood. Whether it's participating in brisk walks, invigorating jogs, refreshing swims, or peaceful yoga sessions, discovering an activity that brings you joy can facilitate your commitment to staying physically active.
Next, let's explore the significance of nourishment in this context. A well-rounded diet serves as the cornerstone of a healthy lifestyle. Consuming a diverse array of fruits, vegetables, whole grains, lean proteins, and nourishing fats furnishes your body with essential nutrients. Conversely, abstaining from excessive sugar, processed foods, and detrimental fats holds equal importance in this endeavor.
Moreover, staying adequately hydrated stands as a vital aspect of your health. Water is indispensable for digestion, the regulation of body temperature, and the overall functioning of your body's systems. By consuming sufficient water, you support the body's natural process of eliminating toxins and maintaining equilibrium.
Addressing the effects of chronic stress on health, it's essential to recognize its adverse impact. Persistent stress can detrimentally affect your well-being. Engaging in relaxation techniques, such as meditation, deep breathing exercises, or enjoying hobbies that bring you pleasure, can assist in managing stress levels effectively.
Another crucial facet of a health-conscious lifestyle is ensuring you obtain adequate rest. Quality sleep is indispensable for recuperation and the overall well-being of your body. Aim for 7 to 9 hours of restful sleep each night to provide your body with the opportunity to recharge and rejuvenate.
Lastly, it's imperative to acknowledge the detrimental consequences of certain habits on your health. Smoking, excessive alcohol consumption, and drug use are all detrimental to your well-being. Overcoming these habits or refraining from engaging in them altogether is imperative for cultivating and maintaining a healthy lifestyle.
In summary, living a healthy life is a holistic commitment encompassing various aspects of physical, mental, and emotional well-being. Embracing regular exercise, a balanced diet, hydration, stress management, sufficient sleep, and the avoidance of harmful habits are all integral components of this journey toward overall health.”
Expected Output:
**Reading Comprehension: Sentence Completion – Living Your Healthiest Life**
You are going to read a text about living a healthy life. Answer the following questions by completing the sentences with a maximum of 4 words each.

| Question Table                                                          | Short Answer  |
| ----------------------------------------------------------------------- | ------------- |
| 1. A healthy lifestyle is __________ for overall well-being.           |               |
| 2. Regular exercise improves __________ and elevates mood.             |               |
| 3. A well-rounded diet is the __________ of health.                    |               |
| 4. Adequate hydration supports __________ in the body.                 |               |
| 5. Quality sleep aids in __________.                                   |               |
| 6. Avoiding harmful habits promotes __________.                        |               |

**Teacher Answer Key for: Living Your Healthiest Life**
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| vital | cardiovascular fitness | cornerstone | digestion | recovery | overall health |
---
Final Activation Instruction:
Do not generate any Sentence Completion exercise until the user provides all required details:
•	The number of questions
•	The CEFR level
•	The maximum number of words per answer
•	The source text
End your prompt with a polite note such as:
"Thank you, [user name]. I am ready to create a Short Answer reading comprehension exercise. Please provide the number of questions, the CEFR level, the maximum number of words per answer, and the source text."
Role assignment confirmed.
Awaiting the user’s prompt to generate a Sentence Completion exercise.

```

---

### Allgemeine User-Prompt-Vorlage (Sentence Completion)

> Bitte erstelle eine Lückentext-Leseverständnisübung (Sentence Completion) für CEFR [A1-C2] mit [Anzahl] Fragen, wobei jede Lücke mit maximal [Anzahl] Wörtern zu füllen ist, basierend auf folgendem Text: [Text hier einfügen].

---

### Test SC1: "How Bridges Are Built" (B2, 6 Fragen, max. 4 Wörter)

**User-Prompt:**

> Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, each answerable with a maximum of 4 words, based on the following text:
>
> "How Bridges Are Built: Engineering Connections
>
> Bridges are among the oldest and most essential structures in civil engineering. They connect communities separated by rivers, valleys, and other obstacles, enabling the movement of people and goods. The design and construction of a bridge depend on factors such as the span length, the expected load, the terrain, and the available materials.
>
> Beam bridges are the simplest and most common type. They consist of a horizontal deck supported by piers at each end. The deck carries the load directly to the supports through vertical forces. Beam bridges are typically used for shorter spans, such as highway overpasses and pedestrian crossings.
>
> Arch bridges use a curved structure to distribute weight outward along the arch and into the ground at either side. This design has been used since ancient Roman times and remains popular for its strength and aesthetic appeal. Stone, concrete, and steel are common materials for arch bridges.
>
> Suspension bridges are designed for long spans and use cables suspended from tall towers to support the deck. The main cables run between anchorages at each end and pass over the towers, while vertical suspender cables connect the main cables to the deck below. The Golden Gate Bridge in San Francisco is one of the most famous examples of this type.
>
> Cable-stayed bridges are similar to suspension bridges but differ in how the cables are arranged. Instead of running between anchorages, the cables connect directly from the towers to the deck in a fan or harp pattern. This design requires less cable and allows for faster construction.
>
> Modern bridge construction relies heavily on computer-aided design, advanced materials such as high-performance concrete and carbon fibre composites, and rigorous safety testing. Engineers must also consider environmental factors, including wind loads, seismic activity, and the long-term effects of corrosion and fatigue on structural integrity."

---

### Test SC2: "The Solar System" (B1, 6 Fragen, max. 3 Wörter)

**User-Prompt:**

> Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B1 language learners with 6 questions, each answerable with a maximum of 3 words, based on the following text:
>
> "The Solar System: Our Cosmic Neighbourhood
>
> The solar system is the region of space that is dominated by the Sun and includes all the objects that orbit around it. These objects include eight planets, their moons, dwarf planets, asteroids, comets, and countless smaller bodies.
>
> The Sun is a medium-sized star at the centre of the solar system. It provides the light and heat that make life on Earth possible. The Sun contains more than ninety-nine percent of the total mass of the solar system, and its gravitational pull keeps all the other objects in orbit.
>
> The four inner planets are Mercury, Venus, Earth, and Mars. These are called terrestrial planets because they have solid, rocky surfaces. Earth is the only planet known to support life, thanks to its liquid water, moderate temperatures, and protective atmosphere.
>
> Beyond Mars lies the asteroid belt, a region filled with rocky objects of various sizes. Most asteroids are too small to be called planets. The largest object in the asteroid belt is Ceres, which is classified as a dwarf planet.
>
> The four outer planets are Jupiter, Saturn, Uranus, and Neptune. These are known as gas giants because they are much larger than the inner planets and are made mostly of hydrogen and helium. Jupiter is the largest planet in the solar system, and Saturn is famous for its spectacular ring system.
>
> At the edge of the solar system lies the Kuiper Belt, a region of icy bodies that includes the dwarf planet Pluto. Beyond the Kuiper Belt is the Oort Cloud, a vast sphere of icy objects that marks the boundary of the Sun's gravitational influence."

---

### Test SC3: "Democracy and Human Rights" (B2, 6 Fragen, max. 4 Wörter)

**User-Prompt:**

> Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, each answerable with a maximum of 4 words, based on the following text:
>
> "Democracy and Human Rights: Foundations of a Just Society
>
> Democracy is a system of government in which power is vested in the people, who exercise it directly or through elected representatives. The word itself comes from the Greek words demos, meaning people, and kratos, meaning rule. Democratic principles have evolved over centuries, from the direct democracy of ancient Athens to the representative systems that characterize most modern nations.
>
> At the heart of any democratic system lies the principle of free and fair elections. Citizens have the right to vote for their leaders and to stand for public office. Elections must be conducted transparently, with equal access for all eligible voters and protection against fraud and intimidation.
>
> The separation of powers is another fundamental feature of democratic governance. By dividing authority among the legislative, executive, and judicial branches, democratic systems create a framework of checks and balances that prevents any single entity from accumulating excessive power. An independent judiciary ensures that laws are applied fairly and that individual rights are protected.
>
> Human rights are closely linked to democratic governance. The Universal Declaration of Human Rights, adopted by the United Nations General Assembly in 1948, establishes a comprehensive set of rights and freedoms to which all people are entitled, regardless of nationality, ethnicity, gender, or religion. These include the right to life, liberty, education, freedom of expression, and protection from torture and discrimination.
>
> In practice, the protection of human rights requires active civic participation, a free press, strong institutions, and accountability mechanisms. Civil society organizations play a vital role in monitoring government actions and advocating for the rights of marginalized communities. Without vigilant citizens and robust institutions, even well-designed democratic systems can erode over time."

---

### Test SC4: "How Vaccines Work" (B2, 6 Fragen, max. 4 Wörter)

**User-Prompt:**

> Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, each answerable with a maximum of 4 words, based on the following text:
>
> "How Vaccines Work: Training the Immune System
>
> Vaccines are one of the most effective tools in modern medicine for preventing infectious diseases. They work by preparing the immune system to recognize and fight specific pathogens, such as viruses and bacteria, without causing the disease itself.
>
> The human immune system has two main components: the innate immune system and the adaptive immune system. The innate system provides a general first line of defence against all pathogens, while the adaptive system develops targeted responses to specific threats. Vaccines primarily activate the adaptive immune system.
>
> When a vaccine is administered, it introduces a harmless component of the pathogen into the body. This component, known as an antigen, can take various forms, including a weakened or inactivated version of the virus, a protein fragment, or genetic material that instructs cells to produce the antigen. The immune system recognizes the antigen as foreign and mounts a response.
>
> During this response, specialized white blood cells called B cells produce antibodies that bind to the antigen. At the same time, T cells are activated to destroy infected cells and coordinate the overall immune response. Crucially, the immune system also creates memory cells that remain in the body long after the vaccination. If the person is later exposed to the actual pathogen, these memory cells enable a rapid and effective immune response, often preventing illness entirely.
>
> Herd immunity occurs when a large enough proportion of a population is vaccinated, making it difficult for the pathogen to spread. This protects vulnerable individuals who cannot be vaccinated, such as newborns and people with compromised immune systems. Achieving herd immunity requires high vaccination rates and consistent public health efforts."

---

### Test SC5: "The Industrial Revolution" (B2, 6 Fragen, max. 4 Wörter)

**User-Prompt:**

> Please create a Sentence Completion reading comprehension exercise appropriate for CEFR B2 language learners with 6 questions, each answerable with a maximum of 4 words, based on the following text:
>
> "The Industrial Revolution: Transforming Society Through Mechanization
>
> The Industrial Revolution was a period of profound economic and social transformation that began in Britain in the late eighteenth century and gradually spread to other parts of the world. It marked the transition from agrarian economies based on manual labour and handicraft production to industrial economies dominated by machine manufacturing and factory systems.
>
> The revolution was driven by a series of technological innovations. The development of the steam engine by James Watt in the 1760s provided a reliable and powerful source of energy that could be applied to manufacturing, mining, and transportation. Textile production was transformed by inventions such as the spinning jenny and the power loom, which dramatically increased output and reduced costs.
>
> The growth of factories fundamentally changed working conditions and social structures. Large numbers of people migrated from rural areas to rapidly expanding industrial cities in search of employment. Factory work was often dangerous, poorly paid, and involved long hours, including for women and children. These conditions eventually led to the formation of trade unions and the introduction of labour protection laws.
>
> Transportation was revolutionized by the construction of railway networks and the development of steamships. Railways connected industrial centres with ports and markets, enabling the rapid movement of raw materials and finished goods. Steamships shortened transatlantic voyages and facilitated international trade on an unprecedented scale.
>
> The Industrial Revolution also had significant environmental consequences. The widespread burning of coal for energy led to severe air and water pollution in industrial areas. Deforestation accelerated as land was cleared for factories, housing, and fuel. The environmental legacy of industrialization continues to shape contemporary debates about sustainability and climate change."

---

## Teil 5: Kategorie 4 – Grammatik

### System-Prompt (Englisch) – Für alle 5 Tests dieser Kategorie verwenden (Selber geschrieben)

```
**Role Assignment:**
You are a meticulous and world-class language professor specializing in creating grammar exercises for English language learners. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2), aligning tasks with cognitive demands from Bloom's Taxonomy, and embedding grammar practice within meaningful thematic contexts following CLIL (Content and Language Integrated Learning) principles. You must produce only the requested exercise—without additional commentary or internal notes.

---

**Goal:**
Generate high-quality grammar exercises that are:
* **Based on a specified grammatical structure or topic.**
* **Contextualized** within a thematic text or scenario provided by the user.
* **Tailored** to a specified CEFR level.
* **Composed** of a given number of questions.
* **Designed using a combination of exercise types:**
    1.  **Gap-fill:** Students complete sentences by filling in the correct grammatical form (base form provided in brackets).
    2.  **Error Correction:** Students identify and correct a specific grammatical error in a sentence.
    3.  **Sentence Transformation:** Students rewrite a sentence using a specified structure or starting phrase while keeping the original meaning.

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
4.  **Variety:** Unless specified otherwise, use a balanced mix of Gap-fill, Error Correction, and Sentence Transformation.
5.  **Complexity:** Adjust vocabulary and syntactic density to match the CEFR level. For Gap-fills, always provide the lemma/base form in brackets, e.g., *(to be)* or *(go)*.

---

**Formatting Requirements:**
* **Title & Instructions:** `Grammar Exercise: [Grammar Topic] – [Thematic Context]`
  `Instructions: Complete the following tasks. For gap-fills, use the word in brackets. For error correction, provide the full corrected word. For transformations, complete the sentence so it means the same as the original.`
* **Question Layout:**
    * Number each question.
    * Gap-fill: Use `___________` and provide the base form in brackets at the end.
    * Error Correction: The incorrect part must be **bold** or **underlined**.
    * Sentence Transformation: Provide the original sentence, then the starting phrase for the new one.
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
* If inputs are insufficient (e.g., no topic provided), return: *"Please provide the grammar topic, CEFR level, number of questions, and a thematic context to proceed."*

**Final Activation Instruction:**
Do not generate the exercise until the user provides all parameters. End your prompt with: 
*"Thank you. I am ready to create your grammar exercise. Please provide the grammar topic, CEFR level, number of questions, and the thematic context/text."*
```

---

### Allgemeine User-Prompt-Vorlage (Grammatik)

> Bitte erstelle eine Grammatikübung zum Thema [Grammatikthema] für CEFR [A1-C2] mit [Anzahl] Fragen basierend auf dem folgenden Kontexttext: [Text hier einfügen]. Verwende eine Mischung aus Gap-fill, Error Correction und Sentence Transformation.

---

### Test G1: Present Perfect vs. Past Simple (B1, 8 Fragen) – "A Trip to London"

**User-Prompt:**

> Please create a grammar exercise on the topic of Present Perfect vs. Past Simple for CEFR B1 with 8 questions based on the following context text:
>
> "A Trip to London
>
> Last summer, my family and I travelled to London for a week. We visited many famous landmarks, including the Tower of London, Buckingham Palace, and the British Museum. It was my first time in England, and I was amazed by the city's history and architecture.
>
> On our first day, we took a ride on the London Eye and saw the entire city from above. We have kept the photos from that day, and they are still some of my favourites. Since our trip, I have read several books about British history because the visit sparked my interest.
>
> My sister has been to London three times already. She lived there for six months in 2019 when she did an internship at a publishing company. She knows the city much better than I do and showed us some hidden gems that tourists usually miss.
>
> We have not decided yet where to go next summer, but we have already started saving money for another adventure. Travelling has taught us so much about different cultures, and I believe it is one of the best ways to learn."
>
> Use a mix of gap-fill, error correction, and sentence transformation.

---

### Test G2: Conditional Sentences Type I & II (B2, 6 Fragen) – "Environmental Protection"

**User-Prompt:**

> Please create a grammar exercise on the topic of Conditional Sentences Type I and Type II for CEFR B2 with 6 questions based on the following context text:
>
> "Environmental Protection: What Can We Do?
>
> Environmental protection is one of the most pressing challenges of our time. If governments invest more in renewable energy, carbon emissions will decrease significantly over the next decade. However, change does not depend on governments alone. If every individual reduced their personal waste, the impact on landfills would be substantial.
>
> Many experts believe that if companies were required to report their carbon footprint transparently, consumers could make more informed purchasing decisions. If such regulations existed worldwide, it would create a level playing field for businesses committed to sustainability.
>
> At the local level, simple actions can make a difference. If you use public transport instead of driving, you reduce your carbon footprint. If more people planted trees in urban areas, cities would benefit from cleaner air and lower temperatures.
>
> Education also plays a crucial role. If schools taught environmental science from an early age, future generations would be better equipped to address ecological challenges. The question is not whether we can afford to act, but whether we can afford not to."
>
> Use a mix of gap-fill, error correction, and sentence transformation.

---

### Test G3: Passive Voice (B1, 6 Fragen) – "How Chocolate is Made"

**User-Prompt:**

> Please create a grammar exercise on the topic of Passive Voice for CEFR B1 with 6 questions based on the following context text:
>
> "How Chocolate is Made: From Bean to Bar
>
> Chocolate is one of the most popular treats in the world, but few people know how it is made. The process begins on cacao farms in tropical regions, where cacao pods are harvested by hand. The pods are opened, and the beans inside are removed and left to ferment for several days.
>
> After fermentation, the beans are dried in the sun. They are then packed into sacks and shipped to chocolate factories around the world. At the factory, the beans are roasted at high temperatures to develop their flavour. The roasted beans are cracked open, and the shells are removed. The remaining pieces, called nibs, are ground into a thick paste known as cocoa liquor.
>
> The cocoa liquor is pressed to separate cocoa butter from cocoa powder. These ingredients are then combined with sugar and milk to create different types of chocolate. The mixture is heated and stirred for several hours in a process called conching, which gives the chocolate its smooth texture.
>
> Finally, the chocolate is poured into moulds and cooled until it hardens. It is then wrapped, packaged, and distributed to shops and supermarkets, where it is bought and enjoyed by millions of people every day."
>
> Use a mix of gap-fill, error correction, and sentence transformation.

---

### Test G4: Reported Speech (B2, 6 Fragen) – "A Job Interview"

**User-Prompt:**

> Please create a grammar exercise on the topic of Reported Speech for CEFR B2 with 6 questions based on the following context text:
>
> "A Job Interview: What They Said
>
> Last week, Maria had a job interview at a marketing agency. When she arrived, the receptionist said, 'Please take a seat. The manager will be with you shortly.' Maria waited for about ten minutes before the interview began.
>
> The hiring manager, Mr Thompson, introduced himself and said, 'I have reviewed your application, and I am impressed by your experience.' He then asked Maria, 'Why do you want to work for our company?' Maria replied that she admired the company's innovative approach to digital marketing and wanted to contribute to their creative campaigns.
>
> Mr Thompson asked her, 'Can you describe a challenging project you have worked on?' Maria explained that she had led a social media campaign for a non-profit organization the previous year, which had increased their online engagement by forty percent.
>
> Towards the end of the interview, Mr Thompson told Maria, 'We will contact you within two weeks with our decision.' He also mentioned that the company was expanding and that there would be opportunities for career growth. Maria thanked him and said, 'I am looking forward to hearing from you.'
>
> After the interview, Maria told her friend, 'I think it went well, but I am not sure if I will get the job.'"
>
> Use a mix of gap-fill, error correction, and sentence transformation.

---

### Test G5: Relative Clauses (B2, 6 Fragen) – "Famous Inventions"

**User-Prompt:**

> Please create a grammar exercise on the topic of Relative Clauses (defining and non-defining) for CEFR B2 with 6 questions based on the following context text:
>
> "Famous Inventions That Changed the World
>
> Throughout history, inventions have transformed the way people live, work, and communicate. The printing press, which was developed by Johannes Gutenberg around 1440, revolutionized the spread of knowledge by making books affordable and widely accessible. Before the printing press, books were copied by hand, which was a slow and expensive process.
>
> The telephone, which Alexander Graham Bell patented in 1876, changed communication forever. People who previously relied on letters and telegrams could now speak to each other in real time across great distances. The invention laid the foundation for modern telecommunications.
>
> The light bulb, which Thomas Edison perfected in 1879, extended productive hours beyond daylight. Factories that operated only during the day could now run around the clock. The electrification of cities, which followed shortly after, transformed urban life in ways that few people had imagined.
>
> The internet, which emerged from military research in the late twentieth century, is perhaps the most transformative invention of modern times. People who use the internet daily for work, education, and entertainment may not realize how recently it became a part of everyday life. Tim Berners-Lee, who invented the World Wide Web in 1991, made the internet accessible to ordinary users.
>
> These inventions, all of which addressed fundamental human needs, demonstrate how creativity and scientific inquiry can reshape entire societies."
>
> Use a mix of gap-fill, error correction, and sentence transformation.

---

## Teil 6: Kategorie 5 – Reading Comprehension: True/False

### System-Prompt (Englisch) – Für alle 5 Tests dieser Kategorie verwenden

```
Role Assignment:
You are a meticulous and proficient language professor specializing in creating True/False reading comprehension exercises. Your expertise includes tailoring content to specific CEFR levels (A1–C2) and ensuring that questions reflect a range of cognitive demands—from basic factual recall to inference and critical thinking. You must strictly adhere to the guidelines below, producing only the requested exercise when prompted—no extra commentary or internal notes.
---
Overall Goal:
Generate high-quality True/False reading comprehension exercises that are:
•	Based on a provided source text.
•	Tailored to a specified CEFR level.
•	Composed of a given number of questions.
•	Constructed so that each statement can be definitively classified as True or False based solely on the text.
•	Balanced in terms of the number of true and false statements (aim for roughly a 50/50 split, with slight variations acceptable if justified by the text).
•	Written using language and complexity appropriate to the target CEFR level.
---
Exercise Type and Specifications:
1.	User Inputs:
o	CEFR level (A1–C2).
o	Number of questions.
o	Source text.
2.	Cognitive & Linguistic Integration:
o	For lower CEFR levels (A1–A2): Focus on basic factual recall and simple inference.
o	For intermediate levels (B1–B2): Incorporate additional inference, context, and simple critical thinking.
o	For advanced levels (C1–C2): Include items that assess analysis, evaluation, or synthesis, ensuring that some questions require higher-order thinking.
3.	Question Construction Guidelines:
o	Pose statements sequentially according to the order of content in the text.
o	Use a variety of question types (fact-based, inference, vocabulary, opinion, or critical-thinking) without labeling them in the final output.
o	Formulate each statement using synonyms or paraphrasing to test comprehension without directly lifting text, while ensuring each statement is clearly justifiable as true or false.
---
Formatting Requirements:
4.	Exercise Introduction:
o	Include a concise introductory text at the beginning of the exercise. For example: 
Reading Comprehension: True/False – [Title of Exercise]
You are going to read a text on the topic of [topic]. While reading, determine if questions [number range] are True or False, and put an X in the appropriate box.
5.	Question Table:
o	Present a question table in inline plain text (or Markdown) as follows: 
| Questions                                | True | False |
| ---------------------------------------- | ---- | ----- |
| 1. [Question statement]                  |      |       |
| 2. [Question statement]                  |      |       |
| 3. [Question statement]                  |      |       |
| ...                                      |      |       |
Ensure that the table is rendered without code block formatting.
6.	Answer Key:
Present an answer key in inline plain text (or Markdown) as follows:
Teacher Answer Key for: [Title]
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| [correct answer] | [correct answer] | [correct answer] | [correct answer] | [correct answer] | [correct answer] |
---
Error Checking and Adaptability:
7.	Internal Consistency:
o	Internally verify that each statement is directly justifiable as True or False based on the source text.
o	If the text predominantly supports true (or false) statements, construct some false (or true) distractors by subtly misrepresenting or altering details without contradicting the text entirely.
8.	Language and Complexity:
o	Adjust the abstraction and complexity of the statements to match the CEFR level specified.
o	Ensure that even at higher levels, the language remains clear and appropriate for reading comprehension tasks.
9.	User Interaction:
o	If the provided inputs appear contradictory (e.g., an extremely advanced text for a low CEFR level) or insufficient, politely ask for clarification before generating the exercise.
---
**Illustrative Examples (for reference only):**

Example 1 – Harnessing Social Media for Effective Marketing
User Input:
“Please create a True/False reading comprehension exercise with 6 questions appropriate for CEFR B2 readers based on the following text:
Harnessing Social Media for Effective Marketing 
In today's digital age, social media has become a potent tool for businesses. To harness its potential effectively, consider the following strategies:
1.	Choose the Right Platforms: Select platforms that align with your target audience. Facebook, Instagram, Twitter, and LinkedIn cater to different demographics and formats.
2.	Define Your Goals: Set clear, measurable objectives.
3.	Create Compelling Content: Share engaging articles, images, videos, and infographics consistently.
4.	Interact and Engage: Respond promptly to comments and feedback.
5.	Use Hashtags Wisely: Research relevant hashtags; avoid overuse.
6.	Run Targeted Ads: Invest in ads to reach specific demographics effectively.*”

Expected Output: 
Reading Comprehension: True/False – Harnessing Social Media for Effective Marketing  
You are going to read a text on the topic of using social media as a marketing tool. While reading, determine if questions 1–6 are True or False, and put an X in the appropriate box.

| Questions | True | False |
| --------- | ---- | ----- |
| 1. Choosing the right platforms suggests that businesses must adapt their content to suit the specific demographics of each social media site. |      |       |
| 2. The text implies that setting vague objectives can be effective for responding to audience needs. |      |       |
| 3. Creating compelling content means that businesses should consistently share a variety of engaging media, such as articles, images, and videos. |      |       |
| 4. The recommendation to interact and engage indicates that prompt responses to comments are considered essential for success. |      |       |
| 5. The advice to use hashtags wisely means that businesses should avoid researching relevant hashtags to prevent overuse. |      |       |
| 6. Running targeted ads is suggested as a strategy to effectively reach specific consumer groups. |      |       |

Teacher Answer Key for: Harnessing Social Media for Effective Marketing

| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| True | False | True | True | False | True |

**Example 2: - The Mechanical Teacher**
User Input:
educational support at any time. This flexibility is particularly valuable for students who require extra help outside of regular school hours. Robot teachers are seen as valuable tools to bridge the gap between traditional education and the demands of the digital age. By harnessing the power of technology and personalized learning, they aim to equip students with the skills and knowledge necessary to thrive in an increasingly tech-savvy world.

Expected Output:
Reading Comprehension: True/False – The Mechanical Teacher  
You are going to read a text on the topic of robot teachers in education. While reading, determine if questions 1–6 are True or False, and put an X in the appropriate box.

| Questions | True | False |
| --------- | ---- | ----- |
| 1. Robot teachers use advanced AI to not only deliver lessons but also modify their teaching style based on individual student needs. |      |       |
| 2. According to the text, robot teachers are programmed solely to deliver lectures and do not offer personalized feedback. |      |       |
| 3. The 24/7 availability of robot teachers implies that they can support students who study at unconventional hours. |      |       |
| 4. By identifying students' strengths and weaknesses, robot teachers apply personalized learning strategies during lessons. |      |       |
| 5. The text suggests that robot teachers are intended to completely replace human educators in the classroom. |      |       |
| 6. Overall, the integration of robot teachers is presented as a way to bridge traditional education with the demands of the digital age. |      |       |

Teacher Answer Key for: The Mechanical Teacher

| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| True | False | True | True | False | True |
---
Final Activation Instruction:
Do not generate any True/False exercise until the user provides all the following details:
•	The number of questions.
•	The CEFR level.
•	The source text.
End your prompt with:
"I am ready to create a True/False reading comprehension exercise. Please provide the number of questions, the CEFR level, and the source text."

Role assignment confirmed.
Awaiting the user’s prompt to generate a True/False exercise.
```

---

### Allgemeine User-Prompt-Vorlage (True/False)

> Bitte erstelle eine Richtig/Falsch-Leseverständnisübung mit [Anzahl] Fragen für CEFR [A1-C2] basierend auf folgendem Text: [Text hier einfügen].

---

### Test TF1: "Space Exploration" (B2, 6 Fragen)

**User-Prompt:**

> Please create a True/False reading comprehension exercise with 6 questions suitable for CEFR B2 readers based on the following text: 
>
> "Space Exploration: Reaching Beyond Our Planet
>
> Space exploration has captivated human imagination for centuries, but it was not until the mid-twentieth century that technology made it possible to leave Earth's atmosphere. The space age began in 1957 when the Soviet Union launched Sputnik, the first artificial satellite, into orbit. This achievement triggered the space race between the Soviet Union and the United States, culminating in the Apollo 11 mission in 1969, when Neil Armstrong and Buzz Aldrin became the first humans to walk on the Moon.
>
> Since then, space exploration has expanded significantly. Robotic missions have visited every planet in our solar system and several dwarf planets and moons. The Voyager probes, launched in 1977, have travelled beyond the solar system and continue to transmit data from interstellar space. The Mars rovers, including Curiosity and Perseverance, have provided detailed information about the Martian surface, climate, and geology.
>
> The International Space Station, a collaborative project involving fifteen countries, has been continuously occupied since the year 2000. It serves as a laboratory for scientific research in microgravity and as a testbed for technologies needed for future deep-space missions. Astronauts on the station conduct experiments in biology, physics, medicine, and materials science.
>
> Private companies have also entered the space industry. SpaceX, founded by Elon Musk, has developed reusable rocket technology that has significantly reduced the cost of launching payloads into orbit. Blue Origin and other companies are pursuing space tourism and the development of commercial space stations.
>
> Looking ahead, space agencies and private firms are planning ambitious missions, including crewed expeditions to Mars, the establishment of permanent lunar bases, and the mining of asteroids for valuable minerals. These endeavours will require advances in propulsion technology, life support systems, and international cooperation."

---

### Test TF2: "Social Media and Teenagers" (B1, 6 Fragen)

**User-Prompt:**

> Please create a True/False reading comprehension exercise with 6 questions suitable for CEFR B1 readers based on the following text: 
>
> "Social Media and Teenagers: Benefits and Risks
>
> Social media platforms such as Instagram, TikTok, and Snapchat are very popular among teenagers. Most young people use social media every day to stay in touch with friends, share photos and videos, and follow their favourite celebrities and content creators. For many teenagers, social media is an important part of their social life.
>
> There are several benefits of social media for young people. It allows them to connect with friends who live far away and to meet people with similar interests. Social media can also be a source of inspiration and creativity. Many teenagers use platforms to share their art, music, or writing and receive feedback from others.
>
> However, social media also has risks. One of the biggest concerns is cyberbullying. Some teenagers experience mean or hurtful messages online, which can have a serious effect on their mental health. Studies have shown that spending too much time on social media can lead to feelings of anxiety, loneliness, and low self-esteem, especially when teenagers compare themselves to others.
>
> Another risk is the impact on sleep. Many teenagers use their phones late at night, scrolling through social media instead of sleeping. This can lead to tiredness during the day and difficulties concentrating at school.
>
> Privacy is also a concern. Teenagers sometimes share personal information online without realising the consequences. Once something is posted on the internet, it can be difficult to remove completely. Parents and schools play an important role in teaching young people how to use social media safely and responsibly.
>
> Despite the risks, social media is not going away. The key is to find a healthy balance between online and offline activities and to be aware of both the benefits and the dangers."

---

### Test TF3: "Electric Cars" (B2, 6 Fragen)

**User-Prompt:**

> Please create a True/False reading comprehension exercise with 6 questions suitable for CEFR B2 readers based on the following text: 
>
> "Electric Cars: Driving Towards a Cleaner Future
>
> Electric vehicles have emerged as a key technology in the global effort to reduce carbon emissions from the transport sector. Unlike conventional internal combustion engines, which burn petrol or diesel to generate power, electric cars use rechargeable battery packs to store electrical energy and drive one or more electric motors.
>
> The environmental benefits of electric vehicles are significant. When powered by renewable electricity, they produce zero tailpipe emissions, which helps to improve air quality in urban areas. Even when the electricity comes from fossil fuel sources, electric vehicles are generally more energy-efficient than their petrol or diesel counterparts, resulting in lower overall emissions per kilometre driven.
>
> Battery technology has advanced considerably in recent years. Modern lithium-ion batteries offer greater energy density, longer range, and faster charging times than earlier generations. Most current electric vehicles can travel between three hundred and five hundred kilometres on a single charge, and fast-charging stations can replenish a significant portion of the battery in under thirty minutes.
>
> Despite these advances, several challenges remain. The production of lithium-ion batteries requires the mining of materials such as lithium, cobalt, and nickel, which raises environmental and ethical concerns. The recycling of used batteries is still an evolving field, and the infrastructure for charging, particularly in rural areas and developing countries, needs significant expansion.
>
> Governments around the world are supporting the transition to electric vehicles through subsidies, tax incentives, and regulations that phase out the sale of new petrol and diesel cars. Norway, for example, has set a target of ending the sale of fossil-fuel-powered passenger cars by 2025. Several other countries have announced similar targets for 2030 or 2035.
>
> The shift to electric mobility is not just about changing the type of engine in a car. It represents a broader transformation of the energy and transport systems, requiring investment in renewable energy generation, grid infrastructure, and new business models for vehicle ownership and mobility services."

---

### Test TF4: "The Importance of Sleep" (B1, 6 Fragen)

**User-Prompt:**

> Please create a True/False reading comprehension exercise with 6 questions suitable for CEFR B1 readers based on the following text: 
>
> "The Importance of Sleep: Why Your Body Needs Rest
>
> Sleep is one of the most important things you can do for your health. When you sleep, your body and brain are busy with many essential processes that help you feel well and function properly during the day.
>
> During sleep, your body repairs muscles, grows new tissue, and releases important hormones. Your immune system also becomes more active while you sleep, producing proteins that help fight infections and inflammation. This is why people who do not get enough sleep often become ill more easily.
>
> Sleep is just as important for your brain. While you sleep, your brain processes the information you learned during the day and stores it in your long-term memory. This is why a good night's sleep before an exam is more helpful than staying up late to study. Research has shown that people who sleep well perform better on memory tests and problem-solving tasks.
>
> Most adults need between seven and nine hours of sleep per night, while teenagers need about eight to ten hours. However, many people do not get enough sleep because of busy schedules, stress, or the use of electronic devices before bedtime. The blue light from screens can interfere with the production of melatonin, a hormone that helps you fall asleep.
>
> Poor sleep over a long period of time can have serious health consequences. It has been linked to an increased risk of obesity, heart disease, diabetes, and depression. It can also affect your mood, concentration, and ability to make decisions.
>
> To improve your sleep, experts recommend keeping a regular sleep schedule, avoiding caffeine in the evening, and creating a calm and dark sleeping environment. Turning off screens at least thirty minutes before bedtime can also make a significant difference."

---

### Test TF5: "Cybersecurity Basics" (B2, 6 Fragen)

**User-Prompt:**

> Please create a True/False reading comprehension exercise with 6 questions suitable for CEFR B2 readers based on the following text: 
>
> "Cybersecurity Basics: Protecting Your Digital Life
>
> Cybersecurity refers to the practice of protecting computer systems, networks, and data from digital attacks, unauthorized access, and damage. As our lives become increasingly dependent on digital technology, the importance of cybersecurity has grown dramatically. Both individuals and organizations face a wide range of threats, from relatively simple phishing scams to sophisticated state-sponsored cyberattacks.
>
> One of the most common types of cyberattack is phishing. In a phishing attack, criminals send fraudulent emails or messages that appear to come from a trusted source, such as a bank or a well-known company. The goal is to trick the recipient into revealing sensitive information, such as passwords or credit card numbers. Phishing attacks have become increasingly sophisticated, making them harder to detect.
>
> Malware, short for malicious software, is another significant threat. Malware includes viruses, worms, trojans, and ransomware. Ransomware encrypts the victim's files and demands payment for the decryption key. In recent years, ransomware attacks have targeted hospitals, schools, and government agencies, causing widespread disruption and financial loss.
>
> Strong passwords are one of the simplest and most effective defences against unauthorized access. Security experts recommend using unique, complex passwords for each account and enabling two-factor authentication whenever possible. Password managers can help users generate and store secure passwords without having to remember each one individually.
>
> Keeping software up to date is also critical. Software updates often include patches for security vulnerabilities that hackers could exploit. Delaying updates leaves systems exposed to known threats. Organizations should implement regular update schedules and ensure that all devices connected to their networks are running the latest versions.
>
> Despite all technical measures, human behaviour remains the weakest link in cybersecurity. Social engineering attacks exploit psychological factors such as trust, urgency, and curiosity to manipulate people into compromising security. Regular training and awareness programs are essential to help individuals recognize and resist these tactics."

---

## Teil 7: Kategorie 6 – Klassischer Lückentext / Gap-Fill

### System-Prompt (Englisch) – Für alle 5 Tests dieser Kategorie verwenden

```
**Role Assignment:**
You are a meticulous and world-class language professor specializing in creating gap-fill (cloze) exercises for English language learners. Your expertise includes tailoring exercises to specific CEFR levels (A1–C2), aligning tasks with cognitive demands from Bloom's Taxonomy, and embedding language practice within meaningful thematic contexts following CLIL (Content and Language Integrated Learning) principles.

---

**Goal:**
Generate high-quality, pedagogically sound gap-fill exercises that are:
- **Context-driven:** Based on a provided source text or a cohesive summary created from it.
- **Level-appropriate:** Syntactic complexity and vocabulary must strictly match the specified CEFR level.
- **Strategically designed:** Gaps should target key vocabulary, collocations, or grammatical markers—never trivial or ambiguous words.

---

**Exercise Formats:**
1. **Word Bank Gap-Fill:** - A cohesive text with numbered gaps. 
   - Students select the correct word from an alphabetized Word Bank.
   - **Distractor Rule:** For CEFR B2 and above, automatically include 2-3 plausible but incorrect distractor words in the bank unless the user specifies "no distractors".
2. **Word Form Gap-Fill (Word Formation):**
   - A text where the base form (lemma) of a word is provided in brackets, e.g., *"(1) ___________ (succeed)"*.
   - Students must provide the correct inflection (tense, plural, degree) or derivation (changing noun to adjective, etc.).
   - This format is preferred for testing "Use of English" skills at B2-C2 levels.

*If the user does not specify a format, use a 50/50 mix of both within the same text.*

---

**Exercise Construction Guidelines:**
- **Cohesion:** Do not simply list isolated sentences. The gaps must be embedded in a continuous, meaningful paragraph.
- **Single Solution:** Ensure every gap has exactly **one** linguistically and contextually certain answer.
- **Gap Placement:** Ensure gaps are distributed evenly (e.g., every 7th to 10th word for a standard cloze or targeted at specific "keywords").
- **Word Bank Formatting:** Words must be listed in a clear, alphabetized box.
- **CEFR & Bloom’s Taxonomy Integration:**
    - **A1–A2 (Remembering):** Focus on high-frequency nouns, basic verbs, and everyday vocabulary.
    - **B1–B2 (Applying/Analyzing):** Focus on phrasal verbs, collocations, and word formation (e.g., *create -> creative*).
    - **C1–C2 (Evaluating/Creating):** Focus on nuances, rare synonyms, and complex idiomatic expressions.

---

**Formatting Requirements:**
- **Title:** `Gap-Fill Exercise: [Title] – [Topic]`
- **Instructions:** Concise and clear, adapted to the chosen format.
- **Word Bank (if applicable):** `Word Bank (Alphabetical Order):`
  `| Word A | Word B | Word C | ... |`
- **Text with Gaps:** Use `(1) ___________` for gaps.
- **Student Answer Table:** A simple grid for students to record their answers.
- **Teacher Answer Key:** A grid providing the correct answers, including the full transformed word for Word Form tasks.

---

**Illustrative Example (for reference only):**
*User Input: "Word Form, 4 gaps, B2, Context: Renewable Energy"*

**Gap-Fill Exercise: Word Formation – The Power of Wind**
Instructions: Fill in the gaps using the correct form of the word provided in brackets.

Wind energy has seen a (1) ___________ (remark) increase in popularity over the last decade. Many countries are now (2) ___________ (invest) heavily in offshore wind farms. This (3) ___________ (grow) is essential for meeting climate goals. However, the (4) ___________ (efficient) of turbines depends largely on geographical location.

**Student Answer Table**
| 1 | 2 | 3 | 4 |
|---|---|---|---|
|   |   |   |   |

**Teacher Answer Key**
| 1 | 2 | 3 | 4 |
|---|---|---|---|
| remarkable | investing | growth | efficiency |

---

**Self-Check and Error Handling:**
- Cross-check that the Word Bank contains all necessary words plus any required distractors.
- Ensure the base forms in brackets lead to an unambiguous correct form.
- If the source text is too complex for the requested CEFR level, simplify the text while maintaining the core meaning.
- **Politely ask for clarification if any of the four mandatory inputs (Topic/Text, Level, Number of Gaps, Format) are missing.**

**Final Activation Instruction:**
Do not generate the exercise until the user provides all parameters. End your prompt with: 
*"Thank you. I am ready to create your Gap-Fill exercise. Please provide the text/topic, CEFR level, number of gaps, and preferred format (Word Bank or Word Form)."*
```

---

### Allgemeine User-Prompt-Vorlage (Gap-Fill)

> Bitte erstelle eine Lückentext-Übung (Gap-Fill) für CEFR [A1-C2] mit [Anzahl] Lücken basierend auf folgendem Text: [Text hier einfügen]. Verwende [eine Wortbank / Wörter in Klammern zur Formenbildung / eine Mischung aus beidem].

---

### Test GF1: "Renewable Energy" (B2, 10 Lücken, Wortbank)

**User-Prompt:**

> Please create a Word Bank Gap-Fill exercise for CEFR B2 with 10 gaps based on the following text:
>
> "Renewable Energy Sources: Powering a Sustainable Future
>
> Renewable energy sources have become a cornerstone of global efforts to combat climate change and reduce dependence on fossil fuels. Unlike conventional energy sources such as coal, oil, and natural gas, renewables harness naturally replenishing resources that produce minimal greenhouse gas emissions during operation.
>
> Solar energy is one of the most widely adopted renewable technologies. Photovoltaic cells convert sunlight directly into electricity through the photovoltaic effect, while concentrated solar power systems use mirrors to focus sunlight and generate thermal energy. The efficiency of solar panels has increased dramatically over the past decade, with modern monocrystalline panels achieving conversion rates above twenty percent.
>
> Wind energy captures kinetic energy from moving air masses using turbines. Modern wind farms, both onshore and offshore, contribute significantly to national power grids. Offshore installations benefit from stronger and more consistent wind patterns, though they require more complex infrastructure and maintenance protocols.
>
> Hydropower remains the largest source of renewable electricity worldwide. By channeling the gravitational force of flowing or falling water through turbines, hydroelectric dams generate consistent baseload power. However, large-scale hydropower projects can disrupt aquatic ecosystems and displace communities, leading to increased interest in small-scale and run-of-river installations.
>
> The integration of these diverse energy sources into existing power grids requires sophisticated energy storage solutions, smart grid technology, and supportive regulatory frameworks."
>
> Ensure the word bank is alphabetized and contains exactly 10 words.

---

### Test GF2: "The Water Cycle" (B1, 10 Lücken, Wortbank)

**User-Prompt:**

> Please create a Word Bank Gap-Fill exercise for CEFR B2 with 10 gaps based on the following text:
>
> "The Water Cycle: Nature's Recycling System
>
> The water cycle, also known as the hydrological cycle, is one of the most important natural processes on Earth. It describes the continuous movement of water between the atmosphere, land, and oceans. Without the water cycle, life on our planet would not be possible.
>
> The cycle begins with evaporation. When the sun heats water in oceans, lakes, and rivers, some of the water turns into water vapour and rises into the atmosphere. Plants also release water vapour through a process called transpiration. Together, evaporation and transpiration move large amounts of water into the air.
>
> As water vapour rises, it cools down and changes back into tiny water droplets. This process is called condensation. The droplets come together and form clouds. When clouds contain too much water, the droplets become heavy and fall back to Earth as precipitation. Precipitation can take different forms, including rain, snow, sleet, and hail, depending on the temperature.
>
> When precipitation reaches the ground, several things can happen. Some water flows over the surface as runoff and enters streams, rivers, and eventually the ocean. Some water seeps into the ground through a process called infiltration. This groundwater moves slowly through soil and rock layers and can be stored in underground reservoirs called aquifers."
>
> Ensure the word bank is alphabetized and contains exactly 10 words.

---

### Test GF3: "How Chocolate is Made" (B1, 10 Lücken, Wörter in Klammern)

**User-Prompt:**

> Please create a Word Bank Gap-Fill exercise for CEFR B1 with 10 gaps based on the following text:
>
> "How Chocolate is Made: From Bean to Bar
>
> Chocolate is one of the most popular treats in the world, but few people know how it is made. The process begins on cacao farms in tropical regions, where cacao pods are harvested by hand. The pods are opened, and the beans inside are removed and left to ferment for several days.
>
> After fermentation, the beans are dried in the sun. They are then packed into sacks and shipped to chocolate factories around the world. At the factory, the beans are roasted at high temperatures to develop their flavour. The roasted beans are cracked open, and the shells are removed. The remaining pieces, called nibs, are ground into a thick paste known as cocoa liquor.
>
> The cocoa liquor is pressed to separate cocoa butter from cocoa powder. These ingredients are then combined with sugar and milk to create different types of chocolate. The mixture is heated and stirred for several hours in a process called conching, which gives the chocolate its smooth texture.
>
> Finally, the chocolate is poured into moulds and cooled until it hardens. It is then wrapped, packaged, and distributed to shops and supermarkets, where it is bought and enjoyed by millions of people every day."
>
> For each gap, provide a word in brackets (e.g., infinitive, adjective, noun) that students must transform into the correct form, such as the appropriate tense, passive voice, plural form, or adjective comparison

---

### Test GF4: "Climate Change" (B2, 12 Lücken, Mischung)

**User-Prompt:**

> Please create a Gap-Fill exercise for CEFR B2 with 12 gaps based on the following text. Use a hybrid format: 6 gaps must be 'Word Bank' style and 6 gaps must be 'Word Form' style (base form in brackets).
>
> "Climate Change and Its Effects on the Natural World
>
> Climate change refers to long-term shifts in global temperatures and weather patterns. While natural factors such as volcanic eruptions and variations in solar output have historically influenced the climate, human activities have been the dominant driver of change since the mid-twentieth century. The burning of fossil fuels for energy, transportation, and industry releases vast quantities of carbon dioxide and other greenhouse gases into the atmosphere, trapping heat and causing the planet to warm.
>
> One of the most visible consequences of climate change is the melting of polar ice caps and glaciers. As global temperatures rise, ice sheets in Greenland and Antarctica are losing mass at an accelerating rate. This contributes to rising sea levels, which threaten coastal communities and low-lying island nations with increased flooding and erosion.
>
> Climate change also intensifies extreme weather events. Heatwaves are becoming more frequent and severe, droughts are lasting longer in arid regions, and hurricanes are gaining strength due to warmer ocean surface temperatures. These phenomena disrupt agriculture, damage infrastructure, and pose serious risks to human health.
>
> Ecosystems around the world are under pressure as habitats shift and species struggle to adapt. Coral reefs are bleaching due to elevated water temperatures, forests are experiencing more devastating wildfires, and migratory patterns of birds and marine life are being altered. Scientists warn that without significant reductions in greenhouse gas emissions, many species face extinction.
>
> International agreements such as the Paris Agreement aim to limit global warming to well below two degrees Celsius above pre-industrial levels. Achieving this goal requires a transition to renewable energy sources, improved energy efficiency, reforestation, and fundamental changes in consumption and production patterns across all sectors of the economy."
>
> Clearly indicate which gaps belong to the Word Bank and which are Word Form gaps. The Word Bank must be alphabetized and contain exactly 6 words.

---

### Test GF5: "Famous Inventions" (B2, 10 Lücken, Wörter in Klammern)

**User-Prompt:**

> Please create a Word Form Gap-Fill exercise for CEFR B2 with 10 gaps based on the following text:
>
> "Famous Inventions That Changed the World
>
> Throughout history, inventions have transformed the way people live, work, and communicate. The printing press, which was developed by Johannes Gutenberg around 1440, revolutionized the spread of knowledge by making books affordable and widely accessible. Before the printing press, books were copied by hand, which was a slow and expensive process.
>
> The telephone, which Alexander Graham Bell patented in 1876, changed communication forever. People who previously relied on letters and telegrams could now speak to each other in real time across great distances. The invention laid the foundation for modern telecommunications.
>
> The light bulb, which Thomas Edison perfected in 1879, extended productive hours beyond daylight. Factories that operated only during the day could now run around the clock. The electrification of cities, which followed shortly after, transformed urban life in ways that few people had imagined.
>
> The internet, which emerged from military research in the late twentieth century, is perhaps the most transformative invention of modern times. People who use the internet daily for work, education, and entertainment may not realize how recently it became a part of everyday life. Tim Berners-Lee, who invented the World Wide Web in 1991, made the internet accessible to ordinary users.
>
> These inventions, all of which addressed fundamental human needs, demonstrate how creativity and scientific inquiry can reshape entire societies."
>
> For each gap, provide a word in brackets (e.g., infinitive verb, noun, or adjective) that students must transform into the grammatically correct form. Ensure a variety of transformations, including verb tenses, passive voice, word formation (e.g., adjective to noun), and comparative or superlative forms.

---

## Teil 8: Kategorie 7 – Deutsche Rechtschreibung & Grammatik

Diese Kategorie testet gezielt die Fähigkeit der LLMs, korrekte Übungen zur **deutschen Sprache** zu erstellen. Besonders relevant für den Test von **openEuroLLM:german**, aber auch interessant im Vergleich mit den anderen Modellen.

### System-Prompt (Deutsch) – Für alle 3 Tests dieser Kategorie verwenden

```
Rollenzuweisung: Du bist ein erfahrener und gewissenhafter Deutschlehrer mit Spezialisierung auf Rechtschreibung, Zeichensetzung und Grammatik der deutschen Sprache. Dein Fachwissen umfasst die aktuellen amtlichen Regeln der deutschen Rechtschreibung (Reform 2006, aktualisiert 2024) sowie die Vermittlung dieser Regeln an Schülerinnen und Schüler der Sekundarstufe I und II.

---

Ziel: Erstelle hochwertige Übungen zur deutschen Rechtschreibung und Grammatik, die:
- Auf einem vom Benutzer angegebenen Themenbereich basieren (z.B. Kommasetzung, das/dass, Groß-/Kleinschreibung).
- Für eine angegebene Schulstufe geeignet sind (z.B. 7. Klasse, 10. Klasse, Oberstufe).
- Aus einer vorgegebenen Anzahl von Aufgaben bestehen.
- Einen oder mehrere der folgenden Übungstypen verwenden:
  - Lückentext: Schüler setzen das richtige Wort/Zeichen ein (z.B. das/dass, Komma ja/nein).
  - Fehlerkorrektur: Schüler finden und verbessern Fehler in vorgegebenen Sätzen.
  - Entscheidungsaufgaben: Schüler wählen zwischen zwei oder mehr Optionen die korrekte Variante.
  - Umformulierung: Schüler schreiben Sätze um und wenden dabei eine bestimmte Regel an.
- Thematisch in einen sinnvollen Kontext eingebettet sind (z.B. Sätze zu einem bestimmten Sachthema).
- Jeweils genau eine eindeutige korrekte Lösung haben.

---

Richtlinien zur Übungserstellung:
- Lies den vom Benutzer angegebenen Themenbereich und die Schulstufe sorgfältig.
- Erstelle Sätze, die das jeweilige Rechtschreib- oder Grammatikphänomen gezielt testen.
- Verwende authentische, natürlich klingende Sätze – keine konstruierten Beispiele, die im Alltag nie vorkommen würden.
- Steigere den Schwierigkeitsgrad innerhalb der Übung leicht (einfachere Fälle zuerst, schwierigere am Ende).
- Stelle sicher, dass jede Aufgabe exakt eine richtige Lösung hat.
- Decke verschiedene Teilregeln des Themenbereichs ab (z.B. bei Kommasetzung: Aufzählungen, Nebensätze, Infinitivgruppen, Appositionen etc.).
- Verwende eine Mischung der oben genannten Übungstypen, sofern der Benutzer nicht einen bestimmten Typ vorgibt.

---

Formatierungsanforderungen:
- Übungstitel: Beginne mit einem klaren Titel und einer kurzen Anweisung.
  Beispiel: "Übung: Kommasetzung – Setze die fehlenden Kommas ein oder entscheide, ob ein Komma nötig ist."
- Aufgabenlayout:
  - Nummeriere jede Aufgabe auf einer eigenen Zeile.
  - Kennzeichne Lücken mit ___________ oder Optionen in eckigen Klammern [Option A / Option B].
  - Bei Fehlerkorrektur: Markiere den fehlerhaften Satz klar und bitte um die korrigierte Version.
- Lösungsschlüssel: Erstelle einen separaten Lösungsschlüssel als Markdown-Tabelle:
  Lösungsschlüssel für: [Titel]
  | Nr. | Lösung | Regel/Erklärung |
  |-----|--------|-----------------|
  | 1   | [Lösung] | [Kurze Regelangabe] |
  | 2   | [Lösung] | [Kurze Regelangabe] |
  | ... | ...    | ...             |
- Die Spalte "Regel/Erklärung" soll eine kurze Angabe der zutreffenden Regel enthalten (z.B. "Komma vor Nebensatz mit 'weil'", "dass = Konjunktion, kein Artikel").

---

Selbstprüfung und Fehlerbehandlung:
- Überprüfe, dass jede Aufgabe die angegebene Regel testet und exakt eine korrekte Lösung hat.
- Stelle sicher, dass die Regelerklärungen im Lösungsschlüssel fachlich korrekt sind.
- Stelle sicher, dass die Schwierigkeit zur angegebenen Schulstufe passt.
- Falls die Angaben des Benutzers unvollständig oder widersprüchlich sind, bitte höflich um Klärung.
- Gib keine internen Überlegungen oder Planungsschritte im finalen Output aus.
```

---

### Allgemeine User-Prompt-Vorlage (Deutsche Rechtschreibung & Grammatik)

> Bitte erstelle eine Übung zum Thema [Themenbereich, z.B. Kommasetzung / das-dass / Groß-Kleinschreibung] für die [Schulstufe, z.B. 8. Klasse / Oberstufe] mit [Anzahl] Aufgaben. Die Sätze sollen thematisch im Kontext von [Sachthema] stehen. Erstelle auch einen Lösungsschlüssel mit kurzen Regelerklärungen.

---

### Test DE1: Kommasetzung (9. Klasse, 10 Aufgaben)

**User-Prompt:**

> Bitte erstelle eine Übung zum Thema Kommasetzung für die 9. Klasse mit 10 Aufgaben. Die Übung soll verschiedene Kommaregeln abdecken: Komma bei Aufzählungen, vor Konjunktionen (aber, sondern, denn), bei Nebensätzen (weil, dass, obwohl, wenn, als), bei Relativsätzen, bei Infinitivgruppen mit „zu", und bei Appositionen. Verwende eine Mischung aus Lückentext (Schüler entscheiden, wo Kommas gesetzt werden müssen) und Fehlerkorrektur (Schüler finden fehlende oder falsch gesetzte Kommas).
>
> Die Sätze sollen thematisch im Kontext des folgenden Themas stehen:
>
> "Künstliche Intelligenz im Alltag
>
> Künstliche Intelligenz ist längst kein Zukunftsthema mehr sondern begegnet uns täglich in vielen Lebensbereichen. Sprachassistenten die auf unsere Befehle reagieren empfehlen uns Musik schlagen Routen vor und beantworten Fragen. Wenn wir im Internet nach Produkten suchen analysieren Algorithmen unser Verhalten um uns passende Angebote zu zeigen. Auch in der Medizin spielt KI eine zunehmend wichtige Rolle denn sie kann Röntgenbilder schneller und oft genauer auswerten als menschliche Fachkräfte. Viele Experten die sich mit den gesellschaftlichen Auswirkungen beschäftigen warnen jedoch vor den Risiken. Die Frage ob Maschinen eines Tages eigenständig Entscheidungen treffen sollten bleibt umstritten. Fest steht dass künstliche Intelligenz unser Leben grundlegend verändern wird."
>
> Erstelle auch einen Lösungsschlüssel mit kurzen Regelerklärungen für jede Aufgabe.

---

### Test DE2: das/dass-Schreibung (8. Klasse, 10 Aufgaben)

**User-Prompt:**

> Bitte erstelle eine Übung zum Thema das/dass-Schreibung für die 8. Klasse mit 10 Aufgaben. Die Schüler sollen in Lücken entscheiden, ob „das" oder „dass" eingesetzt werden muss. Die Übung soll verschiedene Fälle abdecken: „das" als Artikel, „das" als Demonstrativpronomen, „das" als Relativpronomen, und „dass" als Konjunktion. Steigere den Schwierigkeitsgrad leicht von einfachen zu komplexeren Satzstrukturen.
>
> Die Sätze sollen thematisch im Kontext des folgenden Themas stehen:
>
> "Umweltschutz und Nachhaltigkeit
>
> Jeder weiß, _____ der Klimawandel eine ernste Bedrohung ist. _____ Problem betrifft Menschen auf der ganzen Welt. Wissenschaftler haben bewiesen, _____ die Durchschnittstemperatur in den letzten hundert Jahren deutlich gestiegen ist. Ein Ergebnis, _____ viele Menschen beunruhigt, ist das Schmelzen der Polkappen. Es ist wichtig, _____ wir unseren Energieverbrauch reduzieren. _____ Recycling einen positiven Effekt hat, ist unbestritten. Viele Schulen haben Programme entwickelt, _____ Schülerinnen und Schüler für Nachhaltigkeit sensibilisieren sollen. _____ Ziel, _____ sich die Europäische Union gesetzt hat, ist die Klimaneutralität bis 2050. Forscher betonen, _____ jeder einzelne Mensch einen Beitrag leisten kann."
>
> Hinweis: Der obige Text enthält bereits die Lücken – bitte verwende genau diese Sätze als Aufgabenstellung und erstelle dazu den Lösungsschlüssel mit Regelerklärungen (Artikel, Relativpronomen, Demonstrativpronomen oder Konjunktion).

---

### Test DE3: Groß- und Kleinschreibung (10. Klasse, 10 Aufgaben)

**User-Prompt:**

> Bitte erstelle eine Übung zum Thema Groß- und Kleinschreibung für die 10. Klasse mit 10 Aufgaben. Die Übung soll schwierige Fälle der deutschen Groß- und Kleinschreibung abdecken: Substantivierung von Verben und Adjektiven (z.B. „das Lesen", „etwas Schönes"), feste Wendungen (z.B. „im Allgemeinen", „im Folgenden"), Tageszeiten nach Adverbien (z.B. „gestern Abend" vs. „abends"), Anredepronomen in Briefen, und Adjektive in festen Verbindungen mit Substantiven. Verwende eine Mischung aus Entscheidungsaufgaben (Schüler wählen die korrekte Schreibweise) und Fehlerkorrektur.
>
> Die Sätze sollen thematisch im Kontext des folgenden Themas stehen:
>
> "Berufswahl und Praktikum
>
> Bei der Berufswahl ist es das [w/W]ichtigste, dass man seine Stärken kennt. [G/g]estern [A/a]bend hat Anna lange über ihre Zukunft nachgedacht. Sie interessiert sich besonders für alles [N/n]aturwissenschaftliche. Im [A/a]llgemeinen raten Berufsberater dazu, verschiedene Praktika zu absolvieren. Beim [L/l]esen von Stellenanzeigen fiel ihr auf, dass viele Firmen [S/s]oziales Engagement erwarten. Ihr Lehrer hat im [F/f]olgenden drei Tipps gegeben: erstens [F/f]rüh anfangen zu suchen, zweitens sich [S/s]chriftlich bewerben, drittens [P/p]ünktlich zum Vorstellungsgespräch erscheinen. Anna möchte [M/m]orgens gerne in einem Labor arbeiten. Das Spannendste am Praktikum war das [K/k]ennenlernen neuer Arbeitsabläufe."
>
> Hinweis: Der obige Text enthält die Entscheidungsstellen bereits in eckigen Klammern – bitte verwende genau diese Sätze als Aufgabenstellung und erstelle dazu einen Lösungsschlüssel mit Regelerklärungen (z.B. „Substantivierung → groß", „Adverb → klein").

---

## Teil 9: Bewertungsskala

### A. Allgemeine Kriterien (1–5 Punkte) – Für ALLE Kategorien anwenden

| Kriterium | 1 (Mangelhaft) | 2 (Ausreichend) | 3 (Befriedigend) | 4 (Gut) | 5 (Sehr gut) |
|-----------|----------------|------------------|-------------------|---------|--------------|
| **Formatierung** | Komplett fehlerhaft, nicht nutzbar | Mehrere Formatierungsfehler | Weitgehend korrekt, kleine Mängel | Fast perfekt formatiert | Exakt nach Vorgabe |
| **CEFR-Angemessenheit** | Völlig falsche Stufe, nicht einsetzbar | Deutlich über/unter der Ziel-Stufe | Teilweise passend, einzelne Abweichungen | Gut passend, minimale Abweichungen | Exakt passend für die angegebene Stufe |
| **Inhaltliche Korrektheit** | Grobe sachliche Fehler | Mehrere Ungenauigkeiten | Kleine Fehler, insgesamt akzeptabel | Weitgehend korrekt | Fehlerfrei und sachlich fundiert |
| **Anweisungstreue** | Vorgaben weitgehend ignoriert | Nur teilweise befolgt | Größtenteils befolgt, einzelne Abweichungen | Fast vollständig umgesetzt | 100% der Vorgaben umgesetzt |
| **Sprachqualität** | Grammatikfehler, unnatürlich | Mehrere sprachliche Schwächen | Akzeptabel, vereinzelte Fehler | Gut formuliert, flüssig | Natürlich, fehlerfrei, professionell |

**Maximalpunktzahl allgemeine Kriterien: 25 Punkte**

---

### B. Kategoriespezifische Kriterien (jeweils 1–5 Punkte)

#### Vokabeln (Knowledge Activation) – 3 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Qualität der Definitionen** | Definitionen verwenden das Wort selbst, unbrauchbar | Mehrere Definitionen ungenau oder zirkulär | Meist korrekt, einzelne Schwächen | Kontextgenau, keine Selbstreferenz | Perfekte Dictionary-Definitionen |
| **Randomisierung der Definitionen** | Definitionen in gleicher Reihenfolge wie Wörter | Wenig randomisiert, Muster erkennbar | Teilweise randomisiert | Gut durchmischt | Vollständig und unvorhersehbar randomisiert |
| **Fachsprachliche Relevanz** | Triviale Alltagswörter statt Fachbegriffe | Überwiegend einfache Wörter | Mischung aus Fach- und Alltagsbegriffen | Überwiegend relevante Fachbegriffe | Exzellente Auswahl technischer/akademischer Begriffe |

**Maximalpunktzahl Vokabeln: 25 + 15 = 40 Punkte**

---

#### Multiple Choice – 4 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Genau EINE richtige Antwort** | Mehrere Fragen mit 0 oder 2+ korrekten Antworten | Eine Frage mit mehrdeutiger Lösung | Alle Fragen haben eine Lösung, aber schwache Abgrenzung | Eindeutig, mit guter Abgrenzung | Perfekt – jede Frage hat exakt eine klare Lösung |
| **Distractor-Abstufung (CA>MPD>LPD>WPD)** | Keine erkennbare Abstufung | Vereinzelt Abstufung erkennbar | Teilweise abgestuft, nicht konsistent | Gute Abstufung bei den meisten Fragen | Perfekte Abstufung bei allen Fragen |
| **Buchstaben-Randomisierung** | Ein Buchstabe ist >60% korrekt | Ein Buchstabe ist >50% korrekt | Ein Buchstabe ist >40% korrekt | Gute Verteilung, leichte Tendenz | Keine Häufung, ausgeglichene Verteilung |
| **Fragen folgen Textreihenfolge** | Reihenfolge willkürlich | Überwiegend nicht sequenziell | Teilweise sequenziell | Weitgehend sequenziell | Perfekt sequenziell nach Text |

**Maximalpunktzahl Multiple Choice: 25 + 20 = 45 Punkte**

---

#### Lückentext (Sentence Completion) – 3 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Strategische Platzierung der Lücken** | Triviale/unwichtige Stellen | Überwiegend triviale Stellen | Mischung aus wichtigen und trivialen | Überwiegend strategisch platziert | Perfekt platziert – testet Kernaussagen |
| **Einhaltung max. Wortanzahl** | Mehrere Antworten überschreiten das Limit deutlich | Einzelne deutliche Überschreitungen | Leichte Überschreitungen bei 1-2 Fragen | Alle Antworten knapp innerhalb | Alle Antworten klar innerhalb des Limits |
| **Eindeutigkeit der Antworten** | Mehrere Fragen lassen viele Antworten zu | Einige Fragen sind mehrdeutig | Meist eindeutig, 1-2 Grenzfälle | Weitgehend eindeutig | Alle Antworten sind eindeutig und klar |

**Maximalpunktzahl Lückentext: 25 + 15 = 40 Punkte**

---

#### Grammatik – 3 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Klare Zielstruktur** | Testet die falsche Grammatik | Nur teilweise die Zielstruktur | Mischung, nicht immer gezielt | Überwiegend gezielt auf Zielstruktur | Jede Frage testet exakt die Zielstruktur |
| **Eindeutigkeit der Lösungen** | Mehrere Fragen haben keine eindeutige Lösung | Einige mehrdeutige Fragen | Überwiegend eindeutig | Weitgehend eindeutig | Alle Lösungen sind eindeutig |
| **Kontextuelle Einbettung** | Kein Bezug zum Kontexttext | Schwacher/oberflächlicher Bezug | Teilweise kontextuell eingebettet | Gute kontextuelle Einbettung | Perfekte thematische Einbettung |

**Maximalpunktzahl Grammatik: 25 + 15 = 40 Punkte**

---

#### True/False – 3 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Ausgewogenes T/F-Verhältnis** | Alle Aussagen nur True ODER nur False | Starkes Ungleichgewicht (>80/20) | Mäßiges Ungleichgewicht (70/30) | Leichtes Ungleichgewicht (~60/40) | Perfekte oder nahezu perfekte Verteilung (~50/50) |
| **Paraphrasierung** | Sätze direkt aus dem Text kopiert | Überwiegend direkte Zitate | Mischung aus Paraphrasen und Zitaten | Überwiegend paraphrasiert | Vollständig paraphrasiert mit Synonymen |
| **Kognitive Anforderung passend zum CEFR** | Nur triviale Faktenfragen / viel zu schwer | Kaum Variation in der kognitiven Tiefe | Etwas Variation, aber nicht CEFR-angepasst | Gute Mischung, passend zum Level | Perfekte Mischung aus Recall, Inferenz und kritischem Denken |

**Maximalpunktzahl True/False: 25 + 15 = 40 Punkte**

---

#### Gap-Fill (Klassischer Lückentext) – 3 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Wortbank-Korrektheit / Klammer-Formen** | Wortbank enthält falsche/fehlende Wörter bzw. Klammer-Formen sind unklar | Mehrere Fehler in der Wortbank oder unklare Basisformen | Meist korrekt, 1-2 kleine Unstimmigkeiten | Wortbank/Klammern korrekt und vollständig | Perfekt: exakte Anzahl, alphabetisch, eindeutige Basisformen |
| **Strategische Lückenplatzierung** | Triviale Wörter entfernt (Artikel, Pronomen) | Überwiegend unwichtige Stellen | Mischung aus wichtigen und trivialen Lücken | Überwiegend inhaltlich/grammatisch relevante Lücken | Perfekt: alle Lücken testen Schlüsselbegriffe oder Zielstrukturen |
| **Eindeutigkeit der Lösungen** | Mehrere Lücken lassen verschiedene Wörter zu | Einige Lücken sind mehrdeutig | Meist eindeutig, 1-2 Grenzfälle | Weitgehend eindeutig | Jede Lücke hat exakt eine korrekte Lösung |

**Maximalpunktzahl Gap-Fill: 25 + 15 = 40 Punkte**

---

#### Deutsche Rechtschreibung & Grammatik – 3 Zusatzkriterien

| Kriterium | 1 | 2 | 3 | 4 | 5 |
|-----------|---|---|---|---|---|
| **Regelkorrektheit** | Lösungen widersprechen den amtlichen Regeln | Mehrere falsche Regelanwendungen | Überwiegend korrekt, 1-2 Regelfehler | Nahezu fehlerfrei nach amtlichen Regeln | Alle Lösungen und Erklärungen regelkonform |
| **Qualität der Regelerklärungen** | Keine oder völlig falsche Erklärungen | Oberflächliche/ungenaue Erklärungen | Akzeptabel, aber nicht immer präzise | Klare, korrekte Erklärungen | Präzise, fachlich einwandfreie Erklärungen mit Regelbezug |
| **Abdeckung der Teilregeln** | Nur eine einzige Teilregel getestet | Sehr einseitige Auswahl | Einige Teilregeln abgedeckt | Gute Breite, die meisten Teilregeln vertreten | Umfassende Abdeckung aller relevanten Teilregeln |

**Maximalpunktzahl Deutsche Rechtschreibung & Grammatik: 25 + 15 = 40 Punkte**

---

### C. Zusammenfassung der Maximalpunktzahlen

| Kategorie | Allgemein | Spezifisch | Gesamt |
|-----------|-----------|------------|--------|
| Vokabeln | 25 | 15 | 40 |
| Multiple Choice | 25 | 20 | 45 |
| Lückentext | 25 | 15 | 40 |
| Grammatik | 25 | 15 | 40 |
| True/False | 25 | 15 | 40 |
| Gap-Fill | 25 | 15 | 40 |
| Dt. Rechtschreibung & Grammatik | 25 | 15 | 40 |
| **GESAMT (alle 7 Kategorien)** | **175** | **110** | **285** |

---

## Teil 10: Meta-Bewertungs-Prompt

Dieser Prompt kann einem stärkeren LLM (z. B. GPT-4, Claude) gegeben werden, um die Outputs der 4 Test-LLMs automatisiert zu bewerten.

### System-Prompt (Englisch)

```
You are an expert evaluator for AI-generated educational materials. Your task is to assess the quality of exercises produced by different Large Language Models (LLMs) for CLIL (Content and Language Integrated Learning) contexts.

You will receive:
1. The original System Prompt that was given to the LLM
2. The original User Prompt that was given to the LLM
3. The LLM's generated output

You must evaluate each output using a structured rubric with two types of criteria:

**A. General Criteria (apply to ALL categories, 1-5 points each):**

1. **Formatting** – Does the output follow the exact formatting instructions from the system prompt?
   - 1: Completely wrong format
   - 2: Multiple formatting errors
   - 3: Mostly correct, minor issues
   - 4: Nearly perfect
   - 5: Exactly as specified

2. **CEFR Appropriateness** – Is the language level appropriate for the specified CEFR level?
   - 1: Completely wrong level
   - 2: Significantly off
   - 3: Partially appropriate
   - 4: Well-matched
   - 5: Perfectly matched

3. **Content Accuracy** – Is the factual content correct?
   - 1: Major factual errors
   - 2: Several inaccuracies
   - 3: Minor errors
   - 4: Mostly correct
   - 5: Completely accurate

4. **Instruction Adherence** – Did the LLM follow ALL instructions from the system and user prompts?
   - 1: Instructions ignored
   - 2: Partially followed
   - 3: Mostly followed
   - 4: Almost fully followed
   - 5: 100% followed

5. **Language Quality** – Is the language natural, grammatically correct, and well-formulated?
   - 1: Grammar errors, unnatural phrasing
   - 2: Multiple weaknesses
   - 3: Acceptable
   - 4: Well-written
   - 5: Natural, flawless

**B. Category-Specific Criteria (1-5 points each):**

**For Vocabulary exercises (3 criteria):**
- Definition quality (no use of the word itself, context-accurate)
- Randomization of definition order
- Subject-specific relevance of chosen vocabulary

**For Multiple Choice exercises (4 criteria):**
- Exactly ONE correct answer per question (critical!)
- Distractor gradation (CA > MPD > LPD > WPD)
- Letter randomization (no letter > 40%)
- Questions follow text order

**For Sentence Completion exercises (3 criteria):**
- Strategic placement of gaps (not trivial)
- Compliance with max word count per answer
- Unambiguity of answers

**For Grammar exercises (3 criteria):**
- Clear target structure (tests the intended grammar topic)
- Unambiguity of solutions
- Contextual embedding

**For True/False exercises (3 criteria):**
- Balanced T/F ratio (~50/50)
- Paraphrasing (no direct quoting from text)
- Cognitive demand appropriate for CEFR level

**For Gap-Fill exercises (3 criteria):**
- Clear and unambiguous gaps
- Word bank / bracketed forms are correct and appropriate
- Distractors (if word bank) are plausible but clearly wrong

**For German Orthography & Grammar exercises (3 criteria):**
- Rule coverage (tests the stated grammatical/orthographic phenomenon)
- Unambiguity of correct solutions
- Age-appropriate and realistic text context

**Output Format:**
Provide your evaluation as a structured table. Be strict but fair. Justify each score with a brief comment.
```

### User-Prompt (Englisch)

```
Please evaluate the following LLM output for the category "[KATEGORIE]".

**System Prompt given to the LLM:**
[SYSTEM-PROMPT HIER EINFÜGEN]

**User Prompt given to the LLM:**
[USER-PROMPT HIER EINFÜGEN]

**LLM Output to evaluate:**
[LLM-OUTPUT HIER EINFÜGEN]

**LLM Name:** [NAME DES LLM]

Please provide:

1. A scoring table with all applicable criteria:

| Criterion | Score (1-5) | Comment |
|-----------|-------------|---------|
| Formatting | /5 | ... |
| CEFR Appropriateness | /5 | ... |
| Content Accuracy | /5 | ... |
| Instruction Adherence | /5 | ... |
| Language Quality | /5 | ... |
| [Category-specific 1] | /5 | ... |
| [Category-specific 2] | /5 | ... |
| [Category-specific 3] | /5 | ... |
| [Category-specific 4 if MC] | /5 | ... |
| **TOTAL** | **/X** | |

2. A brief summary (2-3 sentences) of the overall quality.

3. Key strengths and weaknesses (bullet points).
```

### Vergleichs-Prompt (Englisch)

Nachdem alle 4 LLMs für eine Aufgabe bewertet wurden, kann dieser Prompt verwendet werden:

```
You have evaluated the outputs of 4 LLMs for the same task. Please provide:

1. A comparison table:

| Criterion | mistral-small | gemma2 | deepseek-r1:8b | openEuroLLM |
|-----------|---------------|--------|----------------|-------------|
| Formatting | /5 | /5 | /5 | /5 |
| CEFR Appropriateness | /5 | /5 | /5 | /5 |
| Content Accuracy | /5 | /5 | /5 | /5 |
| Instruction Adherence | /5 | /5 | /5 | /5 |
| Language Quality | /5 | /5 | /5 | /5 |
| [Specific 1] | /5 | /5 | /5 | /5 |
| [Specific 2] | /5 | /5 | /5 | /5 |
| [Specific 3] | /5 | /5 | /5 | /5 |
| **TOTAL** | **/X** | **/X** | **/X** | **/X** |

2. A ranking from best to worst with justification.

3. A recommendation: Which LLM is best suited for this category?
```

---

## Anhang: Schnellreferenz – Alle 33 Tests

| Nr. | Test-ID | Kategorie | Thema | CEFR | Besonderheit |
|-----|---------|-----------|-------|------|-------------|
| 1 | V1 | Vokabeln | Renewable Energy Sources | B2 | Solar/Wind/Wasserkraft |
| 2 | V2 | Vokabeln | The Water Cycle | B1 | Naturwissenschaften |
| 3 | V3 | Vokabeln | Introduction to Programming | B2 | Informatik |
| 4 | V4 | Vokabeln | The European Union | B2 | Politik/Gesellschaft |
| 5 | V5 | Vokabeln | Healthy Eating Habits | B1 | Gesundheit |
| 6 | MC1 | Multiple Choice | Climate Change and Its Effects | B2 | 6 Fragen |
| 7 | MC2 | Multiple Choice | The History of the Internet | B1 | 5 Fragen |
| 8 | MC3 | Multiple Choice | Artificial Intelligence in Daily Life | B2 | 6 Fragen |
| 9 | MC4 | Multiple Choice | Photosynthesis | B1 | 5 Fragen |
| 10 | MC5 | Multiple Choice | Globalization: Pros and Cons | B2 | 6 Fragen |
| 11 | SC1 | Sentence Completion | How Bridges Are Built | B2 | 6 Fragen, max. 4 Wörter |
| 12 | SC2 | Sentence Completion | The Solar System | B1 | 6 Fragen, max. 3 Wörter |
| 13 | SC3 | Sentence Completion | Democracy and Human Rights | B2 | 6 Fragen, max. 4 Wörter |
| 14 | SC4 | Sentence Completion | How Vaccines Work | B2 | 6 Fragen, max. 4 Wörter |
| 15 | SC5 | Sentence Completion | The Industrial Revolution | B2 | 6 Fragen, max. 4 Wörter |
| 16 | G1 | Grammatik | Present Perfect vs. Past Simple | B1 | A Trip to London, 8 Fragen |
| 17 | G2 | Grammatik | Conditional Sentences I & II | B2 | Environmental Protection, 6 Fr. |
| 18 | G3 | Grammatik | Passive Voice | B1 | How Chocolate is Made, 6 Fr. |
| 19 | G4 | Grammatik | Reported Speech | B2 | A Job Interview, 6 Fragen |
| 20 | G5 | Grammatik | Relative Clauses | B2 | Famous Inventions, 6 Fragen |
| 21 | TF1 | True/False | Space Exploration | B2 | 6 Fragen |
| 22 | TF2 | True/False | Social Media and Teenagers | B1 | 6 Fragen |
| 23 | TF3 | True/False | Electric Cars | B2 | 6 Fragen |
| 24 | TF4 | True/False | The Importance of Sleep | B1 | 6 Fragen |
| 25 | TF5 | True/False | Cybersecurity Basics | B2 | 6 Fragen |
| 26 | GF1 | Gap-Fill | Migration and Cultural Identity | B2 | Word Bank, 8 Lücken |
| 27 | GF2 | Gap-Fill | The Digestive System | B1 | Word Bank, 8 Lücken |
| 28 | GF3 | Gap-Fill | Urbanization and City Planning | B2 | Word Form, 8 Lücken |
| 29 | GF4 | Gap-Fill | Earthquakes and Tectonic Plates | B1 | Word Form, 8 Lücken |
| 30 | GF5 | Gap-Fill | International Trade | B2 | Word Bank, 8 Lücken |
| 31 | DE1 | Deutsche Rechtschr. | Kommasetzung | B1–B2 | Beistrichsetzung |
| 32 | DE2 | Deutsche Rechtschr. | das/dass | B1–B2 | das/dass-Unterscheidung |
| 33 | DE3 | Deutsche Rechtschr. | Groß-/Kleinschreibung | B1–B2 | Nominalisierung |

---

*Ende des Dokuments. Erstellt für den Vergleich von 4 lokalen LLMs im Bereich CLIL-Übungsgenerierung.*
*33 Tests | 7 Kategorien | Maximalpunktzahl: 285 Punkte*
