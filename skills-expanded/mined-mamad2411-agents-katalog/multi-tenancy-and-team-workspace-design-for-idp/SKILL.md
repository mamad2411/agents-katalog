---
name: multi-tenancy-and-team-workspace-design-for-idp
description: >
  Designs tenant/workspace isolation within a shared internal developer
  platform — namespace-per-team patterns, RBAC boundaries, quota
  enforcement, and shared-vs-dedicated infrastructure tradeoffs. Use when
  a user asks to "isolate teams on a shared platform," "design namespace-
  per-team multi-tenancy," "set RBAC boundaries between teams in the
  IDP," "decide shared vs. dedicated clusters per tenant," "stop one
  team's workload from affecting another's," or "scope catalog/self-
  service permissions per team."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Multi-Tenancy and Team Workspace Design for IDP

## Purpose

A shared internal developer platform only stays viable if teams sharing
it can't see, break, or starve each other's resources by accident — the
moment one team's misconfigured workload can exhaust a shared cluster's
capacity, or one team's RBAC role can read another team's secrets, the
platform stops being a trustworthy shared substrate and every team either
demands a dedicated environment or starts treating the platform
defensively. Multi-tenancy design is the discipline of drawing tenant
boundaries — namespace-per-team, RBAC scoping, resource quotas, network
policy — deliberately enough that "shared platform" doesn't quietly mean
"soft-isolated at best," while stopping short of giving every team a
fully dedicated cluster, which defeats the cost and operational-overhead
benefits a shared platform exists to provide. This skill covers designing
that isolation boundary: what to isolate at the namespace/RBAC layer,
what genuinely needs dedicated infrastructure instead, and how catalog/
self-service permissions map onto the same tenant boundaries so a team's
platform access matches its infrastructure access.

## When to use

- Designing the tenant model for a new shared Kubernetes-based platform
  (or IDP layered on top of one) before onboarding the first several
  teams.
- A namespace-per-team pattern already exists but teams can still see or
  affect each other's resources — RBAC roles are too broad, no resource
  quotas are set, or network policies don't isolate east-west traffic
  between tenants.
- Deciding whether a specific team or workload needs a dedicated cluster/
  environment versus fitting into the shared multi-tenant one.
- Scoping catalog entity ownership and self-service action permissions
  (in Backstage, Port, Cortex, OpsLevel, or a custom platform) so a
  team's software-catalog access matches its actual infrastructure
  boundary.
- Investigating an incident where one team's workload affected another's
  (a noisy-neighbor resource exhaustion, an RBAC over-grant) to design the
  boundary that should have prevented it.

## Prerequisites & environment

- A Kubernetes cluster (or clusters) with RBAC enabled — the baseline
  substrate this skill's namespace/RBAC patterns assume; for a non-
  Kubernetes platform, the same isolation principles apply at whatever
  the platform's tenant-scoping primitive is (a Humanitec Environment, a
  cloud account/subscription boundary), substituting the equivalent
  construct.
- Cluster-admin access to configure `ResourceQuota`, `LimitRange`,
  `NetworkPolicy`, and RBAC (`Role`/`RoleBinding`) objects — these are the
  concrete mechanisms this skill's guidance is built on.
- A CNI that enforces `NetworkPolicy` (not all do by default — Calico,
  Cilium, and most managed Kubernetes CNIs support it; flannel's default
  mode does not without an add-on) — confirm this before assuming
  network-level tenant isolation is actually in effect.
- An identity provider integrated with the cluster/platform (OIDC, SAML)
  mapping real team membership to Kubernetes/platform groups, so RBAC
  bindings can reference groups rather than individually-listed users.
- The software catalog or portal tool already in place (Backstage, Port,
  Cortex, OpsLevel) whose entity-ownership model needs to align with the
  infrastructure tenant boundary designed here.

## Step-by-step guidance

1. **Choose the tenancy model deliberately: namespace-per-team (soft
   multi-tenancy) versus cluster-per-team (hard multi-tenancy), per
   workload class, not as a single org-wide default.** Namespace-per-team
   is far cheaper to operate (one control plane, shared node pools) and
   sufficient for the large majority of internal workloads; reserve
   dedicated clusters for tenants with a genuine hard requirement — a
   regulatory boundary (e.g. a workload that must run in a physically or
   logically separate control plane for compliance), a distinct blast-
   radius requirement (a tenant whose outage must never be able to
   correlate with another's), or resource profiles so large/spiky that
   sharing a control plane creates real noisy-neighbor risk even with
   quotas in place.
   ```markdown
   # Tenancy decision, by workload class (illustrative)
   - Standard internal services: namespace-per-team, shared cluster.
   - PCI-scoped payment processing: dedicated cluster (compliance
     boundary requires it, not just preference).
   - ML training workloads with unpredictable GPU-node bursts: dedicated
     node pool within the shared cluster (not a full separate cluster —
     the isolation need is capacity/scheduling, not RBAC/network).
   ```

2. **Create one namespace per team (or per team-environment pair) with a
   consistent naming convention**, provisioned through the platform's
   self-service/scaffolding path rather than a manual `kubectl create
   namespace`, so every namespace's quota, RBAC, and network policy are
   applied consistently from creation:
   ```yaml
   apiVersion: v1
   kind: Namespace
   metadata:
     name: checkout-team-production
     labels:
       team: checkout-team
       environment: production
   ```

3. **Bind RBAC roles per namespace via groups, scoped to the minimum
   verbs/resources a team actually needs**, never a cluster-wide
   `ClusterRoleBinding` granting a team broad access "to be safe":
   ```yaml
   apiVersion: rbac.authorization.k8s.io/v1
   kind: Role
   metadata:
     namespace: checkout-team-production
     name: team-workload-manager
   rules:
     - apiGroups: ["apps", ""]
       resources: ["deployments", "services", "configmaps", "pods", "pods/log"]
       verbs: ["get", "list", "watch", "create", "update", "patch"]
     - apiGroups: [""]
       resources: ["secrets"]
       verbs: ["get", "list"]   # read own secrets, not create/delete via kubectl
   ---
   apiVersion: rbac.authorization.k8s.io/v1
   kind: RoleBinding
   metadata:
     namespace: checkout-team-production
     name: checkout-team-binding
   subjects:
     - kind: Group
       name: "checkout-team"
       apiGroup: rbac.authorization.k8s.io
   roleRef:
     kind: Role
     name: team-workload-manager
     apiGroup: rbac.authorization.k8s.io
   ```
   Binding to the `checkout-team` group (sourced from the identity
   provider) rather than individually listing users means team-membership
   changes take effect through the IdP, not a platform-team ticket.

4. **Enforce resource quotas and default limits per namespace** so one
   team's workload can't exhaust shared node capacity and starve another
   tenant — the single most common "shared platform breaks trust"
   incident:
   ```yaml
   apiVersion: v1
   kind: ResourceQuota
   metadata:
     name: checkout-team-quota
     namespace: checkout-team-production
   spec:
     hard:
       requests.cpu: "20"
       requests.memory: 40Gi
       limits.cpu: "40"
       limits.memory: 80Gi
       pods: "100"
   ---
   apiVersion: v1
   kind: LimitRange
   metadata:
     name: checkout-team-default-limits
     namespace: checkout-team-production
   spec:
     limits:
       - default:
           cpu: "500m"
           memory: 512Mi
         defaultRequest:
           cpu: "250m"
           memory: 256Mi
         type: Container
   ```
   `LimitRange` matters as much as `ResourceQuota` — a quota alone doesn't
   stop a single unbounded container from being scheduled and starving
   everything else in the namespace before the quota is even reached at
   the aggregate level.

5. **Isolate east-west network traffic between tenants with
   `NetworkPolicy`**, defaulting to deny-all-ingress-from-other-namespaces
   and explicitly allowing only what's needed (a shared ingress
   controller, a shared observability agent scraping metrics):
   ```yaml
   apiVersion: networking.k8s.io/v1
   kind: NetworkPolicy
   metadata:
     name: default-deny-cross-namespace
     namespace: checkout-team-production
   spec:
     podSelector: {}
     policyTypes: ["Ingress"]
     ingress:
       - from:
           - podSelector: {}   # allow same-namespace traffic
       - from:
           - namespaceSelector:
               matchLabels:
                 platform-shared: "true"   # allow shared ingress/observability namespaces
   ```
   Without this, RBAC isolation still leaves every pod in the cluster
   able to reach every other pod's network endpoints directly — RBAC and
   network policy are separate isolation layers, and skipping either
   leaves a real gap.

6. **Scope secrets per namespace and per tenant in whatever secret store
   backs the cluster** (Vault, cloud KMS-backed secret managers,
   sealed-secrets) — a secrets engine path convention like
   `secret/data/<team>/<environment>/*` with policies scoped to match, so
   a namespace's RBAC boundary and its secrets-access boundary are the
   same boundary, not two separately-configured systems that can drift
   apart.

7. **Align the software catalog's ownership model to the same tenant
   boundary**, so a team's catalog/self-service permissions match its
   actual infrastructure access — a Backstage `Group` entity, a Port
   `team` blueprint, or an OpsLevel team mapping to the same namespace/
   environment scope defined in steps 2–3, not a separately-maintained
   permission model that can drift out of sync with the real RBAC
   bindings:
   ```yaml
   # Backstage catalog-info.yaml
   apiVersion: backstage.io/v1alpha1
   kind: Component
   metadata:
     name: checkout-api
   spec:
     owner: group:checkout-team
     # the k8s namespace this maps to, so RBAC/catalog stay aligned
     annotations:
       kubernetes.io/namespace: checkout-team-production
   ```

8. **Route dedicated-infrastructure decisions through an explicit
   exception process**, the same discipline as a golden-path escape
   hatch — a team asking for a dedicated cluster "for isolation" should
   name the specific compliance/blast-radius/capacity requirement that
   namespace-per-team with quotas and network policy doesn't satisfy,
   rather than defaulting every request to dedicated infrastructure
   because it feels safer.

## Best practices

- Treat namespace-per-team with RBAC, quotas, and network policy as the
  default tenant boundary, and require a named, specific reason
  (compliance, blast-radius, capacity) before granting dedicated
  infrastructure — dedicated-by-default erodes the cost/operational
  benefit a shared platform exists to provide.
- Bind RBAC to identity-provider groups, never to individually-listed
  users — team-membership changes should propagate through the IdP, not
  a platform-team ticket to update a `RoleBinding`.
- Always pair `ResourceQuota` with a `LimitRange` — a quota alone doesn't
  prevent a single unbounded container from starving a namespace before
  the aggregate quota is reached.
- Verify the cluster's CNI actually enforces `NetworkPolicy` before
  relying on it for isolation — some CNI configurations silently accept
  the object without enforcing it, which is a false sense of security
  worse than not having the policy at all.
- Keep the secrets-access boundary identical to the RBAC/namespace
  boundary — a separately-configured secrets-engine policy path that
  doesn't match the namespace convention is a common place isolation
  quietly drifts.
- Align the software catalog's team/ownership model to the same
  namespace/environment boundary used for RBAC, so a team's catalog
  permissions and its actual infrastructure access never diverge.
- Revisit tenancy decisions as workloads change — a workload that started
  as "fits fine in the shared cluster" can outgrow it (see the noisy-
  neighbor pitfall below), and the exception process from step 8 should
  make it easy to reconsider, not just to grant new exceptions.

## Common pitfalls

- **Symptom:** A single team's misconfigured batch job schedules
  thousands of unbounded pods, and every other team's workloads on the
  same shared cluster start getting evicted or fail to schedule.
  **Fix:** No `ResourceQuota`/`LimitRange` was enforcing a ceiling on that
  namespace — add both (step 4), and treat every namespace provisioned
  through the platform as required to have them set from creation, not
  as an opt-in a team can skip.

- **Symptom:** A security review discovers that a `RoleBinding` intended
  to scope `checkout-team` to their own namespace was actually a
  `ClusterRoleBinding`, granting them read access to every other team's
  secrets cluster-wide.
  **Fix:** Audit for `ClusterRoleBinding`/`ClusterRole` usage granted to
  team groups and replace with namespace-scoped `Role`/`RoleBinding`
  (step 3) unless a capability is genuinely cluster-wide by nature (e.g.
  a platform-team's own operator) — a cluster-wide grant "to avoid
  repeating the RBAC config per namespace" is a common but serious
  over-grant.

- **Symptom:** Two teams' pods on the same shared cluster can reach each
  other's internal service endpoints directly, and a security audit flags
  this as a lateral-movement risk during an incident review.
  **Fix:** RBAC controls the Kubernetes API, not pod-to-pod network
  traffic — add a default-deny `NetworkPolicy` per namespace (step 5) and
  confirm the CNI actually enforces it; RBAC isolation alone is
  frequently mistaken for full tenant isolation when it only covers one
  of the two layers that matter.

- **Symptom:** A team is granted a fully dedicated cluster because they
  "wanted stronger isolation," and eighteen months later the platform
  team is operating a dozen near-identical single-tenant clusters with
  no shared efficiency and a full upgrade/patch burden multiplied by
  twelve.
  **Fix:** Route dedicated-infrastructure requests through an explicit
  exception process (step 8) that requires naming the specific
  requirement namespace-per-team with quotas/network policy doesn't
  satisfy — "wanted stronger isolation" without a specific gap named is
  not sufficient justification, and it's cheaper to close a genuine gap
  in the shared model (e.g. add a missing network policy) than to
  operate another dedicated cluster indefinitely.

- **Symptom:** A team's catalog entry in the software portal lists them
  as owning `checkout-api`, but their actual Kubernetes RBAC access maps
  to a differently-named namespace after an unrelated rename, and nobody
  updated the catalog's annotation — leading to a confused on-call
  handoff during an incident where the responding engineer's kubectl
  access didn't match what the catalog implied.
  **Fix:** Treat the catalog's namespace/environment annotation (step 7)
  as generated from the same source of truth as the RBAC binding (e.g.
  both derived from the same team-onboarding automation), not two
  independently hand-maintained records that can silently diverge.

## Worked example

**Scenario:** A platform team is onboarding 15 product teams onto a
shared Kubernetes cluster for the first time, replacing a prior model
where each team had requested (and gotten) their own small cluster,
which had become expensive and slow to patch consistently. One team
processes payment data under PCI scope and needs to justify whether they
still need dedicated infrastructure under the new model.

1. **Tenancy decision (step 1)**: 14 of the 15 teams' workloads have no
   compliance or blast-radius requirement beyond standard isolation —
   namespace-per-team on the shared cluster. The payments team's PCI
   scope is a named, specific compliance requirement, so they keep a
   dedicated cluster — the exception process (step 8) is satisfied by a
   real, citable reason, not general preference.
2. **Namespace provisioning (step 2)**: each of the 14 teams gets a
   `<team>-production` and `<team>-staging` namespace pair, created
   through the platform's self-service onboarding flow, which also
   applies RBAC, quota, and network policy in the same automation run —
   never a manual `kubectl create namespace` a team could request without
   the accompanying controls.
3. **RBAC (step 3)**: each namespace gets a `Role`/`RoleBinding` scoped to
   that team's IdP group, granting deployment/service/configmap
   management and read-only secret access — no `ClusterRoleBinding`
   anywhere in the 14 namespaces.
4. **Quotas (step 4)**: each namespace gets a `ResourceQuota` sized from
   the team's prior dedicated-cluster usage history (avoiding either
   starving them relative to what they actually used, or over-allocating
   the shared cluster's capacity), plus a default `LimitRange` so no
   single unbounded pod can consume it all at once.
5. **Network policy (step 5)**: a default-deny-cross-namespace policy is
   applied to all 14 namespaces, with an explicit allow rule for the
   shared ingress controller and shared observability agent namespaces
   only — verified against the cluster's Cilium CNI, confirmed to enforce
   `NetworkPolicy` (not assumed).
6. **Catalog alignment (step 7)**: each team's Backstage `Group` entity
   and their services' `catalog-info.yaml` `owner`/namespace annotation
   are generated by the same onboarding automation that created the
   namespace and RBAC bindings, so the three stay in sync by construction
   rather than by separate manual upkeep.
7. **Result**: 14 teams move off dedicated clusters onto the shared,
   quota-and-network-policy-isolated cluster within a quarter, with the
   platform team now patching one control plane instead of fifteen; the
   payments team's dedicated cluster remains, justified and documented,
   rather than becoming an unreviewed default every team could have
   claimed.

## Cross-references

- [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — the "thinnest viable platform" sizing discipline this skill's shared-vs-dedicated infrastructure tradeoff (step 1/8) applies at the infrastructure-tenancy level specifically.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — provisioning a namespace and its RBAC/quota/network-policy bundle consistently is exactly the kind of paved-road automation a golden path or scaffolding template should own, rather than a manual per-team setup.
- [humanitec-score-workload-specification](../humanitec-score-workload-specification/SKILL.md) — for platforms using Score/Humanitec instead of raw Kubernetes manifests, Environments and Resource Definition bindings are the equivalent tenant-scoping primitive to the namespace/RBAC pattern described here.
