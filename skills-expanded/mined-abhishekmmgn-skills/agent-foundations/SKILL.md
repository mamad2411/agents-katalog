---
name: agent-foundations
description: core cognitive architectures for Gemini agents. Use this to implement reasoning loops (ReAct, Chain-of-Thought) and understand the orchestration layer.
---

# Gemini Agent Foundations

## Goal
Design the "Orchestration Layer"—the cognitive loop that enables an agent to plan, execute, and adapt its actions to achieve a goal.

## Cognitive Architectures

### 1. The ReAct Loop (Reason + Act)
* **Concept:** A cyclic process where the model alternates between internal reasoning and external action.
* **The Loop:**
    1.  **Thought:** The agent analyzes the user's request and plans the next step.
    2.  **Action:** The agent selects a tool (e.g., `Flights`) to execute.
    3.  **Action Input:** The agent generates the specific parameters for that tool.
    4.  **Observation:** The agent receives the output from the tool.
    5.  **Repeat:** The loop continues until the agent determines it has enough info to answer.
* **Prompt Structure:**
    ```text
    Question: [User Input]
    Thought: I need to check the flight status first.
    Action: check_flight_status
    Action Input: {"flight_number": "UA123"}
    Observation: [Tool Output]
    Thought: The flight is delayed. I should check connecting flights.
    ...
    Final Answer: Your flight is delayed.
    ```

### 2. Chain-of-Thought (CoT)
* **Concept:** A linear reasoning path best suited for complex logic or math problems where no external tools are needed. It enables reasoning capabilities through intermediate steps.
* **Usage:** Use when the task requires intermediate reasoning steps but is self-contained within the model's training data.

### 3. Tree-of-Thoughts (ToT)
* **Concept:** A branching reasoning strategy for exploration or strategic lookahead tasks. It generalizes CoT and allows the model to explore various thought chains.
* **Usage:** Best for scenarios with multiple potential solutions, allowing the agent to backtrack and explore different "thought branches."

## Agent vs. Model
* **Model:** Knowledge is limited to training data; single inference based on user query; no native tool implementation.
* **Agent:** Knowledge extended through tools; managed session history for multi-turn inference; native cognitive architecture using reasoning frameworks.
