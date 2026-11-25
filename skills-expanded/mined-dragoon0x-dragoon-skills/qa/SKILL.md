---
name: qa
description: Scaffold a playwright e2e test suite with 4 smoke tests (page loads, h1 visible, no console errors, no broken images). Detects the project's stack to set the right baseURL. Writes a runner script that installs browsers on first run. Dragoon does NOT install browsers itself - the runner script does. Defaults to dry-run; pass --apply to write. Run as `node ~/.claude/skills/dragoon/skills/qa/scripts/qa.js`.
version: 1.0.0
---

# /qa

Scaffolds a playwright e2e test suite tuned to the codebase.

## When to use

- The user wants to add e2e tests
- "Set up smoke tests", "scaffold playwright", "browser tests"
- Before a launch, when there are no e2e tests yet

## What it writes

- `playwright.config.ts` configured with the right baseURL for the detected stack (Next.js → 3000, SvelteKit → 5173, etc.)
- `tests/e2e/smoke.spec.ts` with 4 tests: page loads with title, h1 visible, no console errors, no broken images
- `tests/e2e/run.sh` runner that installs `@playwright/test` and Chromium on first run

Dragoon does **not** install playwright or browsers. The runner script does that on first run.

## Run it

```
dragoon qa                      # preview
dragoon qa --apply              # write
```

## Then

```
npm i -D @playwright/test
bash tests/e2e/run.sh
```
