---
name: land-and-deploy
description: Merge-and-verify release workflow for Codex. Use when a reviewed change should be landed, deployed, and checked in production.
---

# Land And Deploy

Use this skill after a branch is reviewed and ready to move from approved code to verified production.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Workflow

1. Confirm the branch is actually ready to land.
2. Merge using the repo's normal process.
3. Wait for CI and deployment to complete.
4. Verify production health using the best available path:
   - deployment status
   - health endpoint
   - targeted canary checks
5. Save a short deploy report when the repo benefits from durable release history.

## Guardrails

- Do not land code with unresolved critical review or test failures.
- Do not claim production verification if you only verified the branch locally.
- Stop and report clearly on merge conflicts, failed CI, or unhealthy deploys.
