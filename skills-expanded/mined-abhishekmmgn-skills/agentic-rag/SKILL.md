---
name: agentic-rag
description: strategies for building Agentic RAG systems. Use this to move beyond static retrieval by using autonomous agents for adaptive source selection, query expansion, and multi-step reasoning.
---

# Agentic RAG Strategies

## Goal
Transform traditional, static Retrieval-Augmented Generation (RAG) into a dynamic, agentic process that actively reasons about *how* and *where* to find information.

## Core Capabilities

### 1. Adaptive Retrieval
* **Concept:** Instead of a single pass against a vector database, the agent dynamically selects the best knowledge source based on the context.
* **Mechanism:** The agent evaluates the query ambiguity and chooses between multiple data stores (e.g., "PDFs" vs. "Web Search" vs. "Structured DB").

### 2. Multi-Step Reasoning
* **Concept:** For complex queries, the agent breaks the problem down into logical steps and retrieves information sequentially.
* **Workflow:**
    1.  **Decompose:** Break "Compare the revenue of Company A and Company B" into two sub-queries.
    2.  **Retrieve:** Fetch revenue for Company A.
    3.  **Retrieve:** Fetch revenue for Company B.
    4.  **Synthesize:** Combine both facts into a final answer.

### 3. Context-Aware Query Expansion
* **Concept:** The agent doesn't just search for the user's raw query. It generates multiple refined search terms to increase recall.
* **Benefit:** Captures synonyms, related concepts, and specific terminology that the user might have missed.

## Optimization Techniques
* **Self-Correction:** Implement an **Evaluator Agent** that reviews retrieved chunks for relevance before generating an answer. If the data is poor, it triggers a new search with better terms.
* **Better Search:** Enhance the underlying engine with **semantic chunking** (keeping topics together) and **re-ranking** (using a second model to order results by quality).
