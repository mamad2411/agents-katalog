---
name: gitops-platform-bootstrap
description: >-
  Design the Git repository structure and Argo CD architecture that runs a GPU
  research platform: app-of-apps bootstrap of platform add-ons (GPU operator,
  DCGM monitoring, KEDA, JupyterHub, model serving), ApplicationSet generators
  for per-researcher environment vending, sync waves for ordered rollout, and
  a secrets strategy (Sealed Secrets vs SOPS vs External Secrets). Use
  whenever the user mentions Argo CD, app of apps, ApplicationSet, GitOps,
  bootstrap a cluster, repo structure or monorepo for Kubernetes, sync waves,
  drift detection, self-heal, Sealed Secrets, SOPS, External Secrets Operator,
  secrets in Git, platform add-ons as code, or vending namespaces/environments
  from Git. Also use to review an existing Argo CD layout. The tenant bundle
  content this vends comes from sibling researcher-tenancy-provisioner; what
  gets deployed (sharing config, ScaledObjects) comes from gpu-sharing-advisor
  and gpu-autoscaling-engineer; policy gates on the repo come from
  k8s-security-baseline.
---

# GitOps Platform Bootstrap

## Purpose
Stand up the delivery backbone of the research platform: every platform add-on and every researcher environment declared in Git, pulled and continuously reconciled by Argo CD, with drift detected and healed automatically. This is the paved road toward an Agentic Developer Portal — when environments are stamped from Git, both humans and agents provision through the same reviewed, auditable path instead of `kubectl apply` side doors.

## Core model to hold in your head

- **GitOps = desired state in Git, an in-cluster agent pulls and reconciles.** Argo CD continuously syncs actual state to the configured revision; `selfHeal: true` reverts manual drift and `prune: true` deletes what Git no longer declares. Argo CD does not prove a commit passed review or CI. Enforce that boundary with protected branches, required checks, CODEOWNERS approval, least-privilege repository writes, and signed commits/tags or immutable production revisions. Deployment credentials never live in CI.
- **App-of-apps** = one root Application pointing at a folder of Application manifests; syncing the root fans out to children. Best for **cluster bootstrap** and managing a related set as one unit.
- **ApplicationSet** = a controller that *generates* Applications from a template + a generator (data source). Best for **scale and vending**: N clusters × M add-ons, or one environment per tenant folder. Field experience: teams converge on ApplicationSets for scalable infrastructure; app-of-apps stays for bootstrap.
- **Sync waves** (`argocd.argoproj.io/sync-wave` annotation) order resources/apps within a sync: lower waves finish healthy before higher waves start. This is how you encode "CRDs and GPU operator before workloads that request GPUs."
- **Argo CD over Flux here**: multi-cluster/vCluster management via cluster secrets + Cluster generator, a UI researchers can read, and ApplicationSets — the multitenancy fit for this platform. (Flux's edge: built-in SOPS decryption.)

## Repository structure

One platform repo (split later only if team boundaries force it):

```
platform/
├── bootstrap/
│   └── root-app.yaml            # the only thing applied by hand, once
├── addons/                      # one folder per platform component (Helm values or manifests)
│   ├── gpu-operator/            # device plugin, MIG manager, driver config, time-slicing ConfigMap
│   ├── monitoring/              # kube-prometheus-stack, dcgm-exporter, dashboards
│   ├── keda/
│   ├── sealed-secrets/
│   ├── ingress/
│   ├── kubecost/                # or opencost
│   ├── jupyterhub/
│   └── serving/                 # vLLM/KServe/Triton platform pieces
├── tenants/                     # one folder per researcher/project environment
│   ├── proj-vision-lab/         # namespace bundle from researcher-tenancy-provisioner
│   │   ├── namespace.yaml
│   │   ├── quota.yaml
│   │   ├── limitrange.yaml
│   │   ├── rbac.yaml
│   │   └── netpol.yaml
│   └── proj-nlp/
├── applicationsets/
│   ├── addons-appset.yaml
│   └── tenants-appset.yaml
└── clusters/                    # per-cluster values overrides (prod / staging / vclusters)
```

Rules: Helm/Kustomize per component with per-cluster value overlays; no environment branches — environments are folders/overlays, promotion is a PR that changes an overlay; CI on the repo runs `kubeconform`/`helm template` + policy checks (Checkov/Kyverno CLI — gates defined with k8s-security-baseline) before merge.

## Bootstrap: the root app (app-of-apps)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: platform-root
  namespace: argocd
spec:
  project: platform
  source:
    repoURL: git@github.com:org/platform.git
    targetRevision: main               # only with protected branch + required checks/CODEOWNERS
    path: applicationsets          # root syncs the ApplicationSets, which generate everything else
    directory:
      recurse: true
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Day-0 sequence on a fresh (Lambda-provisioned) cluster: provider hands you a kubeconfig → install Argo CD (Helm) → apply `root-app.yaml` → everything else flows from Git. Before automated sync/prune, prove branch protection, required CI, CODEOWNERS, least-privilege writers, and audit logging. Prefer signed release tags or commit SHAs for production child applications; a mutable branch is acceptable only when those repository controls are enforced. The managed control plane changes nothing about this pattern; you just never manage etcd/apiserver manifests in the repo.

## Sync-wave plan for a GPU platform

| Wave | Contents | Why first |
|---|---|---|
| 0 | Namespaces, CRDs, Sealed Secrets controller | Everything else depends on them |
| 1 | GPU operator / device plugin (+ time-slicing/MIG config), ingress controller, cert-manager | Nodes must advertise `nvidia.com/gpu` before GPU workloads sync |
| 2 | Monitoring (Prometheus, DCGM-Exporter), KEDA, Kubecost | Scaling and cost need metrics before consumers arrive |
| 3 | JupyterHub, serving platform, tenant environments | Consumers of all the above |

Annotate each child Application: `metadata.annotations: {argocd.argoproj.io/sync-wave: "1"}`. Use sync hooks (PreSync Jobs) for one-time migrations. Without waves, a fresh-cluster bootstrap races: workloads requesting GPUs sync before the device plugin and sit Pending (a signature gpu-workload-troubleshooter recognizes).

## ApplicationSet generators

| Generator | Data source | Platform use |
|---|---|---|
| Git (directories) | Folders in a repo path | **Tenant vending**: one Application per `tenants/*` folder |
| Cluster | Argo CD's registered clusters + labels | Roll add-ons to every cluster/vCluster matching `env=prod` |
| List | Inline list | Small fixed sets; per-add-on values |
| Matrix | Product of two generators | Add-ons × clusters in one spec |
| Pull Request | Open PRs in a repo | Ephemeral preview envs per PR — self-service without cluster permissions |

**Per-researcher environment vending** — the ADP move: creating a tenant = merging a folder; deleting the folder deprovisions (prune):

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: tenants
  namespace: argocd
spec:
  generators:
  - git:
      repoURL: git@github.com:org/platform.git
      revision: main
      directories:
      - path: tenants/*
  template:
    metadata:
      name: "tenant-{{path.basename}}"
      annotations: { argocd.argoproj.io/sync-wave: "3" }
    spec:
      project: tenants                      # Argo CD Project restricting destinations + resource kinds
      source:
        repoURL: git@github.com:org/platform.git
        targetRevision: main
        path: "{{path}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "{{path.basename}}"
      syncPolicy:
        automated: { prune: true, selfHeal: true }
        syncOptions: [CreateNamespace=true]
```

Guard the vending path with an Argo CD **Project**: tenants project may only create the bundle's resource kinds in tenant namespaces — the ApplicationSet can then safely consume folders that tenant leads PR.

**Multitenancy topology**: default to **one shared Argo CD** ("one cockpit") for this platform's size — with RBAC per project/team and the known costs (shared load, coordinated upgrades, single point of failure). Escalate a tenant to a **dedicated Argo CD inside their vCluster** (fleet model) when they need self-managed deployment autonomy — the host Argo CD deploys the vCluster and registers it as a destination cluster; the tenant's instance is theirs (escalation criteria live in researcher-tenancy-provisioner).

## Secrets strategy

Never plaintext secrets in Git. Decision:

| | Sealed Secrets | SOPS | External Secrets Operator (ESO) |
|---|---|---|---|
| Model | Controller in cluster; `kubeseal` encrypts to a cluster keypair; controller decrypts to Secrets | File-level encryption (age/KMS keys); decrypted at deploy | Secrets live in an external manager (Vault/cloud SM); ESO syncs them into the cluster |
| External dependency | None | Key management (KMS or distributed age keys) | A secrets manager must exist |
| Argo CD fit | Native — SealedSecret is just a CR | Needs a plugin (KSOPS); Flux-native, Argo-awkward | Native — ExternalSecret is just a CR |
| Rotation | Manual re-seal | Manual re-encrypt | Automatic sync from the manager |
| Ops trap | Cluster keypair must be backed up; sealed blobs are per-cluster | Key sprawl across teams | Manager availability + auth bootstrap |

Recommendation for Lambda managed K8s (no hyperscaler-native secrets manager wired in): **Sealed Secrets** to start — no external dependencies, the de facto standard where no vault exists — and back up the controller keypair off-cluster from day one. Move to **ESO + self-hosted Vault** when rotation policy, audit requirements, or multi-cluster secret reuse demand it (ask whether the org already runs Vault; ask Lambda if any managed secrets service is on their roadmap). Skip SOPS unless the team is Flux-committed. Typical GPU-platform secrets: Hugging Face tokens, model registry creds, JupyterHub OAuth client, Grafana admin, chargeback API keys.

## Workflow
1. Inventory add-ons and tenants; sketch the repo tree and wave plan.
2. Stand up Argo CD + the root app on a non-prod cluster; bootstrap end-to-end from empty to wave 3; fix ordering issues now.
3. Wire CI validation (schema + policy) as required PR checks on the platform repo.
4. Install the secrets solution at wave 0; migrate existing hand-made Secrets; delete imperative copies.
5. Convert existing hand-deployed add-ons one at a time (import, diff, adopt); forbid `kubectl apply` outside break-glass.
6. Turn on the tenants ApplicationSet; migrate existing namespaces into `tenants/` folders.
7. Document the two golden paths: "add a platform add-on" and "onboard a tenant" — each is a PR template.

## Guardrails
- `prune: true` on tenant apps deletes real environments when folders vanish — protect `tenants/` with CODEOWNERS and branch protection.
- Never let CI push rendered manifests straight to the cluster — that's CI/CD with extra steps, not GitOps; the cluster pulls.
- Argo CD admin creds and the Sealed Secrets keypair are the two crown jewels — RBAC/SSO the first, back up the second.
- selfHeal fights humans silently: if someone must hotfix, they pause sync explicitly (`argocd app set --sync-policy none`), fix, then PR — or their change evaporates.
- One NodePool/add-on config change can drift-replace GPU nodes (expensive); review platform-repo diffs for blast radius like code.
- Don't template what you can't validate: every generator output must pass the same CI checks as hand-written manifests.

## Suggested effort
High initial (3–5 days to a bootstrapped cluster with vending); low steady-state — the point is that onboarding and add-on changes become minutes-long PRs.
