---
name: manage-gcp-iam
description: >
  Provision and sync GCP IAM resources — IAM bindings at Organization / Folder / Project scope,
  custom roles, service accounts with Workload Identity Federation, and organization policies —
  from a core-iam.yaml and tenant.yaml definition. Uses the GCP MCP server. Use when applying
  or updating IAM changes on GCP after running define-core-iam or define-tenant-iam.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "5"
---

# Manage GCP IAM

## Skill Type

Implementation

## System Requirements

- **GCP MCP server** configured and authenticated. The agent will use GCP MCP tools to call Cloud IAM, Resource Manager, and IAM Credentials APIs.
- The executing identity must have sufficient permissions:
  - `resourcemanager.projects.setIamPolicy`, `resourcemanager.folders.setIamPolicy`
  - `iam.serviceAccounts.create`, `iam.serviceAccounts.setIamPolicy`
  - `iam.roles.create`, `iam.roles.update` (if custom roles are needed)
  - `iam.workloadIdentityPools.create`, `iam.workloadIdentityPools.update`
  - Google Workspace / Cloud Identity: group read/write access via `Role("admin")` SDK (if managing groups)
- GCP Organization, Folder, and Project structure must already exist (output of the cloud structure mapping from `design-segmentation`).
- Cloud Identity or Google Workspace must be the identity provider.

## Your Goal

Apply the IAM definitions from `core-iam.yaml` and/or one or more `tenants/{name}.yaml` files to GCP. Ensure that:

1. Cloud Identity groups exist for each declared group.
2. IAM bindings at the correct resource scope (Organization, Folder, or Project) map groups to roles.
3. Service accounts for `Role("operator")` identities exist with Workload Identity Federation pools and providers configured.
4. No service account keys exist for `Role("operator")` identities.
5. IAM conditions are used where available to enforce time-bound or context-aware access.

This skill is **idempotent**: running it multiple times produces the same result.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **IAM definition files**: Path(s) to `core-iam.yaml` and/or `tenants/{name}.yaml`. Read these files first.
- **GCP resource structure**: Organization ID, Folder IDs, and Project IDs for each coordinate. Derive from the segmentation design or ask the user.
- **Google Workspace / Cloud Identity domain**: Used for group email addresses and `Role("admin")` SDK calls.
- **Workload Identity Pool name**: The pool used for external identity federation (create one per `(Sector, Tier)` or one global pool — discuss trade-offs with the user).
- **External IdP integration**: Is the corporate IdP (Entra ID, Okta) federated into Cloud Identity via SAML/SCIM? If yes, groups may already be synced. If no, groups must be managed in Cloud Identity directly.
- **Scope of this run**: Core IAM only, specific tenants, or all tenants?
- **Dry-run mode**: Recommended for first-time runs.

Read the IAM definition files before proceeding.

## Process

### Step 1 — Read and Parse IAM Definitions

Read the specified IAM definition files. Extract:

- All groups (name, type, members, JIT policy)
- Workload Identity Federation conditions for `Role("operator")` groups
- Sector and tier scope for each group
- Project and Folder IDs from the segmentation mapping

Validate the definitions:
- No human members in `Role("operator")` groups
- No nested groups in member lists
- All Workload Identity issuers are OIDC-compatible

Report validation errors and stop before applying any changes.

### Step 2 — Reconcile Cloud Identity Groups

For each group declared in the IAM definition:

1. Check whether a Cloud Identity group with the matching name/email exists.
2. Create it if missing (e.g., `payments-live-admins@mountainlab.io`).
3. Reconcile membership: add declared members, remove undeclared members, log every change.
4. `Role("operator")` groups: verify zero human members. Report and remove any found.

If groups are synced via SCIM from an external IdP, skip creation — only verify existence and log a note that membership is managed externally.

### Step 3 — Create IAM Bindings

Map each group to the correct GCP predefined role and resource scope:

| Group Pattern | GCP Role | Scope |
|---------------|----------|-------|
| `{sector}-{tier}-operator` | `roles/editor` + permission boundary via Org Policy | Project `(sector, tier)` |
| `{sector}-{tier}-admins` | `roles/owner` | Project `(sector, tier)` — via IAM Condition for time-bound access |
| `{sector}-{tier}-contributors` | `roles/editor` | Project `(sector, tier)` |
| `{sector}-{tier}-readers` | `roles/viewer` | Folder `({sector})` |
| `{tenant}-{tier}-operator` | Service Account binding | Project `({sector}, {tier}, _, {tenant})` |
| `{tenant}-{tier}-admins` | `roles/owner` (scoped) | Project for tenant |
| `{tenant}-{tier}-contributors` | `roles/editor` | Project for tenant |
| `{tenant}-readers` | `roles/viewer` | Project(s) for tenant's declared sectors |

For each binding:
1. Read the current IAM policy at the target scope.
2. Identify missing bindings.
3. Add missing bindings in a single `setIamPolicy` call per resource (do not issue one API call per member — batch the policy update to avoid race conditions).
4. Do not remove existing bindings not in the definition without explicit user confirmation.

**IAM Conditions for `Role("admin")` roles**: Where available, use IAM conditions to restrict `Role("admin")` bindings to a time window or require specific resource-level access justification (Access Approval). Document this in the output.

**Custom roles**: If the predefined roles (`editor`, `viewer`) are too broad for the tenant's use case, define a custom role with only the permissions the tenant's workloads require. Create it at the Project or Organization level as appropriate. Prefer Organization-level custom roles for reuse across projects.

### Step 4 — Configure Workload Identity Federation

For each `Role("operator")` group's Workload Identity definition:

1. **Workload Identity Pool**: Check whether a pool exists for the sector/tier or create one. Naming convention: `{sector}-{tier}`.
2. **OIDC Provider**: Add a provider to the pool for each unique issuer. Set the allowed audiences from the `audience` field in the definition.
3. **Attribute mapping**: Map OIDC claims to Google token attributes:
   - `google.subject` ← `assertion.sub`
   - `attribute.repository` ← `assertion.repository` (for GitHub Actions)
   - `attribute.ref` ← `assertion.ref` (for branch-based conditions)
4. **Attribute conditions**: Set a CEL expression to restrict which external identities can impersonate the service account. Do not allow unrestricted pool-wide impersonation.
5. **Service Account**: Create a service account for the `Role("operator")` (e.g., `payments-live-operator@{project}.iam.gserviceaccount.com`).
6. **Impersonation binding**: Grant `roles/iam.workloadIdentityUser` to the pool/provider/subject combination on the service account — this is the binding that allows the external identity to impersonate the account.
7. **No keys**: Verify no service account keys exist. Report any found as a security finding.

### Step 5 — Apply Organization Policies

Complement IAM bindings with Organization Policy constraints to enforce boundaries that IAM alone cannot:

- `iam.disableServiceAccountKeyCreation`: Prevent creation of service account keys in all projects.
- `iam.disableServiceAccountKeyUpload`: Prevent uploading external keys.
- `iam.allowedPolicyMemberDomains`: Restrict IAM members to the organization's domain — prevents accidentally granting access to external Gmail accounts.

Check whether these policies are already set at the Organization or Folder level. If not, recommend enabling them and confirm with the user before applying (Organization Policies are wide in scope).

### Step 6 — Address JIT Access

GCP does not have a built-in JIT tool equivalent to Azure PIM. Available options:

- **IAM Conditions with expiry**: IAM bindings can include a `request.time` condition to make them automatically expire. Use this for time-bound `Role("admin")` access.
- **Access Approval**: For `Role("admin")` roles on sensitive projects, enable Access Approval to require manual approval before the access is granted at the API level.
- **Privileged Access Manager (PAM)**: GCP's Privileged Access Manager (if available in the organization's region) provides JIT grant workflows similar to Azure PIM. Check availability and configure if present.
- **External tools (Teleport)**: If Teleport is in use, record that it handles JIT approval and that GCP bindings define the ceiling.

For each `Role("admin")` and `Tier("live")` `Role("contributor")` group, document the JIT strategy in the output. Flag groups with permanent `roles/owner` bindings on `Tier("live")` projects and recommend a remediation.

### Step 7 — Report Drift and Changes

Produce a summary after applying:

- Groups created / already existed / membership reconciled
- IAM bindings added per resource scope
- Workload Identity pools and providers created / already existed
- Service accounts created / keys found (security finding)
- Organization Policies checked / recommended
- JIT strategy per group
- Items skipped with reason

In dry-run mode, produce the report without making changes.

## Output Format

Produce a Markdown report named `gcp-iam-report.md`:

``markdown
# GCP IAM Sync Report

**Date**: [timestamp]
**Scope**: [core / tenant names applied]
**Mode**: [applied / dry-run]

## Cloud Identity Groups

| Group | Status | Members Added | Members Removed |
|-------|--------|--------------|----------------|
| payments-live-admins@mountainlab.io | created | 1 | 0 |

## IAM Bindings

| Group | Role | Resource | Condition | Status |
|-------|------|----------|-----------|--------|
| platform-sandbox-readers | roles/viewer | folders/123456 | — | created |
| payments-live-admins | roles/owner | projects/payments-live | expiry: 2h | created |

## Workload Identity Federation

| Pool | Provider | Service Account | Attribute Condition | Status |
|------|----------|----------------|--------------------| -------|
| ecommerce-live | github-actions | payments-live-operator@ | sub=repo:mountainlab/payments-service:environment:live | created |

## Organization Policies

| Policy | Status | Recommendation |
|--------|--------|---------------|
| iam.disableServiceAccountKeyCreation | not set | Enable at Org level |

## JIT Status

| Group | Strategy | Standing `Tier("live")` Write | Remediation Needed |
|-------|----------|--------------------|--------------------|
| payments-live-admins | IAM condition expiry | no | no |

## Security Findings

[Service account keys found, unrestricted pool impersonation, permanent owner bindings, etc.]

## Open Items

[Actions requiring manual intervention or external tooling configuration]
``

## Principles to Apply

- **Idempotent by design**: Always read current policy before writing. Batch policy updates — do not issue one API call per member.
- **No service account keys**: Keys on service accounts defeat Workload Identity. Any key found is a security finding.
- **Attribute conditions are mandatory**: A Workload Identity binding without an attribute condition allows any identity in the pool to impersonate the service account. Always set a CEL expression.
- **Organization Policies complement IAM**: IAM is additive and delegation-based. Organization Policies are the enforcement floor — they prevent even IAM admins from creating dangerous configurations.
- **Prefer folder-level reader bindings**: Granting `Role("reader")` at the Folder level cascades to all projects below it. This is the correct pattern for cross-project read access (e.g., a monitoring tool reading all projects in a sector).
- **JIT via IAM conditions or PAM**: Permanent `roles/owner` on `Tier("live")` projects is an anti-pattern. Use expiring conditions or PAM to enforce time-bound access.

## Related Chapter(s)

This skill is grounded in **Chapter 5: Identity and Access Management** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
