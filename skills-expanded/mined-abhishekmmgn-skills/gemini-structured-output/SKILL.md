---
name: gemini-structured-output
description: strategies for forcing Gemini to output valid structured data (JSON/XML). Use this for data extraction, API integrations, and creating machine-readable responses.
---

# Gemini Structured Output Strategies

## Goal
Generate reliable, machine-readable output (JSON/XML) for application integration, minimizing parsing errors and hallucinations.

## Core Techniques

### 1. Enforcing JSON Output
* **Concept:** Explicitly instruct the model to return a specific data format rather than free text.
* **Benefits:**
    * **Consistency:** Returns data in the same style every time.
    * **Focus:** Forces the model to stick to the requested data, reducing "chatter".
    * **Reduced Hallucinations:** The strict structure limits the model's ability to invent unverifiable text.
* **Example Prompt:**
    > "Classify the following review. Return valid JSON only: { 'sentiment': 'POSITIVE' | 'NEGATIVE', 'score': number }".

### 2. Working with Schemas (Input & Output)
* **Input Blueprints:** You can provide a **JSON Schema** as *input* to give the model a "blueprint" of the expected data.
* **Mechanism:** This defines expected fields (e.g., `release_date`), data types (e.g., `string`, `float`), and descriptions, helping the model understand relationships between data points.
* **Example Schema Definition:**
    ```json
    {
      "type": "object",
      "properties": {
        "name": { "type": "string", "description": "Product name" },
        "price": { "type": "number", "format": "float" }
      }
    }
    ```

### 3. Handling Truncation (JSON Repair)
* **The Problem:** JSON is verbose. If the output hits the token limit, the JSON object may be cut off (missing closing braces), making it invalid.
* **The Solution:**
    * **Increase Token Limit:** Ensure the `max_tokens` setting is high enough for the data structure.
    * **Use Tools:** Implement a library like `json-repair` in your application pipeline to automatically close broken tags and fix malformed objects.

## Decision Matrix: Text vs. Structured
| Task Type | Recommended Format |
| :--- | :--- |
| **Creative Writing** | Plain Text / Markdown |
| **Data Extraction** | JSON |
| **Categorization/Ranking** | JSON |
| **Code Generation** | Markdown Code Blocks |
