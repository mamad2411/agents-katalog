---
name: database-operations
description: Runs database work safely in live environments: migration authoring and ordering, lock awareness, batched backfills, index creation, seeding, connection management, production query safety and the destructive statement protocol.
license: MIT
metadata:
  category: devops-skills
  version: 1.0.0
  depends_on: [engineering-core, devops-core, backend-engineering]
  outputs: [migration-plan, lock-assessment, seed-strategy, operation-record]
---

# Database Operations

The database holds the only part of a system that cannot be redeployed. Code
is replaceable; a truncated table is not.

## 1. Migration authoring

```
One migration, one purpose
Reversible, or the irreversibility is stated in the file
Idempotent where the tool does not guarantee single application
Never edited after it has run anywhere but a local machine
Never containing a data change that belongs in a backfill script
```

Ordering rules, per `deployment-engineering` section 3: additive before the
code, destructive after the code that stopped using the old shape.

## 2. Lock awareness

Every statement against a live table has a lock profile. Know it before
running it, not after the application times out.

| Statement | Typical lock | Safe on a large table |
|---|---|---|
| add a nullable column, no default | brief metadata lock | yes |
| add a column with a volatile default | rewrites the table on older engines | check the engine version |
| add a NOT NULL constraint | full scan while locked | no, add as nullable then validate |
| create an index | writes blocked for the duration | no, create concurrently |
| create an index concurrently | writes allowed, slower | yes |
| drop a column | brief metadata lock, data unrecoverable | fast, and irreversible |
| rename a column | brief, and breaks the running code | never in one step |
| alter a column type | rewrites the table | no, expand and contract |
| add a foreign key | locks both tables while validating | add NOT VALID, then validate |
| unbounded update or delete | locks every affected row | no, batch it |
| truncate | exclusive lock, data gone | approval, backup |
| vacuum full | exclusive lock for the duration | never on a live table |

The row that surprises people: creating an index normally blocks writes for
its whole duration, which on a large table is minutes of an application that
appears to hang.

## 3. Backfills

```
Batched         a bounded number of rows per statement
Resumable       the predicate is the state, not a cursor position
Throttled       a pause between batches, so replication and other traffic
                keep up
Observable      each batch reports progress
Interruptible   stopping it leaves the database consistent
Idempotent      running it again finishes the work, it does not redo it
```

```sql
update orders
set buyer_name = customer_name
where buyer_name is null
  and id in (select id from orders where buyer_name is null limit 5000);
```

Rerunnable, interruptible, and it reports how many rows remain by the same
predicate that drives it.

The single unbounded statement is the version that gets written when batching
feels like ceremony, and it is the one that holds locks on a whole table.

## 4. Seeding

```
Development   deterministic, useful, obviously fake, enough volume to reveal
              missing indexes
Test          minimal, created and destroyed per run
Staging       anonymised production shaped data, never real personal data
Production    reference data only: roles, categories, plans; never demo users
```

The seed command refuses to run when the environment is production, unless the
project explicitly seeds reference data there, in which case that path is
separate and named.

Development seeds that contain twenty rows hide every performance defect the
project will have. Seed enough to be honest.

## 5. Connections

```
Pool size      chosen against the database's limit and the instance count,
               not copied from an example
Timeouts       connection, statement and idle, all set
Leaks          every connection returned; a pool that grows monotonically is
               a leak
Migrations     use their own connection, not the application pool
Serverless     a pooler is usually required; connection per invocation
               exhausts a database quickly
```

The arithmetic that gets skipped: instances multiplied by pool size must stay
below the database's connection limit, with room for migrations and manual
access.

## 6. Production queries

Reading production data is an operation, not a convenience.

```
Read only       by default, with a read only role where possible
Bounded         every ad hoc query has a LIMIT
Timed           a statement timeout, so a bad query cannot stall the database
Justified       there is a reason, and it is recorded
No personal     data is not copied out to a local machine
```

Before any write statement in production, run its `SELECT COUNT(*)` form with
the same `WHERE` clause, read the number, and confirm it matches the
expectation. An `UPDATE` reporting far more rows than expected is a restore.

## 7. Destructive statement protocol

Per `devops-core` section 6, with the database specifics:

```
1  Write the statement with its WHERE clause
2  Convert it to SELECT COUNT(*) and run that first
3  Confirm the count matches the intent
4  Verify a backup exists, and when it was taken
5  Verify the target: current database, current host, read back
6  Wrap in a transaction where the engine allows, inspect, then commit
7  Execute, capture the output
8  Verify the effect, and check what else changed
9  Record the operation
```

Step 6 is the strongest safeguard available: run the statement inside a
transaction, check the affected count and a sample of the result, and commit
only then.

## 8. Restores

A backup that has never been restored is a hypothesis. See `backup-recovery`.

Restoring over a live database is irreversible: it destroys everything written
since the backup. It requires a backup of the current state first, taken
immediately before.

## 9. Protocol

1. Author the migration per section 1.
2. Assess the lock profile per section 2, against the real table size.
3. Test the migration against a copy of realistic data, or state that no
   rehearsal was possible.
4. Plan backfills per section 3.
5. Verify connection arithmetic per section 5.
6. For any live operation, classify blast radius and apply section 7.
7. Record the operation.

## 10. Auto-critique

Score from 0 to 5: migration single purpose and correctly ordered, lock
profile known before running, backfills batched and resumable, seeds honest in
volume and free of real personal data, connection arithmetic done, count
before every destructive statement, target verified, operation recorded.

Threshold: no axis below 3, average at least 4. An unbounded update or delete
against a live table, or a destructive statement run without a count first, is
an automatic failure.

## 11. Interfaces

- Upstream: `devops-core`, `backend-engineering`,
  the database section of the architecture document, produced by
  `architecture-proposal`.
- Lateral: `deployment-engineering` for ordering, `performance-engineering`
  for index decisions.
- Downstream: `backup-recovery`, `production-verification`,
  `release-readiness` gate 5.
