---
name: kubernetes-manifest
description: Create production Kubernetes manifests with deployments, services, ingress, configs, and autoscaling. Outputs complete YAML with best practices.
argument-hint: [application type, scale requirements, resources]
allowed-tools: Read, Write, Bash
---

# Kubernetes Manifest Design

Create production-ready K8s manifests with proper resource limits, health checks, autoscaling, and security. Not just basic YAML — complete deployment strategies, rollout controls, and operational patterns.

## Process

1. **Define workload type.** Deployment (stateless), StatefulSet (stateful), DaemonSet (per-node), Job (batch).
2. **Set resource requests/limits.** CPU, memory based on profiling.
3. **Add health checks.** Liveness, readiness, startup probes.
4. **Configure autoscaling.** HPA (horizontal), VPA (vertical).
5. **Design networking.** ClusterIP, NodePort, LoadBalancer, Ingress.
6. **Manage configs/secrets.** ConfigMaps, Secrets, environment variables.
7. **Plan storage.** PersistentVolumes for stateful apps.
8. **Set security.** RBAC, PodSecurityPolicy, NetworkPolicy.

## Output Format

### K8s Deployment: [Application Name]

**Workload:** Deployment (3 replicas)  
**Resources:** 500m CPU, 512Mi RAM per pod  
**Autoscaling:** HPA 3-10 replicas @ 70% CPU  
**Service:** ClusterIP + Ingress (NGINX)  
**Health Checks:** HTTP /health, /ready  

---

## Complete Example: Web Application

### Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
  namespace: production
  labels:
    app: webapp
    tier: frontend
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0  # Zero-downtime
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
        tier: frontend
        version: v1.2.0
    spec:
      # Security
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      
      # Init container (migrations)
      initContainers:
      - name: migrate
        image: myapp:1.2.0
        command: ['python', 'manage.py', 'migrate']
        envFrom:
        - secretRef:
            name: db-credentials
      
      containers:
      - name: webapp
        image: myapp:1.2.0
        ports:
        - containerPort: 8000
          name: http
        
        # Resource limits
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1000m
            memory: 1Gi
        
        # Environment variables
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: redis_url
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        
        # Health checks
        livenessProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready/
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 2
        
        startupProbe:
          httpGet:
            path: /health/
            port: 8000
          initialDelaySeconds: 0
          periodSeconds: 5
          failureThreshold: 30  # 150s startup time
        
        # Volume mounts
        volumeMounts:
        - name: static-files
          mountPath: /app/staticfiles
          readOnly: true
        - name: config
          mountPath: /app/config
          readOnly: true
      
      volumes:
      - name: static-files
        emptyDir: {}
      - name: config
        configMap:
          name: app-config
```

### Service (ClusterIP)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
  namespace: production
spec:
  type: ClusterIP
  selector:
    app: webapp
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
```

### Ingress (NGINX)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: webapp-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
spec:
  tls:
  - hosts:
    - app.example.com
    secretName: webapp-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: webapp-service
            port:
              number: 80
```

### HorizontalPodAutoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp
  minReplicas: 3
  maxReplicas: 10
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
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # Wait 5min before scaling down
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60  # Max 50% scale down per minute
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15  # Double pods every 15s if needed
```

### ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  redis_url: "redis://redis-service:6379/0"
  log_level: "INFO"
  feature_flags: |
    {
      "new_ui": true,
      "beta_features": false
    }
```

### Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: production
type: Opaque
stringData:
  url: "postgresql://user:password@db:5432/myapp"
  password: "actual_password_here"
```

---

## StatefulSet (Database)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: production
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            cpu: 1000m
            memory: 2Gi
          limits:
            cpu: 2000m
            memory: 4Gi
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi
```

---

## Resource Sizing Guidelines

### CPU Requests/Limits
```yaml
# Small app (API server)
resources:
  requests:
    cpu: 100m      # 0.1 core
  limits:
    cpu: 500m      # 0.5 core

# Medium app (web server)
resources:
  requests:
    cpu: 500m
  limits:
    cpu: 1000m     # 1 core

# Large app (background worker)
resources:
  requests:
    cpu: 2000m     # 2 cores
  limits:
    cpu: 4000m     # 4 cores
```

**Rule:** requests = typical usage, limits = max usage + 50%

### Memory Requests/Limits
```yaml
# Java app (higher overhead)
resources:
  requests:
    memory: 1Gi
  limits:
    memory: 2Gi

# Python/Node (lower overhead)
resources:
  requests:
    memory: 256Mi
  limits:
    memory: 512Mi
```

**Rule:** Set limits 2x requests for safety margin

---

## Health Check Patterns

### Liveness Probe (Restart on Failure)
```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3    # Restart after 3 failures (30s)
```

**Check:** Is process alive? (DB connection pool exists, not deadlocked)

### Readiness Probe (Remove from Service)
```yaml
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 2
```

**Check:** Can handle traffic? (DB connected, cache reachable)

### Startup Probe (Slow Startup Apps)
```yaml
startupProbe:
  httpGet:
    path: /health/startup
    port: 8000
  periodSeconds: 10
  failureThreshold: 30   # 300s = 5 minutes max startup
```

**Use:** Apps with slow initialization (Java, ML models)

---

## NetworkPolicy (Security)

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: webapp-netpol
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: webapp
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: redis
    ports:
    - protocol: TCP
      port: 6379
```

---

## PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: webapp-pdb
  namespace: production
spec:
  minAvailable: 2  # Always keep 2 pods running
  selector:
    matchLabels:
      app: webapp
```

**Use:** Prevent node drains from taking down entire service

---

## Deployment Strategies

### Rolling Update (Default)
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # 1 extra pod during update
    maxUnavailable: 0  # Zero downtime
```

### Recreate (Downtime OK)
```yaml
strategy:
  type: Recreate  # Kill all, then start new
```

### Blue-Green (Separate Deployment)
```bash
# Deploy green
kubectl apply -f deployment-green.yaml

# Switch service
kubectl patch service webapp -p '{"spec":{"selector":{"version":"green"}}}'

# Remove blue
kubectl delete deployment webapp-blue
```

---

## Kustomize (Environment Management)

**Base:**
```yaml
# base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 2  # Base value
```

**Production Override:**
```yaml
# overlays/production/kustomization.yaml
resources:
- ../../base

replicas:
- name: webapp
  count: 5  # Override for prod

configMapGenerator:
- name: app-config
  literals:
  - LOG_LEVEL=ERROR
```

**Apply:**
```bash
kubectl apply -k overlays/production/
```

---

## Monitoring

```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-metrics
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8000"
    prometheus.io/path: "/metrics"
spec:
  selector:
    app: webapp
  ports:
  - port: 8000
```

---

## Testing

```bash
# Dry run (validate YAML)
kubectl apply -f deployment.yaml --dry-run=client

# Apply with diff preview
kubectl diff -f deployment.yaml

# Rollout status
kubectl rollout status deployment/webapp

# Rollback
kubectl rollout undo deployment/webapp

# Scale manually
kubectl scale deployment webapp --replicas=5

# Get pod logs
kubectl logs -f deployment/webapp

# Port forward for local testing
kubectl port-forward deployment/webapp 8000:8000
```

## Rules

- Resource requests are mandatory — scheduler needs them to place pods efficiently.
- Limits must be 1.5-2x requests — prevents OOM kills under normal load spikes.
- Readiness probe required for zero-downtime deployments — removes unhealthy pods from service.
- maxUnavailable: 0 for critical services — ensures at least one pod always available.
- PodDisruptionBudget required for HA apps — prevents cluster maintenance from causing outages.
- Never use :latest tag — immutable tags (SHA or version) for reproducibility.
- Secrets must not be in Git — use sealed-secrets, external-secrets, or Vault.
- Namespace separation required for multi-tenancy — production/staging/dev isolation.
- HPA minReplicas ≥ 2 for production — single pod = single point of failure.
- StatefulSet for databases — Deployment loses data on pod restart.
