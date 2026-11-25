---
name: orphaned-cloud-resource-cleanup
description: >
  Finds and safely removes orphaned cloud resources that accumulate
  silent cost — unattached EBS volumes/managed disks, unassociated
  Elastic IPs/Azure Public IPs, orphaned load balancers/target groups,
  and stale manual snapshots — with an explicit non-use confirmation
  procedure before any deletion. Use when a user asks to "find unused EBS
  volumes," "clean up unattached disks," "release unused Elastic IPs,"
  "find orphaned load balancers," or "reduce waste from leftover
  resources nobody is using." Covers AWS and Azure (and the GCP
  equivalents) hands-on deletion workflow, distinct from
  cloud-cost-finops-optimization's broader tagging/rightsizing/commitment
  program and cloud-cost-anomaly-investigation's spike triage.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Orphaned Cloud Resource Cleanup

## Purpose

Every cloud account accumulates a background hum of resources that
outlived the thing they were attached to: an EBS volume/managed disk
left behind after its instance was terminated, an Elastic IP/Public IP
reserved for a test that was never released, a load balancer or target
group pointing at a service that was decommissioned months ago, a manual
snapshot taken "just in case" before a change that was never cleaned up
afterward. None of these show up as a dramatic cost spike — each is
individually cheap — but collectively, across dozens of accounts and
years of accumulation, they become a steady, invisible tax. This skill
covers finding these specific classes of orphaned resource and removing
them safely, with the non-negotiable discipline that "looks unattached"
and "is confirmed unused" are not the same thing — a resource detached
from its original parent can still be an intentional backup, a
disaster-recovery artifact, or something a team meant to reattach next
sprint.

## When to use

- A recurring or one-off request to reduce cloud waste by cleaning up
  unattached storage, unused reserved IPs, or orphaned network resources.
- A cost review or [cloud-cost-anomaly-investigation](../cloud-cost-anomaly-investigation/SKILL.md)
  identifies a resource that appears unused and hands it off for
  confirmed, safe removal.
- Preparing an account/subscription for decommissioning and needing a
  complete sweep of everything left behind by long-terminated workloads.
- A cloud provider's own trusted-advisor/cost-recommendation tooling
  (AWS Trusted Advisor, Azure Advisor) flags idle resources and someone
  needs to action the list rather than let it sit.
- Setting up a *recurring* scheduled check for orphaned resources instead
  of a one-time manual sweep.

## Prerequisites & environment

- Read access to list resources and their attachment state: AWS CLI
  (`ec2`, `elb`/`elbv2`) or Trusted Advisor, Azure CLI (`az disk`,
  `az network public-ip`, `az network lb`) or Azure Advisor, `gcloud
  compute` for the GCP equivalents (persistent disks, static external IP
  addresses, forwarding rules/load balancers).
- Delete/release permissions scoped narrowly to the resource types being
  cleaned up — not a broad admin role — per
  [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md); a cleanup
  script should not be able to touch resources outside its stated scope.
- A tagging/labeling convention (`owner`, `environment`,
  `decommission-date`) to check before deleting anything — per
  [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md) —
  since tag absence is itself a reason for extra caution, not a green
  light to delete faster.
- Awareness of, and a check against, any active
  [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md)
  plan for the account/subscription — DR-pattern resources (a pilot-light
  database replica, a cross-region backup vault, a manually retained
  pre-migration snapshot) can look identical to genuine orphans from a
  pure "is it attached right now" query.
- A grace-period/quarantine mechanism (a tag, a holding folder/resource
  group, or a "stop, don't delete" first pass) rather than immediate
  hard deletion for the first pass of any new cleanup process.

## Step-by-step guidance

1. **Enumerate candidates by state, not by age alone.** Age is a weak
   signal on its own; attachment/association state is the primary
   filter.
   - **AWS unattached EBS volumes**:
     ```bash
     aws ec2 describe-volumes \
       --filters "Name=status,Values=available" \
       --query "Volumes[].{ID:VolumeId,Size:Size,Created:CreateTime,Tags:Tags}"
     ```
     (`available` = not attached to any instance; `in-use` volumes are
     excluded automatically by the filter.)
   - **Azure unattached managed disks**:
     ```bash
     az disk list --query "[?diskState=='Unattached'].{Name:name, Size:diskSizeGb, TimeCreated:timeCreated, Tags:tags}"
     ```
   - **AWS unassociated Elastic IPs**:
     ```bash
     aws ec2 describe-addresses \
       --query "Addresses[?AssociationId==null].{IP:PublicIp,AllocationId:AllocationId,Tags:Tags}"
     ```
   - **Azure unassociated Public IPs**:
     ```bash
     az network public-ip list --query "[?ipConfiguration==null].{Name:name, IP:ipAddress}"
     ```
   - **AWS orphaned/idle load balancers** (no healthy targets, or zero
     registered targets, over a sustained window):
     ```bash
     aws elbv2 describe-target-groups --query "TargetGroups[].TargetGroupArn" \
       | xargs -I{} aws elbv2 describe-target-health --target-group-arn {}
     # empty TargetHealthDescriptions for a sustained period = candidate
     ```
   - **Azure orphaned load balancers** (no backend pool members):
     ```bash
     az network lb list --query "[?backendAddressPools[0].backendIpConfigurations==null].name"
     ```
   - **Stale manual snapshots** (AWS EBS snapshots / Azure disk
     snapshots not tied to a backup policy, older than a defined
     threshold):
     ```bash
     aws ec2 describe-snapshots --owner-ids self \
       --query "Snapshots[?StartTime<='2026-04-01'].{ID:SnapshotId,VolumeId:VolumeId,Description:Description}"
     ```

2. **Cross-check every candidate against tags and DR/backup policy
   before treating it as a true orphan.** A resource with an `owner` tag
   still active, or one covered by
   [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md)'s
   backup vault/retention policy (e.g. a snapshot inside an AWS Backup
   Vault Lock retention window, or a disk explicitly retained as a
   pilot-light DR asset), is not a cleanup candidate regardless of
   attachment state. Filter these out of the candidate list before
   proceeding, don't just note them for later.

3. **Confirm true non-use with a second signal beyond attachment
   state**, not attachment state alone:
   - Check the resource's **creation/last-modified timestamp** against
     a reasonable minimum age (e.g. 14-30 days) — a volume detached
     yesterday during an in-progress migration is not the same as one
     detached for six months.
   - Check **CloudTrail/Activity Log/Cloud Audit Logs** for the
     resource ID to see who detached/created it and why, if the event is
     still within retention.
   - For Elastic IPs/Public IPs specifically, check whether it's
     referenced in any DNS record, firewall allow-list, or partner/
     customer-facing allowlist (a "detached" IP that a customer
     whitelisted is a functional dependency even with no cloud-side
     association).
   - For a snapshot, confirm no automation (a backup job, an AMI/image
     build pipeline) references it as a source before deleting — grep
     Infrastructure-as-code and AMI/image build configs for the
     snapshot/disk ID.

4. **Notify the owner (or last-known owner from tags/audit logs) with a
   grace period before deleting**, rather than deleting immediately on
   finding a candidate:
   ```bash
   # Example: tag as pending-deletion with a future date instead of deleting immediately
   aws ec2 create-tags --resources vol-0123456789abcdef0 \
     --tags Key=pending-deletion,Value=2026-08-11 Key=flagged-by,Value=cleanup-sweep-2026-07
   ```
   Equivalent on Azure: `az tag update` or a resource-group-level
   "quarantine" tag. Send the notification (email, Slack, a ticket) to
   the tagged/last-known owner, or to a general platform-team channel if
   no owner can be identified, with the deletion date and an easy way to
   object.

5. **Delete only after the grace period elapses with no objection**, and
   only the specific confirmed-orphaned resource — never as a bulk
   "delete everything matching the filter" pass without the per-resource
   confirmation from steps 2-3:
   ```bash
   # AWS: release an unassociated Elastic IP
   aws ec2 release-address --allocation-id <ALLOCATION_ID>
   # AWS: delete a confirmed-unattached EBS volume
   aws ec2 delete-volume --volume-id <VOLUME_ID>
   ```
   ```bash
   # Azure: release/delete an unassociated Public IP
   az network public-ip delete --name <PUBLIC_IP_NAME> --resource-group <RESOURCE_GROUP>
   # Azure: delete a confirmed-unattached managed disk
   az disk delete --name <DISK_NAME> --resource-group <RESOURCE_GROUP> --yes
   ```
   > **Warning:** These are destructive, typically irreversible actions
   > (a deleted EBS volume/managed disk cannot be recovered unless a
   > snapshot exists independently; a released Elastic IP/Public IP may
   > be reassigned to another customer entirely and is not guaranteed
   > recoverable). Never run a bulk delete loop directly off the
   > enumeration query in step 1 — always pass every candidate through
   > steps 2-4 first, and prefer taking a final safety snapshot of a
   > volume/disk immediately before deleting it if there is any residual
   > uncertainty.

6. **For load balancers/target groups with zero targets**, confirm the
   downstream DNS/service discovery record no longer points at it before
   deletion — an idle-looking load balancer can still be the intended
   target of a DNS record for a service currently scaled to zero rather
   than decommissioned (e.g. a batch/seasonal workload).

7. **Automate the enumeration + notify steps as a recurring scheduled
   job** (weekly/monthly), not a one-time manual sweep — orphaned
   resources accumulate continuously as workloads are terminated, so a
   one-time cleanup regresses within a quarter without a recurring
   check. Keep the deletion step itself either manual (a human clicks
   "confirm") or gated behind the same grace-period/notification logic
   even when automated.

8. **Track and report savings realized**, feeding it back into the
   FinOps showback view — a completed cleanup sweep is good input for
   [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md)'s
   reporting, and demonstrates the recurring check's value to
   stakeholders who might otherwise question the process overhead.

## Best practices

- **Attachment/association state is a necessary but not sufficient
  signal** — always corroborate with age, tags, audit-log history, and
  DR/backup policy before calling anything a confirmed orphan.
- **Always insert a tagged grace period between "identified as a
  candidate" and "deleted"** — a notify-then-wait step costs a few days
  and catches the cases where the resource wasn't actually orphaned.
- **Snapshot before delete when there's any residual doubt** — an extra
  final snapshot of a volume/disk is cheap insurance against an
  irreversible mistake, especially for anything that held data.
- **Never run cleanup as a single bulk command against a raw enumeration
  query** — always filter, confirm, notify, then act per-resource (or in
  small confirmed batches), so a scripting mistake can't delete an
  entire account's worth of storage in one pass.
- **Prefer scoped delete/release IAM permissions for the cleanup role
  itself** — a cleanup automation account should not hold broader
  permissions than exactly what it needs to enumerate, tag, and delete
  the specific resource types in scope.
- **Make the recurring sweep's findings visible before deleting anything
  automatically** — a dashboard or weekly digest of candidates builds
  trust in the process faster than silent automated deletion, even once
  the process is mature.
- **Treat a resource with no tags as higher risk, not lower** — an
  untagged resource is more likely to be a forgotten manual creation
  from years ago than a well-managed, safe-to-delete artifact; slow down
  and dig into audit-log history rather than treating tag absence as
  "nobody will miss it."

## Common pitfalls

- **Symptom:** A cleanup script deletes an unattached EBS volume that
  turns out to be a manually detached backup source a team relied on,
  and the data is unrecoverable.
  **Fix:** **Never auto-delete storage resources flagged as idle without
  a grace period, notification, and human confirmation** — this is
  destructive and often irreversible. Always run candidates through the
  tag/audit-log/DR-policy cross-check (steps 2-3) and the notify-then-
  wait grace period (step 4) before any deletion, especially for
  anything that held data.

- **Symptom:** A released Elastic IP/Public IP that "looked unused" was
  actually allowlisted by a customer's firewall or referenced in a
  partner integration's static-IP allowlist, and releasing it breaks
  that integration when the IP gets reassigned elsewhere.
  **Fix:** Cloud-side association state doesn't capture external
  dependencies. Before releasing any IP, check firewall rules, DNS
  records, and any documented partner/customer allowlist referencing
  it — treat a static IP as higher-risk to release than a volume, since
  the consequence of a mistake (address reassigned to an unrelated
  account) is harder to reverse than restoring from a snapshot.

- **Symptom:** A load balancer with zero currently-registered targets
  gets deleted, and it turns out to be the intended target of a
  scheduled/seasonal batch workload that scales up only once a quarter.
  **Fix:** Zero targets *right now* isn't the same as permanently
  unused. Check the load balancer's target-group history and any
  scheduled-scaling configuration over a longer window (at least one
  full scaling cycle) before concluding it's orphaned, and confirm with
  the owning team from its tags/naming convention.

- **Symptom:** A recurring cleanup sweep starts flagging (and someone
  eventually deletes) a cross-region backup snapshot or a pilot-light DR
  replica because it looks idle by the same criteria used for genuine
  orphans.
  **Fix:** DR-pattern resources are *supposed* to look idle under normal
  operating conditions — that's not the same as orphaned. Explicitly
  exclude resources tagged or known to be part of an active
  [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md)
  plan from the candidate list at step 2, and require sign-off from
  whoever owns the DR plan before touching anything that might be one.

- **Symptom:** The cleanup process finds hundreds of untagged candidates
  and, to move fast, someone deletes everything older than a threshold
  in one bulk pass.
  **Fix:** Volume of candidates is not a reason to skip per-resource
  confirmation — it's a reason to batch the *notification* step (a
  single digest listing all candidates with their grace-period deadline)
  while still deleting only after the individual grace period elapses
  unobjected, never as one undifferentiated bulk delete command.

## Worked example

**Scenario:** A monthly scheduled cleanup sweep runs against a
`checkout-nonprod` AWS account and finds 14 unattached EBS volumes, 3
unassociated Elastic IPs, and 1 load balancer with no registered targets.

1. Enumerate candidates (step 1): the `describe-volumes --filters
   Name=status,Values=available` query returns 14 volumes; cross-checked
   against `describe-addresses` and `describe-target-health`.
2. Cross-check tags and DR policy (step 2): 2 of the 14 volumes carry a
   `dr-role=pilot-light-replica-source` tag matching an entry in the
   account's DR runbook — excluded immediately, not just noted.
3. Confirm non-use signal (step 3): of the remaining 12 volumes, 9 have a
   `CreateTime`/detachment timestamp older than 60 days with no matching
   CloudTrail `DetachVolume` event tied to an active migration; 3 were
   detached only 4 days ago during an in-progress instance-type change
   still tracked in an open ticket — those 3 are excluded from this
   sweep and re-checked next month.
4. Tag and notify (step 4): the 9 confirmed candidates are tagged
   `pending-deletion=2026-08-11`, and a digest listing all 9 (volume ID,
   size, last-known owner tag or "untagged — flagging platform-team
   channel") is posted to the team channel with a two-week grace period.
5. One volume gets claimed within the grace period — an engineer
   recognizes it as a rollback safety net for a change happening the
   following week — and its `pending-deletion` tag is removed.
6. After the grace period, the remaining 8 volumes and the 3
   unassociated Elastic IPs (independently confirmed via DNS/allowlist
   check to have no external references) are deleted/released
   individually via scripted per-resource calls, not a single bulk
   command, with each deletion logged to the sweep's completion report.
7. The idle load balancer is checked against its target group's history
   over the trailing quarter (step 6): no scheduled scaling activity or
   recent target registration in 90 days, and its name matches a service
   decommissioned two releases ago per the deploy history — confirmed
   orphaned and deleted after the same notify/grace-period cycle.
8. Total savings (volume storage, IP reservation fees, load balancer
   hourly charge) are reported back into the account's FinOps showback
   dashboard for the month.

## Cross-references

- [cloud-cost-finops-optimization](../cloud-cost-finops-optimization/SKILL.md) —
  the broader tagging/rightsizing/commitment program this recurring
  cleanup feeds cost savings data back into.
- [cloud-cost-anomaly-investigation](../cloud-cost-anomaly-investigation/SKILL.md) —
  the source of many cleanup candidates when a spike investigation
  identifies a resource as unused rather than misconfigured.
- [disaster-recovery-and-backup-strategy](../disaster-recovery-and-backup-strategy/SKILL.md) —
  check before deleting anything that could be a DR-pattern asset
  (pilot-light replica, cross-region backup vault, retained pre-change
  snapshot) rather than a genuine orphan.
- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md) — scope the
  cleanup automation's delete/release permissions narrowly, per its
  least-privilege guidance.
