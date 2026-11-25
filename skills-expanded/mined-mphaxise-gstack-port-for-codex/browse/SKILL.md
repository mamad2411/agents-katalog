---
name: browse
description: Browser QA for Codex using @Browser, @Chrome, Computer Use, or repo-local tooling. Use when a user needs rendered-page verification of a web app, page flow, or deployment.
---

# Browse

Use this skill when the task requires browser-based verification instead of static code reading.

This port was reconciled against `garrytan/gstack` at commit
`94993f74012782fd94416dd44b8314f6363a13a4`.

## Important Adaptation

This repo ports the browse workflow, not the upstream browser daemon, telemetry, or Playwright binary itself. Before testing, read `references/runtime-strategy.md` and choose the best documented Codex browser surface for the target:

- `@Browser` / in-app browser for local dev servers, file-backed previews, and public unauthenticated pages
- `@Chrome` for signed-in browser state, browser extensions, or existing Chrome-profile context
- Computer Use for desktop GUI flows that browser tools or structured integrations cannot cover
- repo-local Playwright only when the target repo already owns the scripts, fixtures, and dependencies

## Core Jobs

- verify a page loads and key elements appear
- test a user flow end to end
- capture before/after evidence for bug reports
- inspect console, network, or page state when the tooling allows it
- check responsive layouts and authenticated flows when possible

## Workflow

1. Choose the runtime path from `references/runtime-strategy.md`.
2. Translate the desired action using `references/browser-command-map.md`.
3. Test the target page or flow.
4. Collect evidence: screenshots, repro steps, state changes, and any blind spots.

## Guardrails

- Never claim browser automation happened if you only performed HTTP or static checks.
- If authenticated access is required, coordinate with `setup-browser-cookies`, `@Chrome`, or an app-supported test login path.
- Report what was tested, what was blocked, and what remains unverified.
- Do not vendor upstream GStack browser runtime pieces into this repo during a QA task.
