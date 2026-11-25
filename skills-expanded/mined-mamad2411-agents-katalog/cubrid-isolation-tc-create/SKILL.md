---
name: cubrid-isolation-tc-create
description: "Create, draft, or scaffold a new CUBRID CTP isolation testcase (.ctl) from scratch — for a CBRD bug fix or feature. Use this whenever someone says \"isolation tc 만들어줘\", \"isolation tc 초안 작성해줘\", \"create isolation tc\", \"draft isolation test\", \"새 isolation testcase\", \"isolation testcase 작성\", or \"create draft isolation tc for CBRD-XXXXX\", even if they don't say the word \"testcase\". They usually give a CBRD number, the concurrency behavior to test, and the isolation levels involved. NOT for: running/reviewing existing isolation tests, CTP configuration, or SQL/shell/JDBC/CCI testcases."
---

# Isolation Testcase Creator (CTP)

Generate a CUBRID CTP isolation testcase that passes review on the first try. An isolation test is a `.ctl` script driving N concurrent clients (C1, C2, …) through interleaved transactions, synchronized by a main controller (MC), to verify a specific concurrency behavior — lock contention, read visibility, phantoms, deadlocks.

## Scope

**Produces:** the `.ctl` file(s) — a comment header documenting intent plus a test body of `MC:`/`Cx:` directives, in the correct isolation-level directory.

**Does NOT produce:** answer files (CTP generates these by running the test — never hand-write them), CTP framework changes, CI config, or SQL/shell/JDBC/CCI tests (route those to the matching `cubrid-*-tc-create` skill).

## Before you start

- **CTP must be installed.** Expect it at `$CTP_HOME`, `~/CTP`, or `~/cubrid-testtools/CTP`. Sanity check: `ls $CTP_HOME/isolation/`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES` if set, else discover the `cubrid-testcases` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing cubrid-jira improves accuracy.

## Directory convention

The path encodes the isolation levels under test, so CTP and reviewers categorize the test by where it lives. Tests root at `$TC/isolation/`.

```
# Bug fix:   isolation/_{NN}_{level}/<area>/<test_name>/<test_name>_01.ctl
# Feature:   isolation/_06_features/<feature>/<test_name>/<test_name>_01.ctl
```

Pick the directory by the client isolation levels. For mixed levels, match C1's level first, C2's second:

| C1 / C2 isolation | Directory |
|---|---|
| READ COMMITTED / READ COMMITTED | `_01_ReadCommitted/` |
| REPEATABLE READ / REPEATABLE READ | `_02_RepeatableRead/` |
| REPEATABLE READ / READ COMMITTED | `_04_RepeatableRead_ReadCommitted/` |
| READ COMMITTED / REPEATABLE READ | `_05_ReadCommitted_RepeatableRead/` |
| feature-specific (e.g. SERIALIZABLE, MVCC) | `_06_features/` |

Multiple `.ctl` variants of one scenario number sequentially: `_01.ctl`, `_02.ctl`, …

## Lifecycle contract

Every `.ctl` is a header comment block followed by a body that runs **setup → preparation → test → cleanup → quit**. Missing a phase (or its sync barrier) fails review.

```
/*
Test Case: <short descriptive title>
Priority: 1
Reference case: <CBRD-XXXXX or blank>
Author: <name>

Test Plan:    <1-3 sentences: what concurrency behavior is verified>
Test Scenario: <step-by-step: who does what, when — C1 and C2 actions>
Test Point:
1) <what C1 should/should not experience (block/succeed/see data)>
2) <what C2 should/should not experience>

NUM_CLIENTS = 2
C1: <one-line role>;
C2: <one-line role>;
*/

MC: setup NUM_CLIENTS = 2;

C1: login as 'dba';
C1: set transaction lock timeout INFINITE;
C1: set transaction isolation level read committed;
C2: set transaction lock timeout INFINITE;
C2: set transaction isolation level read committed;

/* preparation */
C1: DROP TABLE IF EXISTS t1;
C1: CREATE TABLE t1 (id INT PRIMARY KEY, val INT);
C1: COMMIT;
MC: wait until C1 ready;

/* test body */
...

/* cleanup */
C1: DROP TABLE IF EXISTS t1;
C1: COMMIT;
MC: wait until C1 ready;

C1: quit;
C2: quit;
```

### Why each phase matters (not just ritual)

- `MC: setup NUM_CLIENTS = N;` must come first — it allocates the connections everything else uses.
- `MC: wait until Cx ready;` is a synchronization barrier: it blocks until that client is idle. Without one after each logical phase, statements from different clients interleave unpredictably and the test goes flaky.
- The header's `NUM_CLIENTS` is documentation only; the real count is the `MC: setup` line.
- `DROP TABLE IF EXISTS` before `CREATE` plus an end cleanup make the test re-runnable; `COMMIT` after preparation releases setup locks before the concurrent phase begins.
- `Cx: quit;` for every client closes sessions; a leaked session can hang the next test.

## Essential helpers (use these, not raw assumptions)

| Directive | Purpose |
|---|---|
| `MC: setup NUM_CLIENTS = N;` | Allocate N concurrent clients (always first) |
| `MC: wait until C1 ready;` / `…C1 ready, C2 ready;` | Barrier — block until the named client(s) idle |
| `Cx: login as 'dba';` / `…as '<user>';` | Authenticate (required at start, or after switching users) |
| `Cx: set transaction lock timeout INFINITE;` / `<ms>;` | Lock wait — `INFINITE` avoids flaky timeouts unless the test verifies timeout |
| `Cx: set transaction isolation level read committed\|repeatable read\|serializable;` | Per-client isolation level |
| `Cx: <SQL>;` / `Cx: COMMIT;` / `Cx: ROLLBACK;` | Execute one statement / transaction control |
| `Cx: quit;` | Close the client session (required at end) |

Label phases with standalone `/* comment */` lines — the runner ignores them.

## Writing rules (principles, not ritual)

- **Set lock timeout and isolation level per client**, before any DML — each client owns its own; don't assume defaults.
- **`login as 'dba'`** at the top for setup/DDL even if a client later switches user.
- **One statement per `Cx:` line** — never combine SQL on one directive.
- **Sync after every phase boundary** with `MC: wait until Cx ready;` — this is the single most common review miss.
- **COMMIT after preparation** so the concurrent phase starts from a clean lock state.
- **Re-runnable:** `DROP TABLE IF EXISTS` before `CREATE`; drop every table/user/object you created during cleanup.
- **No hardcoded paths** — `.ctl` files reference no filesystem paths; route any scratch (e.g. while verifying) through `work=$(mktemp -d)` or the cwd.

## House idioms (quick recipes)

These match what the corpus and reviewers expect.

- **Lock contention** (one writer blocks another): both `Cx: UPDATE … WHERE id = 1;`, `MC: wait until C1 ready;`, `C1: COMMIT;`, then `MC: wait until C1 ready, C2 ready;` lets C2 proceed.
- **Read visibility** (no dirty read): `C1: INSERT …;` then `C2: SELECT …;` (must not see it) → `C1: COMMIT;` → `C2: SELECT …;` again, each followed by its barrier.
- **Phantom read** (SERIALIZABLE prevents phantoms): `C1: SELECT … WHERE val > 0;`, `C2: INSERT …; C2: COMMIT;`, `C1: SELECT … WHERE val > 0;` — assert the phantom row is absent for C1.
- **Privilege / ownership**: `C1: login as 'dba'; C1: ALTER TABLE … OWNER TO u; C1: COMMIT;`, barrier, then `C2: login as 'u'; C2: SELECT …;`.

Full worked scripts: see `@examples/`.

## Verify before claiming done

After authoring, prove the testcase actually runs — don't just eyeball it.

1. **Pod-first:** if a k8s test-shell pod is reachable, run it there for real (install a build, inject the `.ctl`, run via CTP `ctp.sh isolation`, read the feedback log for `OK`/`NOK`). This is ground truth.
2. **Local fallback** (no pod is a clean, expected path): confirm the header parses, every `Cx:` has a matching barrier and `quit`, and run via local CTP if available.

## Self-review checklist

- Header complete? (Test Case, Priority, Test Plan, Test Scenario, Test Point, NUM_CLIENTS, per-client roles)
- `MC: setup NUM_CLIENTS = N;` first, before any client directive?
- `MC: wait until Cx ready;` after **every** phase boundary?
- Lock timeout **and** isolation level set per client, before DML?
- One statement per `Cx:` line? `COMMIT` after preparation?
- Re-runnable (`DROP TABLE IF EXISTS`) and cleaned up (tables/users dropped)?
- All clients `quit`? Correct isolation-level directory? Dir/file numbering right?
- Verified (pod-first, else local)?

## Examples & references

- `@examples/read_committed_lock_test.ctl` — lock contention between two transactions under READ COMMITTED.
- `@examples/serializable_phantom_read.ctl` — phantom-read prevention under SERIALIZABLE.
- Test guide: `isolation_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/isolation_guide.md (or `$CTP_HOME/../doc/isolation_guide.md` if CTP is checked out locally).
