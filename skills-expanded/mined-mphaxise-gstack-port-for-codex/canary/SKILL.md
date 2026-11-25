---
name: canary
description: Post-deploy monitoring workflow for Codex. Use when a live deployment should be watched for obvious breakage, regressions, or unhealthy signals.
---

# Canary

Use this skill after deployment when the right move is to watch the live app for regressions instead of assuming success.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Define the live surface to monitor.
2. Check the most important production signals:
   - page availability
   - console or runtime errors
   - key route health
   - performance drift
3. Record the result in a report if the run should be compared later.
4. If recurring checks are useful, hand off to `cron-scheduler`.

## Guardrails

- Do not treat one successful page load as comprehensive health.
- Be explicit about what was not monitored.
- Prefer short, repeatable checks over broad but vague post-deploy confidence.
