---
name: tooling-strategies
description: decision matrix for agent tools. Use this to choose between Extensions, Functions, and Data Stores based on security, execution location, and data type.
---

# Gemini Tooling Strategies

## Goal
Select the correct tool type to bridge the gap between the model's internal knowledge and the external world.

## Tool Types & Decision Matrix

### 1. Extensions (Agent-Side Execution)
* **Definition:** A standardized bridge to an API where the **Agent** manages the execution using examples to learn how to call the endpoint.
* **Best For:**
    * When you want the agent to control interactions with API endpoints.
    * Leveraging native pre-built Extensions (e.g., Code Interpreter, Vertex Search).
    * Multi-hop planning where the agent needs full autonomy.
* **Mechanism:** The agent uses examples to learn how to call the API and executes it automatically.

### 2. Functions (Client-Side Execution)
* **Definition:** The model generates the *parameters* for a function, but your **Client Application** executes the code.
* **Best For:**
    * **Security:** Handling sensitive credentials (API keys) that you don't want to share with the model.
    * **Control:** When you need to transform data *before* giving it back to the agent (e.g., filtering a huge JSON response).
    * **Timing/Order:** For batch operations or human-in-the-loop reviews.
* **Flow:** Model -> Returns JSON -> Client executes Code -> Client returns result to Model.

### 3. Data Stores (Retrieval/RAG)
* **Definition:** A read-only connection to structured or unstructured data sources (PDFs, Websites, Databases) that converts documents into vector embeddings.
* **Best For:**
    * **Grounding:** Preventing hallucinations by anchoring responses in your private data.
    * **Dynamic Knowledge:** Accessing information that changes frequently or isn't in training data (e.g., internal policies, financial spreadsheets).
* **Mechanism:** Uses Vector Search (Embeddings) to find relevant chunks of text and injects them into the context window.

## Summary Table
| Feature | Extensions | Functions | Data Stores |
| :--- | :--- | :--- | :--- |
| **Execution** | Agent-Side | Client-Side | Agent-Side (Retrieval) |
| **Primary Use** | APIs & Actions | Custom Logic & Security | RAG & Knowledge |
| **Control** | Platform-Managed | Developer-Managed | Platform-Managed |
