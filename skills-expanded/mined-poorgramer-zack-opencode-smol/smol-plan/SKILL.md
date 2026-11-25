---
name: smol-plan
description: Turn a fuzzy idea into an atomic, TDD-ready task plan saved at .smol/plans/. Use whenever you want to "plan", "design", or "scope" a non-trivial change before implementing.
---

# /smol-plan

Delegate to the `planner` agent.

Steps:
1. Planner reads `.smol/codemap.md` and `.smol/wiki/*.md` if present.
2. Planner runs Phase 1 — structured `ask_user` form (goal, constraints, success criteria, scope, existing code).
3. Planner runs Phase 2 — at most 3 targeted follow-ups for ambiguities. May invoke `scout` for external info.
4. Planner saves the plan via the `smol_plan` tool and returns the path.
5. Conductor presents the plan summary and asks the user whether to proceed with `/smol-auto` or step through with `/smol-build`.
