---
name: cicd-pipeline-audit
description: Audit CI/CD pipeline config (CI workflows + Dockerfiles) for security, correctness, reliability/cost, and plugin-convention issues. Use when reviewing or generating pipeline config — by the pipeline-reviewer (Phase 4) and the release-engineer (Phase 5). Prefers real linters, falls back to a checklist.
---

# CI/CD Pipeline Audit

The single source of truth for *what* to check in a CI/CD pipeline and *how*. Applied by the
`pipeline-reviewer` agent (Phase 4, on pre-existing config) and the `release-engineer` (Phase 5, on
its own freshly-generated config).

## How to check (linter-or-checklist, forge-aware)
Prefer real linters when installed; otherwise review the file(s) against the checklist below.
- GitHub Actions workflows (`.github/workflows/*.yml|*.yaml`): `actionlint` if available.
- Dockerfiles (`Dockerfile`, `*.Dockerfile`): `hadolint` if available.
- GitLab pipelines (`.gitlab-ci.yml`): `glab ci lint` / the GitLab CI lint API if available.

Probe before use (e.g. `command -v actionlint`); if absent, fall back to the checklist — no install,
no hard dependency. **Forge-aware:** GitHub is the default; audit `.gitlab-ci.yml` only when the git
remote is a GitLab host (detect during `stack-detection`). See `devops-gcp` / `release-management`
for forge detection.

## What to check (severity in brackets)
### Security
- [high] Plaintext secrets/tokens/passwords in YAML or Dockerfile — use the forge's secret store.
- [high] Unpinned third-party actions — `uses: org/action@main` or `@v1` instead of a pinned SHA.
- [high] Over-broad `permissions:` — default write-all; set least-privilege per job.
- [high] `pull_request_target` running untrusted code / exposing secrets to forks.

### Correctness
- [high] YAML syntax errors / invalid schema (actionlint catches these).
- [med] Broken `needs:` graph, or jobs that never trigger.
- [med] Dockerfile runs as root (no `USER`); unpinned/`latest` base image; missing `WORKDIR`.
- [low] No `.dockerignore`; no `HEALTHCHECK`.

### Reliability / cost
- [med] No `timeout-minutes` on jobs (a hung job runs to the runner limit).
- [med] No dependency caching (slow, costly runs).
- [med] Deploy not gated behind build+test passing.
- [low] No `concurrency:` group (redundant overlapping runs on rapid pushes).

### Plugin-convention consistency
- [high] Deploy auto-runs on merge/push — must be manual-trigger only (`workflow_dispatch`/approval).
- [med] Production (`main`) deploy missing the idempotent tag + Release step (see `release-management`).
- [low] Branch promotion doesn't follow `development → staging → main`.

## Output
Return findings as a severity-sorted list, one per line: `[severity] file:loc — issue — fix`.
If no pipeline config exists, say so explicitly (nothing to audit). Align severities with the other
inspectors so the orchestrator can merge into one list.

## Worked example
Given `.github/workflows/deploy.yml`:
```yaml
on: { push: { branches: [main] } }
permissions: write-all
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@main
      - run: ./deploy.sh
```
Findings:
- [high] deploy.yml:1 — deploy auto-runs on push to main — make it a manual `workflow_dispatch`/approval job.
- [high] deploy.yml:2 — `permissions: write-all` — scope to least privilege (`contents: read`; `contents: write` only on the tag job).
- [high] deploy.yml:6 — `actions/checkout@main` unpinned — pin to a release tag or commit SHA.
- [med] deploy.yml — no `timeout-minutes` and no build/test gate before deploy.
