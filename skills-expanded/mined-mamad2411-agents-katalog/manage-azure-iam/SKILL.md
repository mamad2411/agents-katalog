---
name: manage-azure-iam
description: >
  Provision and sync Azure IAM resources — Entra ID groups, role assignments at Management
  Group / Subscription / Resource Group scope, and Privileged Identity Management (PIM)
  eligible assignments — from a core-iam.yaml and tenant.yaml definition. Uses the Azure MCP
  server. Use when applying or updating IAM changes on Azure after running define-core-iam
  or define-tenant-iam.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "5"
---

# Manage Azure IAM

## Skill Type

Implementation

## System Requirements

- **Azure MCP server** configured and authenticated. The agent will use Azure MCP tools to read and write Entra ID and Azure resource management APIs.
- The executing identity must have sufficient permissions:
  - `Microsoft.Authorization/roleAssignments/write` at the target scope
  - `Microsoft.Authorization/roleDefinitions/write` (if custom roles are needed)
  - Entra ID: `Group.ReadWrite.All` and `Directory.ReadWrite.All`
  - Azure AD PIM: `PrivilegedAccess.ReadWrite.AzureADGroup` (for PIM configuration)
- Azure Management Group hierarchy and Subscription structure must already exist (output of the cloud structure mapping from `design-segmentation`).

## Your Goal

Apply the IAM definitions from `core-iam.yaml` and/or one or more `tenants/{name}.yaml` files to Azure. Ensure that:

1. All required Entra ID groups exist.
2. Group membership matches the declared members.
3. Role assignments are created at the correct scope (Management Group, Subscription, or Resource Group).
4. PIM eligible assignments are configured for `Role("admin")` and `Tier("live")` `Role("contributor")` groups.
5. Workload Identity Federation credentials are configured for `Role("operator")` groups.

Drift between the declared state and the live Azure state must be identified and resolved. This skill is **idempotent**: running it multiple times produces the same result.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **IAM definition files**: Path(s) to `core-iam.yaml` and/or `tenants/{name}.yaml`. Read these files first.
- **Cloud structure mapping**: The Subscription and Resource Group names derived from the segmentation design (e.g., `platform-sandbox`, `ecommerce-live`, `rg-payments-eu01-live`).
- **Entra ID tenant ID**: Required for Workload Identity Federation configuration.
- **Scope of this run**: Apply only core IAM, only a specific tenant, or all tenants? Clarify before making changes.
- **Dry-run mode**: Should the skill list planned changes before applying them? Recommend yes for first-time runs or large change sets.

Read the IAM definition files before proceeding. Do not apply changes based on assumptions about their contents.

## Process

### Step 1 — Read and Parse IAM Definitions

Read the specified IAM definition files. Extract:

- All groups to be managed (name, type, members, JIT policy)
- Workload Identity Federation requirements for `Role("operator")` groups
- JIT policy overrides (from `jit_overrides` in tenant files)
- Sector and tier scope for each group

Validate the definitions before applying:
- No human members in `Role("operator")` groups
- No nested groups in member lists (individuals only)
- All required fields present

Report any validation errors and stop. Do not apply changes against an invalid definition.

### Step 2 — Reconcile Entra ID Groups

For each group in the definition:

1. **Check existence**: Use the Azure MCP to query Entra ID for the group by name.
2. **Create if missing**: If the group does not exist, create it with the correct display name, description, and `isAssignableToRole: true` flag (required for PIM-eligible groups).
3. **Reconcile membership**: Compare declared members against current group members.
   - Add members present in the definition but missing from the group.
   - Remove members present in the group but not in the definition.
   - Log every addition and removal.
4. **`Role("operator")` groups**: Verify that `Role("operator")` groups have zero human members. If any are found, report them and remove them.

### Step 3 — Create Role Assignments

Map each group to the correct Azure built-in role and scope, derived from the coordinate system:

| Group Pattern | Azure Role | Scope |
|---------------|-----------|-------|
| `{sector}-{tier}-operator` | `Role("contributor")` | Subscription `(sector, tier)` |
| `{sector}-{tier}-admins` | `Owner` | Subscription `(sector, tier)` |
| `{sector}-{tier}-contributors` | `Role("contributor")` | Subscription `(sector, tier)` |
| `{sector}-{tier}-readers` | `Role("reader")` | Management Group `({sector})` |
| `{tenant}-{tier}-operator` | `Role("contributor")` | Resource Group `(sector, tier, region, tenant)` |
| `{tenant}-{tier}-admins` | `Owner` | Resource Group(s) for tenant |
| `{tenant}-{tier}-contributors` | `Role("contributor")` | Resource Group(s) for tenant |
| `{tenant}-readers` | `Role("reader")` | Subscription `(sector, tier)` for each declared sector |

For each role assignment:
1. Check if it already exists at the target scope.
2. Create it if missing.
3. Do not remove role assignments not in the definition without explicit user confirmation — this is a destructive action.

If custom roles are required (e.g., a narrower permission set than `Role("contributor")`), define them via the Azure MCP before creating the assignment. Document any custom role definitions in the output.

### Step 4 — Configure PIM Eligible Assignments

For every `Role("admin")` and `Tier("live")` `Role("contributor")` group (which use JIT escalation), configure PIM:

1. Verify the group is PIM-enabled (Security group with `isAssignableToRole: true`).
2. Create an **eligible assignment** (not an active assignment) for each member declared under `admins` or `contributors`.
3. Apply the escalation policy from the IAM definition:
   - **Approval required**: Set to `true` for `Tier("live")` `Role("admin")` and peer-approval `Role("contributor")`; `false` for self-approve.
   - **Maximum duration**: Set from `max_duration_hours` in the definition.
   - **Justification required**: Always `true` for `Tier("live")`.
   - **MFA required**: Enable for `Tier("live")` `Role("admin")` roles.
4. For `Tier("sandbox")` `Role("contributor")` (self-approve, no justification), PIM eligible assignments are still recommended — but the activation policy can be permissive.

Report the PIM assignment state after configuration.

### Step 5 — Configure Workload Identity Federation

For each `Role("operator")` group's Workload Identity definition:

1. Locate or create the **App Registration** or **Managed Identity** that represents the `Role("operator")`.
2. Add a Federated Identity Credential using the declared `issuer`, `subject`, and `audience`.
3. Assign the `Role("operator")` group's role assignment to this App Registration or Managed Identity (not to a human user).
4. Verify the federation claim conditions are as narrow as declared — warn if the subject contains a wildcard.

Do not create or store client secrets. If a client secret is found on an `Role("operator")` identity, report it as a security finding.

### Step 6 — Report Drift and Changes

After applying changes, produce a summary:

- Groups created / already existed
- Members added / removed per group
- Role assignments created / already existed
- PIM assignments configured / already existed
- Workload Identity Federation credentials created / already existed
- Any items skipped with reason
- Any security findings (human members in `Role("operator")` groups, client secrets, wildcard subjects)

If running in dry-run mode, produce this report without making any changes, and ask for confirmation before proceeding.

## Output Format

Produce a Markdown report named `azure-iam-report.md`:

``markdown
# Azure IAM Sync Report

**Date**: [timestamp]
**Scope**: [core / tenant names applied]
**Mode**: [applied / dry-run]

## Groups

| Group | Status | Members Added | Members Removed |
|-------|--------|--------------|----------------|
| platform-sandbox-readers | created | 4 | 0 |
| payments-live-admins | exists | 1 | 0 |

## Role Assignments

| Group | Role | Scope | Status |
|-------|------|-------|--------|
| platform-sandbox-operator | `Role("contributor")` | /subscriptions/platform-sandbox | created |
| payments-readers | `Role("reader")` | /subscriptions/ecommerce-live | exists |

## PIM Eligible Assignments

| Group | Member | Approval | Duration | Status |
|-------|--------|----------|----------|--------|
| payments-live-admins | marta@mountainlab.io | peer | 2h | created |

## Workload Identity Federation

| `Role("operator")` Group | App Registration | Subject | Status |
|----------------|-----------------|---------|--------|
| payments-live-operator | payments-live-runner | repo:mountainlab/payments-service:environment:live | created |

## Security Findings

[List any violations: human members in `Role("operator")` groups, client secrets found, wildcard subjects, etc.]

## Open Items

[Anything that could not be applied automatically and requires manual action]
``

## Principles to Apply

- **Idempotent by design**: Always check current state before making changes. Creating an existing resource is a no-op, not an error.
- **Drift detection before destruction**: Never remove role assignments or group memberships without first presenting the diff to the user and receiving confirmation.
- **Workload Identity over secrets**: If a client secret is found on an `Role("operator")` identity, treat it as a security finding and recommend rotating to Workload Identity.
- **PIM over standing access**: `Role("admin")` and `Tier("live")` `Role("contributor")` groups must use PIM eligible assignments, not active assignments.
- **Narrow trust conditions**: Warn on any Workload Identity subject that uses a wildcard. Recommend scoping to specific repositories, branches, or environments.
- **Tags are metadata**: Azure resource tags are used for cost attribution and IaC references. Do not use ABAC (attribute-based access control on tags) for access management.

## Related Chapter(s)

This skill is grounded in **Chapter 5: Identity and Access Management** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
