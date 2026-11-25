---
name: qt-qml-test
version: 1.0.0
description: Write QML unit tests with Qt Quick Test using TestCase, SignalSpy, and data-driven functions.
author: matrixx0070
tags: [qt6, qml, testing, qtquicktest]
capabilities: []
---

## When to use

Use this when you need to author QML unit tests that exercise Qt Quick components, their properties, signals, and interactions from the QML side. Write one `.qml` test file per component under test and let Qt Quick Test discover the `test_*` functions.

**Not for:** running or triaging an existing suite and reading failures — see `qt-qml-test-run`. For diagnosing jank, binding storms, or slow startup at runtime — see `qt-qml-profiler`.

## Method

1. Create a test file named `tst_<component>.qml` and add `import QtTest` plus the module that exposes the component under test.
2. Add a root `TestCase { }` element and set its `name` property to a unique identifier (the harness uses it to label results).
3. Decide how the component enters the scene. **Decision point:** if the component is stateless and cheap, instantiate it inline with a `Component { }` + `createTemporaryObject()`; if it needs the running window (mouse/key focus), give the `TestCase` a `width`/`height` and use `when: windowShown`.
4. Write each check as a function named `test_something()`. **Decision point:** if you assert a single truth use `verify()`/`compare()`; if the value settles asynchronously (bindings, animations, timers) use `tryCompare()`/`tryVerify()` so the harness spins the event loop until timeout.
5. Observe signals with a `SignalSpy { }` element bound to `target` and `signalName`; assert `spy.count` after the triggering action, or `spy.wait()` for async emission.
6. **Decision point:** if a test repeats over inputs, add a matching `function test_something_data()` returning table rows and read `data` in `test_something(data)`; otherwise keep it a plain function.
7. Add fixtures with `init()`/`cleanup()` (per function) and `initTestCase()`/`cleanupTestCase()` (once per file). **Decision point:** reset shared state in `init()`; do one-time expensive setup in `initTestCase()`.
8. Register the test with `qt_add_qml_module` so imports resolve, and set `TESTED_COMPONENT` where you need the runner pointed at a specific element.

## Example

```qml
import QtQuick
import QtTest

TestCase {
    id: testCase
    name: "SliderTests"
    width: 200; height: 50
    when: windowShown

    Component {
        id: sliderComp
        Slider { from: 0; to: 100; value: 0 }
    }

    SignalSpy {
        id: valueSpy
        signalName: "valueChanged"
    }

    function init() { valueSpy.clear() }

    function test_range_data() {
        return [
            { tag: "min", input: 0,   expected: 0 },
            { tag: "mid", input: 50,  expected: 50 },
            { tag: "max", input: 100, expected: 100 },
        ];
    }

    function test_range(data) {
        let s = createTemporaryObject(sliderComp, testCase);
        valueSpy.target = s;
        s.value = data.input;
        compare(s.value, data.expected, "value should clamp to range");
        tryCompare(valueSpy, "count", 1);
    }

    function test_click_emits() {
        let s = createTemporaryObject(sliderComp, testCase);
        valueSpy.target = s;
        mousePress(s, s.width / 2, s.height / 2);
        keyClick(Qt.Key_Right);
        tryVerify(function() { return valueSpy.count > 0; });
        verify(fuzzyCompare(s.value, s.value, 0.001));
    }
}
```

## Pitfalls

- **Bad function names.** Only functions matching `test_*()` are collected; `init`, `cleanup`, `initTestCase`, `cleanupTestCase`, and `*_data` are reserved hooks and are not run as tests.
- **Missing `when: windowShown`.** `mousePress`/`keyClick` and focus-dependent assertions silently do nothing until the window is shown; gate interactive tests on it.
- **Leaking objects.** Prefer `createTemporaryObject()`; objects from `createObject()` persist across tests and pollute state.
- **Racing on async.** Using `compare()` on a value set by a binding or animation flakes; switch to `tryCompare()`/`tryVerify()` which poll up to the timeout.
- **Stale SignalSpy.** Reassigning `target` does not reset `count`; call `spy.clear()` in `init()`.
- **Data-row tag collisions.** Duplicate `tag` values in a `_data` table make failures ambiguous; keep tags unique.

## Output format

```
tst_<component>.qml
  TestCase name: <Name>
  Functions:
    - test_<a>()            [+ test_<a>_data() if data-driven]
    - test_<b>()
  Fixtures: init/cleanup [+ initTestCase/cleanupTestCase]
  Spies: <SignalSpy targets>
CMake: qt_add_qml_module(<target> ...) ; TESTED_COMPONENT <Element>
Entry: QUICK_TEST_MAIN(<suite>)  // in tst_main.cpp
```

## Reference

- `import QtTest` provides `TestCase`, `SignalSpy`, and the assertion helpers; it ships with the Qt Quick Test module (`Qt6::QuickTest`).
- `TestCase` has a `name` property (labels the suite) and `when` (typically bound to `windowShown` for interactive tests).
- Test functions must be named `test_*()`. Reserved hooks: `initTestCase()` / `cleanupTestCase()` run once per file; `init()` / `cleanup()` run around every test function.
- Assertions: `compare(actual, expected, msg)`, `verify(cond, msg)`, `tryCompare(obj, prop, expected, timeout)`, `tryVerify(fn, timeout)`, `fuzzyCompare(a, b, delta)` for floats.
- Data-driven tests: define `function <name>_data()` returning an array of row objects (each may carry a `tag`); the matching `<name>(row)` receives one row per invocation.
- `SignalSpy` element: set `target` and `signalName`, then read `count`, call `clear()`, or `wait(timeout)`.
- Interaction helpers on `TestCase`: `mousePress`/`mouseRelease`/`mouseClick`/`mouseMove`, `keyClick`/`keyPress`/`keyRelease`. Object lifecycle helpers: `createTemporaryObject()`, `createTemporaryQmlObject()`.
- `QUICK_TEST_MAIN(name)` (from `quicktest.h`, the `quick_test_main` entry point) in a small C++ `main` scans a directory of `tst_*.qml` files and runs them.
- Build wiring: use `qt_add_executable` for the test main and `qt_add_qml_module(<target> URI <uri> VERSION 1.0 QML_FILES ...)` so the tested module imports resolve; point the runner via `TESTED_COMPONENT` when isolating one element. Verified against Qt 6.2–6.8.
