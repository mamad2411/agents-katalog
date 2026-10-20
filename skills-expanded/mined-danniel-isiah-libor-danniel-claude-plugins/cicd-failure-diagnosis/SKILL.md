---
name: cicd-failure-diagnosis
description: Diagnose a failing CI/CD run — retrieve the failed-step logs, classify the root cause (config | code/test | infra/transient), and route or fix. Use when a CI run is red, e.g. by the ci-doctor agent and the /sdlc-fix-ci loop. Forge-aware; reuses the cicd-pipeline-audit fix catalog.
---

# CI/CD Failure Diagnosis

How to interpret a *failing CI run* and decide what to do. Used by the `ci-doctor` agent and the
`/sdlc-fix-ci` loop. (Static review of config that has not failed yet is `cicd-pipeline-audit`'s job;
this skill interprets a live red run and reuses that catalog for fixes.)

## 1. Retrieve the failed-step logs (forge-aware)
- GitHub (default): `gh run view <run-id> --log-failed` (and `gh run view <run-id>` for status/jobs).
- GitLab: `glab ci view` / `glab ci trace <job-id>`.

Detect the forge from the git remote (GitHub default; GitLab if the remote is a GitLab host). If
neither CLI is installed/authenticated (`command -v gh` / `command -v glab` fails), fall back to
**paste mode**: ask the user to paste the failing log and diagnose from that.

## 2. Classify the root cause
- **config** — the pipeline itself is broken: action not found / unpinned ref (`@main` 404), YAML the
  runner rejected, missing secret/env/permission, wrong runner image, Docker build error in the
  Dockerfile, misconfigured deploy step.
- **code/test** — the app is broken: compile/build error in source, test assertion failure, linter
  error on app code, dependency lockfile out of sync.
- **infra/transient** — environment, not your fault: runner lost/unavailable, network/registry
  timeout, rate limit, cache-restore glitch.

When a run shows more than one, report the failure that **actually turned the run red** as primary.

## 3. Route
- **config** → fix it here (step 4); the `/sdlc-fix-ci` loop applies the patch with confirmation.
- **code/test** → **do not edit app code**. Route the user to `/sdlc-implement` (the implementer
  fix-loop owns code fixes); summarize the failing test/error so they have a head start.
- **infra/transient** → recommend a plain re-run of the same commit (`gh run rerun <id>` /
  `glab ci retry`); no patch.

## 4. Map a config failure to a fix
Use the `cicd-pipeline-audit` catalog as the source of truth for the fix (one definition of "good
config", shared with the static auditor). Produce a concrete, minimal patch to the workflow/Dockerfile.

## Worked examples
- `Error: actions/checkout@v9 ... not found` → **config** → pin `actions/checkout` to a valid released tag/SHA.
- `npm ci ... lockfile ... out of sync with package.json` → **code/test** → `/sdlc-implement` to regenerate the lockfile.
- `denied: permission_denied: write_package` pushing to the registry → **config** → add the missing registry permission/secret to the deploy job (least-privilege).
- `The runner has received a shutdown signal` → **infra/transient** → re-run the same commit.
- `FAIL src/auth.test.ts ... expected 200 received 500` → **code/test** → `/sdlc-implement`.
