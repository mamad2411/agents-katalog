---
name: migration-plan
description: >-
  Plan a schema or data change that is safe to deploy and to undo: split it into expand / backfill /
  switch / contract steps that each work with old and new code running at once, write a rollback for
  every step, rehearse on a copy of real data with row counts, and set the checks that decide go or
  stop. Use for "add/rename/drop a column", "migrate this data", "change the schema", "backfill",
  "change a file or message format", "is this migration safe", or any change to stored data.
---

# Migration plan

Code rolls back in a minute. Data, once rewritten, often can't. Plan every data change so that each
step can be deployed alone, can run while old code is still live, and has a way back.

## When it applies

- Any change to a database schema, stored file format, cache layout, queue message shape or index.
- A backfill or bulk rewrite of existing data.

## Procedure

### 1. State the change and the data

Write the before and after shape, how many rows or files are affected (query it), and who reads and
writes this data: services, jobs, other repos, analytics, backups.

### 2. Split into steps that each stand alone

Use expand and contract. A rename of `email` to `contact_email`, for example:

| Step | Change | Old code still works? | Rollback |
| --- | --- | --- | --- |
| 1 Expand | add `contact_email`, nullable | yes | drop the column |
| 2 Dual write | code writes both columns | yes | deploy previous code |
| 3 Backfill | copy `email` to `contact_email` in batches | yes | none needed: old column intact |
| 4 Switch reads | code reads `contact_email` | yes | deploy previous code |
| 5 Contract | stop writing `email`, later drop it | no: point of no return | restore from backup only |

Each step ships separately. Mark the point of no return and put it last, after a waiting period.

### 3. Make the risky steps safe

- **Locks:** know whether the change locks the table on your database and size; use the online or
  concurrent form where it exists (adding indexes, adding columns with defaults).
- **Backfills:** batches of a fixed size, resumable from the last id, safe to run twice, throttled.
- **Defaults and nulls:** decide what old rows get; never let "null" silently mean something new.
- **Backup:** confirm a restorable backup exists before the point of no return. Check the restore,
  not just the backup file.

### 4. Rehearse on a copy

Run the steps on a copy of real data (or a realistic sample at scale). Record time per step and row
counts before and after. Run the rollback for each step and check the data matches the start.

### 5. Set go and stop checks

For each step: the query or metric that shows it worked (row counts match, no nulls where none are
allowed, error rate flat), and the condition that means stop and roll back.

## Output

```
Change: <before -> after>   Affected: <n rows/files>   Readers/writers: <list>
Steps: <the table, with rollback per step>
Point of no return: step <n>, after <wait condition>
Rehearsal: <time per step, counts before/after, rollback tested yes/no>
Checks: <per step: go signal / stop signal>
```

## Rules

- Every step before the point of no return has a tested rollback.
- No step requires old and new code to be deployed at the same instant.
- Never rewrite data in place without a copy or backup you have restored at least once.
- Running the plan against production is the user's call; hand over the plan.
