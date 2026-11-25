---
name: windows-env-path-semantics
description: Windows environment-variable path derivation gotchas — APPDATA vs LOCALAPPDATA (AppData\Local is a sibling of AppData\Roaming, not a child), USERPROFILE vs HOME, HERMES_HOME fallback chains, and hermetic-test isolation for env-resolved paths. The qa-lead pulse's recurring env-var fix class.
version: 1.0.0
author: Hermes Agent (Sentry)
license: MIT
metadata:
  hermes:
    tags: [windows, env-vars, path-resolution, fallback, qa-lead]
    triggers: [APPDATA, LOCALAPPDATA, AppData, Roaming, USERPROFILE, HERMES_HOME, env var path, env path resolution, windows path fallback, roaming local]
    related_skills: [windows-cross-platform-debugging, systematic-debugging, test-driven-development]
---

# Windows Env-Var Path Semantics

Recurring class: deriving filesystem paths from Windows environment variables, and the bugs that come from getting the directory hierarchy wrong. On this host (Windows + MSYS2 git-bash, native Windows Python), every env-var→path derivation is a potential dead path.

## APPDATA vs LOCALAPPDATA

### The Trap
`APPDATA` points at `AppData\Roaming`. `AppData\Local` is a **sibling** of `Roaming`, NOT a child. So:

```python
Path(os.environ["APPDATA"]) / "Local" / "hermes" / "scripts"
# → C:\Users\X\AppData\Roaming\Local\hermes\scripts  ← can never exist on Windows
```

`Roaming\Local\...` is the fingerprint of this bug. The canonical env var for `AppData\Local` is `LOCALAPPDATA`.

### Fix Pattern
```python
local_appdata = os.environ.get("LOCALAPPDATA", "")
appdata = os.environ.get("APPDATA", "")
if local_appdata:
    local_root = Path(local_appdata)              # already ends in ...\AppData\Local — NO "Local" segment
elif appdata:
    local_root = Path(appdata).parent / "Local"   # .parent strips Roaming; re-add Local as sibling
else:
    local_root = Path.home() / "Local"
script = local_root / "hermes" / "scripts" / "godmode_toggle.py"
```

Key detail: `LOCALAPPDATA` already ends in `Local`, so the branch that uses it must NOT append another `"Local"` segment — while the `APPDATA`-derived branch MUST append one. The two branches have different shapes by design; mixing them up is the bug.

## Fallback Chains Must Keep One Final Shape

When chaining fallbacks (`HERMES_HOME` → repo `scripts/` → appdata-derived → `Path.home()`), every branch must resolve to the **same final path shape**. A "fix" that changes only one branch (e.g. `Path(appdata).parent / "hermes" / "scripts"` — silently dropping `Local`) produces a path that looks right and fails only at runtime.

**The reliable guard: a regression test that asserts the EXACT resolved path** (`run.call_args.args[0][1] == str(script_dir / "godmode_toggle.py")`), not just "something ran". In the worked example below, the first fix attempt dropped the `Local` segment and the RED test caught it before commit — the fix's own bug, found by the test, not by a user.

## Env-Dependent Tests Are Host-Dependent

Tests that resolve scripts/paths via env vars (`HERMES_HOME`, `APPDATA`, `LOCALAPPDATA`, `USERPROFILE`) must clear them:

```python
monkeypatch.delenv("HERMES_HOME", raising=False)
monkeypatch.delenv("APPDATA", raising=False)
monkeypatch.delenv("LOCALAPPDATA", raising=False)
```

On a Windows dev host these vars point at REAL directories containing REAL files (e.g. `%LOCALAPPDATA%\hermes\scripts\godmode_toggle.py`). An env-dependent test therefore:
- silently changes meaning once the code path it covers is fixed (a "script not found" test starts resolving the real host script and flips pass/fail), and
- passes on one machine and fails on another.

This bites hardest right after a fallback fix — the fix makes the fallback reach the real location, which is exactly what the test must be isolated from.

## Detection Cues
- A fallback path containing `...\Roaming\Local\...` in error messages or logs
- Code works when `HERMES_HOME` is set but breaks in non-standard setups (service launch, cron, fresh checkout without user env)
- Tests create fixtures under `<tmp>/Local/hermes/...` while code under test looks in `<tmp>/hermes/...` (missing `Local`)
- A "not found — re-run setup" style error from a fallback that should never be reached

## Worked Example — /godmode Handler (2026-08-01, commit `3ea75999e`)
`gateway/slash_commands.py:_handle_godmode_command()` had `Path(APPDATA)/"Local"/"hermes"/"scripts"` as a dead fallback (`Roaming\Local` never exists). Fix: prefer `LOCALAPPDATA`, else `Path(APPDATA).parent/"Local"`. Two RED-verified regression tests (`TestGodmodeAppDataFallback`) asserted the exact resolved script path in both layouts; the first fix attempt dropped `Local` and the tests caught it pre-commit. The pre-existing `test_script_missing_returns_setup_hint` also needed `delenv` isolation — post-fix it would have resolved the real host script.

## Related
- `windows-cross-platform-debugging` — the broader Windows compat umbrella (MSYS path translation, CRLF, USERPROFILE, `git -C`). This skill covers the env-var→path subset in depth; if both are open, prefer the broader one for anything beyond env-var derivation.
- `systematic-debugging` — root-cause process + other Windows pitfalls
- `test-driven-development` — RED-verify regression pattern used here
