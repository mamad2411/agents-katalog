---
id: automation-triggers
name: Automation Triggers
description: Use this skill when designing, reviewing, or validating event triggers, schedule triggers, automation jobs, CI/CD pipeline triggers, deployment workflows, and their edge cases.
category: DevOps
---

# Automation Triggers

Specify dependable trigger logic for automation and release workflows.

## When to Use

- You need to map repository events to CI/CD or operations actions.
- You need guardrails to prevent accidental production deployments.
- You are troubleshooting duplicate, missing, or misfired workflow runs.

## Workflow

1. **Enumerate trigger sources**: List all event types (push, pull_request, tag, schedule, workflow_dispatch, repository_dispatch, webhook), target branches, and which workflows or jobs each triggers. Map external systems (Slack, Jira, deploy tools) that emit webhooks or API calls.

2. **Define conditions explicitly**: Use branch filters (`branches`, `branches-ignore`), path filters (`paths`, `paths-ignore`) to narrow when jobs run. For tag-based releases, use `tags: ['v*']` or `tags: ['release-*']` with explicit patterns. For cron, specify timezone (`schedule: cron('0 9 * * 1-5', 'America/New_York')`) to avoid drift. For manual runs, use `workflow_dispatch` with optional inputs; for cross-repo or API-triggered runs, use `repository_dispatch` with event types.

3. **Add safety checks**: Use concurrency groups (`concurrency: group: deploy-${{ github.ref }}, cancel-in-progress: false`) to prevent duplicate deploys. Require manual approval for production via `environment: production` with protection rules. Add idempotency keys for webhook-triggered jobs. Configure retry limits and backoff for flaky triggers.

4. **Test representative scenarios**: Run workflows for push to feature branch, PR open/update, merge to main, tag push, cron fire, and manual dispatch. Verify path filters exclude irrelevant changes. Simulate webhook retries and ensure idempotency.

5. **Document ownership**: Record who owns each trigger, how to change it, and what downstream systems depend on it. Include runbook links for troubleshooting.

## Common Pitfalls

- **Missing concurrency controls**: Without `concurrency`, multiple pushes or rapid webhook retries can start duplicate deploy jobs. Use `concurrency: group: <unique-key>` and decide whether to cancel in-progress or queue.

- **Overly broad path triggers**: `paths: ['**']` or omitting path filters causes every push to run expensive jobs. Restrict to relevant dirs (e.g., `paths: ['app/', 'lib/']`) so docs-only or config changes skip builds.

- **Cron drift**: Cron runs in UTC by default; specify timezone to match team hours. Avoid overlapping schedules that can double-run jobs. Use `schedule` with `workflow_dispatch` so cron can be tested manually.

- **Webhook retry storms**: External systems often retry failed webhooks. Without idempotency keys or deduplication, each retry starts a new run. Use `X-Request-Id` or payload hash to dedupe; respond 200 quickly and process async.

## Trigger Configuration Patterns

**GitHub Actions**:
```yaml
on:
  push:
    branches: [main]
    paths: ['src/**', 'package.json']
  pull_request:
    branches: [main]
    paths-ignore: ['docs/**', '*.md']
  schedule:
    - cron: '0 9 * * 1-5'
  workflow_dispatch:
    inputs:
      env: { type: choice, options: [staging, prod], default: staging }
  repository_dispatch:
    types: [deploy-request]
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: false
```

**GitLab CI**:
```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
    - if: $CI_COMMIT_BRANCH == "main" && $CI_PIPELINE_SOURCE == "push"
    - if: $CI_COMMIT_TAG =~ /^v\d+\.\d+/
    - when: manual
only:
  changes: [src/**/*, package.json]
except:
  changes: [docs/**]
```

**Generic webhook** (e.g., Jenkins, CircleCI): Use a single endpoint with `X-Event-Type` or `X-Signature` for validation. Parse payload to determine job; include `idempotency_key` in body. Return 200 within 5s to avoid retries; process asynchronously.

## Output Format

```markdown
## Trigger Matrix
| Event | Condition | Workflow/Job | Environment |
|-------|-----------|--------------|-------------|
| push | main, paths: src/ | build-and-deploy | production |
| pull_request | main | test | - |
| schedule | cron 0 9 * * 1-5 | weekly-report | - |
| workflow_dispatch | manual | deploy | staging |
| repository_dispatch | type: deploy-request | deploy | production |

## Safety Controls
- Concurrency: group by ref/env; cancel-in-progress: false for deploys
- Approval gates: production requires manual approval
- Retry policy: webhook endpoint returns 200 immediately; 3 retries with exponential backoff for failed jobs

## Validation Checklist
- [ ] No duplicate runs for same event (concurrency tested)
- [ ] Protected branches require approvals
- [ ] Production trigger path is explicit (no wildcard to prod)
- [ ] Path filters verified with docs-only and code-only pushes
- [ ] Cron timezone and schedule documented
- [ ] Webhook idempotency and retry behavior defined
```

## Constraints

- Prefer explicit conditions over broad wildcard triggers.
- Include failure and retry behavior for critical automations.
- Avoid assumptions about one CI vendor unless requested.
- Do not recommend disabling branch protection or approval gates for convenience.
- Specify timezone for all cron schedules.
