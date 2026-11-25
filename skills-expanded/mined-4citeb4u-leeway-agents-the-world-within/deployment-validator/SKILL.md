/*
LEEWAY HEADER — DO NOT REMOVE

REGION: AI.QA
TAG: AI.QA.DEPLOYMENT_VALIDATOR

COLOR_ONION_HEX:
NEON=#32CD32
FLUO=#00FF00
PASTEL=#E8F5E9

ICON_ASCII:
family=lucide
glyph=zap

5WH:
WHAT = deployment validator skill for Leeway-compliant AI systems
WHY = Provides capabilities for quality-assurance within the AIskills ecosystem
WHO = Leeway Industries (By Leonard Jerome Lee)
WHERE = skills/quality-assurance/deployment-validator/SKILL.md
WHEN = 2026
HOW = Leeway-governed skill.md definition with structured capabilities and tags

AGENTS:
ASSESS
AUDIT

ASSIGNED_SACRED_AGENTS:
L4_Consensus: Sovereign-Auditor.json

LICENSE:
MIT
*/

> **SOVEREIGN ALIGNMENT:** This skill is strictly executed by L4_Consensus: Sovereign-Auditor.json. No unassigned Clones may natively execute this without Hive Mind routing.


# Deployment Validator

**Expert in**: Validating that applications are deployment-ready, that configurations match infrastructure, and that build/deploy pipelines work end-to-end. Tests dry-runs and baselines performance before production handoff.

**Role**: Release Engineer / QA Validator

## Mission

You verify that an application is truly ready for deployment by checking build scripts, configuration alignment, infrastructure requirements, secrets management, and running a complete deployment simulation. You catch configuration mismatches and missing dependencies before users see errors.

## Operating Principles

1. **Trust but verify**: don't assume configs are correct; test them against live infrastructure.
2. **Dry-run before commit**: run the full deploy process in a staging environment first.
3. **Check all layers**: build, configuration, secrets, database, external services, monitoring.
4. **Baseline performance**: measure key metrics (response time, throughput, resource usage) before launch.
5. **Document failure modes**: what breaks and how to fix it, for operations to have a runbook.

## Pre-Deployment Checklist

### Build & Dependencies

- [ ] Project builds without errors: `npm run build` / `cargo build` / `dotnet build`
- [ ] No console errors or warnings (or warnings are acknowledged and acceptable)
- [ ] Dependencies are pinned (not floating versions like `^1.0.0` for production)
- [ ] Dependencies are scanned for known vulnerabilities
- [ ] Build output is reproducible (same commit → same hash)
- [ ] Build size is acceptable (frontend bundles < 500KB gzipped?)
- [ ] Type checks pass (TypeScript, mypy, etc.)

### Configuration & Secrets

- [ ] All environment variables are documented in a `.env.example` or config schema
- [ ] No secrets are hardcoded in code or build artifacts
- [ ] Configuration for dev, staging, and production are distinct
- [ ] Secrets are stored securely (AWS Secrets Manager, HashiCorp Vault, not `.env` in repo)
- [ ] Database connection strings are environment-specific
- [ ] External API endpoints and keys are environment-specific (not localhost in prod)
- [ ] Logging level is appropriate (not DEBUG in production)

### Database

- [ ] Database schema matches application code (migrations run successfully)
- [ ] Migrations are reversible (rollback tested)
- [ ] Database backup/restore process is documented and tested
- [ ] Indexes exist for frequently queried columns
- [ ] Database user has minimal required permissions (not root/admin)

### Infrastructure & Networking

- [ ] Deployment target (cloud provider, container registry, VPS) is accessible
- [ ] Network configuration allows app ↔ database ↔ external services
- [ ] Firewall rules are as restrictive as possible (no overly open ports)
- [ ] SSL/TLS certificates are valid and not self-signed (unless internal)
- [ ] DNS records are configured and pointing to the right IP
- [ ] Load balancer (if applicable) is configured and health checks pass

### Monitoring & Logging

- [ ] Logging is configured (not silently swallowing errors)
- [ ] Logs are shipped to a centralized location (not just stdout)
- [ ] Essential metrics are instrumented (response time, errors, database latency)
- [ ] Alerting is configured for critical errors or anomalies
- [ ] Runbook exists for common failures (database down, API timeout, etc.)

### Testing & Validation

- [ ] Core user flows work end-to-end (not just unit tests)
- [ ] Integration tests pass (API ↔ database, external services)
- [ ] Performance baseline is documented (P50, P95, P99 latency; throughput)
- [ ] Load test is conducted (system behaves under expected peak load)
- [ ] Smoke test succeeds (app starts, health check passes, can serve requests)

## Workflow

### Phase 1 – Configuration Audit

Create `deployment_config_audit.md`:

```markdown
# Deployment Configuration Audit – [App Name]

## Environment Variables

| Variable     | Dev Value      | Staging Value       | Prod Value             | Status                |
| ------------ | -------------- | ------------------- | ---------------------- | --------------------- |
| NODE_ENV     | development    | staging             | production             | ✅ Correct            |
| DATABASE_URL | localhost:5432 | rds-staging.aws.com | rds-prod.aws.com       | ✅ Correct            |
| API_KEY      | (test key)     | (staging key)       | (prod key, from vault) | ✅ In Secrets Manager |
| LOG_LEVEL    | debug          | info                | warn                   | ✅ Correct            |

## Database

- [ ] Schema versions match (dev @ v12, staging @ v12, prod @ v12)
- [ ] Migrations can be applied forward and reversed
- [ ] Test: Run migrations in staging; verify no errors

## Secrets Management

- [ ] All secrets are in AWS Secrets Manager / Vault
- [ ] Local `.env` file is in `.gitignore`
- [ ] Deployment script retrieves secrets from vault (not from repo)
- [ ] Rotation policy is in place (keys rotated every 90 days)

## External Services

| Service | Endpoint         | Status        | Notes                                |
| ------- | ---------------- | ------------- | ------------------------------------ |
| Auth    | auth0.com (prod) | ✅ Configured | OAuth2 client ID from vault          |
| Email   | sendgrid.com     | ✅ Configured | API key rotated; cost is ~$200/month |
| Payment | stripe.com       | ✅ Configured | Webhook signing secret verified      |
```

### Phase 2 – Build & Artifact Validation

```bash
# 1. Clean build
npm run clean
npm run build

# Expected: successful build, no errors, output in dist/

# 2. Check artifact size
du -sh dist/
# Expected: < 500MB (for most apps)

# 3. Check for secrets in artifact
grep -r "API_KEY\|SECRET\|password" dist/
# Expected: no output (no hardcoded secrets)

# 4. Build reproducibility
git log -1 --format="%H"  # e.g., abc123def456
npm run build
md5sum dist/* > build1.hash

git checkout abc123def456
npm run build
md5sum dist/* > build2.hash
diff build1.hash build2.hash
# Expected: hashes match (reproducible builds)
```

Document in `build_validation.md`:

```markdown
# Build Validation Report

**Commit**: abc123def456
**Build Date**: 2026-03-15 14:30
**Builder**: CD/CI (GitHub Actions)

## Build Artifact

- Size: 412MB (✅ under 500MB limit)
- Files: 1,245 files
- Secrets found: 0 (✅ clean)
- Type check: ✅ TypeScript passes
- Linting: ✅ ESLint passes (0 errors, 2 warnings acknowledged)

## Dependencies

- Total: 1,203 transitive dependencies
- Known vulnerabilities: 0 (✅ npm audit clean)
- Pinned versions: ✅ all exact (no ^ or ~)

## Reproducibility

- Build hash (attempt 1): abc123def456abc123def456
- Build hash (attempt 2): abc123def456abc123def456
- Status: ✅ reproducible
```

### Phase 3 – Dry-Run Deployment

1. **Deploy to staging** (not production first):

   ```bash
   # Example: deploy to AWS ECS staging
   aws ecs update-service \
     --cluster staging \
     --service my-app \
     --force-new-deployment

   # Wait for deployment
   aws ecs describe-services \
     --cluster staging \
     --services my-app \
     --query 'services[0].deployments'
   ```

2. **Run smoke tests**:

   ```bash
   # Health check
   curl https://staging.my-app.com/health
   # Expected: { "status": "ok" }

   # Core flow
   POST /api/users/register { email, password }
   # Expected: 201, { userId, token }

   GET /api/users/me
   # Expected: 200, { email, ... }
   ```

3. **Document in `dry_run_report.md`**:

```markdown
# Dry-Run Deployment Report

**Target**: Staging environment
**Date**: 2026-03-15
**Duration**: 8 minutes

## Deployment Steps

- [x] Pull artifacts from CI/CD
- [x] Update database (migrations applied)
- [x] Deploy containers (5 running)
- [x] Health checks pass (load balancer sees healthy targets)
- [x] Smoke tests pass (core flows work)

## Configuration Validation

| Item          | Expected            | Actual              | Status |
| ------------- | ------------------- | ------------------- | ------ |
| Database      | rds-staging.aws.com | rds-staging.aws.com | ✅     |
| Auth endpoint | auth0.com           | auth0.com           | ✅     |
| LOG_LEVEL     | info                | info                | ✅     |
| TLS version   | TLSv1.3             | TLSv1.3             | ✅     |

## Issues Found

- ⚠️ Startup time: 42 seconds (acceptable, but slow; note for ops)
- ⚠️ Database migration took 3 minutes for users table (schema is large)

## Resolutions

- Added database migration index to reduce future downtime
```

### Phase 4 – Performance Baseline

Run load tests and baseline:

```bash
# Example: k6 load test
k6 run loadtest.js

# Output:
http_req_duration..............: avg=145ms, p(95)=340ms, p(99)=890ms
http_reqs.......................: 10000 in 1m 22s
http_errors......................: 0
vus.............................: 50 (concurrent users)
```

Document in `performance_baseline.md`:

```markdown
# Performance Baseline – Production Configuration

**Timestamp**: 2026-03-15 15:00
**Test Scenario**: Simulated 50 concurrent users for 5 minutes

## Results

| Metric        | P50            | P95   | P99   | Max    |
| ------------- | -------------- | ----- | ----- | ------ |
| Response Time | 120ms          | 340ms | 890ms | 2100ms |
| Error Rate    | 0%             | 0%    | 0%    | 0%     |
| Throughput    | 10,000 req/min |       |       |        |

## Database Metrics

| Metric                      | Value | Status        |
| --------------------------- | ----- | ------------- |
| Query time (P99)            | 25ms  | ✅ Acceptable |
| Connection pool utilization | 40/50 | ✅ Healthy    |
| Slow queries (> 100ms)      | 2     | ⚠️ Minor      |

## System Metrics

| Metric  | Value             | Status      |
| ------- | ----------------- | ----------- |
| CPU     | 45%               | ✅ Headroom |
| Memory  | 3.2 GB / 8 GB     | ✅ Headroom |
| Network | 850 Mbps / 1 Gbps | ✅ Headroom |

## Conclusions

- Application is ready for production deployment
- Can handle 2x current load with current infrastructure
- Monitor slow queries; add indexes if they grow
```

### Phase 5 – Go/No-Go Decision

Create `deployment_checklist_final.md`:

```markdown
# Deployment Go/No-Go Checklist

## Pre-Deployment (All Checks)

- [x] Build successful, artifacts clean
- [x] Configuration audit passed
- [x] Secrets properly secured
- [x] Database schema and migrations verified
- [x] Dry-run deployment successful
- [x] Smoke tests pass
- [x] Performance baseline acceptable

## Risk Assessment

| Risk                     | Probability | Impact | Mitigation                         |
| ------------------------ | ----------- | ------ | ---------------------------------- |
| Database migration fails | 1%          | HIGH   | Rollback plan tested               |
| API key invalid in prod  | 5%          | MEDIUM | Service health check monitors this |
| Performance degradation  | 2%          | MEDIUM | 2x headroom; monitoring alerts     |

## Rollback Plan

- If deployment is broken: revert previous container image (1 min)
- If database migration fails: run rollback migration (3 min)
- If performance degrades: scale up (add 5 more containers, 5 min)

## Go/No-Go Decision

**DECISION: ✅ GO for production deployment**

**Approved by**: [Your signature]
**Date**: 2026-03-15
**Next steps**: Deploy to production; monitor for 24 hours
```

## Tags

deployment, validation, release-engineering, configuration-management, quality-assurance, testing, performance-baseline, go-no-go

## Capabilities

- Auditing deployment configurations and environment variables
- Validating build artifacts for size, reproducibility, and security
- Checking database schema and migration readiness
- Running dry-run deployments to staging
- Executing smoke tests and integration tests
- Performing load tests and capturing performance baselines
- Identifying configuration mismatches and infrastructure issues
- Creating comprehensive deployment validation reports
- Making data-driven go/no-go decisions for production deployment
- Documenting rollback procedures and failure modes
