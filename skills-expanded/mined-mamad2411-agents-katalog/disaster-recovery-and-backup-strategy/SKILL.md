---
name: disaster-recovery-and-backup-strategy
description: >
  Guides designing backup and disaster-recovery strategy for cloud
  workloads — RTO/RPO-driven DR pattern selection (backup-restore, pilot
  light, warm standby, multi-site active-active), cross-region/cross-
  account backup replication, and DR runbook testing across AWS, Azure,
  and GCP. Use when a user asks to "design a disaster recovery plan",
  "set an RTO/RPO target", "back up a database/storage account/bucket
  cross-region", "test a DR failover", "protect against a region outage",
  or "recover from accidental deletion or ransomware."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: cloud
  maturity: stable
---

# Disaster Recovery and Backup Strategy

## Purpose

Backups that have never been restored, and DR plans that have never been
tested with a real failover, are aspirational documents, not operational
capabilities — the outage or ransomware event is the worst possible time
to discover a backup is corrupt, a runbook step references a
decommissioned system, or the cross-region replica has silent lag. This
skill covers picking a DR pattern (backup-restore through active-active)
matched to a genuine Recovery Time Objective (RTO) and Recovery Point
Objective (RPO) rather than the most expensive option by default,
implementing cross-region/cross-account backup replication that survives
the loss of the primary account itself, and — critically — testing
failover on a schedule so the plan is proven, not assumed.

## When to use

- Defining or revisiting RTO/RPO targets for a workload or the
  organization's tiered criticality model.
- Designing backup strategy for a database, storage account/bucket, or
  entire application stack, including cross-region and cross-account/
  subscription/project replication.
- Choosing a DR pattern: backup-restore, pilot light, warm standby, or
  multi-site active-active.
- Planning and running a DR failover test (tabletop or live).
- Responding to a real regional outage, ransomware/mass-deletion event,
  or a compliance requirement mandating documented, tested DR.
- Auditing existing backups for actual restorability (as opposed to
  "a backup job completed successfully").

## Prerequisites & environment

- A criticality tiering for workloads (e.g. Tier 0 = customer-facing
  revenue path, Tier 1 = internal but business-critical, Tier 2 =
  everything else) with an agreed RTO/RPO per tier, signed off by the
  business — not decided unilaterally by engineering, since DR pattern
  cost scales steeply as RTO/RPO approach zero.
- Native backup tooling access: AWS Backup (centralized, supports EBS,
  RDS, DynamoDB, EFS, S3), Azure Backup / Azure Site Recovery, or GCP
  Backup and DR Service, plus each data service's own
  point-in-time-recovery/snapshot feature (RDS automated backups, Azure
  SQL PITR, Cloud SQL automated backups).
- Cross-region (and ideally cross-account/subscription/project) write
  access for backup replication targets, following the isolation
  boundaries established in the landing-zone skills — a backup that
  lives only in the same account as the primary data does not protect
  against account-level compromise or accidental account deletion.
- A tested, version-controlled DR runbook (Infrastructure as Code for
  the DR-site infrastructure itself, plus documented manual steps for
  anything not yet automated) — a plan that exists only as institutional
  knowledge in one engineer's head is not a DR plan.
- Executive/business sign-off on the DR pattern's cost, since warm
  standby and active-active both roughly double (or more) infrastructure
  spend compared to backup-restore.

## Step-by-step guidance

1. **Set RTO/RPO per workload tier before choosing a pattern.** Example
   tiering:
   | Tier | RTO | RPO | Pattern |
   |------|-----|-----|---------|
   | 0 (revenue path) | < 15 min | < 5 min | Multi-site active-active or warm standby |
   | 1 (business-critical) | < 4 hours | < 1 hour | Warm standby or pilot light |
   | 2 (internal/batch) | < 24 hours | < 24 hours | Backup-restore |

2. **Match the DR pattern to the tier, not the other way around:**
   - **Backup-restore**: regular backups (snapshots, database exports)
     to a separate region/account; DR-region infrastructure is
     provisioned only when needed. Cheapest, slowest (hours to
     provision + restore).
   - **Pilot light**: core data stores (e.g. a replicated database)
     are always running in the DR region at minimal capacity; compute
     is provisioned and scaled up only during failover. Moderate cost,
     faster than backup-restore.
   - **Warm standby**: a scaled-down but fully functional copy of the
     stack runs continuously in the DR region; failover means scaling
     up and redirecting traffic. Higher cost, RTO measured in minutes.
   - **Multi-site active-active**: both regions serve production traffic
     simultaneously; failover is a traffic-routing change, not a
     resource provisioning event. Highest cost and engineering
     complexity (data consistency across active-active writes is a hard
     problem — don't adopt this pattern without a clear consistency
     model).

3. **Implement cross-region, cross-account backup replication.**
   Example — AWS Backup with a cross-account, cross-region copy:
   ```hcl
   resource "aws_backup_plan" "tier0" {
     name = "tier0-daily"

     rule {
       rule_name         = "daily-backup"
       target_vault_name = aws_backup_vault.primary.name
       schedule          = "cron(0 5 * * ? *)"

       copy_action {
         destination_vault_arn = "arn:aws:backup:eu-west-1:<DR_ACCOUNT_ID>:backup-vault:tier0-dr-vault"
         lifecycle {
           delete_after = 90
         }
       }
     }
   }
   ```
   Equivalent patterns: Azure Backup with a Recovery Services vault in a
   paired region plus cross-subscription vault access, or GCP Backup and
   DR Service / Cloud SQL cross-region replicas combined with
   cross-project backup storage. The DR-account/subscription/project
   backup copy should use a **separate IAM/RBAC trust boundary** from the
   primary so that a compromise of the primary account's credentials
   cannot also delete the DR copy.

4. **Automate DR-site infrastructure as code**, not as a manual runbook
   step performed only during an actual incident — the DR environment's
   Terraform/Bicep/Deployment Manager templates should be applied
   (or kept warm, per the chosen pattern) and validated in CI the same
   way production infrastructure is.

5. **Write the failover runbook as executable steps**, including: DNS/
   traffic-routing cutover (e.g. Route 53 / Azure Traffic Manager /
   Cloud DNS failover routing policies), data promotion (promoting a
   read replica to primary), application configuration changes, and
   the reverse (fail-back) procedure — fail-back is frequently
   forgotten and is often riskier than the initial failover.

6. **Test the failover on a schedule**, not only during a real incident:
   - Tabletop exercise (walk through the runbook without executing it)
     at minimum quarterly.
   - A live, controlled failover test (actually promoting the DR
     database, actually cutting DNS) at least annually for Tier 0/1
     workloads, during a planned maintenance window with rollback
     criteria defined in advance.
   - Restore-only tests (pull a backup and confirm it restores
     successfully and the data is intact) more frequently — monthly for
     Tier 0, since a corrupted or incomplete backup is only discovered
     at restore time, not at backup-job-success time.

7. **Protect backups against ransomware/mass-deletion specifically**:
   enable immutability (AWS Backup Vault Lock, Azure Backup immutable
   vaults, GCP Backup and DR immutable backup storage) so that even a
   fully compromised primary-account administrator credential cannot
   delete or shorten the retention of existing backup copies.

8. **Review and update RTO/RPO and the DR plan whenever the architecture
   changes** — a new dependency, a new database, or a new region added
   to production without a corresponding DR update silently degrades the
   plan's accuracy.

## Best practices

- **Store backups outside the blast radius of the primary account/
  subscription/project**, with a separate trust boundary, so a
  compromised or accidentally deleted primary account doesn't also take
  out its own backups.
- **Test restores, not just backup job success** — a green checkmark on
  a nightly backup job proves the job ran, not that the data is
  recoverable.
- **Enable backup immutability/vault lock for anything protecting
  against ransomware or insider threat**, since a mutable backup that an
  attacker (or a compromised automation credential) can delete provides
  no real protection.
- **Choose the DR pattern the business is actually willing to pay for**
  — do not default every workload to warm standby or active-active; most
  workloads genuinely belong in backup-restore or pilot light once RTO/
  RPO requirements are honestly assessed.
- **Automate DNS/traffic failover**, not manual DNS record edits during
  an incident — manual cutover under pressure is where failover time
  budgets are blown.
- **Document and rehearse fail-back**, not just failover — many
  organizations can execute a failover under pressure but have never
  practiced returning to the primary region cleanly.
- **Version and test DR infrastructure-as-code in CI** the same as
  production IaC — DR infrastructure that only gets applied during a
  real incident is untested infrastructure.

## Common pitfalls

- **Symptom:** During an actual regional outage, the DR failover takes
  many hours longer than the documented RTO.
  **Fix:** The runbook was written and reviewed but never executed
  live — steps referenced outdated resource names, a manual approval
  step wasn't accounted for, or DNS TTLs were set too high to cut over
  quickly. Run at least one live failover test per year for Tier 0/1
  workloads and update the runbook based on what actually happened, not
  what was planned.

- **Symptom:** A backup restore is attempted during an incident and the
  restored data is missing recent transactions or is outright corrupt.
  **Fix:** Backup jobs were reporting success, but nobody had performed
  an actual restore-and-verify test. Add scheduled restore-verification
  jobs (restore to a scratch environment, run an integrity/row-count
  check) as a standing practice, not a one-time validation.

- **Symptom:** Ransomware or a compromised automation credential deletes
  both the production data and its backups.
  **Fix:** Backups shared the same account/credentials/trust boundary as
  production, and were mutable (deletable by the same role that manages
  production). Enable backup vault immutability/lock and store DR
  copies under a separate account/subscription/project with a distinct,
  narrowly scoped IAM/RBAC role — see `cloud-iam-hardening` for how to
  scope that role tightly.

- **Symptom:** RTO/RPO targets exist on paper but every workload was
  assigned the same (usually the strictest) tier by default, and the
  resulting DR infrastructure cost is unsustainable.
  **Fix:** Tiering was never actually reviewed with business
  stakeholders workload-by-workload. Revisit tiering with the business
  owner for each workload, honestly assessing whether a multi-hour RTO
  is genuinely unacceptable before defaulting to the most expensive
  pattern.

- **Symptom:** An engineer, cleaning up "old" DR infrastructure to save
  cost, deletes the DR-region database replica or storage bucket
  entirely.
  **Fix:** **Never tear down DR-region infrastructure (a promoted-
  capable read replica, a cross-region backup vault/bucket) as a cost
  cleanup without explicit sign-off from whoever owns the DR plan for
  that workload** — confirm current RTO/RPO commitments still require it
  before any destructive action, and prefer scaling down (pilot
  light) over full deletion if cost is the concern. See
  `cloud-native-storage-strategy` for the equivalent caution on deleting
  storage resources generally.

## Worked example

**Scenario:** An e-commerce company's checkout service (Tier 0, target
RTO < 15 minutes, RPO < 5 minutes) runs entirely in one AWS region with
only default RDS automated backups (7-day retention, same region, same
account) — effectively no real disaster recovery.

1. Confirm the RTO/RPO with the business: checkout is genuinely revenue-
   critical; a 15-minute RTO and 5-minute RPO are validated as real
   requirements, not aspirational.
2. Given the tight RTO/RPO, select **warm standby**: run a scaled-down
   (e.g. 25% capacity) copy of the checkout stack continuously in a
   second region, with RDS configured for cross-region read replication
   and Route 53 failover routing pointed at both regions' load
   balancers with health checks.
3. Set up AWS Backup with a daily cross-account, cross-region copy
   (as shown in the Terraform snippet above) to a dedicated backup
   account, with Vault Lock enabled in compliance mode so backups cannot
   be deleted even by a compromised admin credential in the primary
   account — this protects against ransomware/mass-deletion in addition
   to the warm-standby replica, which protects against a regional
   outage.
4. Write the failover runbook: promote the DR-region RDS read replica to
   primary, scale the DR-region compute stack from 25% to 100% capacity,
   confirm Route 53 health checks have already begun routing traffic
   (automatic, since failover routing is DNS-health-check-driven rather
   than manual).
5. Schedule a live failover test during a planned low-traffic maintenance
   window: actually promote the replica, actually fail DNS over, measure
   real RTO/RPO achieved, and identify that the compute scale-up step
   took 9 minutes — inside budget, but close enough to warrant
   pre-warming an additional capacity buffer.
6. Document and rehearse fail-back: after the test, reverse the process
   deliberately (re-establish the original region as primary, resync
   data) rather than leaving the DR region as primary indefinitely by
   default.
7. Schedule monthly restore-verification jobs against the backup vault
   copy (independent of the warm-standby replica) so a corrupted backup
   would be caught long before it's ever needed as the last resort.

## Cross-references

- [cloud-native-storage-strategy](../cloud-native-storage-strategy/SKILL.md)
- [multi-cloud-networking-patterns](../multi-cloud-networking-patterns/SKILL.md)
- [cloud-iam-hardening](../cloud-iam-hardening/SKILL.md)
