---
name: complete-idp-deployment-on-azure-from-scratch
description: >
  Sequences a complete, from-scratch Internal Developer Platform deployment
  on Azure: landing zone → AKS cluster → Helm-deployed Backstage backed by
  Azure Database for PostgreSQL Flexible Server → golden-path scaffolding
  template → self-service API wired to Azure provisioning (Azure AD
  Workload Identity federated credentials, Flexible Server instances) →
  scorecards. This is the integration runbook that orders the individual
  Azure/AKS/Backstage skills correctly and flags the handoffs between
  them. Use when a user asks to "deploy an IDP on Azure from scratch,"
  "stand up Backstage on AKS end-to-end," "build our internal developer
  platform on Azure," "wire self-service database/identity provisioning
  into Backstage on AKS," or "sequence an Azure platform rollout from
  subscription vending to golden-path templates."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on Azure from Scratch

## Purpose

An Azure-hosted Internal Developer Platform touches a Management Group/
subscription hierarchy, an AKS cluster, a Backstage instance, a managed
Postgres catalog database, a scaffolding template, a provisioning API, and
a scorecard model — each covered in depth by its own skill in this repo.
What those skills don't cover is the order these phases have to happen in
and the specific handoffs between them on Azure: which subscription hosts
the platform tooling, how the AKS cluster's Workload Identity federation is
carried into both the Backstage backend and the self-service provisioning
layer, and where teams building this for the first time get stuck. This
skill is that integration runbook, not a restatement of Azure Policy,
AKS, or Backstage mechanics.

## When to use

- Standing up a green-field IDP for an organization whose Azure tenant
  exists but has no platform engineering tooling.
- Migrating a set of ad hoc ARM/Bicep deployment scripts and a manually
  maintained service spreadsheet into a Backstage-based platform.
- Bootstrapping a reference IDP as part of an Azure Cloud Adoption
  Framework enterprise-scale rollout.
- Deciding what order to build in when a platform team has Azure budget
  and a mandate but no existing tooling.
- Diagnosing an in-progress Azure IDP build where a phase was skipped or
  under-validated (e.g., self-service wired before Azure Policy guardrails
  were finalized, causing rework once policy tightens).

## Prerequisites & environment

- Access to (or authority to create) the Azure tenant's root Management
  Group, sufficient to design and apply the landing zone hierarchy.
- Terraform or Bicep maturity — every phase below is expressed as IaC.
- `kubectl`, `helm` ≥ 3.8, and `az aks` CLI access for cluster
  provisioning.
- A Node.js/Yarn toolchain to build and customize the Backstage app itself
  (Backstage ships as source, not a pre-built configurable image).
- A registered domain and Azure DNS zone (or delegated subdomain) for
  Backstage's ingress hostname and a managed certificate.
- A decision, before Phase 2, on whether the platform tooling lives in a
  dedicated `Platform` subscription or shares a subscription with early
  workloads — dedicated is strongly preferred and assumed below.
- A named approver for the Phase 6 self-service gate, in place before that
  phase goes live.

## Step-by-step guidance

**Phase 1 — Azure landing zone.** Design the Management Group hierarchy
(a `Platform` MG alongside `Landing Zones` and `Sandbox`), assign Azure
Policy initiatives at the Management Group level (not per-subscription),
and vend the platform-tooling subscription and a first tenant subscription
through a repeatable process (Azure landing zone Terraform module or ALZ
accelerator), following
[azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md).
**Validate with that skill's canary-subscription step before continuing**
— an AKS cluster built in a subscription whose Policy assignments later
tighten (e.g., a "deny public IP" policy added after the cluster's load
balancer is already provisioned) forces avoidable rework in Phase 2.

**Phase 2 — AKS cluster with Azure AD Workload Identity.** Provision the
platform subscription's AKS cluster with a pinned Kubernetes version,
node pools sized for Backstage's steady backend load, and Azure AD
Workload Identity (OIDC issuer + federated credentials) enabled before any
workload is deployed. Record the cluster's OIDC issuer URL — Phase 3 and
Phase 6 both construct federated credentials against it. See
[managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
for AKS provisioning, node pool design, and the Workload Identity
walkthrough specifically.

**Phase 3 — Backstage on AKS, backed by Azure Database for PostgreSQL
Flexible Server.** Package Backstage as a Helm chart and deploy it against
a Flexible Server instance (zone-redundant HA beyond a pilot) as the
catalog database, with the Backstage pod's Kubernetes ServiceAccount
federated to a Microsoft Entra ID (Azure AD) application that has
`Key Vault Secrets User` on the vault holding the database credential —
never a connection string in a plain Secret. Chart packaging and
values-schema design follow
[helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md);
any custom auth provider or backend plugin follows
[backstage-plugin-development](../backstage-plugin-development/SKILL.md).
Mount the credential via the Azure Key Vault Provider for Secrets Store
CSI Driver rather than syncing it into a Kubernetes Secret at rest.

**Phase 4 — Golden-path template design.** Author the first golden-path
template producing a Dockerfile, a CI workflow (GitHub Actions or Azure
DevOps Pipelines), catalog registration, and — Azure-specific — a
scaffolded `ServiceAccount` manifest with the
`azure.workload.identity/client-id` annotation pre-filled for the
service's own federated identity. Tier by complexity rather than one
template trying to cover every service shape. See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

**Phase 5 — Validate the golden path end-to-end.** Run the Phase 4
template through a pipeline that scaffolds a real instance, builds it,
deploys it to an ephemeral AKS namespace, smoke-tests it, and tears
everything down on both success and failure, before it's published as the
org default. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 6 — Self-service API wired to Azure provisioning.** Build the
Scaffolder custom actions that let a developer request a Flexible Server
instance or a new Workload Identity federated credential through the
catalog. Model the request as an explicit state machine, gate
production-tier server SKUs and any identity with broader-than-namespace
federation subject behind human approval, and keep policy/budget rules
external to the action code. The Azure-specific provisioning call —
`az postgres flexible-server create` or an ARM/Bicep deployment scoped by
a managed identity with `Contributor` narrowed to the target resource
group, and creating a federated credential whose `subject` is scoped to
the exact `system:serviceaccount:<namespace>:<name>` — is unique to this
phase; the approval-gate pattern around it is generic. See
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md).

**Phase 7 — Scorecards.** Define checks including Azure-specific ones: is
the service's identity Workload-Identity-federated rather than a service
principal secret embedded anywhere, does the Flexible Server instance have
automated backups and (production tier) zone redundancy enabled, is the
resource group tagged per the Phase 1 tagging policy. See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

**Phase 8 — Multi-tenancy.** If more than one team shares the Phase 2
cluster, decide namespace-per-team vs. dedicated clusters (or dedicated
subscriptions, an Azure-specific option worth weighing given how cheap
subscription vending is under Phase 1's landing zone), scope each
federated credential's `subject` to its namespace/ServiceAccount, and
enforce ResourceQuotas before onboarding a second team. See
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

- Carry the AKS OIDC issuer URL and subscription/resource-group IDs as
  named variables across every phase's IaC — a stale copy of the issuer
  URL in the Phase 6 self-service action after a cluster rebuild is a
  recurring source of federated-credential mismatches.
- Enable zone redundancy and automated backups on the Phase 3 Flexible
  Server instance from day one; the catalog database becomes the single
  source of service ownership records faster than most teams expect.
- Don't let Phase 6 go live before Phase 1's Azure Policy assignments are
  final — a self-service action granting a resource today that a new deny
  policy would block next month leaves an orphaned exception to track down
  manually.
- Re-run Phase 5's validation pipeline on a schedule, not just before
  initial launch — an AKS minor version bump or an Azure provider update
  can silently break a previously-working template.
- Start Phase 9's pilot rollout only against the specific template tier
  that has already cleared Phase 5 — putting a real team through an
  unvalidated golden path costs more adoption trust than it's worth.

## Common pitfalls

- **Symptom:** The Phase 6 self-service action fails every real request
  with `AADSTS70021` (no matching federated identity credential), despite
  working in testing.
  **Fix:** This is a Phase 2/Phase 6 sequencing gap — the federated
  credential's `subject` was written against a namespace/ServiceAccount
  name Phase 4's template scaffolds differently in practice (e.g., an
  environment suffix the credential's `subject` string didn't
  anticipate). Re-derive the `subject` from the actual scaffolded
  manifest, exactly, rather than a hand-typed example.

- **Symptom:** Backstage's catalog shows transient errors during a
  Flexible Server planned maintenance window, even though Azure classifies
  the instance as zone-redundant/highly available.
  **Fix:** The Backstage backend's Postgres connection pool lacks retry/
  reconnect logic tolerant of the brief failover gap zone-redundant HA
  still has; this is a Phase 3 gap invisible until a real maintenance
  event. Add connection retry with backoff to the backend's database
  config.

- **Symptom:** Phase 7's scorecard shows most early services failing the
  "Workload Identity, not service principal secret" check, despite the
  platform mandating Workload Identity from the start.
  **Fix:** Phase 4's template was published and used before Phase 2's
  Workload Identity setup was actually finished, so early services
  scaffolded from an older revision with a service-principal-secret
  fallback. Re-validate the current template (Phase 5) to confirm the
  fallback is gone, then batch-remediate the already-scaffolded services.

- **Symptom:** A team lead runs `az group delete` on what they believe is
  an empty resource group to "clean up," and it turns out to be the
  resource group holding the Phase 3 Flexible Server instance.
  **Fix:** This is destructive and, without `soft delete`/backup retention
  configured on the server, can be unrecoverable. Never treat resource
  group deletion as a routine cleanup step once a phase's production
  resources live in it; enable Flexible Server's backup retention and
  geo-redundant backup before Phase 3 is considered complete, and require
  an explicit confirmation step (separate from a generic "clean up my
  sandbox" habit) before any `az group delete` against a platform-tooling
  resource group.

- **Symptom:** A production Flexible Server instance is discovered
  provisioned with no record of who approved it.
  **Fix:** The Phase 6 approval gate was enforced only in the Scaffolder
  UI's form validation, not on the server-side approval endpoint itself.
  Require the policy check and `requestedBy != approver` guard on every
  code path that reaches the provisioning state, not only the UI path a
  developer is expected to use.

## Worked example

**Scenario:** "Contoso Logistics" has an Azure tenant with a root
Management Group and no platform tooling. The platform team builds an IDP
over one quarter.

1. **Phase 1:** A `Platform` Management Group is added under the root
   alongside existing `Landing Zones` and `Decommissioned` MGs; a
   `sub-platform-tools` subscription and `sub-fleet-dev` (first tenant) are
   vended via the ALZ Terraform module, with an Azure Policy initiative
   denying resource creation without an `owner` tag.
2. **Phase 2:** `sub-platform-tools` gets an AKS cluster
   `platform-aks-weu`, with Workload Identity enabled against OIDC issuer
   `https://weu.oic.prod-aks.azure.com/<TENANT_ID>/<OIDC_ID>/`.
3. **Phase 3:** Backstage is packaged as `charts/backstage-contoso`,
   deployed against Flexible Server `contoso-backstage-catalog`
   (zone-redundant, `Standard_D2ds_v5`), with the backend's
   ServiceAccount `backstage-backend` federated to an Entra ID app with
   `Key Vault Secrets User` on the vault holding the DB credential.
4. **Phase 4:** A "Node.js service" golden-path template is authored,
   producing a Dockerfile, a GitHub Actions workflow, and a
   `ServiceAccount` manifest annotated
   `azure.workload.identity/client-id: <SERVICE_APP_CLIENT_ID>`.
5. **Phase 5:** A validation pipeline scaffolds `test-svc-001`, builds,
   deploys to an `ephemeral-validation` namespace, curls `/healthz`, and
   tears down — required before the template is marked `default`.
6. **Phase 6:** A Scaffolder action `custom:azure:provisionFlexServer`
   checks an OPA policy (auto-approve `Standard_B1ms`/dev, require
   approval otherwise), and on approval runs a Bicep deployment via a
   managed identity scoped to the requesting team's resource group.
7. **Phase 7:** A scorecard adds a "Workload Identity, not SP secret"
   check, weighted highly under Security.
8. **Phase 9:** `fleet-tracking` is recruited as the pilot team (highest
   infra-ticket volume last quarter); after two sprints their Flexible
   Server provisioning turnaround drops from a multi-day ticket to a
   same-day auto-approved or next-business-day approved request, and that
   result is published before the template goes org-wide.

## Cross-references

- [azure-landing-zone-setup](../../../cloud/skills/azure-landing-zone-setup/SKILL.md) — Phase 1.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — Phase 2.
- [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md) — Phase 3 chart packaging.
- [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 3 custom backend/frontend logic.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 4.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 5.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Phase 6.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 7.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — Phase 8.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md), [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md), [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — Phase 9.
- [complete-idp-deployment-on-aws-from-scratch](../complete-idp-deployment-on-aws-from-scratch/SKILL.md) — the same shape on AWS, useful for a multi-cloud platform team comparing the two.
