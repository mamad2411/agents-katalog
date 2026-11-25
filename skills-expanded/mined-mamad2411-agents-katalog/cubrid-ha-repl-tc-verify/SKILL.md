---
name: cubrid-ha_repl-tc-verify
description: "Run one CUBRID CTP ha_repl replication testcase on configured HA infrastructure, judge PASS/FAIL, and on failure diagnose the root cause. Use whenever someone wants to physically run a specific ha_repl test and know whether master/slave stay in sync and why — Korean: \"ha_repl tc 돌려봐\", \"ha replication 테스트 실행\", \"검증해줘\", \"실패 원인 알려줘\", \"패스하는지 확인\"; English: \"run ha_repl test\", \"verify\", \"check if it passes\". A CUBRID build URL alongside a test name or .sql path is a strong signal — invoke this skill. NOT for: creating tests (use cubrid-ha_repl-tc-create), editing/reviewing test code, or whole regression suites."
---

# HA Replication Testcase Verifier (CTP)

Run a single CTP ha_repl testcase, report PASS/FAIL, and — when it fails — diagnose *why* from the evidence the run leaves behind. "Verify" means all three: **run → judge → diagnose**, not just execute.

## Scope

A ha_repl test is a `.sql` with `--test:` / `--check:` markers: CTP runs `--test:` statements on the master and, at each `--check:`, compares the master's result against the slave's. A mismatch is a replication failure.

**Does:** install a given CUBRID build on the configured master+slave nodes, run one ha_repl `.sql` testcase via CTP, read the PASS/FAIL summary, and on FAIL trace the failure to a root cause with a fix recommendation.

**Does NOT:** edit/review test code, create tests, run full suites, or bisect a batch of failures.

> **These tests CANNOT run on a single local machine.** They need a 3-node setup (controller + master + slave) reachable over SSH.

## Before you start

- **CTP installed.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/bin/ctp.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES` if set, else discover the `cubrid-testcases` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below. ha_repl has no own tree — it runs the `cubrid-testcases/sql` testcases (the `--test:`/`--check:` ones) selected via `$TC/sql/config/daily_regression_test_exclude_list_ha_repl.conf`.
- Test guide: `ha_repl_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/ha_repl_guide.md (or `$CTP_HOME/../doc/ha_repl_guide.md` if CTP is checked out locally).
- **HA infrastructure configured.** `ls $CTP_HOME/conf/ha_repl.conf` and confirm master/slave SSH keys are set: `grep -E "env.instance1.(master|slave).ssh.(host|user|password)" $CTP_HOME/conf/ha_repl.conf`. If the file or any key is missing, stop and ask the user to set master/slave SSH credentials.
- **Build URL.** A CUBRID build URL is required so CTP installs the binary on both nodes. If `cubrid_download_url` isn't already set in the conf and the user didn't provide one, ask for it.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` improves accuracy.

## Run

Work from a scratch dir so confs and logs never collide: `work=$(mktemp -d)`.

1. **Locate the testcase** — ha_repl runs `cubrid-testcases/sql` testcases (the `--test:`/`--check:` ones). From a partial name or CBRD number: `find "$TC/sql" -path '*/cases/*.sql' -name '<pattern>.sql'`.
2. **Read the script first** — know its `--test:` / `--check:` markers and what each check expects. This is what makes a failure diagnosable.
3. **Prepare a temp conf** pointing CTP at this one test's `cases/` dir and the build URL:
   ```bash
   cp "$CTP_HOME/conf/ha_repl.conf" "$work/run.conf"
   sed -i "s|^scenario=.*|scenario=/path/to/test_name/cases|" "$work/run.conf"
   sed -i "s|^cubrid_download_url=.*|cubrid_download_url=<build_url>|" "$work/run.conf"   # omit if conf already set
   ```
4. **Execute** with a generous timeout — CTP installs CUBRID on the remote nodes first, so these are slow:
   ```bash
   timeout 1200 "$CTP_HOME/bin/ctp.sh" ha_repl -c "$work/run.conf" 2>&1 | tee "$work/run.log"; echo "exit=$?"   # 124 = timeout
   ```

## Verdict

Read the runtime log and report the summary line verbatim:
```bash
ls -t $CTP_HOME/result/ha_repl/current_runtime_logs/*.log | head -1 | xargs tail -50   # look for PASS / FAIL
```
`PASS` (all `--check:` points matched master↔slave) → PASS. `FAIL`, timeout (exit 124), or an install `[ERROR]` → FAIL; proceed to Failure analysis.

## Failure analysis

On FAIL, gather evidence then classify — don't guess:

1. **Install phase** — `grep '\[ERROR\]' "$work/run.log"`. An error here means the build never installed; it's an env/build problem, not a replication failure.
2. **Failing check** — `grep -A5 'FAIL\|mismatch\|differ' "$work/run.log"`. Identify *which* `--check:` query diverged and the master-result vs slave-result it printed.
3. **Replication lag vs real divergence** — a check that fails because the slave hadn't caught up yet (data committed on master but not yet replicated) is a *test* problem: every `--check:` must be preceded by `--test: COMMIT;`. A check that fails after the slave is fully caught up is a *replication* divergence.
4. **Node errors** — the master or slave `$CUBRID/log/server/*.err` (and replication logs) on the remote hosts. A crash/core on either node is a server bug.

**Classify the failure (test-fix vs bug-report).** This is the decision the user actually needs.
- **test-fix** (the test is wrong): missing `--test: COMMIT;` before a check, a table with no primary key (replication needs one), or a stale expected value. The product replicates correctly; the `.sql` needs fixing.
- **bug-report** (CUBRID regressed): genuine master↔slave divergence after sync, a replication apply error, or a crash on either node. Raise it with the evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an intentional behavior change, prefer test-fix; if it describes this very divergence, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] test_name
  - Result: all --check: points matched between master and slave
  - Summary: <what the test verified>
```
**Fail:**
```
[FAIL] test_name
  - Failed at: --check: <query>
  - Master result: <rows>
  - Slave result:  <rows>
  - Root cause: <diagnosis from the evidence>
  - Verdict: test-fix | bug-report  (<one-line justification>)
  - Key logs: <quoted error / mismatch lines>
  - Suggestion: <fix the .sql | file a CUBRID bug | fix HA env>
```

## Common pitfalls

- **`ha_repl.conf` missing/incomplete** → stop; the master/slave SSH credentials and `cubrid_download_url` must be set before any run.
- **Build URL wrong or unreachable** → CTP prints `[ERROR]` in the install phase (`$work/run.log`); nothing replicates.
- **Slave lag at `--check:`** → add `--test: COMMIT;` before every `--check:` block so the slave can catch up.
- **Table has no PRIMARY KEY** → CTP auto-adds one via `migrate/Convert.java`, but explicit PKs are safer; review the `.sql`.
- **Timeout (exit 124)** → remote install is slow or the slave is unreachable; raise the timeout or check network connectivity.
