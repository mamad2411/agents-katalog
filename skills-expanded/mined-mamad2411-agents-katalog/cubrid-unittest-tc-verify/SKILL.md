---
name: cubrid-unittest-tc-verify
description: "Run one CUBRID unittest binary on this machine, judge PASS/FAIL, and on failure diagnose the root cause. Use whenever someone wants to physically run a specific unit test and know whether it passes and why — Korean: \"unittest 돌려봐\", \"유닛테스트 실행\", \"유닛테스트 수행\", \"패스하는지 확인\", \"검증해줘\", \"실패 원인 알려줘\"; English: \"run unittest\", \"execute unit test\", \"verify\", \"check if it passes\". NOT for: creating new unit tests (use cubrid-unittest-tc-create) or running the whole unittest regression suite."
---

# Unittest Verifier (CTP)

Run a single CUBRID unittest binary, report PASS/FAIL, and — when it fails — diagnose *why* from the run output and any core dump. "Verify" means all three: **run → judge → diagnose**, not just execute.

## Scope

**Does:** locate (or build) one `unittests_<module>` binary, run it, judge from its output text, and on FAIL trace the failure to a root cause. Unittest binaries are compiled from CUBRID source — they live in the build tree, not the testcases repo.

**Does NOT:** edit/review test code, create tests, or run the full unittest regression across all modules.

## Before you start

- **CTP installed.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/bin/ctp.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Binaries available.** The `unittests_*` binaries come from a source build, not a build-URL install. If `$CUBRID/build_release/bin/unittests_*` is missing, ask for the source tarball URL and build it (see Run).
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` improves accuracy.
- Test guide: `unittest_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/unittest_guide.md (or `$CTP_HOME/../doc/unittest_guide.md` if CTP is checked out locally).

## Run

Work from a scratch dir so output never collides: `work=$(mktemp -d)`.

1. **Locate the binary.** `ls $CUBRID/build_release/bin/unittests_*`. If absent, build from source:
   ```bash
   wget <source_tarball_url> && tar xzf cubrid-*.tar.gz
   cd cubrid-*/ && sh build.sh -t 64 -m release -b build_release
   ls build_release/bin/unittests_*
   ```
2. **Pick the target.** Map the request to `unittests_<module>`. If ambiguous, list the binaries above and ask which one.
3. **Execute** with a timeout, capturing all output:
   ```bash
   timeout 600 $CUBRID/build_release/bin/unittests_<module> 2>&1 | tee "$work/run.log"; echo "exit=$?"   # 124 = timeout
   ```

## Verdict

Unittest binaries signal status in their **output text**, not the exit code — judge from the log:
```bash
grep -ci 'fail\|Unit tests failed' "$work/run.log"   # >0 → FAIL
grep -ci 'OK\|success'             "$work/run.log"   # 0  → FAIL (binary likely exited early)
```
**PASS** = no `fail`/`Unit tests failed` AND at least one `OK`/`success` (case-insensitive). **FAIL** = any failure marker, a timeout (exit 124), a missing success marker, or a crash → proceed to Failure analysis.

## Failure analysis

On FAIL, gather evidence then classify — don't guess:

1. **Failing lines** — `grep -i 'fail\|Unit tests failed' "$work/run.log"` to see which assertions failed.
2. **Crash / core dump** — `ls core* $CUBRID/core* 2>/dev/null`. A core means the binary *crashed*, which is a different (more serious) verdict than a failed assertion — report it as a crash.
3. **Early exit** — no `OK`/`success` at all usually means a segfault or a missing runtime dependency; check the tail of `$work/run.log` and stderr.

**Classify the failure (test-fix vs bug-report).** This is the decision the user actually needs — is the test wrong, or is CUBRID wrong?
- **test-fix**: the assertion encodes a stale expectation that an intentional code change made obsolete. The product is correct; the test needs updating.
- **bug-report**: a crash/core, or an assertion that proves CUBRID itself regressed. Raise it with the evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an intentional behavior change, prefer test-fix; if it describes this very failure or crash, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] unittests_<module>
  - Output: <key OK/success lines>
  - Summary: <what the binary tested>
```
**Fail:**
```
[FAIL] unittests_<module>
  - Failed assertions: <FAIL lines from output>
  - Crash: <yes/no — core dump found?>
  - Root cause: <diagnosis from the evidence>
  - Verdict: test-fix | bug-report  (<one-line justification>)
  - Suggestion: <fix the test | file a CUBRID bug | rebuild>
```

## Common pitfalls

- **Binary not found** → a build-URL install has no unittest binaries; they come only from a source build (`sh build.sh -t 64 -m release -b build_release`).
- **`fail` in unrelated output** → the grep is broad; confirm the matched line is a real test failure, not a log line containing the word.
- **No `OK` in output** → the binary exited early (segfault, missing dependency), not a normal failure — treat as a crash and inspect stderr.
- **Full regression instead of one binary** → that is a different job; `ctp.sh unittest -c $CTP_HOME/conf/unittest.conf` runs them all and is out of scope here.
