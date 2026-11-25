---
name: define-naming-convention
description: >
  Define the resource naming pattern and mandatory tagging schema for the platform, derived
  from the Platform Notation. Produces a naming-convention.md document that all
  subsequent skills (landing zone, networking, compute, IaC modules) use as their authoritative
  source of truth for names and tags. Use after design-segmentation and before any
  provisioning skill.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Define Naming Convention

## Skill Type

Design

## Your Goal

Produce a **naming convention document** — a single source of truth for how every resource in the platform is named and tagged. All downstream skills and IaC modules derive their naming from this document. A good convention makes the coordinate of any resource immediately readable from its name, without querying the cloud console.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Segmentation design**: The output of `design-segmentation` — Sectors, Tiers, Regions, Tenants, and their short identifiers. This drives the naming tokens.
- **Cloud provider(s)**: AWS, Azure, GCP, or multi-cloud. Each provider has different naming constraints (character limits, allowed characters, case sensitivity).
- **Company domain / prefix**: The short company identifier used as a prefix or in DNS names (e.g., `mountainlab`, `ml`).
- **Globally-unique resource types in scope**: Some resource types (S3 bucket names, storage account names) must be globally unique and cannot follow a predictable pattern alone — agree on the suffix strategy (random hash, region code, account ID).
- **Existing conventions**: Are there existing naming patterns in the organization? Adopting or extending them reduces friction.

## Process

### Step 1 — Define Coordinate Tokens

Map each coordinate dimension to a canonical short token:

| Dimension | Full Value | Short Token |
|-----------|-----------|------------|
| Sector | `platform` | `platform` (or `plt` if length is constrained) |
| Sector | `ecommerce` | `ecom` |
| Tier | `sandbox` | `sbx` |
| Tier | `live` | `live` |
| Region | `eu01` | `eu01` (already short — keep as is) |
| Tenant | `payments` | `pay` (only if length requires abbreviation) |

Prefer full names where character limits allow. Use abbreviations only when a cloud provider's limit forces it (e.g., Azure storage account names: 24 characters). Document the full-to-short mapping table for every token in use — engineers must never need to guess.

### Step 2 — Define the Naming Pattern per Resource Type

For each resource category, define:
- The token order (coordinate dimensions included, and their order)
- A separator character (`-` is recommended; avoid `_` where provider constraints exist)
- Any prefix/suffix conventions (type prefix recommended for human readability)

**Structural resources** (accounts, subscriptions, projects, OUs, folders):
```
{sector}-{tier}                          # ecommerce-live
{tenant}-{tier}                          # payments-live (tenant-level accounts)
```

**Network resources** (VPCs, VNets, subnets):
```
vnet-{sector}-{tier}-{region}            # vnet-ecommerce-live-eu01
subnet-{visibility}-{sector}-{tier}-{region}  # subnet-private-ecommerce-live-eu01
tgw-{sector}-{tier}-{region}             # tgw-platform-live-eu01
```

**Compute resources** (clusters, node pools, namespaces):
```
k8s-{sector}-{tier}-{region}             # k8s-ecommerce-live-eu01
nodepool-{purpose}-{sector}-{tier}       # nodepool-general-ecommerce-live
ns-{tenant}                              # ns-payments (inside a tier-scoped cluster)
```

**Security resources** (key vaults, secret managers, KMS keys):
```
kv-{tenant}-{tier}-{region}              # kv-payments-live-eu01
```

**Globally-unique resources** (S3 buckets, Azure storage accounts):
```
{tenant}-{tier}-{region}-{random-hex}    # payments-live-eu01-a3f7
```
The random suffix prevents name collision while preserving readability of the coordinate. Generate the suffix at provisioning time and store it in state.

**DNS zones**:
```
Internal: {region}.{tier}.internal.{sector-domain}    # eu01.live.internal.ecommerce.mountainlab.io
Public:   {region}.{tier}.{sector-domain}             # eu01.live.ecommerce.mountainlab.io
```

**IAM entities** (roles, service accounts, managed identities):
```
{tenant}-{tier}-{role}                   # payments-live-operator
{sector}-{tier}-{role}                   # platform-sandbox-admins
```

Adapt these patterns for each cloud provider's syntax. Document any provider-specific deviations.

### Step 3 — Define the Mandatory Tag Schema

Tags are the metadata layer on top of the naming convention — they make the coordinate queryable by automation, cost tooling, and compliance scanners. Define the mandatory tags that every resource must carry.

**Company-prefixed tag keys** prevent collision with cloud provider reserved tags:

| Tag Key | Value Type | Example | Purpose |
|---------|-----------|---------|---------|
| `{company}:tenant` | string | `payments` | Cost attribution and RBAC scope |
| `{company}:sector` | string | `ecommerce` | Policy scoping |
| `{company}:tier` | string | `live` | Policy scoping, lifecycle rules |
| `{company}:region` | string | `eu01` | Data residency queries |
| `{company}:tf-module` | string | `k8s-namespace` | IaC traceability |
| `{company}:tf-module-version` | string | `1.4.2` | IaC traceability and drift detection |

Replace `{company}` with the company's short identifier (e.g., `mountainlab:tenant`).

**Provider-specific syntax notes**:
- AWS and Azure tags use the format `key=value`; colons in key names are valid.
- GCP labels use `key=value` with lowercase keys, hyphens, and no colons — adapt key names: `mountainlab-tenant` instead of `mountainlab:tenant`.
- Kubernetes labels use `prefix/key=value` syntax — use `mountainlab.io/tenant`.

Define whether tags are enforced via cloud guardrails (SCPs, Azure Policy, Org Policies) or applied by convention. Recommend enforcement: unenforced tagging policies drift within months.

### Step 4 — Define the Kubernetes Annotation and Label Schema

For resources inside Kubernetes clusters, define:

**Namespace labels** (applied by the platform to every managed namespace):
```yaml
labels:
  mountainlab.io/tenant: payments
  mountainlab.io/sector: ecommerce
  mountainlab.io/tier: live
  mountainlab.io/region: eu01
```

**Workload labels** (expected on every Deployment, StatefulSet, etc. — enforced via admission webhook):
```yaml
labels:
  app.kubernetes.io/name: payment-processor
  app.kubernetes.io/version: "1.4.2"
  mountainlab.io/tenant: payments
```

The `app.kubernetes.io/` labels are Kubernetes community conventions — use them. The `{company}.io/` labels carry platform coordinate metadata.

### Step 5 — Document Character Limit Constraints

For each cloud provider, document the naming constraints for the resource types in scope:

| Provider | Resource Type | Max Length | Allowed Characters | Case |
|----------|--------------|-----------|-------------------|------|
| Azure | Resource Group | 90 | alphanumeric, hyphens, underscores, periods | Case-insensitive |
| Azure | Storage Account | 24 | alphanumeric only | Lowercase |
| AWS | S3 Bucket | 63 | alphanumeric, hyphens | Lowercase |
| AWS | IAM Role | 64 | alphanumeric, `_`, `+`, `=`, `.`, `@`, `-` | Case-sensitive |
| GCP | Project ID | 30 | lowercase alphanumeric, hyphens | Lowercase |
| GCP | Label key | 63 | lowercase alphanumeric, hyphens, underscores | Lowercase |
| Kubernetes | Namespace | 63 | alphanumeric, hyphens | Lowercase |

Flag any naming pattern that would breach a limit for a given resource type and propose an abbreviated form.

### Step 6 — Review and Iterate

Present the convention to the user. Ask:

- Does the token order feel natural to engineers reading resource names?
- Are there existing naming patterns in the organization that should be incorporated?
- Are there resource types missing from the pattern table?
- Are all mandatory tags aligned with what the FinOps team needs for cost attribution?

Iterate until satisfied.

## Output Format

Produce a Markdown document named `naming-convention.md`:

```markdown
# Platform Naming Convention

## Coordinate Tokens

| Dimension | Value | Token |
|-----------|-------|-------|
| Sector | platform | platform |
| Sector | ecommerce | ecom |
| Tier | sandbox | sbx |
| Tier | live | live |
| Region | eu01 | eu01 |

## Naming Patterns

### Structural Resources
| Resource Type | Pattern | Example |
|---------------|---------|---------|
| AWS Account | `{sector}-{tier}` | `ecommerce-live` |
| Azure Subscription | `sub-{sector}-{tier}` | `sub-ecommerce-live` |
| GCP Project | `{sector}-{tier}` | `ecommerce-live` |

### Network Resources
| Resource Type | Pattern | Example |
|---------------|---------|---------|
| VPC / VNet | `vnet-{sector}-{tier}-{region}` | `vnet-ecommerce-live-eu01` |

### Compute Resources
[...]

### Globally-Unique Resources
[Pattern with random suffix strategy]

### DNS Zones
[Internal and public zone patterns]

## Tag Schema

| Tag Key | Value Type | Example | Mandatory |
|---------|-----------|---------|-----------|
| `mountainlab:tenant` | string | `payments` | Yes |
| `mountainlab:sector` | string | `ecommerce` | Yes |
| `mountainlab:tier` | string | `live` | Yes |
| `mountainlab:region` | string | `eu01` | Yes |
| `mountainlab:tf-module` | string | `k8s-namespace` | Yes |
| `mountainlab:tf-module-version` | string | `1.4.2` | Yes |

## Kubernetes Labels and Annotations

[Namespace label schema and workload label schema]

## Provider Constraint Notes

[Any deviations from the standard pattern due to character limits]

## Assumptions and Open Questions
[...]
```

## Principles to Apply

- **Coordinate readable from the name**: An engineer seeing `vnet-ecommerce-live-eu01` must immediately know the sector, tier, and region without looking it up.
- **Tags complement names, not replace them**: Tags are queryable metadata; names are human-readable identifiers. Both are needed.
- **Globally-unique resources need a suffix strategy**: Predictable names are great until they collide. Random hex suffixes preserve readability while guaranteeing uniqueness.
- **Provider-agnostic keys, provider-specific syntax**: Use the same logical tags everywhere (`tenant`, `sector`, `tier`) and adapt only the key syntax per provider (colons for AWS/Azure, hyphens for GCP, slash notation for Kubernetes).
- **Enforce or expect drift**: Unenforced tagging policies become optional suggestions within a quarter. Design guardrails (SCPs, Azure Policy, Org Policies) that deny resource creation without mandatory tags.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
