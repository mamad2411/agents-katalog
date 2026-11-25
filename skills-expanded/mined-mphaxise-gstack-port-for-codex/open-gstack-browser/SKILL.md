---
name: open-gstack-browser
description: Open or choose the right Codex browser surface. Use when a headed Browser, Chrome, or Computer Use session is needed for testing, inspection, login state, or human handoff.
---

# Open GStack Browser

Use this skill when the user wants a visible browser session rather than a purely headless or code-only review path.

This port is adapted from `garrytan/gstack` at commit `11de390be1be6849eb9a15f91ff4922dd16c589a`.

## Workflow

1. Identify the best available browser runtime in the current environment.
2. Choose the documented Codex surface:
   - `@Browser` / in-app browser for local dev servers, file-backed previews, and public unauthenticated pages
   - `@Chrome` for signed-in browser state, browser extensions, or Chrome-profile context
   - Computer Use for desktop GUI flows that Browser/Chrome cannot cover
   - repo-local Playwright only when the target repo already owns that test path
3. Launch or attach to a visible session when the tooling allows it.
4. Use that surface for inspection, QA, or handoff.
5. Report clearly if the environment only supports headless, read-only, or manual alternatives.

## Guardrails

- Do not claim a headed browser was opened if the environment could not do it.
- Do not use Chrome-profile context when the in-app Browser is sufficient for a local/public page.
- Prefer the repo's normal browser workflow when one already exists.
- Keep the handoff path explicit when human interaction is required.
- Do not install or vendor upstream GStack browser daemons as a side effect of opening a browser.
