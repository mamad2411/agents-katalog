# hospitality-smoke-test

Pre-deploy smoke test for the hospitality app.

## Trigger

Use when the user says "smoke test hospitality", "test hospitality before deploy", or "run hospitality e2e".

## What it does

Runs the Playwright E2E tests for the hospitality app as a pre-deploy gate.

## Usage

```bash
pnpm --dir apps/hospitality test:e2e
```
