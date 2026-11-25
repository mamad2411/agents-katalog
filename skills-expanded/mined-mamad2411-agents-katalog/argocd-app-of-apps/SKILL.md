---
name: argocd-app-of-apps
description: >
  Argo CD app-of-apps (and ApplicationSet) pattern for owned GitOps: root Application
  generating child apps, directory layouts, sync waves, project boundaries, and bootstrap
  order. Use when structuring multi-app monorepos or multi-cluster delivery — not for
  pointing Argo CD at unauthorized third-party clusters or repositories.
---

# Argo CD App Of Apps

## Scope And Authorization

- **In scope:** Argo CD instances, Git repos, and destination clusters you own or may manage under authorization.
- **Out of scope:** Registering unapproved clusters; deploying to customer clusters without agreement; secret exfiltration via Git.
- Root apps are high blast-radius — protect the repo and who can sync the root.
- Prefer declarative Applications in Git over UI-only children.
- Pair with `argo-cd-rbac-basics` for who may sync; use `code-quality-standards` for manifests.

## When To Use

- Bootstrapping many Applications from one root Application.
- Organizing env folders (`apps/base`, `apps/prod`, `apps/dev`) with kustomize/helm.
- Ordering dependencies via sync waves / hooks (CRDs before controllers).
- Choosing app-of-apps vs ApplicationSet (generators for clusters/tenants).
- Recovering from partial sync or orphaned child apps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Argo CD RBAC / policy.csv | `argo-cd-rbac-basics`, `argocd-rbac-csv` |
| Events-driven triggers | `argo-events-sensors` |
| Secrets in Git hygiene | `secrets-management-hygiene` |
| Terraform cloud bootstrap | Terraform skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Pattern | When |
| --- | --- |
| Classic app-of-apps | Static list of Application manifests in a folder |
| Nested app-of-apps | Platform root → team roots → leaf apps |
| ApplicationSet | Generate apps from list/git/cluster/matrix generators |
| AppProject | Bound destinations, source repos, cluster resources |

## Suggested Repo Layout

```text
gitops/
  root/
    Chart.yaml / kustomization.yaml   # or plain Application YAMLs
    applications/
      ingress-nginx.yaml
      cert-manager.yaml
      team-a-app.yaml
  apps/
    team-a/
      base/
      overlays/dev/
      overlays/prod/
```

## Workflow

### 1. Confirm scope and success criteria

1. Record Argo CD version, clusters, Git org, env promotion model, owners.
2. Success: root sync creates/updates all children; orphaned apps pruned only when intended; prod root protected.
3. Define bootstrap order: CRDs → controllers → platform → product apps.

### 2. Inventory current apps

```bash
argocd app list
argocd app get root-apps -o yaml
kubectl -n argocd get applications.argoproj.io
kubectl -n argocd get applicationsets.argoproj.io
kubectl -n argocd get appprojects
```

1. Note which apps are UI-created (not in Git).
2. Map parent/child relationships and destinations.
3. List repos registered in Argo CD.

### 3. Baseline

1. Export all Application CRs before restructuring.
2. Capture sync status and health of critical apps.
3. Confirm AppProject sourceRepos allow the monorepo.

### 4. Implement root Application

**Root Application pointing at folder of children:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-apps
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: platform
  source:
    repoURL: https://git.example.com/org/gitops.git
    targetRevision: main
    path: root/applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

**Child Application example with sync wave:**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: cert-manager
  namespace: argocd
  annotations:
    argocd.argoproj.io/sync-wave: "10"
spec:
  project: platform
  source:
    repoURL: https://git.example.com/org/gitops.git
    targetRevision: main
    path: apps/cert-manager/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: cert-manager
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

**ApplicationSet alternative (cluster generator sketch):**

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: team-a
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - cluster: in-cluster
            url: https://kubernetes.default.svc
            env: prod
  template:
    metadata:
      name: 'team-a-{{env}}'
    spec:
      project: team-a
      source:
        repoURL: https://git.example.com/org/gitops.git
        targetRevision: main
        path: 'apps/team-a/overlays/{{env}}'
      destination:
        server: '{{url}}'
        namespace: team-a
```

**Design rules**

1. Children destination = workload namespaces; root destination = `argocd` (manages Application CRs).
2. Use AppProjects so team apps cannot target `kube-system` or unapproved repos.
3. Separate roots per environment or use overlays carefully — avoid one root auto-pruning prod by mistake.
4. Prefer `Automated` with `prune` only when Git is the SSOT and PR review is mandatory.

### 5. Verify with evidence

```bash
argocd app sync root-apps
argocd app wait root-apps --health
argocd app list -o wide
# Add a child YAML in Git; confirm it appears after refresh
argocd app get cert-manager
# Sync wave order: earlier waves healthy before later apps progress
```

1. Delete a child Application from Git with prune enabled — confirm intentional removal only.
2. Break-glass: disable auto-sync on root during incidents.
3. Confirm RBAC: team cannot sync platform root (`argo-cd-rbac-basics`).

### 6. Observe and harden

1. Alerts on root app Degraded/OutOfSync.
2. Protect `main` with required reviews; restrict who can merge to `root/applications`.
3. Avoid plaintext secrets in app paths; use Sealed Secrets/ESO/SOPS patterns.

### 7. Hand off

1. Diagram root → children → clusters.
2. Onboarding: how a team adds a new Application YAML via PR.
3. Document sync waves and freeze windows.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| SSOT | Applications in Git | UI snowflake apps |
| Projects | Tight source/dest | default project `*` |
| Prune | Automated with review | prune on experimental root against prod |
| Waves | CRDs before consumers | random parallel creates failing |
| Scale | ApplicationSet generators | 500 hand-edited roots |
| Scope | Owned clusters/repos | unapproved destinations |

## Output Checklist

- [ ] Clusters, repos, envs, authorization recorded
- [ ] Root and children inventoried; UI orphans identified
- [ ] Repo layout and AppProjects defined
- [ ] Root Application/ApplicationSet applied
- [ ] Sync waves/hooks for dependencies set
- [ ] Auto-sync/prune policy intentional
- [ ] Evidence of sync health and allow/deny RBAC
- [ ] Alerts on root health
- [ ] `code-quality-standards` applied to GitOps repo

## Rules

- Authorized GitOps only; destinations must be approved clusters.
- Root apps are production control planes — protect Git and RBAC.
- Prefer declarative children; avoid long-lived UI-only apps.
- Never store unencrypted secrets in app paths.
- Focus on app-of-apps topology; route RBAC CSV details to dedicated skills.
