---
name: multi-agent-orchestration
description: design patterns for coordinating multiple agents. Use this to implement Hierarchical, Diamond, Peer-to-Peer, or Collaborative architectures for complex workflows.
---

# Multi-Agent Orchestration Patterns

## Goal
Design robust architectures where specialized agents collaborate to solve complex problems that are too difficult for a single agent.

## Core Design Patterns

### 1. Hierarchical (The "Manager")
* **Structure:** A central **Orchestrator Agent** acts as a router. It classifies the user's intent and delegates the task to a specific specialized agent (e.g., Navigation Agent, Media Agent).
* **Usage:** Best for tasks with clear, distinct domains where a single specialist can handle the request.
* **Flow:** User -> Orchestrator -> Specialist -> User.

### 2. The Diamond Pattern (The "Moderator")
* **Structure:** Similar to Hierarchical, but the specialist's output doesn't go back to the user immediately. It passes through a second central node (e.g., a **Rephraser** or **Safety** agent) to standardize or polish the final response.
* **Usage:** Essential when you need consistent tone, style, or safety guardrails across diverse specialists.
* **Flow:** User -> Orchestrator -> Specialist -> Rephraser -> User.

### 3. Peer-to-Peer (The "Network")
* **Structure:** Agents can hand off tasks directly to one another without returning to a central orchestrator.
* **Usage:** Best for resilience. If the Navigation Agent realizes a query is actually about history, it can hand off directly to the Knowledge Agent, recovering from initial routing errors.
* **Flow:** User -> Agent A -> Agent B -> User.

### 4. Collaborative (The "Mixer")
* **Structure:** Multiple specialists work on the *same* query in parallel. A **Response Mixer** agent then takes the partial answers from all of them and synthesizes a single, comprehensive response.
* **Usage:** Best for multifaceted queries (e.g., "How do I handle hydroplaning?") where you need safety data, physics explanations, and driving tips simultaneously.
* **Flow:** User -> [Agent A, Agent B, Agent C] -> Mixer -> User.

## Orchestration Best Practices
* **Specialization:** Ensure each agent has a narrow, well-defined domain. Specialized agents are easier to optimize and debug than generalists.
* **Adaptive Loops:** Implement retry loops where an agent can reformulate its own query if the initial attempt fails (e.g., broadening search terms if no results are found).
