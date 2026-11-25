---
name: devops-cicd
description: Use this skill for CI/CD pipelines, Docker containerization, Kubernetes orchestration, cloud infrastructure, Infrastructure as Code (IaC), deployment strategies, monitoring, observability, and DevSecOps. Trigger on keywords: pipeline, Docker, Kubernetes, K8s, CI/CD, GitHub Actions, Terraform, cloud, AWS, GCP, Azure, deploy, container, helm, monitoring, observability, IaC.
---

# DevOps & CI/CD

## Core Philosophy

Infrastructure should be code — version-controlled, reviewed, tested, and reproducible. Every deployment should be automated, auditable, and reversible. Security is not a final step; it is embedded in every stage of the pipeline.

---

## CI/CD Pipeline Blueprint

### Standard Pipeline Stages
```text
Code Push → Lint & Format → Unit Tests → Build → Integration Tests → Security Scan → Deploy to Staging → E2E Tests → Deploy to Production
```

### GitHub Actions Template
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup
        uses: actions/setup-node@v4  # or setup-python, etc.
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test:unit -- --coverage

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency audit
        run: npm audit --audit-level=high
      - name: SAST scan
        uses: github/codeql-action/analyze@v3

  build:
    needs: [quality, security]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
      - name: Push to registry
        run: docker push registry/app:${{ github.sha }}

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging
        run: ./scripts/deploy.sh staging ${{ github.sha }}

  e2e:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e -- --base-url=$STAGING_URL

  deploy-production:
    needs: e2e
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to production
        run: ./scripts/deploy.sh production ${{ github.sha }}
```

---

## Docker Best Practices

### Dockerfile Template
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Runtime (minimal image)
FROM node:20-alpine AS runtime
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/server.js"]
```

### Key Rules
- Use **multi-stage builds** to keep final images small
- Never run as root — create a non-root user
- Use **specific version tags**, not `latest`
- Add `HEALTHCHECK` to every service
- Use `.dockerignore` to exclude `node_modules`, `.git`, test files
- Secrets must never be baked into images — use environment variables or secrets managers

---

## Kubernetes Essentials

### Deployment Template
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    spec:
      containers:
      - name: my-app
        image: registry/app:v1.2.0
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
```

### K8s Checklist
- ✓ Resource requests and limits defined
- ✓ Liveness and readiness probes configured
- ✓ Secrets stored in K8s Secrets (not ConfigMaps)
- ✓ Horizontal Pod Autoscaler configured for production
- ✓ Pod Disruption Budget for high-availability services
- ✓ Network policies to limit pod-to-pod communication

---

## Deployment Strategies

| Strategy | Risk | Speed | Best For |
|---|---|---|---|
| **Rolling** | Low | Medium | Standard deployments |
| **Blue-Green** | Very Low | Fast rollback | Zero-downtime critical services |
| **Canary** | Lowest | Gradual | High-traffic, risk-sensitive features |
| **Recreate** | High | Fastest | Dev environments, non-critical |

---

## Infrastructure as Code (IaC)

### Terraform Structure
```
infrastructure/
├── environments/
│   ├── dev/
│   │   └── main.tf
│   ├── staging/
│   │   └── main.tf
│   └── production/
│       └── main.tf
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── variables.tf
```

### IaC Best Practices
- Store state remotely (S3 + DynamoDB for AWS, GCS for GCP)
- Lock state to prevent concurrent modifications
- Use workspaces or separate directories per environment
- Never hardcode secrets — use variables and secrets managers
- Run `terraform plan` and get human approval before `terraform apply` in production

---

## Monitoring & Observability

### The Three Pillars
| Pillar | Tool Examples | What to Capture |
|---|---|---|
| **Metrics** | Prometheus + Grafana | CPU, memory, request rate, error rate, latency |
| **Logs** | ELK Stack, Loki | Structured JSON logs, request/response, errors |
| **Traces** | Jaeger, OpenTelemetry | Distributed request traces across services |

### Golden Signals to Monitor
1. **Latency** — How long requests take (p50, p95, p99)
2. **Traffic** — Requests per second
3. **Errors** — Error rate (4xx, 5xx)
4. **Saturation** — How full the system is (CPU, memory, queue depth)

### Structured Log Format
```json
{
  "timestamp": "2026-03-20T10:30:00Z",
  "level": "error",
  "service": "api-gateway",
  "trace_id": "abc123",
  "message": "Payment gateway timeout",
  "context": {
    "user_id": "u_456",
    "duration_ms": 5002
  }
}
```

---

## DevSecOps Checklist

- [ ] Dependency vulnerability scanning (npm audit, pip-audit, Snyk)
- [ ] SAST (Static Application Security Testing) in pipeline
- [ ] Container image scanning (Trivy, Grype)
- [ ] Secrets scanning — never commit secrets (use `git-secrets` or GitHub secret scanning)
- [ ] SBOM (Software Bill of Materials) generation for compliance
- [ ] Least-privilege IAM roles for all cloud resources
- [ ] Audit logging enabled for all cloud services
