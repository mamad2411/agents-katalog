---
name: manage-azure-landing-zone
description: >
  Provision and sync the Azure landing zone — Management Groups, Subscriptions, Resource Groups,
  Azure Policy assignments, and budget alerts — from a landing-zone-design.md and
  naming-convention.md. Uses the Azure MCP server. Use when applying or updating the Azure
  cloud structure after running design-landing-zone.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage Azure Landing Zone

## Skill Type

Implementation

## System Requirements

- **Azure MCP server** configured and authenticated. The agent will use Azure MCP tools to call Azure Resource Manager, Management Groups, Subscriptions, and Policy APIs.
- The executing identity must have:
  - `Management Group Contributor` at the Tenant Root Group (or `Owner` if Policy assignments need to be created)
  - `Billing Account Owner` or `Enrollment Account Owner` (for Subscription creation via EA or MCA)
  - `Microsoft.Authorization/policyAssignments/write` at the Management Group scope
- The Entra ID tenant must already exist.

## Your Goal

Apply the landing zone definition from `landing-zone-design.md` to Azure. Ensure that:

1. Management Group hierarchy exists and matches the design.
2. All Subscriptions are created and placed under the correct Management Groups.
3. Resource Groups exist per full coordinate `(Sector, Tier, Region, Tenant)`.
4. Azure Policy assignments enforce the guardrails defined in the design.
5. Budget alerts are configured per Subscription.

This skill is **idempotent**: running it multiple times produces the same result.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Landing zone design**: Path to `landing-zone-design.md`. Read it first.
- **Naming convention**: Path to `naming-convention.md`. All resource names must follow it.
- **Entra ID tenant ID**: Required for Management Group and Subscription APIs.
- **Billing account**: EA enrollment account ID or MCA billing profile for Subscription provisioning. Confirm that the executing identity has access.
- **Azure Regions**: The short Azure region names mapping from the naming convention (e.g., `eu01` → `westeurope`).
- **Scope of this run**: Full landing zone, specific Management Groups, or specific Subscriptions?
- **Dry-run mode**: Recommended for first-time runs.

Read both input documents before proceeding.

## Process

### Step 1 — Read and Validate Design Documents

Read `landing-zone-design.md` and `naming-convention.md`. Extract:
- Management Group names and hierarchy
- Subscription names and parent Management Groups
- Resource Group names and coordinates
- Guardrail requirements per structural level
- Budget amounts per Subscription

Validate that all names conform to the naming convention and Azure naming constraints (Management Group display name ≤ 90 chars, Subscription name ≤ 64 chars, Resource Group name ≤ 90 chars).

### Step 2 — Provision Management Group Hierarchy

For each Management Group in the design:
1. Check whether it exists using the Azure MCP.
2. Create it under the correct parent if missing.
3. Set the display name per the naming convention.

Do not delete Management Groups not in the design without explicit user confirmation.

### Step 3 — Provision Subscriptions

For each Subscription in the design:
1. Check whether a Subscription with the declared name exists and is placed under the correct Management Group.
2. If missing, create it via the Billing API (EA or MCA). Note: Subscription creation may require additional approvals in some billing configurations — flag this if the API returns a pending state.
3. Move the Subscription to the correct Management Group if it exists but is misplaced.
4. Tag the Subscription with the mandatory tags from the naming convention (`sector`, `tier`).

### Step 4 — Assign Azure Policies

For each Management Group and Subscription, apply the guardrails from the design as Azure Policy assignments:

**Recommended built-in policies to assign at Management Group (Sector) level**:
- `Require a tag and its value on resources` — for each mandatory tag in the naming convention
- `Allowed locations` — restrict resource creation to declared regions
- `Azure Security Benchmark` (or a custom initiative) — enforce baseline security controls

**`Tier("live")` Subscription level**:
- `Secure transfer to storage accounts should be enabled`
- `Transparent Data Encryption on SQL databases should be enabled`
- `Audit VMs that do not use managed disks`
- `Public network access should be disabled for [resource types in scope]`

**`Tier("sandbox")`** — more permissive; assign only tagging and location policies.

For each assignment:
1. Check whether the assignment already exists at the target scope.
2. Create it if missing. Assign a system-assigned managed identity for `DeployIfNotExists` or `Modify` policies.
3. Set the assignment to `Deny` or `Audit` mode per the design (prefer `Audit` first, then escalate to `Deny` after validation).

### Step 5 — Provision Resource Groups

For each Resource Group in the design (typically one per full coordinate `(Sector, Tier, Region, Tenant)`):
1. Check whether it exists in the correct Subscription.
2. Create it in the correct Azure region (mapped from the naming convention) if missing.
3. Apply all mandatory tags.

### Step 6 — Configure Budget Alerts

For each Subscription, configure a budget alert:
1. Check whether a budget already exists.
2. Create a monthly budget with the threshold from the design.
3. Add alert thresholds at 80% and 100% of the budget.
4. Configure notifications to the platform team's email or action group.

### Step 7 — Report

Produce a summary:
- Management Groups created / already existed
- Subscriptions created / moved / already existed
- Resource Groups created / already existed
- Policy assignments created / already existed
- Budget alerts created / already existed
- Items skipped with reason
- Any naming violations or constraint breaches found

In dry-run mode, produce the report without making changes.

## Output Format

Produce a Markdown report named `azure-landing-zone-report.md`:

```markdown
# Azure Landing Zone Sync Report

**Date**: [timestamp]
**Mode**: [applied / dry-run]

## Management Groups

| Name | Parent | Status |
|------|--------|--------|
| mg-platform | Tenant Root | created |
| mg-ecommerce | Tenant Root | exists |

## Subscriptions

| Name | Management Group | Status |
|------|-----------------|--------|
| sub-ecommerce-live | mg-ecommerce | created |
| sub-platform-sandbox | mg-platform | exists |

## Resource Groups

| Name | Subscription | Region | Status |
|------|-------------|--------|--------|
| rg-payments-eu01-live | sub-ecommerce-live | westeurope | created |

## Policy Assignments

| Policy | Scope | Mode | Status |
|--------|-------|------|--------|
| Require tag: mountainlab:tenant | mg-ecommerce | Deny | created |

## Budget Alerts

| Subscription | Amount | Status |
|-------------|--------|--------|
| sub-ecommerce-live | $5,000/mo | created |

## Open Items
[Subscription creation pending billing approval, policy remediation tasks, etc.]
```

## Principles to Apply

- **Management accounts hold no workloads**: The Tenant Root Group and top-level Management Groups contain only governance resources. Workloads live in Subscriptions, not Management Groups.
- **Policies at Management Group level cascade**: A policy at `mg-ecommerce` applies to all child Subscriptions and Resource Groups. Assign at the highest applicable level.
- **Audit before Deny**: When introducing a new policy, start with `Audit` mode to understand the impact. Escalate to `Deny` after validating that compliant resources are not blocked.
- **Idempotent by design**: Check state before creating. Never delete structural resources without explicit user confirmation.
- **Use Azure Landing Zones accelerator**: For large deployments, reference the Azure Landing Zones Bicep/Terraform accelerator rather than reimplementing the full hierarchy from scratch.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
