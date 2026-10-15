---
name: book-release-readiness
description: Reviews production readiness for services, APIs, jobs, queues, integrations, and deployment-sensitive changes. In strict tasks, mandatory after all applicable testing-tool gates and project validation, and before completion or release, when production-path runtime or deployment behavior changes; in default/lite tasks, use on demand when those risks or explicit delivery requirements are present.
---

# Book Release Readiness

Use this Skill as a production-readiness pass before considering a service or integration change complete.

It is derived from the `mini` rule style of `agent-rules-books` and complements project validation, Playwright, Maestro, Chrome DevTools diagnostics, task check, and human release review.

## Strict Development Gate

In a strict task, run this Skill after all applicable testing-tool gates and project validation, and before the task is declared complete or the final release decision when the task changes any production-path:

- Service, API, auth, billing, or notification behavior.
- Background job, queue, scheduler, or data pipeline.
- External integration.
- Deployment, rollout, migration, or runtime operational behavior.

Emit a separate visible review:

```text
Release Readiness Review
Status: ready | needs-mitigation | blocked
Production path and affected users / systems: ...
Failure modes and safeguards: ...
Capacity / backpressure / limits: ...
Observability / alerts / runbook: ...
Rollout / migration / rollback / cleanup: ...
Required validation and result: ...
Optional checks, accountable owner acceptance, and residual risk: ...
```

- `ready`: all required validation ran and passed; applicable production risks, rollout, rollback, and observability are addressed. An optional check may remain skipped only when an explicit accountable owner accepts the documented residual risk.
- `needs-mitigation`: implement the required mitigation or update the release plan, rerun every affected required validation and testing-tool gate, and rerun this Skill.
- `blocked`: any required validation, environment, operational evidence, or rollback path is missing or failed, or the Skill is unavailable. Required checks cannot be waived or converted to residual risk; state the blocker and do not declare the task complete or release-ready.

## When To Use

- Strict: every development task matching a production-path runtime or deployment trigger above. In default/lite, use this Skill when those risks, project rules, or explicit delivery requirements apply.
- The change affects APIs, background jobs, queues, schedulers, external services, auth, billing, notifications, data pipelines, or deployment behavior.
- Failure modes include timeouts, retries, overload, partial outage, data corruption, duplicate work, or user-visible degradation.
- The task is ready for strict check/finish-work or release review.

When no mandatory trigger matches, do not use this Skill for docs-only changes, local-only scripts, simple UI polish, or code paths that are not production-facing unless the user requests it or another concrete release risk warrants it.

## Workflow

1. Identify the production path and the users or systems affected.
2. Check timeouts, retry limits, backoff, cancellation, and duplicate-work safety.
3. Check fallback, graceful degradation, circuit breaking, or isolation where relevant.
4. Check capacity, backpressure, rate limits, and queue growth behavior.
5. Check logs, metrics, traces, alerts, dashboards, and runbook expectations.
6. Check rollout, rollback, feature flag, migration, and cleanup paths.
7. Confirm that all required validation and applicable testing-tool gates ran; separate them from optional checks, and record any optional-check acceptance by an explicit accountable owner.

## Output

Always emit the visible `Release Readiness Review` for a strict gate. When used in a task-level record, also record:

- Production risk summary.
- Failure modes covered.
- Observability and alerting notes.
- Rollout and rollback path.
- Validation performed and skipped checks.
- Residual risk.

Only recurring release standards belong in `docs/spec`.

## Guardrails

Do not block completion with theoretical production risks that do not apply to the current project. A mandatory review must still inspect every applicable category and may mark irrelevant checks `not-applicable`; required validation cannot be skipped, while an optional check needs explicit accountable-owner acceptance and a documented residual risk.
