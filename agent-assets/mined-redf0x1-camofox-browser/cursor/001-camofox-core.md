---
description: "Core camofox-browser concepts — element refs, snapshot-first workflow, server basics"
alwaysApply: true
---

# CamoFox Core Rules

## What CamoFox Is
- CamoFox Browser is an anti-detection browser automation server built on Camoufox.
- Primary interface is REST API on port `9377` with CLI wrapper `camofox`.
- OpenClaw-compatible routes are available (`/tabs/open`, `/navigate`, `/snapshot`, `/act`).

## Snapshot-First Workflow (Required)
1. Open/create a tab.
2. Capture snapshot to get current `eN` refs.
3. Interact using refs when possible.
4. Re-snapshot after navigation or major UI updates.

Never assume old refs remain valid after:
- navigation
- modal transitions
- SPA rerenders
- display mode toggles

## Element Refs (`eN`) Rules
- Refs are produced by snapshot endpoints and are user/tab scoped.
- Refs are preferred over selectors for robust automation.
- Treat refs as ephemeral state, not permanent IDs.

## User/Session Rules
- Always keep `userId` consistent through a flow.
- `sessionKey` (or legacy `listItemId`) groups tabs by task.
- `DELETE /sessions/:userId` is the full cleanup operation.

## Server Basics
- Health check: `GET /health`.
- Presets list: `GET /presets`.
- Context display toggle: `POST /sessions/:userId/toggle-display`.

## Critical Safety Rules
- If `CAMOFOX_API_KEY` is configured, provide Bearer auth for protected routes.
- OpenClaw `POST /stop` always requires `x-admin-key`, and it must match configured admin key value.
- Use `--format json` for machine parsing.

## Quick Reference
```bash
camofox open https://example.com         # create tab
camofox snapshot                         # get refs
camofox click e5                         # interact by ref
camofox type e8 "hello"                  # type text
camofox get-url --format json            # structured output
```
