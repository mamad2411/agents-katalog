---
name: windows-test-platform-simulation
description: "Windows tests: sys.platform patch breaks shutil.which."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [windows, tests, pytest, sys.platform, monkeypatch, shutil.which, pathext, cross-platform]
    triggers:
      - test fails only when sys.platform is monkeypatched
      - shutil.which returns None on Windows
      - "not found on PATH after platform patch"
      - simulate linux in a Windows test
      - monkeypatch sys.platform
      - PATHEXT
      - cross-platform test windows
    related_skills: [systematic-debugging, test-driven-development, windows-cross-platform-debugging]
---

# Windows Test Platform Simulation

Class: authoring tests on a Windows host that simulate other platforms (`monkeypatch.setattr(sys, "platform", "linux")`) so the code-under-test's platform branch runs, without the simulation silently breaking stdlib behavior. The Hermes Agent codebase is developed for Linux/macOS but tested on Windows — every simulated-platform test is a potential landmine.

## The Core Pitfall: `sys.platform` Patch Breaks `shutil.which()` (PATHEXT)

**WHEN a test simulates a non-Windows platform with `monkeypatch.setattr(sys, "platform", "linux")` (or direct assignment `sched_mod.sys.platform = "linux"`), and the code under test calls `shutil.which("bash")` — or any bare-name executable lookup — the lookup SILENTLY returns None on a real Windows host, even though the binary is on PATH.**

1. **Root cause.** On Windows, `shutil.which("bash")` resolves `bash` → `bash.exe` using the PATHEXT extension list; with `sys.platform` patched to a POSIX value, that extension resolution is skipped and `which()` returns None for the same input that resolved fine moments before. Stdlib behavior, not a test-env quirk.

2. **The symptom is a "not found" branch firing BEFORE your mock.** Code like `cron/scheduler.py:_run_job_script()` treats a None `_bash` as a hard error — the test fails with `success is False` at a `_bash is None` guard, long before the mocked `subprocess.run`. The captured argv is never populated, so the failure looks unrelated to the platform patch.

3. **Fix: stub `shutil.which` alongside `sys.platform`.** Simulated-platform tests must patch the lookup to return a plausible path for the simulated OS:
   ```python
   monkeypatch.setattr(sched_mod.sys, "platform", "linux")
   monkeypatch.setattr(sched_mod.shutil, "which",
       lambda name: "/usr/bin/bash" if name == "bash" else None)
   monkeypatch.setattr(sched_mod.subprocess, "run", fake_run)
   ```

4. **Verify the interaction directly before debugging the test:**
   ```python
   import sys, shutil
   shutil.which("bash")      # → C:\...\Git\usr\bin\bash.EXE  (win32)
   sys.platform = "linux"
   shutil.which("bash")      # → None  ← PATHEXT matching skipped
   ```

**Cues that trigger this pitfall:**
- A test that monkeypatches `sys.platform` fails with a "not found on PATH" error for a binary that demonstrably exists
- The failure happens in code BEFORE the mocked `subprocess.run` — captured argv is empty
- The identical test passes when the platform patch is removed
- Windows host, cross-platform test suite

## Related Pattern: `sys.platform` vs `os.name` in Code Under Test

Code under test may branch on either `sys.platform` (`"win32"`) or `os.name` (`"nt"`). Patching `sys.platform` does NOT change `os.name`, so:
- If code branches on `os.name`, patch `os.name` (or the module's reference) instead — or the win32 branch never runs.
- If code caches a platform flag at module import (`IS_WINDOWS = sys.platform.startswith("win")`), patch the module's flag, not `sys.platform`.

## Worked Example — Forge Pulse 2026-08-05 (cron/scheduler.py win32 fix)

Regression tests for commit `2b4a5b166` (`cron/scheduler.py` backslash→forward-slash conversion for `.sh` script paths on win32) in `tests/cron/test_cron_script.py`:

- `test_win32_sh_script_argv_uses_forward_slashes` — patched `sys.platform` to `"win32"` AND stubbed `shutil.which` (returns git-bash path). Passed.
- `test_non_win32_sh_script_path_untouched` — patched `sys.platform` to `"linux"` but did NOT stub `shutil.which` first. Failed with `success is False` ("bash not found on PATH") even though bash is on PATH. Root cause: PATHEXT lookup skipped under the platform patch. Fix: stub `shutil.which` → `/usr/bin/bash`. 23/23 tests then passed.

Diagnostic sequence that isolated it:
```bash
# 1. Direct shutil.which check in venv python — works:
#    → C:\Program Files\Git\usr\bin\bash.EXE
# 2. Reproduce with scheduler imported — still works (import side effects NOT the cause)
# 3. Set sys.platform = 'linux' → shutil.which('bash') → None  ← root cause
```

## Pitfalls

- **Don't debug the test before checking the interaction.** The 3-line verification snippet above (step 4) is faster than reading tracebacks — run it once and you know whether the platform patch is the culprit.
- **Stub `which`, don't prepend fake PATH entries.** Setting `monkeypatch.setenv("PATH", "/usr/bin:...")` does NOT help — the PATHEXT skip is keyed off `sys.platform`, not PATH contents.
- **Restore `sys.platform` in teardown.** `monkeypatch` auto-restores on fixture teardown, but bare `sched_mod.sys.platform = "linux"` at module level leaks into other tests in the file — use monkeypatch, never direct assignment, unless you explicitly restore.

## Related
- `windows-cross-platform-debugging` — the broader Windows compat umbrella (USERPROFILE monkeypatch, CRLF, MSYS path translation, platform detection idioms). If that skill were curator-managed it would host this pitfall; see curator adoption note.
- `systematic-debugging` — root-cause process + Windows subprocess/backslash pitfalls.
