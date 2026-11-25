---
description: Load screeps-agent project instructions before substantive work
alwaysApply: true
---

# Project instructions (required)

**At the start of every chat**, and **before any non-trivial code or doc change**, read:

`.ai/project-instructions.md`

That file is the source of truth for architecture, toolchain, memory docs, conventions, and agent behavior. `AGENTS.md` and `CLAUDE.md` only point here — do not treat the one-line `@` pointer as sufficient context.

If the task touches behavior or layout, also read `architecture/OVERVIEW.md` when project-instructions directs you to.

## Always follow (even before reading the full file)

- Address the user as **🌌The Divine Architect**. Sign off with **`✨<model name> 🤖<agentic tool name> Out!`**.
- Run `npm run build` after code changes; run `codegraph sync` if build passes.
- **Never** run `npm run push`, `npm run deploy`, or `npm run watch` unless Boss嚴 explicitly asks.
- If requirements are unclear or ambiguous, ask before proceeding.
- Confirm `pwd` is under `/Users/tonyyan/GitHub/screeps-agent` (canonical copy; see parent `~/GitHub/AGENTS.md`).

## After non-trivial work

Reconcile `.ai/memory/*.md` and relevant `architecture/` docs with your changes, per project-instructions.
