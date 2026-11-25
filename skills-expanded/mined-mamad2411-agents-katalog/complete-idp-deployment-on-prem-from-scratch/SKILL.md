---
name: complete-idp-deployment-on-prem-from-scratch
description: >
  Sequences a complete, from-scratch Internal Developer Platform deployment
  for self-hosted, potentially air-gapped on-prem environments: bare-metal/
  vSphere infrastructure → a kubeadm/Cluster API cluster with self-managed
  etcd → a private container registry and mirrored images → Helm-deployed
  Backstage backed by in-cluster PostgreSQL on self-hosted block storage →
  a golden-path template built for internal-only tooling → internal-only
  self-service (LDAP/AD-backed, no cloud IAM) → multi-tenancy and team
  workspace design as a first-class concern, not an afterthought →
  scorecards. Use when a user asks to "deploy an IDP entirely on-prem,"
  "build a self-hosted internal developer platform with no cloud
  dependency," "stand up Backstage in an air-gapped environment," "design
  an on-prem platform with strong team isolation," or "sequence an
  on-prem platform rollout from bare metal to golden-path templates."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on Prem from Scratch

## Purpose

An on-prem Internal Developer Platform inverts almost every assumption
the four cloud-specific skills in this repo make: there is no landing
zone with account-vending guardrails, no managed Kubernetes control plane,
no managed database, and — if the environment is air-gapped or
network-restricted — no assumption of reachable public registries or SaaS
identity providers. What replaces those is self-managed infrastructure the
platform team is fully responsible for at every layer, and a self-service
model built around internal identity (LDAP/AD) and internal-only approval
rather than cloud IAM and cloud budget policy. Multi-tenancy is treated as
a first-class design phase here, not a later add-on, because a shared
on-prem cluster has none of the cheap "just vend another account/
subscription/project" isolation the cloud variants can lean on.

## When to use

- Standing up a platform for regulated, disconnected, or otherwise
  cloud-averse environments where infrastructure must be fully
  self-hosted.
- Building an IDP for an air-gapped or low-connectivity site where image
  pulls, chart repositories, and package installs cannot assume live
  internet access.
- Migrating a self-hosted Kubernetes environment that already exists
  (kubeadm-provisioned, vSphere-hosted) toward a Backstage-based platform,
  rather than starting from a cloud landing zone.
- Designing strong team/tenant isolation on a single shared on-prem
  cluster where there's no cloud-account boundary to fall back on.
- Auditing an in-progress on-prem IDP build for a skipped etcd-backup
  step, an unmirrored image dependency, or a self-service flow that
  quietly assumed cloud IAM was available.

## Prerequisites & environment

- A virtualization baseline (vSphere, or bare-metal via PXE/MAAS) already
  standardized, with inventory-as-code (IPAM/DCIM) covering the nodes this
  cluster will run on.
- Enough physical/VM capacity provisioned with real lead time — unlike
  cloud, there's no on-demand node to add mid-incident; capacity-plan with
  actual procurement/allocation lead time in mind.
- A private container registry (e.g., Harbor or an equivalent) reachable
  from every cluster node, pre-populated with mirrored copies of every
  base image, Helm chart, and CNCF tool image this build needs if the
  environment has no reliable outbound internet access.
- `kubectl`, `helm` ≥ 3.8, `etcdctl` matching the cluster's etcd version,
  and (if adopting Cluster API) `clusterctl`, all available from an
  internal tooling host or bastion — not assumed to be freely
  downloadable at deploy time in an air-gapped site.
- A Node.js/Yarn toolchain to build Backstage, with its own npm/yarn
  registry mirrored internally if public registry access isn't available.
- Existing internal identity (LDAP or Active Directory) the self-service
  layer and Backstage's own auth provider will bind to — there is no
  cloud IAM to substitute.
- A named approver reachable through whatever internal channel this site
  actually has (email, an internal ticketing system) — assume no Slack/
  SaaS notification channel is guaranteed reachable.

## Step-by-step guidance

**Phase 1 — On-prem infrastructure baseline.** Establish inventory-as-code
before touching hardware, choose and standardize the virtualization
platform (vSphere is the common baseline; bare-metal via PXE/MAAS/Redfish
is the alternative), automate provisioning rather than hand-installing
OSes, and decide the hybrid connectivity model back to any cloud
dependency that remains (even an air-gapped site sometimes needs a
one-way path for patches). See
[on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md).
**This phase's capacity-planning step matters more here than in any other
variant** — under-provisioning discovered mid-build costs weeks of
procurement lead time, not a changed instance type.

**Phase 2 — Self-managed Kubernetes cluster via kubeadm/Cluster API, with
etcd health as an explicit ongoing concern.** Bootstrap the control plane
with `kubeadm init`, decide stacked vs. external etcd for the control-plane
HA model, and put a load balancer/VIP in front of the API server before
joining additional control-plane nodes. If lifecycle management
declaratively across many clusters/sites matters, layer Cluster API on
top. See
[kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md).
Because this cluster's control plane has no managed-service SLA behind
it, treat etcd snapshot backups and quorum/health monitoring as a
standing operational phase from day one, not an incident-response
afterthought — see
[etcd-backup-restore-and-cluster-health](../../../kubernetes-platform/skills/etcd-backup-restore-and-cluster-health/SKILL.md).
This phase has no equivalent in the managed-cluster cloud variants, where
the cloud provider owns etcd entirely.

**Phase 3 — Private registry and image/chart mirroring.** Stand up (or
confirm) a private registry reachable from every node, expose it internally
via ingress-nginx with a TLS certificate issued from an internal CA rather
than public ACME — see
[ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md)
and
[cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md)
for the private-CA issuance path specifically — and mirror every image and
chart this build depends on (Backstage's own image, Postgres, any CNCF
add-on) before assuming Phase 4 can simply `helm install` against a public
chart repository. **If this site is genuinely air-gapped, treat any step
below that references a public registry, chart repo, or package index as
requiring its mirrored internal equivalent instead** — this is the single
biggest source of "works everywhere else, fails here" surprises in an
on-prem build.

**Phase 4 — Backstage on the cluster, backed by self-hosted PostgreSQL on
in-cluster block storage.** Package Backstage as a Helm chart, deploy it
against a Postgres instance running in-cluster on Rook-Ceph or Longhorn
block storage (Rook-Ceph if object/shared-filesystem storage is also
needed elsewhere on this cluster; Longhorn if only replicated block
storage is required — see
[rook-ceph-storage-operations](../../../kubernetes-platform/skills/rook-ceph-storage-operations/SKILL.md)
and
[longhorn-storage-configuration](../../../kubernetes-platform/skills/longhorn-storage-configuration/SKILL.md)
for the tradeoff), and bind Backstage's own authentication to the site's
existing LDAP/AD rather than a cloud identity provider. Chart packaging
follows
[helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md);
custom backend/frontend logic (very likely needed here for an LDAP/AD auth
provider plugin) follows
[backstage-plugin-development](../backstage-plugin-development/SKILL.md).

**Phase 5 — Golden-path template built for internal-only tooling.**
Author a golden-path template whose CI pipeline targets internal,
self-hosted runners (not a SaaS CI service assuming outbound internet) and
whose Dockerfile's base images resolve against the Phase 3 private
registry by default. Tier by complexity, same as the cloud variants, but
document explicitly that every external dependency in the template must
resolve internally. See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

**Phase 6 — Validate the golden path end-to-end, on internal
infrastructure only.** Run the scaffold-build-deploy-smoke-test-teardown
pipeline against an ephemeral namespace on this same on-prem cluster (there
is no separate cloud preview environment to spin up on demand), and
confirm the pipeline itself has no accidental outbound dependency that
would fail in the air-gapped case even if it passes in a connected test
run. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 7 — Internal-only self-service, gated by LDAP/AD identity rather
than cloud IAM.** Build Scaffolder actions that provision by calling
internal APIs — a vSphere API call to clone a VM template, an internal
IPAM/DCIM system for address allocation, or a Crossplane provider targeting
on-prem infrastructure if one is available — with approval routed to a
named internal approver reachable through whatever notification channel
this site actually guarantees. There is no cloud budget-policy layer to
lean on, so cost/capacity guardrails here are about physical
capacity headroom (see Phase 1) rather than a per-instance-class dollar
estimate. Keep the same state-machine and server-side-gate pattern as the
cloud variants. See
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md).

**Phase 8 — Multi-tenancy and team workspace design, front and center.**
Because this cluster has no cheap cloud-account-per-team escape hatch,
decide the tenancy model deliberately before onboarding a second team:
namespace-per-team with RBAC, ResourceQuotas, and default-deny
NetworkPolicies is the realistic default; dedicated clusters per tenant
are usually not affordable on-prem the way spinning up another cloud
account is. Route any dedicated-infrastructure request through an
explicit exception process rather than ad hoc. Treat this as a phase to
get right before Phase 7's self-service goes live broadly, not after. See
[multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md).

**Phase 9 — Scorecards, rollout, and operating model.** Define
production-readiness checks appropriate to self-hosted infrastructure (is
the service's image pulled from the internal registry rather than a public
one directly, does it have a NetworkPolicy, is it registered with an
on-call rotation reachable internally), sequence rollout from a real pilot
team, and size the platform team per the thinnest-viable-platform
discipline. See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md),
[idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md),
and
[platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md).

## Best practices

- Treat Phase 3's image/chart mirroring as a permanent pipeline, not a
  one-time pre-load — every subsequent phase that references a new base
  image or chart version needs a corresponding mirror update, or Phase 5's
  golden path silently breaks for the next team that scaffolds from it.
- Test an actual etcd restore from a Phase 2 snapshot before the cluster
  carries real workloads, not for the first time during a real control-
  plane failure — see
  [etcd-backup-restore-and-cluster-health](../../../kubernetes-platform/skills/etcd-backup-restore-and-cluster-health/SKILL.md).
- Decide Phase 8's tenancy model before Phase 7's self-service goes live
  for a second team — retrofitting namespace boundaries onto teams already
  sharing a cluster is materially harder than designing them in up front,
  and there's no cloud-account boundary to paper over the gap in the
  meantime.
- Validate hybrid failover paths (Phase 1) and the air-gapped install
  procedure (Phase 3) before relying on either, exactly as
  [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md)
  recommends — an untested air-gapped install script that quietly reaches
  out to the public internet during a live cutover is a common and
  avoidable failure.
- Keep an explicit runbook for procurement/capacity lead time next to
  Phase 1's inventory-as-code — a platform team used to cloud elasticity
  will otherwise plan Phase 7's self-service approval SLAs assuming
  capacity that isn't actually available on short notice.

## Common pitfalls

- **Symptom:** The golden-path template (Phase 5) works perfectly in the
  platform team's connected test environment but fails immediately at a
  real air-gapped site.
  **Fix:** Some step in the template's CI pipeline or Dockerfile has an
  unmirrored dependency (a base image tag not yet in the Phase 3 registry,
  an npm/yarn package resolving against the public registry). Audit the
  full dependency chain against the site's actual network policy, not
  just against what worked during development, and add any missing
  artifact to the mirror before re-publishing the template.

- **Symptom:** The kubeadm-provisioned control plane (Phase 2) loses
  quorum after a single node failure, taking the whole cluster — including
  Backstage and the self-service layer — down with it.
  **Fix:** This usually means the etcd cluster was left at an
  even-numbered or too-small member count, or health/quorum monitoring
  from
  [etcd-backup-restore-and-cluster-health](../../../kubernetes-platform/skills/etcd-backup-restore-and-cluster-health/SKILL.md)
  was never actually wired up to alert before quorum was lost. Restore
  from the most recent verified snapshot, then correct the member count
  and monitoring gap before declaring the cluster production-ready again.

- **Symptom:** A team requests self-service infrastructure (Phase 7) and
  the request sits unactioned for over a week because the named approver
  was on leave and no one else had visibility into the pending request.
  **Fix:** This is a consequence of routing approval through a single
  person and an unreliable notification channel rather than a
  role-based, monitored queue. Route approval to an internal role/group
  reachable through a channel the site actually guarantees (an internal
  ticketing system, not a single person's inbox), and set an explicit
  escalation SLA even without a cloud-based paging tool to automate it.

- **Symptom:** Two teams sharing the on-prem cluster (no Phase 8 tenancy
  boundaries yet defined) discover one team's workload has been silently
  reading traffic destined for the other's service.
  **Fix:** This is what happens when Phase 8 is treated as a later
  hardening pass instead of a prerequisite to onboarding a second tenant.
  Retrofit namespace-scoped RBAC and a default-deny NetworkPolicy
  immediately, and audit every self-service request made before the fix
  for improperly-scoped access.

- **Symptom:** A platform engineer runs `kubectl delete namespace` against
  what's believed to be a decommissioned team's workspace to reclaim
  capacity, and it turns out another team's shared resources (a
  Crossplane-provisioned internal resource, a shared cache) were
  provisioned into the same namespace.
  **Fix:** This is destructive and, on self-hosted infrastructure with no
  managed-service undo path, often unrecoverable without a very recent
  backup. Never delete a tenant namespace without first confirming (via
  Phase 8's ownership model) that nothing shared or still in use lives in
  it, and prefer scaling a workload to zero over deleting its namespace
  when reclaiming capacity is the actual goal.

## Worked example

**Scenario:** "Anchorage Defense Systems" runs a regulated, network-
segmented on-prem environment with no reliable outbound internet access
and must self-host its entire IDP.

1. **Phase 1:** Inventory-as-code models three racks of bare-metal hosts;
   PXE-based automated provisioning installs the base OS; capacity
   planning reserves headroom for one full node failure without service
   loss.
2. **Phase 2:** A kubeadm cluster `platform-onprem-01` bootstraps with a
   3-node stacked-etcd control plane behind a keepalived VIP; etcd
   snapshots are taken every 6 hours and a restore drill is run once
   before go-live.
3. **Phase 3:** An internal Harbor registry `registry.internal.anchorage`
   mirrors the Backstage image, Postgres image, and every Helm chart the
   build needs; it's exposed via ingress-nginx with a cert issued from the
   internal CA.
4. **Phase 4:** Backstage is packaged as `charts/backstage-anchorage`,
   deployed against an in-cluster Postgres instance on Rook-Ceph block
   storage, authenticating developers via the site's existing Active
   Directory.
5. **Phase 5:** A golden-path template's CI workflow runs on an internal
   Jenkins instance and pulls its base image exclusively from
   `registry.internal.anchorage`.
6. **Phase 6:** A validation pipeline scaffolds a test service on this
   same cluster's `ephemeral-validation` namespace and confirms zero
   outbound network calls occur during the build.
7. **Phase 7:** A Scaffolder action requests a new internal VM via a
   vSphere API call, gated by an approval routed to the
   `platform-approvers` AD group and tracked in the site's internal
   ticketing system with a 2-business-day escalation SLA.
8. **Phase 8:** Each of 5 onboarded teams gets a dedicated namespace with
   RBAC bound to its AD group, a ResourceQuota sized from its historical
   VM usage, and a default-deny NetworkPolicy.
9. **Phase 9:** A scorecard checks that every service's image resolves
   from the internal registry, and the platform team (2 people,
   part-time) is explicitly scoped per the thinnest-viable-platform model.

## Cross-references

- [on-prem-infrastructure-patterns](../../../cloud/skills/on-prem-infrastructure-patterns/SKILL.md) — Phase 1.
- [kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api](../../../kubernetes-platform/skills/kubernetes-cluster-provisioning-with-kubeadm-and-cluster-api/SKILL.md), [etcd-backup-restore-and-cluster-health](../../../kubernetes-platform/skills/etcd-backup-restore-and-cluster-health/SKILL.md) — Phase 2.
- [ingress-nginx-configuration](../../../kubernetes-platform/skills/ingress-nginx-configuration/SKILL.md), [cert-manager-tls-automation](../../../kubernetes-platform/skills/cert-manager-tls-automation/SKILL.md) — Phase 3.
- [rook-ceph-storage-operations](../../../kubernetes-platform/skills/rook-ceph-storage-operations/SKILL.md), [longhorn-storage-configuration](../../../kubernetes-platform/skills/longhorn-storage-configuration/SKILL.md), [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md), [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 4.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 5.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 6.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Phase 7.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — Phase 8.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md), [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md), [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md) — Phase 9.
- [complete-idp-deployment-on-k3s-from-scratch](../complete-idp-deployment-on-k3s-from-scratch/SKILL.md) — the lighter-weight self-hosted variant for a single small site rather than a full regulated on-prem estate.
