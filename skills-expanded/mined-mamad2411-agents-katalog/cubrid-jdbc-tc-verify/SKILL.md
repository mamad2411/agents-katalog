---
name: cubrid-jdbc-tc-verify
description: "Run one CUBRID JDBC testcase (a standard JUnit 4 class) on this machine, judge OK/NOK, and on failure diagnose the root cause. Use whenever someone wants to physically run a specific JDBC test and know whether it passes and why — Korean: \"jdbc tc 돌려봐\", \"jdbc 테스트 실행\", \"jdbc tc 수행\", \"패스하는지 확인\", \"검증해줘\", \"실패 원인 알려줘\"; English: \"run jdbc test\", \"execute jdbc tc\", \"verify\", \"check if it passes\". A CUBRID build URL alongside a JDBC test path is a strong signal — invoke this skill. NOT for: creating JDBC tests (use cubrid-jdbc-tc-create) or running the full JDBC regression suite."
---

# JDBC Testcase Verifier (CTP)

Run a single CUBRID JDBC testcase (a JUnit 4 class) through CTP, report OK/NOK, and — when it fails — diagnose *why*. "Verify" means all three: **run → judge → diagnose**.

CTP's `JdbcLocalTest` runner has **no single-case filter** — it compiles and runs *every* `.java` in the scenario dir. So to verify one TC, run it inside a **one-case temporary scenario** (default), falling back to a direct JUnit run when its dependencies are awkward to copy.

## Scope

**Does:** install a given CUBRID build, run one JDBC `Test*.java` class via CTP, read its OK/NOK, and on failure trace the cause with a fix recommendation.

**Does NOT:** edit/review/create tests, run the full suite, or bisect a batch across commits.

## Before you start

- **CTP installed.** Resolve `$CTP_HOME` (env → `~/CTP` → `~/cubrid-testtools/CTP`). Sanity check: `ls $CTP_HOME/bin/ctp.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES_PRIVATE` if set, else discover the `cubrid-testcases-private` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below. The testcase tree (`$TC/interface/JDBC/test_jdbc`) must be present.
- **Build URL.** A CUBRID build URL is required to install the binary under test. If not given, ask for it.
- Test guide: `jdbc_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/jdbc_guide.md (or `$CTP_HOME/../doc/jdbc_guide.md` if CTP is checked out locally).
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground diagnosis (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` sharpens the failure verdict.

## Run

Work from a scratch dir: `work=$(mktemp -d)`. Let `TREE=$TC/interface/JDBC/test_jdbc`.

1. **Install CUBRID** and verify it really worked (`run_cubrid_install` returns 0 even on failure):
   ```bash
   sh "$CTP_HOME/common/script/run_cubrid_install" <build_url> 2>&1 | tee "$work/install.log"
   grep '\[ERROR\]' "$work/install.log" && echo "install failed — stop & show these"
   source ~/.cubrid.sh && cubrid --version && cubrid service start
   ```
2. **Locate the class & its pattern** — `find "$TREE/src" -name '<Pattern>.java'`. Package `cubrid.jdbc.driver` → driver pattern; `com.cubrid.jdbc.test.spec.*` → spec pattern. Note its fully-qualified class name.
3. **Build a one-case scenario (default, A).** Copy the target plus the small, fixed dependency set for its pattern, preserving package directories:
   ```bash
   S="$work/scenario"; mkdir -p "$S/src" "$S/lib"
   cp -r "$TREE/lib/." "$S/lib/"; cp "$TREE/jdbc.properties" "$S/"      # CTP rewrites the live port
   # copy target preserving its src/<pkg>/ path, then its deps:
   #   driver pattern: src/cubrid/jdbc/{ConnectionProvider,SqlUtil,PropertiesUtil}.java
   #   spec pattern:   src/com/cubrid/jdbc/test/spec/{GeneralTestCase,ConnectionProvider}.java
   #                   + src/com/cubrid/jdbc/test/PropertiesUtil.java
   ```
   If the class pulls in more helpers than the standard set (compile error in step 4), either add the missing `.java` or switch to the C fallback below.
4. **Run via CTP** with an INI conf (CTP creates the DB, sets the broker port, rewrites `jdbc.properties`, compiles, and runs):
   ```bash
   printf '[common]\nscenario=%s\n' "$S" > "$work/jdbc.conf"
   "$CTP_HOME/bin/ctp.sh" jdbc -c "$work/jdbc.conf" 2>&1 | tee "$work/run.log"
   ```

**Fallback C (direct JUnit) — when deps are awkward to copy.** Compile the whole real tree once and run just the target class with JUnit:
```bash
cd "$TREE"
port=$(cubrid broker status -b | grep -vE 'OFF|off' | grep -E 'broker1|query_editor' | awk '{print $4}' | tail -1)
sed -i "s#jdbc.url=.*#jdbc.url=jdbc:cubrid:localhost:$port:demodb:::#" jdbc.properties   # PropertiesUtil reads ./jdbc.properties
javac -cp "lib/*:$CUBRID/jdbc/cubrid_jdbc.jar" -d "$work/bin" $(find src -name '*.java')
java -cp "$work/bin:lib/*:$CUBRID/jdbc/cubrid_jdbc.jar" org.junit.runner.JUnitCore <fully.qualified.ClassName> 2>&1 | tee "$work/run.log"
```

## Verdict

CTP path (A) writes results under `$CTP_HOME/result/jdbc/current_runtime_logs/`:
```bash
grep -E '\[TESTCASE\]|\[OK\]|\[NOK\]' "$CTP_HOME/result/jdbc/current_runtime_logs/feedback.log"
grep total_fail_case_count "$CTP_HOME/result/jdbc/current_runtime_logs/test_status.data"
```
Fallback C: read the JUnit tally from `$work/run.log` (`OK (N tests)` or `Tests run: N, Failures: F`).

`[OK]` for every method / `total_fail_case_count=0` (or JUnit `OK`) → **PASS**. Any `[NOK]`, failure, error, timeout, or crash → **FAIL**; go to Failure analysis. After the verdict, check for leftovers (`cubrid server status`) and offer cleanup.

## Failure analysis

On FAIL, gather evidence then classify — don't guess:

1. **Per-case detail** — `$CTP_HOME/result/jdbc/current_runtime_logs/run_case_details.log` (A) or `$work/run.log` (C). `AssertionError` = expected-vs-actual mismatch; `SQLException` = DB/driver error (note the error code); `ClassNotFoundException` / `Connection refused` = env, not a real failure.
2. **Server / broker logs** — `cat $CUBRID/log/server/*.err`, `ls $CUBRID/log/broker/*.err`.
3. **Core dumps** — `ls $CUBRID/core*` → a core means a server crash.
4. **Connection** — confirm broker up and conf's host/port/db match: `cubrid broker status -b`.

**Classify (test-fix vs bug-report)** — is the test wrong, or is CUBRID wrong?
- **test-fix** (the test's expectation is stale): the `AssertionError` reflects an *intentional* output/format change, or the test hard-codes an env detail that drifted. Update the test.
- **bug-report** (CUBRID regressed): a crash/core, a wrong result, an unexpected `SQLException`, or a driver fault. Raise it with the evidence.
- **Cross-check with JIRA** when available: if the CBRD issue describes an intentional change for this release, prefer test-fix; if it describes this very failure mode, prefer bug-report and cite the issue.

## Output format

**Pass:**
```
[PASS] TestClassName
  - Result: total_fail_case_count=0 (N methods OK)
  - Summary: <what the test verified>
```
**Fail:**
```
[FAIL] TestClassName
  - Result: <N NOK> (which method)
  - Failed method: <test1 | ...>
  - Root cause: <AssertionError | SQLException | crash | env>
  - Verdict: test-fix | bug-report  (<one-line justification>)
  - Key trace: <quoted stack-trace lines>
  - Suggestion: <fix the test | file a CUBRID bug | fix env>
```

## Common pitfalls

- **Compile error in the temp scenario** → a helper wasn't copied; add the missing `.java` or use fallback C.
- **`Connection refused` / `Cannot connect to a broker`** → `cubrid service start`; verify `cubrid broker status -b`.
- **`ClassNotFoundException: cubrid.jdbc.driver.CUBRIDDriver`** → the JDBC jar isn't on the classpath; CTP copies `$CUBRID/jdbc/cubrid_jdbc.jar` into the scenario `lib/` automatically (A), or add it explicitly (C).
- **Zero tests run** → the class name doesn't start with `Test` (Ant) or the method lacks `@Test` / the substring `test` (JdbcLocalTest).
