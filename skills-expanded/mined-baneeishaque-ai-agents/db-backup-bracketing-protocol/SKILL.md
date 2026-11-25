---
name: db-backup-bracketing-protocol
description: Defines when and how to dispatch a database backup GitHub Actions workflow as a safety bracket around destructive production operations.
category: Database
---

# Database Backup Bracketing Protocol Skill

> **Skill ID:** `db-backup-bracketing-protocol`<br>
> **Version:** 1.0.0<br>
> **Type:** Composer over [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md)

## Description

Define WHEN and HOW to dispatch a database-backup GitHub Actions
workflow as a **safety bracket** around destructive production
operations (UPDATE / DELETE / ALTER / trigger install / TRUNCATE).

Brackets come in three patterns — pre+post, post-only, or none — chosen
per §Decision: Bracket Pattern below. The actual `gh workflow run` +
`gh run watch` mechanics delegate to
[`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md).

## When to Apply

- About to execute any DML/DDL on production that mutates rows OR
  schema OR triggers/views/procs.
- About to authorize a [`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md)
  destructive step (Phase 3 UPDATE, Phase 5 ALTER, Phase 6 trigger install).

Do NOT apply when:
- Read-only probing (any [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) script).
- Dry-run within a `START TRANSACTION ... ROLLBACK` harness (never commits).
- Local / staging DB operations not connected to the backup workflow.

## Decision: Bracket Pattern

| Op risk | Pattern | Rationale |
|---|---|---|
| Reversible UPDATE on ≤100 rows, single column | **post-only** | Pre-existing backup probably ≤ 24 h old; post-snapshot is the recovery point. |
| Bulk UPDATE / DELETE > 100 rows | **pre + post** | Pre-snapshot bounds the worst-case revert; post-snapshot captures new-known-good state. |
| ALTER TABLE (add FK / add column / drop column) | **pre + post** | Schema rollback requires more than DML revert; pre-snapshot is mandatory. |
| Trigger / view / proc install or drop | **post-only** | Easily re-installable from source; post-snapshot proves working state. |
| TRUNCATE / DROP TABLE | **pre + post** | Pre-snapshot is the ONLY recovery; post confirms intentional state. |
| Routine maintenance (ANALYZE / OPTIMIZE) | **none** | No data mutation. |

## Procedure

### Step 1 — Pre-bracket (when pattern is pre+post)

Dispatch backup BEFORE the destructive op:

```bash
gh -R <owner>/<repo> workflow run database-backup.yml
sleep 5
RUN_ID=$(gh -R <owner>/<repo> run list --workflow=database-backup.yml --limit 1 --json databaseId -q '.[0].databaseId')
gh -R <owner>/<repo> run watch "$RUN_ID"
```

Or delegate to the dispatch skill's helper:

```bash
python3 .agents/skills/github-actions-workflow-dispatch/scripts/dispatch-and-wait.py \
    --repo <owner>/<repo> --workflow database-backup.yml --wait
```

### Step 2 — Capture pre-bracket evidence

After the run completes, record:
- Run ID
- Backup commit SHA (the workflow's resulting commit in the backup repo)
- UTC + local timestamp from the commit title

These three items form the **recovery anchor** if the destructive op
misfires.

### Step 3 — Execute the destructive op

Run the DML / DDL. On any error, ABORT and use the pre-bracket as the
restore point.

### Step 4 — Post-bracket

Dispatch backup AGAIN, capture the same three items. Two evidence
points = two-snapshot guarantee.

### Step 5 — Record both anchors in the work log

For audit / forensic recovery, the destructive op's log entry MUST list
both backup commit SHAs (pre and post). At minimum:

```text
2026-05-29 22:14 IST  UPDATE accounts SET parent_account_id=NULL WHERE parent_account_id=0
  pre-backup:  bf58cb3  2026-05-29 22:10 IST
  post-backup: 067d661  2026-05-29 22:18 IST
  affected:    72 rows
```

## Timing & Cost

| Step | Latency | Cost |
|---|---|---|
| `gh workflow run` dispatch | < 1 s | $0 |
| Backup job (mysqldump + commit) | 30–60 s typical | free CI minutes (public repo) |
| `gh run watch` until completion | 30–60 s | $0 |
| **End-to-end pre-bracket** | **~1 min** | $0 |

For a chart-of-accounts workload, pre+post bracketing adds ~2 min total
per destructive op — trivial cost relative to recovery time if the op misfires.

## Backup Workflow Self-Audit

Before relying on the bracket, verify the backup workflow itself works:

1. The workflow MUST commit the dump (or push to LFS) — not just produce an artifact.
2. The commit title MUST embed a timestamp captured at **job start**, not at
   mysqldump completion (else `commit_time` drifts from the actual dump time
   by the dump's duration — the longer the dump, the worse the lie).
3. Test by dispatching with no DB changes pending; confirm a new commit lands
   and the title reflects current time.

See the Account-Ledger-Server `database-backup.yml` `BACKUP_TIMESTAMP`
fix (commit `8610ec3`) as a reference.

## Pitfalls

| Pitfall | Mitigation |
|---|---|
| Pre-bracket dispatched but not waited on; destructive op ran during dump | Always `gh run watch` (or block on the dispatch skill's `--wait`). |
| Backup commit lands but actual dump file is empty / truncated | The backup workflow MUST verify dump size > N bytes before committing. |
| Post-bracket dispatched immediately; backup captures state BEFORE the destructive op's COMMIT replicated | Add a 5-10 s sleep between destructive COMMIT and post-bracket dispatch. |
| Daily scheduled backup ran 30 min before the destructive op; "pre-bracket" feels redundant | If the destructive op is risky, dispatch on-demand anyway — saves an hour of recovery on misfire. |
| Workflow uses dump-finish time in commit title → drift | See "Backup Workflow Self-Audit" above. |

## Related Skills

- [`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md) — primitive: dispatch + watch mechanics.
- [`github-actions-run-audit`](../github-actions-run-audit/SKILL.md) — primitive: retrieve completed run details.
- [`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md) — invokes this protocol around each Phase-3 / Phase-5 / Phase-6 destructive step.
- [`work-log-processing`](../work-log-processing/SKILL.md) — for recording pre/post anchor pairs in the session log.

## No scripts

This is a composer skill — mechanics delegate to
[`github-actions-workflow-dispatch`](../github-actions-workflow-dispatch/SKILL.md)
scripts. No new scripts are introduced.
