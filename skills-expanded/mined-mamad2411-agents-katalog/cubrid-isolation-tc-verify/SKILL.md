---
name: cubrid-isolation-tc-verify
description: "Run one CUBRID CTP isolation testcase (.ctl) on this machine, judge PASS/FAIL, and on failure diagnose the root cause from the concurrent scenario's evidence. Use whenever someone wants to physically run a specific isolation test and know whether it passes and why — Korean: \"isolation tc 돌려봐\", \"격리 테스트 실행\", \"수행해줘\", \"패스하는지 확인\", \"검증해줘\", \"실패 원인 알려줘\"; English: \"run isolation test\", \"execute isolation tc\", \"verify\", \"check if it passes\". A CUBRID build URL alongside a test name or .ctl path is a strong signal — invoke this skill. NOT for: creating isolation tests (use cubrid-isolation-tc-create), reviewing test code, or running the whole isolation regression suite."
---

# Isolation Testcase Verifier (CTP)

Run a single CTP isolation testcase (`.ctl`), report PASS/FAIL, and — when it fails — diagnose *why* from the evidence the concurrent run leaves behind. "Verify" means all three: **run → judge → diagnose**, not just execute.

## Scope

**Does:** install a given CUBRID build, locate and run one `.ctl` testcase via CTP, read its result, and on FAIL trace the failure to a root cause with a fix recommendation. Isolation tests drive multiple concurrent clients, so the failure is usually a lock/visibility/ordering change rather than a single error line.

**Does NOT:** edit/review test code, create tests, run full suites, or bisect a batch of failures across commits.

## Before you start

- **CTP installed.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/bin/ctp.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES` if set, else discover the `cubrid-testcases` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **Build URL.** A CUBRID build URL is required to install the binary under test. If not given, ask for it.
- **Java.** CTP is Java-based; `JAVA_HOME` must be set (`export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which java))))`).
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` improves accuracy.
- Test guide: `isolation_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/isolation_guide.md (or `$CTP_HOME/../doc/isolation_guide.md` if CTP is checked out locally).

## Run

Work from a scratch dir so logs and configs never collide: `work=$(mktemp -d)`.

1. **Install CUBRID** and verify it really worked — `run_cubrid_install` returns 0 even on failure and wipes `$HOME/CUBRID` first, so trust the binary, not the exit code:
   ```bash
   sh "$CTP_HOME/common/script/run_cubrid_install" <build_url> 2>&1 | tee "$work/install.log"
   grep '\[ERROR\]' "$work/install.log" && { echo "install failed"; }   # stop & show these lines if present
   source ~/.cubrid.sh && cubrid --version                              # must print a version
   ```
2. **Locate the testcase** — isolation tests live under `$TC/isolation/`: `find "$TC/isolation" -name '<pattern>.ctl'`.
3. **Read the `.ctl` first** — know the concurrent scenario, which clients/transactions it runs, and what serialization it expects. This is what makes a failure diagnosable.
4. **Write a CTP config** pointed at the *directory* containing the `.ctl` (not the file). A directory runs every `.ctl` in it, so isolate the one test if needed:
   ```bash
   printf 'scenario=%s\ntest_category=isolation\nfeedback_type=file\n' "<ctl_dir>" > "$work/runone.conf"
   ```
5. **Execute** with a timeout — isolation tests can deadlock and hang:
   ```bash
   timeout 600 "$CTP_HOME/bin/ctp.sh" isolation -c "$work/runone.conf" 2>&1 | tee "$work/run.log"; echo "exit=$?"   # 124 = timeout
   ```

## Verdict

Read the CTP output and the generated result file:
```bash
grep -E 'PASS|FAIL|success|fail' "$work/run.log" | tail -20
cat <ctl_dir>/<test_name>.result
```
All cases PASS → PASS. Any FAIL, timeout (exit 124), or a crash → FAIL; proceed to Failure analysis. After the verdict, check for leftovers (`cubrid server status`, `ps -ef | grep cub_`) and offer cleanup.

## Failure analysis

On FAIL, gather evidence then classify — don't guess:

1. **Expected vs actual** — `diff <ctl_dir>/<test_name>.answer <ctl_dir>/<test_name>.result`. The `.answer` is the expected interleaving of the concurrent scenario; any diff is a behavioral change.
2. **Server logs** — `cat $CUBRID/log/server/*.err | tail -50` for deadlocks, lock timeouts, or aborts.
3. **Lock state on a hang** — `cubrid lockdb` shows the blocking transaction when the run times out.
4. **Core dumps** — `ls <ctl_dir>/core* $CUBRID/core*` → a core means a server crash.

**Classify the failure (answer-fix vs bug-report).** This is the decision the user actually needs — is the test wrong, or is CUBRID wrong?
- **answer-fix** (the expected output is stale): the diff is a benign *format/identifier* change — timestamps, transaction ids, plan-text formatting. The concurrency behaved correctly; the `.answer` baseline needs regenerating.
- **bug-report** (CUBRID regressed): a crash/core, a wrong query result, or a changed lock/visibility outcome — a row now visible/blocked that wasn't, a new deadlock, or a serialization-order change. Raise it with the evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an *intentional* isolation-behavior change for this release, prefer answer-fix; if it describes this very failure mode, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] test_name.ctl
  - Result: <pass count from CTP output>
  - Summary: <which concurrent scenario was verified>
```
**Fail:**
```
[FAIL] test_name.ctl
  - Result: <fail count from CTP output>
  - Summary: <which concurrent scenario was verified>
  - Failed at: <phase + step>
  - Root cause: <diagnosis from the evidence>
  - Verdict: answer-fix | bug-report  (<one-line justification>)
  - Key logs: <quoted diff / server-log lines>
  - Suggestion: <regenerate answer file | file a CUBRID bug | fix env>
```

## Common pitfalls

- **Hangs** → lock contention between clients; the 600s timeout kills it. Inspect `cubrid lockdb` and `$CUBRID/log/server/*.err` for the blocking transaction.
- **Env unset** → `source ~/.cubrid.sh`; set `JAVA_HOME` (CTP won't start without it).
- **Whole directory runs** → `scenario=` targets a directory, so every `.ctl` in it runs. Put the single test in its own dir to isolate it.
- **Answer file missing** → the test has no reference output yet; generate the baseline before judging a diff.
