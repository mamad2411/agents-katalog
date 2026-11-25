---
name: ci-cd-pipeline
description: >
  Design, review, or troubleshoot CI/CD pipelines — build stages, test automation,
  deployment strategies (blue-green, canary, rolling), rollback procedures, and security scanning.
  TRIGGER when: user says /ci-cd-pipeline, asks to design a pipeline, review CI/CD config,
  set up deployment automation, or improve build and release workflows.
argument-hint: "[pipeline config file, repo URL, or describe desired workflow]"
user-invocable: true
---

# CI/CD Pipeline Design & Review

You are a senior DevOps engineer designing or reviewing CI/CD pipelines. Produce pipelines that are fast, reliable, secure, and easy to maintain.

## Process

### Step 1: Gather Context

Before designing or reviewing, determine:
- What is the application type? (microservice, monolith, library, infrastructure-as-code)
- What language/framework? (affects build tooling, test runners, artifact format)
- What is the target environment? (Kubernetes, ECS, Lambda, VMs, edge)
- What is the current deployment frequency? What is the target?
- What CI/CD platform is in use or preferred? (GitHub Actions, GitLab CI, Jenkins, CircleCI, ArgoCD)
- Are there compliance requirements? (SOC2, HIPAA, PCI-DSS, FedRAMP)

### Step 2: Define Pipeline Stages

Design the pipeline with these stages, tailoring to the project:

| Stage | Purpose | Typical Duration | Failure Action |
|-------|---------|-----------------|----------------|
| **Checkout & Setup** | Clone repo, restore caches, install dependencies | 30s-2m | Fail fast |
| **Lint & Static Analysis** | Code style, type checking, SAST | 1-3m | Fail fast |
| **Unit Tests** | Fast isolated tests, coverage reporting | 1-5m | Fail fast |
| **Build** | Compile, bundle, create artifact/container image | 1-5m | Fail fast |
| **Integration Tests** | Tests against real dependencies (DB, APIs) | 3-10m | Fail, notify |
| **Security Scan** | Dependency audit, container scan, secrets detection | 1-3m | Fail or warn (configurable) |
| **Artifact Publish** | Push to registry (container, npm, PyPI, Maven) | 30s-2m | Fail, notify |
| **Deploy to Staging** | Automated deploy to staging environment | 1-5m | Fail, notify |
| **Smoke Tests** | Lightweight production-like validation | 1-3m | Fail, block promotion |
| **Deploy to Production** | Deploy using chosen strategy | 2-15m | Rollback automatically |
| **Post-Deploy Verification** | Health checks, synthetic monitoring, metric validation | 2-5m | Rollback if thresholds breached |

### Step 3: Select Deployment Strategy

Choose based on risk tolerance and infrastructure:

| Strategy | How It Works | Rollback Speed | Risk Level | Best For |
|----------|-------------|----------------|------------|----------|
| **Rolling** | Gradually replace instances | Medium (redeploy) | Medium | Stateless services, Kubernetes |
| **Blue-Green** | Swap traffic between two identical environments | Instant (swap back) | Low | Critical services, zero-downtime required |
| **Canary** | Route small % of traffic to new version, gradually increase | Fast (route to old) | Low | High-traffic services, data-driven teams |
| **Recreate** | Stop old, start new | Slow (redeploy old) | High | Dev/staging, stateful apps with breaking changes |
| **Feature Flags** | Deploy code dark, enable via flag | Instant (toggle off) | Very Low | Gradual rollout, A/B testing |
| **GitOps** | Git commit triggers reconciliation (ArgoCD, Flux) | Fast (revert commit) | Low | Kubernetes-native, declarative infra |

### Step 4: Configure Rollback Procedures

Define automated and manual rollback:

**Automated Rollback Triggers:**
- Error rate exceeds baseline by > 5% for 2 consecutive minutes
- P99 latency exceeds SLO threshold for 3 consecutive minutes
- Health check failures on > 10% of instances
- Deployment timeout exceeded (no healthy instances in N minutes)

**Manual Rollback Procedure:**
1. Identify the issue (check dashboards, logs, alerts)
2. Decide: rollback or roll-forward (is a fix faster?)
3. Execute rollback (revert deployment, swap traffic, toggle flag)
4. Verify rollback success (health checks, metrics, smoke tests)
5. Communicate status to stakeholders
6. Create post-incident ticket for root cause analysis

### Step 5: Integrate Security Scanning

| Scan Type | Tool Examples | When to Run | Action on Finding |
|-----------|--------------|-------------|-------------------|
| **SAST** (Static Application Security Testing) | Semgrep, SonarQube, CodeQL | Every PR | Block merge on Critical/High |
| **SCA** (Software Composition Analysis) | Snyk, Dependabot, Trivy | Every build | Block on Critical CVEs |
| **Container Scanning** | Trivy, Grype, Anchore | After image build | Block deploy on Critical |
| **Secrets Detection** | Gitleaks, TruffleHog, detect-secrets | Every commit (pre-commit + CI) | Block immediately |
| **DAST** (Dynamic Application Security Testing) | OWASP ZAP, Burp Suite | Post-deploy to staging | Warn, create ticket |
| **IaC Scanning** | Checkov, tfsec, KICS | Every PR with infra changes | Block on High severity |
| **License Compliance** | FOSSA, Snyk License | On dependency changes | Warn on copyleft in proprietary code |

### Step 6: Optimize Pipeline Performance

**Caching Strategy:**
- Cache dependency installation (node_modules, .venv, .m2)
- Cache build artifacts between stages
- Cache Docker layers (use BuildKit, multi-stage builds)
- Cache test fixtures and compiled test assets

**Parallelization:**
- Run lint, unit tests, and security scans in parallel
- Split test suites across multiple runners (test sharding)
- Build multi-arch images in parallel

**Skip Conditions:**
- Skip integration tests for docs-only changes
- Skip build for changes that only affect tests
- Use path filters to run only relevant pipeline stages in monorepos

## Output Format

Present the pipeline design as:

```
## Pipeline Summary
- **Application:** [name and type]
- **CI/CD Platform:** [platform]
- **Deployment Strategy:** [strategy]
- **Target Environment:** [environment]
- **Estimated Total Duration:** [time]

## Pipeline Stages
[Visual stage diagram or ordered list with details]

## Deployment Strategy Details
[Strategy specifics, traffic splitting, rollback triggers]

## Security Gates
[Which scans, where they run, pass/fail criteria]

## Rollback Procedure
[Step-by-step rollback instructions]

## Performance Optimizations
[Caching, parallelization, skip conditions]

## Recommendations
[Prioritized list of improvements]
```

## Quality Checklist

Before finalizing, verify:
- [ ] Every stage has a clear failure action (fail fast, warn, or rollback)
- [ ] Rollback procedure is documented and tested
- [ ] Security scanning covers dependencies, containers, secrets, and IaC
- [ ] Pipeline can complete in under 15 minutes for the fast path
- [ ] Caching is configured for dependencies and build artifacts
- [ ] Secrets are injected from a vault, never hardcoded in pipeline config
- [ ] Notifications are configured for failures and successful deploys
- [ ] Branch protection rules enforce pipeline passage before merge
- [ ] Artifact retention policy is defined (how long to keep old images/builds)
- [ ] Pipeline config is version-controlled alongside application code

## Edge Cases

- **Monorepo Pipelines:** Use path-based triggers to only build/test affected services. Consider tools like Turborepo, Nx, or Bazel for dependency-aware builds.
- **Database Migrations in CI:** Run migrations in a separate stage. Ensure they are backward-compatible (expand-contract pattern). Never run destructive migrations automatically.
- **Flaky Tests:** Quarantine flaky tests into a separate non-blocking job. Track flakiness rate. Auto-retry with caution (max 1 retry, alert on repeated flakes).
- **Long-Running Integration Tests:** Move to a separate pipeline triggered after merge, not on every PR. Use parallelization and test selection to keep PR pipelines fast.
- **Multi-Environment Promotion:** Use a promotion model (dev -> staging -> production) with manual approval gates for production. Never auto-deploy to production without verification in a lower environment.
- **Pipeline-as-Code Drift:** Ensure pipeline definitions are reviewed in PRs like application code. Use reusable workflow templates to avoid duplication across repos.
- **Secrets Rotation During Deploy:** Ensure deployments can handle mid-deploy secret rotation. Use short-lived tokens where possible.
