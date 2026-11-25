---
name: "playwright"
description: "Use when the task requires automating a real browser from the terminal (navigation, form filling, snapshots, screenshots, data extraction, UI-flow debugging) via `npx @playwright/cli`."
---


# Playwright CLI Skill

Drive a real browser from the terminal using `@playwright/cli`. 
Treat this skill as CLI-first automation. Do not pivot to `@playwright/test` unless the user explicitly asks for test files.

## Prerequisite check (required)

Before proposing commands, check whether `npx` is available:

```bash
command -v npx >/dev/null 2>&1
```

If it is not available, pause and ask the user to install Node.js/npm (which provides `npx`). Provide these steps verbatim:

```bash
# Verify Node/npm are installed
node --version
npm --version

# If missing, install Node.js/npm, then:
npm install -g @playwright/cli@latest
playwright-cli --help
```

Once `npx` is present, proceed with the CLI commands. A global install of `@playwright/cli` is optional but helpful if used frequently.

## Quick start

Use `npx @playwright/cli` to run commands:

```bash
npx @playwright/cli open https://playwright.dev --headed
npx @playwright/cli snapshot
npx @playwright/cli click e15
npx @playwright/cli type "Playwright"
npx @playwright/cli press Enter
npx @playwright/cli screenshot
```

If the user prefers a global install, this is also valid:

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
```

## Core workflow

1. Open the page.
2. Snapshot to get stable element refs.
3. Interact using refs from the latest snapshot.
4. Re-snapshot after navigation or significant DOM changes.
5. Capture artifacts (screenshot, pdf, traces) when useful.

Minimal loop:

```bash
npx @playwright/cli open https://example.com
npx @playwright/cli snapshot
npx @playwright/cli click e3
npx @playwright/cli snapshot
```

## When to snapshot again

Snapshot again after:

- navigation
- clicking elements that change the UI substantially
- opening/closing modals or menus
- tab switches

Refs can go stale. When a command fails due to a missing ref, snapshot again.

## Recommended patterns

### Form fill and submit

```bash
npx @playwright/cli open https://example.com/form
npx @playwright/cli snapshot
npx @playwright/cli fill e1 "user@example.com"
npx @playwright/cli fill e2 "password123"
npx @playwright/cli click e3
npx @playwright/cli snapshot
```

### Debug a UI flow with traces

```bash
npx @playwright/cli open https://example.com --headed
npx @playwright/cli tracing-start
# ...interactions...
npx @playwright/cli tracing-stop
```

### Multi-tab work

```bash
npx @playwright/cli tab-new https://example.com
npx @playwright/cli tab-list
npx @playwright/cli tab-select 0
npx @playwright/cli snapshot
```

## Reference

Open only what you need:

- CLI command reference: `references/cli.md`
- Practical workflows and troubleshooting: `references/workflows.md`

## Guardrails

- Always snapshot before referencing element ids like `e12`.
- Re-snapshot when refs seem stale.
- Prefer explicit commands over `eval` and `run-code` unless needed.
- When you do not have a fresh snapshot, use placeholder refs like `eX` and say why; do not bypass refs with `run-code`.
- Use `--headed` when a visual check will help.
- When capturing artifacts in this repo, use `output/playwright/` and avoid introducing new top-level artifact folders.
- Default to CLI commands and workflows, not Playwright test specs.
