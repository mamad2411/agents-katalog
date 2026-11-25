---
name: design-segmentation
description: >
  Design a platform segmentation strategy — defining Sectors, Tiers, Regions, and Tenants —
  and produce a Platform Notation document tailored to the organization's scale,
  cloud provider, and regulatory requirements. Use when starting a new platform, formalizing
  an ad-hoc environment structure, or evaluating whether the current segmentation model fits
  the organization's growth stage.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "4"
---

# Design Segmentation

## Skill Type

Design

## Your Goal

Produce a **segmentation design document** — a structured record of the organization's boundary model: which Sectors exist, how Tiers are defined, which Regions are in scope, and how Tenants are isolated. The document must include a **Platform Notation** (the `(Sector, Tier, Region, Tenant)` formula), a cloud structure mapping, an isolation level recommendation for each dimension, and rationale for every decision.

The output should be concrete enough for a platform engineer to begin provisioning cloud accounts, subscriptions, or projects from it.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Organization profile**: Company name, industry, size (number of engineers and teams), cloud provider(s) — AWS, Azure, GCP, or multi-cloud.
- **Business domains**: How many distinct lines of business or product areas exist? Do they have fundamentally different security postures (e.g., a regulated payments domain alongside a general e-commerce domain)?
- **Environment requirements**: What environments do teams currently use? (e.g., `dev`, `qa`, `staging`, `prod`) — understand the intent behind each, not just the names.
- **Regulatory requirements**: Any compliance mandates — PCI-DSS, HIPAA, GDPR, SOC 2, FedRAMP? Do any frameworks require physical isolation of specific workloads?
- **Data residency requirements**: Must any data stay within a specific geographic region or jurisdiction? Any latency requirements that drive multi-region deployment?
- **Tenant model**: Are tenants internal teams, external B2B customers, or both? How many tenants are expected now and at scale?
- **Operational capacity**: How large is the platform team? How many separate cloud accounts/subscriptions/projects can they realistically manage today?
- **Current state**: What does the existing environment structure look like? What problems has it caused? (e.g., noisy neighbors, compliance failures, runaway costs)

If the user cannot answer all questions, proceed with available information and note assumptions explicitly in the output.

## Process

### Step 1 — Assess Organizational Maturity and Momentum

Before recommending a segmentation model, calibrate to the organization's current reality:

- **Startup (Pre-Product Market Fit)**: Minimal segmentation is appropriate. Over-engineering here stalls product development.
- **Scale-up (Growth Phase)**: Introduce `Sector("platform")`. Add Tenant isolation logically (namespaces, resource groups) as headcount grows. Begin moving critical boundaries up the isolation spectrum.
- **Enterprise / Heavily Regulated**: Implement all four dimensions with hard physical boundaries. Account-per-`(Sector, Tier)` at minimum. Microsegmentation within segments. Strict network isolation to satisfy compliance auditors.

Document the maturity tier and its implications for scope. A startup does not need the same model as a regulated enterprise — and proposing one for the other is a mistake.

### Step 2 — Define Sectors

Sectors separate the *engineering platform domain* from the *business domain*. Identify:

- **Engineering sectors**: Internal enablement and platform tooling (CI/CD runners, observability stack, identity management, security tooling). Recommend at least one `Sector("platform")`. If the organization handles regulated data, recommend a dedicated `Sector("security")` for log archives, SIEM, and audit systems.
- **Business sectors**: Workloads that generate revenue. If the company has multiple distinct lines of business (Retail, Finance, Insurance), propose a separate sector per line of business. If there is one product, one business sector is sufficient.

For each sector, specify:
- Its name and purpose
- Who owns it (which team)
- What type of workloads it hosts
- Why it is separated (compliance boundary, resilience requirement, or team ownership)

::: note
Sectors are not organizational units — they are technical boundaries. A single team can operate workloads in multiple sectors (e.g., a security team that also runs platform tooling).
:::

### Step 3 — Define Tiers

Tiers separate workloads by criticality and data classification. Do not simply rename the organization's existing `dev/qa/staging/prod` labels — reason about them from first principles:

- What is the **blast radius** if this tier fails?
- What **data** does it process — synthetic, anonymized, or real customer data?
- What **access model** does it require — open for experimentation, or strictly controlled?

Recommend two tiers as the baseline:

- **`Tier("sandbox")`**: Non-production. Synthetic or anonymized data. Engineers have freedom to experiment. Access policies are relaxed. Contains the organization's existing `dev`, `qa`, and `staging`-equivalent environments as logical sub-spaces.
- **`Tier("live")`**: Production. Real customer data. Strictly controlled access. All changes flow through automated pipelines. Break-glass access only for humans. Contains `staging` (final pre-production validation) and `prod`.

If the organization has strict regulatory requirements — PCI-DSS cardholder data environments, HIPAA covered data — propose additional tiers or sub-tiers as warranted and explain why.

For each tier, specify:
- Its name and the data classification it handles
- Its access model (who can access, how, and under what conditions)
- Whether it corresponds to a hard physical boundary (separate account/subscription) or a logical one

### Step 4 — Define Regions

Map the organization's geographic deployment requirements to a **provider-agnostic naming convention**. Use short codes (`eu01`, `us01`, `ap01`) rather than cloud-specific names (`us-east-1`, `East US 2`). This insulates the coordinate system from provider lock-in and makes coordinates readable by developers regardless of which cloud they use.

For each region in scope:

- **Internal name**: e.g., `eu01`
- **Cloud mapping**: e.g., `eu01` → AWS `eu-west-1`, Azure `West Europe`, GCP `europe-west1`
- **Reason for inclusion**: latency, data residency, regulatory requirement, or high availability
- **Region groups**: If the organization has resources that span multiple regions but must stay within a geographic boundary (e.g., `europe`, `americas`), define named groups. Include a `global` group if applicable.

If the organization currently operates in a single region with no regulatory requirements, recommend one region and note when to revisit (multi-region availability or expansion to a regulated geography).

### Step 5 — Define Tenants

Tenants isolate workloads by owner. Identify whether tenants are:

- **Internal teams**: Engineering teams owning microservices or products (e.g., `payments`, `recommendations`, `identity`)
- **External customers**: B2B clients requiring dedicated infrastructure and data isolation

For each tenant type:
- How many tenants exist today, and how many are expected at a 2–3 year horizon?
- What isolation level do they require? (See Step 6)
- What cost attribution requirements exist? (Tenants should map to a billing boundary)

List the initial set of tenants for each business sector. For platform sectors, tenants are typically internal teams (e.g., the platform team itself, security team).

### Step 6 — Assign Isolation Levels

For each dimension, recommend an isolation level on the spectrum:

| Level | Name | Cloud Examples | Compute Examples |
|:-----:|:-----|:---------------|:-----------------|
| 1 | Air-Gapped | Disconnected DC, sovereign cloud | N/A |
| 2 | Dedicated Hardware | Dedicated Hosts, Outposts, Azure Stack | Dedicated node pools |
| 3 | Account / Subscription / Project | AWS Account, Azure Subscription, GCP Project | Separate cluster per account |
| 4 | Separate Network | VPC / VNet with no default routing | Cluster-per-tenant |
| 5 | Resource Group / Logical Partition | Azure Resource Group, GCP project-within-folder | Virtual clusters |
| 6 | Namespace / Logical Container | — | K8s Namespace + RBAC + NetworkPolicy + Quotas |

Guidance:
- **Sector and Tier**: Use the hardest boundary the operational capacity allows — Level 3 (account/subscription) at minimum.
- **Region**: Level 4 (separate network/VPC per region) is the recommended default.
- **Tenant**: Level 5–6 is acceptable for most organizations. Level 3–4 for regulated workloads (e.g., PCI-DSS cardholder data environment).

Document the isolation level per dimension, the reason for the choice, and any known exceptions. Highlight where a **bridge model** applies — different resource types at the same coordinate using different isolation levels (e.g., silo database, pool compute).

**Important**: Tags and labels are overlays, not boundaries. Never recommend tag-based access control for isolation — it is inconsistent across cloud providers and silently fails on misconfiguration.

### Step 7 — Define the Coordinate Notation

Summarize the **Platform Notation** as a formula:

```
(Sector, Tier, Region, Tenant)
```

Explain the two special symbols:
- `*` (wildcard): all values of a dimension — used in policy scope definitions (e.g., a policy at `("ecommerce", "live", "*", "*")` applies to all regions and tenants within that subscription)
- `_` (ignore): dimension is not relevant for the resource being described (e.g., an AWS Account exists at `("ecommerce", "live", "_", "payments")` — it is tenant-scoped but not region-scoped)

Provide a naming convention for cloud resources derived from the coordinate. Example: `rg-{tenant}-{region}-{tier}` for Azure Resource Groups, or `{tenant}-{tier}` for AWS Account names. The naming should make the coordinate readable from the resource name alone.

### Step 8 — Flag Cross-Cutting Concerns

Briefly address these overlays — they shape how segments are configured without adding new dimensions:

- **Data Classification**: Which coordinate ranges handle Restricted or Confidential data? These may need stricter isolation levels.
- **Identity Alignment**: Are separate identity tenants or directories needed per Sector or Tier? `Tier("sandbox")` and `Tier("live")` should use separate identity boundaries.
- **Cost Attribution**: Which coordinate dimension maps to a billing boundary? Confirm that the cloud structure enables accurate cost attribution per tenant.
- **CI/CD Pipeline Isolation**: Build runners in `Tier("sandbox")` must not access `Tier("live")` secrets. State the principle and note it will be addressed in the CI/CD chapter.

### Step 9 — Review and Iterate

Present the complete design to the user. Ask:

- Does the Sector breakdown reflect real ownership boundaries in the organization?
- Are the Tiers named and defined in a way the engineering team will respect and understand?
- Does the Region list match current and planned deployment targets?
- Is the proposed isolation level achievable with the current platform team size?
- Are there any compliance requirements not yet accounted for?

Iterate until the user is satisfied, then produce the final document.

## Output Format

Produce a single Markdown document named `segmentation-design.md` with this structure:

```markdown
# Platform Segmentation Design

## Organization Context
[Brief summary of the organization profile, maturity tier, and key constraints]

## Sectors
| Sector | Owner | Purpose | Compliance Notes |
|--------|-------|---------|-----------------|
| platform | Platform Team | CI/CD, monitoring, identity | — |
| ecommerce | Product Teams | Business workloads | PCI-DSS scope if applicable |

## Tiers
| Tier | Data Classification | Access Model | Physical Boundary |
|------|--------------------|--------------|--------------------|
| sandbox | Synthetic / Anonymized | Open (engineers) | Separate account/subscription |
| live | Confidential / Restricted | Controlled (pipelines + break-glass) | Separate account/subscription |

## Regions
| Internal Name | Cloud Mapping | Purpose |
|---------------|--------------|---------|
| eu01 | AWS eu-west-1 / Azure West Europe / GCP europe-west1 | GDPR data residency |
| us01 | AWS us-east-1 / Azure East US / GCP us-east1 | Primary market |

## Tenants
### [Sector Name]
| Tenant | Type | Owner | Notes |
|--------|------|-------|-------|
| payments | Team | Payments Squad | PCI-DSS scope |
| recommendations | Team | ML Platform | — |

## Platform Notation

Every resource is addressed by `(Sector, Tier, Region, Tenant)`.

### Example Coordinates
- `("ecommerce", "live", "eu01", "payments")` — Payments team, European production
- `("platform", "sandbox", "us01", "*")` — all platform tooling in US sandbox

### Resource Naming Convention
[Convention derived from the coordinate, e.g., `{tenant}-{tier}` for accounts, `rg-{tenant}-{region}-{tier}` for resource groups]

## Cloud Structure Mapping

### [Cloud Provider]
[Hierarchy diagram or table mapping cloud primitives to coordinate dimensions]

## Isolation Levels
| Dimension | Recommended Level | Boundary Type | Rationale |
|-----------|------------------|---------------|-----------|
| Sector | 3 | Account / Subscription | Compliance and resilience isolation |
| Tier | 3 | Account / Subscription | Data classification boundary |
| Region | 4 | VPC / VNet | Network isolation, data residency |
| Tenant | 5–6 | Resource Group / Namespace | Cost attribution, access scoping |

## Bridge Model Exceptions
[Any resource types where isolation levels differ from the dimension recommendation]

## Cross-Cutting Concerns
- **Data Classification**: [Which coordinates handle Restricted data]
- **Identity Alignment**: [Separate identity tenants or directories per Tier]
- **Cost Attribution**: [How billing is tracked by coordinate]
- **CI/CD Isolation**: [Principle and forward reference to CI/CD chapter]

## Assumptions and Open Questions
[Anything assumed or requiring further investigation before implementation]

## Next Steps
- **Landing zone**: Use the `design-landing-zone` skill to map this coordinate system to cloud
  provider primitives (accounts, subscriptions, projects, OUs, folders).
- **Networking**: Use the `design-networking` skill to plan the hub-and-spoke topology, IPAM
  allocation, and DNS zones.
- **Compute**: Use the `design-compute` skill to plan the Kubernetes cluster topology, node
  pools, and quota templates.
- **IAM**: Use the `define-core-iam` and `define-tenant-iam` skills to define the access model.
```

## Principles to Apply

- **Blast radius first**: Every segmentation decision should answer "what fails when this boundary is breached?" Start from the worst-case scenario and work backward.
- **Hard boundaries for Sector and Tier, soft for Region and Tenant**: The Sector and Tier segmentation defines your strongest physical isolation. Region and Tenant can be softer while still effective.
- **Tags are overlays, not boundaries**: Never use tag-based access control for isolation. Tags enrich the coordinate system with metadata — they do not enforce it.
- **Name coordinates into resources**: A developer reading `db.payments.eu01.live.internal.mountainlab.io` should immediately know the security posture and criticality of that resource. Design naming conventions that make coordinates readable.
- **Operational capacity is a constraint**: A model that requires fifty separate accounts is useless to a platform team of two. Match segmentation depth to team capacity, then evolve.
- **Bridge models are the norm**: Most real-world platforms use different isolation levels for different resource types at the same coordinate. A silo database alongside a pool compute cluster is a valid and common pattern.
- **Start simple, evolve deliberately**: Apply the minimum segmentation that solves the immediate blast-radius and compliance problem. Add dimensions as organizational complexity demands — not in anticipation of it.

## Related Chapter(s)

This skill is grounded in **Chapter 4: Segmentation** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
