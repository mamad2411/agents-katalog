---
name: godot-testing-debug
description: Test and debug Godot 4.7 projects - GdUnit4 (GDScript) and gdUnit4Net (C#) with verified versions, unit/scene-runner tests, mocks, signal asserts, input simulation, headless runs as JSON, debugger, breakpoints, custom Logger, backtraces, reading errors. Use when writing or running tests, or tracking down bugs and crashes.
license: MIT
compatibility: Godot 4.7+. GdUnit4 6.2.x, gdUnit4Net (gdUnit4.api 5.1, test.adapter 3.1). Python 3.9+.
metadata:
  author: godot-agent-skills
  version: "1.1.0"
---

# Testing and debugging (4.7)

**Run tests:** `python scripts/test_run.py [--gd|--cs] [-a res://test/x] [--filter expr]` returns `{gd: {total, failed, failures: [{test, file, line, msg}]}, cs: {...}}`. It imports first, runs headless, and parses the JUnit/console results.
Before tests, compile: `../godot-gdscript/scripts/gd_check.py` and `../godot-csharp/scripts/cs_build.py`. Smoke-run the game with `../godot-core/scripts/run_godot.py smoke`.

## GDScript: GdUnit4 (verified 6.2.2 on 4.7.2)
- Install: copy `addons/gdUnit4` from the GitHub release (github.com/godot-gdunit-labs/gdUnit4, tag v6.2.x) and enable the plugin. Tests go in `res://test/`, with names ending in `_test.gd`.
- A suite `extends GdUnitTestSuite`. Tests are `func test_*()`. Hooks: `before()`, `after()` (per suite), `before_test()`, `after_test()`.
- Assertions: `assert_int/float/str/bool/vector/array/dict/object(x).is_equal(...)`, `assert_that(x)`, `assert_signal(obj).is_emitted("died")` (after `monitor_signals(obj)`), `assert_error(func() -> void: ...)`, and `await assert_func(obj, "is_ready").is_true()`.
- Memory: wrap created objects in `auto_free(...)`. The report flags orphan nodes, so treat them as bugs.
- Doubles: `mock(Class)` + `do_return(v).on(m).method()`, `spy(instance)`, `verify(m, times).method(args)`, `any_int()` and friends.
- Integration: `var runner := scene_runner("res://player.tscn")`, then `runner.simulate_action_pressed("jump")`, `await runner.simulate_frames(30)`, `runner.simulate_key_pressed(KEY_SPACE)`, `await runner.await_signal("landed")`, `runner.invoke("method")` and `runner.scene()`.
- CLI (what `test_run.py` calls): `godot --headless --path . -s -d res://addons/gdUnit4/bin/GdUnitCmdTool.gd --ignoreHeadlessMode -c -a res://test`. Exit code 0 means pass and 100 means failures. If you launch it yourself, close stdin (`< /dev/null`): with `-d`, a runtime error in a test otherwise waits forever at the `debug>` prompt (`test_run.py` already does this). Reports are JUnit XML under the `-rd` directory.

## C#: gdUnit4Net (verified with Godot.NET.Sdk 4.7.2, .NET 10 SDK)
- Add to the game csproj: `Microsoft.NET.Test.Sdk` 18.x, `gdUnit4.api` **5.1.0-rc5** (adapter 3.1.1 requires ≥5.1.0-rc5; 5.0.0 fails restore with NU1605), `gdUnit4.test.adapter` 3.1.1, `gdUnit4.analyzers` 1.0.0, plus `<CopyLocalLockFileAssemblies>true</CopyLocalLockFileAssemblies>`.
- Add a `.runsettings` with `<GdUnit4><Parameters>--headless</Parameters><GodotConnectTimeout>60000</GodotConnectTimeout></GdUnit4>`. Without it, Godot-runtime tests time out connecting. Run with `GODOT_BIN=<godot exe> dotnet test --settings .runsettings`.
- `[TestSuite]` classes, `[TestCase]` methods, `[Before]/[After]/[BeforeTest]/[AfterTest]`, `[DataPoint(nameof(Cases))]` for parameterized tests. Use `using static GdUnit4.Assertions;` → `AssertThat(x).IsEqual(y)`, `AutoFree(node)`.
- **`[RequireGodotRuntime]`** is required on any test that touches Godot types, including `Mathf`, nodes and resources. The analyzer reports `GdUnit0501` otherwise. Pure C# tests run without the engine and much faster.
- Scenes: `ISceneRunner.Load("res://x.tscn")` → `SimulateFrames`, `SimulateActionPressed`, `AwaitSignal`, `Invoke`.

## What to test
Pure logic (damage, inventory, save migration) as fast unit tests. Scenes through scene runners for controller feel, UI flows and signal wiring. Every bug fix gets a regression test. Keep suites fast, because slow suites stop getting run.

## Debugging
- Run from the editor (F5) for the full debugger: errors with stack traces, breakpoints (or a `breakpoint` statement), step in/out (Step Out arrived in 4.6), the **Remote** scene tree (live node and property inspection while playing), Profiler, Monitors and ObjectDB snapshots (4.6).
- Logging: `print`, `print_rich("[color=yellow]...")`, `print_debug` (adds file and line), `push_warning`/`push_error` (shown in the debugger with a stack, and non-fatal), `printerr`. `assert(cond, "msg")` only runs in debug builds, so never put side effects inside it.
- File logs: `debug/file_logging/enable_file_logging` (on by default for desktop, `user://logs/godot.log`). Find `user://` with `OS.get_user_data_dir()`.
- **Custom `Logger` (4.5+):** subclass it, override `_log_error`/`_log_message`, and register with `OS.add_logger()`. Use it for in-game bug reports with `script_backtraces`. Turn on `debug/settings/gdscript/always_track_call_stacks` for release-build backtraces. `Engine.capture_script_backtraces()` captures one on demand.
- CLI: `-d` (stdout debugger), `--verbose`, `--debug-collisions`/`--debug-navigation`, and `--remote-debug tcp://host:6007` to attach a running build to the editor.
- C#: attach an IDE debugger to the game process (Rider and VS Code C# Dev Kit can launch Godot with `--path`). Exceptions are logged, not fatal, so watch the Output panel.

## Reading errors fast
`res://file.gd:LINE` points at the line. "null instance" means a bad node path or something used before `_ready`. "previously freed" means an await or callback outlived its node. A "Parse Error" or "Compile Error" stops the script from loading, so everything using it fails, and you fix the first error first. "Condition "!is_inside_tree()" is true" means a tree API was called on a node that isn't in the tree yet. Engine C++ file references (`scene/main/node.cpp:123`) still mean *your* call was wrong, so read the stack.

GdUnit suites (unit, mocks, signals, scene runner), C# tests, in-game Logger (compiled by the tests): [references/patterns.md](references/patterns.md)
