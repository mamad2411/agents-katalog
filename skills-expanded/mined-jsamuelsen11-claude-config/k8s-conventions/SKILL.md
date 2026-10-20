---
name: k8s-conventions
description:
  This skill should be used when working with Kubernetes manifests, designing deployments,
  configuring services, or reviewing cluster configuration.
version: 0.1.0
---

# Kubernetes Conventions and Best Practices

This skill provides comprehensive guidelines for writing production-grade Kubernetes manifests that
are secure, maintainable, and follow industry best practices. Apply these conventions when creating
or reviewing any Kubernetes resources including Deployments, Services, ConfigMaps, and cluster
configurations.

## Existing Repository Compatibility

Before applying these conventions, analyze the existing Kubernetes setup:

1. **Manifest Organization** - Check how manifests are organized (kustomize overlays, Helm charts,
   raw YAML, directory structure)
2. **Label Taxonomy** - Identify existing label patterns and naming conventions across resources
3. **Namespace Strategy** - Understand if namespaces are per-environment, per-team, or
   per-application
4. **Tooling Patterns** - Determine if the project uses kustomize, Helm, or plain kubectl
5. **Validation Tools** - Check for existing validation in CI/CD (kubeconform, kubeval, kube-score)
6. **Security Policies** - Review existing PodSecurityStandards, NetworkPolicies, RBAC patterns

When these patterns exist, preserve them. When introducing new resources, follow established
conventions. Only propose changes to existing patterns when they conflict with critical security or
reliability requirements.

## API Version Standards

Always use stable API versions in production manifests. Beta APIs may change or be removed.

### Required Stable Versions

```yaml
# CORRECT: Use stable API versions
apiVersion: apps/v1
kind: Deployment

---
apiVersion: v1
kind: Service

---
apiVersion: networking.k8s.io/v1
kind: Ingress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy

---
apiVersion: batch/v1
kind: Job

---
apiVersion: batch/v1
kind: CronJob

---
apiVersion: policy/v1
kind: PodDisruptionBudget

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
```

```yaml
# WRONG: Beta or deprecated versions
apiVersion: extensions/v1beta1 # Deprecated
kind: Deployment

---
apiVersion: networking.k8s.io/v1beta1 # Use v1
kind: Ingress
```

## Metadata Requirements

Every Kubernetes resource must have complete, consistent metadata.

### Required Metadata Fields

```yaml
# CORRECT: Complete metadata
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
  namespace: production
  labels:
    app.kubernetes.io/name: web-api
    app.kubernetes.io/instance: web-api-prod
    app.kubernetes.io/version: '1.5.2'
    app.kubernetes.io/component: api
    app.kubernetes.io/part-of: e-commerce-platform
    app.kubernetes.io/managed-by: helm
  annotations:
    deployment.kubernetes.io/revision: '3'
    kubectl.kubernetes.io/last-applied-configuration: |
      {...}
```

```yaml
# WRONG: Missing namespace and labels
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
spec:
  replicas: 3
```

### Label Taxonomy

Use the standard `app.kubernetes.io/*` label schema for consistency and tool interoperability.

| Label                          | Required    | Purpose                    | Example                     |
| ------------------------------ | ----------- | -------------------------- | --------------------------- |
| `app.kubernetes.io/name`       | Yes         | Application name           | `web-api`                   |
| `app.kubernetes.io/instance`   | Yes         | Unique instance identifier | `web-api-prod`              |
| `app.kubernetes.io/version`    | Recommended | Application version        | `1.5.2`                     |
| `app.kubernetes.io/component`  | Recommended | Component role             | `api`, `database`, `cache`  |
| `app.kubernetes.io/part-of`    | Recommended | Higher-level application   | `e-commerce-platform`       |
| `app.kubernetes.io/managed-by` | Recommended | Management tool            | `helm`, `kustomize`, `flux` |

```yaml
# CORRECT: Standard label schema with selectors
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
  labels:
    app.kubernetes.io/name: web-api
    app.kubernetes.io/instance: web-api-prod
    app.kubernetes.io/version: '1.5.2'
    app.kubernetes.io/component: api
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: web-api
      app.kubernetes.io/instance: web-api-prod
  template:
    metadata:
      labels:
        app.kubernetes.io/name: web-api
        app.kubernetes.io/instance: web-api-prod
        app.kubernetes.io/version: '1.5.2'
        app.kubernetes.io/component: api
```

```yaml
# WRONG: Custom label schema without standards
metadata:
  labels:
    app: web-api
    env: prod
    version: v1
```

### Annotation Patterns

Use annotations for non-identifying metadata and tool-specific configuration.

```yaml
# CORRECT: Meaningful annotations
metadata:
  annotations:
    # Documentation
    description: 'Public-facing web API for customer orders'
    owner: 'platform-team@example.com'

    # Monitoring
    prometheus.io/scrape: 'true'
    prometheus.io/port: '9090'
    prometheus.io/path: '/metrics'

    # Security scanning
    container.apparmor.security.beta.kubernetes.io/web: runtime/default

    # Change tracking
    change-ticket: 'JIRA-12345'
    deployment-date: '2026-02-09'
```

## Resource Management

Resource requests and limits are critical for cluster stability and scheduling efficiency.

### Resource Specification Rules

1. **Always set both requests and limits** - No exceptions for production workloads
2. **Requests = Limits for Guaranteed QoS** - Critical workloads need consistent resources
3. **CPU in millicores** - Use 100m, 500m, 1000m (not 0.1, 0.5, 1.0)
4. **Memory in Mi/Gi** - Use 128Mi, 1Gi (not MB/GB which are ambiguous)
5. **Start conservative** - Right-size based on metrics, don't guess high

```yaml
# CORRECT: Complete resource specification
apiVersion: v1
kind: Pod
metadata:
  name: web-api
spec:
  containers:
    - name: api
      image: web-api:1.5.2
      resources:
        requests:
          cpu: 500m
          memory: 512Mi
        limits:
          cpu: 1000m
          memory: 1Gi
```

```yaml
# WRONG: No resource specification
apiVersion: v1
kind: Pod
metadata:
  name: web-api
spec:
  containers:
    - name: api
      image: web-api:1.5.2
      # Missing resources - pod can starve cluster
```

```yaml
# WRONG: Incorrect units
resources:
  requests:
    cpu: 0.5 # Use 500m
    memory: 512MB # Use 512Mi
  limits:
    cpu: 1.0 # Use 1000m
    memory: 1GB # Use 1Gi
```

### Quality of Service Classes

Kubernetes assigns QoS classes based on resource configuration:

| QoS Class  | Criteria                             | Use Case                      | Priority               |
| ---------- | ------------------------------------ | ----------------------------- | ---------------------- |
| Guaranteed | requests = limits for all containers | Production critical workloads | Highest                |
| Burstable  | requests < limits                    | Most workloads                | Medium                 |
| BestEffort | No requests or limits                | Development only              | Lowest (first evicted) |

```yaml
# CORRECT: Guaranteed QoS for production database
apiVersion: v1
kind: Pod
metadata:
  name: postgres
spec:
  containers:
    - name: postgres
      image: postgres:14
      resources:
        requests:
          cpu: 2000m
          memory: 4Gi
        limits:
          cpu: 2000m
          memory: 4Gi
```

```yaml
# CORRECT: Burstable QoS for web application
apiVersion: v1
kind: Pod
metadata:
  name: web
spec:
  containers:
    - name: web
      image: nginx:1.24
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi
```

### Namespace Resource Quotas

Every namespace must have ResourceQuota and LimitRange to prevent resource exhaustion.

```yaml
# CORRECT: Namespace resource quota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: '50'
    requests.memory: 100Gi
    limits.cpu: '100'
    limits.memory: 200Gi
    persistentvolumeclaims: '10'
    services.loadbalancers: '5'
    pods: '100'
```

```yaml
# CORRECT: Namespace limit ranges
apiVersion: v1
kind: LimitRange
metadata:
  name: production-limits
  namespace: production
spec:
  limits:
    - max:
        cpu: '4'
        memory: 8Gi
      min:
        cpu: 100m
        memory: 64Mi
      default:
        cpu: 500m
        memory: 512Mi
      defaultRequest:
        cpu: 200m
        memory: 256Mi
      type: Container
    - max:
        cpu: '8'
        memory: 16Gi
      min:
        cpu: 100m
        memory: 64Mi
      type: Pod
```

### Right-Sizing Strategy

1. **Start Conservative** - Begin with lower resource allocations
2. **Monitor Actual Usage** - Use metrics-server, Prometheus, VPA recommendations
3. **Analyze Peak Periods** - Check resource usage during highest load
4. **Apply Headroom** - Add 20-30% buffer for spikes
5. **Test Under Load** - Validate changes with load testing
6. **Iterate** - Continuously refine based on production data

```yaml
# CORRECT: Using VPA in recommend mode
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: web-api-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: web-api
  updateMode: 'Off' # Recommend only, don't auto-apply
  resourcePolicy:
    containerPolicies:
      - containerName: api
        minAllowed:
          cpu: 100m
          memory: 128Mi
        maxAllowed:
          cpu: 2000m
          memory: 4Gi
```

## Security Requirements

Security must be built into every manifest from the start.

### Pod Security Standards

Apply the restricted profile to production namespaces.

```yaml
# CORRECT: Namespace with restricted pod security
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### Security Context Standards

Every pod and container must have appropriate security context.

```yaml
# CORRECT: Complete security context
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 3000
        fsGroup: 2000
        seccompProfile:
          type: RuntimeDefault
      containers:
        - name: api
          image: web-api:1.5.2
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
            runAsNonRoot: true
            runAsUser: 1000
          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache
      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}
```

```yaml
# WRONG: Running as root with privileges
apiVersion: v1
kind: Pod
metadata:
  name: insecure-pod
spec:
  containers:
    - name: app
      image: app:latest
      securityContext:
        privileged: true # Never use in production
        runAsUser: 0 # Never run as root
```

### RBAC Best Practices

Apply least privilege principle to all service accounts.

```yaml
# CORRECT: Dedicated ServiceAccount with minimal permissions
apiVersion: v1
kind: ServiceAccount
metadata:
  name: web-api
  namespace: production
automountServiceAccountToken: false

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: web-api
  namespace: production
rules:
  - apiGroups: ['']
    resources: ['configmaps']
    verbs: ['get', 'list']
    resourceNames: ['web-api-config']

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: web-api
  namespace: production
subjects:
  - kind: ServiceAccount
    name: web-api
    namespace: production
roleRef:
  kind: Role
  name: web-api
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
  namespace: production
spec:
  template:
    spec:
      serviceAccountName: web-api
      automountServiceAccountToken: false # Explicitly disable if not needed
```

```yaml
# WRONG: Using default ServiceAccount
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
spec:
  template:
    spec:
      # No serviceAccountName specified - uses default
      # Default SA often has excessive permissions
```

### Network Policy Requirements

Implement default-deny network policies in all namespaces.

```yaml
# CORRECT: Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# CORRECT: Allow specific ingress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-api-allow-ingress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: web-api
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: internal-client
      ports:
        - protocol: TCP
          port: 8080

---
# CORRECT: Allow specific egress
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-api-allow-egress
  namespace: production
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: web-api
  policyTypes:
    - Egress
  egress:
    - to:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

## Namespace Organization

Choose a namespace strategy and apply it consistently across the cluster.

### Strategy Options

1. **Per-Environment** - Separate namespaces for dev, staging, production
2. **Per-Team** - Namespaces organized by owning team
3. **Per-Application** - Each major application gets dedicated namespace
4. **Hybrid** - Combine approaches (team-environment pattern)

```yaml
# CORRECT: Per-environment strategy
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: production
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: development
    pod-security.kubernetes.io/enforce: baseline
    pod-security.kubernetes.io/audit: baseline
    pod-security.kubernetes.io/warn: baseline
```

```yaml
# CORRECT: Per-team with resource controls
apiVersion: v1
kind: Namespace
metadata:
  name: platform-team
  labels:
    team: platform
    cost-center: '1234'
    pod-security.kubernetes.io/enforce: restricted

---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: platform-team-quota
  namespace: platform-team
spec:
  hard:
    requests.cpu: '20'
    requests.memory: 40Gi
    limits.cpu: '40'
    limits.memory: 80Gi
    persistentvolumeclaims: '10'
```

## Manifest Validation

Use modern validation tools in CI/CD pipelines.

### Kubeconform (Recommended)

Kubeconform is faster and more maintained than kubeval.

```bash
# Install kubeconform
go install github.com/yannh/kubeconform/cmd/kubeconform@latest

# Validate manifests
kubeconform -strict -summary manifests/

# Validate with CRDs
kubeconform -schema-location default \
  -schema-location 'https://raw.githubusercontent.com/datreeio/CRDs-catalog/main/{{.Group}}/{{.ResourceKind}}_{{.ResourceAPIVersion}}.json' \
  manifests/

# Validate Helm chart output
helm template my-chart | kubeconform -strict
```

### Additional Validation Tools

```bash
# kube-score - Best practices analysis
kube-score score manifests/*.yaml

# kubeval - Alternative validator (older)
kubeval --strict manifests/*.yaml

# kubectl dry-run
kubectl apply --dry-run=server -f manifests/
```

## Configuration Management

Handle configuration and secrets properly.

```yaml
# CORRECT: ConfigMap for non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: web-api-config
  namespace: production
data:
  app.properties: |
    server.port=8080
    log.level=INFO
    cache.ttl=300
  feature-flags.json: |
    {
      "newUI": true,
      "betaFeatures": false
    }

---
# CORRECT: Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: web-api-secrets
  namespace: production
type: Opaque
stringData:
  database-url: 'postgresql://user:pass@postgres:5432/app'
  api-key: 'secret-key-here'

---
# CORRECT: Using config and secrets
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-api
spec:
  template:
    spec:
      containers:
        - name: api
          image: web-api:1.5.2
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: web-api-secrets
                  key: database-url
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: web-api-secrets
                  key: api-key
            - name: LOG_LEVEL
              valueFrom:
                configMapKeyRef:
                  name: web-api-config
                  key: log.level
          volumeMounts:
            - name: config
              mountPath: /etc/config
              readOnly: true
      volumes:
        - name: config
          configMap:
            name: web-api-config
```

```yaml
# WRONG: Sensitive data in ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: bad-config
data:
  database-password: 'secretpassword123' # Should be in Secret
  api-key: 'prod-key-12345' # Should be in Secret
```

## Validation Checklist

Before committing any Kubernetes manifest, verify:

- [ ] API version is stable (v1, apps/v1, not beta)
- [ ] Metadata includes name, namespace, and standard labels
- [ ] Resources have both requests and limits defined
- [ ] Security context configured at pod and container level
- [ ] Dedicated ServiceAccount assigned (not default)
- [ ] automountServiceAccountToken explicitly set
- [ ] NetworkPolicy exists for the workload
- [ ] Namespace has ResourceQuota and LimitRange
- [ ] Manifests pass kubeconform validation
- [ ] No secrets in ConfigMaps or environment variables
- [ ] Labels follow app.kubernetes.io/\* taxonomy
- [ ] Annotations include owner and description

Apply these conventions consistently to maintain a secure, reliable, and maintainable Kubernetes
environment.
