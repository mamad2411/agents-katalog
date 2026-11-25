---
name: setup-browser-cookies
description: Authenticated browser-session setup for Codex. Use when QA needs signed-in Chrome state, manual login, test-user access, app session seeding, or carefully approved cookie handling.
---

# Setup Browser Cookies

Use this skill when a browser-based workflow needs authentication and the safest path must be chosen before QA starts.

This port is adapted from `garrytan/gstack` at commit `2aa745cb0e4331d683e727ec77385d04cdbb45a2`.

## Workflow

1. Read `references/session-options.md`.
2. Choose the safest available session strategy.
3. Prefer Chrome extension state, manual login, test-user access, or app-supported session seeding before raw cookie handling.
4. Verify the session works before starting QA.

## Guardrails

- Never print raw cookie values.
- Prefer successful page access, domain counts, or session summaries as proof.
- Treat raw cookie JSON import as exceptional and user-provided; prefer `@Chrome`, manual login, or app-supported test-session seeding.
- Do not add upstream cookie-extraction daemons or profile readers to this repo without a separate security review.
