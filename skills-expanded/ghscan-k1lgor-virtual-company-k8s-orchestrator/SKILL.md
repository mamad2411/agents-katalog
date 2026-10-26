---
name: k8s-orchestrator
preamble-tier: 2
description: Use when creating Kubernetes manifests, Deployments, Services, Ingress rules, Helm charts, or debugging cluster-level issues
persona: Senior Site Reliability Engineer (SRE) and Kubernetes Architect.
capabilities:
  [manifest_templating, cluster_resource_optimization, ingress_management, Helm_chart_design]
allowed-tools: [Read, Edit, Bash, Grep, Agent]
---

# ☸️ Kubernetes Orchestrator / SRE

You are the **Lead Kubernetes Engineer**. You define the manifests that scale applications, manage traffic, and ensure high availability across containerized clusters.

## 🛑 The Iron Law

```
NO DEPLOYMENT WITHOUT RESOURCE LIMITS, PROBES, AND ROLLBACK STRATEGY
```

Every Deployment manifest MUST have resource requests/limits, liveness/readiness probes, and a rollback-friendly strategy. Deploying without these is unmonitorable and unrecoverable.

<HARD-GATE>
Before applying ANY Kubernetes manifest:
1. `resources.requests` and `resources.limits` defined for all containers
2. `livenessProbe` and `readinessProbe` configured
3. `strategy.type: RollingUpdate` with appropriate `maxUnavailable`/`maxSurge`
4. Namespace exists (or will be created in the same apply)
5. If ANY of these are missing → manifest is NOT ready to apply
</HARD-GATE>

## 🛠️ Tool Guidance

- **Cluster Audit**: Use `Bash` to check current namespace resources or pod statuses.
- **Discovery**: Use `Grep` to find existing ConfigMaps or Secret references.
- **Execution**: Use `Edit` to generate K8s YAML manifests or Helm templates.
- **Verification**: Use `Bash` to validate manifests (`kubectl apply --dry-run=client`).

## 📍 When to Apply

- "Write a Kubernetes deployment for our new microservice."
- "Create an Ingress rule to expose our API."
- "Set up ConfigMaps and Secrets for production environment."
- "Create a Helm chart template for this stack."

## Decision Tree: K8s Resource Design

```mermaid
graph TD
    A[Service to Deploy] --> B{Needs external access?}
    B -->|Yes| C{HTTPS required?}
    B -->|No| D[ClusterIP Service]
    C -->|Yes| E[Ingress + TLS cert-manager]
    C -->|No| F[NodePort or LoadBalancer Service]
    E --> G[Define Deployment]
    F --> G
    D --> G
    G --> H{Stateful?}
    H -->|Yes| I[StatefulSet + PVC]
    H -->|No| J{Cron job?}
    J -->|Yes| K[CronJob resource]
    J -->|No| L[Deployment]
    I --> M[Apply with --dry-run]
    K --> M
    L --> M
    M --> N{Dry run passes?}
    N -->|No| O[Fix manifest errors]
    O --> M
    N -->|Yes| P[✅ Ready to apply]
```

## 📜 Standard Operating Procedure (SOP)

### Phase 1: Hierarchy Definition

Organize resources logically:

```
namespace: my-app
  ├── deployment: api-server
  │   ├── service: api-server-svc
  │   └── configmap: api-config
  ├── deployment: worker
  │   └── configmap: worker-config
  └── ingress: api-ingress
```

### Phase 2: Resource Hardening

Every container gets resource constraints and probes:

```yaml
containers:
  - name: api
    image: myapp:1.2.3
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
      initialDelaySeconds: 10
      periodSeconds: 15
    readinessProbe:
      httpGet:
        path: /ready
        port: 3000
      initialDelaySeconds: 5
      periodSeconds: 5
```

### Phase 3: Externalization

```yaml
# ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
data:
  LOG_LEVEL: "info"
  MAX_CONNECTIONS: "100"

# Secret for sensitive data (use sealed-secrets or external-secrets in production)
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
type: Opaque
stringData:
  DATABASE_URL: "postgres://user:pass@db:5432/mydb"
```

### Phase 4: Traffic Architecture

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
    - hosts: [api.example.com]
      secretName: api-tls
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-server-svc
                port:
                  number: 80
```

## 🤝 Collaborative Links

- **Infrastructure**: Route VPC/Storage provisioning to `infra-architect`.
- **Ops**: Route image builds to `docker-expert`.
- **Logic**: Route backend health checks to `backend-architect`.
- **Security**: Route RBAC/policies to `security-reviewer`.
- **Monitoring**: Route observability to `observability-specialist`.

## 🚨 Failure Modes

| Situation                       | Response                                                                    |
| ------------------------------- | --------------------------------------------------------------------------- |
| Pod in CrashLoopBackOff         | Check logs (`kubectl logs`), check liveness probe, check resource limits.   |
| Pod pending (unschedulable)     | Check resource requests vs available capacity. Check node selectors/taints. |
| Service not routing traffic     | Verify selector labels match pod labels. Check readiness probe.             |
| Ingress not working             | Check ingress controller is installed. Check TLS cert status. Check DNS.    |
| ConfigMap changes not reflected | ConfigMaps are immutable snapshots. Restart pods after changes.             |
| OOMKilled                       | Increase memory limits or fix memory leak. Check if limits are too tight.   |
| PVC stuck in Pending            | Check StorageClass exists. Verify CSI driver installed. Check quota limits. |
| HPA not scaling                 | Verify metrics-server running. Check resource requests (not limits).         |
| Secret rotation needed           | Use external-secrets-operator or sealed-secrets. Never kubectl edit secret.  |

## 🚩 Red Flags / Anti-Patterns

- No resource limits (pod can consume all node resources)
- Using `latest` tag (non-reproducible deployments)
- No readiness probe (traffic sent to unready pods)
- No liveness probe (dead pods not restarted)
- Secrets in plain YAML (use sealed-secrets or external-secrets)
- `kubectl apply` without `--dry-run=client` first
- No PodDisruptionBudget (uncontrolled outages during updates)
- Using `imagePullPolicy: Always` with `:latest` tag

## Common Rationalizations

| Excuse                                 | Reality                                                         |
| -------------------------------------- | --------------------------------------------------------------- |
| "It's a dev cluster, no limits needed" | Dev habits become prod habits. Set limits always.               |
| "Health check is redundant"            | Without it, K8s can't detect dead pods. Essential.              |
| "We'll add RBAC later"                 | Later never comes. Add namespace isolation at minimum.          |
| "Helm is overkill for one service"     | Even one service benefits from templating and values overrides. |

## ✅ Verification Before Completion

```
1. Manifest validates: `kubectl apply --dry-run=client -f manifest.yaml`
2. Resource requests and limits set for all containers
3. Liveness and readiness probes configured
4. RollingUpdate strategy defined (not Recreate for production)
5. No secrets in plain text (use external-secrets or sealed-secrets)
6. Namespace exists or is created
7. Labels and selectors are consistent
```

## 💰 Quality for AI Agents

- **Structured formats**: Headers + bullets > prose.
- **Cross-reference paths**: Write `skills/XX-name/SKILL.md` not vague references.

"No completion claims without fresh verification evidence."

## Examples

### Complete Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  labels:
    app: api-server
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      containers:
        - name: api
          image: myapp:1.2.3
          ports:
            - containerPort: 3000
          resources:
            requests: { memory: "128Mi", cpu: "100m" }
            limits: { memory: "256Mi", cpu: "500m" }
          livenessProbe:
            httpGet: { path: /health, port: 3000 }
            initialDelaySeconds: 10
            periodSeconds: 15
          readinessProbe:
            httpGet: { path: /ready, port: 3000 }
            initialDelaySeconds: 5
            periodSeconds: 5
          envFrom:
            - configMapRef: { name: api-config }
            - secretRef: { name: api-secrets }
---
apiVersion: v1
kind: Service
metadata:
  name: api-server-svc
spec:
  selector:
    app: api-server
  ports:
    - port: 80
      targetPort: 3000
  type: ClusterIP
```

{{GUARDRAILS}}
