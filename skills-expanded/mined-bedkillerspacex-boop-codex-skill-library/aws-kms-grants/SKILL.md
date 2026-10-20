---
name: aws-kms-grants
description: >
  AWS KMS grants for owned accounts: CreateGrant/RetireGrant, grant constraints,
  grantee principals, grant tokens, and least-privilege temporary permissions
  beyond key policies. Use when services or accounts need scoped cryptographic
  operations without permanent key policy expansion — not for unauthorized key use.
---

# AWS KMS Grants

## Scope And Authorization

- **In scope:** Customer managed keys (CMKs) and grants in accounts you own or manage with authorization.
- **Out of scope:** Creating grants on keys you do not control; decrypting third-party data without authority.
- Grants can allow decrypt/encrypt — treat grant creation as privileged.
- Prefer short-lived grants with constraints and automatic retirement.
- Pair with `aws-kms-key-policy-basics` for permanent policy design.

## When To Use

- Allowing a role/service to use a key without editing key policy for every principal.
- AWS services that create grants on your behalf (understand them).
- Cross-account use cases with grant tokens during eventual consistency windows.
- Auditing orphaned grants after migrations.
- Replacing overly broad key policy statements with constrained grants.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Key policy structure / admins | `aws-kms-key-policy-basics` |
| General IAM least privilege | `aws-iam-least-privilege` |
| S3 encryption defaults | `aws-s3-bucket-hardening` |
| Secrets Manager | secrets skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Grant | Capability token-like permission on a CMK for operations |
| Grantee principal | Who receives the grant permissions |
| Operations | Encrypt, Decrypt, GenerateDataKey, CreateGrant, RetireGrant, etc. |
| Constraints | Encryption context equality/substring requirements |
| Grant token | Returned for immediate use before eventual consistency |
| Retirement principal | Who may retire the grant |

## Grants vs Key Policy vs IAM

```text
Effective KMS authz ≈ key policy (required allow path) + IAM allow + grants − denies
```

Key policy must allow grant creation/use patterns; IAM alone cannot bypass key policy.

## Workflow

### 1. Confirm scope and success criteria

1. Record KeyId/ARN, intended grantee, operations, encryption context, lifetime.
2. Success: grantee can only required ops; context enforced; grant retired after job; CloudTrail shows grant lifecycle.
3. Identify who may create grants (key admins / services).

### 2. Inventory grants

```bash
KEY=arn:aws:kms:REGION:ACCT:key/KEY_ID
aws kms list-grants --key-id "$KEY"
aws kms list-retirable-grants --retiring-principal "$PRINCIPAL_ARN"
aws kms get-key-policy --key-id "$KEY" --policy-name default
```

1. Flag grants with `CreateGrant` operation (delegation risk).
2. Note grants without constraints on sensitive keys.
3. Map grants to owners/tags where possible.

### 3. Baseline

1. Export grant list JSON before changes.
2. Sample CloudTrail `CreateGrant` events for the key.
3. Document required encryption context keys for the app (e.g., `service=payments`).

### 4. Create constrained grants

```bash
aws kms create-grant \
  --key-id "$KEY" \
  --grantee-principal arn:aws:iam::ACCT:role/batch-job \
  --operations Decrypt Encrypt GenerateDataKey \
  --constraints EncryptionContextEquals={service=payments,env=prod} \
  --retiring-principal arn:aws:iam::ACCT:role/batch-job \
  --name payments-batch-2026q3
```

**Immediate use**

```bash
# Use GrantTokens in decrypt/encrypt APIs if needed right after create
aws kms decrypt --ciphertext-blob fileb://blob --grant-tokens "$TOKEN" ...
```

**Hardening rules**

1. Least operations: prefer `GenerateDataKey` + `Decrypt` over admin ops.
2. Avoid granting `CreateGrant` unless hierarchical delegation is required and reviewed.
3. Always set encryption context constraints for app data keys.
4. Set `RetiringPrincipal` so automation can clean up.
5. Prefer grants for ephemeral jobs; permanent access often better as key policy + IAM role.

**Retire / revoke**

```bash
aws kms retire-grant --grant-id "$GID" --key-id "$KEY"
# or
aws kms revoke-grant --key-id "$KEY" --grant-id "$GID"
```

Revoke is key admin style; retire is by retiring principal.

### 5. Verify with evidence

```bash
aws kms list-grants --key-id "$KEY" --query "Grants[?Name=='payments-batch-2026q3']"
# Positive: decrypt with correct encryption context succeeds
# Negative: wrong context fails; principal without grant fails
```

1. Confirm grant token path works for latency-sensitive create-then-use.
2. After retire, operations fail as expected.
3. CloudTrail contains CreateGrant/RetireGrant with actor identity.

### 6. Observe and harden

1. Periodic list-grants; ticket grants older than N days without owner.
2. Alert on CreateGrant with `CreateGrant` operation or missing constraints.
3. Integrate grant cleanup into job finalizers.

### 7. Hand off

1. Document when to use grants vs key policy statements.
2. Standard encryption context dictionary for the org.
3. Runbook for emergency revoke-grant.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Ops | minimal set | `*` operations including CreateGrant casually |
| Context | required equality constraints | no constraints on multi-tenant key |
| Lifetime | create/retire with job | permanent forgotten grants |
| Auth path | understand key policy still needed | grant-only myths |
| Audit | named grants + CloudTrail | anonymous pile of grants |
| Delegation | rare, reviewed | grantees can mint child grants freely |

## Output Checklist

- [ ] Key, grantee, ops, context documented
- [ ] Existing grants inventoried
- [ ] New grants constrained and named
- [ ] Retiring principal set
- [ ] Positive/negative crypto tests evidenced
- [ ] Cleanup/retire path verified
- [ ] Monitoring for risky grants
- [ ] Key policy compatibility confirmed (`aws-kms-key-policy-basics`)
- [ ] `code-quality-standards` for automation

## Rules

- Authorized keys only; grants are cryptographic power.
- Prefer encryption context constraints always for app data.
- Retire grants; do not accumulate forever.
- Avoid CreateGrant-to-others without strong review.
- Focus on grants; permanent key policy design in the companion skill.
