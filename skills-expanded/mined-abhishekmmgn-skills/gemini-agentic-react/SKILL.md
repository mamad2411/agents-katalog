---
name: gemini-agentic-react
description: strategies for implementing the ReAct (Reason and Act) paradigm. Use this to enable Gemini to use external tools, APIs, and perform multi-step research.
---

# Gemini Agentic ReAct Strategies

## Goal
Enable Gemini to solve complex tasks by combining natural language reasoning with external actions (tools), mimicking how humans operate in the real world.

## The ReAct Paradigm (Reason & Act)

### 1. The Thought-Action Loop
* **Concept:** Instead of answering immediately, the model enters a loop of reasoning and acting until the answer is found.
* **Workflow:**
    1.  **Reason (Thought):** The model analyzes the request and generates a plan of action.
    2.  **Act (Action):** The model performs a specific action (e.g., `Search`, `CodeInterpreter`).
    3.  **Observe (Observation):** The model waits for the result of that action from the external tool.
    4.  **Update:** The model uses the new information to update its reasoning and determine the next step.

### 2. Example Structure
To implement ReAct, the prompt must enforce a strict format so the system knows when to stop generating and execute code.

**Standard ReAct Format:**
```text
Question: [Input]
Thought: [Reasoning about what to do next]
Action: [Tool Name]
Action Input: [Arguments for the tool]
Observation: [Result from the tool - User/System provides this]
... (Repeat until solution is found)
Final Answer: [The conclusion]
