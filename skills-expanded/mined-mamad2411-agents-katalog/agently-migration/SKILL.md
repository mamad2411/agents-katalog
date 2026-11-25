---
name: agently-migration
description: Use when the user wants to migrate an existing LangChain, LangGraph, LlamaIndex, CrewAI, or similar system into Agently, including choosing whether the source belongs to request/agent-side Agently behavior or TriggerFlow orchestration.
---

# Agently Migration

Use this skill for framework migration work. Start here when the source system
already exists and the main decision is how to map it into Agently-native
layers.

If the user is not migrating an existing framework, start with
`agently`.

## Route Inside This Skill

- unresolved migration ownership or mixed LangChain/LangGraph source -> `references/migration-playbook.md`
- LangChain agent-side setup, tools, structured output, retrieval, or short-term memory -> `references/langchain-to-agently.md`
- LangGraph orchestration, stages, checkpoints, interrupts, persistence, streaming, or subgraphs -> `references/langgraph-to-triggerflow.md`

## Native-First Rules

- classify the source system before producing implementation steps
- map LangChain agent-side behavior into `agently-request` and `agently-runtime`
- map LangGraph orchestration behavior into `agently-triggerflow`
- preserve explicit checkpoints, interrupts, persistence, and streaming semantics when they exist in the source
- use migration-specific compatibility notes only when the source API forces them

## Anti-Patterns

- do not flatten graph orchestration into one large request
- do not preserve old abstractions when Agently has a direct native surface
- do not mix agent-side and orchestration-side migration guidance without naming the owner layer first

## Read Next

- `references/migration-playbook.md`
- `references/langchain-to-agently.md`
- `references/langgraph-to-triggerflow.md`
