---
name: manage-aws-landing-zone
description: >
  Provision and sync the AWS landing zone — Organizations, Organizational Units, Accounts,
  Service Control Policies, and budget alerts — from a landing-zone-design.md and
  naming-convention.md. Uses the AWS MCP server. Use when applying or updating the AWS cloud
  structure after running design-landing-zone.
license: Apache-2.0
metadata:
  version: "0.1.0"
  chapter: "6"
---

# Manage AWS Landing Zone

## Skill Type

Implementation

## System Requirements

- **AWS MCP server** configured and authenticated. The agent will use AWS MCP tools to call Organizations, Account Management, SCP, Config, and Budgets APIs.
- The executing identity must be in the **management account** (root) of the AWS Organization with:
  - `organizations:CreateOrganizationalUnit`, `organizations:MoveAccount`
  - `organizations:CreateAccount` (or use Control Tower `CreateManagedAccount` if Control Tower is in use)
  - `organizations:CreatePolicy`, `organizations:AttachPolicy`
  - `budgets:CreateBudget`, `budgets:ModifyBudget`
- AWS Organizations must already be enabled with all features enabled (not consolidated billing only).

> **Note**: For organizations using AWS Control Tower, Account Factory should be used to provision accounts. This skill supports both the raw Organizations API and Control Tower. Clarify which is in use before starting.

## Your Goal

Apply the landing zone definition from `landing-zone-design.md` to AWS. Ensure that:

1. Organizational Unit hierarchy exists and matches the design.
2. All Accounts are created or adopted and placed under the correct OUs.
3. Service Control Policies (and/or Resource Control Policies) enforce the guardrails.
4. Budget alerts are configured per Account.
5. The audit/log-archive account is set up with centralized CloudTrail and Config aggregation.

This skill is **idempotent**.



## Notation & Types Reference

When writing configurations or documentation, you **MUST** strictly adhere to the structural notation and types defined in the book. Before proceeding, read the following reference files:
- `references/notation.md`
- `references/types.md`

## What to Gather First

Before proceeding, ask the user (or infer from context):

- **Landing zone design**: Path to `landing-zone-design.md`. Read it first.
- **Naming convention**: Path to `naming-convention.md`.
- **Control Tower**: Is AWS Control Tower in use? If yes, Account Factory must be used for account vending — direct `CreateAccount` calls bypass Control Tower's enrollment and leave accounts ungoverned.
- **Management account ID**: Required for SCP and OU operations.
- **Audit account destination**: Email address for the centralized audit/log-archive account.
- **Scope of this run**: Full organization, specific OUs, or specific accounts?
- **Dry-run mode**: Recommended for first-time runs.

Read both input documents before proceeding.

## Process

### Step 1 — Read and Validate Design Documents

Read `landing-zone-design.md` and `naming-convention.md`. Extract:
- OU names and hierarchy
- Account names, parent OUs, and email addresses
- SCP requirements per OU level
- Budget amounts per Account
- Audit account location

Validate that all names conform to AWS naming constraints (OU name ≤ 128 chars, Account name ≤ 50 chars).

### Step 2 — Provision Organizational Unit Hierarchy

For each OU in the design:
1. Check whether it exists at the correct position in the hierarchy using the AWS MCP.
2. Create it under the correct parent OU if missing.

Do not delete OUs not in the design — OUs with child accounts cannot be deleted, and deletion is destructive.

### Step 3 — Provision Accounts

For each Account in the design:
1. Check whether an account with the declared name exists.
2. If missing:
   - **Without Control Tower**: Call `organizations:CreateAccount`. Account creation is asynchronous — poll for completion.
   - **With Control Tower**: Use Account Factory (Service Catalog or Control Tower API). Flag this as requiring Control Tower enrollment and await completion before proceeding.
3. Move the account to the correct OU if it exists but is misplaced.
4. Tag the account with mandatory tags (`sector`, `tier`) using `organizations:TagResource`.

**Required accounts beyond the design**:
- Verify the management account has no workload resources.
- Verify the audit/log-archive account exists and is placed in the Security sector OU.

### Step 4 — Create and Attach Service Control Policies

Service Control Policies (SCPs) are permission guardrails applied at the OU level. Create SCPs from the guardrail requirements in the design:

**Recommended SCPs by OU level**:

*Organization Root*:
- `DenyLeavingOrganization` — prevent accounts from leaving the Organization
- `DenyDisablingCloudTrail` — block `cloudtrail:StopLogging`, `cloudtrail:DeleteTrail`
- `DenyDeletedLogArchive` — protect the audit account's S3 buckets from deletion

*Sector OU*:
- `AllowedRegions` — restrict `ec2:*`, `rds:*`, etc. to declared regions using `aws:RequestedRegion` condition
- `RequireMandatoryTags` — deny resource creation without mandatory tags (note: tag enforcement via SCPs is complex; alternative is AWS Config rules)

*`Tier("live")` OU*:
- `DenyPublicS3Buckets` — block `s3:PutBucketPublicAccessBlock` with public access enabled
- `RequireEncryptionAtRest` — deny unencrypted EBS volumes, RDS instances, S3 buckets
- `DenyRootUserActions` — deny all actions for the root user except those required for billing

*`Tier("sandbox")` OU*:
- `AllowedRegions` (same as Sector, but may allow broader regions for experimentation)
- No encryption-at-rest mandate (to allow faster iteration)

For each SCP:
1. Check whether it already exists by name/content.
2. Create it if missing.
3. Attach it to the correct OU if not already attached.

### Step 5 — Configure Centralized Audit

For the audit/log-archive account:
1. Enable CloudTrail at the Organization level (if not already enabled) — trails in all accounts, stored in the audit account's S3 bucket.
2. Enable AWS Config at the Organization level — aggregate findings to Config Aggregator in the audit account.
3. Enable Security Hub at the Organization level — designate the audit account as the delegated administrator.
4. Verify that the audit account's S3 bucket has:
   - Versioning enabled
   - Object lock enabled (compliance mode, 7-year retention)
   - No public access
   - KMS encryption

### Step 6 — Configure Budget Alerts

For each Account, configure a budget:
1. Check whether a budget already exists.
2. Create a monthly cost budget with the threshold from the design.
3. Add alert thresholds at 80% (actual) and 100% (forecasted).
4. Notify the platform team's email or SNS topic.

### Step 7 — Report

Produce a summary:
- OUs created / already existed
- Accounts created / moved / already existed (note any Control Tower enrollments pending)
- SCPs created / attached / already existed
- Audit configuration status
- Budget alerts created / already existed
- Items skipped with reason

In dry-run mode, produce the report without making changes.

## Output Format

Produce a Markdown report named `aws-landing-zone-report.md`:

```markdown
# AWS Landing Zone Sync Report

**Date**: [timestamp]
**Mode**: [applied / dry-run]
**Control Tower**: [yes / no]

## Organizational Units

| Name | Parent | Status |
|------|--------|--------|
| Platform | Root | created |
| ECommerce | Root | exists |

## Accounts

| Name | OU | Email | Status |
|------|----|-------|--------|
| ecommerce-live | ECommerce/Live | ecommerce-live@mountainlab.io | created |
| audit | Security | audit@mountainlab.io | exists |

## Service Control Policies

| Policy Name | Attached To | Status |
|------------|------------|--------|
| DenyLeavingOrganization | Root | exists |
| AllowedRegions-ECommerce | OU: ECommerce | created |

## Centralized Audit

| Component | Status |
|-----------|--------|
| Org-level CloudTrail | enabled |
| Config Aggregator | exists |
| Security Hub delegated admin | configured |

## Budget Alerts

| Account | Amount | Status |
|---------|--------|--------|
| ecommerce-live | $5,000/mo | created |

## Open Items
[Control Tower enrollments pending, SCP propagation delay notes, etc.]
```

## Principles to Apply

- **Management account is governance-only**: No workloads, no application deployments. The management account's credentials are the master keys to the entire Organization.
- **Control Tower if available**: Control Tower provides account vending, guardrail enforcement, and landing zone provisioning that would otherwise require significant custom automation. Use it rather than reinventing it.
- **SCPs are deny-by-design**: SCPs restrict what *can* be done, even by account admins. They don't grant permissions. Keep them focused on the highest-risk actions.
- **Audit account is immutable**: The log archive must survive even a full account compromise. Object Lock and deletion protection are not optional.
- **Idempotent**: Always check state before creating. Never delete OUs or accounts without confirmation — account deletion in AWS is a multi-step, multi-day process.

## Related Chapter(s)

This skill is grounded in **Chapter 6: Infrastructure** of *Crafting Platforms*.

- Read the book: [leanpub.com/crafting-platforms](https://leanpub.com/crafting-platforms)
- Project home: [craftingplatforms.com](https://www.craftingplatforms.com)
