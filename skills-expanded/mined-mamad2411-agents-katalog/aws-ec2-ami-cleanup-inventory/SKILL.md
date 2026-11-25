---
name: aws-ec2-ami-cleanup-inventory
description: Build a read-only AWS EC2, EBS volume, AMI, and EBS snapshot cleanup inventory across one or more profiles/accounts. Use when Amit asks which DEV/PROD EC2s, EBS volumes, AMIs, or snapshots can be cleaned up, which are protected, or asks for cleanup candidate tables before any termination, volume deletion, deregistration, snapshot deletion, or AMI retirement.
---

# AWS EC2 AMI EBS Cleanup Inventory

Use this skill before cleanup decisions for EC2, EBS volumes, AMIs, or EBS
snapshots.

## Default

Read-only inventory first. Do not stop, terminate, detach/delete EBS volumes,
deregister AMIs, delete snapshots, edit SSM pointers, change launch templates,
remove sharing, or mutate AWS.

Decision rule:

- inventory + review stays in this skill;
- cleanup execution must be delegated to the owning stack command or the
  `terraform-terragrunt-cleanup` skill.

## Use when

- Amit asks which EC2/EBS/AMI/snapshot resources can be cleaned
- DEV/PROD validation resources have expired TTLs
- AMI Factory, Image Builder, scan, validation, canary, debug, or review
  resources need sorting into cleanup/retain buckets
- a cleanup goal needs evidence before approval

## Read first

- repo `AGENTS.md`
- repo `SPEC.md` if present
- `/home/dev/.codex/AWS.md`
- owning repo lifecycle rules when available, for example AMI Factory `SPEC.md`

## Evidence root

Use:

```text
~/.AGENTS-temp/<repo>/ec2-ami-cleanup-inventory/<YYYYMMDD-HHMMSS>/
```

Save raw AWS JSON under `raw/<profile>/`.

## Minimum inventory

For each account/profile/region:

- `sts get-caller-identity`
- `ec2 describe-instances`
- `ssm describe-instance-information`
- `ec2 describe-volumes`
- `ec2 describe-images --owners self`
- `ec2 describe-snapshots --owner-ids self`

When cleanup may affect AMIs or EBS, also check before recommending delete:

- SSM parameter pointers relevant to the repo/lane
- EC2 references to AMI IDs
- EBS volumes attached to instances
- unattached EBS volumes and their create time, tags, and delete-on-termination
- launch template latest/default references
- AMI-to-snapshot block device mappings
- snapshot references from AMIs
- AMI sharing and snapshot permissions when cross-account use is possible

## Classification

Use these buckets:

- `scan-ready`: running, private-only, SSM Online, ready for requested Ops scan
- `cleanup-after-scan`: temporary scan/validation host with `keep_until_scan`
- `cleanup-candidate`: expired TTL or explicit cleanup tag, no obvious protection
- `needs-owner-confirmation`: stopped/old/data/security/jumpbox or unclear owner
- `retain-protected`: current workload, current/previous pointer, rollback, data,
  attached EBS volume, launch template, shared PROD path, or unclear critical
  dependency
- `retain-shared-iam`: shared IAM roles/policies used by zero-cost shared
  validation paths, fallback roles, or cross-account callers

Do not call something safe to delete only because TTL expired.
Retain shared IAM roles/policies by default unless the request includes explicit
approval to delete them and ownership confirmation.

## Output

Write `RESULT.md` with:

- profiles/accounts/regions checked
- EC2 review table for each environment checked
- EBS volume table
- AMI table
- snapshot table
- `tf-tg-stack` and/or repo-owned command mapping for each cleanup class (when
  known)
- rough, non-management-grade cost/savings note (for example deleted hourly cost
  or snapshot storage reduction)
- cleanup candidates with confidence and reason
- retain/protected resources and reason
- missing checks/blockers
- exact approval needed for any cleanup

For EC2 tables, make the review easy:

- show DEV and PROD separately when both are checked
- put likely cleanup candidates first
- hide or collapse obvious long-term PROD workloads into a short
  `retain-protected` table
- do not mix durable PROD workloads with temporary validation/debug resources
- include columns:
  - decision
  - account/env
  - instance id
  - state
  - private IP
  - Name
  - AMI
  - tf/tg owner
  - TTL
  - cleanup/lifecycle tag
  - reason
- optional rough `cost impact` column when quick estimate is available

Keep chat summary short and point to `RESULT.md`.

## Recommended handoff

When cleanup is approved:

1. If resources are Terraform/Terragrunt-managed:
   - call `terraform-terragrunt-cleanup` with the owning stack path(s) and
     approved resource IDs.
2. If cleanup is AMI Factory-only EC2/EBS/AMI/snapshot and the owning repo exposes
   a cleanup command (not raw AWS CLI), hand to that command with the approved list.
3. Keep shared IAM roles/policies as `retain` unless an explicit exception is added
   to the approval note.

## Safety

- read-only until Amit approves exact cleanup
- EC2 termination, EBS volume deletion, AMI deregistration, and snapshot deletion
  are separate approvals unless a goal explicitly bundles exact resources
- no AWS SSO login
- no secrets in output
- no public exposure changes
- if account/profile/env is unclear, stop and record blocker
