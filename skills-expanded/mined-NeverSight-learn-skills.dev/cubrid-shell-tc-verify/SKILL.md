---
name: cubrid-shell-tc-verify
description: "Run one CUBRID CTP shell testcase on this machine, judge OK/NOK, and on failure diagnose the root cause. Use whenever someone wants to physically run a specific shell test and know whether it passes and why — Korean: \"돌려봐\", \"수행해줘\", \"실행해봐\", \"패스하는지 확인\", \"검증해줘\", \"실패 원인 알려줘\"; English: \"run\", \"execute\", \"verify\", \"check if it passes\". A CUBRID build URL alongside a test name or .sh path is a strong signal — invoke this skill. NOT for: reviewing/editing test code, creating new tests, exclusion lists, or whole regression suites (a multi-failure bisect report is a different job)."
---

# Shell Testcase Verifier (CTP)

Run a single CTP shell testcase, report OK/NOK, and — when it fails — diagnose *why* from the evidence the run leaves behind. "Verify" means all three: **run → judge → diagnose**, not just execute.

## Scope

**Does:** install a given CUBRID build, locate and run one `.sh` testcase, read its `.result`, and on NOK trace the failure to a root cause with a fix recommendation.

**Does NOT:** edit/review test code, create tests, run full suites, or bisect a batch of failures across commits.

## Before you start

- **CTP installed.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/shell/init_path/init.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`). CUBRID itself need not be pre-installed.
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES_PRIVATE_EX` if set, else discover the `cubrid-testcases-private-ex` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **Build URL.** A CUBRID build URL is required to install the binary under test. If not given, ask for it.
- Test guide: `shell_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/shell_guide.md (or `$CTP_HOME/../doc/shell_guide.md` if CTP is checked out locally).
- **JIRA context (optional).** If the test maps to a `CBRD-XXXXX`, run `cubrid-jira search CBRD-XXXXX` first to ground diagnosis in the issue's real symptom and expected behavior (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` notably sharpens the failure verdict.

## Run

Work from a scratch dir so logs never collide: `work=$(mktemp -d)`.

1. **Install CUBRID** and verify it really worked — `run_cubrid_install` returns 0 even on failure and wipes `$HOME/CUBRID` first, so trust the binary, not the exit code:
   ```bash
   sh "$CTP_HOME/common/script/run_cubrid_install" <build_url> 2>&1 | tee "$work/install.log"
   grep '\[ERROR\]' "$work/install.log" && { echo "install failed"; }   # stop & show these lines if present
   source ~/.cubrid.sh && cubrid --version                               # must print a version
   ```
2. **Locate the testcase** — shell tests live at `{test_name}/cases/{test_name}.sh`. From a partial name or CBRD number: `find $TC/shell -path '*/cases/*' -name '<pattern>.sh'`.
3. **Read the script first** — know what it tests, which DBs/services it touches, and any platform guard (`WINDOWS_NOT_SUPPORTED`). This is what makes a failure diagnosable.
4. **Execute** from the `cases/` dir (tests use relative paths) with a timeout:
   ```bash
   export init_path="$CTP_HOME/shell/init_path"
   cd /path/to/test_name/cases/
   timeout 300 sh test_name.sh 2>&1 | tee "$work/run.log"; echo "exit=$?"   # 124 = timeout
   ```

## Verdict

Read the result file and report each line verbatim:
```bash
cat /path/to/test_name/cases/test_name.result    # "test_name-1 : OK" (pass) | "... : NOK" (fail)
```
`OK` → PASS. `NOK`, timeout (exit 124), or a crash → FAIL; proceed to Failure analysis. After the verdict, check for leftovers (`cubrid server status`, `ps -ef | grep cub_`) and offer cleanup.

## Failure analysis

On NOK, gather evidence then classify — don't guess:

1. **Run log** (`$work/run.log`) — csql/utility errors, shell errors, `write_nok` assertions.
2. **Server / broker logs** — `cat $CUBRID/log/server/*.err`, `ls $CUBRID/log/broker/*.err`.
3. **Core dumps** — `ls /path/to/test_name/cases/core* $CUBRID/core*` → a core means a server crash.
4. **Expected vs actual** — if the test compares files, `diff` the `.answer` against the result.

**Classify the failure (answer-fix vs bug-report).** This is the decision the user actually needs — is the test wrong, or is CUBRID wrong?
- **answer-fix** (the test's expected output is stale): the diff is a *format/identifier* change — hash-text suffixes, cache keys, XASL/SHA1 ids, byte-counter shifts, plan-text formatting. The product behaves correctly; the `.answer` baseline needs regenerating.
- **bug-report** (CUBRID regressed): a crash/core, a wrong query result, a lock/deadlock change, or a performance regression. Raise it with the evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an *intentional* output change for this release, prefer answer-fix; if it describes this very failure mode, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] test_name
  - Result: test_name-1 : OK
  - Summary: <what the test verified>
```
**Fail:**
```
[FAIL] test_name
  - Result: test_name-1 : NOK
  - Summary: <what the test verified>
  - Failed at: <phase + command>
  - Root cause: <diagnosis from the evidence>
  - Verdict: answer-fix | bug-report  (<one-line justification>)
  - Key logs: <quoted error lines>
  - Suggestion: <regenerate answer file | file a CUBRID bug | fix env>
```

## Common pitfalls

- **Hangs** → unbounded loop, stuck server (`$CUBRID/log/server/*.err`), or lock wait (`cubrid lockdb`).
- **Env unset** → `source ~/.cubrid.sh`; `export init_path="$CTP_HOME/shell/init_path"`.
- **Answer file missing** → the test needs `init answer` mode first to generate the baseline.
