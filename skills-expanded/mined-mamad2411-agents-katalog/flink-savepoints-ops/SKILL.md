---
name: flink-savepoints-ops
description: >
  Operate Apache Flink savepoints for upgrades, rescaling, and controlled restarts:
  trigger, catalog, restore, compatibility across job graph changes, and cleanup.
  Use for owned Flink jobs when performing stateful upgrades or disaster recovery drills
  without losing operator state.
---

# Flink Savepoints Ops

## Scope And Authorization

- **In scope:** Flink jobs and savepoint storage you operate.
- **Out of scope:** restoring foreign jobs from unauthorized state copies.
- Savepoints can contain sensitive state—apply same controls as checkpoints.
- Prefer staging drills before production stop-with-savepoint.
- Pair automation with `code-quality-standards`.

## When To Use

- **Version upgrades** of Flink or job jars with state continuity.
- Changing parallelism (rescale) from a savepoint.
- Planned maintenance stop/start with consistency.
- Distinguishing savepoints (operator-owned) from automatic checkpoints.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Checkpoint storage security | `flink-checkpoint-security` |
| CDC connector setup | `flink-cdc-connectors` |
| General backup program | org backup skills / catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Op | Command / API (typical) |
| --- | --- |
| Trigger | `flink savepoint <jobId> [targetDir]` or stop-with-savepoint |
| Restore | `flink run -s <savepointPath> ...` / K8s operator restore path |
| Dispose | `flink savepoint -d <path>` when supported |
| List | JobManager UI / object store listing |

| Compatibility | Notes |
| --- | --- |
| Operator UIDs | Stable UIDs required for state mapping |
| Serializer changes | May need state migration / schema evolution |
| Max parallelism | Cannot always shrink below key-group constraints without care |

## Workflow

### 1. Confirm scope and success criteria

1. Job id, jar version current/target, parallelism, state backend, savepoint dir.
2. Success: savepoint completed; new job restored; golden traffic checks pass; old savepoint retained until validation window ends.
3. Rollback plan: keep previous jar + last good savepoint.

### 2. Pre-checks

```bash
flink list
flink info /path/to/job.jar   # if available in your distro
```

1. Confirm all stateful operators have **explicit UIDs** in code.
2. Confirm savepoint directory writable and secured (`flink-checkpoint-security`).
3. Drain or accept in-flight expectations with downstream consumers.

### 3. Trigger savepoint

```bash
# Cancel with savepoint (preferred for clean stop) — exact flags depend on version
flink stop --savepointPath s3://flink-state-prod/savepoints/jobA/ ${JOB_ID}
# Or trigger without cancel
flink savepoint ${JOB_ID} s3://flink-state-prod/savepoints/jobA/
```

1. Record returned savepoint path exactly.
2. Verify object store contains `_metadata` / expected files.
3. Tag path with job version, time, ticket id in runbook.

### 4. Upgrade / change graph safely

1. Deploy new jar only after reviewing operator UID stability.
2. If removing operators, understand unused state discard options (allowNonRestoredState) **explicitly**—do not enable casually.
3. Align Flink minor version upgrade notes for state compatibility.

### 5. Restore

```bash
flink run \
  -s s3://flink-state-prod/savepoints/jobA/savepoint-XXXX \
  -d /path/to/new-job.jar \
  --parallelism 8
```

1. Watch restore time and checkpoint success after start.
2. Validate business metrics (lag, row counts, idempotent sinks).

### 6. Verify with evidence

| Check | Pass criteria |
| --- | --- |
| Savepoint size/path | Logged and accessible only to ops roles |
| Job RUNNING | After restore |
| State continuity | No unexplained full reprocess (unless planned) |
| Downstream | No sustained duplicate storm / gap beyond design |

### 7. Cleanup and hand off

1. Retain N last good savepoints; delete abandoned after TTL.
2. Document command history and jar digests.
3. Dispose savepoints with official tools when retiring jobs.
4. Apply `code-quality-standards` for any automation scripts.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| UIDs | Explicit stable UIDs | Auto UIDs then “why state gone” |
| Stop | stop-with-savepoint | kill -9 TaskManagers |
| Path | Cataloged immutable path | “Whatever was in /tmp” |
| allowNonRestored | Rare, ticketed | Always on |
| Security | Same as checkpoint ACL | World-readable savepoints |
| Drill | Staging rehearsal | First try on Black Friday |

## Output Checklist

- [ ] Job, versions, parallelism recorded
- [ ] Operator UIDs verified in code
- [ ] Savepoint triggered and path stored
- [ ] Restore succeeded with validation metrics
- [ ] Rollback artifacts retained for window
- [ ] ACL/encryption of savepoint path confirmed
- [ ] Cleanup policy applied
- [ ] Runbook updated
- [ ] `code-quality-standards` applied

## Rules

- Owned jobs only; treat savepoint data as sensitive.
- Prefer rehearsed upgrades; never delete last good savepoint before validation.
- Coordinate storage security with `flink-checkpoint-security`.
- Exact CLI flags vary by Flink version—verify against your distro docs.
