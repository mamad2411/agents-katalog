---
name: aws-s3-object-lock
description: >
  Amazon S3 Object Lock for owned accounts: governance vs compliance mode, retention
  periods, legal holds, bucket-level default retention, and WORM protection for logs,
  backups, and evidence. Use when enabling Object Lock on new buckets, setting retain-
  until dates, or verifying immutability — not for bypassing retention on systems you
  do not own or for generic bucket public-access hardening alone.
---

# AWS S3 Object Lock

## Scope And Authorization

- **In scope:** Buckets and objects in AWS accounts you own or are authorized to harden (backups, audit logs, ransomware-resistant archives, legal hold).
- **Out of scope:** Attempting to shorten compliance-mode retention without proper legal/process authority; third-party bucket abuse.
- Object Lock is enabled at bucket creation (or via supported migration); plan versioning and capacity first.
- Redact object keys that embed PII; treat legal-hold inventories as sensitive.
- Pair automation/IaC with `code-quality-standards`.

## When To Use

- Immutable backups, CloudTrail/log archives, ransomware recovery stores, regulatory WORM.
- Choosing **GOVERNANCE** vs **COMPLIANCE** retention mode.
- Applying per-object retain-until-date, default bucket retention, or legal hold.
- Verifying that overwrite/delete of protected versions is denied as designed.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Public access / encryption / TLS bucket hardening | `aws-s3-bucket-hardening` |
| Org SCPs denying S3 deletes globally | `aws-scps-organization` |
| Secrets Manager rotation | `aws-secrets-manager-rotation` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Detail |
| --- | --- |
| Versioning | Required; Object Lock protects object **versions** |
| Governance mode | Privileged users with `s3:BypassGovernanceRetention` can override if IAM allows |
| Compliance mode | No principal (including root) can shorten/remove retention until expiry |
| Legal hold | On/off flag independent of retention period; holds until released |
| Default retention | Bucket-level default applied on new objects |
| Tooling | AWS CLI lock configuration, retention, legal-hold APIs; CloudTrail data events |

## Workflow

### 1. Confirm scope and success criteria

1. Record account, region, bucket purpose, retention days/years, mode (GOVERNANCE/COMPLIANCE), legal owners.
2. Success: Object Lock enabled; versioning On; test object cannot be deleted until retain-until; compliance mode cannot be bypassed.
3. Compliance mode is effectively irreversible for the retention window — get legal/compliance sign-off first.

### 2. Inventory and prerequisites

```bash
aws sts get-caller-identity
BUCKET=audit-logs-prod
aws s3api get-bucket-versioning --bucket "$BUCKET"
aws s3api get-object-lock-configuration --bucket "$BUCKET"
aws s3api get-public-access-block --bucket "$BUCKET"
```

1. If Object Lock is not enabled on an existing ordinary bucket, plan **new bucket + copy/replication**.
2. Confirm MFA Delete policy if org requires it (separate from Object Lock).
3. Ensure BPA and encryption baselines via `aws-s3-bucket-hardening`.

### 3. Baseline

1. Document current retention policy, legal-hold process, and who holds governance bypass.
2. Estimate storage growth under versioning + long retention.
3. Sample critical prefixes (e.g. `AWSLogs/`, `backups/`).

### 4. Enable and configure Object Lock

**Create bucket with Object Lock:**

```bash
aws s3api create-bucket --bucket "$BUCKET" --region us-east-1 \
  --object-lock-enabled-for-bucket

aws s3api put-bucket-versioning --bucket "$BUCKET" \
  --versioning-configuration Status=Enabled

aws s3api put-object-lock-configuration --bucket "$BUCKET" --object-lock-configuration '{
  "ObjectLockEnabled": "Enabled",
  "Rule": {
    "DefaultRetention": {
      "Mode": "COMPLIANCE",
      "Days": 365
    }
  }
}'
```

**Per-object retention / legal hold:**

```bash
aws s3api put-object --bucket "$BUCKET" --key evidence/case-1.bin --body ./case-1.bin \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "2027-07-01T00:00:00Z"

aws s3api put-object-legal-hold --bucket "$BUCKET" --key evidence/case-1.bin \
  --legal-hold Status=ON

aws s3api put-object-retention --bucket "$BUCKET" --key evidence/case-1.bin \
  --retention "Mode=GOVERNANCE,RetainUntilDate=2026-12-31T00:00:00Z"
```

1. IAM for governance bypass must be break-glass only: `s3:BypassGovernanceRetention` with strong controls.
2. Never assume an API bypass for COMPLIANCE before expiry.
3. Align lifecycle rules carefully with locked noncurrent versions.

### 5. Verify with evidence

```bash
aws s3api get-object-lock-configuration --bucket "$BUCKET"
aws s3api head-object --bucket "$BUCKET" --key evidence/case-1.bin
aws s3api get-object-retention --bucket "$BUCKET" --key evidence/case-1.bin
aws s3api get-object-legal-hold --bucket "$BUCKET" --key evidence/case-1.bin
aws s3api delete-object --bucket "$BUCKET" --key evidence/case-1.bin --version-id "$VID" || true
```

1. Overwrite same key → new version; old locked version remains.
2. In GOVERNANCE, only designated break-glass role can bypass; daily roles cannot.
3. Record CLI output (redacted keys) in the change ticket.

### 6. Observe and harden

1. CloudTrail data events for `DeleteObject`, `PutObjectRetention`, `BypassGovernanceRetention`, legal hold changes.
2. Alerts on Object Lock configuration removal attempts and unexpected public access.
3. Periodic inventory of objects under legal hold for legal review.

### 7. Hand off

1. Runbook: place legal hold, approve governance bypass, retention calendar.
2. IaC modules for Object Lock buckets only for audit data classes.
3. Cross-link general bucket hardening checklist.

## Mode Selection

| Mode | Use when | Risk |
| --- | --- | --- |
| GOVERNANCE | Operational immutability; rare admin override needed | Bypass if IAM too broad |
| COMPLIANCE | Regulatory WORM; no technical override | Mistaken long retention is costly |
| Legal hold | Indefinite preserve for investigation/litigation | Process debt if never released |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Bucket creation | Object Lock enabled at create | Assuming Lock can be bolted on later casually |
| Mode choice | Compliance only with signed retention policy | Compliance “to be safe” for scratch data |
| Governance IAM | Break-glass role + MFA + ticket | `s3:*` on admin SSO with bypass |
| Verification | Failed delete of locked version recorded | “Versioning is on so we are fine” |
| Lifecycle | Compatible with retention | Aggressive expire deleting protected versions unexpectedly |

## Output Checklist

- [ ] Authorization, retention policy owner, mode, and duration documented
- [ ] Versioning + Object Lock configuration verified
- [ ] Default and/or per-object retention applied as designed
- [ ] Legal hold process defined (if used)
- [ ] Delete/overwrite tests show expected denials
- [ ] Governance bypass IAM reviewed (if GOVERNANCE)
- [ ] CloudTrail / alerting for retention changes considered
- [ ] BPA/encryption baseline still met (`aws-s3-bucket-hardening`)
- [ ] `code-quality-standards` applied if automation shipped

## Rules

- Authorized accounts and lawful retention purposes only.
- Treat COMPLIANCE retention as permanent for the period — double-check days/years.
- Do not weaken BPA or encryption when adding Object Lock.
- Never paste production object keys with sensitive paths into public tickets.
- Focus this skill on WORM/Object Lock; route general S3 hardening elsewhere.
