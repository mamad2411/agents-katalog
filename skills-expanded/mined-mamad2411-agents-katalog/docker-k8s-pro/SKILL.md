---
name: docker-k8s-pro
description: "Multi-stage Docker, K8s manifests, Helm, service mesh, scaling, monitoring. Use when containerizing or deploying services."
---

# Docker & Kubernetes Pro

## Purpose

Containerize and orchestrate applications at production scale. Covers multi-stage Docker builds, Kubernetes manifests, Helm charts, service mesh, horizontal scaling, and production monitoring.

## When to Use

**Use this when:**
- Writing or reviewing Dockerfiles, docker-compose files, or Kubernetes manifests
- Setting up CI/CD pipelines that build, push, and deploy container images
- Configuring Helm charts, ingress rules, or autoscaling policies for a production cluster

**Use this ESPECIALLY when:**
- Containers run as root, lack health checks, or use `latest` image tags in production
- A Kubernetes deployment is missing resource limits, liveness/readiness probes, or HPA configuration
- Secrets are stored as plain Kubernetes Secrets rather than via External Secrets Operator or Vault

**Don't skip when:**
- Sizing resource requests/limits — getting these wrong causes OOMKills and throttling under load
- Defining rolling update strategy — `maxUnavailable: 0` is required to avoid downtime during deploys

## Core Patterns

### 1. Docker Multi-Stage Build

```dockerfile
# ===== BUILDER STAGE =====
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# ===== TEST STAGE =====
FROM builder AS tester
RUN npm run test:ci

# ===== PRODUCTION STAGE =====
FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./
COPY --from=builder /app/node_modules ./node_modules

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1
CMD ["node", "server.js"]
```

### 2. Production Docker Compose

```yaml
version: '3.8'
services:
  app:
    build:
      context: .
      target: runner
    ports: ["3000:3000"]
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    depends_on:
      db:
        condition: service_healthy
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 3. Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
      - name: app
        image: ghcr.io/org/app:${IMAGE_TAG}
        ports:
        - containerPort: 3000
        envFrom:
        - secretRef:
            name: app-secrets
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 15
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: app
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 3000
  selector:
    app: app
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 4. Helm Chart Structure

```
chart/
  Chart.yaml          ← name, version, dependencies
  values.yaml          ← Default config values
  values-production.yaml
  templates/
    deployment.yaml
    service.yaml
    ingress.yaml
    hpa.yaml
    configmap.yaml
    secrets.yaml
    _helpers.tpl       ← Named templates
  charts/              ← Subcharts (Redis, Postgres)
```

### 5. Ingress & TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "10r/s"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: app
            port:
              number: 80
```

### 6. CI/CD Integration

```yaml
# .github/workflows/deploy.yml (excerpt)
- name: Build & Push Docker
  run: |
    docker build --target=runner -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
    docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

- name: Deploy to K8s
  run: |
    helm upgrade --install app ./chart \
      --namespace production \
      --set image.tag=${{ github.sha }} \
      --values chart/values-production.yaml \
      --wait --timeout 5m
```

### Checklist

- [ ] Docker: multi-stage, non-root, health check, .dockerignore
- [ ] K8s: resource limits + requests on every container
- [ ] HPA configured with CPU + memory metrics
- [ ] Rolling update strategy (maxUnavailable: 0)
- [ ] Liveness + readiness probes (not just the same endpoint)
- [ ] PodDisruptionBudget for production
- [ ] Network policies (zero-trust between namespaces)
- [ ] Secrets via External Secrets Operator or vault (not plain secrets)
- [ ] Helm: values per environment (dev/staging/prod)
- [ ] Monitoring: metrics-server, Prometheus, Grafana dashboards

## Related Skills

- **devops-release-engineer** — coordinates the CI/CD pipeline that builds images and triggers Helm deployments produced by this skill
- **cloud-security-auditor** — audit Kubernetes RBAC, network policies, and pod security standards after manifests are drafted here
- **security-reviewer** — review Dockerfiles for secrets baked into layers, non-root user enforcement, and base image CVE exposure
- **performance-engineer** — right-size resource requests/limits and tune HPA thresholds based on observed pod metrics
- **backend-senior-engineer** — define health check endpoint contracts (`/health/live`, `/health/ready`) that probes declared in manifests will call
- **soc2-audit-prep** — verify that logging drivers, image provenance, and secret management patterns satisfy SOC 2 control requirements
- **architecture-planner** — use when choosing between Docker Compose, single-cluster K8s, and multi-cluster topologies before writing manifests
