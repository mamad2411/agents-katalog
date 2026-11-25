---
name: cloud-native-storage-strategy
description: >
  Guides choosing and configuring cloud storage services — object storage
  (S3, Azure Blob, GCS), block storage, file storage, and lifecycle/
  tiering policies — with encryption, access control, and cost-tiering
  best practices across AWS, Azure, and GCP. Use when a user asks to
  "design a storage architecture", "choose between object/block/file
  storage", "set up storage lifecycle/tiering policies", "encrypt data at
  rest", "prevent a storage bucket from being public", "reduce storage
  costs", or "pick a storage class for infrequently accessed data".
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Cloud-Native Storage Strategy

## Purpose

Storage decisions compound: the wrong storage class silently inflates
cost every month, a bucket/container left with default-permissive access
becomes a headline data breach, and a lifecycle policy applied without
understanding retrieval patterns can turn "save money" into "delete data
we needed." This skill covers choosing the right storage primitive
(object, block, file) for the workload, applying encryption and
access-control defaults that are safe out of the box, and designing
lifecycle/tiering policies that reduce cost without silently increasing
retrieval latency or cost for data that's actually still needed
regularly.

## When to use

- Choosing between object storage (S3/Blob/GCS), block storage (EBS/
  Managed Disks/Persistent Disk), and file storage (EFS/Azure Files/
  Filestore) for a new workload.
- Designing or auditing bucket/container/storage-account access controls
  and encryption defaults.
- Setting up lifecycle policies to move data between storage tiers
  (hot/cool/cold/archive) based on access patterns.
- Investigating unexpectedly high storage costs or unexpectedly slow/
  expensive data retrieval.
- Responding to a security finding like "publicly accessible storage
  bucket" or "storage account without encryption enforced."
- Planning storage for a new data pipeline, backup target, or static
  content/CDN origin.

## Prerequisites & environment

- Clarity on the workload's actual access pattern before choosing a
  storage class: how often is data read/written, how quickly must a read
  return (milliseconds vs. minutes-to-hours for archive tiers), and how
  long must data be retained (see `disaster-recovery-and-backup-strategy`
  for retention/backup-specific concerns, which overlap but are not
  identical to lifecycle tiering).
- Cloud CLI/Terraform access appropriate to the storage service:
  Terraform ≥ 1.5 with `aws`/`azurerm`/`google` providers ≥ their current
  major version for lifecycle and encryption resources.
- The account/subscription/project's landing-zone guardrails already in
  place (e.g. an SCP/Organization Policy/Azure Policy that blocks public
  bucket ACLs by default) — storage security should be defense-in-depth,
  not solely per-resource configuration; see the relevant
  `*-landing-zone-setup` skill.
- A key management strategy decided (cloud-managed keys vs.
  customer-managed keys in AWS KMS / Azure Key Vault / GCP Cloud KMS) —
  customer-managed keys add operational overhead (rotation, access
  policy) but are often required for regulated data.

## Step-by-step guidance

1. **Match the storage primitive to the access pattern:**
   - **Object storage** (S3, Azure Blob, GCS) for unstructured data
     accessed over HTTP(S) APIs — static assets, data lake files, backup
     targets, logs. Effectively unlimited scale, pay-per-GB-and-request.
   - **Block storage** (EBS, Azure Managed Disks, GCP Persistent Disk)
     for a single VM's low-latency, POSIX-filesystem-backed disk —
     databases, boot volumes. Attached to one instance at a time in most
     configurations (multi-attach exists but is the exception, not the
     default).
   - **File storage** (EFS, Azure Files, Filestore) for POSIX or SMB file
     shares accessed concurrently by multiple instances — shared config,
     content management systems, legacy lift-and-shift apps expecting a
     shared filesystem.
   Don't default to block storage for something object storage handles
   better (e.g. storing user-uploaded files on an EBS volume instead of
   S3) — it's a common lift-and-shift anti-pattern that blocks
   horizontal scaling later.

2. **Set secure defaults at creation, not as an afterthought:**
   - **AWS S3**: enable S3 Block Public Access at the account level (in
     addition to per-bucket), default encryption with SSE-KMS, and
     versioning for anything mutable:
     ```hcl
     resource "aws_s3_bucket_public_access_block" "this" {
       bucket                  = aws_s3_bucket.data.id
       block_public_acls       = true
       block_public_policy     = true
       ignore_public_acls      = true
       restrict_public_buckets = true
     }

     resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
       bucket = aws_s3_bucket.data.id
       rule {
         apply_server_side_encryption_by_default {
           sse_algorithm     = "aws:kms"
           kms_master_key_id = aws_kms_key.data.arn
         }
       }
     }
     ```
   - **Azure Blob**: set the storage account's public network access and
     "allow blob public access" to disabled, enforce HTTPS-only traffic,
     and use a customer-managed key in Key Vault if required by
     compliance scope.
   - **GCP Cloud Storage**: enable uniform bucket-level access (disables
     legacy per-object ACLs), set the bucket's public access prevention
     to `enforced`, and use a CMEK from Cloud KMS if required.

3. **Design the lifecycle/tiering policy from real access-frequency
   data, not intuition.** Example AWS S3 lifecycle rule moving log data
   through tiers:
   ```hcl
   resource "aws_s3_bucket_lifecycle_configuration" "logs" {
     bucket = aws_s3_bucket.logs.id
     rule {
       id     = "tier-down-logs"
       status = "Enabled"
       transition {
         days          = 30
         storage_class = "STANDARD_IA"
       }
       transition {
         days          = 90
         storage_class = "GLACIER"
       }
       expiration { days = 365 }
     }
   }
   ```
   Equivalent tiering exists as Azure Blob lifecycle management policies
   (Hot → Cool → Cold → Archive) and GCP Cloud Storage Object Lifecycle
   Management (Standard → Nearline → Coldline → Archive). Confirm the
   **minimum storage duration and early-deletion/retrieval fees** for
   each tier before committing data to it — archive tiers commonly carry
   both a minimum retention period charge and a retrieval delay measured
   in hours, not seconds.

4. **Separate lifecycle tiering from retention/deletion policy.**
   Tiering changes *where* data is stored to reduce cost; it should not
   be conflated with *whether* data should still exist. Any `expiration`
   rule that deletes data must be reviewed against actual compliance/
   backup retention requirements — see
   `disaster-recovery-and-backup-strategy` for retention policy design.

5. **Enable versioning and object lock / immutability for anything that
   must survive accidental overwrite or deletion** — S3 Versioning +
   Object Lock (compliance or governance mode), Azure Blob immutability
   policies, or GCP Bucket Lock — particularly for backup targets,
   audit logs, and anything subject to a regulatory retention
   requirement (WORM).

6. **Monitor cost and access patterns continuously.** Use S3 Storage
   Lens / Azure Storage insights / GCP Storage Insights (or the
   organization's FinOps tooling — see `cloud-cost-finops-optimization`)
   to catch data that was tiered to archive but is now being retrieved
   frequently (a sign the lifecycle policy needs adjusting the other
   direction) or data sitting in an expensive hot tier that hasn't been
   accessed in months.

7. **Test retrieval before relying on an archive tier operationally.**
   Confirm actual retrieval latency (e.g. AWS Glacier Flexible Retrieval
   standard tier is hours, not the milliseconds of S3 Standard) meets
   the business requirement before moving data that might be needed
   urgently into a cold tier.

## Best practices

- **Default to encrypted, private, versioned** for any new object
  storage bucket/container — make the secure configuration the
  templated default (via the landing-zone module), not an opt-in step
  each team remembers separately.
- **Use uniform/account-level public-access blocking** in addition to
  per-resource settings — defense in depth against one misconfigured
  bucket policy.
- **Prefer customer-managed keys (CMEK) only where genuinely required**
  (compliance scope, cross-account key control) — they add real
  operational burden (rotation schedules, key access policy management)
  that isn't worth it for every bucket.
- **Right-size block storage IOPS/throughput to the workload**, not the
  largest available tier "to be safe" — over-provisioned IOPS is a
  common, invisible cost leak that FinOps rightsizing (see
  `cloud-cost-finops-optimization`) should catch.
- **Treat file storage (EFS/Azure Files/Filestore) as the exception, not
  the default**, for new cloud-native workloads — it exists mainly for
  shared-filesystem compatibility with legacy applications; new
  workloads should generally be designed around object storage or a
  managed database instead.
- **Model lifecycle transitions against real retrieval-fee and
  minimum-duration terms** — moving data to archive tiers too
  aggressively can make the total cost (storage + early-deletion fee +
  retrieval fee) higher than leaving it in a warmer tier, if it turns
  out to be accessed sooner than expected.

## Common pitfalls

- **Symptom:** A storage bucket/container is found publicly accessible
  during a security review, months after creation.
  **Fix:** Public-access blocking was set per-resource but not enforced
  at the account/subscription/project level, and a later change (a
  well-meaning but overly broad bucket policy, or a CORS misconfiguration)
  silently reopened access. Enforce public-access prevention at the
  account/landing-zone level (see the `*-landing-zone-setup` skills) so
  no single resource-level change can reopen it, and add continuous
  scanning (AWS Config rule `s3-bucket-public-read-prohibited`, Azure
  Policy, GCP Security Command Center finding) rather than a one-time
  check.

- **Symptom:** A cost review finds a large volume of data in an archive/
  cold storage tier with a surprisingly high bill, higher than when it
  was in the standard tier.
  **Fix:** Data is being retrieved far more often than the tier's access
  pattern assumption, incurring per-retrieval fees and, in some cases,
  early-deletion charges from data that hadn't met the tier's minimum
  storage duration before being moved again. Re-tier based on actual
  access logs (Storage Lens / Storage insights), not a one-time
  assumption, and consider an intermediate tier (Infrequent Access/Cool/
  Nearline) instead of jumping straight to archive/deep-archive tiers.

- **Symptom:** An application unexpectedly loses the ability to read
  data it needs same-day, after a "cost optimization" lifecycle policy
  rollout.
  **Fix:** The lifecycle rule moved data to an archive tier with
  hours-long retrieval latency without validating the application's
  actual latency requirement. Before applying archive-tier transitions,
  confirm the data's access-time SLA with the owning team, and stage the
  lifecycle rule on a subset of data first.

- **Symptom:** An engineer runs a cleanup script that deletes what
  appears to be an old, unused storage bucket/account, and a downstream
  reporting job breaks weeks later.
  **Fix:** **Never delete a storage bucket/container/account (or run
  `aws s3 rb --force`, `az storage account delete`, or
  `gsutil rm -r` against a bucket) based on "looks unused" without
  confirming no lifecycle policy, replication rule, backup job, or IAM
  policy references it, and without a recoverable grace period** — soft
  delete or a staged rename-then-delete-later process is much safer than
  irreversible deletion. Cross-check dependencies (see
  `multi-cloud-networking-patterns` for shared-network implications and
  `disaster-recovery-and-backup-strategy` for backup-target
  implications) before any destructive storage action.

## Worked example

**Scenario:** A data-platform team stores 50 TB of application logs in
AWS S3 Standard, at rest for 18 months, most of it never queried after
the first 30 days, and the FinOps review flags it as the largest single
storage cost line item.

1. Query S3 Storage Lens / CloudTrail data-event logs to confirm actual
   access pattern: 95%+ of objects older than 30 days have zero GET
   requests; the remaining 5% (recent incident-investigation lookups)
   are accessed within the first 90 days only.
2. Design a lifecycle policy: Standard for 0-30 days, Standard-IA for
   30-90 days, Glacier Flexible Retrieval for 90-365 days, expire
   (delete) after 365 days — cross-checked against the company's
   18-month-to-1-year log retention compliance requirement, adjusting
   the expiration to align with the actual required retention (not
   shorter than compliance mandates).
3. Enable S3 Block Public Access at the account level and confirm
   default SSE-KMS encryption is applied bucket-wide, since the audit
   also flagged that the bucket previously had no explicit encryption
   configuration (relying on account defaults that changed over time).
4. Roll out the lifecycle policy to a 10% sample of prefixes first,
   monitor for a week to confirm no unexpected retrieval-fee spike from
   the incident-investigation access pattern colliding with the Glacier
   tier's retrieval latency, then apply to the remaining prefixes.
5. Result: storage cost for this bucket drops materially (moving the
   bulk of aged data out of Standard tier) while the 90-day
   investigation-lookback window remains in a tier with acceptable
   retrieval latency, and encryption/public-access gaps found during the
   review are closed as part of the same change.

## Cross-references

- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
- [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md)
- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)
