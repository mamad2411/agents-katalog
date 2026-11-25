---
name: gemini-memory-lifecycle
description: strategies for the agent memory lifecycle (Extraction, Consolidation, Retrieval). Use this to implement long-term learning and personalization beyond a single session.
---

# Gemini Memory Lifecycle Strategies

## Goal
Transform transient conversation data into persistent, high-value "Memories" that allow the agent to learn about the user over time, creating a personalized experience.

## The Core Lifecycle (ETL for Agents)

### 1. Extraction (Signal vs. Noise)
* **Concept:** Use an LLM to scan the raw session logs and extract only "meaningful" information, discarding pleasantries and filler.
* **Method:** Define "Topic Definitions" (e.g., User Preferences, Goals, Facts). If the data doesn't fit a topic, do not create a memory.
* **Technique:**
    * **Schema-Based:** Extract specific fields (e.g., `{"food_preference": "vegan"}`).
    * **Natural Language:** Extract atomic statements (e.g., "The user prefers window seats").

### 2. Consolidation (The Gardener)
* **Concept:** "Self-editing" the knowledge base. New information must be merged with old information to prevent contradictions and duplicates.
* **Operations:**
    * **Create:** If the insight is novel.
    * **Update:** If the insight refines existing knowledge (e.g., "User likes spicy food" -> "User likes *mildly* spicy food").
    * **Delete/Invalidate:** If the new info contradicts old info, remove the stale memory.

### 3. Retrieval (Finding Context)
* **Concept:** Fetching the right memory at the right time.
* **Scoring Dimensions:** Do not rely on Semantic Similarity alone. Use a **Blended Score**:
    1.  **Relevance:** Vector similarity to the current query.
    2.  **Recency:** Favor newer memories over older ones.
    3.  **Importance:** Weight memories based on their significance (defined at generation time).

## Memory Types

### Declarative Memory ("Knowing What")
* **Definition:** Facts, figures, and user details (e.g., "My anniversary is October 26th").
* **Storage:** Best stored in **Vector Databases** (for semantic search) or **Knowledge Graphs** (for relationship mapping).

### Procedural Memory ("Knowing How")
* **Definition:** Strategies and workflows. The agent remembers *how* it successfully solved a problem in the past.
* **Application:** Used to inject a "playbook" of successful steps into the prompt for complex tasks.

## Best Practices
* **Asynchronous Generation:** Memory generation is expensive. Always run the Extraction and Consolidation steps in the **background** after the agent has responded to the user. Never block the user interface.
* **Provenance:** Track the "Source Reliability" of every memory. A memory derived from explicit user input ("I am vegan") is higher trust than one inferred from conversation ("User asked about salads").
