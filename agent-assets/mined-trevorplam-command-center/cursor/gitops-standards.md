---
description: Run GitOps and Progressive Delivery Standards Check
globs: ["**/gitops/**/*.yaml", "**/argocd/**/*.yaml", "**/flux/**/*.yaml", "**/helm/**/*.yaml"]
---
# DevOps: GitOps & Progressive Delivery Standards

<audit_rules>
- You MUST implement proper GitOps workflows with declarative configuration management.
- You MUST ensure all infrastructure and application configurations are stored in Git.
- You MUST configure proper automated deployment pipelines with Git as the source of truth.
- You MUST implement proper progressive delivery strategies (canary, blue-green, feature flags).
- You MUST ensure proper rollback mechanisms and automated recovery procedures.
- You MUST configure proper secrets management in GitOps workflows (never store secrets in Git).
- You MUST implement proper drift detection and automated reconciliation.
- You MUST ensure proper audit trails and change tracking for all deployments.
- You MUST configure proper multi-environment GitOps strategies (dev, staging, prod).
- You MUST implement proper compliance and security scanning in GitOps pipelines.
</audit_rules>

<example_good>
```yaml
# GitOps Application Manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: microservice-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/company/k8s-manifests
    targetRevision: main
    path: apps/microservice
  destination:
    server: https://kubernetes.default.svc
    namespace: microservice
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
    - PrunePropagationPolicy=foreground
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
  hooks:
    - type: Sync
      hook:
        command:
        - kubectl
        - apply
        - -f
        - https://github.com/company/pre-deploy-hooks/main.yaml
    - type: PostSync
      hook:
        command:
        - kubectl
        - apply
        - -f
        - https://github.com/company/post-deploy-hooks/main.yaml
---
# Progressive Delivery Strategy
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: microservice-rollout
  namespace: microservice
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 10m}
      - setWeight: 40
      - pause: {duration: 10m}
      - setWeight: 60
      - pause: {duration: 10m}
      - setWeight: 80
      - pause: {duration: 10m}
      canaryService: microservice-canary
      stableService: microservice-stable
      trafficRouting:
        istio:
          virtualService:
            name: microservice-vs
            routes:
            - primary
          destinationRule:
            name: microservice-dr
            canarySubsetName: canary
            stableSubsetName: stable
      analysis:
        templates:
        - templateName: success-rate
        - templateName: latency
        args:
        - name: service-name
          value: microservice-canary
        startingStep: 2
        interval: 5m
  selector:
    matchLabels:
      app: microservice
  template:
    metadata:
      labels:
        app: microservice
    spec:
      containers:
      - name: microservice
        image: microservice:latest
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
# Analysis Template for Progressive Delivery
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  args:
  - name: service-name
  metrics:
  - name: success-rate
    interval: 30s
    count: 10
    successCondition: result[0] >= 0.95
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc.cluster.local:9090
        query: |
          sum(rate(http_requests_total{service="{{args.service-name}}",status!~"5.."}[2m])) /
          sum(rate(http_requests_total{service="{{args.service-name}}"}[2m]))
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: latency
spec:
  args:
  - name: service-name
  metrics:
  - name: latency
    interval: 30s
    count: 10
    successCondition: result[0] <= 0.5
    failureLimit: 3
    provider:
      prometheus:
        address: http://prometheus.monitoring.svc.cluster.local:9090
        query: |
          histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket{service="{{args.service-name}}"}[2m])) by (le)
          )
```
</example_good>

<example_bad>
```yaml
# BAD: No GitOps practices
apiVersion: apps/v1
kind: Deployment
metadata:
  name: microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: microservice
  template:
    spec:
      containers:
      - name: microservice
        image: microservice:latest
        # BAD: No progressive delivery
        # BAD: No health checks
        # BAD: No resource limits
        # BAD: No GitOps automation
        # BAD: No rollback strategy
```
</example_bad>
