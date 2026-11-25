---
name: vesper-electron-testing
description: "This skill should be used when testing Vesper Electron UI features or debugging renderer regressions. Apply a layered strategy: component tests first, Playwright Electron E2E for workflows, visual snapshots for regressions, and raw CDP only as fallback diagnostics."
---

# Vesper Electron Testing

Build reliable Electron test coverage without spending cycles on manual CDP debugging.

## When To Use

Use this skill when:
- Validating renderer behavior in Vesper Electron.
- Reproducing and fixing UI regressions (hover/focus/layout/disappearing components).
- Adding or updating test coverage for Scheduler, chat, settings, or navigation flows.
- Designing a test plan for a new Electron feature.

## Core Strategy

Apply this order by default:

1. Component tests (`Vitest` + Testing Library) for local UI/state logic.
2. Electron E2E tests (`Playwright Electron`) for real user workflows.
3. Visual snapshots for layout/readability regressions.
4. Raw CDP scripts only for deep diagnostics or temporary fallback.

Use the smallest layer that can prove the behavior.

## Execution Workflow

1. Define the regression in one sentence.
2. Add or update a deterministic fixture dataset for the scenario.
3. Reproduce with a failing test at the lowest valid layer.
4. Implement the fix.
5. Add a higher-layer E2E test if the behavior depends on true browser interaction (hover/pointer/focus/layout).
6. Capture one screenshot artifact for verification.
7. Run targeted tests, then broader suite if touching shared UI infrastructure.
8. Report root cause, fix, and tests added.

## Vesper-Specific Guardrails

- Prefer stable selectors (`data-testid`) for E2E interaction targets.
- Avoid selectors tied to mutable text content for critical actions.
- Avoid tests that depend on personal workspace state or live schedule data.
- Seed known schedules/personas in tests to keep outcomes deterministic.
- Keep CDP page-dump output minimal; avoid large text extraction that wastes context.

## Commands

Run what exists first:

```bash
# Existing Electron CDP e2e tests
bun test apps/electron/src/__tests__/e2e/

# Run a single e2e file
bun test apps/electron/src/__tests__/e2e/telegram-settings.e2e.test.ts

# Existing helper scripts
node scripts/e2e/scheduler-continuation.e2e.cjs
```

Add Playwright Electron tests when possible:

```bash
# Example (once Playwright is added to repo)
bunx playwright test apps/electron/src/__tests__/playwright/
```

## CDP Fallback Policy

Use raw CDP only when:
- A real Electron window must be introspected quickly.
- Existing tests cannot yet reproduce the issue.

When using CDP fallback:
- Reuse script files under `scripts/e2e/` instead of ad-hoc one-liners.
- Capture compact JSON reports and screenshots.
- Convert the finding into a permanent automated test immediately after fixing.

## Done Criteria

Mark complete only when all are true:

- Regression reproduced in automation before fix.
- Fix validated by passing automation after change.
- At least one persistent test prevents reintroduction.
- Evidence includes command outputs summary and artifact paths.

## References

- `references/electron-test-pyramid.md`
- `references/scheduler-timetable-regression-suite.md`

