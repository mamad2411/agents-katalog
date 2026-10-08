---
name: ci-cd
description: >-
  CI/CD pipeline shape, local verify commands, deploy order. Load for CI, deploy, pipeline,
  verify job.
---

# CI/CD and verification

## Local verify (discover from repo)

Read root `package.json` scripts before assuming names. Typical monorepo scripts:

| Kind | Purpose |
|------|---------|
| lint | formatter + import-boundary lint (Biome) |
| typecheck | project references + per-member noEmit |
| build | turbo or workspace build |
| test | vitest via turbo filter |
| format fix / check | biome or equivalent |

**Definition of done:** tests for touched behavior; lint/typecheck/build for touched workspaces; brief summary of results to the human.

## CI pipeline (typical shape)

Read `.github/workflows/` (or equivalent) for exact jobs — do not assume paths.

- **Trigger:** PRs run the gating checks; push to main deploys.
- **Path filter:** separate frontend vs backend change detection.
- **Verify (the deploy gate):** the **full** check set — lint, build, typecheck, test, schema check. Deploy jobs run only if it passes.
- **Deploy:** API/backend first (build → upload → migrate → promote); frontend after backend succeeds.
- **Target:** often Cloudflare Workers; secrets via CI env/vars.
- **Gate the deploy _inside the deploy workflow_.** A separate CI workflow runs independently and **can't** block a deploy — so the deploy's own verify must run the full gate, or a direct push (no PR) to a deploy branch can ship a failure. Keep the PR-CI and deploy-verify checks in sync.

## Pre-commit hook

May run formatter on staged files and re-stage. Does not always block on lint failures — still run full verify before finishing.

## Agent rules

- Do not deploy or push unless the human asked.
- When CI fails due to constraints outside your scope — stop, report evidence, offer choices; do not expand scope to green CI.
