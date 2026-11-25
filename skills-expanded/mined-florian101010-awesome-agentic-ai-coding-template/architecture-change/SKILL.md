---
name: architecture-change
description: Architecture change workflow with mandatory ADR and controlled rollout. Use when proposing or implementing a structural/architectural change to the codebase.
disable-model-invocation: true
---

# Architecture Change

Follow `.agent/workflows/architecture-change.md` strictly.

Execution requirements:

1. Write architecture proposal with options/trade-offs.
2. Create/update ADR file in `docs/decisions/` before finalizing.
3. Implement in isolated steps and validate regressions.
4. Sync architecture-relevant docs and `CHANGELOG.md`.
5. Run pre-commit checks before final handoff.
6. End with ADR + DoD confirmation.

No architecture-level change may be closed without ADR entry.
