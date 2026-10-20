---
name: follow-tool-playwright-config-projects
description: Configure Playwright projects, devices, baseURL, retries, and reporters
argument-hint: "[scope]"
related:
  - follow-tool-playwright
  - update-config
  - run-test
  - setup-cicd
---

## Goal

Configure advanced `playwright.config.ts` options — multi-browser projects, device emulation, `baseURL`, retries, reporters — merging with the existing config without clobbering

## Scope

- Editing an existing `playwright.config.ts` (first-time setup → `workflows/setup-playwright`)
- Covers: `projects`, `devices`, `use.baseURL`, `retries`, `reporter`, project dependencies
- Not covered: writing test specs, page objects

## Execute

### 1. Read Current Config

> Goal: understand the existing config before editing

1. Read the current `playwright.config.ts` — run `/deep-review-codebase` domain `review-config` if the config looks suspicious
2. Identify the keys already present — merge with them, never overwrite the whole file
3. If no config is found → run `workflows/setup-playwright` instead

### 2. Configure Projects And Devices

> Goal: set up multi-browser/device projects

1. Use the `projects` array — each project has a unique `name` and `use` options
2. Use `devices` from `@playwright/test`, e.g. `...devices['Desktop Chrome']`, `...devices['iPhone 14']` for device emulation
3. Create separate projects per concern: browsers (chromium/firefox/webkit), viewports (mobile/desktop), or auth state
4. Use project `dependencies` for setup projects (e.g. login → save `storageState`)
5. Run a single project with `bunx playwright test --project=chromium`

### 3. Configure baseURL And Context

> Goal: set `use` options shared across tests

1. Set `use.baseURL` — tests can then use relative paths `page.goto('/login')`
2. Support env override: `baseURL: process.env.BASE_URL ?? 'http://localhost:5173'` for staging/prod targets
3. Add `use` options as needed: `locale`, `timezoneId`, `viewport`, `storageState`, `extraHTTPHeaders`
4. Project-level `use` overrides the global `use` — set only what actually differs

### 4. Configure Retries And Reporters

> Goal: set retries and reporters per environment

1. `retries: process.env.CI ? 2 : 0` — retry in CI only; never use retries to hide flaky tests
2. `reporter`: local uses `[['list'], ['html']]` — CI uses `blob` for sharding, combined with `bunx playwright merge-reports`
3. Add the `['github']` reporter in CI for PR annotations
4. Set `fullyParallel: true` for parallel tests within one file (when tests are independent)

### 5. Verify

> Goal: validate the config and smoke test

1. Run `bunx playwright test --list` — verify tests are discovered per project
2. Run `bunx playwright test --project=<name>` to smoke 1 spec per project
3. If it breaks → revert the key just changed and report the diff — run `/report-before-after`

## Rules

- Merge with the existing config — never rewrite the whole file unless necessary
- `retries` in CI only — local must see failures immediately
- `baseURL` must be overridable via env — never hardcode a single environment
- Every project needs a unique `name` — shards/CI filters reference names
- If unsure about a config option → check the official docs or `references/apis.md`

## Expected Outcome

- Config supports multi-browser/device projects with clear names
- `baseURL`, retries, reporters set correctly per environment
- `playwright test --list` shows the right tests for every project
