---
name: llm-default-architecture
description: Use when deciding how to make frontier LLMs the default cognitive engine in a task, automation, feature, or workflow. Trigger when the main risk is falling back to deterministic-first, keyword-first, or semantic-first designs before checking what frontier models can already do.
---
# LLM-Default Architecture

Goal: choose an architecture where frontier LLMs own the cognition by default and deterministic systems provide the surrounding control structure.

## Core rule
Default to an LLM core unless the problem is obviously a narrow deterministic case.

Before decomposing the system, model it as:

- goal
- state
- tools
- policy
- evaluation
- guardrails

## LLM core fit (+1 each)
- unstructured inputs
- search or exploration
- interpretation
- planning
- synthesis
- dynamic tool choice
- context-sensitive judgment
- changing environments

## Deterministic wrapper fit (+1 each)
- stable schemas
- exact validation needs
- persistent state transitions
- retries, budgets, or rate limits
- rollback needs
- compliance or policy checks
- hard latency or throughput boundaries
- executable tests or graders

## Decision
- Pure deterministic only if the problem is mostly a fixed transform or stable rule system
- LLM-first with deterministic support for most real knowledge-work systems
- Hybrid only means "LLM core plus deterministic scaffolding", not a 50/50 split by default

## Ownership split
LLM owns:
- reasoning
- planning
- search
- synthesis
- tool routing
- code / query generation
- exception handling
- adaptation

Deterministic systems own:
- wrappers and adapters
- schema validation
- idempotency
- retries, timeouts, rate limits
- persistence and state transitions
- tests, graders, validators
- rollback and safe failure

## Anti-patterns
- replacing reasoning with keywords because the task feels large
- using semantic retrieval as a substitute for model cognition
- trying to deterministic-code the whole workflow before running an LLM-first probe

This failure mode is usually legacy automation fallback.

When in doubt, build the thinnest LLM-first probe with strong deterministic validation around it.

## Output
### Goal-state-tools loop
### LLM core fit
### Deterministic wrapper fit
### Recommended architecture
### LLM core
### Deterministic support
### Verifiers and guardrails
### Next prototype
