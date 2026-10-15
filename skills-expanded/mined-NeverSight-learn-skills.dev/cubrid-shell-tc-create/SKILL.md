---
name: cubrid-shell-tc-create
description: "Create, draft, or scaffold a new CUBRID CTP shell testcase (.sh) from scratch — for a CBRD bug fix or feature. Use this whenever someone says \"shell tc 만들어줘\", \"shell tc 초안 작성해줘\", \"create shell tc\", \"draft shell test\", \"새 shell testcase\", or \"create draft shell tc for CBRD-XXXXX\", even if they don't say the word \"testcase\". They usually give a CBRD number, the behavior to test, and sometimes a target release dir. NOT for: reviewing/debugging existing tests, running tests, CTP configuration, HA/replication tests (use cubrid-ha-* skills), or SQL/JDBC/CCI testcases."
---

# Shell Testcase Creator (CTP)

Generate a CUBRID CTP shell testcase that passes review on the first try. A good testcase is one self-contained `.sh` following a five-phase flow — **init → setup → test → verify → cleanup** — that CTP runs, collects, and regression-tracks.

## Scope

**Produces:** the entry script (owns the full lifecycle), optional helper scripts and embedded C clients (same `cases/` dir), correct directory paths.

**Does NOT produce:** answer files (CTP generates these by running in `init answer` mode — never hand-write them), CTP framework changes, CI config, SQL/MEDIUM/JDBC tests, or HA/replication tests (route those to `cubrid-ha-*`).

## Before you start

- **CTP must be installed.** Expect it at `$CTP_HOME`, `~/CTP`, or `~/cubrid-testtools/CTP`. Sanity check: `ls $CTP_HOME/shell/init_path/init.sh`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **Testcase repo.** Resolve its root without a hardcoded home path: use `$CUBRID_TESTCASES_PRIVATE_EX` if set, else discover the `cubrid-testcases-private-ex` checkout from the current dir (`git rev-parse --show-toplevel` or search upward), else ask the user. Call it `$TC` below.
- **JIRA context (optional).** If the request names a `CBRD-XXXXX`, run `cubrid-jira search CBRD-XXXXX` first to ground the test in the issue's real reproduction and expected behavior (reuse if already fetched). If the CLI isn't installed, skip — but installing `cubrid-jira` notably improves accuracy.

## Directory convention

The path is how CTP identifies and categorizes a test. The directory name and the script filename **must match** (`test_name/cases/test_name.sh`).

```
# Bug fix:   shell/_06_issues/_{yy}_{1|2}h/cbrd_xxxxx/cases/cbrd_xxxxx.sh
# Feature:   shell/_{no}_{release_code}/{feature_group}/cbrd_xxxxx_{kw}/cases/cbrd_xxxxx_{kw}.sh
```

`{yy}` = 2-digit year, `{1|2}h` = first/second half (issue creation date). Multiple tests for one issue get a suffix: `cbrd_xxxxx_1`, `cbrd_xxxxx_{keyword}`. Full rules and the excluded-list mechanism: see `@references/directory_guide.md`.

## Lifecycle contract

Every entry script follows this skeleton. Missing a step fails review.

```bash
#!/bin/bash
# CBRD-XXXXX: one-line statement of what this verifies.
# Setup → action → expected outcome, in 1-2 lines.

. $init_path/init.sh
init test

dbname=db_xxxxx

# --- Setup ---
cubrid_createdb $dbname
cubrid server start $dbname

# --- Test --- (capture output to logs; keep SQL inline via heredocs)
csql -udba "$dbname" > result.log 2>&1 <<'EOF'
CREATE TABLE t1 (id INT PRIMARY KEY);
EOF

# --- Verify ---
if [ <condition> ]; then write_ok; else write_nok "$result_log"; fi

# --- Cleanup (reverse order) ---
cubrid server stop $dbname
cubrid deletedb $dbname
rm -f *.log csql.*
finish
```

### Why each phase matters (not just ritual)

- `. $init_path/init.sh` loads every CTP helper; `init test` resets prior state and sets up logging. Without them nothing else resolves.
- Use `#!/bin/bash` (the house majority). Keep the body portable anyway — reach for a bashism only when it earns its place.
- `finish` reverts every conf change, stops services, and frees broker shared memory. It must be the **last** call, and **every** exit path (including early `write_nok` returns) must reach it — otherwise the next test inherits dirty state.
- Every code path must end at exactly one of `write_ok` / `write_nok`, then `finish`.

## Essential helpers (use these, not raw commands)

Raw equivalents fail review because these handle cross-version/charset quirks and auto-revert.

| Use | Instead of | Why |
|---|---|---|
| `cubrid_createdb $db` | `cubrid createdb $db` | charset/locale compatibility across versions |
| `change_db_parameter "k=v"` / `change_broker_parameter "k=v"` | editing `.conf` | auto-reverted by `finish` |
| `xgcc -o bin src.c` | `gcc ... -lcascci` | auto `-I/-L $CUBRID`, `-lcascci -lpthread`, 32/64-bit + OS detection |
| `xkill <pattern>` | `kill -9` / `pkill` | user-scoped, cross-platform |
| `write_ok` / `write_nok [file]` | echoing PASS/FAIL | CTP result tracking |

Full reference (output normalization, SQL asserts, ports, platform macros): `@references/init_sh_helpers.md`.

## Writing rules (principles, not ritual)

- **Inline SQL** via single-quoted heredocs (`<<'EOF'`) so the shell doesn't expand `$`/backticks in your SQL. Never split SQL into separate `.sql` files.
- **Quote variables** (`"$db"`), space your tests (`[ "$x" -eq 0 ]`).
- **Error handling:** check exit codes for things that can fail (`cubrid server start`, `csql`, compiles). Pattern: `cmd || { write_nok "reason"; <cleanup>; finish; exit 0; }`.
- **No hardcoded paths** (`/tmp`, `/home`, `/opt`); use `$init_path`, `$CUBRID`, cwd, `$TMPDIR`.
- **Bounded loops only** — poll with a counter, never `while true`. Sleep 0-2s is fine; >10s must become polling.
- **Track every background PID** (`cmd & pid=$!`) with a matching `wait`/`xkill`; leave no orphans.
- **Clean up on every exit path:** `rm -f *.log csql.* <binaries>` before `finish`, in early-exit branches too.
- **Platform exclusion:** put the macro (`WINDOWS_NOT_SUPPORTED` / `LINUX_NOT_SUPPORTED`) *before* sourcing init.sh.

## House idioms (quick recipes)

These match what the corpus and reviewers expect. Details + a full crash-repro walkthrough: `@references/crash_cas_patterns.md`.

- **Broker is `broker1`** (not `query_editor`). Live port: `port=\`cubrid broker status -b | grep broker1 | awk '{print $4}'\``.
- **CAS process / PID:** `ps -f -u $USER | grep -v grep | grep broker1_cub_cas | awk '{print $2}'`.
- **Force a single CAS** (for CAS-reuse / crash repros): `change_broker_parameter "MIN_NUM_APPL_SERVER=1"` and `"MAX_NUM_APPL_SERVER=1"`, then `cubrid broker restart`.
- **Coredump check:** clean a baseline, then count after the action — `find "$CUBRID" ./ \( -name "core.*" -o -name "*coredump*" \) | wc -l` before vs. after; assert no new cores. For crash bugs also assert the CAS PID is unchanged.
- **Compile + run an embedded CCI C client:** `xgcc -o client client.c` then `./client <args>`; commit the `.c` next to the `.sh`.

## Verify before claiming done

After authoring, prove the testcase actually runs — don't just eyeball it.

1. **Pod-first:** if a k8s test-shell pod is reachable, run it there for real (install a build via CTP `run_cubrid_install`, inject the TC, run `ctp.sh shell`, read `feedback.log` for `OK`/`NOK`). This is ground truth.
2. **Local fallback** (no pod is a clean, expected path): `bash -n` the script, `xgcc`-compile any `.c`, and run via local CTP if available.

Procedure detail: `@references/verification_protocol.md`.

## Self-review checklist

- Lifecycle complete? (`init.sh`, `init test`, one of `write_ok`/`write_nok`, `finish` last)
- CTP helpers over raw commands? (`cubrid_createdb`, `change_*_parameter`, `xgcc`, `xkill`)
- SQL inline via single-quoted heredoc? No hardcoded paths? Bounded loops? No orphan PIDs?
- Cleanup (`rm -f *.log csql.* <bin>`) on **every** exit path, before `finish`?
- Crash test: coredump baseline taken and CAS PID compared?
- Dir name == filename? Correct `_{yy}_{1|2}h` bucket?
- Verified (pod-first, else local)?

## Examples & references

- `@examples/` — working patterns: `basic_entry.sh`, `config_change.sh`, `utility_test.sh`, `output_comparison.sh`, and `cci_crash_repro.sh` (+ `.c`) for the CAS-coredump / CCI-client pattern.
- `@references/directory_guide.md`, `@references/init_sh_helpers.md`, `@references/crash_cas_patterns.md`, `@references/verification_protocol.md`.
- Test guide: `shell_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/shell_guide.md (or `$CTP_HOME/../doc/shell_guide.md` if CTP is checked out locally).
