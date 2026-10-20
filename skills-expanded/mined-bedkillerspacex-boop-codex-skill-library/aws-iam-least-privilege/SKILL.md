---
name: aws-iam-least-privilege
description: >
  AWS IAM least privilege for owned accounts: identity vs resource policies, action
  and resource ARNs, condition keys, permission boundaries, session policies, and
  iterative tightening from CloudTrail. Use when designing roles for apps/humans —
  not for privilege escalation against accounts you do not own.
---

# AWS IAM Least Privilege

## Scope And Authorization

- **In scope:** IAM policies, roles, users, and permission boundaries in authorized accounts.
- **Out of scope:** Attempting to expand privileges in third-party AWS environments.
- Over-broad wildcards (`*/*`) are a primary cloud risk — treat policy review as security-critical.
- Prefer roles + SSO over long-lived access keys.
- Pair with `aws-iam-policy-simulator` and `aws-iam-access-analyzer-unused`; IaC with `code-quality-standards`.

## When To Use

- Creating task/pod/Lambda execution roles.
- Replacing `Action: *` / `Resource: *` in production policies.
- Applying condition keys (`aws:SourceVpce`, `aws:PrincipalOrgID`, MFA).
- Designing permission boundaries for developers/power users.
- Reviewing trust policies for confused deputy risks.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Unused access cleanup | `aws-iam-access-analyzer-unused` |
| Dry-run evaluation | `aws-iam-policy-simulator` |
| Roles Anywhere for on-prem | `aws-iam-roles-anywhere` |
| KMS key policies | `aws-kms-key-policy-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Lever | Use |
| --- | --- |
| Actions | Fine-grained service actions; avoid `service:*` unless temporary |
| Resources | Specific ARNs; patterns only as wide as needed |
| Conditions | Network, MFA, tags, org ID, source account |
| Boundary | Max permissions ceiling for principals you vend |
| Session policy | Further reduce STS assumed sessions |
| Trust policy | Who can assume; service principals; conditions |

## Policy Building Blocks

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadAppBucket",
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::app-data-prod",
        "arn:aws:s3:::app-data-prod/prefix/*"
      ],
      "Condition": {
        "StringEquals": { "aws:RequestedRegion": "us-east-1" }
      }
    }
  ]
}
```

**Trust policy (service) sketch:**

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": "sts:AssumeRole",
    "Condition": {
      "StringEquals": { "aws:SourceAccount": "ACCT" }
    }
  }]
}
```

## Workflow

### 1. Confirm scope and success criteria

1. Record principal type (human/app), account, data class, required tasks.
2. Success: app works with explicit allows only; simulator/canaries pass; Access Analyzer clean of obvious overshare; no standing admin.
3. Define non-goals (e.g., temporary break-glass separate role).

### 2. Inventory current permissions

```bash
aws iam list-attached-role-policies --role-name "$ROLE"
aws iam list-role-policies --role-name "$ROLE"
aws iam get-role --role-name "$ROLE"
aws iam get-policy-version --policy-arn "$ARN" --version-id "$V"
```

1. Expand AWS managed admin policies attached to custom roles.
2. Note resource wildcards and missing conditions.
3. Pull CloudTrail for actual actions used (last 30–90 days).

### 3. Baseline

1. Save full effective policy set (identity + boundaries).
2. Capture working canary requests (read object, write queue, etc.).
3. Snapshot policy versions for rollback.

### 4. Apply least privilege iteratively

**Method A — start deny-broad, add from CloudTrail**

1. Begin with empty/custom minimal policy in non-prod.
2. Run integration tests; add missing actions/resources as AccessDenied appears.
3. Promote to prod with same ARNs (account/Region parameterized).

**Method B — shrink existing**

1. Generate service last accessed; remove unused services.
2. Replace `Resource: *` with explicit ARNs.
3. Add conditions: `aws:PrincipalTag`, `ec2:ResourceTag`, MFA for humans.

**Human access**

1. SSO permission sets with job functions; time-bound elevation for admin.
2. Require MFA conditions on sensitive actions (`iam:*`, `s3:DeleteBucket`, KMS deletes).
3. Permission boundaries for anyone who can create roles.

**Anti-patterns to remove**

| Bad | Replace with |
| --- | --- |
| `Action":"*"` | enumerated actions |
| `Resource":"*"` on data services | object/table/queue ARNs |
| Trust `Principal":"*"` | specific AWS principals + conditions |
| Long-lived AKIA admin | SSO + role |

### 5. Verify with evidence

```bash
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::ACCT:role/"$ROLE" \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::app-data-prod/prefix/o.txt
# App canaries
# Access Analyzer external access findings for related resources
```

1. Negative tests: role cannot read other teams’ buckets.
2. Human admin path still works via separate break-glass.
3. Document residual wildcards with tickets.

### 6. Observe and harden

1. Access Analyzer unused + external analyzers continuous.
2. CloudTrail metrics on AccessDenied for the role (sudden spikes after shrink).
3. Quarterly review of managed policy AWS updates if using AWS managed.

### 7. Hand off

1. Role catalog: purpose, owner, policy ARNs, data class.
2. IaC modules with forced conditions for org ID / source account.
3. Link simulator and unused analyzer skills in runbooks.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Actions | explicit list | `*:` or service admin managed casually |
| Resources | ARNs + prefixes | `*` on S3/KMS |
| Trust | service + source account | any account assume |
| Humans | SSO + MFA + JIT | shared admin keys |
| Boundaries | on builders | builders can create unbounded roles |
| Evolution | CloudTrail-informed | copy-paste from blogs with `*` |

## Output Checklist

- [ ] Principal purpose and data class recorded
- [ ] Current policies inventoried
- [ ] CloudTrail/last-accessed used for evidence
- [ ] Actions/resources/conditions tightened
- [ ] Trust policies reviewed for deputy risks
- [ ] Simulator/canary evidence green
- [ ] Negative authorization tests done
- [ ] Break-glass separated and documented
- [ ] Owners + review date set
- [ ] `code-quality-standards` on IaC policies

## Rules

- Authorized accounts only.
- Default deny; explicit allow only what is required.
- Separate break-glass from daily driver roles.
- Conditions are part of least privilege, not optional polish.
- Focus on designing least privilege; unused cleanup and simulation are companions.
