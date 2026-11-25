---
name: dev-init
description: "Initialize repository context using the dev++ workflow. Use when the user invokes /dev-init or asks to inspect project rules, API/frontend inventory surfaces, reusable implementations, docs gaps, verification constraints, or git risks before development."
---

# dev-init

Initialize repository context for the requested scope.

Use any text supplied after the slash command as the requested scope, path, domain, or empty whole-repository context.

Rules:
- Read project instructions first: root and nested `AGENTS.md`, README, and relevant project docs.
- Inspect architecture, runtime/test constraints, git rules, docs conventions, and ownership boundaries.
- Check whether `docs/ai-context/` or an equivalent project intelligence folder exists.
- Scan API, frontend, reusable implementation, shared template, and verification surfaces at a high level.
- Identify gaps, broken workflow chains, missing docs, and unclear requirements.
- Do not edit files, run tests/builds, install dependencies, start services, or change git state.
- If durable docs should be created or refreshed, propose the exact file plan and wait for approval.
- Output a concise initialization report with findings, risks, questions, and recommended next commands.
