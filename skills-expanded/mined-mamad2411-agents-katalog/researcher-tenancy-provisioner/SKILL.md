---
name: researcher-tenancy-provisioner
description: >-
  Stamp out researcher and project environments on a shared GPU Kubernetes
  cluster: namespace + ResourceQuota (including GPU quota via
  requests.nvidia.com/gpu) + LimitRange + RBAC role patterns + default-deny
  NetworkPolicy + Pod Security labels, a JupyterHub workbench with GPU
  notebook profiles, and the call on when a tenant outgrows namespaces and
  needs a vCluster. Use whenever the user asks to onboard a researcher or
  team, create a project namespace, set GPU quotas per team, limit how many
  GPUs a user can take, configure multi-tenancy, isolate researchers from
  each other, set up JupyterHub or notebook profiles with GPUs, write
  Role/RoleBinding for a research team, or asks about ResourceQuota,
  LimitRange, namespace-as-a-service, or vCluster. For vending these bundles
  through Git use sibling gitops-platform-bootstrap; for which GPU slice sizes
  to quota use gpu-sharing-advisor; for the security posture of the shared
  cluster use k8s-security-baseline.
---

# Researcher Tenancy Provisioner

## Purpose
Give every researcher/project a self-contained, bounded environment on the shared GPU cluster in minutes, not tickets: one namespace bundle (quota, limits, RBAC, network isolation, security labels, cost labels) plus an optional JupyterHub workbench with GPU profiles. Enforce fairness on the scarcest resource — GPUs — while keeping the escalation path (vCluster, dedicated pool) explicit. This is the tenancy layer of an Agentic Developer Portal: templated, declarative, stampable.

## Core model to hold in your head

**The tenancy ladder** — start at the bottom, escalate only on evidence:
1. **Namespace-as-a-service** (default): namespace + quota + LimitRange + RBAC + NetworkPolicy + PSS labels. Covers ~90% of research tenants.
2. **vCluster**: a virtual control plane inside a host-cluster namespace. The tenant gets their own API server, CRDs, and even their own Argo CD; workloads still run on shared (or dedicated) host nodes, so GPU scheduling and node pooling stay centralized.
3. **Dedicated cluster**: compliance walls or a project that has matured to production.

**Quota semantics that bite**: ResourceQuota is namespace-scoped and admission-time — a pod exceeding remaining quota is rejected with `Forbidden: exceeded quota` (a *creation* error, distinct from Pending; see gpu-workload-troubleshooter). Quota counts what pods *request*, not what they use — an idle notebook holding 2 GPUs consumes quota and money (gpu-cost-optimizer hunts that gap). Extended resources are quota'd in `requests.<resource>` form only (requests==limits for GPUs anyway). If a namespace has a quota on a resource, every pod must specify that resource — which is why the LimitRange with defaults is mandatory, or podless researchers get rejections they don't understand.

**Every boundary is layered**: quota bounds *how much*, LimitRange bounds *per-container shape*, RBAC bounds *who can act*, NetworkPolicy bounds *who can talk*, PSS labels bound *what privilege pods get*. Ship them as one bundle; a namespace with only some of these is a finding, not a tenant.

## The namespace bundle (stamp per tenant)

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: proj-vision-lab
  labels:
    team: vision-lab
    project: proj-vision
    owner: jdoe
    env: research
    pod-security.kubernetes.io/enforce: baseline   # restricted where images allow
    pod-security.kubernetes.io/warn: restricted
    goldilocks.fairwinds.com/enabled: "true"
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: proj-vision-lab-quota
  namespace: proj-vision-lab
spec:
  hard:
    requests.cpu: "32"
    requests.memory: 256Gi
    limits.cpu: "64"
    limits.memory: 512Gi
    requests.nvidia.com/gpu: "4"          # the headline number per tenant
    # requests.nvidia.com/mig-1g.18gb: "8"  # quota MIG slices separately if fleet uses MIG
    requests.storage: 2Ti
    persistentvolumeclaims: "20"
    pods: "60"
---
apiVersion: v1
kind: LimitRange
metadata:
  name: proj-vision-lab-limits
  namespace: proj-vision-lab
spec:
  limits:
  - type: Container
    default:            { cpu: "2",    memory: 8Gi }   # applied when limits omitted
    defaultRequest:     { cpu: "500m", memory: 2Gi }   # applied when requests omitted
    max:                { cpu: "16",   memory: 128Gi }
    min:                { cpu: "100m", memory: 256Mi }
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: proj-vision-lab
spec:
  podSelector: {}
  policyTypes: [Ingress, Egress]
```

Default-deny is only the base. Add narrow, reviewed policies for required flows: cluster DNS, ingress-controller traffic, Prometheus scraping, approved object-store endpoints, Git/registry egress, telemetry, and explicitly approved external services. Prefer namespace selectors plus destination CIDRs or FQDN-aware policy where the CNI supports it; never add unrestricted `0.0.0.0/0` egress as a convenience. Test both cross-namespace and internet denial from a tenant pod before declaring the boundary complete.

Sizing GPU quota: total of all tenants' `requests.nvidia.com/gpu` may exceed physical supply only if you accept queueing; keep hard-guaranteed tenants ≤ node-pool capacity (ask Lambda: GPUs per node type and max pool size). Under time-slicing, quota counts *virtual* GPUs — set numbers accordingly and say so in the tenant docs. The `team`/`project`/`owner`/`env` labels are the chargeback keys gpu-cost-optimizer depends on — non-negotiable.

## RBAC role patterns

Namespace-scoped only; no cluster-scope grants to researchers; no wildcards in verbs/resources (CIS 5.1.3); `cluster-admin` never bound to humans day-to-day (CIS 5.1.1).

| Persona | Grant | Notes |
|---|---|---|
| Researcher | Role: CRUD on pods, deployments, jobs, services, configmaps, pvcs + pods/log, pods/exec, pods/portforward | The Role below |
| Team lead | Researcher + read quota/limitrange + manage rolebindings within ns | Can onboard teammates, can't raise own quota |
| CI/pipeline SA | Minimal apply rights for its manifests; no secrets read beyond its own | Bind to a dedicated ServiceAccount, never `default` |
| Platform | Built-in `admin` ClusterRole via RoleBinding per ns, or cluster roles held by the platform group | Quota/limits/netpol changes go through Git only |

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: researcher
  namespace: proj-vision-lab
rules:
- apiGroups: ["", "apps", "batch"]
  resources: ["pods", "pods/log", "pods/exec", "pods/portforward", "deployments",
              "statefulsets", "jobs", "cronjobs", "services", "configmaps",
              "persistentvolumeclaims"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list", "create", "update", "delete"]   # own-namespace secrets only, by scoping
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: researcher-jdoe
  namespace: proj-vision-lab
subjects:
- kind: User        # or Group, from the cluster's OIDC identity — ask Lambda how user identity maps in
  name: jdoe@example.org
roleRef: { kind: Role, name: researcher, apiGroup: rbac.authorization.k8s.io }
```

Also stamp: `automountServiceAccountToken: false` on the `default` ServiceAccount (CIS 5.1.5/5.1.6). Verify grants with `kubectl auth can-i --as=jdoe@example.org -n proj-vision-lab <verb> <resource>`.

## When to escalate to vCluster

Escalate a tenant from namespace to vCluster when any of these appear; otherwise don't (it adds an API server + etcd per tenant to operate):
- Needs to install **CRDs/operators** (Ray, Kubeflow, Argo Workflows) that would collide or demand cluster-admin on the host.
- Needs **own Argo CD / own platform tooling** or admin-like experimentation ("Kubernetes-as-a-Service" feel).
- Needs a **different Kubernetes version** or webhook/admission configs than the host.
- Chronic **noisy-neighbor disputes** at the API/controller level that namespaces can't arbitrate.

Pattern: vCluster per tenant in a host namespace (still wrapped by the same quota bundle — the vCluster's workloads consume host quota), host Argo CD registers each vCluster as a destination cluster (see gitops-platform-bootstrap). GPU scheduling remains a host concern: device plugin, taints, and node pools live on the host cluster.

## JupyterHub workbench with GPU profiles

JupyterHub on K8s (Zero-to-JupyterHub Helm chart) gives researchers on-demand notebooks with GPU access and no local setup. Platform decisions that matter:

- **Real authentication** — OIDC/GitHub/institutional SSO. The chart's dummy authenticator is for demos only.
- **Profile list = your GPU menu.** Tie each profile to a resource shape and scheduling constraints:

```yaml
singleuser:
  profileList:
  - display_name: "CPU only (default)"
    default: true
    kubespawner_override:
      cpu_limit: 2
      mem_limit: 8G
  - display_name: "GPU - shared (time-sliced)"
    kubespawner_override:
      extra_resource_limits: { "nvidia.com/gpu": "1" }   # one virtual GPU on time-sliced nodes
      tolerations: [{ key: "nvidia.com/gpu", operator: "Exists", effect: "NoSchedule" }]
      node_selector: { "gpu-sharing": "time-sliced" }
  - display_name: "GPU - dedicated (whole card)"
    kubespawner_override:
      extra_resource_limits: { "nvidia.com/gpu": "1" }
      tolerations: [{ key: "nvidia.com/gpu", operator: "Exists", effect: "NoSchedule" }]
      node_selector: { "gpu-sharing": "exclusive" }
  storage:
    dynamic: { storageClass: standard }   # per-user PVC persists work across sessions
cull:
  enabled: true
  timeout: 3600        # cull idle servers after 1h — the GPU cost control that matters most
```

- Spawn notebooks **into the user's tenant namespace** (or a dedicated hub namespace with its own quota) so notebook GPUs draw from the same quota as batch jobs — one budget per tenant, no side door.
- Default profile is CPU-only; GPU profiles are a deliberate click. Add a MIG-slice profile (`nvidia.com/mig-1g.18gb`) when the fleet runs MIG — slice menu comes from gpu-sharing-advisor.

## Onboarding checklist (per tenant)
1. Intake: team, project name, owner, expected GPU shape (slices vs whole cards), storage need, external endpoints needed.
2. Set quota numbers against current fleet headroom (check node-pool capacity and other tenants' guarantees).
3. Stamp the namespace bundle + Role/RoleBindings from templates; commit to the tenants/ path in Git — the GitOps pipeline applies it (gitops-platform-bootstrap vends this via ApplicationSet).
4. Map identities: confirm the users/group exist in the cluster's OIDC source; bind group not individuals where possible.
5. JupyterHub: add users/group to the hub allowlist; confirm the right profiles are visible.
6. Verify as the tenant: `kubectl auth can-i` matrix; launch a GPU smoke-test pod; confirm quota rejection past the limit; confirm default-deny blocks cross-namespace and unapproved internet traffic while approved DNS/object-store/registry paths still work.
7. Register the tenant in the cost report (labels flow automatically if step 3 was clean) and record the review date for quota right-sizing.

## Guardrails
- Never create a namespace without the full bundle — a quota-less namespace on a GPU cluster is an unbounded budget.
- Never hand out cluster-scope roles or wildcard verbs to researchers; escalation requests route to the vCluster decision instead.
- LimitRange defaults must exist wherever quota exists, or every unspecified pod gets rejected.
- Don't set GPU quota below what a single legitimate job needs (a 2-GPU training job under a 1-GPU quota fails confusingly at admission).
- Quota changes are Git changes, reviewed — no `kubectl edit quota` favors.
- Idle culling on notebooks is on by default; opting out requires the team to accept the cost line in their chargeback.

## Suggested effort
Low per tenant once templated (minutes via GitOps). Initial template build + JupyterHub profile design: 1–2 days. vCluster escalation: half a day per tenant plus ongoing operational ownership — make the tenant accept that cost explicitly.
