---
name: architect-first
description: "Settle types, module shape, and boundaries before implementation. Trigger: 'architect this', 'design module structure', 'settle types first'. For multi-module changes."
when_to_use: "Activate BEFORE writing code that crosses function/module boundaries or changes public APIs. Do NOT use for single-function fixes or when types are obvious."
argument-hint: "[feature or change to architect]"
disable-model-invocation: true
license: Apache-2.0
compatibility:
  - opencode-native
  - claude-standalone
  - cursor-native
  - codex
metadata:
  author: controlkeel
  version: "1.1"
  category: planning
  ck_mcp_tools: [ck_memory_record, ck_memory_search, ck_review_submit]
  related_skills: [align, plan-slice, investigate]
---

# Architect First

Settle types, module shape, and boundaries before writing code. Cheaper to fix the design now than rewrite callers later.

## Do NOT use when
- Single-function fix (use `tdd-bugfix`)
- Types are obvious and scope is narrow
- The change fits in one module with no boundary changes
- During implementation (design is already approved)

## Workflow

1. Search `ck_memory_search` for prior decisions about the affected area.
2. Investigate existing module boundaries (use `investigate` skill if needed).
3. Define:
   - **Types/structs** for key data structures
   - **Module boundaries**: owns / exposes / depends / does-not for each module
   - **Data flow**: trace primary use case across boundaries
4. Mark unresolved decisions as `[DECISION NEEDED]`.
5. Record design via `ck_memory_record` (type: `decision`).
6. Submit via `ck_review_submit` (review_type: `plan`, plan_phase: `design_options`). **Wait for approval**.

## Design principles

- Boundary discipline — modules own their data and invariants
- Type-system discipline — structs and typespecs, not bare maps
- Subtract before you add — can existing module absorb this?
- Minimize reader load — purpose clear from public API alone

## Output

- Types and structs
- Module boundary definitions
- Data flow for primary use case
- `ck_review_submit` plan awaiting approval
- `ck_memory_record` with the design
