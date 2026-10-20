---
name: complete-idp-deployment-on-gcp-from-scratch
description: >
  Sequences a complete, from-scratch Internal Developer Platform deployment
  on GCP: landing zone → GKE cluster → Helm-deployed Backstage backed by
  Cloud SQL for PostgreSQL → golden-path scaffolding template →
  self-service API wired to GCP provisioning (Workload Identity Federation
  bindings, Cloud SQL instances) → scorecards. This is the integration
  runbook that orders the individual GCP/GKE/Backstage skills correctly
  and flags the handoffs between them. Use when a user asks to "deploy an
  IDP on GCP from scratch," "stand up Backstage on GKE end-to-end,"
  "build our internal developer platform on Google Cloud," "wire
  self-service database/identity provisioning into Backstage on GKE," or
  "sequence a GCP platform rollout from project vending to golden-path
  templates."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on GCP from Scratch

## Purpose

A GCP-hosted Internal Developer Platform touches a folder/project
hierarchy, a GKE cluster, a Backstage instance, a managed Postgres catalog
database, a scaffolding template, a provisioning API, and a scorecard
model — each already covered by its own skill in this repo. What isn't
covered elsewhere is the order these phases must happen in on GCP
specifically, and the handoffs between them: which project hosts platform
tooling, how the GKE cluster's Workload Identity Federation pool is
carried into both the Backstage backend and the self-service provisioning
layer, and where teams get stuck wiring these together for the first
time. This skill is that integration runbook, not a restatement of
Organization Policy, GKE, or Backstage mechanics.

## When to use

- Standing up a green-field IDP for an organization with a GCP
  organization but no platform engineering tooling.
- Migrating ad hoc `gcloud`/Deployment Manager scripts and a manually
  maintained service inventory into a Backstage-based platform.
- Bootstrapping a reference IDP as part of adopting Google's enterprise
  foundations blueprint.
- Deciding build order when a platform team has GCP budget and a mandate
  but no existing tooling.
- Diagnosing an in-progress GCP IDP build where a phase's validation gate
  was skipped (e.g., self-service provisioning wired before VPC Service
  Controls were finalized around the catalog's project).

## Prerequisites & environment

- Access to (or authority to create) the GCP organization's root folder
  hierarchy, sufficient to design and apply Organization Policy
  constraints.
- Terraform maturity — every phase below is expressed as IaC via the
  project-factory pattern, not manual `gcloud` commands.
- `kubectl`, `helm` ≥ 3.8, and `gcloud container clusters` access for
  cluster provisioning.
- A Node.js/Yarn toolchain to build and customize the Backstage app.
- A registered domain and Cloud DNS managed zone (or delegated subdomain)
  for Backstage's ingress hostname and a managed certificate.
- A decision, before Phase 2, on whether platform tooling lives in a
  dedicated project under an `fldr-platform` folder or shares a project
  with early workloads — dedicated is assumed below.
- A named approver for the Phase 6 self-service gate, in place before that
  phase goes live.

## Step-by-step guidance

**Phase 1 — GCP landing zone.** Design the Resource Manager folder
hierarchy (an `fldr-platform` folder alongside `fldr-workloads` and
`fldr-sandbox`), apply Organization Policy constraints at the folder level,
and vend the platform-tooling project and a first tenant project through a
project factory rather than manual `gcloud projects create`, per
[gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md).
**Validate with that skill's canary-project step before continuing** — a
GKE cluster built in a project whose Organization Policy or VPC Service
Controls perimeter changes later forces avoidable rework in Phase 2 and
Phase 3.

**Phase 2 — GKE cluster with Workload Identity Federation.** Provision
the platform project's GKE cluster with a pinned Kubernetes version, node
pools sized for Backstage's steady backend load, and Workload Identity
Federation enabled on the cluster before any workload is deployed. Record
the cluster's workload identity pool
(`<PROJECT_ID>.svc.id.goog`) — Phase 3 and Phase 6 both bind Kubernetes
ServiceAccounts to Google service accounts against this pool. See
[managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
for GKE provisioning, node pool design, and the Workload Identity
Federation walkthrough specifically.

**Phase 3 — Backstage on GKE, backed by Cloud SQL for PostgreSQL.**
Package Backstage as a Helm chart and deploy it against a Cloud SQL for
PostgreSQL instance (regional/HA beyond a pilot) as the catalog database,
connecting via the Cloud SQL Auth Proxy sidecar rather than a public IP
and static password. The Backstage backend's Kubernetes ServiceAccount is
bound (via Workload Identity Federation from Phase 2) to a Google service
account holding only `cloudsql.client` and `secretmanager.secretAccessor`
on the specific catalog-DB secret. Chart packaging follows
[helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md);
custom backend/frontend logic follows
[backstage-plugin-development](../backstage-plugin-development/SKILL.md).

**Phase 4 — Golden-path template design.** Author the first golden-path
template producing a Dockerfile, a CI workflow (GitHub Actions or Cloud
Build), catalog registration, and — GCP-specific — a scaffolded
`ServiceAccount` manifest with the
`iam.gke.io/gcp-service-account` annotation pre-filled for the service's
own Google service account. Tier by complexity. See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

**Phase 5 — Validate the golden path end-to-end.** Run the Phase 4
template through a pipeline that scaffolds a real instance, builds,
deploys to an ephemeral GKE namespace, smoke-tests, and tears everything
down on both success and failure, before publishing it as the org
default. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 6 — Self-service API wired to GCP provisioning.** Build the
Scaffolder custom actions that let a developer request a Cloud SQL
instance or a new Workload Identity Federation binding through the
catalog. Model the request as an explicit state machine, gate
production-tier Cloud SQL machine types and any IAM binding broader than
namespace-scoped behind human approval, and keep policy/budget rules
external. The GCP-specific provisioning call — creating the Cloud SQL
instance via the Cloud SQL Admin API or a Config Connector `SQLInstance`
custom resource, and binding
`roles/iam.workloadIdentityUser` on the target Google service account
scoped to exactly
`serviceAccount:<PROJECT_ID>.svc.id.goog[<namespace>/<ksa-name>]` — is
unique to this phase; teams already using Crossplane elsewhere may prefer
its Kubernetes-native Claim model for this instead of a bespoke API call,
per
[crossplane-kubernetes-native-provisioning](../../../kubernetes-platform/skills/crossplane-kubernetes-native-provisioning/SKILL.md).
The approval-gate pattern itself is generic; see
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md).

**Phase 7 — Scorecards.** Define checks including GCP-specific ones: is
the service's identity Workload-Identity-Federation-bound rather than a
downloaded service account key anywhere, does the Cloud SQL instance have
automated backups and (production tier) regional HA enabled, is the
project labeled per the Phase 1 labeling policy. See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

**Phase 8 — Multi-tenancy.** If more than one team shares the Phase 2
cluster, decide namespace-per-team vs. project-per-team (GCP's project
factory from Phase 1 makes project-per-team cheap to vend, so weigh it
seriously alongside a shared-cluster model), scope each Workload Identity
Federation binding to its namespace/ServiceAccount, and enforce
ResourceQuotas before onboarding a second team. See
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

- Carry the workload identity pool name and project IDs as named
  variables across every phase's IaC — a stale pool reference in the
  Phase 6 self-service action after a project migration is a recurring
  source of binding mismatches.
- Enable regional (HA) configuration and automated backups on the Phase 3
  Cloud SQL instance from day one — the catalog database becomes the
  authoritative service-ownership record faster than most teams plan for.
- Don't let Phase 6 go live before Phase 1's Organization Policy and any
  VPC Service Controls perimeter are final — a self-service action
  granting a binding today that a new perimeter would block next month
  leaves a resource unreachable in a confusing way.
- Re-run Phase 5's validation pipeline on a schedule, not just before
  launch — a GKE minor version bump or a Google provider update can
  silently break a previously-working template.
- Start Phase 9's pilot rollout only against a template tier that has
  already cleared Phase 5.

## Common pitfalls

- **Symptom:** The Phase 6 self-service action fails every real request
  with a `PERMISSION_DENIED` on `iam.serviceAccounts.getAccessToken`,
  despite working in testing.
  **Fix:** This is a Phase 2/Phase 6 sequencing gap — the
  `roles/iam.workloadIdentityUser` binding's member string was written
  against a namespace/ServiceAccount name Phase 4's template scaffolds
  differently in practice (e.g., an environment suffix the binding didn't
  anticipate). Re-derive the exact
  `serviceAccount:<PROJECT_ID>.svc.id.goog[<namespace>/<ksa-name>]` string
  from the actual scaffolded manifest.

- **Symptom:** Backstage's catalog shows connection errors during a Cloud
  SQL maintenance window, even though the instance is configured for
  regional (HA) availability.
  **Fix:** The Backstage backend and the Cloud SQL Auth Proxy sidecar lack
  retry/reconnect logic tolerant of the brief failover gap regional HA
  still has; this is a Phase 3 gap invisible until a real maintenance
  event. Add connection retry with backoff and confirm the sidecar
  reconnects automatically.

- **Symptom:** Phase 7's scorecard shows most early services failing the
  "Workload Identity Federation, not a downloaded key" check, despite the
  platform mandating it from the start.
  **Fix:** Phase 4's template was published and used before Phase 2's
  Workload Identity Federation setup was actually finished, so early
  services scaffolded from an older revision with a downloaded-key
  fallback. Re-validate the current template (Phase 5), then
  batch-remediate already-scaffolded services.

- **Symptom:** Someone runs `gcloud projects delete` on what looks like an
  unused sandbox project, and it turns out to be the Phase 3 platform
  project holding the Cloud SQL catalog instance.
  **Fix:** This is destructive; GCP gives a 30-day recovery window for
  project deletion but Cloud SQL instances inside can still be
  unrecoverable depending on backup configuration. Never treat project
  deletion as routine cleanup once a phase's production resources live in
  it; confirm the project's resource inventory first, and prefer
  disabling billing or removing specific resources over a blanket project
  delete for anything under active platform use.

- **Symptom:** A production-tier Cloud SQL instance is discovered
  provisioned with no approval record.
  **Fix:** The Phase 6 approval gate was enforced only in the Scaffolder
  UI's form, not on the server-side approval endpoint. Require the same
  policy check and `requestedBy != approver` guard on every code path
  reaching the provisioning state.

## Worked example

**Scenario:** "Helios Media" has a GCP organization with an existing
folder hierarchy but no platform tooling. The platform team builds an IDP
over one quarter.

1. **Phase 1:** An `fldr-platform` folder is added alongside
   `fldr-workloads` and `fldr-sandbox`; a project factory vends
   `helios-platform-tools` and `helios-streaming-dev` (first tenant), with
   an Organization Policy constraint requiring a `team` label on all
   resources.
2. **Phase 2:** `helios-platform-tools` gets a GKE cluster
   `platform-gke-us-central1`, with Workload Identity Federation enabled
   against pool `helios-platform-tools.svc.id.goog`.
3. **Phase 3:** Backstage is packaged as `charts/backstage-helios`,
   deployed against Cloud SQL instance `helios-backstage-catalog`
   (regional, `db-custom-2-8192`), connected via the Cloud SQL Auth Proxy
   sidecar, with the backend's ServiceAccount `backstage-backend` bound to
   Google service account `backstage-backend@helios-platform-tools.iam`.
4. **Phase 4:** A "Node.js service" golden-path template is authored,
   producing a Dockerfile, a GitHub Actions workflow, and a
   `ServiceAccount` manifest annotated
   `iam.gke.io/gcp-service-account: ${service-name}@helios-platform-tools.iam.gserviceaccount.com`.
5. **Phase 5:** A validation pipeline scaffolds `test-svc-001`, builds,
   deploys to an `ephemeral-validation` namespace, curls `/healthz`, and
   tears down — required before the template is marked `default`.
6. **Phase 6:** A Scaffolder action `custom:gcp:provisionCloudSql` checks
   an OPA policy (auto-approve `db-f1-micro`/dev, require approval
   otherwise), and on approval creates the instance via the Cloud SQL
   Admin API using a Google service account scoped to the requesting
   team's project.
7. **Phase 7:** A scorecard adds a "Workload Identity Federation, not a
   downloaded key" check, weighted highly under Security.
8. **Phase 9:** `streaming-platform` is recruited as the pilot team
   (highest infra-ticket volume last quarter); after two sprints their
   Cloud SQL provisioning turnaround drops from a multi-day ticket to a
   same-day auto-approved or next-business-day approved request, and that
   result is published before the template goes org-wide.

## Cross-references

- [gcp-landing-zone-setup](../../../cloud/skills/gcp-landing-zone-setup/SKILL.md) — Phase 1.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — Phase 2.
- [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md) — Phase 3 chart packaging.
- [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 3 custom backend/frontend logic.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 4.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 5.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md), [crossplane-kubernetes-native-provisioning](../../../kubernetes-platform/skills/crossplane-kubernetes-native-provisioning/SKILL.md) — Phase 6.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 7.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — Phase 8.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md), [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md), [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — Phase 9.
- [complete-idp-deployment-on-aws-from-scratch](../complete-idp-deployment-on-aws-from-scratch/SKILL.md) — the same shape on AWS, useful for a multi-cloud platform team comparing the two.
