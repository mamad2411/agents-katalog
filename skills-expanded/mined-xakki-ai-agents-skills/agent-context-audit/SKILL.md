---
name: agent-context-audit
description: 'Assess agent context and agent-skill-find budgets using the real runtime interfaces. Use when asked why context is consumed or to optimize it. RU: бюджет контекста, что съедает контекст.'
disable-model-invocation: true
---

# Context budget

Use when the user asks why an agent's context or skill discovery budget is consumed or wants a measured optimization. Identify the runtime, selected session, component types, available measurements and applicable limits. Inspect the actual model-visible catalog, active instructions and configured tools only through authorized interfaces; a configured component is not necessarily loaded in every turn.

Measure token counts with the runtime's real tokenizer or reported metrics when available. Clearly label byte counts, word-based estimates, missing schemas and frozen-session behavior; do not add them as if they were measured tokens. Identify omitted descriptions, conflicting discovery policies or duplication with concrete evidence.

Recommend removing repeated instruction text, improving descriptions, deferring conditional detail or selecting an explicit-on-demand subset only where the user permits. Show important before/after descriptions and preserve triggers and required capabilities. Configuration changes, disabling tools, deleting skills and updating active sessions require their own scope and verification.
