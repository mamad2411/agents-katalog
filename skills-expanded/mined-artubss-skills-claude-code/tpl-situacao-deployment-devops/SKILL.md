---
name: tpl-situacao-deployment-devops
description: Template do pack (situacao/10-deployment-devops.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/10-deployment-devops.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Deployment & DevOps Pipeline Setup

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/10-deployment-devops.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when setting up or improving the deployment pipeline — building CI/CD, configuring environments, managing secrets in production, setting up health checks, establishing rollback procedures, or preparing for a production go-live. The goal is deployments that are automated, observable, reversible, and boring. "Boring" is good — exciting deployments are emergencies.

## OBJECTIVES
- Achieve fully automated deployments with no manual steps
- Establish environment parity (dev/staging/production behave the same)
- Make rollbacks fast and practiced before they're needed in an emergency
- Set up monitoring BEFORE going live, not after the first incident
- Make secrets management systematic and auditable

## APPROACH RULES

1. **Every environment is cattle, not pets.** Environments must be reproducible from code and configuration. If a server needs manual steps to configure, that knowledge is lost when the server is replaced.

2. **Environment parity is non-negotiable.** Staging must mirror production in: OS, runtime versions, database engine and version, memory/CPU class (within budget). Any difference is a potential "works in staging" failure.

3. **Deploy from artifacts, not from source.** Build once, deploy the artifact. Never run `npm install` or build steps on production servers. The artifact that passes staging is the artifact deployed to production.

4. **Feature flags over long-lived branches.** If a feature is too risky to deploy to all users, use a feature flag. Don't maintain a branch for months. Dark launch → canary → full rollout.

5. **Health checks are load-balancer ready before deployment.** Every service must expose a `/health` endpoint that returns 200 when healthy. The load balancer must be configured to stop routing traffic to unhealthy instances.

6. **Monitoring is a prerequisite for go-live, not a follow-up task.** If you cannot observe the service after deployment, you cannot safely deploy. Error rate, latency P95, and CPU/memory must be visible on a dashboard before the first production deployment.

7. **Rollback must be practiced.** Run a rollback drill in staging before the first production deployment. The procedure must be documented and under 10 minutes.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Secrets in code or config files | Stop everything. Move to secrets manager (AWS Secrets Manager, Vault, GitHub Secrets). Rotate all exposed secrets. |
| `npm install` running on production server | Wrong pattern. Build Docker image in CI. Push to registry. Deploy the image. |
| No staging environment | Create one before continuing. Deployments without staging are exploratory surgery without anesthesia. |
| Database migration as part of deployment | Run migrations BEFORE deploying new code, using expand-contract. Never migrate during traffic spike. |
| Manual approval gate before production | Use protected environments in GitHub Actions. Require explicit approval from named individuals. |
| "Works on my machine" reports | Standardize on Docker for local development. If it runs in Docker locally, it runs the same way in CI. |
| No rollback procedure documented | Write rollback procedure. Test it in staging. Link it from deployment runbook. |
| Zero-downtime deployment needed | Use: rolling update, blue-green deployment, or canary deployment. Configure readiness probes. |
| Long-running deploy causing downtime | Implement: graceful shutdown signal handling, connection draining (30s), health check that returns unhealthy before process exits |
| New team member deploying for first time | Pair program the first deploy. Runbook must be sufficient for them to do it alone the second time. |

## Deployment Checklist (Pre-Deploy)

### Code Readiness
- [ ] All CI checks passing (lint, tests, build, security scan)
- [ ] PR reviewed and approved
- [ ] Database migrations written and tested on staging
- [ ] Feature flags configured (if applicable)
- [ ] `CHANGELOG.md` updated

### Environment Readiness
- [ ] Secrets updated in secrets manager (if changed in this release)
- [ ] External service credentials valid and tested
- [ ] Staging deployment successful with E2E smoke tests passing
- [ ] Database backup confirmed (before migration-heavy releases)

### Monitoring Readiness
- [ ] Dashboards displaying current baseline metrics
- [ ] Alert thresholds defined: error rate > 1%, P95 latency > 2s
- [ ] On-call person informed of deployment
- [ ] Runbook link bookmarked for quick access

### Rollback Readiness
- [ ] Previous version artifact available in registry
- [ ] Rollback procedure documented and accessible
- [ ] Database rollback script prepared (if migration involved)
- [ ] Decision criteria defined: what metric/threshold triggers rollback?

## Zero-Downtime Deployment Strategies

| Strategy | Use When | Complexity | Rollback Speed |
|----------|----------|------------|----------------|
| Rolling Update | Stateless services, N instances | Low | Fast (redeploy old version) |
| Blue-Green | Critical services, need instant cutover | Medium | Instant (switch load balancer) |
| Canary | High risk change, need gradual validation | High | Fast (remove canary) |
| Feature Flag | Code shipped but not activated | Low | Instant (toggle flag) |

## CI/CD Pipeline Template (GitHub Actions)

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - run: npm run build

  deploy-staging:
    needs: test
    environment: staging
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: ./scripts/deploy.sh staging ${{ github.sha }}
      - name: Run smoke tests
        run: npm run test:smoke -- --env staging

  deploy-production:
    needs: deploy-staging
    environment: production  # Requires manual approval
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh production ${{ github.sha }}
      - name: Verify health checks
        run: ./scripts/verify-health.sh production
```

## DO NOT

- **DO NOT** deploy on Fridays or before holidays unless it's an emergency hotfix
- **DO NOT** deploy without a monitoring dashboard open and visible
- **DO NOT** deploy during high-traffic hours — choose low-traffic windows
- **DO NOT** skip staging — ever
- **DO NOT** manually modify production servers — all changes through code
- **DO NOT** store secrets in environment variables baked into Docker images
- **DO NOT** deploy without notifying the on-call person
- **DO NOT** run database migrations and deploy application code in the same step

## OUTPUT FORMAT

For each deployment, produce a **Deployment Record**:

```markdown
## Deployment Record

**Version:** v2.4.1
**Environment:** Production
**Date:** 2024-01-15 14:30 UTC
**Deployer:** [name]
**Changes:** [link to CHANGELOG / PR list]

### Pre-Deploy Checklist
[x] All CI checks passing
[x] Staging deployment successful
[x] Database migrations tested on staging
[x] On-call notified
[x] Rollback procedure accessible

### Deployment Timeline
- 14:30: Migration started
- 14:32: Migration complete. Row counts verified.
- 14:33: Rolling update started (3 of 5 instances updated)
- 14:36: Rolling update complete. All instances healthy.
- 14:37: Smoke tests passed.

### Post-Deploy Metrics (15 min observation)
- Error rate: 0.02% (baseline: 0.01%) ✅
- P95 latency: 245ms (baseline: 230ms) ✅
- CPU: 42% (baseline: 38%) ✅

**Status: Successful ✅**
```

## QUALITY GATES

- [ ] Deploy pipeline fully automated — zero manual SSH steps
- [ ] `/health` endpoint returns 200 on healthy instance, 503 on unhealthy
- [ ] Rollback tested in staging before first production deploy
- [ ] Zero secrets in codebase, config files, or Docker images
- [ ] Staging and production have matching runtime versions (verify: `node --version`)
- [ ] Monitoring dashboard created and showing pre-deploy baseline
- [ ] Deployment runbook accessible to all team members
- [ ] Recovery time < 10 minutes for standard rollback scenario
- [ ] CI build produces immutable artifact tagged with git SHA
- [ ] Deployment notification sent to team channel on success/failure
