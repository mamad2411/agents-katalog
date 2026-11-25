---
name: qt-qml-test-run
version: 1.0.0
description: Run and triage Qt Quick Test and CTest suites, drive them headless in CI, and read failures.
author: matrixx0070
tags: [qt6, qml, ctest, ci, triage]
capabilities: []
---

## When to use

Use this when a QML test suite already exists and you need to execute it, run it headless in CI, and interpret PASS/FAIL/QWARN output down to the failing function and data row. Covers both `qmltestrunner` and CTest-driven runs.

**Not for:** authoring the test files, `TestCase`, or `SignalSpy` — see `qt-qml-test`. For runtime performance analysis (jank, binding storms, startup) — see `qt-qml-profiler`.

## Method

1. Locate the runner. **Decision point:** if the project builds a `QUICK_TEST_MAIN` binary, run that binary; otherwise use the SDK's `qmltestrunner` with `-input <dir-or-file>`.
2. Ensure imports resolve before blaming the tests: export `QML2_IMPORT_PATH` (or `QML_IMPORT_PATH`) to include the built module directory.
3. **Decision point:** if you are on a headless machine or CI, set `QT_QPA_PLATFORM=offscreen` so window-dependent tests run without a display; otherwise use the native platform.
4. Prefer CTest for suite orchestration when the project uses `qt_add_test`/`add_test`; run `ctest --output-on-failure` from the build dir.
5. **Decision point:** if only some tests are relevant, narrow with `ctest -R <regex>`; after a red run, iterate with `ctest --rerun-failed --output-on-failure`; when a single test misbehaves, re-run it directly with `-V` (or the binary with `-v2`).
6. Read the output top-down: `PASS` lines confirm, `FAIL!` lines name `suite::test_function(tag)` with file:line, and `QWARN` lines flag runtime warnings (often binding loops) that do not fail the run by themselves.
7. **Decision point:** if warnings are drowning the signal, raise or cap with `-maxwarnings <n>`; if a binding-loop `QWARN` appears, treat it as a real defect to fix even when the assertion passed.
8. For CI artifacts, emit machine-readable results with `-o <file>,junitxml` (or `-o <file>,xml`) and let the CI collect the JUnit file.

## Example

```bash
# Headless environment for CI
export QT_QPA_PLATFORM=offscreen
export QML2_IMPORT_PATH="$PWD/build/qml:$QML2_IMPORT_PATH"

# 1) Standalone runner against a directory of tst_*.qml
qmltestrunner -input tests/qml -maxwarnings 50

# 2) Via CTest from the build directory
cmake --build build
ctest --test-dir build --output-on-failure -R qml

# 3) Re-run just the failures verbosely
ctest --test-dir build --rerun-failed --output-on-failure -V

# 4) JUnit XML for CI
qmltestrunner -input tests/qml -o results.xml,junitxml
```

```
********* Start testing of qml_tests *********
PASS   : SliderTests::test_range(min)
FAIL!  : SliderTests::test_range(max) value should clamp to range
   Actual   (): 99
   Expected (): 100
   Loc: [tst_slider.qml(28)]
QWARN  : SliderTests::test_click_emits QML Slider: Binding loop detected for property "value"
Totals: 5 passed, 1 failed, 0 skipped, 0 blacklisted
```

## Pitfalls

- **Unresolved imports read as test failures.** A missing `QML2_IMPORT_PATH` surfaces as `module "X" is not installed`; fix the path before debugging assertions.
- **No display in CI.** Without `QT_QPA_PLATFORM=offscreen` the run aborts with "could not connect to display"; window-shown tests need it.
- **Ignoring QWARN.** Binding-loop and type warnings are printed as `QWARN` and do not fail the suite by default — they are still real bugs.
- **CTest hides output.** A bare `ctest` prints only pass/fail; you need `--output-on-failure` (or `-V`) to see the QtTest messages.
- **Regex over-match.** `ctest -R` matches the CTest test *name*, not the QML function; scope names carefully or you will run the wrong set.
- **Stale build.** Running the test binary without rebuilding after editing `.qml` files tests old copies when files are compiled/embedded via `qt_add_qml_module`.

## Output format

```
Runner: qmltestrunner | <QUICK_TEST_MAIN binary> | ctest
Env: QT_QPA_PLATFORM=offscreen ; QML2_IMPORT_PATH=<...>
Command: <exact invocation>
Result: <N passed / M failed / K skipped>
Failures:
  - <Suite>::<test_fn>(<tag>)  <file>:<line>  actual=<> expected=<>
Warnings (QWARN):
  - <message>  [binding-loop? y/n]
Artifact: <results.xml (junitxml)>
```

## Reference

- `qmltestrunner` is the standalone Qt Quick Test runner (from `Qt6::QuickTest`); key flags: `-input <path>` (dir or single `tst_*.qml`), `-maxwarnings <n>`, `-o <file>,<format>` where format is `txt`, `xml`, or `junitxml`.
- A `QUICK_TEST_MAIN(name)` build produces its own executable that behaves like `qmltestrunner`, scanning for `tst_*.qml`.
- CTest integration comes from `qt_add_test(...)` / `add_test(NAME ... COMMAND ...)`; useful CTest options: `--output-on-failure`, `-R <regex>`, `-E <regex>` (exclude), `--rerun-failed`, `-V`/`-VV` (verbose), `-j <n>` (parallel), `--test-dir <build>`.
- Headless/CI env: `QT_QPA_PLATFORM=offscreen` (or `minimal`) avoids needing an X/Wayland display; `QML2_IMPORT_PATH` / `QML_IMPORT_PATH` add module search dirs.
- Output tokens: `PASS`, `FAIL!`, `XFAIL`, `SKIP`, `QWARN`, `QDEBUG`; totals line reports passed/failed/skipped/blacklisted.
- Binding-loop warnings appear as `QWARN ... Binding loop detected for property "<p>"` during a test; they indicate a cyclic property dependency and should be fixed at the QML source, not suppressed.
- Verified against Qt 6.2–6.8; `qmltestrunner` ships in the Qt bin directory (e.g. `$QTDIR/bin/qmltestrunner`).
