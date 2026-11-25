---
name: production-validation
description: "Before declaring engineering work done, validate that what you built matches the production reality — not just the local or test environment — using the real signals (CI, observability, smoke tests)."
---

# Production validation

The biggest gap between agent work and human-quality work is that agents tend to call something done when the local checks pass. Production validation is the layer on top: confirm the change actually behaves correctly where it runs.

## When to run

- Before marking any code-writing planning task as `done`.
- After deploying to staging or production.
- After a rollback under `rollback-runbook`.
- After completing an `incident-postmortem-loop` action item that promises a fix.

## The 4-gate checklist

Treat this as a hard gate before closing the work.

### Gate 1 — CI green

- All required status checks on the PR are green via `github_status_checks`.
- No `skipped` checks that should have run.
- If you cannot fetch CI status, fail closed — do not declare done.

### Gate 2 — Reproducible local checks

- Tests run from a fresh clone (not an incremental cache).
- Lint, typecheck, and unit tests all pass.
- For UI work, the relevant Storybook or Cypress flow runs without manual fix-ups.

### Gate 3 — Observability sanity

- Logs at the relevant level show the expected entries for the new path.
- Metrics (Datadog/Grafana) for error rate, latency, throughput show no regression in the last 15 minutes after deploy.
- If a new metric or alert was added, confirm it is reporting.

### Gate 4 — User-visible smoke

- Trigger the user-visible flow at least once on the deployed environment.
- For background jobs, verify one job completes successfully end-to-end.
- For data writes, confirm the write reached the destination (DB row, file, event).

## What to record

After all four gates pass, post a brief validation summary on the PR or task:

```
production-validation:
  ci: <PR url / commit>
  local_checks: <pass/fail>
  observability: <link to dashboard>
  smoke: <description of the flow run>
```

## Anti-patterns

- Closing the task as soon as the PR merges.
- Skipping Gate 3 because the change "felt small".
- Running the smoke check in local instead of production.
