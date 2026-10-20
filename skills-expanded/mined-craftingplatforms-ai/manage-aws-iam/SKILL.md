---
name: manage-aws-iam
description: >
  Provision and sync AWS IAM resources — IAM roles, permission boundaries, IAM Identity Center
  permission sets, and OIDC identity provider trust policies — from a core-iam.yaml and
  tenant.yaml definition. Uses the AWS MCP server. Use when applying or updating IAM changes
  on AWS after running define-core-iam or define-tenant-iam.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "5"
---

# Manage AWS IAM

## Skill Type

Implementation

## System Requirements

- **AWS MCP server** configured and authenticated. The agent will use AWS MCP tools to call IAM, IAM Identity Center (SSO), Organizations, and STS APIs.
- The executing identity must have sufficient permissions:
  - `iam:CreateRole`, `iam:AttachRolePolicy`, `iam:PutRolePermissionsBoundary`
  - `iam:CreateOpenIDConnectProvider`, `iam:UpdateOpenIDConnectProviderThumbprint`
  - `sso-admin:CreatePermissionSet`, `sso-admin:ProvisionPermissionSet`, `sso-admin:CreateAccountAssignment`
  - `organizations:ListAccounts`, `organizations:DescribeOrganization`
- AWS Organization structure and Account layout must already exist (output of the cloud structure mapping from `design-segmentation`).
- IAM Identity Center must be enabled in the management account.

## Your Goal

Apply the IAM definitions from `core-iam.yaml` and/or one or more `tenants/{name}.yaml` files to AWS. Ensure that:

1. IAM roles for `Role("operator")` (non-human) identities exist in the correct accounts with the correct trust policies and permission boundaries.
2. IAM Identity Center permission sets exist for `Role("admin")`, `Role("contributor")`, and `Role("reader")` roles.
3. Permission sets are assigned to the correct groups and AWS accounts.
4. OIDC identity providers are registered for Workload Identity Federation.
5. No long-lived IAM access keys exist for `Role("operator")` identities.

This skill is **idempotent**: running it multiple times produces the same result.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **IAM definition files**: Path(s) to `core-iam.yaml` and/or `tenants/{name}.yaml`. Read these files first.
- **Account structure**: The AWS Account IDs for each `(Sector, Tier)` or `(Sector, Tier, _, Tenant)` combination. Derive from the segmentation design or ask the user.
- **IAM Identity Center instance ARN**: Required for permission set and assignment operations.
- **External IdP integration**: Is the corporate IdP (Entra ID, Okta, Google Workspace) federated into IAM Identity Center? If yes, groups from the IdP will be synced automatically via SCIM. If no, groups must be managed inside IAM Identity Center directly.
- **Scope of this run**: Core IAM only, a specific tenant, or all tenants?
- **Dry-run mode**: Recommend yes for first-time runs.

Read the IAM definition files before proceeding. Do not apply changes based on assumptions.

## Process

### Step 1 — Read and Parse IAM Definitions

Read the specified IAM definition files. Extract:

- All groups (name, type, members, JIT policy)
- Workload Identity Federation conditions for `Role("operator")` groups
- Sector and tier scope for each group
- Account IDs from the segmentation mapping

Validate the definitions:
- No human members in `Role("operator")` groups
- No nested groups in member lists
- All Workload Identity issuers reference OIDC-compatible endpoints

Report validation errors and stop. Do not apply changes against an invalid definition.

### Step 2 — Register OIDC Identity Providers

For each unique Workload Identity `issuer` referenced across all `Role("operator")` groups:

1. Check whether an OIDC provider with this issuer URL already exists in the relevant account(s).
2. If missing, create it using the AWS MCP. Fetch the TLS thumbprint from the issuer's well-known configuration endpoint.
3. Verify the registered thumbprint is current — OIDC provider thumbprints can expire.

Register the OIDC provider in each account where `Role("operator")` roles will be created.

### Step 3 — Create IAM Roles for Operators

For each `{sector}-{tier}-operator` and `{tenant}-{tier}-operator` group:

1. Determine the target account(s) — derived from the `(Sector, Tier)` or `(Sector, Tier, _, Tenant)` coordinate.
2. Check whether the IAM role already exists in the account.
3. Create or update the role with:
   - **Trust policy**: `sts:AssumeRoleWithWebIdentity`, restricted to the declared OIDC issuer, subject, and audience claims. Use `StringEquals` conditions for subject and audience — never `StringLike` with wildcards.
   - **Permission boundary**: Attach a permission boundary that limits the role to the resource scope of its coordinate (e.g., resources tagged or named with the sector/tier/tenant prefix). This prevents a compromised runner from affecting resources outside its scope.
   - **Managed policies**: Attach the appropriate AWS managed policy for the access level:
     - `Role("operator")`: `PowerUserAccess` with a permission boundary, or a custom policy scoped to the resources the pipeline manages.
4. Verify no access keys exist on the role. If found, report as a security finding.

### Step 4 — Create IAM Identity Center Permission Sets

IAM Identity Center permission sets represent the human-facing roles (`Role("admin")`, `Role("contributor")`, Reader). Create one permission set per role type:

| Permission Set Name | Managed Policy | Session Duration |
|--------------------|----------------|-----------------|
| `PlatformAdmin` | `AdministratorAccess` | 2 hours |
| `PlatformContributor` | `PowerUserAccess` | 4 hours |
| `PlatformReader` | `ReadOnlyAccess` | 8 hours |
| `TenantAdmin` | `AdministratorAccess` (scoped) | 2 hours |
| `TenantContributor` | `PowerUserAccess` (scoped) | 4 hours |
| `TenantReader` | `ReadOnlyAccess` | 8 hours |

For each permission set:
1. Check whether it exists in IAM Identity Center.
2. Create it if missing, with the correct session duration and inline/managed policies.
3. For `Role("admin")` and `Tier("live")` `Role("contributor")` sets, configure the session duration to match the JIT window defined in the IAM definition.

Prefer AWS managed policies where they fit. Use inline policies only when the scope must be narrowed further (e.g., restricting a `Role("contributor")` to resources within the tenant's account only).

### Step 5 — Create Account Assignments

Assign permission sets to groups and accounts:

- **Core IAM groups** (sector-level): Assign at the account level for each account in the sector.
- **Tenant groups**: Assign at the specific tenant account(s).

The mapping:

| Group | Permission Set | Account(s) |
|-------|---------------|------------|
| `{sector}-{tier}-admins` | `PlatformAdmin` | Account for `(Sector, Tier)` |
| `{sector}-{tier}-contributors` | `PlatformContributor` | Account for `(Sector, Tier)` |
| `{sector}-{tier}-readers` | `PlatformReader` | All accounts in Sector |
| `{tenant}-{tier}-admins` | `TenantAdmin` | Account for `(Sector, Tier, _, Tenant)` |
| `{tenant}-{tier}-contributors` | `TenantContributor` | Account for `(Sector, Tier, _, Tenant)` |
| `{tenant}-readers` | `TenantReader` | All accounts for tenant's sectors |

For each assignment:
1. Check whether the assignment already exists.
2. Create it if missing.
3. Provision the permission set to the account (permission sets must be provisioned after assignment).

If the corporate IdP is federated via SCIM, groups are synced automatically. Reference the group by its IdP group ID or display name as supported by IAM Identity Center. If groups are managed natively in IAM Identity Center, create them and add members per the IAM definition.

### Step 6 — Validate JIT / Session Duration Alignment

AWS IAM Identity Center does not have a native JIT approval workflow equivalent to Azure PIM. Options:

- **Service Control Policies (SCPs)**: Use SCPs to restrict what `Role("admin")` permission sets can do without an active session — this is not true JIT but limits standing power.
- **AWS IAM Identity Center with Approval workflows**: If integrated with an external approval tool (PagerDuty, Slack workflows, Teleport), document the integration point.
- **Teleport**: If Teleport is in use, record that it handles JIT approval at the access request level, and that IAM Identity Center permission sets define the ceiling of what can be requested.

For each `Role("admin")` and `Tier("live")` `Role("contributor")` group, record the JIT strategy in the output report. Flag groups that currently have standing write access to `Tier("live")` accounts and recommend a remediation path.

### Step 7 — Report Drift and Changes

After applying, produce a summary:

- OIDC providers created / already existed / thumbprint updated
- IAM roles created / already existed / trust policy updated
- Permission sets created / already existed
- Account assignments created / already existed
- Security findings (access keys found, wildcard subjects, standing `Tier("live")` write access)
- Items skipped with reason

In dry-run mode, produce the report without making changes and await confirmation.

## Output Format

Produce a Markdown report named `aws-iam-report.md`:

``markdown
# AWS IAM Sync Report

**Date**: [timestamp]
**Scope**: [core / tenant names applied]
**Mode**: [applied / dry-run]

## OIDC Identity Providers

| Issuer | Account(s) | Status |
|--------|-----------|--------|
| https://token.actions.githubusercontent.com | 123456789012 | created |

## IAM `Role("operator")` Roles

| Role Name | Account | Trust Subject | Permission Boundary | Status |
|-----------|---------|--------------|---------------------|--------|
| payments-live-operator | 123456789012 | repo:mountainlab/payments-service:environment:live | attached | created |

## Permission Sets

| Name | Managed Policy | Session Duration | Status |
|------|---------------|-----------------|--------|
| TenantContributor | PowerUserAccess | 4h | exists |

## Account Assignments

| Group | Permission Set | Account | Status |
|-------|---------------|---------|--------|
| payments-live-admins | TenantAdmin | 123456789012 | created |

## JIT Status

| Group | Strategy | Standing `Tier("live")` Write | Remediation Needed |
|-------|----------|--------------------|--------------------|
| payments-live-contributors | session duration only | no | no |

## Security Findings

[Access keys found, wildcard trust subjects, standing `Tier("live")` write access, etc.]

## Open Items

[Actions requiring manual intervention or external tooling configuration]
``

## Principles to Apply

- **Idempotent by design**: Check state before creating. Existing resources are not errors.
- **Trust policy precision**: Use `StringEquals` for OIDC subject and audience claims. Warn on any wildcard. A compromised trust policy can grant arbitrary runners access to production.
- **Permission boundaries are required for Operators**: An `Role("operator")` with `PowerUserAccess` and no boundary can escalate privileges. Always attach a boundary scoped to the tenant's resource prefix.
- **No access keys for Operators**: Access keys on `Role("operator")` identities defeat the purpose of Workload Identity. Treat any found key as a security incident.
- **Session duration is your JIT lever**: AWS Identity Center's session duration is the primary time-bound control. Set it conservatively; developers can re-escalate if the window closes.
- **SCPs enforce, permission sets grant**: Structure SCPs at the OU level to deny sensitive operations (e.g., disabling CloudTrail, modifying billing settings) regardless of what permission sets allow.

## Related Chapter(s)

This skill is grounded in **Chapter 5: Identity and Access Management** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
