---
name: deployment-planner
description: Plan deployment environments, infrastructure, secrets, migrations, workers, schedulers, storage, domains, SSL, and release flow.
---

# deployment-planner

## Token Budget

Medium. Chunk by environment if needed.

## When to Use

- Before first deploy.
- Before production release.
- When deploy target/environment changes.

## Entry Conditions

- The user request matches this skill.
- Required prior outputs are available or explicitly missing.

## Procedure

- Identify deploy target and environments.
- Define secrets/env vars and protection rules.
- Plan build artifacts, migrations, queues/workers, scheduler, storage, cache, domain/SSL.
- Include preflight and smoke checks.
- Hand off rollback requirements to `rollback-planner`.

## Exit Conditions

- Deploy plan is actionable and rollback requirements are explicit.

## Loop Conditions

- If environment conflicts with architecture, route to `architecture-review`.
- If rollback is incomplete, route to `rollback-planner`.

## Escalation Conditions

- Escalate to human when requirements conflict, data loss is possible, production risk appears, or safe verification is not possible.

## Required Output

1. Deployment target.
2. Environment map.
3. Secrets/env requirements.
4. Build/release steps.
5. Migration/worker/storage considerations.
6. Smoke checks.
7. Rollback requirements.


## Universal Contract

For every run, report:

- What was inspected.
- What changed, if anything.
- What assumptions were made.
- What verification was run.
- What loop, blocker, or escalation remains.
- Whether `.agent/` shared state or `context/` should be updated.

Do not edit files unless the user explicitly requested implementation or this skill's task requires file creation.
Do not store secrets in shared state or context.

