---
name: agent-ops
description: operationalization strategies for agents (AgentOps). Use this to manage internal/external tools, optimize agent "brain" prompts, and handle task decomposition.
---

# Agent Ops (AgentOps)

## Goal
Implement a robust framework for the efficient operationalization of agents, moving beyond simple prototypes to reliable production systems .

## Core Components
Successful AgentOps requires managing the following "agentic" dependencies:
* **Tool Management:** Coordinating internal and external tools and APIs.
* **Agent Brain Prompt:** Defining the core goal, profile, and instructions that drive the model.
* **Orchestration:** Managing the loops of reasoning and planning.
* **Memory:** Handling both short-term working memory (sessions) and long-term storage.
* **Task Decomposition:** Breaking complex user objectives into manageable sub-tasks.

## The Ops Relationship
AgentOps is a subcategory of **GenAIOps** and inherits best practices from its predecessors:
1. **DevOps:** Foundation for deterministic software, CI/CD, and version control.
2. **MLOps:** Management of non-deterministic models and data pipelines.
3. **PromptOps:** Versioning and optimization of the instruction sets.

## Production Best Practices
* **Observability (Traces):** Use "traces" to log the inner workings of an agent, including internal steps and tool calls, to facilitate debugging.
* **Feedback Loops:** Instrument your agent to capture human feedback (e.g., thumbs up/down) to calibrate performance and autoraters.
* **Hybrid Instrumentation:** Track both business-level KPIs (goal completion rate) and application telemetry (latency, errors).
