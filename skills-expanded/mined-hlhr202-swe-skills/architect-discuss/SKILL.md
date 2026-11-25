---
name: architect-discuss
description: Use only when the user explicitly includes `architect-discuss` or directly asks to use the architect-discuss skill. Turns raw or ambiguous product and technical requirements into a product and architecture draft before tracked Architect proposal work.
---

# Architect Discuss

Clarify early product and technical direction before tracked proposal work. Follow `references/discuss-protocol.md` as the source of truth.

## Hard Boundaries

- Require explicit `architect-discuss` invocation.
- Do not create tracked Architect artifacts, modify implementation code, scaffold systems, or run implementation validation.
- Save a standalone draft only to a user-confirmed safe relative path; never overwrite without exact confirmation.
- Do not commit unless explicitly requested in the current conversation.

## Run

1. Read `references/discuss-protocol.md`.
2. Qualify the trigger and build only the repository context needed for the discussion.
3. Progress through resumable gates; ask only material questions and auto-pass established decisions.
4. Generate the synthesis only after readiness, or explicitly label unresolved synthesis.
5. Offer continue, save, split, proposal handoff, or stop. Never execute the handoff automatically.
