---
name: cubrid-cdc_repl-tc-create
description: "Create, draft, or scaffold a new CUBRID CTP CDC replication testcase (.sql) from scratch — for a CBRD bug fix or feature. Use this whenever someone says \"cdc_repl tc 만들어줘\", \"cdc tc 초안 작성해줘\", \"create cdc repl tc\", \"draft cdc test\", \"새 cdc 테스트케이스\", or \"create draft cdc tc for CBRD-XXXXX\", even if they don't say the word \"testcase\". They usually give a CBRD number, the behavior to capture, and sometimes a target release dir. NOT for: running/reviewing existing CDC tests, CTP configuration, HA/log replication (use cubrid-ha-* skills), or SQL/shell/JDBC testcases."
---

# CDC Replication Testcase Creator (CTP)

Generate a CUBRID CTP CDC replication testcase that passes review on the first try. CDC (Change Data Capture) reads DML from a source DB and applies it to a target; a good testcase is one self-contained `.sql` of `--test:`/`--check:` markers that CTP replays on both nodes and diffs with `CheckDiff.java`.

## Scope

**Produces:** the `.sql` testcase (header + `--test:`/`--check:` markers driving source DML and source/target comparison), in the correct `$TC/sql/` `cases/` directory.

**Does NOT produce:** CTP config (`conf/cdc_repl.conf`), the `cdc_test_helper` / `CdcReplUtils.java` / `CheckDiff.java` tooling, CI config, or HA/log-replication tests — route those to `cubrid-ha-*`. CDC differs from `ha_repl`: it diffs via `CheckDiff` (not master/slave row compare), needs an explicit PRIMARY KEY on every table (ha_repl auto-adds one), and has limited LOB support.

## Before you start

- **CTP must be installed.** Expect it at `$CTP_HOME`, `~/CTP`, or `~/cubrid-testtools/CTP`. Sanity check: `ls $CTP_HOME/bin/ctp.sh $CTP_HOME/conf/`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES` if set, else discover the `cubrid-testcases` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing cubrid-jira improves accuracy.

## Directory convention

The path is how CTP identifies and categorizes a test. Multiple `.sql` files for one issue share the same `cases/` dir — never per-test subdirectories.

```
# Bug fix:   $TC/sql/_13_issues/_{yy}_{1|2}h/cases/cbrd_xxxxx.sql
# Feature:   $TC/sql/_{no}_{release_code}/{feature_group}/cases/cbrd_xxxxx.sql
```

`{yy}` = 2-digit year, `{1|2}h` = first/second half (issue creation date). Split scenarios get a suffix: `cbrd_27100_insert.sql`, `cbrd_27100_update.sql`.

cdc_repl has no own tree — it runs the `cubrid-testcases/sql` testcases (the `--test:`/`--check:` ones) selected via `$TC/sql/config/daily_regression_test_exclude_list_cdc_repl.conf`.

## Lifecycle contract

Every testcase follows this skeleton. Missing a step fails review or causes false diffs.

```sql
/**
 * This test case verifies CBRD-XXXXX: <one-line statement of what CDC behavior this checks>
 *
 * Coverage:
 * 1 - CDC captures INSERT
 * 2 - CDC captures UPDATE / DELETE
 * 3 - Data consistency verified via CheckDiff
 */

-- Setup (re-runnable)
--test: DROP TABLE IF EXISTS t1;
--test: CREATE TABLE t1 (id INT PRIMARY KEY, val VARCHAR(100));
--test: COMMIT;

-- Action on source + compare on both
--test: INSERT INTO t1 VALUES (1, 'hello');
--test: COMMIT;
--check: SELECT id, val FROM t1 ORDER BY id;

-- Cleanup
--test: DROP TABLE IF EXISTS t1;
--test: COMMIT;
```

### Why each marker matters (not just ritual)

- `--test:` runs a DML/DDL statement on the **source** DB; CDC captures it. `--check:` runs a query on **both** source and target, and `CheckDiff` compares the two result sets.
- **Every `--test:` data change must end with `--test: COMMIT;`** — CDC captures committed changes only; uncommitted DML never reaches the target, so the diff stalls or fails.
- **Never mix `--test:` and `--check:` in one logical block without a `COMMIT` between them** — you'd compare a state the target hasn't received yet.
- Header `/** ... */` first, setup at top, cleanup at bottom. The header's `CBRD-XXXXX` + `Coverage:` block is what reviewers read first.

## Essential helpers (use these, not raw values)

CDC has hard requirements that raw SQL silently violates — these are the load-bearing conventions.

| Use | Instead of | Why |
|---|---|---|
| explicit `PRIMARY KEY` on every table | a keyless table | CDC tracks rows by PK; keyless tables can't replicate reliably |
| `--test: COMMIT;` after each DML batch | leaving DML open | CDC only captures committed work |
| `--check: ... ORDER BY <pk>` | `--check:` with no order | source/target row order may differ → false diff |
| `DROP TABLE IF EXISTS` before each `CREATE` | bare `CREATE TABLE` | makes the test re-runnable |

The `cdc_test_helper` (native C, built via its `build.sh`), `CdcReplUtils.java`, and `CheckDiff.java` are CTP-side infrastructure — you reference the behavior, you don't author them.

## Writing rules (principles, not ritual)

- **One feature/behavior per file.** Typical: 3–8 `--check:` blocks; give each DML type (INSERT/UPDATE/DELETE) its own `--check:`.
- **Deterministic checks only:** every `--check:` ends in `ORDER BY` on the primary key, with simple predictable values for easy diff inspection.
- **Explicit PK, explicit values:** single-column INT PK is clearest; composite PK is allowed but verbose. Don't rely on `AUTO_INCREMENT` alone when you need to predict inserted IDs — write explicit values.
- **Avoid LOB:** BLOB/CLOB may not replicate via CDC — skip them unless the issue explicitly targets LOB CDC.
- **Test the edges the issue cares about:** empty result after DELETE, multi-row UPDATE, NULL values — each with its own `--check:`.

## House idioms (quick recipes)

These match what the corpus and `CheckDiff` expect.

- **NULL round-trip:** `--test: INSERT INTO t1 VALUES (3, NULL); --test: COMMIT;` then `--check: SELECT id, val FROM t1 WHERE val IS NULL ORDER BY id;`.
- **Multi-table / joins:** create *all* tables before any inserts, dropping children before parents — `DROP t2; DROP t1; CREATE t1 ...; CREATE t2 ...; COMMIT;`.
- **Composite PK:** `--test: CREATE TABLE t1 (id1 INT, id2 INT, val VARCHAR(100), PRIMARY KEY (id1, id2));`.

## Verify before claiming done

CDC needs a full source+target cluster, so local execution is usually impossible — be honest about that.

1. **Cluster-first:** if a CDC-enabled environment is reachable (source + target, `cdc_test_helper` built, `conf/cdc_repl.conf` pointing at both nodes), run via `bin/ctp.sh cdc_repl -c conf/cdc_repl.conf` and read `CTP/result/cdc_repl/current_runtime_logs/` for the `CheckDiff` verdict. This is ground truth.
2. **Static fallback** (no cluster is an expected path): re-read the file against the checklist below — every table has a PK, every DML batch commits, every `--check:` orders by PK, drops precede creates. Route any scratch output through `work=$(mktemp -d)`, never a hardcoded path.

## Self-review checklist

- Header present with `CBRD-XXXXX` and a `Coverage:` section?
- Every table has an explicit PRIMARY KEY?
- Every `--test:` DML batch ends with `--test: COMMIT;`?
- Every `--check:` query has `ORDER BY` on the PK?
- `DROP TABLE IF EXISTS` before every `CREATE TABLE`? Cleanup at the bottom?
- No LOB columns unless the issue requires them? No `--test:`/`--check:` mixed without a commit between?
- Correct `$TC/sql/_13_issues/_{yy}_{1|2}h/cases/` (or feature) path? Filename == `cbrd_xxxxx[_kw].sql`?
- Verified (cluster-first, else static)?

## Examples & references

- `@examples/basic_dml_capture.sql` — INSERT/UPDATE/DELETE CDC capture with consistency checks.
- `@examples/schema_change_capture.sql` — DDL changes captured by CDC.
- Reference: no dedicated cdc_repl guide — see `ha_repl_guide.md` (https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/ha_repl_guide.md) and `$CTP_HOME/common/ext/run_cdc_repl.sh`.
