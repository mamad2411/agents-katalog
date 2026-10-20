---
name: k8s-skill
description: Generate Kubernetes manifests — deployments, services, ingress, HPA, ConfigMaps, secrets, and Helm charts. Use when the user mentions "Kubernetes", "K8s", "Helm", "deployment manifest", or needs to deploy to a Kubernetes cluster.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Kubernetes Skill

## Output Structure

Generate manifests into a `k8s/` directory at the project root. One resource per file, prefixed with a sort order number:

```
k8s/
├── base/
│   ├── 01-namespace.yaml
│   ├── 02-configmap.yaml
│   ├── 03-secret.yaml
│   ├── 04-deployment.yaml
│   ├── 05-service.yaml
│   ├── 06-ingress.yaml
│   ├── 07-hpa.yaml
│   └── kustomization.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── patches/
    │       └── deployment-replicas.yaml
    ├── staging/
    │   └── kustomization.yaml
    └── prod/
        ├── kustomization.yaml
        └── patches/
            ├── deployment-replicas.yaml
            └── hpa-targets.yaml
```

## Deployment (with Resource Limits)

Every container MUST have `resources.requests` and `resources.limits`. Missing limits = pod can OOM-kill neighbors.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: myapp
  labels:
    app.kubernetes.io/name: api
    app.kubernetes.io/part-of: myapp
    app.kubernetes.io/managed-by: kustomize
spec:
  replicas: 3
  revisionHistoryLimit: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app.kubernetes.io/name: api
  template:
    metadata:
      labels:
        app.kubernetes.io/name: api
    spec:
      serviceAccountName: api
      terminationGracePeriodSeconds: 30
      containers:
        - name: api
          image: registry.example.com/myapp/api:v1.2.0
          ports:
            - name: http
              containerPort: 3000
              protocol: TCP
          env:
            - name: NODE_ENV
              value: production
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: api-config
                  key: log-level
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health
              port: http
            initialDelaySeconds: 15
            periodSeconds: 20
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10
          startupProbe:
            httpGet:
              path: /health
              port: http
            failureThreshold: 30
            periodSeconds: 2
```

## Service + Ingress

```yaml
# 05-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: myapp
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: api
  ports:
    - name: http
      port: 80
      targetPort: http
      protocol: TCP
---
# 06-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  namespace: myapp
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.example.com
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  name: http
```

## HorizontalPodAutoscaler

```yaml
# 07-hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api
  namespace: myapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 20
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
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

## ConfigMap and Secret Patterns

```yaml
# 02-configmap.yaml — non-sensitive configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: myapp
data:
  log-level: "info"
  cache-ttl: "300"
  feature-flags: |
    {
      "new-dashboard": true,
      "beta-search": false
    }
---
# 03-secret.yaml — template only, actual values injected via CI or sealed-secrets
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: myapp
type: Opaque
stringData:
  database-url: "REPLACE_VIA_CI"
  jwt-secret: "REPLACE_VIA_CI"
```

## Constraints

1. **Never use `latest` tag** in container images. Always pin to a specific version (`v1.2.0`) or SHA digest (`@sha256:abc...`).
2. **Never put real secret values in YAML files.** Use placeholder values with a comment indicating the injection method (sealed-secrets, external-secrets-operator, CI pipeline).
3. **Always set `revisionHistoryLimit`** on Deployments. Default of 10 wastes etcd storage in active clusters. Use 5.
4. **Always include `startupProbe`** for containers with slow initialization. Without it, `livenessProbe` can kill pods that haven't finished starting.
5. **HPA `scaleDown` must have a stabilization window** of at least 300 seconds. Without it, the cluster thrashes during traffic fluctuations.
6. **Use `app.kubernetes.io/*` labels** (name, part-of, managed-by) instead of ad-hoc `app: foo` labels. This is the Kubernetes recommended label schema.
7. **Ingress must include rate-limiting annotations.** Unprotected ingress = trivial DDoS target.

## Anti-Patterns

- **No resource limits** — pods without CPU/memory limits can starve other workloads; always set requests and limits
- **Using :latest tag** — non-reproducible deployments; pin to specific version or SHA digest
- **Secrets in YAML** — real secret values in manifest files; use sealed-secrets or external-secrets-operator
- **No probes** — missing liveness/readiness/startup probes; K8s can't manage pod lifecycle without them
- **Single replica** — running one replica with no PDB; any node issue takes the service down

## Checklist

- [ ] Deployment has resource requests and limits
- [ ] Container images pinned to specific version
- [ ] Liveness, readiness, and startup probes configured
- [ ] HPA configured with scaleDown stabilization window
- [ ] Secrets managed via sealed-secrets or external-secrets
- [ ] Ingress has TLS and rate-limiting annotations
- [ ] app.kubernetes.io/* labels on all resources
- [ ] PodDisruptionBudget defined for production workloads
