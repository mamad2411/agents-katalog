---
name: follow-tool-playwright-setup-playwright
description: Install Playwright with browsers and a basic playwright.config.ts
argument-hint: "[scope]"
related:
  - follow-tool-playwright
  - run-test
  - update-tests
  - setup-cicd
---

## Goal

Install and configure Playwright for the first time, ready to run E2E tests — packages, browser binaries, basic config, smoke test

## Scope

- First-time Playwright setup in a web project
- Covers: install, `playwright install`, basic `playwright.config.ts`, sample test, verify
- Not covered: advanced projects/devices/reporters (`workflows/config-projects`), migration (`workflows/migrate-from-cypress`)

## Execute

### 1. Check Prerequisites

> Goal: check prerequisites and current state

1. Verify the Node.js version meets the requirement — Playwright needs Node >= 20 (check official docs for the latest requirement)
2. Identify the package manager from the lockfile and use it consistently
3. Check `package.json` — if `@playwright/test` is already present (idempotent check) → skip install, go to verify
4. Identify the app's dev server command and port (`bun dev`, `vite`, `next dev`)

### 2. Install Packages And Browsers

> Goal: install `@playwright/test` and the browser binaries

1. Install with `bun add -D @playwright/test` (or the package manager equivalent)
2. Run `bunx playwright install` — installs chromium, firefox, webkit
3. For CI/minimal → install only the browsers used, e.g. `bunx playwright install chromium`
4. Install the VS Code extension for IDE integration (optional)

### 3. Create Config

> Goal: create a minimal `playwright.config.ts`

1. Create `playwright.config.ts` at the root with `defineConfig` from `@playwright/test`
2. Set `testDir` (e.g. `./e2e` or `./tests`) — separate from unit tests
3. Set `use.baseURL` to the dev server (e.g. `http://localhost:5173`)
4. Set `retries: process.env.CI ? 2 : 0`, `workers: process.env.CI ? 4 : undefined`, `forbidOnly: !!process.env.CI`
5. Set `trace: 'on-first-retry'` and `screenshot: 'only-on-failure'` for debugging artifacts
6. Set `webServer: { command, url, reuseExistingServer: !process.env.CI }` so Playwright starts the dev server itself

### 4. Add Scripts And Smoke Test

> Goal: add scripts and write a smoke test

1. Add `"test:e2e": "playwright test"` to `package.json`
2. Write a sample spec: `page.goto('/')` then `expect(page).toHaveTitle(...)` or assert a stable locator
3. Add `test-results/` and `playwright-report/` to `.gitignore`

### 5. Verify

> Goal: smoke check that the setup works

1. Run `bun run test:e2e` — the sample spec must pass with the webServer auto-starting correctly
2. Run `bunx playwright test --ui` if you want to see it in UI mode
3. If verify fails → run `/resolve-errors` max 3 rounds, then stop and report

## Rules

- Use official docs as the primary source — check the docs before using an uncertain option
- Install only the browsers actually used in CI — saves time and disk
- `testDir` must be separate from unit tests — never let Vitest pick up e2e specs
- secrets/env for E2E → `/follow-secret-manager`, never commit
- Never put `page.waitForTimeout()` in a smoke test — use web-first assertions

## Expected Outcome

- `@playwright/test` installed with browsers and a verified `playwright.config.ts`
- Smoke test passes with webServer auto-start
- Artifact dirs are gitignored
