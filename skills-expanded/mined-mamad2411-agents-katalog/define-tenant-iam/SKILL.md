---
name: define-tenant-iam
description: >
  Define the standard IAM groups and roles for a platform tenant — covering the groups that
  developers use to access their own workloads across all sectors and tiers (e.g.,
  "payments-sandbox-contributors", "payments-readers"). Produces a tenant.yaml file
  (the platform's source of truth for membership) and an IAM group matrix.
  Use when onboarding a new tenant or formalizing an existing team's access model.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "5"
---

# Define Tenant IAM

## Skill Type

Design

## Your Goal

Produce a **tenant IAM definition** — a `tenant.yaml` file that captures the membership and role model for one or more tenants. This file is the source of truth for membership sync, group provisioning, and JIT escalation configuration. It is the input for the cloud-specific IAM provisioning skills (`manage-azure-iam`, `manage-aws-iam`, `manage-gcp-iam`) and the Kubernetes RBAC skill (`manage-k8s-iam`).



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Segmentation design**: Which Sectors and Tiers does this tenant operate in? (Ideally, import the output of the `design-segmentation` skill.)
- **Tenant name(s)**: The canonical short name used in group naming (e.g., `payments`, `recommendations`). Must be slug-compatible: lowercase, hyphens only.
- **Tenant type**: Internal team or external B2B customer. Affects isolation requirements.
- **Cloud provider(s)**: AWS, Azure, GCP, or multi-cloud. Affects group provisioning targets.
- **Identity Provider**: Microsoft Entra ID, Okta, Google Workspace. Groups will be created here.
- **Tenant members**: List of individuals (email or username) and their intended role — `Role("admin")`, `Role("contributor")`, or `Role("reader")`.
- **CI/CD system**: Which system deploys to this tenant's namespaces? Determines the Workload Identity trust anchor for the `Role("operator")` group.
- **JIT tooling**: Azure PIM, AWS IAM Identity Center, Teleport, or none. Determines how escalation policies are expressed.
- **Special requirements**: Any compliance constraints (PCI, HIPAA) that affect session durations or approval requirements?

If the user is defining multiple tenants, gather this information for each one. Common fields (IdP, cloud provider, JIT tooling) can be inherited from a shared defaults block.

## Process

### Step 1 — Enumerate the Group Matrix

For each tenant, derive the standard groups from the role taxonomy. The naming pattern follows:

| Group Name Pattern | Role | Scope | Membership Policy |
|--------------------|------|-------|-------------------|
| `{tenant}-{tier}-operator` | `Role("operator")` | Non-human | CI/CD runner identity only — no human members |
| `{tenant}-{tier}-admins` | `Role("admin")` | Human | JIT-only. Justification required. |
| `{tenant}-{tier}-contributors` | `Role("contributor")` | Human | JIT for `Tier("live")`. Standing available in `Tier("sandbox")`. |
| `{tenant}-readers` | `Role("reader")` | Human | Standing. Cross-tier read access. |

Note that the `Role("reader")` group is **cross-tier** — once granted, it provides read access across both `Tier("sandbox")` and `Tier("live")`. This is intentional: developers should always be able to see their production resources for troubleshooting. Write access, however, is always tier-scoped.

Example group matrix for a `payments` tenant with `Tier("sandbox")` and `Tier("live")`:

- `payments-sandbox-operator` (non-human)
- `payments-sandbox-admins` (JIT)
- `payments-sandbox-contributors` (standing or JIT)
- `payments-live-operator` (non-human)
- `payments-live-admins` (JIT)
- `payments-live-contributors` (JIT)
- `payments-readers` (standing, cross-tier)

### Step 2 — Define `Role("operator")` Identity Requirements

For each `{tenant}-{tier}-operator` group, define the Workload Identity Federation trust conditions:

- **Trust anchor**: Which external IdP issues the tokens? (e.g., GitHub Actions, GitLab, Kubernetes OIDC)
- **Subject claim**: The specific pipeline, repository, or service account. Scope as narrowly as possible — use branch or environment constraints, not wildcards.
- **Permitted operations**: Scoped to the tenant's own resources within the sector/tier, not the full account. The operator should not be able to modify other tenants' resources.
- **No human members**: Explicitly state this. Human members in an `Role("operator")` group are a misconfiguration.

If the tenant has separate pipelines for infrastructure (Terraform/Pulumi) and application deployment (Kubernetes manifests), consider defining two distinct `Role("operator")` identities with different scopes rather than one over-privileged runner.

### Step 3 — Define JIT Escalation Policies

For each `Role("admin")` and `Role("contributor")` group, define escalation behaviour:

**`Tier("sandbox")` `Role("contributor")`**:
- Eligible: all tenant Readers
- Approval: self-approve
- Duration: up to 8 hours
- Justification: optional

**`Tier("live")` `Role("contributor")`**:
- Eligible: members listed under `contributors` in the tenant definition
- Approval: self-approve with mandatory justification
- Duration: up to 4 hours
- Justification: required (e.g., incident reference, change request ID)

**`Tier("sandbox")` `Role("admin")`**:
- Eligible: members listed under `admins`
- Approval: peer or self-approve
- Duration: up to 4 hours
- Justification: recommended

**`Tier("live")` `Role("admin")`**:
- Eligible: members listed under `admins`
- Approval: peer approval mandatory
- Duration: up to 2 hours
- Justification: required

For tenants under compliance scope (PCI-DSS, HIPAA), reduce `Tier("live")` `Role("admin")` duration to 1 hour and require two-party approval.

### Step 4 — Assign Initial Membership

For each tenant, classify members into the three human roles:

- **Admins**: The team's tech lead or senior engineer responsible for the tenant. Usually one or two people. Eligible for JIT `Role("admin")` escalation.
- **Contributors**: Active engineers on the team. Eligible for JIT `Role("contributor")` escalation in `Tier("live")`, standing `Role("contributor")` access in `Tier("sandbox")` if the team requests it.
- **Readers**: All team members and any stakeholder who needs visibility (e.g., product managers with read access for cost review). Standing access.

Rules:
- Always list individuals by email or username — never a group. Group nesting breaks the audit trail.
- An individual can appear in only one role tier; the platform derives eligibility upward (an `Role("admin")` is implicitly eligible for `Role("contributor")` escalation).
- Do not add platform team members here. They have access via the core IAM definition.

### Step 5 — Define Sector Scope

Specify which sectors the tenant operates in. Most product tenants will only be in a single business sector (`ecommerce`, `retail`, etc.). Some may span multiple sectors if they own cross-cutting infrastructure (e.g., a shared services team owning resources in both the Platform and `Sector("ecommerce")`s).

For each sector, the groups are scoped to that sector's accounts, subscriptions, or projects. The automation (`manage-azure-iam`, `manage-aws-iam`, `manage-gcp-iam`) creates role assignments only within the correct scope.

### Step 6 — Handle Multiple Tenants

If defining IAM for more than one tenant, check for:

- **Shared readers**: A platform-wide `Role("reader")` policy may be desirable (all engineers can read all tenants), or readers may be strictly per-tenant. Decide and document the policy.
- **Cross-tenant access**: If two tenants need to interact (e.g., `payments` calling `fraud-detection`), this is a service-to-service communication pattern handled via Workload Identity, not human group membership. Do not add one tenant's groups to another.
- **Shared `Role("contributor")` groups**: Avoid this. Shared contributors obscure the audit trail and make least-privilege impossible to enforce.

### Step 7 — Validate Against Principles

Review each tenant definition against the core IAM principles:

- [ ] No human is a member of any `Role("operator")` group
- [ ] No standing write access exists for the `Tier("live")`
- [ ] All members are listed as individuals, not nested groups
- [ ] `Role("operator")` trust conditions are scoped to specific pipeline references, not wildcards
- [ ] Workload Identity Federation is used instead of static keys
- [ ] Cross-tenant access is not modelled as group membership

Flag violations and propose remediations before producing the output.

### Step 8 — Review and Iterate

Present the complete tenant matrix to the user. Ask:

- Are there team members missing or miscategorised?
- Are the JIT session durations appropriate for this team's deployment cadence?
- Does the sector scope correctly reflect where this team's workloads live?
- Is there a compliance requirement (PCI, HIPAA) that requires stricter escalation policies?

Iterate until satisfied, then produce the final document.

## Output Format

Produce one YAML file per tenant named `tenants/{tenant-name}.yaml`. If multiple tenants are being defined, produce one file each.

``yaml
# tenants/payments.yaml
# Tenant IAM definition — source of truth for group membership and access.
# Processed by: manage-azure-iam, manage-aws-iam, manage-gcp-iam, manage-k8s-iam

name: payments
sectors:
  - ecommerce

# Human members — individuals only, no nested groups
members:
  admins:
    - marta@mountainlab.io
  contributors:
    - javi@mountainlab.io
    - ana@mountainlab.io
  readers:
    - pedro@mountainlab.io
    - lucia@mountainlab.io

# Workload Identity — non-human runner identities per tier
workload_identity:
  sandbox:
    issuer: https://token.actions.githubusercontent.com
    subject: repo:mountainlab/payments-service:ref:refs/heads/main
    audience: api://AzureADTokenExchange
  live:
    issuer: https://token.actions.githubusercontent.com
    subject: repo:mountainlab/payments-service:environment:live
    audience: api://AzureADTokenExchange

# JIT escalation policy overrides (leave empty to use platform defaults)
jit_overrides:
  live_admin:
    approval: peer
    max_duration_hours: 2
    justification_required: true
    # compliance: pci-dss  # uncomment to apply stricter PCI policy
``

Accompany the YAML with a brief Markdown summary: the group matrix that will be created, the escalation policy in plain language, and any open questions.

## Principles to Apply

- **People-first IAM**: Define members once at the tenant level. The platform automation handles all cloud-specific group provisioning and role binding.
- **`Role("reader")` by default**: All members get standing read access across tiers. Write access is gated by JIT.
- **Cross-tier readers, tier-scoped writers**: The `{tenant}-readers` group spans tiers; `Role("contributor")` and `Role("admin")` groups are always tier-scoped.
- **No group nesting in membership**: Always list individuals. Nested groups break audit trails.
- **Service-to-service is not IAM groups**: Cross-tenant communication is handled by Workload Identity, not by adding groups to other groups.
- **Compliance overrides are explicit**: PCI, HIPAA, and other regulated scopes must be annotated so that stricter escalation policies are applied by the automation.

## Related Chapter(s)

This skill is grounded in **Chapter 5: Identity and Access Management** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
