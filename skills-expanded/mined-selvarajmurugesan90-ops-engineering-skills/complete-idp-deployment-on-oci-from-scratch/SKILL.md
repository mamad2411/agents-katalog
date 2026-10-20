---
name: complete-idp-deployment-on-oci-from-scratch
description: >
  Sequences a complete, from-scratch Internal Developer Platform deployment
  on Oracle Cloud Infrastructure: compartment/Identity-Domain landing zone
  → OKE cluster → Helm-deployed Backstage backed by OCI Database with
  PostgreSQL → golden-path scaffolding template → self-service API wired
  to OCI provisioning (Dynamic Group/Resource Principal identity, Database
  with PostgreSQL instances) → scorecards. This is the integration runbook
  that orders the individual OCI/Backstage skills correctly and flags the
  handoffs between them, including the OKE cluster-provisioning gap this
  repo doesn't yet cover with a dedicated skill. Use when a user asks to
  "deploy an IDP on OCI from scratch," "stand up Backstage on OKE
  end-to-end," "build our internal developer platform on Oracle Cloud,"
  "wire self-service database/identity provisioning into Backstage on
  OKE," or "sequence an OCI platform rollout from compartment design to
  golden-path templates."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on OCI from Scratch

## Purpose

An OCI-hosted Internal Developer Platform touches a compartment/Identity
Domain hierarchy, an OKE (Oracle Kubernetes Engine) cluster, a Backstage
instance, a managed Postgres catalog database, a scaffolding template, a
provisioning API, and a scorecard model. Most of these phases are covered
in depth elsewhere in this repo — but this repo does not currently carry a
dedicated OKE cluster-provisioning skill the way it does for EKS/AKS/GKE,
so this skill both sequences the phases that do exist and is explicit
about where it's supplying OKE-specific guidance directly because no
deeper skill exists yet. Treat the OKE-specific steps below as the
authoritative source for this repo until a dedicated OKE skill is added;
everything else defers to the skill it links to.

## When to use

- Standing up a green-field IDP for an organization with an OCI tenancy
  but no platform engineering tooling.
- Migrating ad hoc OCI CLI/Terraform scripts and a manually maintained
  service inventory into a Backstage-based platform.
- Bootstrapping a reference IDP as part of adopting the CIS OCI Landing
  Zone reference architecture.
- Deciding build order when a platform team has OCI budget and a mandate
  but no existing tooling.
- Diagnosing an in-progress OCI IDP build where a phase's validation gate
  was skipped (e.g., self-service provisioning wired before Cloud
  Guard/Security Zones were enabled on the platform compartment).

## Prerequisites & environment

- Access to (or authority to create) the OCI tenancy's root compartment
  and Identity Domain configuration, sufficient to design and apply the
  CIS OCI Landing Zone.
- Terraform maturity — every phase below is expressed as IaC via the CIS
  OCI Landing Zone Terraform reference, not manual OCI Console clicks.
- `kubectl`, `helm` ≥ 3.8, and the OCI CLI (`oci ce cluster ...`) for
  cluster provisioning and kubeconfig retrieval.
- A Node.js/Yarn toolchain to build and customize the Backstage app.
- A registered domain and OCI DNS zone (or delegated subdomain) for
  Backstage's ingress hostname and a managed certificate.
- A decision, before Phase 2, on whether platform tooling lives in a
  dedicated `platform` compartment under the tenancy root or shares a
  compartment with early workloads — dedicated is assumed below.
- A named approver for the Phase 6 self-service gate, in place before that
  phase goes live.
- **A known gap to plan around:** this repo's
  [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
  skill covers EKS/AKS/GKE only, not OKE. Phase 2 below gives the OKE
  equivalent directly; use the EKS/AKS/GKE skill only for its
  cloud-agnostic node-pool-sizing and workload-identity *concepts*, not
  for OCI-specific commands.

## Step-by-step guidance

**Phase 1 — OCI landing zone.** Design the compartment hierarchy (a
`platform` compartment alongside `workloads` and `security` compartments),
configure Identity Domains and IAM policies scoped to compartments, deploy
the CIS OCI Landing Zone Terraform reference, and enable Cloud Guard and
Security Zones tenancy-wide before provisioning anything else, per
[oci-landing-zone-setup](../../../cloud/skills/oci-landing-zone-setup/SKILL.md).
**Validate with that skill's canary-compartment step before continuing** —
a Security Zone that later denies a resource shape (e.g., a public load
balancer) already in use by Phase 2's cluster forces avoidable rework.

**Phase 2 — OKE cluster with Dynamic-Group-based workload identity.**
Because this repo has no dedicated OKE skill, provision the cluster
directly: create the OKE cluster in the `platform` compartment with a
pinned Kubernetes version and a managed node pool sized for Backstage's
steady backend load (OKE also offers virtual node pools for
serverless-style scaling, worth considering for bursty CI workloads
scaffolded later, but the platform-tooling node pool itself should be
sized for predictable steady load). Configure workload identity using
OCI's **Dynamic Groups** and **Resource Principals** — the OCI analog to
IRSA/Workload Identity — by defining a Dynamic Group whose matching rule
scopes to the specific OKE node pool or, more narrowly, to pods via the
OKE Workload Identity feature (`instance_id` or `resource.type` and
`resource.compartment.id` rules), then writing IAM policies granting that
Dynamic Group only the specific verbs on the specific resource types it
needs (e.g., `allow dynamic-group backstage-platform-dg to use
secret-family in compartment platform where target.secret.name=
'backstage-db-credential'` — never a tenancy-wide `manage` policy for
convenience). Record the Dynamic Group's OCID — Phase 3 and Phase 6 both
reference it. For general node-pool-sizing and workload-identity-as-a-
*concept* framing (not OCI syntax), the shape of
[managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)'s
node-group and workload-identity guidance still applies by analogy.

**Phase 3 — Backstage on OKE, backed by OCI Database with PostgreSQL.**
Package Backstage as a Helm chart and deploy it against an OCI Database
with PostgreSQL instance (multi-AZ within the region beyond a pilot) as
the catalog database, with the Backstage backend pod's node covered by
the Phase 2 Dynamic Group so it can call
`secrets-retrieval` on OCI Vault for the DB credential via a Resource
Principal — never an embedded connection string. Chart packaging follows
[helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md);
custom backend/frontend logic follows
[backstage-plugin-development](../backstage-plugin-development/SKILL.md).

**Phase 4 — Golden-path template design.** Author the first golden-path
template producing a Dockerfile, a CI workflow (GitHub Actions or OCI
DevOps), catalog registration, and — OCI-specific — documentation of which
Dynamic Group matching rule a newly scaffolded service needs to be
included under (since OCI's model grants identity by Dynamic Group
membership rather than a per-ServiceAccount annotation, a golden-path
template here should scaffold the IAM policy statement request as a
reviewable artifact, not assume it self-provisions). Tier by complexity.
See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

**Phase 5 — Validate the golden path end-to-end.** Run the Phase 4
template through a pipeline that scaffolds a real instance, builds,
deploys to an ephemeral OKE namespace, smoke-tests, and tears everything
down on both success and failure, before publishing it as the org
default. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 6 — Self-service API wired to OCI provisioning.** Build the
Scaffolder custom actions that let a developer request an OCI Database
with PostgreSQL instance or a new Dynamic-Group-scoped IAM policy
statement through the catalog. Model the request as an explicit state
machine, gate production-tier database shapes and any IAM policy broader
than a single named secret/compartment behind human approval, and keep
policy/budget rules external. The OCI-specific provisioning call —
creating the database instance via the Database with PostgreSQL API using
a Resource Principal scoped to the requesting team's compartment, and
drafting (never auto-applying without review) the corresponding IAM
policy statement scoping a Dynamic Group to that exact resource — is
unique to this phase; the approval-gate pattern is generic. See
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md).

**Phase 7 — Scorecards.** Define checks including OCI-specific ones: is
the service's identity Dynamic-Group/Resource-Principal-based rather than
a long-lived API signing key embedded anywhere, does the database instance
have automated backups enabled, does Cloud Guard report no open findings
for the service's compartment, is the compartment tagged per the Phase 1
tagging policy. See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

**Phase 8 — Multi-tenancy.** If more than one team shares the Phase 2
cluster, decide namespace-per-team vs. compartment-per-team (OCI's
compartment model, from Phase 1, makes compartment-per-team relatively
cheap and gives cleaner IAM policy boundaries than namespace RBAC alone),
scope each team's Dynamic Group matching rule and IAM policy to its
namespace/compartment, and enforce ResourceQuotas before onboarding a
second team. See
[multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md).

**Phase 9 — Rollout, operating model, and measurement.** Sequence
adoption starting from a pilot team with genuine current pain, run the
platform team per the "thinnest viable platform" discipline, and measure
with SPACE/DX Core 4 metrics. See
[idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md),
[platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md),
and
[developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md).

## Best practices

- Carry the Dynamic Group OCID and compartment OCIDs as named variables
  across every phase's IaC — a stale OCID in the Phase 6 self-service
  action after a compartment reorganization is a recurring source of
  policy mismatches.
- Enable automated backups on the Phase 3 database instance from day one
  — the catalog database becomes the authoritative service-ownership
  record faster than most teams plan for.
- Don't let Phase 6 go live before Phase 1's Cloud Guard/Security Zones
  configuration is final — a self-service action granting a resource
  today that a newly enabled Security Zone would deny next month leaves a
  confusing, hard-to-diagnose failure for the requesting developer.
- Because OCI's identity model grants access via Dynamic Group
  *membership rules*, not a per-workload annotation, review every new
  matching rule as carefully as an IAM policy itself — an overly broad
  rule (e.g., matching on compartment alone rather than a specific
  resource) silently grants every workload in that compartment the same
  access.
- Start Phase 9's pilot rollout only against a template tier that has
  already cleared Phase 5.

## Common pitfalls

- **Symptom:** The Phase 6 self-service action fails every real request
  with a `NotAuthorizedOrNotFound` when the workload tries to read its
  database secret, despite working in testing.
  **Fix:** This is a Phase 2/Phase 6 sequencing gap — the Dynamic Group's
  matching rule was written against a node pool or compartment shape that
  Phase 4's template's scaffolded workload doesn't actually match (e.g.,
  the workload lands in a different sub-compartment than the rule
  anticipated). Re-derive the matching rule from the actual scaffolded
  deployment's compartment placement, not from a hand-typed example.

- **Symptom:** Backstage's catalog shows connection errors during a
  database maintenance window.
  **Fix:** The Backstage backend lacks retry/reconnect logic tolerant of
  the brief failover gap even a well-configured database instance has;
  add connection retry with backoff.

- **Symptom:** Phase 7's scorecard shows most early services failing the
  "Dynamic Group identity, not a long-lived API key" check, despite the
  platform mandating it from the start.
  **Fix:** Phase 4's template was published and used before Phase 2's
  Dynamic Group setup was actually finished, so early services scaffolded
  from an older revision with an embedded API signing key fallback.
  Re-validate the current template (Phase 5), then batch-remediate
  already-scaffolded services.

- **Symptom:** A platform engineer deletes what looks like an unused
  compartment to tidy up the hierarchy, and it turns out to be the `data`
  sub-compartment holding the Phase 3 database instance.
  **Fix:** OCI compartment deletion cascades to everything inside it and,
  once the grace period elapses, is not reversible. Never delete a
  compartment without first listing its full resource inventory (`oci
  search resource structured-search` scoped to the compartment) and
  confirming nothing under active platform use lives inside it.

- **Symptom:** A production-tier database instance is discovered
  provisioned with no approval record.
  **Fix:** The Phase 6 approval gate was enforced only in the Scaffolder
  UI's form, not on the server-side approval endpoint. Require the same
  policy check and `requestedBy != approver` guard on every code path
  reaching the provisioning state.

## Worked example

**Scenario:** "Meridian Freight" has an OCI tenancy with a root
compartment but no platform tooling. The platform team builds an IDP over
one quarter.

1. **Phase 1:** A `platform` compartment is created alongside `workloads`
   and `security` compartments; the CIS OCI Landing Zone Terraform
   reference is applied, enabling Cloud Guard and a Security Zone around
   `platform` and `workloads`.
2. **Phase 2:** An OKE cluster `platform-oke-phx` is created in
   `platform`, with a Dynamic Group `backstage-platform-dg` matching rule
   `ALL {resource.type = 'cluster', resource.compartment.id =
   '<PLATFORM_COMPARTMENT_OCID>'}`, and an IAM policy granting it
   `use secret-family` scoped to the specific catalog-DB secret only.
3. **Phase 3:** Backstage is packaged as `charts/backstage-meridian`,
   deployed against an OCI Database with PostgreSQL instance
   `meridian-backstage-catalog` (multi-AZ), with the backend pod reading
   its DB credential from OCI Vault via the Phase 2 Resource Principal.
4. **Phase 4:** A "Node.js service" golden-path template is authored,
   producing a Dockerfile, a GitHub Actions workflow, and a documented IAM
   policy-statement request template for the service's own Dynamic Group
   membership.
5. **Phase 5:** A validation pipeline scaffolds `test-svc-001`, builds,
   deploys to an `ephemeral-validation` namespace, curls `/healthz`, and
   tears down.
6. **Phase 6:** A Scaffolder action `custom:oci:provisionPostgresDb`
   checks an OPA policy (auto-approve the smallest shape/dev, require
   approval otherwise), and on approval provisions via the Database with
   PostgreSQL API using a Resource Principal scoped to the requesting
   team's compartment.
7. **Phase 7:** A scorecard adds a "Dynamic Group identity, not API key"
   check, weighted highly under Security.
8. **Phase 9:** `dispatch-routing` is recruited as the pilot team (highest
   infra-ticket volume last quarter); after two sprints their database
   provisioning turnaround drops from a multi-day ticket to a same-day
   auto-approved or next-business-day approved request, and that result is
   published before the template goes org-wide.

## Cross-references

- [oci-landing-zone-setup](../../../cloud/skills/oci-landing-zone-setup/SKILL.md) — Phase 1.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — Phase 2 conceptual analog only (this repo has no dedicated OKE skill).
- [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md) — Phase 3 chart packaging.
- [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 3 custom backend/frontend logic.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 4.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 5.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Phase 6.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 7.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — Phase 8.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md), [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md), [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — Phase 9.
- [complete-idp-deployment-on-aws-from-scratch](../complete-idp-deployment-on-aws-from-scratch/SKILL.md) — the same shape on AWS, a useful comparison for the identity-model differences (IRSA vs. Dynamic Groups) called out above.
