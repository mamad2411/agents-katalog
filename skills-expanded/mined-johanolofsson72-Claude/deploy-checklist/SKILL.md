---
name: deploy-checklist
description: Pre-deployment verification checklist for Docker Swarm deployments to Azure. Use before deploying to production. Trigger words include deploy, release, production, go live.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Deploy Checklist

Pre-deployment verification for Docker Swarm on Azure (live4.se).

## Verification steps

Run each step and report pass/fail:

### 1. Build verification
```bash
dotnet build --configuration Release
```

### 2. Test verification
```bash
dotnet test --configuration Release
```

### 3. Git status
- All changes committed?
- On correct branch?
- Up to date with remote?

### 4. Configuration check
- No secrets in `appsettings*.json` or the image (`ENV`/`ARG`); committed config holds placeholders only
- Production secrets (connection strings included) are Swarm secrets mounted as files, not the service `environment:` (`.claude/docs/security.md` § Secrets)
- HTTPS enforced
- CORS configured correctly

### 5. Docker verification
```bash
docker build -t app:test .
```

### 6. Migration check
- Any pending EF Core migrations?
- Migration reviewed (Up and Down methods)?

### 7. Stress testing (MANDATORY)

Run stress tests against both API and frontend. For full details, thresholds, and script templates, read `${CLAUDE_SKILL_DIR}/../../docs/stress-testing.md`.

**API** (if the project has API endpoints):
```bash
k6 run --env BASE_URL=http://localhost:5000 tests/stress/stress-api.js
```
- p95 response time < 500ms
- Error rate < 5%
- Sustained throughput > 50 rps

**Frontend**:
```bash
npx @lhci/cli@0.14.x autorun --collect.url=http://localhost:5000
```
- LCP < 2.5s, FID < 100ms, CLS < 0.1, TTFB < 800ms
- Lighthouse score > 70

If stress tests are not set up yet, create them from the templates in `.claude/docs/stress-testing.md` BEFORE proceeding with the deploy.

## Report

| Step | Status | Notes |
|------|--------|-------|
| Build | PASS/FAIL | |
| Tests | PASS/FAIL | X passed, Y failed |
| Git | PASS/FAIL | |
| Config | PASS/FAIL | |
| Docker | PASS/FAIL | |
| Migrations | PASS/FAIL/N/A | |
| Stress (API) | PASS/FAIL/N/A | p95: Xms, error rate: X%, rps: X |
| Stress (Frontend) | PASS/FAIL | LCP: Xs, Lighthouse: X/100 |

**Recommendation**: READY TO DEPLOY / NOT READY (with blocking issues)

For deployment commands and infrastructure details, read `${CLAUDE_SKILL_DIR}/../../docs/deployment.md`.
