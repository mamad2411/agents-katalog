---
name: gemini-advanced-reasoning
description: advanced logic and problem-solving strategies for Gemini. Use this for complex math, multi-step reasoning, or deep analysis tasks where standard prompting fails.
---

# Gemini Advanced Reasoning Strategies

## Goal
Apply sophisticated reasoning frameworks to break down complex problems, reduce hallucinations, and improve accuracy in logic-heavy tasks.

## Reasoning Frameworks

### 1. Step-Back Prompting
* **Concept:** Improves performance by asking the model to first recall relevant general knowledge or principles before solving the specific problem.
* **Workflow:**
    1.  **Abstraction:** Prompt the model to ask a generic question related to the specific task.
    2.  **Reasoning:** Feed the answer to that general question into the final prompt.
* **Example:**
    * *Instead of:* "Write a story about a specific game level."
    * *Step 1 (Step-Back):* "What are 5 key settings that contribute to a challenging FPS level?".
    * *Step 2 (Final):* "Context: [Insert Answer from Step 1]. Now write the story...".

### 2. Chain of Thought (CoT)
* **Concept:** Forces the model to generate intermediate reasoning steps rather than jumping to a final answer.
* **Zero-Shot Trigger:** Append the phrase **"Let's think step by step"** to the end of the prompt.
* **Few-Shot CoT:** Provide examples that include the reasoning steps (Question -> Reasoning -> Answer).
* **Configuration:** Always set **Temperature to 0** when using CoT to ensure deterministic, focused reasoning paths.
* **Structure:** Ensure the final answer is separated from the reasoning steps to allow for easy extraction.



### 3. Self-Consistency
* **Concept:** Overcomes the limitations of a single "greedy" decoding path by generating multiple diverse reasoning paths and selecting the most consistent answer.
* **Workflow:**
    1.  **Generate:** Run the same CoT prompt multiple times with a **higher temperature** (e.g., 0.7 or 1.0) to encourage diverse thinking.
    2.  **Vote:** Extract the final answer from all generated responses.
    3.  **Select:** Choose the answer that appears most frequently (majority voting).

### 4. Tree of Thoughts (ToT)
* **Concept:** Generalizes CoT by allowing the model to explore multiple reasoning branches simultaneously, rather than a single linear line.
* **Usage:** Best suited for tasks requiring exploration or strategic planning.
* **Mechanism:** The model maintains a "tree" where each node is a coherent thought/step. It can branch out to explore different possibilities before converging on a solution.



## Decision Matrix: Which Technique to Use?
| Complexity | Technique | Configuration |
| :--- | :--- | :--- |
| **Medium (Math/Logic)** | Zero-Shot CoT | Temp = 0 |
| **High (Strategic/Creative)** | Step-Back Prompting | Standard Temp |
| **High (Ambiguous)** | Self-Consistency | High Temp + Multiple Calls |
| **Very High (Exploratory)** | Tree of Thoughts | Standard Temp |
