---
name: complete-idp-deployment-on-kubernetes-from-scratch
description: >
  Sequences a complete, cloud-agnostic Internal Developer Platform
  deployment on any CNCF-conformant Kubernetes cluster: cluster
  conformance validation → cluster add-ons (ingress, TLS, in-cluster
  storage) → Helm-deployed Backstage backed by an in-cluster PostgreSQL
  instance → golden-path scaffolding template → self-service scaffolder
  actions calling generic Kubernetes/Crossplane APIs, deliberately not
  tied to one cloud's IAM or managed-database provisioning APIs →
  scorecards. Use when a user asks to "deploy an IDP on Kubernetes without
  tying it to one cloud," "build a portable/cloud-agnostic internal
  developer platform," "stand up Backstage on any conformant cluster,"
  "design self-service provisioning that doesn't assume AWS/Azure/GCP,"
  or "sequence a vendor-neutral platform rollout on Kubernetes."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on Kubernetes from Scratch

## Purpose

The four cloud-specific IDP deployment skills in this repo
([AWS](../complete-idp-deployment-on-aws-from-scratch/SKILL.md),
[Azure](../complete-idp-deployment-on-azure-from-scratch/SKILL.md),
[GCP](../complete-idp-deployment-on-gcp-from-scratch/SKILL.md),
[OCI](../complete-idp-deployment-on-oci-from-scratch/SKILL.md)) each wire
self-service provisioning directly to one cloud's IAM and managed-database
APIs. This skill is the deliberately different baseline: a platform team
that runs on multiple clouds, wants portability, or simply doesn't want
its self-service layer's core logic to assume a specific cloud provider
needs a version where the cluster is "any CNCF-conformant Kubernetes"
(managed, self-managed, or on the way to being either) and every
provisioning action targets the Kubernetes API itself — Namespaces,
ResourceQuotas, and Crossplane Claims — rather than a cloud SDK call. This
is not a lowest-common-denominator compromise dressed up as "portable";
it's a real architectural choice with a real cost (no cloud-native
IAM-scoped identity federation, no managed-database SLA) that this skill
states plainly rather than glossing over.

## When to use

- A platform team explicitly wants the self-service provisioning layer
  decoupled from any single cloud's IAM/database APIs, whether for
  multi-cloud portability or to avoid cloud-specific lock-in in the
  platform's own core logic.
- Standing up an IDP on a cluster whose underlying infrastructure isn't
  fixed yet, or that will run identically across more than one
  environment (e.g., the same platform stack on a customer's cluster and
  on the vendor's own cluster).
- A team already running Crossplane or another Kubernetes-native
  provisioning control plane that wants the IDP's self-service layer to
  target that abstraction instead of calling a cloud SDK directly.
- Migrating away from a cloud-specific self-service implementation (one
  of the four skills above) toward a portable one, or the reverse —
  auditing whether a "portable" build has secretly grown cloud-specific
  assumptions.

## Prerequisites & environment

- A CNCF-conformant Kubernetes cluster already exists, or is being
  provisioned — either a managed offering (used here purely as compute,
  ignoring its cloud-specific IAM integration; see
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md))
  or self-managed via kubeadm/Cluster API (see
  [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md)).
- `kubectl`, `helm` ≥ 3.8, and Sonobuoy for the Phase 1 conformance check.
- A Node.js/Yarn toolchain to build and customize the Backstage app.
- A CSI-capable default `StorageClass` already available on the cluster
  (block storage of some kind — Longhorn, Rook-Ceph, or the cluster's own
  CSI driver if managed) before Phase 3, since the catalog database here
  is an in-cluster StatefulSet, not a cloud-managed instance.
- A decision, before Phase 6, on whether the generic self-service layer
  provisions via raw Kubernetes objects (Namespaces, Roles) only, or also
  via Crossplane Claims for anything resembling "infrastructure" — this
  materially changes what Phase 6 can actually provision.
- A named approver for the Phase 6 self-service gate, in place before that
  phase goes live.

## Step-by-step guidance

**Phase 1 — Get a conformant cluster and prove it.** Whichever path
produced the cluster — a managed offering per
[managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
or a self-managed one per
[kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md)
— run Sonobuoy conformance (quick mode, then
`certified-conformance`) plus the targeted smoke tests (Service DNS,
cross-node connectivity, PVC provisioning) before treating the cluster as
a platform-hosting target, per
[kubernetes-cluster-post-provision-conformance-validation](../../../kubernetes-platform/skills/kubernetes-cluster-post-provision-conformance-validation/SKILL.md).
This phase is unique to the portable variant — the cloud-specific skills
inherit a managed control plane's own conformance guarantee, but a design
goal here is "any conformant cluster," so verify that guarantee explicitly
rather than assuming it.

**Phase 2 — Cluster add-ons: ingress, TLS, storage.** Install
ingress-nginx for host/path routing to Backstage (and to every service the
golden path later scaffolds), per
[ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md);
install cert-manager for automated TLS issuance (ACME DNS-01 if there's no
single cloud LB to terminate at, or a private CA for internal-only
platforms), per
[cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md);
and confirm a `StorageClass` backed by either Longhorn (simpler, block-only)
or Rook-Ceph (block + object + shared filesystem) is available for Phase
3's catalog database PVC, per
[longhorn-storage-configuration](../../../kubernetes-platform/skills/longhorn-storage-configuration/SKILL.md)
or
[rook-ceph-storage-operations](../../../kubernetes-platform/skills/rook-ceph-storage-operations/SKILL.md).
None of this is needed in the cloud-specific variants, which lean on the
cloud's own load balancer, ACM/managed-cert service, and managed database
— this phase exists specifically because this variant deliberately avoids
those.

**Phase 3 — Backstage on the cluster, backed by in-cluster PostgreSQL.**
Package Backstage as a Helm chart and deploy it against a PostgreSQL
instance running as a StatefulSet inside the same cluster (or a
CloudNativePG-style operator-managed instance, still in-cluster) rather
than any cloud-managed database service — this is the phase where the
"cloud-agnostic" design goal is most concrete: the catalog database's
availability model is now the platform team's own responsibility (backup
schedule, failover), not inherited from a managed service's SLA. Chart
packaging follows
[helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md);
custom backend/frontend logic follows
[backstage-plugin-development](../backstage-plugin-development/SKILL.md).
Credentials come from a Kubernetes Secret populated by whatever
generic secrets tooling the org already runs (External Secrets Operator
against any backend, or a sealed-secrets pattern) — not a cloud-specific
credential-fetch call, since that would reintroduce the cloud coupling
this variant exists to avoid.

**Phase 4 — Golden-path template design.** Author the first golden-path
template producing a Dockerfile, a CI workflow using a portable
build/push flow (any OCI-compliant registry, not a specific cloud's
container registry), and catalog registration — deliberately no
cloud-specific identity annotation on the scaffolded `ServiceAccount`,
since one doesn't exist in this model. Tier by complexity. See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

**Phase 5 — Validate the golden path end-to-end.** Run the Phase 4
template through a pipeline that scaffolds a real instance, builds,
deploys to an ephemeral namespace on the same conformant cluster, smoke-
tests, and tears everything down on both success and failure, before
publishing it as the org default. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 6 — Self-service scaffolder actions calling generic Kubernetes
APIs.** This is the phase that most distinguishes this variant from the
four cloud-specific ones. Build Scaffolder custom actions that provision
by calling the Kubernetes API server directly — creating a Namespace with
a bound `ResourceQuota` and `NetworkPolicy` for a new service, or, for
anything resembling infrastructure (a database, a message queue), creating
a Crossplane `Claim` against a `CompositeResourceDefinition` the platform
team has already defined, rather than calling any cloud SDK from inside
the action. State the honest limitation directly to requesting teams: a
Crossplane Claim still ultimately provisions cloud infrastructure through
whichever Provider is installed, so "cloud-agnostic" here means the
*Scaffolder action's own code* has no cloud-specific branching — the
underlying Composition can still target a specific cloud, or even multiple
clouds behind the same Claim shape. Model the request as the same explicit
state machine as the cloud-specific variants
(`requested → policy_checked → pending_approval → approved →
provisioning → completed`), keep policy/budget rules external, and gate
anything provisioning real infrastructure behind approval. See
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md)
for the state-machine and policy-gate pattern, and
[crossplane-kubernetes-native-provisioning](../../../kubernetes-platform/skills/crossplane-kubernetes-native-provisioning/SKILL.md)
for the Claim/Composition/XRD mechanics this phase relies on.

**Phase 7 — Multi-tenancy.** Namespace-per-team is the default and
usually the only real option in this variant (there's no cloud-specific
"dedicated account/subscription/project per team" escape hatch to lean on
instead), so get RBAC, quotas, and NetworkPolicy-based isolation right
before onboarding a second team. See
[multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md).

**Phase 8 — Scorecards.** Define checks that stay cloud-agnostic by
construction: does the service have a NetworkPolicy, a PodDisruptionBudget,
resource requests/limits set, and (if it uses Phase 6's Crossplane path)
a Claim rather than an inline cloud SDK call embedded in application code.
See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

**Phase 9 — Rollout, operating model, and measurement.** Sequence
adoption starting from a pilot team with genuine current pain, run the
platform team per the "thinnest viable platform" discipline, and measure
with SPACE/DX Core 4 metrics. See
[idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md),
[platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md),
and
[developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md).

## Best practices

- Resist the temptation to special-case a specific cloud "just this once"
  inside a Phase 6 Scaffolder action — the entire value of this variant is
  that its core logic has zero cloud branching; push any cloud-specific
  behavior down into a Crossplane Composition instead, where it's isolated
  and swappable.
- Treat Phase 3's in-cluster Postgres availability model with the same
  seriousness a managed service would get automatically — set up an actual
  backup schedule (e.g., a CronJob running `pg_dump` to object storage) and
  test a restore before Phase 4 goes live, since nothing does this for you
  here.
- Re-run Phase 1's conformance validation after any CNI, storage driver,
  or Kubernetes upgrade — a cluster that was conformant at launch can
  silently regress after infrastructure changes, and this variant has no
  managed-control-plane vendor re-certifying it for you.
- Keep Phase 6's Crossplane Compositions in their own version-controlled
  repo, reviewed like the policy bundle in the self-service skill — a
  Composition change is as consequential as an IAM policy change in the
  cloud-specific variants, even though it doesn't look like one.
- Don't let "cloud-agnostic" quietly become "no governance" — the
  approval-gate and policy-check pattern from
  [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md)
  applies here exactly as it does in the cloud-specific variants.

## Common pitfalls

- **Symptom:** A Phase 6 Crossplane Claim gets stuck in `SYNCED: False`
  indefinitely, and the requesting developer has no idea why.
  **Fix:** This is usually a missing or misconfigured Provider credential
  behind the Composition, not a problem with the Claim itself — check the
  Provider's own status/events, per
  [crossplane-kubernetes-native-provisioning](../../../kubernetes-platform/skills/crossplane-kubernetes-native-provisioning/SKILL.md),
  before assuming the Scaffolder action's request shape is wrong.

- **Symptom:** The platform "works" in every test but the first real
  multi-team onboarding immediately causes one team's noisy workload to
  starve another's, something the cloud-specific variants' account/
  subscription/project boundaries would have prevented by default.
  **Fix:** This variant has no cloud-account-level isolation to fall back
  on — Phase 7's namespace ResourceQuotas and NetworkPolicies are load-
  bearing, not optional hardening. Confirm they're actually enforced (not
  just defined) before onboarding a second team, not after the first
  incident.

- **Symptom:** After a cluster upgrade, several previously-working
  Scaffolder-provisioned Namespaces lose their NetworkPolicy enforcement,
  and cross-team traffic that should be blocked isn't.
  **Fix:** The CNI's NetworkPolicy support (or a specific CNI upgrade) is
  the likely cause — re-run Phase 1's conformance and smoke-test suite
  after every infrastructure change, since this variant's isolation model
  depends entirely on the CNI enforcing policy correctly, unlike a cloud's
  VPC-level isolation as a backstop.

- **Symptom:** The in-cluster Postgres catalog database (Phase 3) runs out
  of disk and Backstage goes fully read-only with no warning beforehand.
  **Fix:** There's no cloud-managed storage-autoscaling safety net in this
  variant; set up a PVC usage alert well below capacity and a documented
  volume-expansion runbook (`kubectl edit pvc` with a CSI driver that
  supports online expansion) before this becomes a production incident,
  not after.

- **Symptom:** Someone runs `kubectl delete namespace <team-namespace>`
  to "reset" a team's environment, and it silently deletes every
  Crossplane Claim in that namespace along with the real infrastructure
  those Claims provisioned.
  **Fix:** This is destructive and, depending on the Composition's
  reclaim policy, can delete real cloud resources behind the Claims, not
  just Kubernetes objects. Never delete a tenant namespace as a routine
  reset; first list every Claim in it (`kubectl get claims -n
  <namespace>`) and confirm each Composition's `spec.compositeDeletePolicy`
  and reclaim behavior, or explicitly orphan the underlying resources
  first if they must be preserved.

## Worked example

**Scenario:** "Ferrovia Labs" runs workloads split across two clouds and
wants the platform's self-service layer to have zero cloud-specific code,
even though the underlying infrastructure it provisions is still real
cloud infrastructure.

1. **Phase 1:** An existing self-managed cluster `platform-shared` passes
   Sonobuoy `certified-conformance` and the DNS/cross-node/PVC smoke
   tests.
2. **Phase 2:** ingress-nginx and cert-manager (DNS-01 against the org's
   shared DNS provider) are installed; Rook-Ceph provides the
   `rook-ceph-block` `StorageClass`.
3. **Phase 3:** Backstage is packaged as `charts/backstage-ferrovia`,
   deployed against an in-cluster Postgres StatefulSet
   `backstage-catalog-db` on a 100Gi `rook-ceph-block` PVC, with a nightly
   `pg_dump` CronJob backing up to object storage.
4. **Phase 4:** A "Node.js service" golden-path template is authored,
   producing a Dockerfile, a portable CI workflow pushing to a shared
   OCI registry, and catalog registration — no cloud identity annotation.
5. **Phase 5:** A validation pipeline scaffolds, builds, deploys to an
   `ephemeral-validation` namespace, smoke-tests, and tears down.
6. **Phase 6:** A Scaffolder action `custom:k8s:provisionDatabase` creates
   a Crossplane `Claim` of kind `PostgreSQLInstance`; the Composition
   behind it happens to target whichever cloud that team's workloads
   already run in, decided once by the platform team, not by the action.
7. **Phase 7:** Each of 6 onboarded teams gets its own namespace with a
   `ResourceQuota` and a default-deny `NetworkPolicy`.
8. **Phase 8:** A scorecard checks for a `NetworkPolicy`, a
   `PodDisruptionBudget`, and resource limits on every scaffolded service.
9. **Phase 9:** The team with the most cross-cloud deployment pain is
   recruited as the pilot; after rollout, its deploy-to-either-cloud time
   drops from a bespoke script per cloud to one Claim shape.

## Cross-references

- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md), [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md) — cluster-acquisition options ahead of Phase 1.
- [kubernetes-cluster-post-provision-conformance-validation](../../../kubernetes-platform/skills/kubernetes-cluster-post-provision-conformance-validation/SKILL.md) — Phase 1.
- [ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md), [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md), [longhorn-storage-configuration](../../../kubernetes-platform/skills/longhorn-storage-configuration/SKILL.md), [rook-ceph-storage-operations](../../../kubernetes-platform/skills/rook-ceph-storage-operations/SKILL.md) — Phase 2.
- [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md), [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 3.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 4.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 5.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md), [crossplane-kubernetes-native-provisioning](../../../kubernetes-platform/skills/crossplane-kubernetes-native-provisioning/SKILL.md) — Phase 6.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — Phase 7.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 8.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md), [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md), [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — Phase 9.
- [complete-idp-deployment-on-aws-from-scratch](../complete-idp-deployment-on-aws-from-scratch/SKILL.md) — the cloud-committed alternative, worth reading to understand exactly what this variant trades away.
