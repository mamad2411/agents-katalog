---
name: use-playwright-cli
description: Use when the user wants to automate, inspect, debug, or verify browser behavior in this repo with Playwright CLI, or wants concise guidance on using Playwright CLI inside Codex.
---

# Use Playwright CLI

Use this skill when a task needs browser-level verification instead of source-only inspection. Typical cases:

- Reproduce a UI bug in a running app
- Click through a flow and confirm it behaves as expected
- Capture a screenshot or visual proof
- Check console, network, or navigation behavior
- Explain how to ask Codex to run a Playwright CLI workflow

## How to use it

1. Start or confirm the app you want to test.
2. Invoke this skill explicitly with `$use-playwright-cli` when you want Codex to handle the browser flow.
3. Give the target URL, the user journey, and the expected result.
4. Ask for concrete evidence when needed: screenshot, failing step, selector, or error text.

## Good prompts

- `Use $use-playwright-cli to open localhost:5173 and verify the homepage renders.`
- `Use $use-playwright-cli to reproduce the modal bug and capture the failure.`
- `Use $use-playwright-cli to click through checkout and report any console errors.`
- `Use $use-playwright-cli to explain the Playwright CLI steps for this repo.`

## Execution rules

- Prefer stable selectors and visible text over brittle DOM paths.
- Wait for the UI to settle before asserting results.
- If the app is not running, start it first or ask for the dev server command.
- If source inspection is enough, read the files first instead of using browser automation.
- When a browser run fails, report the exact step, selector, or error that broke.

## Output

When you use this skill, return a short, actionable result:

- what was tested
- the command or steps used
- the outcome
- any evidence or blocker
