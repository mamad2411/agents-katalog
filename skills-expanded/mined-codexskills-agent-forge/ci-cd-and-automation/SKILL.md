# CI/CD and Automation

## Description
Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies.

## Core Philosophy: Shift Left, Fail Fast

The earlier in the pipeline you catch a defect, the cheaper it is to fix. Every CI/CD pipeline should:
- Fail within 30 seconds for syntax/type errors
- Fail within 3 minutes for unit test failures
- Fail within 15 minutes for integration test failures
- Never let a known-bad commit reach a deployable artifact

## Principles

### 1. Shift Left
Move quality checks as early in the pipeline as possible.
- Lint and type-check before unit tests
- Unit tests before integration tests
- Integration tests before build
- Build before deployment

### 2. Faster is Safer
Slow pipelines encourage workarounds, skip-the-line requests, and unreviewed code.
- Total pipeline should complete under 20 minutes for most projects
- Parallelize independent jobs aggressively
- Cache dependencies, node_modules, build artifacts
- Use remote caching (Turbo, Nx, Bazel) for monorepos

### 3. Quality Gates
Every artifact that reaches production must pass defined quality gates:

```
Gate 1: Pre-commit (local)
  - Lint passes
  - Type-check passes
  - Unit tests pass
  - No secrets committed

Gate 2: Push (CI)
  - Build succeeds
  - All tests pass
  - Code coverage >= 80%
  - No known vulnerabilities (npm audit, trivy)

Gate 3: PR Merge
  - Approved review
  - All CI checks green
  - Branch up to date with target

Gate 4: Staging Deploy
  - Smoke tests pass
  - Integration tests pass
  - Performance budget met
  - Accessibility checks pass

Gate 5: Production Deploy
  - Canary passes (5% traffic, 10 min)
  - Error rate < 0.1% increase
  - P95 latency < 200ms increase
```

### 4. Feature Flags
Separate deployment from release.
- Deploy code behind feature flags
- Enable flags per environment
- Use flags for gradual rollouts
- Kill switch for instant rollback
- Remove flags after full rollout (flag debt is real)

### 5. Fast Failure Feedback Loops
Developers should know they broke something within minutes, not hours.
- Push webhooks → CI triggers automatically
- PR status updates in real-time
- Slack/Discord notifications for failures
- Blame-aware alerts: tag the author
- Weekly pipeline health reports

## GitHub Actions Patterns

### Standard CI Workflow Structure

```yaml
name: CI
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm test -- --coverage

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
```

### Optimizations
- **Matrix builds**: Test across Node versions, OS, browsers
- **Conditional jobs**: Skip docs-only changes, skip dependency-only changes
- **Caching**: `actions/cache` for `node_modules`, `~/.npm`, build outputs
- **Concurrency**: Cancel in-progress runs on new pushes
- **Reusable workflows**: Extract common patterns into shared workflows
- **Composite actions**: Bundle multi-step logic into single actions

### Deployment Workflows

```yaml
deploy-staging:
  needs: build
  runs-on: ubuntu-latest
  environment: staging
  steps:
    - uses: actions/download-artifact@v4
    - run: ./deploy.sh staging

deploy-production:
  needs: [build, deploy-staging]
  runs-on: ubuntu-latest
  environment: production
  steps:
    - uses: actions/download-artifact@v4
    - run: ./deploy.sh production --canary=5
    - run: ./monitor.sh --wait=10m
    - run: ./promote.sh
```

## Pipeline Patterns by Language

### Node.js / TypeScript
- `npm ci` for deterministic installs
- `npm run build` with `--noEmit` for type checking
- Use `c8` or `vitest` for coverage
- Bundle analysis on every PR

### Python
- `pip install -e .` or `poetry install`
- `ruff check .` for lint, `ruff format --check` for formatting
- `pytest --cov` for test + coverage
- `mypy` for type checking

### Go
- `go vet ./...` for static analysis
- `go test -race ./...` for race detection
- `golangci-lint run` for comprehensive lint
- `go build` for compilation check

### Rust
- `cargo check` for fast compilation check
- `cargo test` for tests
- `cargo clippy` for lint
- `cargo fmt --check` for formatting

## Secrets and Security in CI
- Never hardcode secrets in workflow files
- Use GitHub Secrets / Actions Secrets
- Mask secrets in logs automatically
- Run `trufflehog` or `git-secrets` on every push
- Rotate credentials on a schedule
- Use OIDC for cloud provider access instead of static keys

## Pipeline Monitoring
- Track pipeline duration trends (weekly)
- Track failure rate by stage
- Alert on flaky tests (pass then fail on retry)
- Measure MTTR (mean time to repair) for broken builds
- Dashboard: https://github.com/org/project/actions

## Common Anti-Patterns
- **Fat pipelines**: Running everything in one job. Break into parallel jobs.
- **No caching**: Rebuilding node_modules every time. Cache aggressively.
- **Hardcoded secrets**: In workflow files. Use secrets store.
- **Silent failures**: `|| true` swallowing errors. Remove unconditional passthrough.
- **Overly long pipelines**: >30 min total. Parallelize or split.
- **Config drift**: CI config diverging from local dev setup. Use same lint/test commands.
- **Skipping CI**: `[skip ci]` abused. Require CI on protected branches.

## Usage
When the user asks to set up CI/CD, create pipeline configs, or automate quality checks, load this skill and follow the principles above. Generate `.github/workflows/` files, configure quality gates, and document the pipeline strategy.
