---
name: complete-idp-deployment-on-aws-from-scratch
description: >
  Sequences a complete, from-scratch Internal Developer Platform deployment
  on AWS: landing zone → EKS cluster → Helm-deployed Backstage backed by
  RDS PostgreSQL → golden-path scaffolding template → self-service API
  wired to AWS provisioning (IRSA roles, RDS instances) → scorecards. This
  is the integration runbook that orders the individual AWS/EKS/Backstage
  skills correctly and flags the handoffs between them. Use when a user
  asks to "deploy an IDP on AWS from scratch," "stand up Backstage on EKS
  end-to-end," "build our internal developer platform on AWS," "wire
  self-service database/IAM provisioning into Backstage on AWS," or
  "sequence an AWS platform rollout from account creation to golden-path
  templates."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: internal-developer-platform
  maturity: stable
---

# Complete IDP Deployment on AWS from Scratch

## Purpose

Standing up an Internal Developer Platform on AWS touches a landing zone,
a Kubernetes cluster, a Backstage instance, a catalog database, a
scaffolding template, a provisioning API, and a maturity model — each of
which is already covered in depth elsewhere in this repo. What isn't
covered elsewhere is the **sequencing**: which phase has to finish and be
validated before the next one starts, which decisions made in an early
phase (account structure, IRSA trust policy shape) quietly constrain every
later phase, and where teams actually get stuck gluing these pieces
together. This skill is that integration runbook — a phase-by-phase path
from an empty AWS Organization to a Backstage instance developers
self-service against, with each phase handing off to the deep skill that
covers its mechanics. It does not restate EKS, Backstage, or Terraform
mechanics; it tells you which skill to open next and what to carry forward
from the previous phase.

## When to use

- Standing up a green-field IDP for an organization that has AWS accounts
  but no platform team tooling yet.
- Migrating a collection of ad hoc AWS deployment scripts and a wiki-based
  service list into a Backstage-based platform.
- Bootstrapping a reference IDP in a newly created AWS Organization as part
  of a broader AWS adoption.
- Planning the order of operations for a platform team that has budget and
  a mandate but hasn't decided what to build first.
- Auditing an in-progress AWS IDP build to find which phase's missing
  validation gate is causing downstream problems (e.g., a self-service API
  built before the landing zone's SCPs were finalized, requiring rework).

## Prerequisites & environment

- Authority to create or already-existing access to an AWS Organization's
  management account, sufficient to bootstrap Control Tower or extend an
  existing landing zone.
- Terraform (or CDK) maturity across the team — every phase below produces
  IaC, not console clicks, so this isn't optional tooling.
- `kubectl`, `helm` ≥ 3.8 (for OCI registry chart support), and either
  `eksctl` or the Terraform EKS module for cluster provisioning.
- A Node.js/Yarn toolchain capable of building and customizing a Backstage
  app (Backstage itself is a Node/TypeScript monorepo, not a pre-built
  image you configure purely via Helm values).
- A registered domain and Route 53 hosted zone (or delegated subdomain)
  for Backstage's ingress hostname and an ACM certificate.
- A decision, made before Phase 2, on whether this IDP targets a **new**
  EKS cluster dedicated to platform tooling or an **existing** cluster
  already running workloads — this changes the tenancy phase's scope
  significantly (see Phase 8).
- A named owner for the self-service approval gate (Phase 6) — someone has
  to actually receive and act on approval requests before that phase goes
  live, not after.

## Step-by-step guidance

**Phase 1 — AWS landing zone.** Design the OU hierarchy (e.g., separate
`Platform`, `Workloads`, `Security` OUs), bootstrap Control Tower, vend
accounts through Account Factory, and attach the SCPs that will constrain
every later phase (a guardrail denying un-tagged resource creation now
saves a scorecard check in Phase 7 from ever failing). Vend at least two
accounts before continuing: one for the platform tooling itself (EKS
cluster, Backstage, RDS) and one as the first "tenant" workload account —
building the IDP against a single-account model here is the single most
common rework trigger later. See
[aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md).
**Do not proceed to Phase 2 until the landing zone's dry-run account
(step 8 of that skill) has been validated** — an EKS cluster built inside
an account whose guardrails aren't finalized will need its IAM/network
config redone when the SCPs change.

**Phase 2 — EKS cluster with IRSA.** Provision the platform-tooling
account's EKS cluster with a pinned Kubernetes version, node groups sized
for Backstage's backend (steady CPU/memory, not bursty), and IRSA
(IAM Roles for Service Accounts) configured on the cluster's OIDC provider
before anything is deployed to it. Record the cluster's OIDC provider ARN
— Phase 3 and Phase 6 both need it to construct IRSA trust policies. See
[managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md)
for cluster provisioning, node group design, and the IRSA trust-policy
walkthrough specifically.

**Phase 3 — Backstage on EKS, backed by RDS PostgreSQL.** Package
Backstage as a Helm chart (Backstage's own scaffolded output is a Node
app; wrap its container image in a chart rather than hand-writing raw
manifests) and deploy it against an RDS PostgreSQL instance — Multi-AZ for
anything beyond a pilot — as the catalog database, with the Backstage pod
authenticating to RDS via IAM database authentication through the IRSA
role from Phase 2 rather than a static password baked into a Secret. Any
custom backend plugin logic (a custom auth provider, a proxy to an
internal system) is built per
[backstage-plugin-development](../backstage-plugin-development/SKILL.md);
the chart packaging and values-schema design is per
[helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md).
Wire the RDS credential lookup through Secrets Manager (an
IRSA-scoped `secretsmanager:GetSecretValue` call at pod startup, or the
Secrets Store CSI driver) rather than committing a connection string.

**Phase 4 — Golden-path template design.** With Backstage's Scaffolder
running, design the first golden-path template: an opinionated new-service
default that produces a Dockerfile, a CI pipeline (GitHub Actions or the
CodePipeline/CodeDeploy pattern), catalog registration, and — for AWS
specifically — a scaffolded IRSA-ready Kubernetes `ServiceAccount`
manifest with the trust-policy annotation pre-filled. Tier the template by
complexity (a minimal tier and a "batteries-included" tier) rather than
building one template that tries to fit every service shape. See
[golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md).

**Phase 5 — Validate the golden path end-to-end.** Before publishing the
Phase 4 template as the org default, run it through a CI pipeline that
scaffolds a real instance, builds it, deploys it to an ephemeral namespace
in the Phase 2 cluster (or a short-lived preview account), smoke-tests it,
and tears every created resource down on both success and failure — an
untested template that silently fails on its first real use burns the
platform team's credibility before Phase 9's rollout even starts. See
[golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md).

**Phase 6 — Self-service API wired to AWS provisioning.** Build the
Scaffolder custom actions (or a bespoke internal API) that let a developer
request an IRSA-scoped IAM role or an RDS instance through the catalog,
not through a ticket. Model the request as a state machine
(`requested → policy_checked → pending_approval → approved →
provisioning → completed`), gate production-tier RDS instance classes and
any IAM role with broader-than-namespace-scoped trust policy behind human
approval, and keep the policy/budget rules external (OPA/Rego) so a
security or FinOps change doesn't require redeploying the action. The
AWS-specific provisioning call itself — assuming a role via STS to run
`rds:CreateDBInstance` or `iam:CreateRole` with a trust policy scoped to
the requesting namespace's service account subject — is the part unique to
this phase; the gating pattern around it is generic. See
[platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md).

**Phase 7 — Scorecards.** Define production-readiness and security-posture
checks, including AWS-specific ones a generic scorecard wouldn't include:
does the service's IAM role use IRSA rather than a static access key
embedded anywhere, is the RDS instance backed by automated backups and
(for production tier) Multi-AZ, are resources tagged per the Phase 1 tag
policy. Weight by blast radius, not equally. See
[service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md).

**Phase 8 — Multi-tenancy, if more than one team shares the Phase 2
cluster.** Decide namespace-per-team vs. dedicated clusters, bind RBAC and
IRSA trust policies per namespace (scope the trust policy's
`sub` condition to the specific namespace/ServiceAccount, not the whole
OIDC provider), and enforce ResourceQuotas before onboarding the second
team — retrofitting tenancy boundaries after several teams are already on
a shared cluster is materially harder than designing it in up front. See
[multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md).

**Phase 9 — Rollout, operating model, and measurement.** Sequence the
rollout starting from a pilot team with real, current pain (not the
easiest team to please), run the platform team per Team Topologies'
"thinnest viable platform" discipline, and measure adoption with SPACE/DX
Core 4 metrics rather than catalog entity counts. See
[idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md),
[platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md),
and
[developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md).

## Best practices

- Carry the same OIDC provider ARN and account IDs forward as named
  variables across every phase's IaC — a hand-copied ARN that drifts
  between the Phase 2 cluster config and the Phase 6 self-service action
  is a recurring source of silent trust-policy mismatches.
- Stand up Phase 3's RDS instance with `deletion_protection = true` and a
  final snapshot requirement from day one — the catalog database is easy
  to treat as "just infrastructure" until it holds the only record of
  which team owns which service.
- Don't let Phase 6 (self-service) go live before Phase 1's SCPs are
  final. A self-service action that grants an IAM role today, followed by
  a new SCP next month that would have denied it, leaves existing
  resources in a state the guardrail can't retroactively fix.
- Treat Phase 5's validation pipeline as a permanent CI job, not a one-time
  check before launch — re-run it on every template change and on a
  schedule, since an unrelated AWS provider or EKS version change can
  silently break a previously-working template.
- Sequence Phase 9's pilot-team rollout to start only after Phase 5 has
  passed for the specific template tier that pilot team will use — putting
  a real team through an unvalidated golden path converts a platform
  adoption win into a trust-destroying incident.

## Common pitfalls

- **Symptom:** The self-service API (Phase 6) works fine in testing but
  every real request from a developer fails with an IRSA
  `AssumeRoleWithWebIdentity` `AccessDenied`.
  **Fix:** This is almost always a Phase 2/Phase 6 sequencing gap — the
  IRSA trust policy's `sub` condition was written against a namespace/
  ServiceAccount name that Phase 4's golden-path template scaffolds
  differently (e.g., the template appends an environment suffix the trust
  policy didn't anticipate). Re-derive the trust policy condition from the
  actual scaffolded manifest, not from a hand-typed example.

- **Symptom:** Backstage's catalog intermittently shows stale or missing
  entities after the RDS instance in Phase 3 fails over during a Multi-AZ
  maintenance event.
  **Fix:** The Backstage backend's database connection pool wasn't
  configured with retry/reconnect logic tolerant of an RDS failover's
  brief unavailability window; this is a Phase 3 gap that surfaces only
  under real AWS maintenance, not in initial testing. Add connection
  retry with backoff in the Backstage backend config, and confirm the
  failover behavior once against a non-production RDS instance before
  relying on it.

- **Symptom:** Phase 7's scorecard shows most services failing the "no
  static AWS credentials" check, even though the platform mandated IRSA
  from day one.
  **Fix:** Phase 4's golden-path template was published before Phase 2's
  IRSA setup was finished, so early-adopting services scaffolded from an
  older template revision with a static-credential fallback baked in.
  Re-run Phase 5's validation against the current template to confirm the
  fallback is gone, then batch-remediate the already-scaffolded services
  rather than treating each one as an isolated scorecard failure.

- **Symptom:** A platform engineer runs `terraform destroy` against the
  Phase 1 landing zone module to "start clean" after a mistake, and it
  also tears down the OU structure accounts in Phase 2 through 8 were
  built inside.
  **Fix:** This is destructive and often irreversible for account-level
  resources (a closed AWS account has a 90-day reactivation window at
  best, and Control Tower re-enrollment is not instantaneous). Never run a
  blanket `destroy` against the landing zone module once downstream
  phases depend on it; scope any correction to the specific resource via
  `terraform destroy -target` after confirming no later phase references
  it, and prefer `terraform plan` review over destroy-and-reapply as the
  default fix for a landing zone misconfiguration.

- **Symptom:** The Phase 6 self-service action's "approve" endpoint is
  discovered to have been called directly, bypassing the Scaffolder UI
  entirely, and a production-tier RDS instance appears with no approval
  record.
  **Fix:** The policy/approval gate was implemented only in the Scaffolder
  action's client-facing form validation, not enforced server-side on the
  approval endpoint itself. Require the same policy check and
  `requestedBy != approver` guard on every code path that can reach
  `provisioning`, per the self-service skill's server-side-gate guidance —
  not just the one a developer is expected to use.

## Worked example

**Scenario:** "Acme Retail" has an AWS Organization with three existing
OUs but no platform tooling. The platform team builds an IDP from scratch
over one quarter.

1. **Phase 1:** A `Platform` OU is added alongside existing `Workloads`
   and `Security` OUs; Control Tower vends `acme-platform-tools` (hosts
   EKS + Backstage + RDS) and `acme-checkout-dev` (first tenant) through
   Account Factory, with an SCP denying resource creation without an
   `owner` tag.
2. **Phase 2:** `acme-platform-tools` gets an EKS cluster
   `platform-eks-use1`, IRSA enabled against its OIDC provider
   `oidc.eks.us-east-1.amazonaws.com/id/<OIDC_ID>`.
3. **Phase 3:** Backstage is packaged as a Helm chart
   `charts/backstage-acme`, deployed against RDS instance
   `acme-backstage-catalog` (Multi-AZ, `db.r6g.large`), with the backend
   pod's ServiceAccount `backstage-backend` annotated with an IRSA role
   scoped to `secretsmanager:GetSecretValue` on exactly the RDS credential
   secret.
4. **Phase 4:** A "Node.js service" golden-path template is authored,
   producing a Dockerfile, a GitHub Actions CI workflow, and a
   `ServiceAccount` manifest annotated
   `eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/${service-name}-irsa`.
5. **Phase 5:** A validation pipeline scaffolds `test-svc-001` from the
   template, builds it, deploys it to an `ephemeral-validation` namespace,
   curls its `/healthz`, and tears the namespace down — wired as a
   required check before the template can be marked `default`.
6. **Phase 6:** A Scaffolder action `custom:aws:provisionRds` checks an
   OPA policy (auto-approve `db.t3.micro`/dev, require approval for
   anything larger or production-tagged), and on approval calls
   `rds:CreateDBInstance` via an STS-assumed role scoped to the requesting
   team's namespace.
7. **Phase 7:** A scorecard adds an "IRSA, not static keys" check (fails
   any service whose deployed `ServiceAccount` lacks the
   `eks.amazonaws.com/role-arn` annotation) weighted highly under Security.
8. **Phase 9:** `acme-checkout` is recruited as the pilot team (they'd
   filed the most infra tickets last quarter); after two sprints, their
   RDS provisioning turnaround drops from a 3-day ticket to a same-day
   auto-approved or next-business-day approved request, and the platform
   team publishes that result before opening the template org-wide.

## Cross-references

- [aws-landing-zone-setup](../../../cloud/skills/aws-landing-zone-setup/SKILL.md) — Phase 1.
- [managed-kubernetes-eks-aks-gke](../../../kubernetes-platform/skills/managed-kubernetes-eks-aks-gke/SKILL.md) — Phase 2.
- [helm-chart-authoring](../../../kubernetes-platform/skills/helm-chart-authoring/SKILL.md) — Phase 3 chart packaging.
- [backstage-plugin-development](../backstage-plugin-development/SKILL.md) — Phase 3 custom backend/frontend logic.
- [golden-path-template-design-for-developer-platforms](../golden-path-template-design-for-developer-platforms/SKILL.md) — Phase 4.
- [golden-path-template-validation-and-testing](../golden-path-template-validation-and-testing/SKILL.md) — Phase 5.
- [platform-self-service-api-and-workflow-design](../platform-self-service-api-and-workflow-design/SKILL.md) — Phase 6.
- [service-scorecards-and-maturity-model-design](../service-scorecards-and-maturity-model-design/SKILL.md) — Phase 7.
- [multi-tenancy-and-team-workspace-design-for-idp](../multi-tenancy-and-team-workspace-design-for-idp/SKILL.md) — Phase 8.
- [idp-adoption-rollout-and-change-management-strategy](../idp-adoption-rollout-and-change-management-strategy/SKILL.md), [platform-engineering-team-topology-and-operating-model](../platform-engineering-team-topology-and-operating-model/SKILL.md), [developer-experience-measurement-and-platform-adoption](../developer-experience-measurement-and-platform-adoption/SKILL.md) — Phase 9.
- [complete-idp-deployment-on-kubernetes-from-scratch](../complete-idp-deployment-on-kubernetes-from-scratch/SKILL.md) — the cloud-agnostic equivalent, useful if a future migration away from AWS-specific self-service wiring is on the roadmap.
