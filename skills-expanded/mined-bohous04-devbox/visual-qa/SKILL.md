---
name: visual-qa
description: Visual QA of a running website from a devbox session — the agent uses a headless browser to verify that the page actually renders. Use when the user says "do a visual QA", "check how it looks", "go through the UI", "take a screenshot of the page", "visual QA", "check the rendered page" — typically after starting a dev server.
---

# visual-qa

Verify the render of a running website **inside the devbox container** with a headless browser — on your own,
without a human and without the mac.

## When to use

The agent in the devbox has finished a web UI and wants to confirm that the page renders (content,
structure, layout). Phrases: "do a visual QA", "check how it looks", "go through the
UI", "screenshot of the page", "visual QA".

## How

Chromium (`/opt/ms-playwright`, headless) and the dev server run in the **same container**,
so QA goes **directly against `http://localhost:<port>`** — no relay, no mac.

Via Playwright MCP:

1. `mcp__playwright__browser_navigate` → `http://localhost:<port>[/path]`.
2. **Primarily `mcp__playwright__browser_snapshot`** — the a11y tree (content and structure
   as text). Cheap on tokens; verifies "is that element / text / state there".
3. `mcp__playwright__browser_take_screenshot` — only when it is about **visuals** (layout, style)
   and you want to see the render as an image.

Interaction (click, form) uses the same `mcp__playwright__browser_*` tools, should QA
require clicking through.

## Difference from `mac-preview`

`mac-preview` / `preview` sends the running website to a **human** on the mac to look at. `visual-qa` is
the agent's **own** QA inside the container. Do not confuse them.

## When you do not see the tools

If `mcp__playwright__*` is missing, Playwright MCP is not registered — this is solved via
`agent-sync` (it registers the built-in `playwright` MCP on the claude-home volume).
**Do not install Chrome nor start another chromium manually** — Chromium is in the image,
only the MCP registration is missing.
