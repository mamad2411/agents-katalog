---
name: aws-sso-permission-sets
description: >
  AWS IAM Identity Center (successor to AWS SSO) permission sets for owned orgs:
  session duration, managed/inline policies, account assignments, permission
  boundaries, ABAC attributes, and least-privilege admin patterns. Use when designing
  or reviewing Identity Center access to AWS accounts — not for application OIDC
  user login alone or third-party org takeover.
---

# AWS IAM Identity Center Permission Sets

## Scope And Authorization

- **In scope:** Identity Center instances and AWS account assignments you administer.
- **Out of scope:** Changing identity providers or assignments without IAM/security authority; accessing member accounts outside role.
- Over-privileged permission sets equal standing admin — treat like production IAM.
- Pair with `aws-scps-organization` for org guardrails; use `code-quality-standards` for IaC.

## When To Use

- Creating ReadOnly, PowerUser, Admin break-glass, or app-team permission sets.
- Mapping IdP groups → permission sets → accounts.
- Reducing `AdministratorAccess` on daily duties; shorter sessions; job functions.
- Reviewing inline policies and customer managed policies attached to permission sets.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Org SCPs | `aws-scps-organization` |
| Secrets Manager rotation | `aws-secrets-manager-rotation` |
| Azure PIM eligible roles | `azure-pim-eligible-roles` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Permission set | IAM policy template provisioned as roles per account assignment |
| Assignment | Principal (user/group) + permission set + account |
| Session duration | Max console/CLI session length for that set |
| Permission boundary | Optional ceiling on the provisioned role |
| Identity store | Users/groups from IdP (SCIM) or Identity Center store |
| Tooling | `sso-admin`, `identitystore` CLI, Console, Terraform `aws_ssoadmin_*` |

## Workflow

### 1. Confirm scope and success criteria

1. Identity Center region/instance ARN, target accounts, IdP groups, change ticket.
2. Success: group members assume intended role only; admin set is break-glass; Access Analyzer clean.
3. Break-glass: offline root/process if Identity Center misconfigured.

### 2. Inventory permission sets and assignments

```bash
aws sts get-caller-identity
INSTANCE_ARN=$(aws sso-admin list-instances --query "Instances[0].InstanceArn" --output text)
aws sso-admin list-permission-sets --instance-arn "$INSTANCE_ARN"
aws sso-admin describe-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN"
aws sso-admin list-managed-policies-in-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN"
aws sso-admin get-inline-policy-for-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN"
aws sso-admin list-accounts-for-provisioned-permission-set --instance-arn "$INSTANCE_ARN" --permission-set-arn "$PS_ARN"
aws sso-admin list-account-assignments --instance-arn "$INSTANCE_ARN" --account-id "$ACCOUNT_ID" --permission-set-arn "$PS_ARN"
```

1. Flag any daily-driver assignment of `AdministratorAccess`.
2. List permission sets with session duration > 8–12h for high privilege.
3. Map orphaned assignments (left company but group residual).

### 3. Baseline least privilege model

| Persona | Permission set pattern | Session |
| --- | --- | --- |
| Viewer | `ViewOnlyAccess` or custom read | 4h |
| Developer nonprod | PowerUser-like minus IAM/org | 8h |
| Developer prod | App-scoped custom policies | 4h |
| Security audit | SecurityAudit + limited | 4h |
| Break-glass admin | AdministratorAccess + ticket | 1h + MFA via IdP |

### 4. Create or harden permission sets

```bash
aws sso-admin create-permission-set \
  --instance-arn "$INSTANCE_ARN" \
  --name "ps-app-dev-readonly" \
  --session-duration "PT4H" \
  --description "Read-only for app developers"

aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn "$INSTANCE_ARN" \
  --permission-set-arn "$PS_ARN" \
  --managed-policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess

# Optional inline deny for dangerous actions even on power users
aws sso-admin put-inline-policy-to-permission-set \
  --instance-arn "$INSTANCE_ARN" \
  --permission-set-arn "$PS_ARN" \
  --inline-policy file://deny-iam-org.json

aws sso-admin create-account-assignment \
  --instance-arn "$INSTANCE_ARN" \
  --target-id "$ACCOUNT_ID" --target-type AWS_ACCOUNT \
  --permission-set-arn "$PS_ARN" \
  --principal-type GROUP --principal-id "$GROUP_ID"

aws sso-admin provision-permission-set \
  --instance-arn "$INSTANCE_ARN" \
  --permission-set-arn "$PS_ARN" \
  --target-type ALL_PROVISIONED_ACCOUNTS
```

1. Prefer customer managed policies versioned in git over huge inline JSON.
2. Use permission boundaries for sets that still need broad service access.
3. ABAC: tag-based conditions on permission sets when attributes come from IdP.
4. Remove standing admin; require group membership just-in-time via IdP PAM if available.

### 5. Verify with evidence

```bash
# As a test user in the group: aws sso login ; assume role into account
aws sts get-caller-identity
aws iam list-attached-role-policies --role-name "AWSReservedSSO_ps-app-dev-readonly_..."
# Expect denied: iam:CreateUser, organizations:LeaveOrganization, etc.
```

1. Confirm only intended accounts appear in the user portal.
2. Access Analyzer / CloudTrail: review high-privilege usage weekly.
3. Offboard test: remove from IdP group → assignment gone after sync.

### 6. Observe and harden

1. CloudTrail `CreateAccountAssignment`, `AttachManagedPolicy...`, permission set updates.
2. Periodic access reviews of admin and prod write sets.
3. Align SCPs so even admin sets cannot disable org security services.

### 7. Hand off

1. Catalog of permission sets with owners and intended groups.
2. IaC module for assignments; ban Console-only drift for prod.
3. Break-glass procedure documented and tested.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Daily access | Scoped job-function sets | Everyone has AdministratorAccess |
| Session | Short for high privilege | 12h admin sessions default |
| Policies | Git-reviewed managed policies | Unreviewed inline `*` |
| Assignments | Group-based | Per-user snowflakes at scale |
| Offboarding | SCIM + access review | Orphan SSO roles months later |

## Output Checklist

- [ ] Instance ARN and IdP integration confirmed
- [ ] Permission sets inventoried; admin usage flagged
- [ ] Least-privilege sets designed per persona
- [ ] Assignments group-based and documented
- [ ] Provisioning completed to target accounts
- [ ] Test user verification (allow + deny) evidenced
- [ ] Session durations appropriate
- [ ] Monitoring/access review scheduled
- [ ] SCPs considered for hard guardrails
- [ ] `code-quality-standards` applied to IaC

## Rules

- Authorized identity administration only.
- No standing production admin without break-glass process.
- Prefer groups + SCIM over manual users.
- Permission sets are not a substitute for SCPs or resource policies.
- Never embed long-lived access keys as a workaround for SSO issues.
