---
name: cubrid-cci-tc-create
description: "Create, draft, or scaffold a new CUBRID CTP CCI testcase (shell + C source, optionally an answer file) from scratch — for a CBRD bug fix or feature exercising the C Client Interface (libcascci). Use this whenever someone says \"cci tc 만들어줘\", \"cci 테스트케이스 작성\", \"새 cci 테스트케이스\", \"create cci testcase\", or \"draft cci test for CBRD-XXXXX\", even if they don't say the word \"testcase\". They usually give a CBRD number, the CCI behavior to test, and sometimes a target category. NOT for: cci_compatibility tests (use cubrid-cci-compatibility-tc-create), JDBC tests (use cubrid-jdbc-tc-create), plain shell tests (use cubrid-shell-tc-create), or HA/replication tests (use cubrid-ha-* skills)."
---

# CCI Testcase Creator (CTP)

Generate a CUBRID CTP CCI testcase that passes review on the first try. A CCI test exercises CUBRID's C client driver (`libcascci`): a `.sh` entry script drives a compiled `test.c` against a running broker, and CTP collects and regression-tracks the result. There are two shapes — **simple** (output compared to a `.answer` file) and **issue** (explicit pass/fail check).

## Scope

**Produces:** the entry `.sh` (owns the full lifecycle), the `test.c` client, and — simple pattern only — the `.answer` file, in the right `cases/` dir with correct paths.

**Does NOT produce:** CTP framework changes, CI config, cci_compatibility tests (route to `cubrid-cci-compatibility-tc-create`), JDBC/SQL/MEDIUM tests, or HA/replication tests (route to `cubrid-ha-*`).

## Before you start

- **CTP must be installed.** Expect it at `$CTP_HOME`, `~/CTP`, or `~/cubrid-testtools/CTP`. Sanity check: `ls $CTP_HOME/shell/init_path/init.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES_PRIVATE` if set, else discover the `cubrid-testcases-private` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing cubrid-jira improves accuracy.

## Directory convention

The path is how CTP identifies and categorizes a test. The directory name and the `.sh` filename **must match** (`test_name/cases/test_name.sh`). CCI tests live under `$TC/interface/CCI/shell/_20_cci/`.

```
# Feature:  _20_cci/<category>/<test_name>/cases/<test_name>.sh (+ test.c [+ <test_name>.answer])
# Bug fix:  _20_cci/_12_issue/<bug_id>/cases/<bug_id>.sh (+ test.c)
```

Bug-fix dirs use `cbrd_xxxxx` or `bug_bts_xxxxx` naming. Category dirs include `_01_simple` (API sanity), `_03_func`, `_06_bind`, `_07_query`, `_12_issue` (bug fixes), `_14_ENUM`, `_15_Cursor`, `_28_features_84x`, and more — pick the one matching the feature area, or `_12_issue` for a bug fix. Full list and the `.answer`-only rule: browse `$TC/interface/CCI/shell/_20_cci/`.

## Lifecycle contract

Every entry script follows this skeleton. Missing a step fails review.

```bash
#!/bin/bash                       # always bash, not /bin/sh
. $init_path/init.sh              # loads every CTP helper
init test                         # resets prior state, sets up logging
set -x

# --- Setup ---
create_ccidb                      # simple: standard ccidb + server (or cubrid_createdb $db for issue)
cubrid broker start

# --- Build + run client ---
xgcc -o test test.c               # CTP wrapper auto-resolves -I/-L $CUBRID, -lcascci, arch
port=`cubrid broker status -b | grep broker1 | awk '{print $4}'`
./test "$port" > "${case_name}.output" 2>&1

# --- Verify (pick ONE) ---
compare_result_between_files "${case_name}.output" "${case_name}.answer"  # simple
# if grep -q "EXPECTED" "${case_name}.output"; then write_ok; else write_nok; fi  # issue

# --- Cleanup (reverse order) ---
cubrid server stop ccidb; cubrid deletedb ccidb   # only if the test created it
rm -f *.output *.log test
finish                            # MUST be last; reverts conf, stops services, frees broker shm
```

**Why each phase matters:** `init.sh` + `init test` make every helper and `$case_name` resolve; without them nothing works. Every code path must end at exactly one of `compare_result_between_files` / `write_ok` / `write_nok`, then `finish` — and **every** exit path (early failures too) must reach `finish`, or the next test inherits dirty state.

## Essential helpers (use these, not raw commands)

Raw equivalents fail review because these handle version/charset/arch quirks and auto-revert.

| Use | Instead of | Why |
|---|---|---|
| `create_ccidb` | `cubrid createdb ccidb` + schema | builds the standard `ccidb` with schema and starts the server |
| `cubrid_createdb [opts] $db` | `cubrid createdb $db` | charset/locale compatibility across versions |
| `xgcc -o test test.c` | `gcc ... -lcascci` | auto `-I/-L $CUBRID`, `-lcascci -lpthread`, 32/64-bit + OS detection |
| `get_broker_port_from_shell_config` | hardcoded port | reads the live broker port from CTP config (issue pattern) |
| `compare_result_between_files a b` | manual `diff` | compares output to answer and writes ok/nok automatically |
| `write_ok` / `write_nok [file]` | echoing PASS/FAIL | CTP result tracking |

Auto-set vars: `$case_name` (test name), `$isdbexist` (1 if `ccidb` pre-existed, else 0 — gate cleanup on it). For manual builds: `gcc -o test test.c -I${CUBRID}/include -L${CUBRID}/lib -lcascci` (add `-m32` for 32-bit CUBRID, `-lpthread` for thread-safe). CCI API header: `${CUBRID}/include/cas_cci.h`.

## Writing rules (principles, not ritual)

- **Two patterns, don't mix:** *simple* = `create_ccidb` + `xgcc` + `.answer` + `compare_result_between_files`; *issue* = `cubrid_createdb` + explicit `gcc` + `grep` + `write_ok`/`write_nok`.
- **`test.c` checks every return** — `cci_connect`/`cci_prepare`/`cci_execute` return `<0` on error; print `error.err_msg`, then `cci_close_req_handle`/`cci_disconnect` before returning nonzero. Leaked handles or unchecked returns fail review.
- **No hardcoded ports** — derive from `cubrid broker status -b ... broker1` (simple) or `get_broker_port_from_shell_config` (issue).
- **No hardcoded paths** (`/tmp`, `/home`, `/opt`); use `${CUBRID}/include`, `${CUBRID}/lib`, cwd, `$TMPDIR`.
- **Quote variables** (`"$port"`, `"$db"`); space your tests (`[ "$x" -eq 0 ]`).
- **Clean up on every exit path:** stop/delete any DB the test created (gate on `$isdbexist`), `rm -f *.output *.log test` before `finish`.

## House idioms (quick recipes)

- **Broker is `broker1`** (not `query_editor`). Live port: `port=\`cubrid broker status -b | grep broker1 | awk '{print $4}'\``.
- **Minimal CCI client:** `cci_connect("127.0.0.1", port, "ccidb", "public", "")` → `cci_prepare` → `cci_execute` → `cci_cursor(req,1,CCI_CURSOR_FIRST,&err)` → `cci_fetch` → `cci_get_data(req,col,CCI_A_TYPE_STR,&val,&ind)` → `printf`. See `@examples/cci_simple_test.c`.
- **Data-type fetch constants:** `CCI_A_TYPE_STR` (`char*`), `CCI_A_TYPE_INT` (`int`), `CCI_A_TYPE_BIGINT` (`int64_t`), `CCI_A_TYPE_DOUBLE` (`double`), `CCI_A_TYPE_DATE` (`T_CCI_DATE`).
- **Bind parameters:** `cci_bind_param(req, idx, a_type, val, u_type, flag)` before `cci_execute`.
- **URL connect** (with options): `cci_connect_with_url(url, user, pw)`.

## Verify before claiming done

After authoring, prove the testcase actually runs — don't just eyeball it.

1. **Pod-first:** if a k8s test-shell pod is reachable, run it there for real (install a build via CTP `run_cubrid_install`, inject the TC, run `ctp.sh shell`, read `feedback.log` for `OK`/`NOK`). This is ground truth.
2. **Local fallback** (a clean, expected path): `bash -n` the script, `xgcc`-compile `test.c` against a built `$CUBRID`, and run via local CTP if available.

## Self-review checklist

- Lifecycle complete? (`init.sh`, `init test`, one verify call, `finish` last)
- CTP helpers over raw commands? (`create_ccidb`/`cubrid_createdb`, `xgcc`, port helpers)
- One pattern, not mixed? `.answer` present iff simple pattern?
- `test.c` checks every CCI return and closes handles before exit?
- No hardcoded ports or paths? Variables quoted?
- Cleanup (DB gated on `$isdbexist`, `rm -f *.output *.log test`) on **every** exit path, before `finish`?
- Dir name == filename? Correct category (or `_12_issue` for a bug fix)?
- Verified (pod-first, else local)?

## Examples & references

- `@examples/cci_simple_test.sh` + `@examples/cci_simple_test.c` + `@examples/cci_simple_test.answer` — output-comparison (simple) pattern.
- `@examples/cci_issue_test.sh` + `@examples/cci_issue_test.c` — explicit pass/fail (issue) pattern.
- `$TC/interface/CCI/shell/_20_cci/` — existing CCI testcases by category.
- `$CTP_HOME/shell/init_path/init.sh` — CTP core helpers. CCI API header: `${CUBRID}/include/cas_cci.h`.
- Test guide: `cci_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/cci_guide.md (or `$CTP_HOME/../doc/cci_guide.md` if CTP is checked out locally).
