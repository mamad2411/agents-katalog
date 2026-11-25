---
name: container-security
description: Docker image hardening, rootless containers, K8s security contexts, network policies, pod security standards, and OPA/Gatekeeper policies
triggers:
  - container security
  - docker hardening
  - rootless container
  - k8s security
  - pod security
  - network policy
  - security context
  - OPA
  - gatekeeper
---

# Container Security

Harden Docker images, enforce Kubernetes security policies, and implement defense-in-depth for containerized services.

## Docker Image Hardening

```dockerfile
# Multi-stage, minimal, rootless
FROM python:3.10-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.10-slim
RUN groupadd -r appuser && useradd --no-log-init -r -g appuser appuser
COPY --from=builder /install /usr/local
COPY --chown=appuser:appuser src/ /app/src/
WORKDIR /app
USER appuser
EXPOSE 8000
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
ENTRYPOINT ["python", "-m", "uvicorn", "coremind.api.main:app", "--host", "0.0.0.0"]
```

### Hardening Checklist
- Use specific image tags, never `latest`
- Multi-stage builds (separate build/runtime)
- Run as non-root user (USER directive)
- No secrets in image layers
- Minimal base image (slim/alpine/distroless)
- HEALTHCHECK defined
- Read-only filesystem where possible
- No unnecessary packages or tools

## Kubernetes Security Context

```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: coremind-api
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

## Network Policies

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: coremind-api-netpol
spec:
  podSelector:
    matchLabels:
      app: coremind-api
  policyTypes: [Ingress, Egress]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: ingress-nginx
      ports:
        - port: 8000
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
    - to:  # DNS
        - namespaceSelector: {}
      ports:
        - port: 53
          protocol: UDP
```

## Scanning Commands

```bash
# Scan Docker image
trivy image coremind-fresh:latest --severity HIGH,CRITICAL

# Scan K8s manifests
trivy config k8s/ --severity HIGH,CRITICAL

# Scan running cluster
trivy k8s --report summary cluster
```
