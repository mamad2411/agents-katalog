---
name: managing-aws-iam
description: |
  Use when working with Aws Iam — aWS IAM deep analysis for policy evaluation,
  role trust relationship review, access advisor data, credential reports,
  permission boundary inspection, and identity-based vs resource-based policy
  analysis. Covers IAM users, roles, groups, policies, SCPs, and cross-account
  access patterns. Read this skill before any IAM operations — it enforces
  discovery-first patterns and strict read-only safety rules.
connection_type: aws
preload: false
---

# AWS IAM Deep Analysis Skill

Safely read and audit AWS IAM — the identity and access management service for AWS.

## MANDATORY: Discovery-First Pattern

**Always discover the account context, IAM entities, and existing policies before analyzing permissions. Never guess ARNs or policy names.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Account Identity ==="
aws sts get-caller-identity | jq '{
    account: .Account,
    arn: .Arn,
    user_id: .UserId
}'

echo ""
echo "=== Account Summary ==="
aws iam get-account-summary | jq '.SummaryMap | {
    Users: .Users,
    Groups: .Groups,
    Roles: .Roles,
    Policies: .Policies,
    MFADevices: .MFADevices,
    AccessKeysPerUserQuota: .AccessKeysPerUserQuota,
    AccountMFAEnabled: .AccountMFAEnabled,
    ServerCertificates: .ServerCertificates
}'

echo ""
echo "=== IAM Users (first 20) ==="
aws iam list-users --max-items 20 | jq -r '.Users[] | "\(.UserName)\t\(.UserId)\t\(.CreateDate)\t\(.PasswordLastUsed // "Never")"' | column -t

echo ""
echo "=== IAM Roles (first 20) ==="
aws iam list-roles --max-items 20 | jq -r '.Roles[] | "\(.RoleName)\t\(.Arn)\t\(.CreateDate)"' | column -t

echo ""
echo "=== Customer Managed Policies ==="
aws iam list-policies --scope Local --max-items 20 | jq -r '.Policies[] | "\(.PolicyName)\t\(.Arn)\t\(.AttachmentCount)"' | column -t
```

**Phase 1 outputs:** Account context, user/role/policy inventory — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess ARNs or policy names** — always list entities in Phase 1
- **NEVER assume trust relationships** — always read role trust policy documents
- **NEVER fabricate permission sets** — always read actual policy documents
- **ONLY read and describe** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: `get-*`, `list-*`, `describe-*`, `generate-credential-report`, `get-credential-report`
- **MASK sensitive data**: Redact access key secrets, never display full credential report passwords
- **FORBIDDEN without explicit request**: `create-*`, `delete-*`, `put-*`, `attach-*`, `detach-*`, `update-*`
- **NEVER print secret keys**: Access key IDs are fine; secret access keys must never be displayed

## Core Helper Functions

```bash
#!/bin/bash

# Get effective policy for a user (all attached + inline)
get_user_effective_policies() {
    local username="$1"

    echo "--- Attached Policies ---"
    aws iam list-attached-user-policies --user-name "$username" | jq -r '.AttachedPolicies[] | "\(.PolicyName)\t\(.PolicyArn)"' | column -t

    echo "--- Inline Policies ---"
    aws iam list-user-policies --user-name "$username" | jq -r '.PolicyNames[]'

    echo "--- Group Memberships ---"
    aws iam list-groups-for-user --user-name "$username" | jq -r '.Groups[] | .GroupName' | while read group; do
        echo "  Group: $group"
        aws iam list-attached-group-policies --group-name "$group" | jq -r '    .AttachedPolicies[] | "    \(.PolicyName)"'
    done
}

# Read a policy document by ARN
read_policy_document() {
    local policy_arn="$1"
    local version=$(aws iam get-policy --policy-arn "$policy_arn" | jq -r '.Policy.DefaultVersionId')
    aws iam get-policy-version --policy-arn "$policy_arn" --version-id "$version" | jq '.PolicyVersion.Document'
}
```

## Common Operations

### Policy Analysis

```bash
#!/bin/bash
POLICY_ARN="${1:?Policy ARN required — discover via Phase 1}"

echo "=== Policy Metadata ==="
aws iam get-policy --policy-arn "$POLICY_ARN" | jq '{
    name: .Policy.PolicyName,
    arn: .Policy.Arn,
    default_version: .Policy.DefaultVersionId,
    attachment_count: .Policy.AttachmentCount,
    is_attachable: .Policy.IsAttachable,
    create_date: .Policy.CreateDate,
    update_date: .Policy.UpdateDate
}'

echo ""
echo "=== Policy Document ==="
VERSION=$(aws iam get-policy --policy-arn "$POLICY_ARN" | jq -r '.Policy.DefaultVersionId')
aws iam get-policy-version --policy-arn "$POLICY_ARN" --version-id "$VERSION" | jq '.PolicyVersion.Document'

echo ""
echo "=== Entities Attached To ==="
aws iam list-entities-for-policy --policy-arn "$POLICY_ARN" | jq '{
    groups: [.PolicyGroups[].GroupName],
    users: [.PolicyUsers[].UserName],
    roles: [.PolicyRoles[].RoleName]
}'
```

### Role Trust Relationship Review

```bash
#!/bin/bash
ROLE_NAME="${1:?Role name required}"

echo "=== Role: $ROLE_NAME ==="
aws iam get-role --role-name "$ROLE_NAME" | jq '{
    arn: .Role.Arn,
    create_date: .Role.CreateDate,
    max_session_duration: .Role.MaxSessionDuration,
    permissions_boundary: (.Role.PermissionsBoundary.PermissionsBoundaryArn // "None"),
    trust_policy: .Role.AssumeRolePolicyDocument
}'

echo ""
echo "=== Attached Policies ==="
aws iam list-attached-role-policies --role-name "$ROLE_NAME" | jq -r '.AttachedPolicies[] | "\(.PolicyName)\t\(.PolicyArn)"' | column -t

echo ""
echo "=== Inline Policies ==="
aws iam list-role-policies --role-name "$ROLE_NAME" | jq -r '.PolicyNames[]' | while read policy; do
    echo "--- $policy ---"
    aws iam get-role-policy --role-name "$ROLE_NAME" --policy-name "$policy" | jq '.PolicyDocument'
done

echo ""
echo "=== Trust Policy Analysis ==="
aws iam get-role --role-name "$ROLE_NAME" | jq '.Role.AssumeRolePolicyDocument.Statement[] | {
    effect: .Effect,
    principal: .Principal,
    action: .Action,
    condition: (.Condition // "None")
}'
```

### Credential Report & Access Keys

```bash
#!/bin/bash
echo "=== Generating Credential Report ==="
aws iam generate-credential-report > /dev/null 2>&1
sleep 3
aws iam generate-credential-report | jq -r '.State'

echo ""
echo "=== Credential Report Summary ==="
aws iam get-credential-report | jq -r '.Content' | base64 -d | head -1
aws iam get-credential-report | jq -r '.Content' | base64 -d | tail -n +2 | while IFS=',' read -r user arn created pw_enabled pw_last_used pw_last_changed pw_next_rotation mfa_active key1_active key1_last_rotated key1_last_used rest; do
    echo "User: $user | MFA: $mfa_active | PW Enabled: $pw_enabled | Key1 Active: $key1_active"
done | head -20

echo ""
echo "=== Users Without MFA ==="
aws iam get-credential-report | jq -r '.Content' | base64 -d | awk -F',' 'NR>1 && $4=="true" && $8=="false" {print "WARNING: "$1" has password but NO MFA"}'

echo ""
echo "=== Old Access Keys (>90 days) ==="
aws iam list-users | jq -r '.Users[].UserName' | while read user; do
    aws iam list-access-keys --user-name "$user" | jq -r --arg u "$user" '.AccessKeyMetadata[] | select(.Status=="Active") | "\($u)\t\(.AccessKeyId)\t\(.CreateDate)"'
done | column -t | head -20
```

### Access Advisor (Last Accessed)

```bash
#!/bin/bash
ARN="${1:?ARN required (user, role, or group ARN)}"

echo "=== Generating Service Last Accessed Report ==="
JOB_ID=$(aws iam generate-service-last-accessed-details --arn "$ARN" | jq -r '.JobId')
sleep 5

echo "=== Services Last Accessed ==="
aws iam get-service-last-accessed-details --job-id "$JOB_ID" | jq -r '.ServicesLastAccessed | sort_by(.LastAuthenticated) | reverse | .[:20][] | "\(.ServiceName)\t\(.LastAuthenticated // "Never")\t\(.TotalAuthenticatedEntities)"' | column -t

echo ""
echo "=== Unused Services (never accessed) ==="
aws iam get-service-last-accessed-details --job-id "$JOB_ID" | jq -r '.ServicesLastAccessed | map(select(.LastAuthenticated == null)) | length | "Services never used: \(.)"'
```

### Permission Boundary Analysis

```bash
#!/bin/bash
echo "=== Roles with Permission Boundaries ==="
aws iam list-roles --max-items 100 | jq -r '.Roles[] | select(.PermissionsBoundary) | "\(.RoleName)\t\(.PermissionsBoundary.PermissionsBoundaryArn)"' | column -t

echo ""
echo "=== Users with Permission Boundaries ==="
aws iam list-users --max-items 100 | jq -r '.Users[] | select(.PermissionsBoundary) | "\(.UserName)\t\(.PermissionsBoundary.PermissionsBoundaryArn)"' | column -t

echo ""
echo "=== Cross-Account Roles ==="
aws iam list-roles --max-items 100 | jq -r '.Roles[] | select(.AssumeRolePolicyDocument.Statement[].Principal.AWS? // "" | test("arn:aws:iam::[0-9]+:")) | "\(.RoleName)\t\(.AssumeRolePolicyDocument.Statement[0].Principal.AWS)"' | column -t 2>/dev/null
```

## Output Format

Present results as a structured report:
```
Managing Aws Iam Report
═══════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **Policy evaluation order**: Explicit Deny > SCP > Permission Boundary > Identity Policy > Resource Policy — a single Deny overrides all Allows
- **Credential report generation**: Takes a few seconds; poll `generate-credential-report` until state is `COMPLETE`
- **Access Advisor lag**: Service last accessed data can be 4+ hours behind — do not use for real-time decisions
- **Trust policy vs permissions**: A role's trust policy controls WHO can assume it; attached policies control WHAT it can do — both must be reviewed
- **AWS-managed vs customer-managed**: `arn:aws:iam::aws:policy/*` are AWS-managed and cannot be modified — only audit customer-managed policies for changes
- **Inline vs managed policies**: Inline policies are embedded in users/roles/groups and not reusable — check both types during audits
- **SCP interaction**: Organization SCPs can restrict permissions even if IAM allows them — check Organizations if permissions seem unexpectedly denied
- **Wildcard resources**: `"Resource": "*"` grants access to ALL resources — flag these during policy reviews
