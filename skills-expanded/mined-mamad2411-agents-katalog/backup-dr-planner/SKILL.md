---
name: backup-dr-planner
description: "Designs backup and disaster-recovery strategy: RPO/RTO targets, backup types, 3-2-1 rule, encryption, retention, and tested restore drills. Use when defining DR plans, setting up backups, or validating recoverability."
---

# Backup & DR Planner

## Overview

Design, document, and validate a backup and disaster-recovery (DR) strategy before any incident forces the question. This skill drives you through the full lifecycle: setting measurable RPO and RTO targets per system, choosing the right backup type and cadence, enforcing the 3-2-1 storage rule, configuring encryption and retention, and — most critically — running real restore tests and DR drills that prove the strategy works. A backup plan that has never been exercised is a false promise.

**Core principle:** Define RPO and RTO first. Everything else — tooling, cadence, storage tier — follows from those two numbers.

## The Iron Law

```
AN UNTESTED BACKUP IS NOT A BACKUP.
DEFINE RPO AND RTO BEFORE CHOOSING ANY TOOLING.
```

You do not have a backup strategy until a restore has succeeded in a timed drill. You do not have a DR plan until a failover has been rehearsed end-to-end against documented runbooks.

## When to Use

**Use this when:**
- Setting up backups for a new system, database, or storage layer
- Auditing or overhauling an existing backup/DR posture
- Preparing for SOC 2, ISO 27001, or any audit requiring demonstrated recoverability
- Recovering from or post-mortem-ing a data-loss or outage event
- Onboarding a new cloud region or account that needs DR coverage

**Use this ESPECIALLY when:**
- Someone says "we have backups" but no one has tested a restore recently
- The team is under pressure to ship and proposes skipping DR setup "for now"
- A new database engine, object store, or SaaS dependency is added to the stack
- RPO/RTO are defined only informally ("we back up nightly, that should be fine")

**Don't skip when:**
- The system seems small — small systems get forgotten and are hardest to recover cold
- Time is tight — an untested backup discovered during an incident costs 10× more time than this skill

## Phase 1: Establish RPO and RTO Targets Per System

**BEFORE touching any tooling:**

1. **Enumerate every system that holds state** — databases (primary + replicas), object storage, message queues, secrets vaults, configuration stores, external SaaS data.

2. **For each system, define two numbers:**
   - **RPO (Recovery Point Objective)** — maximum acceptable data loss, measured in time. "We can lose up to 4 hours of orders" is an RPO of 4 h.
   - **RTO (Recovery Time Objective)** — maximum acceptable downtime before the system must be serving traffic again.

3. **Assign each system to a recovery tier** using the table below. Tier drives every subsequent decision.

| Tier | RPO | RTO | Typical systems |
|------|-----|-----|-----------------|
| **Tier 0 — Mission critical** | < 1 min | < 15 min | Payment processing, auth, primary OLTP DB |
| **Tier 1 — Business critical** | < 1 h | < 4 h | Analytics DB, order history, CMS content |
| **Tier 2 — Important** | < 24 h | < 24 h | Internal dashboards, audit logs, ML feature store |
| **Tier 3 — Best-effort** | < 7 days | < 72 h | Dev/staging data, archived reports, cold backups |

4. **Get stakeholder sign-off on targets** — RPO/RTO are business decisions, not engineering ones. Confirm in writing before proceeding.

**Output:** A signed-off RPO/RTO register (one row per system, tier assigned).

## Phase 2: Design Backup Strategy Per Tier

Map each tier to a concrete backup approach:

1. **Choose backup type per system:**

   | Type | When to use | Tool examples |
   |------|-------------|---------------|
   | **Full snapshot** | Small datasets, Tier 2–3, simple restore path | pg_dump, mysqldump, AWS RDS snapshot |
   | **Incremental / WAL streaming** | Large databases, Tier 0–1, low RPO | pgBackRest, Barman, MySQL binlog |
   | **PITR (Point-in-Time Recovery)** | Tier 0–1, sub-hour RPO, need surgical replay | Postgres WAL + base backup, Aurora PITR |
   | **Continuous replication** | Tier 0, near-zero RPO | Multi-region read replicas, CockroachDB, DynamoDB Global Tables |
   | **Object/file snapshot** | Object storage, NFS, blob stores | S3 versioning + lifecycle, restic, Velero for k8s |

2. **Set cadence** — derived from RPO, not from convenience:
   - RPO < 1 h → continuous WAL shipping or replication; snapshots every 1–6 h max
   - RPO < 24 h → daily full + incremental every 1–4 h
   - RPO < 7 days → daily full; weekly off-site copy

3. **Apply the 3-2-1 rule — no exceptions for Tier 0–2:**
   ```
   3 copies of the data
   2 different storage media/services
   1 copy stored off-site (different region or provider)
   ```

4. **Enforce encryption end-to-end:**
   - Backups encrypted at rest (AES-256 minimum) with keys stored separately from data
   - Keys rotated on the same schedule as the backup retention window
   - TLS in transit for any remote backup transfer

5. **Define retention per tier:**
   - Tier 0: 30-day rolling + monthly archives for 1 year
   - Tier 1: 14-day rolling + weekly for 90 days
   - Tier 2: 7-day rolling + monthly for 6 months
   - Tier 3: weekly for 30 days

**Output:** A backup design table: system → type → cadence → storage locations → encryption → retention.

## Phase 3: Write DR Runbooks

For each Tier 0 and Tier 1 system, write a step-by-step runbook that anyone on the on-call rotation can execute at 3 AM:

1. **Runbook must include:**
   - Symptom checklist — how to confirm this system needs recovery (not just monitoring noise)
   - Decision tree — restore from backup vs. promote replica vs. failover to secondary region
   - Exact commands with environment variables called out explicitly
   - Expected duration at each step with a "something is wrong" threshold
   - Rollback path — what to do if the recovery itself fails
   - Escalation contacts with phone/Slack handles (not just email)

2. **Runbook location:** store in version control alongside infrastructure code; link from the service's `README.md` and your incident-response tool.

3. **Runbook sign-off:** a second engineer must read and verify each runbook before it is considered valid.

```markdown
## [Service Name] Restore Runbook

**Last tested:** YYYY-MM-DD by @engineer  
**RTO target:** X hours  
**RPO target:** Y hours  

### 1. Confirm outage (5 min)
- Check [monitoring link]: expect error rate > 5% for > 2 min
- Check [replica status]: confirm primary is unreachable, not just slow

### 2. Choose recovery path
- If replica is healthy → promote replica (go to step 3a)
- If replica is also down → restore from backup (go to step 3b)

### 3a. Promote replica
```bash
# Exact command here
```
Expected: promotion completes in < 90 s. If > 3 min, stop and call @escalation.

### 3b. Restore from backup
```bash
# Exact restore command with explicit env vars
BACKUP_DATE=YYYY-MM-DD \
RESTORE_TARGET=hostname \
./scripts/restore-db.sh
```
Expected duration: ~45 min for a 200 GB database. Monitor progress with `tail -f /var/log/restore.log`.
```

## Phase 4: Test Restores and Run DR Drills

**This phase is non-negotiable. The strategy is not complete until testing passes.**

1. **Restore test (run before going live, then on a fixed schedule):**
   - Restore each Tier 0–1 backup to a staging environment
   - Verify data integrity: row counts, checksums, or application-level smoke tests
   - Measure actual restore duration against RTO target
   - Document pass/fail with timestamp and engineer name
   - Tier 0–1: test monthly minimum; Tier 2: quarterly

2. **DR drill (full failover exercise):**
   - Simulate the failure scenario (cut network, stop the primary, corrupt a volume)
   - Execute the runbook as written — no improvising
   - Measure time-to-recovery against RTO
   - Record every deviation from the runbook as a finding
   - Update the runbook immediately after the drill; re-test any step that required improvisation

3. **Automated restore verification (for continuous confidence):**

   ```bash
   # Example: nightly restore-verify job (adapt to your stack)
   #!/bin/bash
   set -euo pipefail
   BACKUP_FILE=$(aws s3 ls s3://backups/db/ | sort | tail -n 1 | awk '{print $4}')
   aws s3 cp "s3://backups/db/${BACKUP_FILE}" /tmp/restore-test.dump
   pg_restore --dbname=restore_verify /tmp/restore-test.dump
   psql restore_verify -c "SELECT COUNT(*) FROM orders;" > /tmp/row_count.txt
   # Compare to expected baseline; alert if delta > threshold
   ```

4. **Track all test results** in a DR test log with columns: date, system, backup age tested, restore duration, integrity check result, gap vs. RTO, action items.

## Phase 5: Operationalize and Monitor

1. **Alert on backup job failures** — silence is not success; a missed backup that generates no alert is as dangerous as no backup.
2. **Alert on backup age** — if the most recent backup is older than 1.5× the expected cadence, page on-call.
3. **Review the DR register quarterly** — systems change; RPO/RTO targets that made sense at launch may be wrong after a product pivot.
4. **Rotate and audit encryption keys** on schedule; confirm backup decryption succeeds after each rotation.
5. **Include backup/DR status in change management** — any infrastructure change that could affect recoverability must note the impact on backup strategy.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "We have automated backups, so we're covered" — without a tested restore, you are not covered
- "We'll set up DR after launch" — DR retrofit is 5× harder than DR by design
- "Our cloud provider handles backups" — provider backups have their own RPO limits and do not replace your own strategy
- "The replica is the backup" — replicas propagate corruption and deletions instantly; they are not backups
- "Testing restores would take too long" — an untested restore during an incident takes longer and fails more often
- "RPO/RTO are ops concerns, not engineering" — engineers choose the tools; they must know the targets

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "When did we last test this?" — restore tests are not documented or not running
- "How long would it actually take to recover?" — RTO has never been measured against a real restore
- "What's our RPO again?" — targets were never defined or are not written down
- "Did we back up [service X]?" — inventory is incomplete; return to Phase 1
- "The runbook doesn't work" — runbook was written but never drilled; return to Phase 3–4

**When you see these:** STOP. Return to Phase 1 and verify the RPO/RTO register is current.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We use managed cloud services, backups are automatic" | Managed backups have retention limits and do not cover user error or ransomware; you still own the strategy. |
| "We've never had a data loss incident" | Survivorship bias. The first incident without a tested plan is catastrophic. |
| "Restore testing is expensive and risky" | A restore drill in staging costs a few hours. An untested restore in production costs days and careers. |
| "The team knows how to recover this" | Tribal knowledge evaporates at 3 AM under incident pressure. Written, drilled runbooks do not. |
| "We'll add DR to the next sprint" | DR is always deprioritized until it isn't. Define RPO/RTO now; the rest follows. |
| "Encryption slows backups down" | Modern AES-NI hardware makes encryption overhead negligible. Unencrypted backups are a compliance and breach liability. |

## Related Skills

- **cloud-security-auditor** — use to verify backup storage permissions, IAM policies, and encryption key management alongside the DR posture
- **data-retention-manager** — use to align backup retention windows with legal hold, GDPR, and data-classification policies
- **chaos-engineer** — use to run controlled failure injection that exercises DR runbooks under realistic conditions
- **soc2-audit-prep** — use when backup/DR evidence (restore logs, drill records, RPO/RTO documentation) must be packaged for an auditor
- **devops-release-engineer** — use to wire backup-job failures and backup-age alerts into the release pipeline and on-call rotation

## Verification

Before marking this skill complete:

- [ ] RPO and RTO defined for every stateful system (not just databases)
- [ ] Every system assigned to a recovery tier (0–3) with stakeholder sign-off
- [ ] Backup type and cadence chosen based on RPO target, not convenience
- [ ] 3-2-1 rule satisfied for all Tier 0–2 systems (3 copies, 2 media, 1 off-site)
- [ ] Encryption at rest confirmed with keys stored separately from data
- [ ] Retention policy set per tier and enforced (not just configured)
- [ ] DR runbook written for every Tier 0 and Tier 1 system
- [ ] Runbook reviewed and signed off by a second engineer
- [ ] At least one full restore tested in staging and duration recorded
- [ ] Restore duration is within RTO target (or RTO has been revised upward with sign-off)
- [ ] Automated restore verification or scheduled restore test cadence is in place
- [ ] DR drill completed with findings logged and runbook updated
- [ ] Backup job failure alerts are active and tested
- [ ] Backup age alerts are active (trigger at 1.5× expected cadence)
- [ ] DR register review scheduled quarterly in the team calendar
