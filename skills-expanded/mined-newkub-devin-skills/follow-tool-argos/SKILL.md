---
name: follow-tool-argos
description: Argos (argos-ci) — open-source visual testing with Playwright SDK, baseline/review workflow
argument-hint: "[project-or-test-file]"
related:
  - deep-test
  - follow-tool-playwright
  - follow-my-techstack
  - run-test
  - follow-tool-storybook
---

## Goal

Add visual regression testing with Argos (MIT, `argos-ci/argos`) — screenshots captured in Playwright tests, baselines resolved from Git history (no committed PNGs), visual diffs surfaced as a pull-request check reviewable by humans and AI agents

## Scope

Use when a web project needs visual/UX regression coverage — the `visual` domain of `/deep-test` and `/run-test visual`

- Captures via the Playwright SDK (`@argos-ci/playwright`); Cypress/Storybook SDKs exist but Playwright is the default here
- Upload goes to an Argos project (hosted free tier or self-hosted — the platform repo is MIT); CI token is `ARGOS_TOKEN`
- Functional assertions stay in Playwright — Argos reviews pixels, not behavior

## Execute

### 1. Install

> Goal: wire the SDK into the existing Playwright setup

1. `bun add -d @argos-ci/playwright` via `/run-install` (Node 22+ for the toolchain)
2. Create an Argos project (hosted app or self-hosted instance) and take the project token from Settings → General → Token
3. Store the token as a CI secret — never in the repo (`/check-secrets` applies)

### 2. Configure The Reporter

> Goal: upload screenshots only from CI

```ts
// playwright.config.ts
import { defineConfig } from "@playwright/test";
import { createArgosReporterOptions } from "@argos-ci/playwright/reporter";

export default defineConfig({
  reporter: [
    process.env.CI ? ["dot"] : ["list"],
    ["@argos-ci/playwright/reporter", createArgosReporterOptions({ uploadToArgos: !!process.env.CI })],
  ],
  use: {
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    launchOptions: { args: ["--disable-lcd-text", "--font-render-hinting=none"] },
  },
});
```

### 3. Capture Screenshots

> Goal: stable, meaningful screenshots

1. In tests: `await argosScreenshot(page, "homepage")` after `page.goto(...)`
2. Screenshots land in `./screenshots` — add it to `.gitignore` (`/update-gitignore`)
3. Cover multiple routes and viewports (Playwright projects per viewport); name screenshots semantically (`homepage`, `checkout--tablet`)

### 4. CI And Review

> Goal: visual diffs become a PR check

1. Run `npx playwright test` on CI with `ARGOS_TOKEN` set (GitHub Actions also supports OIDC/tokenless auth)
2. First run on the default branch establishes the baseline; PR builds compare against it and post a check
3. Review the build in Argos: approve intended changes (approved builds become future baselines), request fixes on regressions
4. Watch the flaky badge/stability score — unstable screenshots get fixed at the source, not ignored

## Rules

### 1. No Baselines In The Repo

- Never commit reference PNGs; Argos picks baselines from Git history — that is the point of using it over `toHaveScreenshot()`

### 2. CI-Only Comparison

- Upload with `uploadToArgos: !!process.env.CI` — local runs don't pollute the project; text-rendering flags are mandatory to avoid machine-vs-CI diffs

### 3. Deterministic Screenshots

- Freeze time, seed data, disable animations, log in to a fixed account or inject fixtures — a flaky pixel diff destroys review trust
- Mock external content (dates, ads, avatars) via `/follow-lib-mswjs` or Playwright routes

## Expected Outcome

- Visual regressions caught as PR checks with zero committed snapshots
- Stable screenshot pipeline (fonts/animations/data deterministic)
- Review history in Argos doubles as the approved-change audit trail
