---
name: aws-s3-access-grants
description: >
  Amazon S3 Access Grants for owned accounts: identity-aware prefix grants mapped
  from IAM Identity Center / IAM principals, grant scopes, locations, and migration
  from broad bucket policies. Use when implementing scalable per-prefix access for
  data lakes — not for accessing buckets outside authorization.
---

# AWS S3 Access Grants

## Scope And Authorization

- **In scope:** S3 Access Grants instances, locations, and grants in AWS accounts you own or operate under authorization.
- **Out of scope:** Creating grants on third-party buckets; data exfiltration.
- Access Grants complement (not always replace) bucket policies, BPA, and encryption — keep baseline hardening.
- Prefer Identity Center users/groups for human data access at scale.
- Pair with `aws-s3-bucket-hardening`, `aws-iam-least-privilege`, `code-quality-standards`.

## When To Use

- Granting many users/groups read/write to specific prefixes without mega bucket policies.
- Mapping corporate directory identities to S3 prefixes.
- Reviewing grant sprawl and temporary grants.
- Integrating applications that call `get-data-access` for scoped credentials.
- Migrating from per-user IAM policies with wide `s3:*` on whole buckets.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| BPA/encryption/public block | `aws-s3-bucket-hardening` |
| Object Lock / WORM | `aws-s3-object-lock` |
| Cross-account RAM | `aws-ram-resource-share` |
| Generic IAM design | `aws-iam-least-privilege` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Object | Role |
| --- | --- |
| Access Grants instance | Account/Regional control plane for grants |
| Location | Registers S3 prefix/URI under grants (often whole bucket or prefix) with scope IAM role |
| Grant | Maps grantee identity to location subprefix with READ/WRITE |
| Credentials | Temporary credentials via Access Grants for the grant scope |
| IAM Identity Center | Common identity source for human grantees |

## Mental Model

```text
Identity (IDC user/group or IAM) + Grant (READ on s3://bucket/prefix/*)
  → get-data-access → short-lived creds scoped to that prefix
Location role must be able to access underlying S3
```

## Workflow

### 1. Confirm scope and success criteria

1. Record buckets, prefix layout, identity source (IDC/IAM), apps vs humans.
2. Success: grantee can only their prefix; others denied; BPA still on; grants inventoried with owners.
3. Decide which buckets enroll in Access Grants vs classic IAM only.

### 2. Inventory

```bash
aws s3control get-access-grants-instance --account-id "$ACCOUNT" 2>/dev/null || true
aws s3control list-access-grants-locations --account-id "$ACCOUNT"
aws s3control list-access-grants --account-id "$ACCOUNT"
aws s3api get-public-access-block --bucket "$BUCKET"
aws s3api get-bucket-policy --bucket "$BUCKET"
```

1. Existing bucket policy principals that grants might replace.
2. IDC groups for data domains.
3. Location IAM roles and their policies.

### 3. Baseline

1. Export grants and locations JSON.
2. Map data domains → prefixes (e.g., `s3://lake/domain=payments/`).
3. Confirm encryption and BPA baselines (`aws-s3-bucket-hardening`).

### 4. Configure Access Grants

1. Create Access Grants instance (once per account/Region pattern per current feature).
2. Register location for `s3://bucket` or prefix with a **location scope role** that has least S3 access to that path.
3. Create grants:

```bash
aws s3control create-access-grant \
  --account-id "$ACCOUNT" \
  --access-grants-location-id "$LOC" \
  --access-grants-location-configuration S3SubPrefix=team-a/ \
  --grantee GranteeType=DIRECTORY_GROUP,GranteeIdentifier="$IDC_GROUP_ARN" \
  --permission READ
```

4. Application pattern: call Access Grants `GetDataAccess` (API name per SDK) to obtain credentials; use them for S3 calls; refresh as needed.
5. Humans: IDC-integrated access via supported consoles/tools.
6. Prefer time-bound operational processes for contractor grants; delete when done.
7. Keep bucket policy deny statements for insecure transport and unencrypted puts.

**Location role policy:** only the prefixes it serves; no `s3:*` on `*`.

### 5. Verify with evidence

```bash
aws s3control list-access-grants --account-id "$ACCOUNT"
# As grantee identity: list/get own prefix succeeds
# Access other team prefix fails
# Anonymous still denied; BPA on
```

1. Credential scope: temporary keys cannot read outside grant prefix.
2. CloudTrail: data events show expected principals.
3. Remove grant → access revoked promptly.

### 6. Observe and harden

1. Periodic grant inventory; expire stale grants.
2. Alert on new locations registering sensitive buckets.
3. Access Analyzer still enabled for external access surprises.

### 7. Hand off

1. Prefix ownership table + grant request workflow.
2. App developer guide for GetDataAccess.
3. Emergency revoke grant steps.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Scope | prefix-level READ/WRITE | whole-bucket grants for everyone |
| Identity | IDC groups | one shared IAM user |
| Baseline | BPA + encryption still on | grants instead of BPA |
| Location role | least privilege path | admin on all buckets |
| Lifecycle | delete stale grants | permanent contractor access |
| Audit | inventory + CloudTrail | unknown grant sprawl |

## Output Checklist

- [ ] Buckets/prefixes/identities recorded
- [ ] Access Grants instance/locations configured
- [ ] Grants least privilege with owners
- [ ] Location IAM roles scoped
- [ ] BPA/encryption baselines verified
- [ ] Allow/deny tests evidenced
- [ ] App credential flow documented
- [ ] Stale grant review process
- [ ] Analyzer/hardening companions applied
- [ ] `code-quality-standards` for automation

## Rules

- Owned buckets only.
- Access Grants do not replace encryption, BPA, or logging.
- Prefer group-based grants and short-lived credentials.
- Inventory and expire grants regularly.
- Focus on Access Grants; general bucket hardening in `aws-s3-bucket-hardening`.
