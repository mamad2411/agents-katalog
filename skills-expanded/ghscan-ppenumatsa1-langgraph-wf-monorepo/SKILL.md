---
name: local-validation
description: Run existing underwriting local validation gates and report actionable pass, fail, or blocker status.
---

# Local Validation Skill

Use this skill before completing work that changes frontend, workflow, AG-UI, CopilotKit, durable projections, or runnable release behavior.

## Guardrails

- Run only existing repository commands.
- Use narrow prechecks while iterating, but run the full applicable local gates before declaring completion.
- Do not mask failures; report the exact failing command and rerun command.

## Full local gates

Run these when shared operator or workflow contracts changed:

```bash
make test
make quality
make test-e2e
```

`make test-e2e` is mandatory for frontend, API, AG-UI, CopilotKit, workflow, checkpoint, or run-history changes.

## Narrow prechecks

Use these only as interim checks, not final substitutes for shared-surface changes:

```bash
make test-backend
make test-frontend
```

## Hosted companion gates

If the change touches `backend/foundry/**`, `infra/foundry-hosted/**`, telemetry, or `scripts/foundry/**`, pair local validation with the release skills that run:

```bash
make foundry-smoke
make foundry-eval
```

## Blockers

If a gate cannot run, report the blocker and exact rerun command. Common blockers include:

- Docker daemon unavailable for backend or E2E database setup.
- Playwright or browser runtime missing for `make test-e2e`.
- Missing authenticated Azure context for hosted release gates.

## Reporting

- Report each command run with pass/fail/blocker status.
- Include concise failure or blocker details.
- State whether validation is complete or partially blocked.

