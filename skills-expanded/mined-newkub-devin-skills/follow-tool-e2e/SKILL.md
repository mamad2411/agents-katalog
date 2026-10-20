---
name: follow-tool-e2e
description: Agentic E2E testing (tester.army) web/mobile — act/assert, screen locators, replay cache
argument-hint: "[test-file-or-goal]"
allowed-tools:
  - exec
  - read
  - write
  - edit
  - grep
  - find_file_by_name
related:
  - run-test
  - follow-my-techstack
  - check-secrets
  - deep-review-codebase
---

## Goal

Write and run e2e tests with the `e2e` framework (e2e.tester.army) — choose the agentic level per step: deterministic locators (`screen` + `expect`), agent goals (`agent.act` from natural language), or a mix in one test — the same test runs on both web (Playwright engine) and mobile (iOS/Android via agent-device)

## Scope

Use when the project installs the `e2e` package or needs agentic testing — general E2E strategy choice → `/deep-test e2e`; mobile-specific → `/deep-test mobile`; catalog default → `/follow-my-techstack`

- Deterministic test suites that need no model → `screen`/`expect` steps only (no token cost)
- API checks can be mixed into the same test file via `fetch` + value matchers

## Execute

### 1. Setup

> Goal: install and configure the runner

1. `bun add -d e2e` via `/run-install` (packages split by platform — see `references/apis.md`)
2. Configure the model for agent steps: subscription (ChatGPT/Copilot/SuperGrok), API key via AI SDK providers, or a local model — see `references/cli.md`
3. Define targets: `web` (Chromium via Playwright), iOS simulator, Android emulator
4. Import `test` from `@e2e-dev/web` or `@e2e-dev/mobile` to get typed `browser`/`device` fixtures

### 2. Write Test

> Goal: combine the 3 step types at the right points

```ts
import { test, expect, unique } from 'e2e';

test('member upgrades to Pro', async ({ app, agent, screen }) => {
  await app.open('/settings/billing');
  await agent.act('upgrade the workspace to Pro');
  await agent.assert('the invoice preview shows a prorated amount');
  await expect(screen.getByRole('status')).toContainText('Pro');
});
```

- **Goal** — `agent.act('one goal per call', { params })` — the agent picks its own actions; use `unique()` for values that change every run so the replay cache still works; use `Secret` for passwords (the model never sees the real value)
- **Assertion** — `agent.assert` (current screen), `agent.waitFor` (wait until a real condition; the model is called only when the screen changes), `agent.extract` → Standard Schema (e.g. Zod); `{ vision: true }` when pixels must be judged (chart/layout)
- **Locator** — `screen.getByRole/getByLabel/getByTestId` (that priority order), `.filter()/.first()/.nth()` when multiple nodes match, actions `tap/fill/swipe`, `expect(locator)` retries until pass/timeout — costs no model call

### 3. Structure And Run

> Goal: organize the suite and run the right scope

1. `describe` + `{ tags }`, `beforeEach`, per-test `{ retries, timeout }`, `{ serial: true }` for flows spanning tests, `test.skip(condition, reason)`, `test.extend` for fixtures
2. `bunx e2e run tests/x.e2e.ts:12` / `--grep checkout` / `--target web` — see `references/cli.md`
3. Exploring with no test file → `e2e explore` lets the agent pursue a goal and report findings
4. `e2e mcp` — expose a live app session so a coding agent can inspect/interact via MCP

### 4. Cache And Debug

> Goal: cut cost and debug failures

1. An `agent.act` whose later check passes → recorded; the next run replays from cache without calling the model — the agent steps in only when the app changes
2. `assert`/`waitFor`/`extract` always call the model (never cached)
3. Read the trace page + evidence + model input in the report — registered secrets are redacted
4. Flaky `act` → make the instruction more specific, move repeated wording into the agent `context`, or convert it to a locator step

### 5. CI

> Goal: run on CI and report

- GitHub Actions, EAS Workflows, Bitrise, Codemagic — the `@e2e-dev/github` reporter posts a per-run comment on the PR
- Hosted targets: `@e2e-dev/kernel` (Kernel Chromium), `@e2e-dev/eas` (EAS simulators/emulators)
- After the suite goes green → run `/run-test` and `/check-secrets` to confirm no secret is in the test files

## Rules

### 1. Await Everything

- await every agent call, screen call, `expect.poll` — a test that returns while steps are still running fails with `STEP_NOT_AWAITED`
- direct reads (`textContent()`) do not retry — use an `expect` matcher instead when waiting is needed

### 2. Secrets

- pass secrets only via `Secret`/`params` — never interpolate them directly into the goal string
- sign in once and reuse the session across tests

### 3. Determinism First

- use `agent.*` only where a selector cannot be written or changes often — where the exact action is known, use a `screen` locator (free, deterministic)
- always follow `agent.act` with an `expect` locator check — the cache records only goals whose later check passes

- Use /deep-test e2e when a framework/strategy choice is needed
- Use /deep-test mobile for device specifics
- Use /deep-review-codebase domain `review-test` for suite review

## Expected Outcome

- Tests mixing deterministic + agentic steps at the right points, runnable on web + mobile targets
- Replay cache cuts model calls; report/debug is readable; secrets never leak into model input
