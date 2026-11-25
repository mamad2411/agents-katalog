---
name: setting-up-ci-cd
description: Sets up and improves CI/CD pipelines (GitHub Actions, GitLab CI, Azure Pipelines) — build, lint, test, security scans, artifact build, environment promotion, deployment strategies (rolling, blue/green, canary), and rollback. Use when creating a pipeline, adding a deployment, fixing a slow or flaky pipeline, or setting up environments.
---

# Setting up CI/CD

## Principles

- **Every push to a branch or pull request:** run the fast checks. Merging is blocked if they fail.
- **Every merge to main:** build the artifact once, then promote that *same* artifact from test to staging to production.
- **Infrastructure and pipelines live in code, in the repo.** No hand-configured servers.
- **Deployments are automated, repeatable, and can be rolled back with one action.**

## Pipeline stages

| Stage | Runs on | Contents | Target time |
|-------|---------|----------|-------------|
| Verify | Every push and PR | Install with cache → format check → lint → type-check → unit tests | < 5 min |
| Integration | Every PR | Integration tests with real services (containers), plus the build | < 10 min |
| Security | Every PR + nightly | Dependency audit, secret scan, static analysis (e.g. CodeQL, Semgrep), container image scan | — |
| Package | Merge to main | Build a versioned artifact or container image, then push it to a registry | — |
| Deploy test/staging | Merge to main | Deploy automatically, run migrations, run smoke and E2E tests | — |
| Deploy production | Tag or manual approval | Gradual rollout, health checks, automatic rollback if they fail | — |

## GitHub Actions starting point

```yaml
name: ci
on:
  push:
    branches: [main]
  pull_request:
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # setup-<language> with dependency caching, then:
      - run: <install command>
      - run: <lint command>
      - run: <type-check command>
      - run: <test command>
      - run: <build command>
```

Replace the `<…>` commands with the real ones from CLAUDE.md.

## Rules

- **Secrets:** keep them in the CI platform's secret store or use OIDC federation to the cloud provider. Never put them in the repo. Use least-privilege tokens, and set `permissions:` explicitly.
- **Supply chain:** pin third-party actions to a commit SHA, and commit lockfiles.
- **Speed:** cache dependencies, run independent jobs in parallel, and split tests into shards when the suite grows.
- **Flaky tests:** fix them or quarantine them right away (see `writing-tests`). Never just re-run until green.
- **Deployment strategies:**
  - rolling — the default
  - blue/green — instant switch and rollback
  - canary — a small percentage of traffic first, then more
  - feature flags — separate deploying code from releasing a feature
- **Database migrations** run as a separate pipeline step before the new code goes live, and must be backward compatible (expand → migrate → contract).
