---
name: cubrid-ha_shell-tc-verify
description: "Run one CUBRID CTP HA shell testcase on a configured master+slave pair, judge OK/NOK, and on failure diagnose the root cause across both nodes. Use whenever someone wants to physically run a specific HA shell test and know whether it passes and why — Korean: \"ha shell tc 돌려봐\", \"ha shell 테스트 실행\", \"수행해줘\", \"패스하는지 확인\", \"검증해줘\", \"실패 원인 알려줘\"; English: \"run ha shell test\", \"verify\", \"check if it passes\". NOT for: creating/editing HA tests (use cubrid-ha_shell-tc-create), single-node shell tests (use cubrid-shell-tc-verify), or whole regression suites."
---

# HA Shell Testcase Verifier (CTP)

Run a single CTP HA shell testcase, report OK/NOK, and — when it fails — diagnose *why* from the evidence both nodes leave behind. "Verify" means all three: **run → judge → diagnose**, not just execute.

## Scope

**Does:** run one HA `.sh` testcase (built on `make_ha.sh`) on a configured master+slave pair, read its `.result`, and on NOK trace the failure to a root cause with a fix recommendation. DB name is always `hatestdb`.

**Does NOT:** edit/review test code, create tests, run full suites, or run on a single machine — HA tests need a master + slave node pair.

## Before you start

- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES_PRIVATE` if set, else discover the `cubrid-testcases-private` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **CTP + HA helpers.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/shell/init_path/make_ha.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **HA infrastructure.** A configured slave is mandatory: `find $CTP_HOME -name HA.properties` must yield a file with slave SSH credentials (host/user/password). CUBRID must be installed on both nodes. If unconfigured, stop and explain HA tests cannot run without a reachable slave.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` improves accuracy.
- Test guide: `ha_shell_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/ha_shell_guide.md (or `$CTP_HOME/../doc/ha_shell_guide.md` if CTP is checked out locally).

## Run

Work from a scratch dir so logs and conf never collide: `work=$(mktemp -d)`.

1. **Locate the testcase** — HA shell tests live at `$TC/HA/shell/{name}/cases/{name}.sh`. From a partial name or CBRD number: `find $TC/HA/shell -path '*/cases/*' -name '<pattern>.sh'`.
2. **Read the script first** — know its setup/test/verify/cleanup phases and which `make_ha.sh` helpers (`setup_ha_environment`, `wait_for_slave`, `run_on_slave`) it uses. This is what makes a failure diagnosable.
3. **Build a run conf** pointing at the `cases/` dir, carrying any HA settings from the template:
   ```bash
   { echo "scenario=/path/to/name/cases"; echo "test_category=shell"; \
     grep -E '^(ha_|slave_|master_)' "$CTP_HOME/conf/shell_template.conf"; } > "$work/run.conf"
   ```
4. **Execute** via CTP with a long timeout — HA setup creates `hatestdb` on both nodes and starts heartbeat:
   ```bash
   timeout 1200 "$CTP_HOME/bin/ctp.sh" shell -c "$work/run.conf" 2>&1 | tee "$work/run.log"; echo "exit=$?"   # 124 = timeout
   ```

## Verdict

Read the result file and report each line verbatim:
```bash
cat /path/to/name/cases/name.result    # "name-1 : OK" (pass) | "... : NOK" (fail)
```
`OK` → PASS. `NOK`, timeout (exit 124), or a crash → FAIL; proceed to Failure analysis. After the verdict, check for leftovers (`cubrid hb status`, `cubrid server status`) on both nodes and offer cleanup.

## Failure analysis

On NOK, gather evidence then classify — don't guess. HA failures land in one of four phases: **setup / test / verify / cleanup**.

1. **Run log** (`$work/run.log`) — `grep -E 'ERROR|FAILED|write_nok|exit 1'`; find which phase aborted.
2. **Master logs** — `cat $CUBRID/log/server/*.err`; `cubrid hb status` (both nodes must be in HA mode).
3. **Slave logs** — inspect via the helper, not raw ssh: `run_on_slave -c "cat \$CUBRID/log/server/*.err"`, `run_on_slave -c "cubrid hb status"`.
4. **Replication** — did `setup_ha_environment` bring both nodes up, and did `wait_for_slave` complete before the verify step? A master/slave data mismatch usually means a missing sync wait.

**Classify the failure (answer-fix vs bug-report)** — the decision the user needs: is the test wrong, or is CUBRID wrong?
- **answer-fix** (stale baseline): the diff is a format/identifier change — the product replicated correctly, the `.answer` needs regenerating.
- **bug-report** (CUBRID regressed): a crash/core, replication that never converged, wrong query result, deadlock, or a heartbeat/failover defect. Raise it with the evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an intentional output change, prefer answer-fix; if it describes this very failure mode, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] name
  - Result: name-1 : OK
  - Summary: <what HA behavior was verified>
```
**Fail:**
```
[FAIL] name
  - Result: name-1 : NOK
  - Summary: <what HA behavior was verified>
  - Failed at: <phase — setup/test/verify/cleanup + command>
  - Root cause: <diagnosis from the evidence, master vs slave>
  - Verdict: answer-fix | bug-report  (<one-line justification>)
  - Key logs: <quoted error lines>
  - Suggestion: <regenerate answer file | file a CUBRID bug | fix HA env>
```

## Common pitfalls

- **`setup_ha_environment` fails early** → slave unreachable; check SSH connectivity and `HA.properties` credentials.
- **`setup_ha_environment` hangs** → heartbeat startup on the slave timed out, often because CUBRID is already running there — clean up the slave and retry.
- **`wait_for_slave` timeout** → replication didn't finish in time (network latency / slave overload); check slave logs via `run_on_slave`.
- **Master/slave data mismatch at verify** → a `wait_for_slave` is likely missing before the comparison; review the `.sh` for the absent sync wait.
- **`make_ha.sh` not found** → reinstall CTP; HA helpers must be in `$CTP_HOME/shell/init_path/`.
