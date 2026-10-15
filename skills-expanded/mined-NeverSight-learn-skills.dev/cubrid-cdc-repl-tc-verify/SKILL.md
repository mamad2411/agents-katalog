---
name: cubrid-cdc_repl-tc-verify
description: "Run one CUBRID CTP cdc_repl replication testcase on configured CDC infrastructure, judge PASS/FAIL, and on failure diagnose the root cause. Use whenever someone wants to physically run a specific cdc_repl test and know whether it passes and why — Korean: \"cdc_repl tc 돌려봐\", \"cdc 테스트 실행\", \"수행해줘\", \"패스하는지 확인\", \"검증해줘\", \"실패 원인 알려줘\"; English: \"run cdc_repl test\", \"verify\", \"check if it passes\". A CUBRID build URL alongside a test name or .sql path is a strong signal — invoke this skill. NOT for: creating tests (use cubrid-cdc_repl-tc-create), reviewing test code, or running full regression suites."
---

# CDC Replication Testcase Verifier (CTP)

Run a single CTP cdc_repl testcase, report PASS/FAIL, and — when it fails — diagnose *why*. "Verify" means all three: **run → judge → diagnose**, not just execute. CDC tests replicate rows from a source node to a target node and compare the two with `CheckDiff.java`; a failure means the data diverged.

## Scope

**Does:** install a given CUBRID build on the configured CDC cluster, locate and run one cdc_repl `.sql` testcase via CTP, read the CheckDiff result, and on FAIL trace the divergence to a root cause with a fix recommendation.

**Does NOT:** edit/review test code, create tests, run full suites, or bisect a batch of failures.

## Before you start

- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES` if set, else discover the `cubrid-testcases` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below. cdc_repl has no own tree — it runs the `cubrid-testcases/sql` testcases (the `--test:`/`--check:` ones) selected via `$TC/sql/config/daily_regression_test_exclude_list_cdc_repl.conf`.
- Reference: no dedicated cdc_repl guide — see `ha_repl_guide.md` (https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/ha_repl_guide.md) and `$CTP_HOME/common/ext/run_cdc_repl.sh`.
- **CTP installed.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/bin/ctp.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **CDC infrastructure required.** These tests CANNOT run on a single local machine. They need a source + target cluster declared in `$CTP_HOME/conf/cdc_repl.conf` (SSH host/user/password for both nodes) with `cdc_test_helper` already built on each node via `cdc_test_helper/build.sh`. Sanity check: `grep -E 'ssh\.(host|user|password)' $CTP_HOME/conf/cdc_repl.conf`. If the conf is missing or credentials are absent, stop and ask the user to configure it.
- **Build URL.** A CUBRID build URL is required so CTP installs the binary on both nodes. If neither `cubrid_download_url` in the conf nor the user supplies one, ask for it.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` improves accuracy.

## Run

Work from a scratch dir so logs and the temp conf never collide: `work=$(mktemp -d)`.

1. **Locate the testcase** — cdc_repl runs `cubrid-testcases/sql` testcases (the `--test:`/`--check:` ones). From a partial name or CBRD number: `find "$TC/sql" -path '*/cases/*.sql' -name '<pattern>.sql'`.
2. **Read the script first** — understand its `--test:` (apply on source) and `--check:` (compare source vs target) markers. Confirm every table declares an explicit `PRIMARY KEY`; CDC tracks rows by PK and cannot replicate a table without one. This is what makes a failure diagnosable.
3. **Prepare a temp conf** pointed at this test's `cases/` dir and build URL:
   ```bash
   cp "$CTP_HOME/conf/cdc_repl.conf" "$work/cdc_repl.conf"
   sed -i "s|^scenario=.*|scenario=/path/to/test/cases|" "$work/cdc_repl.conf"
   sed -i "s|^cubrid_download_url=.*|cubrid_download_url=<build_url>|" "$work/cdc_repl.conf"   # only if user supplied one
   ```
4. **Execute** with a generous timeout — CDC needs remote install plus daemon startup:
   ```bash
   timeout 1200 "$CTP_HOME/bin/ctp.sh" cdc_repl -c "$work/cdc_repl.conf" 2>&1 | tee "$work/run.log"; echo "exit=$?"   # 124 = timeout
   ```

## Verdict

Read the runtime log and report the result line verbatim:
```bash
cat "$CTP_HOME"/result/cdc_repl/current_runtime_logs/*.log | tail -50    # look for PASS / FAIL
```
`PASS` (CheckDiff found no source/target discrepancy) → PASS. `FAIL`, timeout (exit 124), or a crash → FAIL; proceed to Failure analysis.

## Failure analysis

On FAIL, gather evidence then classify — don't guess:

1. **Run log** (`$work/run.log`) — CTP `[ERROR]` lines (install/config failure), CDC daemon startup errors.
2. **CheckDiff output** — `grep -A10 'CheckDiff\|FAIL\|differ\|mismatch' "$work/run.log"`. Identify which `--check:` query diverged and the source-vs-target rows it printed.
3. **Helper / server logs** — confirm `cdc_test_helper` captured changes without error, and check the remote node's `$CUBRID/log/server/*.err` for replication failures.

**Classify the failure (answer-fix vs bug-report).** This is the decision the user actually needs — is the test wrong, or is CUBRID's CDC wrong?
- **answer-fix** (the test is at fault): a table missing a `PRIMARY KEY`, an unsupported scenario, or an expected-result baseline that's stale. Fix the `.sql`/baseline.
- **bug-report** (CDC regressed): rows that should have replicated are missing or wrong at the target, a crash/core, or a column type (e.g. BLOB/CLOB) that silently fails to replicate. Raise it with the CheckDiff evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an intentional replication-behavior change, prefer answer-fix; if it describes this very divergence, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] test_name
  - Result: CheckDiff found no discrepancy between source and target
  - Summary: <what the test verified>
```
**Fail:**
```
[FAIL] test_name
  - Failed at: <--check: query that diverged>
  - CheckDiff: <source vs target diff lines>
  - Root cause: <diagnosis from the evidence>
  - Verdict: answer-fix | bug-report  (<one-line justification>)
  - Key logs: <quoted error / diff lines>
  - Suggestion: <add PRIMARY KEY | file a CUBRID bug | fix conf/build URL>
```

## Common pitfalls

- **`cdc_repl.conf` missing/incomplete** → stop; SSH credentials and `cubrid_download_url` must be set before running.
- **Table missing PRIMARY KEY** → CDC cannot track rows; every table in the `.sql` must declare one explicitly.
- **`cdc_test_helper` not built** → build it on both infrastructure nodes before retrying.
- **Build URL wrong/unreachable** → CTP prints `[ERROR]` during install; grep `$work/run.log`.
- **LOB column divergence** → BLOB/CLOB may not replicate correctly; check whether the failing `--check:` touches LOB columns.
