---
name: gemini-prompt-construction
description: effective prompt structure strategies for Gemini, including Zero-shot, Few-shot, Role, and System prompting. Use this to refine queries for better accuracy and style.
---

# Gemini Prompt Construction Strategies

## Goal
Design high-quality prompts that guide Gemini to produce accurate, relevant, and stylistically appropriate outputs by applying proven prompting techniques.

## Core Techniques

### 1. Zero-Shot Prompting
* **Usage:** Use for simple tasks where no prior examples are needed.
* **Format:** Provide a clear description of the task and the input text.
* **Constraint:** Best for straightforward requests like "Summarize this text" or "Translate this sentence."

### 2. Few-Shot Prompting
* **Usage:** Use when you need to steer the model toward a specific output structure, pattern, or style.
* **Rule of Thumb:** Provide **3 to 5 examples** of the input-output pattern.
* **Classification Tasks:** When using few-shot for classification, ensure you **mix up the classes** in your examples to prevent the model from overfitting to a specific order.
* **Format:**
    ```text
    Input: [Example 1]
    Output: [Desired Result 1]
    Input: [Example 2]
    Output: [Desired Result 2]
    ...
    Input: [Actual Task]
    Output:
    ```

### 3. Role Prompting
* **Usage:** Assign a specific persona (e.g., "book editor," "travel guide") to control the tone, style, and perspective of the response.
* **Implementation:** Start the prompt with "Act as a [Role]..." or "You are a [Role]...".
* **Benefit:** Improves relevance and consistency with the desired domain expertise.

### 4. System vs. Contextual Prompting
* **System Prompting:** Define the "big picture" goal or overarching rule (e.g., "Always return JSON," "Be respectful").
* **Contextual Prompting:** Provide immediate, task-specific background info (e.g., "Context: You are writing for a blog about retro 80's arcade games").

## Configuration Guidelines
* **Creativity (Temperature):**
    * **Factual/Math:** Set Temperature to `0`.
    * **Balanced:** Set Temperature to `0.2`, Top-P to `0.95`, Top-K to `30`.
    * **Creative:** Set Temperature to `0.9`, Top-P to `0.99`, Top-K to `40`.

## Best Practices
* **Simplicity:** Use positive instructions (what *to* do) rather than negative constraints (what *not* to do).
* **Specificity:** Be specific about the output format. For data extraction, explicitly request **JSON** output to limit hallucinations.
