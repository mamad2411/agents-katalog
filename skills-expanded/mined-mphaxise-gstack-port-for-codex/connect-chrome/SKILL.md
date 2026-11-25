---
name: connect-chrome
description: Chrome session workflow for Codex. Use when the user asks to connect Chrome, use signed-in browser state, or attach a visible browser session for browser-driven work.
---

# Connect Chrome

Use this skill when the task specifically needs Chrome profile state or the user explicitly asks to connect Chrome. For unauthenticated local or public pages, prefer `browse` / `open-gstack-browser` with the in-app Browser path.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Confirm the task really needs Chrome:
   - signed-in website
   - browser extension
   - existing Chrome profile, tabs, cookies, or history
   - explicit user request for Chrome
2. If the task does not need Chrome, route to `browse` or `open-gstack-browser` and use the in-app Browser when available.
3. If Chrome is needed, check whether the Codex Chrome plugin/extension is available in the current session.
4. Use `@Chrome` when available; otherwise report the missing Chrome capability and choose the safest fallback.
5. Make the actual runtime capabilities explicit.

## Guardrails

- Do not imply that a Chrome-specific integration exists if the environment only supports a generic browser path.
- Do not use Chrome for a local/public unauthenticated page when the in-app Browser is enough.
- Do not read browser history or signed-in pages unless the user task requires it and the host asks for/has approval.
