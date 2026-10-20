---
name: ci-cd-standards
description: CI/CD pipeline standards — pipeline stages, gates, environment promotion, rollback triggers, secret management
globs: ["**/*.yml", "**/*.yaml", "**/Dockerfile"]
alwaysApply: false
---

# CI/CD Pipeline Standards

Automated quality gates ensure only good code reaches production.

## Pipeline Stages (Required)

Every merge to main must pass:

```
┌──────────────┐
│  Lint Check  │  (2 min) — Code style, no syntax errors
└──────┬───────┘
       │ ✅ Pass
       ↓
┌──────────────┐
│  Unit Tests  │  (5 min) — Fast, isolated tests
└──────┬───────┘
       │ ✅ All pass
       ↓
┌──────────────────┐
│  Build/Compile   │  (3 min) — Code compiles, no errors
└──────┬───────────┘
       │ ✅ Build succeeds
       ↓
┌──────────────────┐
│ Integration Tests│  (10 min) — Tests that touch DB, external APIs
└──────┬───────────┘
       │ ✅ All pass
       ↓
┌──────────────────┐
│  Security Scan   │  (3 min) — OWASP, dependency vulns, secrets
└──────┬───────────┘
       │ ✅ No critical vulns
       ↓
┌──────────────────┐
│  Coverage Check  │  (1 min) — Code coverage >= 80%
└──────┬───────────┘
       │ ✅ Pass
       ↓
┌──────────────────┐
│ Deploy to Staging│  (2 min) — Auto-deploy for testing
└──────┬───────────┘
       │ ✅ Smoke tests pass
       ↓
┌──────────────────┐
│    Ready to      │
│    Prod Deploy   │  (Manual approval required)
└──────────────────┘
```

---

## Gate Requirements (Hard Blocks)

**ALWAYS block merge if:**
- [ ] Linter fails (code style issues)
- [ ] Any test fails
- [ ] Code coverage decreases
- [ ] Security scanner finds Critical/High
- [ ] Compilation fails
- [ ] Unauthorized secrets detected

**Never skip gates** (not even for "quick fixes").

### Gate Configuration

```yaml
# Example: GitHub Actions
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm run lint
      - run: npm run format:check  # Ensure formatted

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm install
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v2  # Report coverage
        with:
          fail_ci_if_error: true  # Fail if coverage decreases

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]  # Wait for lint & test
    steps:
      - uses: actions/checkout@v2
      - run: npm run build
      - uses: actions/upload-artifact@v2  # Save build output

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: npm audit --production  # Check dependencies
      - run: npm run security-scan    # Custom scan

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test, build, security]
    if: github.ref == 'refs/heads/main'  # Only on main
    steps:
      - name: Deploy to Staging
        run: ./scripts/deploy-staging.sh
      - name: Smoke Tests
        run: npm run smoke-tests:staging

  deploy-prod:
    runs-on: ubuntu-latest
    needs: deploy-staging
    if: github.ref == 'refs/heads/main'
    environment: production  # Requires manual approval
    steps:
      - name: Deploy to Production
        run: ./scripts/deploy-prod.sh
      - name: Health Checks
        run: ./scripts/healthchecks-prod.sh
```

---

## Environment Promotion

**Development** → (auto) → **Staging** → (manual) → **Production**

| Stage | Auto? | Duration | Smoke Test | Rollback |
|-------|-------|----------|-----------|----------|
| **DEV** | ✅ Yes | On merge | None | Instant (dev) |
| **STAGING** | ✅ Yes | 5 min | Yes (2 min) | < 5 min |
| **PROD** | 🟡 Manual | 10 min | Yes (3 min) | < 10 min |

---

## Secrets Management

**ALWAYS**:
- Store secrets in CI/CD secrets, not in code
- Rotate secrets quarterly
- Use different secrets per environment
- Audit access to production secrets
- Never log secrets (redact in logs)

**NEVER**:
- Hardcode secrets in code
- Commit .env files to git
- Use same secret for dev/staging/prod
- Share secrets in Slack/email
- Log API keys or passwords

### Secret Injection Pattern

```yaml
# ✅ GOOD: Secrets from CI/CD environment
env:
  DATABASE_URL: ${{ secrets.DB_CONNECTION_STRING }}
  API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
  JWT_SECRET: ${{ secrets.JWT_SECRET }}

# ❌ BAD: Hardcoded in workflow
env:
  DATABASE_URL: "Server=prod.example.com;Password=SuperSecret123!"
```

---

## Rollback Triggers

**Auto-Rollback if:**
- Error rate spikes > 5% above baseline
- Response time > 2x baseline
- CPU/memory > 90% for 5 minutes
- Database connections pooled out
- Key service unreachable

**Manual Rollback if:**
- Critical security vulnerability discovered
- Data corruption detected
- Major feature broken
- External service dependency down

### Rollback Procedure

```bash
# 1. Declare incident
echo "INCIDENT: Rollback initiated for v2.3.4"

# 2. Check current version
kubectl get deployment api -o yaml | grep image

# 3. Rollback to previous version
kubectl rollout undo deployment/api

# 4. Verify health
./scripts/healthchecks-prod.sh

# 5. Post-mortem
# Schedule review within 24 hours
```

---

## Deployment Checklist

Before deploying to production:

- [ ] All tests passing (CI green)
- [ ] Code reviewed and approved (2 approvals)
- [ ] CHANGELOG.md updated
- [ ] Release notes prepared
- [ ] Database migrations tested in staging
- [ ] Secrets rotated (if needed)
- [ ] Health checks configured
- [ ] Rollback plan documented
- [ ] On-call team notified
- [ ] Monitoring/alerts configured

---

## Post-Deployment Validation

After every production deploy:

```
5 min: Smoke tests pass
10 min: Error rate normal, no spike
15 min: Response times normal, no slow endpoint
30 min: Database connections stable
1 hour: No unusual logs/errors
3 hours: User-facing functionality confirmed (spot checks)
```

---

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Tests fail** | CI fails, blocks merge | Fix code, retest |
| **Build fails** | CI fails, blocks merge | Debug compilation error |
| **Deploy to staging fails** | CI fails, notifies team | Check logs, retry |
| **Prod deploy fails** | CI fails, auto-rollback | Investigate, retry tomorrow |
| **Error rate spikes** | Monitoring alert | Auto-rollback, investigate |
| **Performance degrades** | APM alert | Auto-rollback, profile |

---

## Monitoring & Alerts

**Monitor these metrics:**
- Error rate (target: < 0.1%)
- Response time P95 (target: < 200ms)
- Database query time (target: < 100ms)
- CPU usage (target: < 70%)
- Memory usage (target: < 80%)
- Disk usage (target: < 80%)

**Alert on:**
- Error rate > 1% for 5 minutes
- Response time P95 > 500ms
- CPU > 90% for 5 minutes
- Disk > 95%
- Service unreachable

---

## Release Notes Template

```markdown
# Release v2.3.5 (2026-04-09)

## New Features
- Automatic password reset flow (#342)
- Dark mode support for dashboard (#451)

## Bug Fixes
- Fixed N+1 query in user list (perf)
- Fixed XSS in comment editor (security)

## Breaking Changes
- Removed deprecated /api/v1/old-endpoint
  Migration: Use /api/v2/new-endpoint instead

## Database Migrations
Run: `npm run migrate:prod`
Rollback: `npm run rollback:prod`

## Security Updates
- Updated dependencies (npm audit clean)
- Rotated API keys

## Testing
All tests passing. Coverage: 92%
Staging validation: ✅ Passed
Production validation: ✅ All healthy

## Deployment
Deployed: 2026-04-09 14:32 UTC
Deployed by: @alice
Rollback: `git revert abc123`
```

---

## Continuous Deployment Decision Tree

```
Code pushed to main
  ↓
Run CI pipeline (lint, test, build, security, etc.)
  ↓
Pass? ── NO ──→ Notify author ── Author fixes ──→ Re-run
  │
  YES
  ↓
Deploy to staging (auto)
  ↓
Smoke tests pass?
  ↓
YES ── Ready for production
  ↓
Manual approval required
  │ (Required for production)
  ↓
Deploy to production (manual)
  ↓
Post-deploy validation (auto)
  ↓
All good? ── NO ──→ Auto-rollback
  │
  YES
  ↓
✅ Deployment complete
   Monitor for issues (1 hour)
```

---

## Pipeline Checklist

- [ ] Lint stage: code style enforced
- [ ] Test stage: all tests required to pass
- [ ] Build stage: compilation required
- [ ] Security stage: no critical vulns
- [ ] Coverage check: >= 80% required
- [ ] Staging deploy: automatic
- [ ] Production deploy: manual approval
- [ ] Health checks: post-deploy validation
- [ ] Monitoring: alerts configured
- [ ] Rollback: documented and tested

---

## Summary

Good CI/CD:
1. **Automates quality** (catch issues early)
2. **Blocks bad code** (gates are non-negotiable)
3. **Promotes safely** (dev → staging → prod)
4. **Rolls back quickly** (no manual steps)
5. **Monitors relentlessly** (know when things break)

This turns deployment from a scary manual process into an automated, trustworthy, reversible operation.
