---
name: pipeline-quality-gates
description: >-
  Standard quality gates and best practices for CI/CD pipelines (Azure Pipelines
  and GitHub Actions). Enforces reproducibility, security, observability, and
  operational excellence before pipeline code merges.
when-to-use: >-
  Invoke when designing or reviewing pipeline YAML (azure-pipelines.yml,
  .github/workflows/*.yml) to enforce org standards for testing, deployment
  gates, secret handling, and notifications.
categories:
  - ci-cd
  - devops
  - quality-assurance
  - security
---

# Pipeline Quality Gates

Standard set of quality checks for Azure Pipelines and GitHub Actions pipelines. Use this to ensure pipelines are safe, observable, and maintainable.

## Pre-Flight Checks (Before Merge)

Every pipeline should pass these fundamental checks:

### 1. Secret & Credential Handling

- [ ] **No hardcoded secrets**
  - No passwords, keys, tokens in YAML
  - No secrets in logs (use masking)
  - Secrets injected via variables, not environment

- [ ] **Proper secret source**
  - Azure Pipelines: Using `$(secretVariable)` from variable groups
  - Azure Pipelines: Key Vault tasks for dynamic secret retrieval
  - GitHub Actions: Using `secrets.SECRET_NAME` context
  - GitHub Actions: Secrets not printed to stdout/logs

- [ ] **Secret rotation policy defined**
  - Document rotation interval in PR description
  - Service account credentials reviewed quarterly

### 2. Permissions & Access Control

- [ ] **Azure Pipelines**
  - Service connection permissions follow least-privilege
  - Pipeline can only access resources it needs
  - Queue restrictions configured for sensitive pipelines
  - Approval gates required for production deployments

- [ ] **GitHub Actions**
  - Explicit `permissions` set at workflow level
  - `permissions: {}` as baseline, only grant needed scopes
  - `id-token: write` only for OIDC deployments
  - No overly broad token permissions

### 3. Trigger & Filter Sanity

- [ ] **Correct branch filters**
  - `trigger` branches appropriate for production pipelines
  - `pr` branches appropriate for PR pipelines
  - Path filters prevent unnecessary runs

- [ ] **Scheduled triggers**
  - Cron schedules UTC (no timezone surprises)
  - Schedule not too aggressive (don't overload infrastructure)
  - Off-hours scheduling considered for long-running jobs

- [ ] **Manual trigger (`workflow_dispatch`)**
  - Typed inputs (not free-form strings)
  - Descriptions clear for each input
  - Defaults safe (don't accidentally deploy to prod)

---

## Testing & Quality Gates

### Build Job Standards

- [ ] **Compilation/Linting**
  - Code compiles without warnings (treat warnings as errors for critical paths)
  - Linting passes (configured linters enforced)
  - Type checking passes (TypeScript, Python type hints, etc.)

- [ ] **Unit Tests**
  - Tests run on every code change
  - Test results published to pipeline UI
  - Test coverage metrics tracked (target ≥80%)
  - Failing tests block merge

- [ ] **Security Scanning**
  - Dependency scanning (SAST for dependencies)
  - Code scanning (CodeQL, SonarQube, or equivalent)
  - Secrets scanning enabled
  - Container image scanning if applicable

- [ ] **Artifact Management**
  - Build artifacts clearly named
  - Artifact retention policy defined
  - No oversized artifacts (>500MB unless justified)

### Test Job Standards

- [ ] **Integration Tests**
  - Tests run against real/test environment
  - Database seeded properly
  - Test data cleaned up after run
  - Flaky test tracking documented

- [ ] **Test Result Visibility**
  - Test results published (Azure test results, GitHub test report)
  - Failed tests surface in PR comments
  - Coverage report published
  - Performance regression detected

- [ ] **Performance Testing** (for user-facing services)
  - Baseline performance documented
  - Load tests run on changes to critical paths
  - Performance regression gates deployment

---

## Deployment Standards

### Pre-Deployment Gates

- [ ] **Manual Approvals**
  - Production deployments require explicit approval
  - Approval from code reviewer (CODEOWNERS check)
  - Approval timeout set (max wait time enforced)

- [ ] **Deployment Environment Protection** (GitHub Actions)
  - Production environments have protection rules
  - Required reviewers configured
  - Allowed deployment branches restricted
  - Wait timer (e.g., 24 hours for rollback window)

- [ ] **Policy as Code**
  - No deployment to production during business hours (optional)
  - Deployment only from specific branches (main/release)
  - Rollback SOP documented

### Deployment Job Standards

- [ ] **Deployment Safety**
  - Idempotent deployments (safe to re-run)
  - Automatic rollback on failed health checks
  - Blue-green or canary deployments for stateful services
  - Infrastructure updated before application code

- [ ] **Connectivity & Secrets**
  - Cloud authentication uses OIDC (not stored credentials)
  - Database credentials injected at runtime
  - API tokens refreshed before timeout
  - Network connectivity verified before deployment

- [ ] **Health & Validation**
  - Post-deployment health checks run
  - Deployment verified with smoke tests
  - Rollback triggered on health check failure
  - Deployment logs captured for audit

### Artifact Deployment

- [ ] **Container Image Deployment**
  - Image signed/attested (supply chain security)
  - Image scanned for vulnerabilities
  - Image pulled by digest (not tag)
  - Registry authentication verified

- [ ] **Code Deployment**
  - Syntax validation before pushing code
  - Dependencies checked and compatible
  - Database migrations applied before code
  - Feature flags checked (graceful degradation)

---

## Observability & Notifications

### Pipeline Observability

- [ ] **Logging Standards**
  - Key step outputs captured
  - Deployment parameters logged
  - Environment variables (non-secrets) logged
  - Build duration tracked

- [ ] **Metrics & Alerting**
  - Pipeline run duration monitored
  - Failure rate tracked
  - Deployment frequency visible
  - Lead time for changes tracked (DORA metric)

- [ ] **Audit Trail**
  - Deployment history visible
  - Who triggered deployment captured
  - Approval chains documented
  - Rollback reasons captured

### Notifications

- [ ] **Failure Notifications**
  - Failed builds notify team in Slack/Teams
  - Notifications include build link + error summary
  - Retry link included in notification
  - Escalation on repeated failures

- [ ] **Deployment Notifications**
  - Production deployments announce in team channel
  - Deployment includes version/commit SHA
  - Rollback announcements sent immediately
  - Status updates on long deployments

- [ ] **SLA Compliance**
  - Notifications to on-call rotation on critical failure
  - Escalation timeout enforced
  - Post-incident follow-up scheduled

---

## Cost & Performance

### Pipeline Efficiency

- [ ] **Build Duration**
  - Build completes within SLA (e.g., <10 min)
  - Parallelization used where possible
  - Caching configured to reduce rebuild time
  - Unnecessary steps removed

- [ ] **Resource Allocation**
  - Agent pool/runner selection appropriate
  - No over-provisioned build infrastructure
  - Job-level timeouts prevent hung builds
  - Spot instances used where fault-tolerant

- [ ] **Artifact Cleanup**
  - Retention policy enforced
  - Old artifacts deleted automatically
  - Build logs retained per compliance requirements
  - Cost of artifacts reviewed quarterly

---

## Pipeline-Specific Standards

### Azure Pipelines

- [ ] **YAML Structure**
  - `trigger` and `pr` sections clearly defined
  - Variables organized in sections
  - Stages named descriptively
  - Jobs within stages properly scoped

- [ ] **Template Usage**
  - Common patterns extracted to templates
  - Template versioning used (pin to tag/commit)
  - Parameter names clear and documented
  - Conditional template insertion works as expected

- [ ] **Service Connections**
  - Service connections follow least-privilege
  - Used only by pipelines that need them
  - Credentials rotated periodically
  - Audit enabled

- [ ] **Variable Groups**
  - Secrets stored in variable groups (not YAML)
  - Key Vault linked for sensitive values
  - Variable naming convention consistent
  - Usage documented

### GitHub Actions

- [ ] **Workflow Structure**
  - `on` triggers clearly defined
  - Jobs scoped and named appropriately
  - Step names are descriptive
  - Concurrency groups prevent duplicate runs

- [ ] **Action Pinning**
  - All third-party actions pinned to commit SHA
  - Version comment included (e.g., `# v5.2.0`)
  - Dependabot configured for auto-updates
  - Unsafe action tags (`@main`, `@latest`) not used

- [ ] **Secrets & Environment Variables**
  - Secrets passed explicitly via `with:` or `env:`
  - Environment variables used for non-sensitive config
  - No interpolation of untrusted input in scripts
  - Secrets not printed to logs

- [ ] **Reusable Workflows**
  - Callable workflows have clear purpose
  - Inputs properly typed and documented
  - Outputs map correctly to job outputs
  - Secrets passed explicitly with `secrets: inherit`

---

## Quality Gate Decision Matrix

### Approve When:

✅ All security gates pass  
✅ Test results included  
✅ Deployment gates functional  
✅ Rollback procedure documented  
✅ Notifications configured  
✅ Artifact retention appropriate  

### Block When:

❌ Hardcoded secrets found  
❌ No test coverage for deployment logic  
❌ Production deployments lack approval gates  
❌ No rollback mechanism  
❌ Overly broad service account permissions  
❌ No failure notifications configured  

### Request Changes When:

⚠️ Secrets not properly masked  
⚠️ CODEOWNERS review required  
⚠️ Test coverage below threshold  
⚠️ Pipeline timeouts too aggressive  
⚠️ Documentation missing  
⚠️ Non-idempotent deployment detected  

---

## Approval Template

When reviewing a new/modified pipeline, use this checklist:

```
## Pipeline Review: [Pipeline Name]

### Security
- [ ] No hardcoded secrets
- [ ] Service connections follow least-privilege
- [ ] Secret masking configured

### Quality Gates
- [ ] Tests run and pass
- [ ] Deployment gates functional
- [ ] Rollback procedure clear

### Observability
- [ ] Logging captured
- [ ] Notifications configured
- [ ] Audit trail enabled

### Performance
- [ ] Build duration acceptable
- [ ] Artifact retention policy defined
- [ ] Caching configured

### Approval
Approval: [ ] Approved [ ] Changes Required
Notes: [Any concerns or improvements suggested]
```
