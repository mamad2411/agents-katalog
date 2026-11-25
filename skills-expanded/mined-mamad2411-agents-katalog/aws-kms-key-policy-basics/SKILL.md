---
name: aws-kms-key-policy-basics
description: >
  AWS KMS key policies for owned CMKs: default root behavior, key admins vs users,
  service principal statements, encryption context conditions, cross-account use,
  and avoiding lockout. Use when creating or reviewing customer managed keys —
  not for unauthorized decryption or disabling others’ keys.
---

# AWS KMS Key Policy Basics

## Scope And Authorization

- **In scope:** Customer managed KMS keys and their key policies in authorized accounts.
- **Out of scope:** Attempting to alter or misuse keys outside authorization.
- Key policies are the root of KMS authorization — a mistake can lock out admins or open decrypt to the world.
- Prefer CMKs for sensitive workloads; understand AWS managed key limitations.
- Pair with `aws-kms-grants` for temporary access; `aws-iam-least-privilege` for identity policies.

## When To Use

- Creating CMKs for S3, EBS, RDS, secrets, or app envelope encryption.
- Separating key administrators from key users.
- Enabling CloudWatch Logs / ASG / other services to use your CMK.
- Cross-account decrypt/encrypt patterns.
- Fixing `AccessDeniedException` on KMS despite IAM allows.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Temporary KMS grants | `aws-kms-grants` |
| IAM identity policy design | `aws-iam-least-privilege` |
| S3 default encryption setup | `aws-s3-bucket-hardening` |
| Secrets storage choice | `aws-parameter-store-vs-secrets` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Statement purpose | Typical principals |
| --- | --- |
| Key admins | IAM admins roles — put key policy, schedule delete |
| Key users | app roles — encrypt/decrypt/generate data key |
| Services | `logs.REGION.amazonaws.com`, `s3.amazonaws.com`, etc. with conditions |
| Root | Account root enable IAM policies to matter |

**Critical fact:** If the key policy does not allow the account/root (or equivalent), IAM policies alone may not grant use. Default console policies usually enable IAM via root.

## Minimal Safe Structure (illustrative)

```json
{
  "Version": "2012-10-17",
  "Id": "key-policy",
  "Statement": [
    {
      "Sid": "EnableRootIdentityPolicies",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::ACCT:root" },
      "Action": "kms:*",
      "Resource": "*"
    },
    {
      "Sid": "KeyAdmins",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::ACCT:role/KmsAdmins" },
      "Action": [
        "kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*",
        "kms:Update*", "kms:Revoke*", "kms:Disable*", "kms:Get*", "kms:Delete*",
        "kms:ScheduleKeyDeletion", "kms:CancelKeyDeletion", "kms:TagResource"
      ],
      "Resource": "*"
    },
    {
      "Sid": "KeyUsers",
      "Effect": "Allow",
      "Principal": { "AWS": "arn:aws:iam::ACCT:role/AppRole" },
      "Action": [
        "kms:Encrypt", "kms:Decrypt", "kms:ReEncrypt*",
        "kms:GenerateDataKey*", "kms:DescribeKey"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": { "kms:EncryptionContext:service": "payments" }
      }
    }
  ]
}
```

Narrow admin actions further when possible; `kms:*` for root is common to enable IAM but review org standards.

## Workflow

### 1. Confirm scope and success criteria

1. Record key purpose, Region, multi-Region key needs, admins, users, services.
2. Success: admins manage key; apps encrypt/decrypt only with context; deletion protection; no anonymous principals.
3. Break-glass: second admin role or root procedure documented offline.

### 2. Inventory keys and policies

```bash
aws kms list-keys
aws kms list-aliases
aws kms get-key-policy --key-id alias/app-prod --policy-name default --output text
aws kms describe-key --key-id alias/app-prod
```

1. Flag policies with `"Principal":"*"` without tight conditions.
2. Note pending deletion keys.
3. Map aliases to applications.

### 3. Baseline

1. Export key policy JSON to Git (as IaC).
2. Test current encrypt/decrypt with app role.
3. Snapshot key rotation status (`key-rotation-status`).

### 4. Apply key policy design

1. **Separate** admin vs use statements.
2. **Services:** follow AWS docs for each service’s required ViaService / encryption context conditions (CloudWatch Logs, Yubi, etc.).
3. **Cross-account:** grant external account root or roles carefully; external still needs IAM in their account.
4. **Conditions:** `kms:CallerAccount`, `kms:EncryptionContext`, `kms:ViaService`, `aws:PrincipalOrgID`.
5. **Rotation:** enable automatic annual rotation for symmetric CMKs when compatible.
6. **Deletion:** prefer disable + waiting period; multi-person approval for schedule delete.

```bash
aws kms put-key-policy --key-id alias/app-prod --policy-name default --policy file://key-policy.json
aws kms enable-key-rotation --key-id alias/app-prod
```

### 5. Verify with evidence

```bash
# As app role
aws kms generate-data-key --key-id alias/app-prod --key-spec AES_256 \
  --encryption-context service=payments
# Wrong context should fail if enforced
aws kms generate-data-key --key-id alias/app-prod --key-spec AES_256 \
  --encryption-context service=other || true
# As non-principal role expect deny
```

1. Confirm admins can `get-key-policy` and cannot be locked out (have break-glass).
2. Integration: S3/RDS/secret using key succeeds.
3. CloudTrail: Decrypt events only from expected roles.

### 6. Observe and harden

1. Alert on `PutKeyPolicy`, `ScheduleKeyDeletion`, `DisableKey`.
2. Access Analyzer for external key access if applicable.
3. Quarterly review of principals in key policies.

### 7. Hand off

1. Key catalog: alias, purpose, owners, rotation, policy repo path.
2. How apps must set encryption context.
3. Incident: revoke via policy edit + grant revoke (`aws-kms-grants`).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Root/IAM | enable identity policies intentionally | remove root and lock everyone out |
| Principals | named roles | `Principal":"*"` decrypt |
| Context | required for app use | no context multi-tenant key |
| Admins | small role set | every developer admin |
| Services | conditioned ViaService | blanket service principal unlimited |
| Delete | waiting period + dual control | immediate delete on prod key |

## Output Checklist

- [ ] Key purpose, alias, owners recorded
- [ ] Policy exported and reviewed
- [ ] Admin vs user separation applied
- [ ] Service principals conditioned
- [ ] Encryption context requirements documented
- [ ] Rotation enabled where appropriate
- [ ] Positive/negative use tests evidenced
- [ ] Alerts on policy/deletion events
- [ ] Break-glass admin path confirmed
- [ ] Grants companion considered

## Rules

- Authorized CMKs only.
- Never ship key policies that allow world decrypt.
- Avoid lockout: test admin access after changes in non-prod first.
- Encryption context is part of authorization design.
- Focus on key policies; temporary grants in `aws-kms-grants`.
