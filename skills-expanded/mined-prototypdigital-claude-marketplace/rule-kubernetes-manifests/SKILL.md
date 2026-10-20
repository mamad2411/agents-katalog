---
name: kubernetes-manifests
description: Write safe, production-grade Kubernetes manifests with resource limits, health checks, and security context.
---

# Kubernetes manifests

Missing resource limits let one pod starve a node; missing probes leave dead pods serving traffic; privileged or root containers turn a compromise into a node takeover. Validate manifests in CI with `kubeconform` or `kube-score` so these gaps fail the build, not production.

## Resource requirements

- Every container must define `resources.requests` and `resources.limits` for CPU and memory.
- Avoid `resources.limits.cpu` throttling in latency-sensitive services — set requests only and rely on node limits.
- Use `LimitRange` objects to enforce defaults at the namespace level.

## Health checks

- Every Deployment and StatefulSet must define `livenessProbe` and `readinessProbe`.
- Use `startupProbe` for slow-starting containers to prevent premature restarts.
- Liveness probes should target a dedicated health endpoint, not the main application endpoint.

## Security

- Never use `privileged: true` without documented justification.
- Set `runAsNonRoot: true` and `readOnlyRootFilesystem: true` in `securityContext`.
- Drop all capabilities and add back only those required: `capabilities: { drop: [ALL] }`.
- Avoid `hostNetwork: true`, `hostPID: true`, and `hostIPC: true`.
- Do not store secrets in plain Kubernetes `Secret` objects in version control; use sealed-secrets, SOPS, or external secrets.

## Image and update strategy

- Never use `:latest` or `:main` image tags; pin to a specific version or digest.
- Set `imagePullPolicy: IfNotPresent` for pinned tags; `Always` only for digest-pinned images.
- Use `RollingUpdate` strategy; set `maxUnavailable: 0` for zero-downtime deploys.
- Define `podDisruptionBudget` for production services.

## Configuration

- Use `ConfigMap` for non-sensitive config; reference in env with `envFrom` for cleanliness.
- Label all resources consistently: `app.kubernetes.io/name`, `app.kubernetes.io/version`, `app.kubernetes.io/managed-by`.
- Validate manifests with `kubeconform` or `kube-score` before applying.

## Examples

```yaml
# BAD — no resource limits, no probes, privileged, floating image tag
containers:
  - name: api
    image: myapp:latest
    securityContext:
      privileged: true

# GOOD — resource limits, probes, non-root, pinned image
containers:
  - name: api
    image: myapp:1.4.2
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        memory: "256Mi"
    securityContext:
      runAsNonRoot: true
      readOnlyRootFilesystem: true
      capabilities:
        drop: [ALL]
    livenessProbe:
      httpGet:
        path: /healthz
        port: 3000
      initialDelaySeconds: 10
    readinessProbe:
      httpGet:
        path: /ready
        port: 3000
```
