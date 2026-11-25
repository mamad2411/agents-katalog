---
name: cubrid-unittest-tc-create
description: "Create, draft, or scaffold a new CUBRID CTP unittest — a low-level C/C++ unit test compiled from CUBRID source. Use this whenever someone says \"unittest tc 만들어줘\", \"unit test 작성\", \"새 유닛테스트\", \"C unit test 추가\", \"create unittest for CUBRID\", or \"draft unit test\", even if they don't say \"testcase\". NOT for: CCI tests (use cubrid-cci-tc-create), shell tests (use cubrid-shell-tc-create), JDBC tests (use cubrid-jdbc-tc-create), reviewing/running existing tests, or CTP config."
---

# CUBRID Unittest Creator (CTP)

Generate a CUBRID CTP unittest that passes on the first try. A unittest is a self-contained C/C++ program compiled from CUBRID source that exercises an internal component directly (no broker, no server), prints pass/fail to stdout, and is discovered and judged by CTP's unittest runner.

## Scope

**Produces:** the test source (`test_<module>.c`/`.cpp`) under the CUBRID source tree, plus the `CMakeLists.txt` entry that builds and installs the binary so CTP can find it.

**Does NOT produce:** CTP framework changes, CI config, server/broker-dependent tests, or CCI/shell/JDBC/SQL tests (route those to the matching `cubrid-*-tc-create` skill). Unittests test pure logic — anything needing a running server is out of scope.

## Before you start

- **CTP must be installed.** Expect it at `$CTP_HOME`, `~/CTP`, or `~/cubrid-testtools/CTP`. Sanity check: `ls $CTP_HOME/bin/ctp.sh $CTP_HOME/conf/`. If absent, stop and tell the user to install it (`git clone https://github.com/CUBRID/cubrid-testtools.git && cp -rf cubrid-testtools/CTP ~/`).
- **CUBRID source tree** must be present — unittests are compiled from it, not from a testcases repo. Confirm the `unit_tests/` and `src/` directories exist before writing.
- **JIRA context (optional).** If a `CBRD-XXXXX` is referenced, run `cubrid-jira search CBRD-XXXXX` first to ground the work (reuse if already fetched). If the CLI isn't installed, skip — but installing cubrid-jira improves accuracy.

## Directory convention

Source lives in the CUBRID source repo; the binary must install to `bin/` so CTP discovers it by the `unittests_*` prefix.

```
# Source:  cubrid/unit_tests/<module>/test_<module>.cpp   (shared helpers in unit_tests/common/)
#     or:  cubrid/src/<module>/test_<name>.{c,cpp}
# Binary:  cubrid/build_release/bin/unittests_<module>     (also build_debug/)
```

Binary name is always `unittests_<module>` — plural, `unittests_` prefix, one binary per logical module. CTP discovers it via `$CUBRID/build_release/bin/unittests_*`.

## Lifecycle contract

CTP runs each binary and judges it by **scanning stdout** — exit code is ignored. The judgment is literally:

```bash
# PASS iff: no "fail"/"Unit tests failed" (case-insensitive) AND at least one "OK"/"success"
if [ `grep -i 'fail\|Unit tests failed' "$unittestlog" | wc -l` -eq 0 \
  -a `grep -i 'OK\|success' "$unittestlog" | wc -l` -ne 0 ]; then IS_SUCC=true; fi
```

So every binary's `main` must:

1. Run its test functions, counting failures.
2. On all-pass: print a line containing `OK` or `success` (e.g. `printf("All tests passed. OK\n")`).
3. On any failure: print `FAIL`/`fail` per failing assertion — these lines make CTP record FAIL.
4. Print to **stdout**, not stderr; CTP reads stdout only.

Miss the `OK`/`success` line and a passing run is still recorded as FAIL.

## Essential helpers (use these, not ad-hoc checks)

Define assertion macros that increment a `failed` counter and print a `FAIL:` line carrying the expected/actual values — that single line satisfies the FAIL contract and gives a readable diff. The example files ship ready-to-copy macros:

| Use | For | Why |
|---|---|---|
| `ASSERT_EQ(a, b, msg)` | integer/scalar equality | prints `FAIL: msg (expected, got)`, bumps `failed` |
| `ASSERT_STR_EQ(a, b, msg)` | C string equality | same, with `strcmp` |
| `CHECK(cond, msg)` (C++) | any boolean condition | `std::cout` variant |

Full macro bodies and a working `main`: see `@examples/test_simple_module.c` and `@examples/test_simple_module.cpp`. Copy one, rename, fill in tests.

## Writing rules (principles, not ritual)

- **No server, no broker, no network.** Unittests link CUBRID internals and test pure logic; if it needs a running server it isn't a unittest.
- **No external deps** beyond CUBRID internal headers — the binary must build and run standalone.
- **Print the verdict on stdout:** `OK`/`success` on full pass, `fail` per failed assertion. This is the only thing CTP reads.
- **One logical module per binary**, named `unittests_<module>`.
- **No hardcoded paths** (`/tmp`, `/home`, absolute build dirs). If a test needs scratch space, use a `mktemp`-derived dir or the cwd, and clean it up.
- **Build via** `sh build.sh -t 64 -m release -b build_release` (or `build_debug`); the binary lands in `build_*/bin/`.

## House idioms (quick recipes)

- **Wire the build** in `CMakeLists.txt` so the binary installs to `bin/`:

  ```cmake
  add_executable(unittests_mymodule
      unit_tests/mymodule/test_mymodule.cpp
      src/mymodule/mymodule.c)            # the module under test
  target_include_directories(unittests_mymodule PRIVATE src/include)
  target_link_libraries(unittests_mymodule cubrid_static)
  install(TARGETS unittests_mymodule DESTINATION bin)
  ```

- **Match an existing pattern.** Look at neighbors before inventing: `unittests_area` (extent mgmt), `unittests_bit` (bit ops), `unittests_lf` (lock-free structures), `unittests_snapshot` (MVCC). Mirror the closest one's structure and output style.

## Verify before claiming done

Don't eyeball it — prove it compiles and that CTP would judge it PASS.

1. **Compile** the test into the tree: `sh build.sh -t 64 -m release -b build_release` (or just compile the one target). Fix until clean.
2. **Run the binary** and capture stdout: `build_release/bin/unittests_<module> | tee out.log`.
3. **Apply CTP's own rule** to `out.log`: confirm zero `fail`/`Unit tests failed` lines AND at least one `OK`/`success` line. If the run should fail, confirm a `fail` line appears.
4. If a CTP unittest runner is reachable, run through it for ground truth.

## Self-review checklist

- Prints `OK`/`success` on full pass, and `fail` per failing assertion — on **stdout**?
- Binary named `unittests_<module>` and installed to `bin/` via `CMakeLists.txt`?
- No server/broker/network dependency? No external libs beyond CUBRID headers?
- No hardcoded paths? Scratch (if any) via `mktemp`/cwd and cleaned up?
- One logical module per binary?
- Compiled clean and the produced stdout actually satisfies CTP's PASS rule?

## Examples & references

- `@examples/test_simple_module.c` — minimal C unittest: assertion macros + `OK`-on-pass `main`.
- `@examples/test_simple_module.cpp` — minimal C++ unittest (same shape, `std::cout`).
- Test guide: `unittest_guide.md` — https://github.com/CUBRID/cubrid-testtools/blob/develop/doc/unittest_guide.md (or `$CTP_HOME/../doc/unittest_guide.md` if CTP is checked out locally).
- `$CUBRID/build_release/bin/unittests_*` and the CUBRID `unit_tests/` source dir — existing binaries to model.
