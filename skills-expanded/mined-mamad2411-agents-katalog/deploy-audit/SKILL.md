---
name: deploy-audit
description: "Audit deployment: CI/CD pipelines, IaC configurations, container security, secrets management, supply chain, deployment strategy."
---

# Deploy Audit

Аудит как проект собирается, тестируется, деплоится.

## Принципы

1. **CI/CD is code too** - applies same standards (security, testing, idempotency)
2. **Secrets are never in code** - не в Dockerfile, не в CI workflows, не в configs
3. **Reproducibility** - same commit + same inputs = same artifact

## Workflow

### DP1. Discovery

Найти deployment artifacts:

```bash
# CI/CD configs
ls -la .github/workflows/ 2>/dev/null
ls -la .gitlab-ci.yml Jenkinsfile bitbucket-pipelines.yml 2>/dev/null

# Containers
ls -la Dockerfile docker-compose*.yml 2>/dev/null
find . -name "Dockerfile*" 2>/dev/null

# IaC
ls -la terraform/ infra/ helm/ k8s/ kubernetes/ 2>/dev/null
find . -name "*.tf" -o -name "Chart.yaml" -o -name "kustomization.yaml" 2>/dev/null

# Deploy scripts
ls -la scripts/deploy* bin/deploy* deploy/ 2>/dev/null
```

### DP2. CI/CD Pipeline Review

Для каждого pipeline (например `.github/workflows/ci.yml`):

**Quality gates**:
- [ ] Тесты запускаются перед merge
- [ ] Все тесты required (не optional)
- [ ] Linting/formatting checks
- [ ] Type checking (mypy, tsc)
- [ ] SAST scan (bandit, eslint-security, semgrep)
- [ ] Dependency vulnerability scan (pip-audit, npm audit)
- [ ] License check для dependencies (если applicable)

**Security**:
- [ ] Secrets через `${{ secrets.X }}` или secret manager (не hardcoded)
- [ ] Third-party actions pinned to commit SHA, не tag (для immutability)
- [ ] Permissions principle of least privilege (`permissions:` block правильно настроен)
- [ ] No `pull_request_target` где не должно быть (security risk)

**Efficiency**:
- [ ] Caching используется (npm, pip, gradle, Docker layers)
- [ ] Concurrent job execution где возможно
- [ ] Conditional execution (skip docs-only changes)

**Reliability**:
- [ ] Retry logic для flaky steps
- [ ] Timeout limits настроены
- [ ] Cleanup steps (даже на failure)

### DP3. Container Security

Для Dockerfile:

**Best practices**:
- [ ] Multi-stage build (separates build deps from runtime)
- [ ] Pinned base image versions (`python:3.11.7-slim`, не `python:latest`)
- [ ] Non-root user (`USER appuser`)
- [ ] Minimal layers (combined RUN statements)
- [ ] No secrets via `--build-arg` (visible в `docker history`)
- [ ] `.dockerignore` correctly excludes secrets, .env files, .git

**Common issues**:
- Running as root (CRITICAL для production)
- Hardcoded secrets in ENV (CRITICAL)
- COPY всего проекта (`COPY . .`) без .dockerignore
- Latest tag base images

### DP4. IaC Review

Если есть Terraform/Helm/Kubernetes:

**Terraform**:
- State management - где state? Local file (bad), S3+DynamoDB (good), Terraform Cloud (good)
- Drift detection - есть ли `terraform plan` в CI?
- Modules переиспользуются или копипаста?
- Hardcoded vs variables

**Helm/Kubernetes**:
- Resource limits/requests заданы?
- Health checks (liveness, readiness probes)
- Service Account permissions минимальны?
- Secrets через Kubernetes Secrets, External Secrets Operator, или Sealed Secrets?
- ConfigMaps vs Secrets - sensitive data в Secrets?

### DP5. Secrets Management

Cross-cutting check across всех deployment artifacts:

**Bad patterns** (findings):
- Secrets in `.env` files committed in git
- Secrets in CI workflow files в plaintext
- Secrets in Dockerfile ENV/ARG
- Secrets в Kubernetes ConfigMaps (должны быть в Secrets)

**Good patterns**:
- Secret managers (Infisical, HashiCorp Vault, AWS Secrets Manager, Doppler, Bitwarden Secrets Manager)
- CLI runner pattern (`vault run -- ...`, `infisical run -- ...`, `doppler run -- ...`)
- External Secrets Operator (Kubernetes) - syncs from any of above
- Encrypted Sealed Secrets (Kubernetes) - if no central manager

**Verification по выбранному менеджеру**:
- Используется через CLI runner / SDK init at startup, не прямые HTTP вызовы из application code
- Secrets корректно загружаются в Docker entrypoint / k8s init container
- Секреты не cached в plain text на диске

### DP6. Deployment Strategy

**Production deployment**:
- [ ] Health checks before routing traffic
- [ ] Rolling/blue-green/canary (не "stop-and-replace")
- [ ] Rollback capability (хотя бы git revert + redeploy)
- [ ] Database migrations strategy (forward-only? reversible?)
- [ ] Zero-downtime deployment возможен?

**Environments**:
- [ ] dev/staging/prod parity достаточная?
- [ ] Environment-specific configurations через secrets manager, не git branches?
- [ ] Production deployment требует approval?

### DP7. Monitoring/Observability Setup

Часто упускается:

- [ ] Application logs (structured JSON)
- [ ] Error tracking (Sentry, Rollbar)
- [ ] Metrics (Prometheus/StatsD/Datadog)
- [ ] Tracing (для distributed systems)
- [ ] Alerts настроены для critical paths

В коде искать:
- Logging libraries usage
- Sentry/error tracker initialization
- Metrics emission

### DP8. Supply Chain

- [ ] SBOM генерация в CI (CycloneDX/SPDX)?
- [ ] Image signing (cosign, notary)?
- [ ] Dependency lock files committed (poetry.lock, package-lock.json)?
- [ ] Reproducible builds возможны?

## Severity Application

См. severity rules в `audit-deploy.md` команды.

## Output

Findings в `docs/audit/<TS>/deploy/findings.json`.

Supporting артефакты:
- `pipeline-review.md`
- `container-security.md`
- `iac-review.md`

## Manual review checklist

- [ ] CI runs on every PR
- [ ] Production deploy не возможен без CI passing
- [ ] Secrets никогда в plaintext в репо
- [ ] Containers run as non-root
- [ ] Production deploy reversible (rollback < 5 минут)
- [ ] Critical alerts configured (downtime, errors > threshold)
- [ ] Deployment requires approval для production
