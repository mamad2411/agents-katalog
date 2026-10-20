---
description: Run Cloud Native and Kubernetes Standards Check
globs: ["k8s/**/*.yaml", "helm/**/*.yaml", "docker-compose*.yml", "Dockerfile*", "*.tf"]
---
# Infrastructure: Cloud Native & Kubernetes Standards

<audit_rules>
- You MUST implement proper resource requests and limits for all containers to prevent resource exhaustion.
- You MUST configure health checks (liveness and readiness probes) for all containerized applications.
- You MUST use specific image tags with digest pinning for reproducible deployments.
- You MUST implement proper secrets management using Kubernetes secrets or external secret stores.
- You MUST configure network policies and security contexts to limit container privileges.
- You MUST ensure all deployments have proper replica sets and anti-affinity rules for high availability.
- You MUST implement proper rolling update strategies with health check thresholds and pod disruption budgets.
- You MUST configure monitoring and logging integration for observability across all services.
- You MUST use infrastructure as code with proper version control and change management.
</audit_rules>

<example_good>
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  labels:
    app: webapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1001
        fsGroup: 2000
      containers:
      - name: webapp
        image: myregistry/webapp@sha256:abc123...
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
```
</example_good>

<example_bad>
```yaml
# BAD: No resource limits, no health checks, using latest tag
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 1
  template:
    spec:
      containers:
      - name: webapp
        image: myregistry/webapp:latest # BAD: Using latest tag
        ports:
        - containerPort: 3000
        # BAD: No resource limits defined
        # BAD: No health checks configured
        env:
        - name: DATABASE_URL
          value: "postgres://user:pass@localhost/db" # BAD: Hardcoded secret
```
</example_bad>

