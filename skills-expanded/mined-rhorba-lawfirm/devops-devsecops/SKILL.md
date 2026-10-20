---
name: devops-devsecops
description: >
  Combined DevOps and DevSecOps skill for CI/CD pipelines, infrastructure as code, security scanning,
  container hardening, cloud infrastructure, and monitoring. Use when the user needs CI/CD setup,
  Docker/Kubernetes configs, Terraform/IaC, security scanning (SAST/DAST/SCA), secrets management,
  monitoring/alerting, cloud infra, or any ops + security work. Trigger on: "CI/CD", "pipeline",
  "Docker", "Kubernetes", "Terraform", "infrastructure", "monitoring", "alerting", "Grafana",
  "Prometheus", "security scan", "Trivy", "Semgrep", "Checkov", "Snyk", "hardening", "DevOps",
  "DevSecOps", "infra as code", "cloud", "AWS", "GCP", "Azure", or ops/security work.
---

# DevOps & DevSecOps Engineer

## Role
You build and secure the infrastructure, pipelines, and operational foundation.

**YAGNI for DevOps**: Docker Compose before Kubernetes. Single server before auto-scaling. Simple CI before 15-stage pipelines. Add complexity only when current setup provably can't handle the load.

## Decision Router
Read the relevant reference file ONLY when doing a deep dive:

| Task | Reference |
|---|---|
| Security scanning, OWASP, code vulns | `references/code-security.md` |
| CI/CD pipeline setup and hardening | `references/cicd-security.md` |
| Docker, K8s, container hardening | `references/container-k8s-security.md` |
| AWS/GCP/Azure, IAM, cloud infra | `references/cloud-security.md` |
| Threat modeling, compliance | `references/threat-model-compliance.md` |

## Stack — This Project
**Docker Compose (dev + prod) · Maven (backend) · PNPM (frontend) · Spring Boot Actuator (health) · Prometheus-compatible metrics**

Docker Compose files:
- `docker-compose.dev.yml` — H2 in-memory DB, hot-reload for both backend and frontend
- `docker-compose.prod.yml` — PostgreSQL, multi-stage production builds

## Quick CI/CD Pipeline (GitHub Actions — this project)
```yaml
name: ci
on: [push, pull_request]
permissions:
  contents: read
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin' }
      - name: Build & Test
        run: cd backend && mvn clean verify    # Checkstyle + SpotBugs + JaCoCo (70%)
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install -g pnpm
      - run: cd frontend && pnpm install && pnpm lint && pnpm build
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntocorp/semgrep-action@v1
        with: { config: p/owasp-top-ten }
      - uses: aquasecurity/trivy-action@master
        with: { scan-type: fs, severity: CRITICAL,HIGH, exit-code: '1' }
  build-images:
    needs: [backend, frontend, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose -f docker-compose.prod.yml build
```

## Dev Environment (Docker)
```bash
# Start full stack with hot-reload (H2 database)
docker compose -f docker-compose.dev.yml up --build

# View logs
docker compose -f docker-compose.dev.yml logs -f

# Stop
docker compose -f docker-compose.dev.yml down
```
Access: Frontend → http://localhost:4200 | Backend → http://localhost:8080/api | Swagger → http://localhost:8080/swagger-ui.html

## Production Deploy (Docker Compose + PostgreSQL)
```bash
# Required env vars (set in .env or environment)
# POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
# JWT_SECRET (256-bit minimum)
# CORS_ALLOWED_ORIGINS

docker compose -f docker-compose.prod.yml up --build -d
```
Access: Frontend → http://localhost | Backend → http://localhost:8080

## Spring Boot Actuator Health Checks
```
GET /actuator/health     → overall health
GET /actuator/metrics    → Prometheus-compatible metrics
```
Used by Docker Compose health checks — don't remove these endpoints.

## Infrastructure as Code (Terraform starter)
```hcl
terraform {
  required_version = ">= 1.5"
  backend "s3" {}  # remote state
}

# Adapt provider to user's cloud
provider "aws" {
  region = var.region
}
```

## Monitoring Stack
```
App → Metrics (Prometheus) → Dashboards (Grafana)
  └→ Logs (Loki/ELK) → Alerts (PagerDuty/Slack)
  └→ Traces (Jaeger/Tempo)
  └→ Errors (Sentry)
```

**Essential alerts:**
- Error rate > 1% for 5 min
- Latency p99 > 2s for 5 min
- CPU > 80% for 10 min
- Disk > 85%
- Health check failures
- Certificate expiry < 14 days

## Security Scanning Quick Commands
```bash
# SAST
semgrep ci --config p/owasp-top-ten --config p/security-audit

# SCA (dependency vulns)
trivy fs --severity CRITICAL,HIGH .

# Container image scan
trivy image --severity CRITICAL,HIGH myapp:latest

# IaC scan
checkov -d ./terraform --framework terraform

# Secrets scan
gitleaks detect --source . --verbose
```

## Handoff Points
- **← From Tech Lead**: Receives infra requirements
- **← From Security Engineer**: Receives scanning policies, compliance rules to enforce
- **← From Deployment**: Receives deployment configs to secure
- **← From DBA**: Receives backup/replication infra requirements
- **→ Security Engineer**: Reports scan findings for triage and risk assessment
- **→ Tester**: Provides staging environments
- **→ Deployment**: Provides hardened pipeline and infra
- **→ DBA**: Provides database infra (instances, networking, encryption)
- **→ PM**: Reports security posture, infrastructure status
