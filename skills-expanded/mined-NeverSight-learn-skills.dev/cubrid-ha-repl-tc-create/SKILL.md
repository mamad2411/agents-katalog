---
name: cubrid-ha_repl-tc-create
description: "Create, draft, or scaffold a new CUBRID CTP HA replication testcase (.sql) from scratch — for a CBRD bug fix or feature. Use this whenever someone says \"ha_repl tc 만들어줘\", \"ha_repl tc 초안 작성해줘\", \"ha replication 테스트케이스 작성\", \"새 ha_repl testcase\", \"create ha_repl tc\", \"draft ha replication test\", or \"create draft ha_repl tc for CBRD-XXXXX\", even if they don't say the word \"testcase\". They usually give a CBRD number, the behavior to replicate-test, and sometimes a target release dir. NOT for: running/reviewing existing ha_repl tests, CTP configuration, or plain SQL/JDBC/CCI/shell testcases (use the matching cubrid-*-tc-create skill)."
---

# HA Replication Testcase Creator (CTP)

Generate a CUBRID CTP HA replication testcase that passes review on the first try. An ha_repl test is a `.sql` file of `--test:` / `--check:` lines that CTP replays on a master/slave pair; pass/fail is result-set equality between the two nodes at each `--check:`.

## Scope

**Produces:** one self-contained `.sql` testcase under `$TC/sql/` with a `/** ... */` header, balanced `--test:`/`--check:` markers, and correct directory path.

**Does NOT produce:** `.answer` files (ha_repl has none — correctness is master/slave equality), CTP framework/conf changes, CI config, or SQL/JDBC/CCI/shell tests (route those to the matching `cubrid-*-tc-create`).

## Before you start

- **CTP must be installed.** Expect it at `$CTP_HOME`, `~/CTP`, or `~/cubrid-testtools/CTP`. Sanity check: `ls $CTP_HOME/conf/ha_repl.conf`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES` if set, else discover the `cubrid-testcases` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing cubrid-jira improves accuracy.

## Directory convention

The path is how CTP identifies and categorizes a test. Multiple `.sql` files for the same area share one `cases/` dir — never create per-test subdirectories.

```
# Bug fix:   $TC/sql/_13_issues/_{yy}_{1|2}h/cases/cbrd_xxxxx.sql
# Feature:   $TC/sql/_{no}_{release_code}/{feature_group}/cases/cbrd_xxxxx.sql
```

`{yy}` = 2-digit year, `{1|2}h` = first/second half (issue creation date). Multiple tests for one issue get a suffix: `cbrd_xxxxx_insert.sql`, `cbrd_xxxxx_ddl.sql`.

ha_repl has no own tree — it runs the `cubrid-testcases/sql` testcases (the `--test:`/`--check:` ones) selected via `$TC/sql/config/daily_regression_test_exclude_list_ha_repl.conf`.

## Lifecycle contract

Every testcase follows this skeleton. Missing a step fails review.

```sql
/**
 * This test case verifies CBRD-XXXXX: one-line title.
 *
 * Coverage:
 * 1 - scenario one
 * 2 - scenario two
 */

--test: DROP TABLE IF EXISTS t1;
--test: CREATE TABLE t1 (id INT PRIMARY KEY, val VARCHAR(100));
--test: INSERT INTO t1 VALUES (1, 'a'), (2, 'b');
--test: COMMIT;

--check: SELECT * FROM t1 ORDER BY id;

--test: DROP TABLE IF EXISTS t1;
--test: COMMIT;
```

### Why each phase matters (not just ritual)

- The `/** ... */` header (CBRD number + `Coverage:` list) is how reviewers and CTP attribute the test — first line must be `This test case verifies CBRD-XXXXX: <title>`.
- `--test:` runs on the **master only** and drives state (DML/DDL/COMMIT); `--check:` runs on **both nodes** and the framework compares result sets. Any mismatch is a replication failure.
- `--test: COMMIT;` after every DML batch is load-bearing: the slave only sees committed data, so an uncommitted change makes the next `--check:` flap.
- The closing `DROP TABLE IF EXISTS` + `COMMIT` leaves the cluster clean for the next test; the leading `DROP` makes the test re-runnable.

## Essential helpers (use these, not raw SQL habits)

| Use | Instead of | Why |
|---|---|---|
| explicit `PRIMARY KEY` on every table | relying on auto-PK | `migrate/Convert.java` auto-adds one, but explicit is clearer and deterministic |
| `--test: COMMIT;` after each DML batch | letting writes ride uncommitted | slave replicates committed data only |
| `--check: SELECT ... ORDER BY` | unordered SELECT | result-set comparison is order-sensitive across nodes |
| `--test: DROP TABLE IF EXISTS t;` | bare `DROP TABLE t;` | re-runnable; survives a prior failed run |

## Writing rules (principles, not ritual)

- **One statement per line** — exactly one SQL statement per `--test:` or `--check:`; never mix both markers on one line.
- **`--check:` is read-only** — SELECT/SHOW only, never DML; that is what gets cross-node compared.
- **Deterministic checks** — `ORDER BY` every `--check:` SELECT; prefer simple data values for easy comparison. 3–8 `--check:` points per file is typical.
- **Commit discipline** — `--test: COMMIT;` after each INSERT/UPDATE/DELETE batch and after DDL that precedes DML, and at the end of cleanup.
- **DDL replicates too** — drive schema changes with `--test:` and verify the resulting state with a `--check:` (e.g. `SELECT COUNT(*) FROM t1`).
- **Keep it focused** — minimal setup, simple names (`t1`, `col1`), no SQL complexity unrelated to the behavior under test.

## House idioms (quick recipes)

These match what the corpus and reviewers expect.

- **Re-runnable table setup:** `--test: DROP TABLE IF EXISTS t1;` immediately before each `--test: CREATE TABLE t1 ...;`.
- **Verify a DML batch:** `--test:` the writes, `--test: COMMIT;`, then a single `--check: SELECT * FROM t1 ORDER BY id;`.
- **Verify DDL replicated:** after the DDL + `COMMIT`, `--check: SELECT COUNT(*) FROM t1;` (or a schema-revealing read) to confirm the slave applied it.
- **vs. SQL testcases:** same `/** ... */` header, but no `evaluate`, no `--+ server-message on/off`, no `.answer` files; lines are prefixed `--test:`/`--check:` and the file lives under `$TC/sql/`.

## Verify before claiming done

ha_repl needs a **3-node cluster** (controller + master + slave) and cannot run locally. Prove correctness as far as the environment allows:

1. **Cluster-first:** if a 3-node test environment is reachable, run it for real — `bin/ctp.sh ha_repl -c conf/ha_repl.conf`, then read `$CTP_HOME/result/ha_repl/current_runtime_logs/` and confirm every `--check:` matched between master and slave. This is ground truth.
2. **Local fallback** (no cluster is a clean, expected path): statically validate the file — header present, markers balanced, every DML batch committed, every `--check:` ordered — and confirm the SQL parses (e.g. via a local `csql -` dry run of the `--test:`/`--check:` statements).

## Self-review checklist

- Header `/** ... */` present with `This test case verifies CBRD-XXXXX:` + Coverage list?
- One statement per line, no line mixing `--test:` and `--check:`?
- Every table has an explicit `PRIMARY KEY`?
- Every DML batch followed by `--test: COMMIT;` before the next `--check:`?
- Every `--check:` is read-only and uses `ORDER BY`?
- Cleanup (`DROP TABLE IF EXISTS` + `COMMIT`) at the end? Leading `DROP` for re-runnability?
- Correct path / `cases/` dir and `_{yy}_{1|2}h` bucket?
- Verified (cluster-first, else static validation)?

## Examples & references

- `@examples/basic_insert_replicate.sql` — INSERT/UPDATE/DELETE replication with consistency checks.
- `@examples/ddl_replicate.sql` — DDL (CREATE/ALTER/DROP TABLE) replication.
- Test guide: `ha_repl_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/ha_repl_guide.md (or `$CTP_HOME/../doc/ha_repl_guide.md` if CTP is checked out locally).
