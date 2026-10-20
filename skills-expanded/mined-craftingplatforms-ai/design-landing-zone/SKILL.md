---
name: design-landing-zone
description: >
  Design the cloud account/subscription/project and organizational hierarchy — the landing zone —
  by mapping the Platform Notation to cloud provider primitives. Produces a
  landing-zone-design.md document specifying which accounts/subscriptions/projects/OUs/folders
  exist per coordinate, their guardrails strategy, and the isolation level rationale.
  Use after design-segmentation, before manage-azure-landing-zone / manage-aws-landing-zone /
  manage-gcp-landing-zone.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Design Landing Zone

## Skill Type

Design

## Your Goal

Produce a **landing zone design document** — a cloud-agnostic specification of the organizational hierarchy and guardrails that enforces the segmentation model. This document is the input for the cloud-specific provisioning skills (`manage-azure-landing-zone`, `manage-aws-landing-zone`, `manage-gcp-landing-zone`).

The output must be concrete: every structural node named, its coordinate annotation stated, its guardrail requirements listed, and its isolation rationale documented.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Segmentation design**: The output of the `design-segmentation` skill (`segmentation-design.md`) — Sectors, Tiers, Regions, Tenants, and isolation levels. This is required input.
- **Cloud provider(s)**: AWS, Azure, GCP, or multi-cloud. The hierarchy design differs substantially per provider.
- **Tenant isolation model**: Should each tenant have a dedicated account/subscription/project, or is tenant isolation handled at a softer boundary (resource group, namespace)? Reference the isolation levels from the segmentation design.
- **Operational capacity**: How many accounts/subscriptions/projects can the platform team realistically manage? This constrains the structural depth.
- **Compliance requirements**: Any mandates (PCI-DSS, HIPAA, FedRAMP) that require specific structural isolation? Some frameworks require dedicated accounts for in-scope workloads.
- **Existing structure**: Does a cloud organization already exist? Are there legacy accounts or subscriptions to incorporate?

Read the segmentation design document before proceeding. Do not derive the structure from assumptions.

## Process

### Step 1 — Determine the Structural Granularity

Decide which coordinate dimensions map to hard structural boundaries vs. softer ones, based on the isolation levels in the segmentation design:

**Minimum recommended baseline** (suitable for most scale-ups):
- `(Sector, Tier)` → hard boundary (account / subscription / project)
- `(Sector, Tier, Region)` → network boundary (VPC / VNet) — addressed in `design-networking`
- `(Sector, Tier, Region, Tenant)` → soft boundary (resource group / namespace)

**Strong isolation** (for regulated workloads or enterprise scale):
- `(Sector, Tier, _, Tenant)` → hard boundary (dedicated account per tenant within the tier)
- This trades operational simplicity for a much smaller blast radius between tenants.

Document the chosen granularity and the reasons — operational capacity, compliance, cost, and blast radius tolerance.

### Step 2 — Define the Organizational Hierarchy

For each cloud provider in scope, enumerate the structural nodes:

**AWS:**
- **Organization root**: The management account. No workloads live here.
- **Organizational Units**: One per Sector at minimum. Sub-OUs for Tier grouping if needed.
- **Accounts**: One per `(Sector, Tier)` for standard isolation, or one per `(Sector, Tier, _, Tenant)` for strong isolation. Always include:
  - A dedicated `audit` / `log-archive` account (Security sector, any tier) — receives centralized CloudTrail, Config, and Security Hub findings.
  - A dedicated `network` or `transit` account for the hub network (if using a central Transit Gateway).
  - A management account used only for Organizations API and billing — no workloads.

**Azure:**
- **Tenant Root Group**: The root of the Management Group hierarchy.
- **Management Groups**: One per Sector. Nested sub-groups for Tiers if policy inheritance needs refinement.
- **Subscriptions**: One per `(Sector, Tier)` for standard isolation. One per `(Sector, Tier, _, Tenant)` for strong isolation.
- **Resource Groups**: One per full coordinate `(Sector, Tier, Region, Tenant)`.
- Required platform subscriptions: `platform-sandbox`, `platform-live`, `connectivity` (hub networking), `identity` (Entra ID DS if needed), `management` (monitoring, update management).

**GCP:**
- **Organization**: The root node. Organization Policies set here apply everywhere.
- **Folders**: One per Sector. Nested sub-folders for Tier grouping (keep hierarchy ≤ 3 levels deep).
- **Projects**: One per `(Sector, Tier)` for standard isolation, or one per `(Sector, Tier, _, Tenant)` for strong isolation. Always include:
  - A dedicated `audit` project (centralized log sink, Security Command Center).
  - A `connectivity` project (Shared VPC host project for hub networking).
- **Billing Accounts**: Linked to projects. Do not use the project hierarchy for billing — link separately.

For multi-cloud, produce the hierarchy table for each provider independently. The coordinate labels are the same; only the primitives differ.

### Step 3 — Name Every Structural Node

Apply the naming convention (from `define-naming-convention` if already run, or define a working convention here). Examples:

| Provider | Node Type | Convention | Example |
|----------|-----------|-----------|---------|
| AWS | Account | `{sector}-{tier}` or `{tenant}-{tier}` | `ecommerce-live`, `payments-live` |
| AWS | OU | `{sector}` | `ecommerce`, `platform` |
| Azure | Management Group | `mg-{sector}` | `mg-ecommerce`, `mg-platform` |
| Azure | Subscription | `sub-{sector}-{tier}` | `sub-ecommerce-live` |
| Azure | Resource Group | `rg-{tenant}-{region}-{tier}` | `rg-payments-eu01-live` |
| GCP | Folder | `{sector}` | `ecommerce`, `platform` |
| GCP | Project | `{sector}-{tier}` or `{tenant}-{tier}` | `ecommerce-live`, `payments-live` |

If a naming convention document already exists, defer to it.

### Step 4 — Define Guardrails per Structural Level

Guardrails are preventive controls applied at the organizational hierarchy level. They enforce baseline security and compliance regardless of what individual teams configure.

For each structural level, specify the guardrails that apply:

**Sector level (Management Group / OU / Folder)**:
- Restrict which cloud services can be used (e.g., deny compute regions outside declared regions)
- Enforce mandatory resource tagging
- Require specific audit logging to be enabled

**Tier level (Subscription / Account / Project sub-group)**:
- Sandbox: more permissive; allow broad experimentation but deny cross-tier access
- Live: strict; deny public resource exposure without explicit exception, enforce encryption at rest and in transit, require change management tags

**Account / Subscription / Project level**:
- Budget alerts and spending limits
- Mandatory services (audit logging, security posture management)
- Deny deletion of audit log destinations

Document these as logical requirements — the cloud-specific skills translate them to SCPs, Azure Policy, or Organization Policies.

### Step 5 — Map Shared Services

Identify resources that exist outside the `(Sector, Tier, _, Tenant)` pattern because they are shared across multiple coordinates:

- **Hub network** / **Transit account**: Lives in the platform sector; provides connectivity between spokes.
- **Audit / Log archive**: Receives logs from all other accounts — lives in the security sector.
- **Identity**: Shared identity provider (Entra ID / AWS IAM Identity Center instance / Cloud Identity) that is not itself a workload account.
- **DNS root zone**: The authoritative root DNS zone for the internal domain, typically in the platform sector.

For each shared service, specify its coordinate (or note that it transcends a single coordinate), its owner, and which other nodes depend on it.

### Step 6 — Assess Operational Impact

State the operational consequence of the proposed structure:

- How many structural nodes (accounts/subscriptions/projects) does the platform team need to maintain?
- What is the estimated cost of the hierarchy itself (management overhead, minimum subscription/account fees)?
- What tooling is needed to manage it at scale? (e.g., AWS Control Tower, Azure Landing Zones accelerator, GCP Fabric FAST)

If the node count exceeds the team's realistic capacity, recommend a simpler structure and note when to evolve it.

### Step 7 — Review and Iterate

Present the hierarchy to the user. Ask:

- Does the structural depth match the isolation levels agreed in the segmentation design?
- Are all shared services correctly identified and placed?
- Is the operational cost of this structure acceptable?
- Are there compliance requirements that mandate a different structure?

Iterate until satisfied, then produce the final document.

## Output Format

Produce a Markdown document named `landing-zone-design.md`:

```markdown
# Landing Zone Design

## Structural Granularity

[Which coordinate dimensions map to hard structural boundaries vs. softer ones, and why]

## Organizational Hierarchy

### AWS (or Azure / GCP)

| Node | Type | Coordinate | Guardrails |
|------|------|-----------|-----------|
| Organization Root | — | — | Management only, no workloads |
| OU: Platform | OU | (platform, *) | Restrict to platform tooling services |
| Account: platform-sandbox | Account | (platform, sandbox) | Budget alert: $500/mo |
| Account: platform-live | Account | (platform, live) | Encryption required, no public resources |
| OU: ECommerce | OU | (ecommerce, *) | Deny regions outside eu01, us01 |
| Account: ecommerce-sandbox | Account | (ecommerce, sandbox) | Budget alert: $2000/mo |
| Account: ecommerce-live | Account | (ecommerce, live) | PCI scope, encryption required |
| Account: audit | Account | Security sector | Immutable log archive, no workloads |

## Shared Services

| Service | Location | Coordinate | Depends On |
|---------|----------|-----------|-----------|
| Hub network | Account: network-hub | ("platform", "live", "*) | Transit Gateway |
| Log archive | Account: audit | (security", "live") | All accounts |

## Guardrails Summary

### `Tier("sandbox")`
- [List of controls]

### `Tier("live")`
- [List of controls]

## Operational Assessment

- Total structural nodes: [count]
- Recommended management tooling: [e.g., AWS Control Tower, Azure Landing Zones]
- Evolution path: [when to add more structure]

## Assumptions and Open Questions
[Anything assumed or requiring further investigation]
```

## Principles to Apply

- **Structure serves isolation, not billing**: Design the hierarchy to enforce security boundaries. Use tags for cost attribution.
- **Management accounts hold no workloads**: The root management account, organization admin, or tenant root is for governance only. A compromised workload in the root account can affect everything.
- **Dedicated audit accounts are non-negotiable**: Every cloud provider recommends a separate, immutable log-archive account. If a workload account is compromised, the audit trail must remain intact.
- **Operational capacity is a hard constraint**: An elegant hierarchy that requires fifty accounts is counterproductive for a team of three. Start with `(Sector, Tier)` accounts and evolve toward tenant-level accounts as headcount and compliance demands grow.
- **Use provider accelerators**: AWS Control Tower, the Azure Landing Zones reference architecture, and GCP Fabric FAST are production-proven implementations of these patterns. Do not reinvent the wheel.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
