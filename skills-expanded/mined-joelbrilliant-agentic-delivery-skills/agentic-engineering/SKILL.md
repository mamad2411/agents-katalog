---
name: agentic-engineering
description: Disciplined agentic engineering workflow for clarifying scope, writing build plans, breaking work into vertical slices, designing uncertain interfaces, using TDD tracer bullets, converting QA into durable briefs, and deepening architecture. Use when work needs a plan, refactor path, issue breakdown, test-first implementation, or handoff between agents.
---

# Agentic Engineering

Use this skill to turn vague engineering work into a safe, reviewable slice.

## Default flow

### 1. Clarify only if needed

- If the task is obvious and reversible, act.
- If scope, behaviour, owner, interface, or acceptance criteria are unclear, ask one decision-driving question at a time.
- Include your recommended answer with each question.
- If the answer can be found by reading code or docs, do that instead of asking.
- Do not use clarification as a way to avoid simple work.

### 2. Shape the work

Convert the agreed direction into a concise requirement.

For each slice, capture:

- owner;
- target behaviour;
- likely files or surfaces;
- acceptance criteria;
- blockers;
- human-signoff status;
- required evidence.

Prefer vertical slices with user-visible behaviour. Avoid horizontal plumbing unless it is the smallest safe step.

### 3. Respect the lane

Use explicit roles:

- orchestrator writes the brief and judges final evidence;
- designer/spec agent explores options only when design is in scope;
- builder implements the approved slice;
- reviewer reviews adversarially;
- final judge signs off against brief, evidence, and review outcome.

Do not let multiple agents co-build the same slice unless the write sets are independent and explicitly split.

### 4. Design interfaces before uncertain implementation

For uncertain APIs, modules, or UI surfaces:

- ask for divergent options first;
- prefer simple public interfaces with deep internal implementation;
- avoid abstractions that hide lack of understanding;
- state tradeoffs before building.

### 5. Use TDD tracer bullets where risk warrants it

- Write one behaviour test through a public interface.
- Implement the minimum to go green.
- Repeat one behaviour at a time.
- Refactor only while green.
- Avoid private-method tests and mock-heavy tests that lock implementation details.

### 6. Turn QA into durable briefs

Capture:

- what happened;
- expected behaviour;
- reproduction steps;
- evidence;
- severity;
- candidate files or functions.

Start with user-facing behaviour. Implementation details support the bug report, they are not the bug report.

### 7. Deepen architecture deliberately

Before broad changes:

- read current state, recent work, and relevant docs;
- name the domain concepts;
- prefer deep modules with small interfaces;
- use the deletion test: if removing a module spreads the same complexity into callers, it was earning its keep;
- evaluate seams by locality, leverage, test surface, and number of real adapters or uses;
- propose architecture changes before mutating them.

## Hard stops

- Do not create external issues, comments, posts, hooks, or writes without explicit approval.
- Do not bulk-install upstream scripts into live config without security intake.
- Do not let multiple agents co-build the same slice by default.
- Do not claim done without evidence: tests, build, runtime check, browser check, or a named blocker.
