---
name: manage-gcp-landing-zone
description: >
  Provision and sync the GCP landing zone — Organization, Folders, Projects, Organization
  Policies, Billing Account links, and budget alerts — from a landing-zone-design.md and
  naming-convention.md. Uses the GCP MCP server. Use when applying or updating the GCP cloud
  structure after running design-landing-zone.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage GCP Landing Zone

## Skill Type

Implementation

## System Requirements

- **GCP MCP server** configured and authenticated. The agent will use GCP MCP tools to call Resource Manager, Organization Policy, Billing, and Cloud Asset APIs.
- The executing identity must have at the Organization level:
  - `resourcemanager.folders.create`, `resourcemanager.folders.update`
  - `resourcemanager.projects.create`, `resourcemanager.projects.move`
  - `orgpolicy.policies.create`, `orgpolicy.policies.update`
  - `billing.accounts.getIamPolicy`, `billing.accounts.setIamPolicy`
  - `billing.resourceAssociations.create` (to link projects to billing accounts)
  - `budgets.budgets.create`, `budgets.budgets.update`
- The GCP Organization must already exist (requires a Google Workspace or Cloud Identity domain).

> **Note**: For large deployments, consider using GCP Fabric FAST or the Google Cloud Landing Zones blueprint rather than provisioning resources individually.

## Your Goal

Apply the landing zone definition from `landing-zone-design.md` to GCP. Ensure that:

1. Folder hierarchy exists and matches the design.
2. All Projects are created and placed under the correct Folders.
3. Organization Policies enforce the guardrails at the correct resource levels.
4. Projects are linked to the correct Billing Account.
5. Budget alerts are configured per Project.

This skill is **idempotent**.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Landing zone design**: Path to `landing-zone-design.md`. Read it first.
- **Naming convention**: Path to `naming-convention.md`.
- **GCP Organization ID**: Required for all resource hierarchy operations.
- **Billing Account ID**: All projects must be linked to a Billing Account for resources to be provisioned.
- **GCP Regions**: The mapping from the naming convention's region tokens (e.g., `eu01`) to GCP region names (e.g., `europe-west1`).
- **Scope of this run**: Full organization, specific Folders, or specific Projects?
- **Dry-run mode**: Recommended for first-time runs.

Read both input documents before proceeding.

## Process

### Step 1 — Read and Validate Design Documents

Read `landing-zone-design.md` and `naming-convention.md`. Extract:
- Folder names and hierarchy
- Project names, parent Folders
- Organization Policy requirements per resource level
- Budget amounts per Project

Validate that all names conform to GCP naming constraints:
- Folder display name: ≤ 30 characters
- Project ID: ≤ 30 characters, globally unique, lowercase alphanumeric and hyphens
- Label key: ≤ 63 characters, lowercase, hyphens and underscores only (no colons)

Note that GCP Project IDs are globally unique and immutable — once created, they cannot be renamed. Confirm the proposed IDs before proceeding.

### Step 2 — Provision Folder Hierarchy

For each Folder in the design:
1. Check whether it exists under the correct parent using the GCP MCP.
2. Create it if missing. Set the display name per the naming convention.
3. Keep the folder hierarchy as flat as possible — GCP recommends ≤ 3 levels of nesting. Deeper nesting adds policy inheritance complexity.

Do not delete Folders not in the design — Folders containing Projects cannot be deleted.

### Step 3 — Provision Projects

For each Project in the design:
1. Check whether a Project with the declared ID already exists.
2. Create it under the correct parent Folder if missing. Project creation is asynchronous — poll for completion.
3. Move the Project to the correct Folder if it exists but is misplaced.
4. Link the Project to the Billing Account — without a billing link, most GCP APIs are unavailable.
5. Apply mandatory labels from the naming convention (`sector`, `tier`, etc.). Remember: GCP uses label keys without colons — adapt from the naming convention's tag keys accordingly.

**Required projects beyond the design**:
- Verify the `audit` project exists in the Security folder and has a centralized log sink.
- Verify the `connectivity` project (Shared VPC host) exists in the Platform folder.

### Step 4 — Apply Organization Policies

Organization Policies constrain what can be configured within the GCP resource hierarchy. Apply constraints from the guardrail requirements in the design.

**Recommended constraints at Organization level**:
- `constraints/compute.disableSerialPortAccess` — deny serial port access to VMs
- `constraints/iam.disableServiceAccountKeyCreation` — prevent long-lived service account keys
- `constraints/iam.disableServiceAccountKeyUpload` — prevent external key upload
- `constraints/iam.allowedPolicyMemberDomains` — restrict IAM members to the organization's domain
- `constraints/storage.uniformBucketLevelAccess` — enforce uniform bucket-level access on Cloud Storage

**At Sector Folder level**:
- `constraints/gcp.resourceLocations` — restrict resource creation to declared regions

**At `Tier("live")` Folder level**:
- `constraints/compute.requireShieldedVm` — require Shielded VM on all Compute Engine instances
- `constraints/sql.restrictPublicIp` — deny public IP assignment to Cloud SQL instances

**`Tier("sandbox")`** — more permissive; omit compute security constraints to allow faster iteration.

For each constraint:
1. Check whether the policy is already set at the target resource scope.
2. Create or update the policy if missing or mismatched.
3. Note that Organization Policy changes can take several minutes to propagate — document this in the report.

### Step 5 — Configure Centralized Audit

For the audit project:
1. Create a centralized log sink at the Organization level that exports all audit logs to a Cloud Storage bucket in the audit project.
2. Enable the log sink for: Admin Activity audit logs, Data Access audit logs (for sensitive projects), System Event logs.
3. Set the bucket's retention policy (object hold, minimum 7 years for compliance).
4. Enable Security Command Center at the Organization level and designate the audit project as the findings destination.

### Step 6 — Configure Budget Alerts

For each Project, configure a budget:
1. Check whether a budget already exists for the project.
2. Create a monthly budget with the threshold from the design, linked to the project's Billing Account subaccount.
3. Add alert thresholds at 50%, 80% (actual spend), and 100% (forecasted).
4. Send notifications to the platform team via Pub/Sub or email.

Note: GCP billing budgets are created on the Billing Account, filtered by project. Ensure the Billing Account permits the executing identity to manage budgets.

### Step 7 — Report

Produce a summary:
- Folders created / already existed
- Projects created / moved / linked to billing / already existed
- Organization Policies applied / already existed / propagation pending
- Audit configuration status
- Budget alerts created / already existed
- Items skipped with reason
- Any naming validation failures (e.g., Project ID too long or already taken globally)

In dry-run mode, produce the report without making changes.

## Output Format

Produce a Markdown report named `gcp-landing-zone-report.md`:

```markdown
# GCP Landing Zone Sync Report

**Date**: [timestamp]
**Mode**: [applied / dry-run]
**Organization ID**: [org-id]

## Folders

| Display Name | Parent | Status |
|-------------|--------|--------|
| Platform | Organization | created |
| ECommerce | Organization | exists |

## Projects

| Project ID | Folder | Billing Linked | Status |
|-----------|--------|---------------|--------|
| ecommerce-live | ECommerce/Live | yes | created |
| audit | Security | yes | exists |

## Organization Policies

| Constraint | Scope | Status |
|-----------|-------|--------|
| iam.disableServiceAccountKeyCreation | Organization | applied |
| gcp.resourceLocations (eu01, us01) | ECommerce folder | applied |
| compute.requireShieldedVm | ECommerce/Live folder | applied |

## Centralized Audit

| Component | Status |
|-----------|--------|
| Org-level log sink | created |
| Security Command Center | enabled |
| Audit bucket retention policy | applied |

## Budget Alerts

| Project | Amount | Status |
|---------|--------|--------|
| ecommerce-live | $5,000/mo | created |

## Open Items
[Policy propagation delays, globally taken Project IDs, billing account access issues, etc.]
```

## Principles to Apply

- **Keep the folder hierarchy shallow**: GCP recommends ≤ 3 levels. Every level adds a place where policy exceptions can be introduced.
- **Project IDs are permanent**: Unlike display names, Project IDs cannot be changed after creation. Confirm IDs before provisioning — a wrong ID means creating a new project.
- **Billing Accounts are not the hierarchy**: GCP explicitly recommends against structuring the resource hierarchy around billing accounts. Link projects to Billing Accounts separately; use labels for cost attribution.
- **Organization Policies are the enforcement floor**: They constrain what can be configured even by project owners. Apply them broadly and selectively relax at lower levels, not the reverse.
- **Use GCP Fabric FAST for large deployments**: Fabric FAST provides Terraform modules for GCP landing zones that implement these patterns at scale. Reference it rather than reimplementing.
- **Idempotent**: Check before creating. Never delete Folders or Projects without confirmation.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
