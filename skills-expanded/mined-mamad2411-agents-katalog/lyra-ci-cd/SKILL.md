---
name: lyra-ci-cd
description: "Language-agnostic CI/CD rules across GitHub Actions, GitLab CI, and CircleCI for pipelines that stay fast, safe, and reversible."
compatibility: "No tools required. Optional: CI platform CLI (gh, glab, circleci), Docker, kubectl, terraform. Wires with lyra-tdd, lyra-code-review, lyra-e2e-testing."
---

# lyra-ci-cd

## What it does

> **Successor note:** for containerized stacks, [`lyra-ci-cd-automation`](../lyra-ci-cd-automation/SKILL.md) restates these core rules in their current form (actions pinned by commit SHA, OIDC, digest promotion, signing) and supersedes this skill where the two disagree — e.g. prefer SHA pins over the `@v4` tags shown in the examples below. Reach for this skill for deliberately minimal, non-container pipelines.

CI/CD pipeline rules that hold across GitHub Actions, GitLab CI, and CircleCI. The pipeline is the source of truth: stages gate each other in cost order, quality gates block merge, promotion moves one artifact through dev → staging → prod, and every deploy has a tested rollback. Caching and parallelization keep the loop fast; secrets stay out of code and logs. The three Lyra gate skills plug in as non-optional stages.

| Gate   | Lyra skill         | Stage                  | Blocks merge when                                           |
| ------ | ------------------ | ---------------------- | ----------------------------------------------------------- |
| Test   | `lyra-tdd`         | `test`                 | Branch coverage < 100%, dummy tests, mutation MSI < 95%     |
| Review | `lyra-code-review` | Pre-merge              | Any P0 finding, unresolved P1 without written justification |
| E2E    | `lyra-e2e-testing` | Post-staging, pre-prod | E2E suite fails on staging                                  |

## The rules

### 1. Stages gate each other in cost order: lint → type-check → test → build → deploy

Cheap checks run first so a two-second lint failure kills the pipeline before a two-minute build; each stage depends on the previous one and no stage runs until its gate passes. GitLab uses `stages:` + `needs:`, CircleCI uses `requires:` — same pattern, different syntax.

```yaml
# bad — one job, build before lint, deploy runs regardless
jobs:
  everything:
    steps:
      - run: npm run build      # expensive, before lint
      - run: npm run lint
      - run: npm test
      - run: ./deploy.sh        # runs even if lint failed

# good — gated, ordered, fail-fast
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run lint
  type-check: { needs: lint }       # setup-node + npm run type-check
  test:        { needs: type-check }
  build:       { needs: test }
  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    steps: [ { uses: actions/download-artifact@v4 }, { run: ./deploy.sh } ]
```

### 2. Quality gates block merge — no bypass, no override

Every PR passes lint, type-check, and the full test suite before merge: no `--no-verify`, no "skip CI" labels, no `allow_failure: true` on gates, no "I tested it locally." Branch protection enforces required status checks and blocks direct commits and force-push to main.

### 3. Promotion is one-way: dev → staging → prod, same artifact

Staging is automatic on merge to main; prod requires a version tag plus human approval on a protected environment. The artifact that passed staging is the one that ships — never rebuild for a different environment, and never deploy to prod from a laptop.

### 4. Match deployment strategy to risk

| Strategy   | When                                            | Rollback                          |
| ---------- | ----------------------------------------------- | --------------------------------- |
| Rolling    | Stateless services, backward-compatible changes | Re-deploy previous image          |
| Blue-green | Zero-downtime, instant rollback needed          | Switch traffic back to idle env   |
| Canary     | High-risk, uncertain impact                     | Stop canary, traffic auto-reverts |

Canary steps 5% → 25% → 50% → 100% with health checks at each stage; blue-green keeps the previous environment warm for 30 minutes after cutover.

### 5. Secrets are injected, never committed, never logged

Secrets come from the platform secret store (GitHub Secrets, GitLab masked+protected variables, CircleCI Contexts), scoped per environment and rotated quarterly. Never `echo` one or pass it as a CLI argument — platforms mask known values but not derived ones, and arguments show up in the process list.

### 6. Cache everything cacheable with deterministic keys

Cache dependencies keyed on the lockfile hash, build artifacts keyed on inputs, and Docker layers keyed on the Dockerfile plus lockfile. Never use timestamp keys — they invalidate for no reason and rebuild from scratch.

### 7. Parallelize independent work

Run independent jobs in parallel and use matrix builds for multi-version, multi-platform testing — a 12-minute sequential pipeline often becomes a 3-minute parallel one. Keep `fail-fast: true` so a failure cancels the rest of the matrix.

### 8. Every deploy has an automated, tested rollback under five minutes

If you cannot roll back in under five minutes, the deployment strategy is wrong; rollback runs on health-check failure, not human intervention. Run a rollback drill in staging monthly — an untested rollback is not a rollback.

### 9. Keep pipelines under ten minutes

Target PR feedback under five minutes and full deploy under ten; measure per-stage duration and attack the slowest stage first, usually the test suite (shard it) or the build (cache it). A 15-minute pipeline is one people avoid running.

### 10. Quarantine flaky gates within 24 hours

A flaky gate is no gate — quarantine on first flake, fix the root cause, un-quarantine with a regression test that reproduces it. Never retry-to-green; track flake rate and auto-quarantine anything above 2%.

### 11. Emit telemetry on every run

Each pipeline emits duration per stage, pass/fail per stage, artifact hash, deploy version, and rollback events. Alert on duration regression > 20%, flake rate > 2%, or rollback rate > 5% — the leading indicators that the pipeline is quietly going wrong.

---

_Part of the [skill collection](../README.md)._