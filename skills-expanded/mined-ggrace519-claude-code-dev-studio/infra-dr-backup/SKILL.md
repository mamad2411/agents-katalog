---
name: infra-dr-backup
description: Disaster recovery, backup strategy, RPO / RTO targets, cross-region failover, and restore drills. Auto-invoked when designing DR posture, reviewing backup coverage, or running recovery game-days.
---

# Infra DR/Backup

"We have backups" is not a DR posture. Untested backups are Schrödinger's
backups — they exist and don't exist until you try to restore. What counts is
restore time under pressure, with evidence.

## When to reach for this

- Setting or reviewing RPO/RTO targets and the DR topology that meets them
- Auditing backup coverage — what's enrolled, what drifted out, what was never in
- Designing or running a restore drill / DR game-day
- Hardening backups against ransomware (immutability, isolation)

## Principles

1. **Tier by business impact, not uniform policy.** Assign every service a tier
   — T0 (critical), T1 (important), T2 (best-effort) — each with its own RPO/RTO
   and a written business justification. A transactional DB and a log archive do
   not share a tier.
2. **Restore is the only test that counts.** Drill per tier on a schedule;
   capture wall-clock from decision-to-failover through service-restored. If the
   measured number exceeds the RTO, the RTO is fiction — fix one or the other.
3. **Immutable backups for ransomware.** Object lock / WORM on critical backup
   buckets, replicated cross-account under *separate* IAM. Attackers target
   backups first; the last line of defense must be unreachable with production
   credentials.
4. **Practice the full failover, not just DB promotion.** DNS/traffic switch,
   queue drain, cache warm-up, downstream reconnects, session failover. Every
   "we forgot that" in a drill is a "we forgot that" in the real outage.
5. **Document the break-glass path.** Who initiates DR, what MFA is required,
   where the runbook lives when the wiki is down. DR happens precisely when
   normal tooling is unavailable.
6. **Measure coverage continuously.** New services auto-enroll in backup;
   dashboard "enrolled vs. total", last-successful-backup age, and
   last-restore-drill age. Drift — the database added six months ago that nobody
   enrolled — is the most common DR failure mode.

## Tiering starting points

| Tier | RPO | RTO | Topology | Drill cadence |
|---|---|---|---|---|
| T0 (revenue/safety critical) | ≤ 5 min (PITR / continuous) | ≤ 1 h | warm-standby or active-active | quarterly, full failover |
| T1 (important, degradable) | ≤ 1 h | ≤ 4 h | pilot-light | semi-annual, partial restore |
| T2 (best-effort) | ≤ 24 h | ≤ 72 h | backup-and-restore | annual, tabletop + sample restore |

Topology cost rises steeply left-to-right (active-active ≈ 2× run cost;
backup-and-restore ≈ storage only) — tie each tier choice to the dollar cost of
the outage hour it prevents, and record it as an ADR.

## Backup coverage checklist

- [ ] Databases: point-in-time recovery enabled, retention ≥ RPO window
- [ ] Object storage: versioning + cross-region replication for T0/T1 buckets
- [ ] IaC state (Terraform state, etc.) and CI/CD config backed up
- [ ] Secrets/KMS: recovery path documented (keys are often the restore blocker)
- [ ] Container images replicated to a second registry/region
- [ ] Restore validation step defined per dataset (checksum, row counts, smoke test)
- [ ] Retention lifecycle policies set — backups age into cheaper storage classes, then expire

## Pitfalls

- Backups in the same account/region/credential boundary as production — one
  compromised key deletes both
- RTO measured from "restore started" instead of "decision made" — paging,
  approvals, and finding the runbook are usually the slow part
- Restoring data but not *access*: IAM, DNS, TLS certs, and secrets missing in
  the recovery region
- Drills always run by the same senior engineer — the drill must prove the
  runbook works, not that one person does
- Backup jobs that report success on empty or truncated dumps; validate
  content, not exit codes

---
*Related: `infra-sre` (SLO impact of RPO/RTO, incident practice), `infra-k8s`
(Velero / PV snapshots), `infra-finops` (standby + storage cost) · domain agent:
`infra-architect` · output/ADR format: `playbook-conventions`*
