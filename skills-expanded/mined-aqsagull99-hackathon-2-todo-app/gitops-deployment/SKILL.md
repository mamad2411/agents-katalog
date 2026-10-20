---
name: gitops-deployment
description: Master GitOps with ArgoCD for automating Kubernetes deployments from hello world to professional production pipelines. This skill covers ArgoCD installation, application management, sync operations, RBAC, health assessment, and deployment strategies. Use when implementing GitOps practices for Kubernetes with ArgoCD.
---

# GitOps with ArgoCD Deployment Skill

Master GitOps with ArgoCD for automating Kubernetes deployments from hello world to professional production pipelines. This skill covers ArgoCD installation, application management, sync operations, RBAC, health assessment, and deployment strategies.

## Table of Contents
1. [GitOps Principles](#gitops-principles)
2. [ArgoCD Architecture](#argocd-architecture)
3. [Installation and Setup](#installation-and-setup)
4. [Application Management](#application-management)
5. [Sync Operations](#sync-operations)
6. [Projects and RBAC](#projects-and-rbac)
7. [Repositories and Clusters](#repositories-and-clusters)
8. [Health Assessment](#health-assessment)
9. [Automation Policies](#automation-policies)
10. [Deployment Strategies](#deployment-strategies)
11. [Production Best Practices](#production-best-practices)

## GitOps Principles

GitOps is a set of practices that leverage Git as a single source of truth for declarative infrastructure and applications. Key principles include:

### Core Principles
- **Declarative**: Desired state is declared in Git
- **Version Controlled**: All changes are tracked in Git
- **Automated**: Changes are automatically applied to clusters
- **Auditable**: All changes are logged and traceable
- **Reversible**: Rollbacks are simple Git operations

### GitOps Benefits
- **Consistency**: Environments are identical across deployments
- **Traceability**: Every change is tracked in Git history
- **Reliability**: Automated reconciliation ensures desired state
- **Collaboration**: Teams can collaborate using familiar Git workflows
- **Security**: Access control through Git permissions

## ArgoCD Architecture

ArgoCD implements the GitOps pattern by continuously comparing the desired application state from Git repositories with the actual state in target Kubernetes clusters.

### Core Components
- **API Server**: Exposes REST/gRPC APIs and Web UI
- **Repository Server**: Caches Git repositories and generates Kubernetes manifests
- **Application Controller**: Continuously monitors applications and reconciles state differences

### Architecture Diagram
```
┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────────┐
│   Git Repo      │    │     ArgoCD Server    │    │  Target Kubernetes  │
│                 │◄──►│                      │◄──►│                     │
│  (Source of     │    │  • API Server        │    │  • Live State       │
│   Truth)        │    │  • Repository Server │    │                     │
│                 │    │  • Application       │    │                     │
│                 │    │    Controller        │    │                     │
└─────────────────┘    └──────────────────────┘    └─────────────────────┘
```

### Supported Manifest Formats
- Plain YAML/JSON
- Helm Charts
- Kustomize
- Jsonnet
- Custom config management plugins

## Installation and Setup

### Install ArgoCD on Kubernetes
```bash
# Create argocd namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Access ArgoCD UI
```bash
# Port forward to access UI
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Get initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Install ArgoCD CLI
```bash
# Download and install argocd CLI
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install argocd-linux-amd64 /usr/local/bin/argocd
chmod +x /usr/local/bin/argocd
```

## Application Management

### Create Application with Auto-Sync
```bash
argocd app create my-app \
  --repo https://github.com/myorg/myapp.git \
  --path manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production \
  --sync-policy automated
```

### Application Management Commands
```bash
# Get application details
argocd app get my-app

# List applications
argocd app list

# Delete application
argocd app delete my-app

# Set application parameters
argocd app set my-app --parameter image.tag=v1.0.0
```

### Application Manifest (YAML)
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

## Sync Operations

### Sync Strategies
- **Hard Sync**: Delete and recreate resources (potentially disruptive)
- **Apply Sync**: Apply resources using kubectl apply (recommended)
- **Server-Side Apply**: Use server-side apply for merging resources

### Sync Commands
```bash
# Sync application manually
argocd app sync my-app

# Sync specific resources
argocd app sync my-app --resource apps:Deployment:my-deployment

# Sync to specific revision
argocd app sync my-app --revision abc123

# Preview sync (dry run)
argocd app sync my-app --dry-run
```

### Sync Options
```bash
# Enable auto-pruning (delete resources removed from Git)
argocd app set my-app --sync-policy automated --auto-prune

# Enable self-healing (revert manual changes)
argocd app set my-app --self-heal

# Set sync options
argocd app set my-app \
  --sync-option Prune=true \
  --sync-option CreateNamespace=true \
  --sync-option Validate=false
```

### Sync Retry Configuration
```bash
# Configure sync retry backoff
argocd app set my-app \
  --sync-retry-limit 5 \
  --sync-retry-backoff-duration 5s \
  --sync-retry-backoff-factor 2 \
  --sync-retry-backoff-max-duration 3m
```

## Projects and RBAC

### AppProject CRD
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: my-project
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  description: Example Project
  # Allow manifests to deploy from any Git repos
  sourceRepos:
  - '*'
  # Only permit applications to deploy to the guestbook namespace in the same cluster
  destinations:
  - namespace: guestbook
    server: https://kubernetes.default.svc
  # Deny all cluster-scoped resources from being created, except for Namespace
  clusterResourceWhitelist:
  - group: ''
    kind: Namespace
  # Allow all namespaced-scoped resources to be created, except for ResourceQuota, LimitRange, NetworkPolicy
  namespaceResourceBlacklist:
  - group: ''
    kind: ResourceQuota
  - group: ''
    kind: LimitRange
  - group: ''
    kind: NetworkPolicy
  # Deny all namespaced-scoped resources from being created, except for Deployment and StatefulSet
  namespaceResourceWhitelist:
  - group: 'apps'
    kind: Deployment
  - group: 'apps'
    kind: StatefulSet
  roles:
  # A role which provides read-only access to all applications in the project
  - name: read-only
    description: Read-only privileges to my-project
    policies:
    - p, proj:my-project:read-only, applications, get, my-project/*, allow
    groups:
    - my-oidc-group
  # A role which provides sync privileges to only the guestbook-dev application
  - name: ci-role
    description: Sync privileges for guestbook-dev
    policies:
    - p, proj:my-project:ci-role, applications, sync, my-project/guestbook-dev, allow
    jwtTokens:
    - iat: 1535390316
```

### Project Management Commands
```bash
# Create project
argocd proj create my-project

# Get project details
argocd proj get my-project

# Set project parameters
argocd proj set my-project --dest https://kubernetes.default.svc,guestbook
```

### RBAC Configuration
```bash
# RBAC rules for project scoped repositories
p, proj:my-project:admin, repositories, create, my-project/*, allow
p, proj:my-project:admin, repositories, delete, my-project/*, allow
p, proj:my-project:admin, repositories, update, my-project/*, allow
```

## Repositories and Clusters

### Add Repository
```bash
# Add repository via CLI
argocd repo add https://github.com/myorg/myapp.git --insecure-ignore-host-key

# Add repository with credentials
argocd repo add https://github.com/myorg/myapp.git \
  --username myuser \
  --password mypass
```

### Repository Configuration (Secret)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-repo
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: https://github.com/argoproj/private-repo
```

### Cluster Management
```bash
# Add cluster to ArgoCD
argocd cluster add my-cluster-context

# List clusters
argocd cluster list
```

## Health Assessment

### Health States
- **Healthy**: The resource is in a steady, working state
- **Progressing**: The resource is progressing toward a steady state
- **Degraded**: The resource is not functioning as expected
- **Missing**: The resource is not found in the cluster
- **Unknown**: The resource health cannot be determined

### Health Assessment Configuration
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /status/readyReplicas
  - group: argoproj.io
    kind: Application
    jsonPointers:
    - /status/operationState
```

## Quality Gates and Testing

Quality gates ensure that deployments meet predefined criteria before being promoted to production. ArgoCD supports various testing and validation mechanisms to prevent bad deployments.

### Health Checks and Validation
ArgoCD continuously monitors the health of deployed applications and can block deployments based on health status:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    path: manifests
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /status/readyReplicas
  - group: argoproj.io
    kind: Application
    jsonPointers:
    - /status/operationState
```

### Sync Hooks for Quality Gates

Sync hooks allow you to run pre-deployment checks and validation. If the hook fails, the sync operation is blocked:

#### PreSync Hook Example (Database Migration)
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migrate
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookSucceeded
    argocd.argoproj.io/sync-wave: '-1'
spec:
  ttlSecondsAfterFinished: 360
  template:
    spec:
      containers:
        - name: postgresql-client
          image: 'my-postgres-data:11.5'
          imagePullPolicy: Always
          env:
            - name: PGPASSWORD
              value: admin
            - name: POSTGRES_HOST
              value: my_postgresql_db
          command:
            - psql
            - '-h=my_postgresql_db'
            - '-U postgres'
            - '-f preload.sql'
      restartPolicy: Never
  backoffLimit: 1
```

#### PreSync Hook Example (Integration Tests)
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: integration-tests
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: HookFailed
    argocd.argoproj.io/sync-wave: '0'
spec:
  template:
    spec:
      containers:
      - name: test-runner
        image: alpine:latest
        command:
        - sh
        - -c
        - |
          # Run integration tests against the staging environment
          apk add curl
          # Check if staging service is responsive
          timeout 30 sh -c 'until curl -f http://staging-service:8080/health; do sleep 2; done'
          # Run additional validation checks
          if [ $? -eq 0 ]; then
            echo "All quality gates passed"
            exit 0
          else
            echo "Quality gates failed"
            exit 1
          fi
      restartPolicy: Never
```

### Sync Waves for Ordered Execution
Sync waves ensure resources are deployed in a specific order, allowing for validation at each stage:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-with-sync-waves
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    path: manifests-with-waves
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

In the manifest files, annotate resources with sync waves:
- `argocd.argoproj.io/sync-wave: '-3'` - Infrastructure (configmaps, secrets)
- `argocd.argoproj.io/sync-wave: '-2'` - PreSync hooks (validation jobs)
- `argocd.argoproj.io/sync-wave: '-1'` - Additional setup jobs
- `argocd.argoproj.io/sync-wave: '0'` - Main application resources (default)
- `argocd.argoproj.io/sync-wave: '1'` - PostSync hooks (notifications, cleanup)

### Custom Health Checks
Define custom health checks to validate application-specific metrics:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  resource.customizations.health.mycompany.com_MyCustomResource: |
    hs = {}
    if obj.status ~= nil then
      if obj.status.health ~= nil then
        hs.status = obj.status.health.status
        hs.message = obj.status.health.message
      else
        hs.status = "Progressing"
        hs.message = "Waiting for health status"
      end
    else
      hs.status = "Progressing"
      hs.message = "Waiting for resource status"
    end
    return hs
```

## Rollback Strategies

### Application Rollback Using History
ArgoCD maintains a history of deployments, allowing for easy rollbacks to previous versions:

```bash
# View application deployment history
argocd app history my-app

# Expected output:
# ID  DATE                           REVISION
# 0   2025-10-08 10:00:00 +0000 UTC  3f8a19c (HEAD)
# 1   2025-10-08 09:30:00 +0000 UTC  2a1b3c4 (v1.0.1)
# 2   2025-10-08 09:00:00 +0000 UTC  1234567 (v1.0.0)

# Rollback to previous version (ID 1)
argocd app rollback my-app 1

# Rollback without confirmation
argocd app rollback my-app 2 --yes

# Rollback and wait for sync completion
argocd app rollback my-app 1 --timeout 300
```

### Rollback Using Git Tags/Branches
Rollback by reverting to a specific Git tag or commit in your repository:

```bash
# Update application to use a previous version tag
argocd app set my-app --revision v1.0.0

# Or sync to a specific commit hash
argocd app sync my-app --revision abc123def456
```

### Automated Rollback Based on Health
Configure ArgoCD to automatically rollback if health checks fail after deployment:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-auto-rollback
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    path: manifests
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m
```

### Versioned Artifacts Management
Use versioned artifacts to ensure reproducible deployments:

#### Using Helm Charts with Versioned Images
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-helm-versioned
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: helm-chart
    helm:
      valueFiles:
      - values.yaml
      parameters:
      - name: image.repository
        value: myregistry/myapp
      - name: image.tag
        value: v1.2.3  # Versioned artifact
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

#### Using Kustomize with Image Overrides
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-kustomize-versioned
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    targetRevision: HEAD
    path: kustomize-base
    kustomize:
      images:
      - myregistry/myapp:v1.2.3  # Versioned artifact
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### Rollback Procedures
1. **Immediate Rollback**: Use `argocd app rollback` for quick recovery
2. **Manual Sync**: Sync to a known good Git commit/branch
3. **Infrastructure Rollback**: Use infrastructure as code to revert changes
4. **Database Rollback**: Use PreSync/PostSync hooks to handle database migrations

## Automation Policies

### Automated Sync Policy
```yaml
spec:
  syncPolicy:
    automated:
      enabled: true
      prune: true
      selfHeal: true
```

### CLI Configuration
```bash
# Enable automated sync
argocd app set my-app --sync-policy automated

# Enable auto-prune
argocd app set my-app --auto-prune

# Enable self-healing
argocd app set my-app --self-heal

# Disable automated sync
argocd app set my-app --sync-policy none
```

### Sync Options
- **Prune**: Remove resources that are no longer defined in Git
- **Self-Heal**: Automatically revert manual changes to live state
- **CreateNamespace**: Automatically create destination namespace if it doesn't exist
- **Validate**: Validate resources before applying (disable for CRDs)

## Deployment Strategies

### Blue-Green Deployment
```yaml
# Use Argo Rollouts for blue-green deployments
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-rollout
spec:
  strategy:
    blueGreen:
      activeService: my-service-active
      previewService: my-service-preview
      autoPromotionEnabled: false
```

### Canary Deployment
```yaml
# Use Argo Rollouts for canary deployments
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-rollout
spec:
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
```

### Multi-Environment Deployment
```yaml
# Deploy to multiple environments from the same Git repository
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-dev
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    path: manifests/dev
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: dev
---
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-prod
spec:
  source:
    repoURL: https://github.com/myorg/myapp.git
    path: manifests/prod
    targetRevision: HEAD
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
```

## Production Best Practices

### Security
- Use RBAC to restrict access to sensitive projects
- Enable TLS for secure communication
- Rotate admin password regularly
- Use service accounts instead of personal credentials

### Observability
- Enable detailed logging
- Integrate with monitoring systems
- Set up alerts for sync failures
- Monitor application health continuously

### Performance
- Use appropriate resource limits for ArgoCD components
- Configure repository caching appropriately
- Set up proper networking for large repositories
- Use compression for large manifests

### Disaster Recovery
- Backup ArgoCD configuration regularly
- Maintain Git repository backups
- Document recovery procedures
- Test backup/restore procedures regularly

Mastering these GitOps principles and ArgoCD practices will help you build robust, automated Kubernetes deployment pipelines.