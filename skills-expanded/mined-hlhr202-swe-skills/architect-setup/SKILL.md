---
name: architect-setup
description: Initialize or resume Architect project setup by creating only the core architect/ context. Use when the user asks to set up Architect, scaffold Architect context, or recover an interrupted setup before discussion or proposal work.
---

# Architect Setup

Initialize or resume the durable Architect core context, then hand off to discussion. Follow `references/setup-protocol.md` as the source of truth.

## Hard Boundaries

- Create only product, product-guideline, tech-stack, code-style, workflow, and index context. Never create or repair tracks.
- Keep writes under `architect/`; reject absolute paths and `..`.
- Use reviewable edits, preferably patches; never use shell redirection for writes.
- Commit only when the user explicitly requests it in the current conversation.

## Run

1. Read `references/setup-protocol.md`.
2. Audit core artifacts and resume at the earliest incomplete state.
3. Detect Greenfield or Brownfield context and follow the required approval gates.
4. Complete and approve each missing core artifact in order.
5. Stop when core context is ready; summarize changes and recommend `/architect-discuss`.

Bundled `references/workflow.md` is the default workflow. Enumerate `references/code_styleguides/*.md` at runtime so newly bundled guides remain available.
