---
name: gitops-multi-cluster-management
description: >
  Designs hub-and-spoke GitOps topology for managing a fleet of Kubernetes
  clusters from one Argo CD control plane — cluster registration, RBAC
  scoping per spoke cluster, and using the ApplicationSet cluster
  generator to roll out workloads fleet-wide. Use when the user asks to
  "manage multiple clusters with one Argo CD," "register a new cluster
  for GitOps," "design a hub-and-spoke Argo CD topology," "roll a change
  out to every cluster in the fleet," or "scope per-cluster RBAC so one
  compromised spoke can't affect the rest."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: gitops-argo-ecosystem
  maturity: stable
---

# GitOps Multi-Cluster Management

## Purpose

Once an organization runs more than a few Kubernetes clusters (per
environment, per region, per customer, or per team), running a separate
Argo CD instance per cluster stops scaling — every fleet-wide change
requires N manual repeats, and there's no single place to answer "what
version is running where across the whole fleet." Hub-and-spoke topology
puts one Argo CD control plane (the "hub," itself running on a cluster) in
charge of reconciling `Application`s onto many registered "spoke"
clusters, using
[argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)'
Cluster generator to template per-cluster `Application`s automatically.
This matters operationally because it turns fleet management from "how do
we remember to update every cluster" into "how do we register/label a
cluster correctly once," and it centralizes the audit trail and RBAC
boundary for who can change what, where.

## When to use

- Operating more than a handful of Kubernetes clusters that need
  consistent GitOps-managed workloads (platform agents, ingress
  controllers, monitoring stacks, or application workloads themselves).
- Standing up a new cluster and needing it to automatically receive its
  expected baseline workloads without hand-authoring `Application`
  manifests for it.
- Designing RBAC boundaries so a hub compromise, or a single spoke
  compromise, has bounded blast radius rather than fleet-wide access.
- Deciding between a single shared hub Argo CD instance versus
  regional/per-tier hub instances, based on blast-radius and
  latency/availability tradeoffs.
- Diagnosing a cluster that isn't receiving the Applications it should, or
  one receiving Applications it shouldn't.

## Prerequisites & environment

- A hub cluster running Argo CD ≥ 2.9 with network reachability
  (typically via the spoke cluster's Kubernetes API endpoint, reachable
  from the hub, or vice versa via Argo CD's cluster-add mechanism) to
  every spoke cluster's API server.
- Read/apply credentials for each spoke cluster: a `ServiceAccount` +
  `ClusterRole`/`ClusterRoleBinding` created *on the spoke* that Argo CD
  authenticates as, scoped to only the namespaces/resource kinds that
  cluster's workloads need — not the spoke's own cluster-admin.
- `argocd` CLI with hub cluster context configured
  (`argocd login <HUB_ARGOCD_SERVER>`), and `kubectl` contexts for each
  spoke cluster available locally for registration and verification.
- A GitOps config repo structure that already separates workload
  definitions by concern (per-service overlays) — see
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md) — since
  multi-cluster management builds a cluster dimension on top of that, not
  a replacement for it.
- A decided labeling scheme for clusters (tier, region, business unit)
  before registering any cluster — retrofitting labels onto dozens of
  already-registered clusters is far more error-prone than deciding the
  scheme up front.

## Step-by-step guidance

1. **Register each spoke cluster with the hub**, either via the CLI
   (creates the underlying `Secret` for you) or by authoring the `Secret`
   directly for GitOps-managed registration:
   ```bash
   argocd cluster add <SPOKE_KUBECONFIG_CONTEXT> \
     --name us-east-1-prod \
     --label tier=production \
     --label region=us-east-1
   ```
   Declarative equivalent (preferred for auditability — the registration
   itself becomes a Git-tracked change):
   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: cluster-us-east-1-prod
     namespace: argocd
     labels:
       argocd.argoproj.io/secret-type: cluster
       tier: production
       region: us-east-1
   type: Opaque
   stringData:
     name: us-east-1-prod
     server: https://<SPOKE_API_SERVER_ENDPOINT>
     config: |
       {
         "bearerToken": "${SPOKE_CLUSTER_TOKEN}",
         "tlsClientConfig": {
           "insecure": false,
           "caData": "${SPOKE_CA_DATA_BASE64}"
         }
       }
   ```
   The `${SPOKE_CLUSTER_TOKEN}`/`${SPOKE_CA_DATA_BASE64}` placeholders
   must be filled from a secrets-management pipeline (Sealed Secrets,
   External Secrets Operator) before this is committed — never commit the
   literal bearer token in plaintext, per
   [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)'s
   secrets guidance.

2. **Scope the spoke-side ServiceAccount narrowly**, created on each
   spoke cluster before registration, rather than granting the hub
   cluster-admin on every spoke:
   ```yaml
   # Applied ON the spoke cluster, not the hub
   apiVersion: v1
   kind: ServiceAccount
   metadata:
     name: argocd-manager
     namespace: kube-system
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRole
   metadata:
     name: argocd-manager-role
   rules:
     - apiGroups: ["*"]
       resources: ["*"]
       verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
       # Narrow this to only the resource kinds/namespaces this spoke's
       # workloads actually need, rather than "*" on every fleet member —
       # a platform-agent-only spoke needs far less than an
       # application-workload spoke.
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: ClusterRoleBinding
   metadata:
     name: argocd-manager-role-binding
   subjects:
     - kind: ServiceAccount
       name: argocd-manager
       namespace: kube-system
   roleRef:
     kind: ClusterRole
     name: argocd-manager-role
     apiGroup: rbac.authorization.k8s.io
   ```
   > **Warning:** the Argo CD documentation's default cluster-registration
   > `ClusterRole` grants `*`/`*` across all resources for convenience.
   > Treat that as a starting point to narrow, not a safe production
   > default — a hub credential with cluster-admin on every spoke means a
   > single hub compromise is a fleet-wide compromise.

3. **Use `AppProject` to scope which clusters/namespaces/repos an
   `Application` or `ApplicationSet` may target**, per team or tier:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: AppProject
   metadata:
     name: platform-team
     namespace: argocd
   spec:
     sourceRepos:
       - https://github.com/example/gitops-config.git
     destinations:
       - server: "*"
         namespace: platform-system
     clusterResourceWhitelist:
       - group: ""
         kind: Namespace
   ```
   Restricting `destinations` and `clusterResourceWhitelist` per
   `AppProject` bounds what any `Application`/`ApplicationSet` assigned to
   that project can touch, independent of the broader hub RBAC.

4. **Roll workloads out fleet-wide with the `ApplicationSet` Cluster
   generator**, filtering by the labels set at registration (full
   mechanics in
   [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)):
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: ApplicationSet
   metadata:
     name: fleet-baseline
     namespace: argocd
   spec:
     goTemplate: true
     generators:
       - clusters:
           selector:
             matchLabels: { tier: production }
     template:
       metadata:
         name: "fleet-baseline-{{.name}}"
       spec:
         project: platform-team
         source:
           repoURL: https://github.com/example/gitops-config.git
           targetRevision: main
           path: fleet/baseline
         destination:
           server: "{{.server}}"
           namespace: platform-system
         syncPolicy:
           automated: { prune: true, selfHeal: true }
     syncPolicy:
       preserveResourcesOnDeletion: true
   ```
   New clusters registered with `tier: production` automatically receive
   `fleet-baseline`'s workloads on the next generator refresh — no manual
   `Application` authored per cluster.

5. **Stage fleet-wide rollouts in waves, not one atomic push**, using
   labels to phase which clusters receive a change first:
   ```yaml
   generators:
     - clusters:
         selector:
           matchLabels: { tier: production, rollout-wave: "1" }
   ```
   Bump `rollout-wave` labels on a subset of clusters first (canary
   clusters), verify, then relabel the remaining fleet — this is the
   multi-cluster analog of canary weighting within a single cluster (see
   [argo-rollouts-progressive-delivery](../argo-rollouts-progressive-delivery/SKILL.md)),
   applied at the cluster-fleet level instead of the traffic-percentage
   level.

6. **Decide hub topology deliberately**: one shared hub for the whole
   fleet is simplest to operate but is a single point of failure and a
   single blast radius for a hub-side misconfiguration; per-region or
   per-tier hubs (e.g., a hub per compliance boundary) add operational
   overhead but bound blast radius and reduce cross-region API latency for
   reconciliation. Choose based on fleet size, compliance boundaries
   (data residency requirements often force separate hubs per region), and
   how much a hub outage should be allowed to affect.

7. **Verify fleet state centrally:**
   ```bash
   argocd cluster list
   argocd app list -l argocd.argoproj.io/application-set-name=fleet-baseline
   kubectl get applications -n argocd -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status
   ```
   A single `argocd app list` (or equivalent `kubectl get applications`)
   against the hub answers "what's deployed where and is it healthy"
   across the entire fleet — the concrete payoff of centralizing on one
   control plane.

## Best practices

- Decide the cluster-labeling taxonomy (tier, region, business unit,
  rollout-wave) before registering clusters at scale — labels are how
  every `ApplicationSet` Cluster generator selects its targets, and
  retrofitting a taxonomy onto an already-large fleet means auditing and
  relabeling every cluster Secret.
- Register clusters declaratively (a `Secret` manifest committed to Git,
  values injected via a secrets pipeline) rather than only via
  `argocd cluster add` run ad hoc from someone's laptop — the former is
  auditable and reproducible; the latter isn't.
- Scope the hub's credential on each spoke to the minimum RBAC that
  spoke's workloads need, never blanket cluster-admin — treat each
  spoke's `argocd-manager` `ClusterRole` as something to narrow per
  spoke's actual workload set, not a fleet-wide copy-paste of the
  broadest example.
- Stage fleet-wide changes in labeled waves (canary clusters first) for
  anything riskier than a routine config bump — a single
  `ApplicationSet` targeting the entire fleet with `automated:
  {selfHeal: true}` means one bad manifest reaches every cluster
  simultaneously with no canary period.
- Monitor hub Argo CD's own health and capacity (controller CPU/memory,
  reconciliation queue depth) as fleet size grows — a hub sized for 10
  clusters silently degrades (slow reconciliation, delayed drift
  detection) well before it hard-fails at 100 clusters.
- Keep per-cluster overrides (region-specific config, sizing) in the
  `ApplicationSet` template's parameterization (values injected from the
  cluster Secret's own labels/fields) rather than one-off manual
  `Application` edits that bypass the generator entirely and silently
  drift from the fleet-wide pattern.

## Common pitfalls

- **Symptom:** A newly registered cluster doesn't receive any of the
  expected fleet-wide `Application`s.
  **Fix:** Check the cluster Secret's labels against every fleet
  `ApplicationSet`'s `clusters.selector` — the most common cause is a
  missing or mistyped label at registration time. Confirm with
  `kubectl get secret -n argocd -l argocd.argoproj.io/secret-type=cluster
  --show-labels` before assuming the `ApplicationSet` itself is broken.

- **Symptom:** A change rolled out via a fleet-wide `ApplicationSet` broke
  every cluster simultaneously, with no canary warning.
  **Fix:** This is the risk of targeting the entire fleet in one
  generator match with `automated` sync and no wave staging. Adopt a
  `rollout-wave` label dimension (step 5) so future fleet-wide changes hit
  a small labeled subset first, and roll back the current incident via
  Git revert (per
  [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)),
  which the fleet's `selfHeal` will then propagate back out uniformly.

- **Symptom:** The hub Argo CD instance's reconciliation is falling
  further and further behind as more clusters were added, and drift
  detection/alerts are now hours stale.
  **Fix:** This is hub capacity, not spoke-side, and shows up as
  generically "slow" rather than a specific error — check controller
  resource limits and reconciliation queue metrics on the hub itself,
  and consider splitting into per-region/per-tier hubs (step 6) once a
  single hub's reconciliation latency for the fleet size exceeds
  acceptable drift-detection windows.

- **Symptom:** A spoke cluster's `argocd-manager` credential was scoped
  to cluster-admin "to avoid RBAC troubleshooting," and a later
  investigation found the hub's compromise blast radius included every
  spoke with that same broad role.
  **Fix:** Audit every spoke's `ClusterRole` bound to the hub's service
  account and narrow each to the specific resource kinds/namespaces that
  spoke's workloads require (step 2) — treat "cluster-admin on the spoke"
  as a finding to remediate, not an acceptable operational shortcut.

- **Symptom:** Deregistering a decommissioned cluster (deleting its
  cluster Secret) also deleted the fleet-wide `Application`s that
  targeted it, which cascaded to delete the live workloads on a cluster
  that was actually still receiving production traffic during a delayed
  decommission window.
  **Fix:** This is the same underlying mechanism as the `ApplicationSet`
  pruning pitfall in
  [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)
  — set `syncPolicy.preserveResourcesOnDeletion: true` on fleet-wide
  `ApplicationSet`s, and treat cluster deregistration as a two-step
  process (drain/verify no traffic first, deregister second) rather than
  a single irreversible action.

## Worked example

**Scenario:** Roll a new `network-policy-baseline` workload out to every
production cluster in a 40-cluster fleet, staged as a 3-cluster canary
wave before the remaining 37.

1. Label the 3 canary clusters' registration Secrets
   `rollout-wave: canary` (in addition to their existing `tier:
   production` label); the remaining 37 keep `rollout-wave: stable`.
2. Apply the canary `ApplicationSet`:
   ```yaml
   apiVersion: argoproj.io/v1alpha1
   kind: ApplicationSet
   metadata:
     name: network-policy-baseline-canary
     namespace: argocd
   spec:
     goTemplate: true
     generators:
       - clusters:
           selector:
             matchLabels: { tier: production, rollout-wave: canary }
     template:
       metadata: { name: "netpol-baseline-{{.name}}" }
       spec:
         project: platform-team
         source:
           repoURL: https://github.com/example/gitops-config.git
           targetRevision: main
           path: fleet/network-policy-baseline
         destination: { server: "{{.server}}", namespace: kube-system }
         syncPolicy: { automated: { prune: true, selfHeal: true } }
     syncPolicy: { preserveResourcesOnDeletion: true }
   ```
3. Verify with `argocd app list -l
   argocd.argoproj.io/application-set-name=network-policy-baseline-canary`
   that all 3 canary clusters are `Synced`/`Healthy`, and confirm no
   unexpected traffic drops from the new policy over a soak window.
4. Relabel the remaining 37 clusters' Secrets from `rollout-wave: stable`
   to `rollout-wave: canary` (or introduce a second `ApplicationSet`
   targeting `rollout-wave: stable` with the same `path`), so the
   `Cluster` generator picks them up on its next refresh and the same
   baseline reaches the full fleet.
5. `kubectl get applications -n argocd -l
   argocd.argoproj.io/application-set-name=network-policy-baseline-canary
   -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status`
   gives a single-command view confirming all 40 clusters converged,
   rather than checking each cluster individually.

## Cross-references

- [argocd-applicationset-patterns](../argocd-applicationset-patterns/SKILL.md)
- [argocd-application-configuration](../argocd-application-configuration/SKILL.md)
- [argo-rollouts-progressive-delivery](../argo-rollouts-progressive-delivery/SKILL.md)
- [gitops-workflow](../../../devops/skills/gitops-workflow/SKILL.md)
