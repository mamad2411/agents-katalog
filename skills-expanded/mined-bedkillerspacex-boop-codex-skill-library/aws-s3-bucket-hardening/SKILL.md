---
name: aws-s3-bucket-hardening
description: >
  AWS S3 bucket hardening for owned cloud accounts: Block Public Access, encryption
  (SSE-S3/SSE-KMS), bucket policies and ACLs, versioning, access logging, TLS-only
  access, and ownership controls. Use when reviewing public buckets, missing BPA,
  plaintext objects, overly broad Principal "*", or hardening app/logs/tfstate buckets —
  not for abusing third-party buckets.
---

# AWS S3 Bucket Hardening

## Scope And Authorization

- **In scope:** S3 buckets in AWS accounts you own, operate, or assess under written authorization.
- **Out of scope:** Enumerating or abusing third-party buckets, unauthorized open-bucket hunting, or data exfiltration.
- Prefer non-production validation first; schedule production policy changes in a change window.
- Redact bucket ARNs with customer data, access keys, and object paths from tickets when required by policy.
- Pair IaC/app code changes with `code-quality-standards`.

## When To Use

- Hardening application, logs, backups, artifacts, or Terraform state buckets.
- Findings: public ACL/policy, missing Block Public Access, unencrypted default, `Principal: "*"` without conditions.
- Enabling versioning, server access logging / CloudTrail data events, TLS-only policies.
- Ownership Controls (`BucketOwnerEnforced`) migration away from ACLs.
- CIS / AWS Foundational Security Best Practices gaps on S3.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| S3 Object Lock / WORM retention | `aws-s3-object-lock` |
| Org-wide deny via SCPs | `aws-scps-organization` |
| Secrets rotation in Secrets Manager | `aws-secrets-manager-rotation` |
| Generic secrets hygiene / git leaks | `secrets-management-hygiene` |
| Terraform state / provider hardening | `terraform-security-basics` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Block Public Access (BPA) | Account-level + bucket-level; all four settings on unless deliberate static website/CDN exception |
| Encryption | Default SSE-S3 or SSE-KMS; prefer CMK for regulated data; deny unencrypted `PutObject` |
| Access | Prefer bucket policies + IAM; disable ACLs (`BucketOwnerEnforced`); least-privilege principals |
| Transport | `aws:SecureTransport` true condition; optional VPC endpoint conditions |
| Durability / audit | Versioning on for critical data; access logging or CloudTrail data events; Config rules |
| Tooling | AWS CLI, Access Analyzer (S3), Config, Security Hub, CloudTrail, IaC (Terraform/CDK) |

## Workflow

### 1. Confirm scope and success criteria

1. Record account ID(s), region(s), bucket name/ARN list, owner team, data classification.
2. Success examples: BPA fully enabled; default encryption set; public access analyzer clean; TLS-only policy; no world-readable ACL.
3. Note break-glass: who can temporarily open access; ticket expiry.

### 2. Inventory buckets and exposure

```bash
aws sts get-caller-identity
aws s3api list-buckets --query "Buckets[].Name" --output text
BUCKET=example-app-prod
aws s3api get-public-access-block --bucket "$BUCKET"
aws s3api get-bucket-encryption --bucket "$BUCKET"
aws s3api get-bucket-versioning --bucket "$BUCKET"
aws s3api get-bucket-policy --bucket "$BUCKET"
aws s3api get-bucket-acl --bucket "$BUCKET"
aws s3api get-bucket-ownership-controls --bucket "$BUCKET"
aws s3api get-bucket-logging --bucket "$BUCKET"
aws s3api get-bucket-policy-status --bucket "$BUCKET"
```

1. Flag account-level BPA gaps: `aws s3control get-public-access-block --account-id "$ACCOUNT_ID"`.
2. Run Access Analyzer for S3 / Security Hub S3 controls if enabled.
3. List intentional public buckets (static sites, public assets) with owners and tickets.

### 3. Baseline before change

1. Export current policy JSON, ACL, BPA, encryption, ownership controls to a dated, access-controlled store.
2. Sample a few object ACLs if legacy ACLs exist.
3. Note apps that rely on public read or cross-account ACL grants.

### 4. Apply hardening controls

**Account-level BPA (preferred default):**

```bash
aws s3control put-public-access-block --account-id "$ACCOUNT_ID" --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

**Bucket-level BPA + encryption + ownership + versioning:**

```bash
aws s3api put-public-access-block --bucket "$BUCKET" --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

aws s3api put-bucket-encryption --bucket "$BUCKET" --server-side-encryption-configuration \
  '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"aws:kms","KMSMasterKeyID":"alias/s3-prod"},"BucketKeyEnabled":true}]}'

aws s3api put-bucket-ownership-controls --bucket "$BUCKET" --ownership-controls \
  'Rules=[{ObjectOwnership=BucketOwnerEnforced}]'

aws s3api put-bucket-versioning --bucket "$BUCKET" --versioning-configuration Status=Enabled
```

**TLS-only policy statement (merge carefully with existing policy):**

```json
{
  "Sid": "DenyInsecureTransport",
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": [
    "arn:aws:s3:::example-app-prod",
    "arn:aws:s3:::example-app-prod/*"
  ],
  "Condition": {
    "Bool": { "aws:SecureTransport": "false" }
  }
}
```

**Optional: deny puts missing SSE-KMS:**

```json
{
  "Sid": "DenyIncorrectEncryption",
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:PutObject",
  "Resource": "arn:aws:s3:::example-app-prod/*",
  "Condition": {
    "StringNotEquals": {
      "s3:x-amz-server-side-encryption": "aws:kms"
    }
  }
}
```

1. Replace `Principal: "*"` allow statements with specific IAM roles/accounts + conditions (`aws:PrincipalOrgID`, VPC endpoint IDs).
2. Enable server access logging to a dedicated logging bucket (separate account preferred) or ensure CloudTrail data events cover the bucket.
3. For tfstate/logs: restrict delete/list; consider Object Lock via `aws-s3-object-lock` where WORM is required.

### 5. Verify with evidence

```bash
aws s3api get-public-access-block --bucket "$BUCKET"
aws s3api get-bucket-encryption --bucket "$BUCKET"
aws s3api get-bucket-policy-status --bucket "$BUCKET"
aws s3api get-bucket-ownership-controls --bucket "$BUCKET"
# Expect failure when TLS/SSE policy is enforced incorrectly by client
aws s3api put-object --bucket "$BUCKET" --key probe.txt --body ./probe.txt || true
```

1. Confirm Access Analyzer / Config / Security Hub findings resolve or are exception-ticketed.
2. App smoke: authorized role can read/write; anonymous and wrong-account principals denied.
3. Keep redacted before/after policy diffs in the change ticket.

### 6. Observe and harden

1. CloudWatch/Security Hub alarms for public bucket policy changes, BPA disabled, encryption removed.
2. Periodic Config rules: `s3-bucket-public-read-prohibited`, `s3-bucket-ssl-requests-only`, `s3-bucket-server-side-encryption-enabled`.
3. Review cross-account grants and CloudFront OAC patterns annually.

### 7. Hand off

1. Document remaining public or cross-account exceptions with owner + expiry.
2. Update IaC so Console drift does not reintroduce ACLs or open policies.
3. Apply `code-quality-standards` to policy/Terraform modules.

## Control Matrix

| Control | Default target | Exception pattern |
| --- | --- | --- |
| Account BPA | All four true | Rare; document org waiver |
| Bucket BPA | All four true | Static website only if not using CloudFront |
| Default encryption | SSE-KMS (CMK) or SSE-S3 | Legacy SSE-S3 with plan |
| Ownership | BucketOwnerEnforced | Temporary ACL migration ticket |
| Versioning | Enabled on stateful/critical | Ephemeral caches may skip |
| TLS-only policy | Deny `SecureTransport=false` | None recommended |
| Logging | Access log bucket or data events | SIEM equivalent |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Public access | BPA + no public policy; CDN private origin | Public ACL “for testing” left on |
| Encryption | Default SSE + deny wrong SSE headers | Client-only optional encryption flags |
| Principals | Role ARNs + org/VPC conditions | `Principal: "*"` with only referer checks |
| ACLs | Disabled via BucketOwnerEnforced | Mixed ACL + policy ownership confusion |
| Verification | CLI + analyzer evidence | “Bucket looks private in Console list” |

## Output Checklist

- [ ] Scope, accounts, buckets, data class, authorization recorded
- [ ] Baseline policies/BPA/encryption exported
- [ ] Account and bucket BPA aligned to target
- [ ] Default encryption and TLS-only controls applied
- [ ] Ownership controls / ACL strategy decided
- [ ] Versioning and logging/audit path confirmed
- [ ] Public/cross-account exceptions ticketed with expiry
- [ ] Verification commands and app smoke evidence attached (redacted)
- [ ] Monitoring/Config rules considered
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Authorized accounts only; never use this skill to attack third-party storage.
- Prefer account-level BPA; treat public buckets as explicit products with owners.
- Do not disable logging or encryption “temporarily” without expiry and ticket.
- Keep secrets and customer object keys out of chat and git.
- Route Object Lock, org SCPs, and Secrets Manager work to their dedicated skills.
