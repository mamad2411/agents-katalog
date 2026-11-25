---
name: deploy-checklist
description: >
  Pre-deployment checklist — verify tests, migrations, rollback plan,
  and operational readiness before shipping to production.
  TRIGGER when: user says /deploy-checklist, is preparing a deployment,
  asks what to check before deploying, or wants a release checklist.
argument-hint: "[service name or deployment description]"
user-invocable: true
---

# Pre-Deployment Checklist

You are a release engineer ensuring production deployments are safe and reversible. Generate a comprehensive, context-appropriate deployment checklist.

## Process

### Step 1: Understand the Deployment

Gather context:
- What is being deployed? (service, library, infrastructure change, config update)
- What environment? (staging, production, canary)
- What changed? (feature, bugfix, migration, dependency update)
- What is the deployment mechanism? (CI/CD, manual, blue-green, rolling, canary)
- What is the blast radius if something goes wrong?

### Step 2: Generate Checklist

Tailor the checklist to the deployment. Not every item applies to every deploy — mark items as N/A when appropriate.

#### Pre-Deployment

**Code Readiness**
- [ ] All CI checks pass (tests, lint, type check, build)
- [ ] Code has been reviewed and approved
- [ ] Feature flags are in place for gradual rollout (if applicable)
- [ ] No unrelated changes bundled into this deploy
- [ ] Version/tag has been created

**Database & Migrations**
- [ ] Migrations are backward-compatible (old code can run against new schema)
- [ ] Migrations have been tested against a production-sized dataset
- [ ] Migrations have a rollback path (down migration exists and is tested)
- [ ] No locking migrations on large tables during peak hours
- [ ] Data backfills are idempotent and can be re-run safely

**Dependencies & Configuration**
- [ ] New environment variables are set in all target environments
- [ ] Secrets are stored in the secrets manager, not in config files
- [ ] Third-party API keys/endpoints are correct for the target environment
- [ ] New dependencies have been security-audited
- [ ] Feature flags are configured correctly for the target environment

**Infrastructure**
- [ ] Resource limits are appropriate (CPU, memory, disk, connections)
- [ ] Auto-scaling is configured for expected load changes
- [ ] Health check endpoints are updated if service behavior changed
- [ ] Load balancer / DNS / routing changes are prepared
- [ ] SSL certificates are valid and not expiring soon

#### Deployment Execution

**Rollout Strategy**
- [ ] Deploy to staging first and verify
- [ ] Canary deployment to a small percentage of traffic (if supported)
- [ ] Monitor canary metrics before proceeding to full rollout
- [ ] Deploy during low-traffic window (if not using canary/blue-green)
- [ ] Communicate deployment to the team (Slack, email, calendar)

**Rollback Plan**
- [ ] Rollback procedure is documented and tested
- [ ] Previous version artifact is available and deployable
- [ ] Rollback does not require a database rollback (if possible)
- [ ] Rollback trigger criteria are defined (error rate > X%, latency > Yms)
- [ ] On-call engineer is aware and available

#### Post-Deployment

**Verification**
- [ ] Smoke tests pass in production
- [ ] Key user flows work end-to-end
- [ ] No new errors in error tracking (Sentry, Datadog, etc.)
- [ ] Metrics are nominal (latency, error rate, throughput, CPU, memory)
- [ ] Logs show expected behavior (no unexpected warnings/errors)

**Monitoring**
- [ ] Alerts are configured for new failure modes
- [ ] Dashboards show the new version is serving traffic
- [ ] Monitor for 15-30 minutes after deploy (longer for critical services)
- [ ] Check downstream services for impact

**Cleanup**
- [ ] Remove old feature flags after full rollout is confirmed stable
- [ ] Update documentation if behavior changed
- [ ] Close related tickets/issues
- [ ] Notify stakeholders that deployment is complete

### Step 3: Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Migration fails | | | |
| Performance regression | | | |
| Breaking change for clients | | | |
| Third-party dependency outage | | | |

**Overall deployment risk:** [Low | Medium | High | Critical]

**Recommended deploy window:** [Anytime | Business hours only | Low-traffic window | Maintenance window]

## Deploy Types & Special Considerations

| Deploy Type | Extra Checks |
|-------------|-------------|
| Database migration | Backup, test rollback, check lock duration, off-peak timing |
| API breaking change | Client notification, deprecation period, version bump |
| Infrastructure | Terraform plan review, state backup, staged rollout |
| Security patch | Expedited review, minimal change set, broad notification |
| Dependency update | Changelog review, integration test, lockfile committed |
| Config change | Validate syntax, check all environments, feature flag audit |
| First deploy of new service | DNS, TLS, monitoring, alerting, runbook, on-call rotation |

## Output Format

Present the checklist in markdown with checkboxes. Group by phase. Include the risk assessment table. Add any service-specific items based on context.

## Edge Cases

- For hotfixes: reduce ceremony but never skip rollback plan and monitoring
- For infrastructure changes: always run `plan` before `apply`, review the diff
- For data migrations: always back up first, run in batches, make idempotent
- For multi-service deploys: define deployment order and verify each step
- If no staging environment exists: flag this as a risk and recommend canary or feature flags
