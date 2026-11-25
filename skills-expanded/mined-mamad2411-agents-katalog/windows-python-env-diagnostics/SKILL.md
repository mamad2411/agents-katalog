---
name: windows-python-env-diagnostics
description: Diagnose Windows Python environment failures — compiled-extension (.pyd) load failures, interpreter/venv ABI mismatches, and two-venv confusion where pip and the interpreter disagree on which site-packages is live.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [windows, python, venv, pyd, dll, pip, environment, debugging]
    triggers:
      - ModuleNotFoundError pydantic_core
      - _pydantic_core not found but .pyd exists
      - cp311 wheel on python 3.13
      - pip Not uninstalling outside environment
      - two venvs site-packages mismatch
      - fastapi import fails in venv
      - corrupted .pyd after interrupted upgrade
      - DLL load failed for .pyd
      - which venv is the real one
      - force-reinstall pydantic-core
    related_skills: [windows-cross-platform-debugging, systematic-debugging]
---

# Windows Python Environment Diagnostics

Recurring failure class on Windows hosts: a Python import dies even though the package
is installed, or a `pip install` "succeeds" without fixing anything. Root causes live in
the **environment layer** (compiled binaries, venv resolution), not in the code being run.
Symptom patterns below are ordered from most to least common.

## 1. `.pyd` Exists but Won't Import (DLL/ABI Load Failure)

### The Trap
`ModuleNotFoundError: No module named 'pkg._pydantic_core'` (or similar) while the `.pyd`
file **exists** in site-packages. The message is misleading — the module is missing because
the DLL failed to **load**, not because it's absent. Python masks DLL load failures as
ModuleNotFoundError, which sends you hunting for a missing file that is actually there.

### Diagnostic Ladder
1. Confirm the file exists:
   `ls site-packages/pydantic_core/_pydantic_core*.pyd`
2. Get the REAL error with ctypes — bypasses the import system's masking:
   ```python
   import ctypes, os
   p = os.path.abspath('.../_pydantic_core.cp311-win_amd64.pyd')
   try:
       ctypes.CDLL(p); print('OK')
   except OSError as e:
       print('DLL load failed:', e)
   ```
   `Could not find module '...' (or one of its dependencies)` = DLL-level failure.
3. Check ABI match: `python -c "import sys; print(sys.version)"` vs the `cpNNN` tag in the
   wheel filename. A `cp311` wheel **cannot** load into a 3.13 interpreter (and vice versa) —
   the most common cause of "exists but won't import".
4. Check WHICH site-packages the interpreter actually resolves vs which pip targets:
   ```bash
   python -c "import sys; print(sys.prefix)"
   python -m pip show <pkg>   # note the Location line
   ```

## 2. The Two-Venv Tell

pip error: `Not uninstalling <pkg> at C:\...\venv\lib\site-packages, outside environment
C:\...\.venv` — the interpreter loads site-packages from a **different venv than pip
manages**. Consequence: `pip install` "succeeds" but changes nothing (wheels land in the
wrong venv; the import failure persists). Also the `pip show` Location will disagree with
the `sys.prefix`-relative path the interpreter actually imports from.

**Fix: always run pip from the venv that OWNS the site-packages directory.**

### Stray-Venv Variant
A repo can contain two venvs (`venv/` and `.venv/`) created by different interpreters
(e.g. `venv/` = 3.11.9 with all the wheels, `.venv/` = a stray 3.13 shell). `which python`
resolving to the stray one makes every import of compiled packages fail confusingly.
Before debugging anything: confirm `sys.version` AND `sys.prefix` — the interpreter you
think you're using is not always the one that's live.

### PYTHONPATH Contamination Variant
A persistent `PYTHONPATH` env var can list BOTH venvs' site-packages — usually the old
venv FIRST (`...\venv\Lib\site-packages;...\.venv\Lib\site-packages`). First match wins
on import, so the interpreter loads the OLD venv's compiled binaries even when the
shell's `python` is the NEW venv's interpreter → binary-incompatible `.pyd` crash
(cp311 wheel inside a 3.13 interpreter) that survives every reinstall. This is the
variant that outlives a force-reinstall fix — the wheels are fine, the path ordering
isn't. Check `echo "$PYTHONPATH"` before anything else; if it interleaves two venvs'
site-packages, that IS the bug. Fix at the source (shell profile/env config); for a
one-off run, don't inherit it:
```bash
unset PYTHONPATH
<venv-with-deps>/Scripts/python.exe -m pytest ...   # repo-only path, interpreter resolves its own site-packages
```

### Test-Deps Location Check (mid-migration)
During a half-finished venv migration (new `.venv/` created, test deps not yet installed),
pytest lives ONLY in the old venv. Probe before running a suite:
`<venv>/Scripts/python.exe -m pytest --version` — then run under the interpreter that
answers, with `PYTHONPATH=<repo-root>` only. Do not assume the new venv is usable for
tests just because it imports app code.

## 2b. Stale Packages in the Base Interpreter ROOT (not site-packages)

A package directory sitting directly in the interpreter root (`C:\...\Python311\fastmcp\`
with `fastmcp-3.4.2.dist-info`) — NOT in `Lib\site-packages` — shadows every venv built
on that interpreter, because the base root precedes the venv's site-packages in
`sys.path`. Symptom: a freshly created, correctly-pinned project venv imports `fastmcp`
3.4.2 from the BASE root (check the `__file__` path in the traceback — it won't point at
the venv), then fails on a missing dep (e.g. `No module named 'pydantic'` or `uvicorn`).

**Diagnose:** `ls /c/.../PythonNN/ | grep -i <pkg>` — look for the package dir AND its
dist-info directly in the root, alongside `python.exe` / `Lib`.
**Fix:** rename, don't delete (cheap rollback):
```bash
cd ${USER_HOME}/AppData/Local/Programs/Python/Python311
mv fastmcp fastmcp.renamed && mv fastmcp-3.4.2.dist-info fastmcp-3.4.2.dist-info.renamed
```
Check BOTH the base root and `Lib\site-packages` when imports resolve to unexpected
paths. Proven 2026-07-31 on git-stars MCP (`fastmcp` 3.4.2 in Python311 root shadowing
a venv pinned to 0.4.1); same class as the earlier `mcp.renamed` fix.

## 2c. PYTHONPATH Injecting Hermes-Agent Site-Packages Into Every Process

A persistent `PYTHONPATH` that includes the hermes-agent venv paths
(`...\hermes-agent;...\hermes-agent\venv\Lib\site-packages;...\hermes-agent\.venv\Lib\site-packages`)
forces EVERY python process — including project venv interpreters — to import hermes'
`mcp`/`fastmcp`/`pydantic` copies instead of the project's pinned ones. PYTHONPATH
entries land BEFORE site-packages in `sys.path`, so even `./.venv/Scripts/python.exe`
loses to the global env. Consequences: `ModuleNotFoundError: pydantic_core._pydantic_core`
or `McpError: Invalid request parameters` (the wrong mcp version gets loaded).

**Exact mechanism (proven 2026-07-31, Weaver pulse):** the hermes-agent `.venv` is a
**Python 3.13** venv — its `pydantic_core/_pydantic_core.cp313-win_amd64.pyd` is fine for
3.13 but the ABI tag is wrong for every other interpreter. When PYTHONPATH injects that
site-packages dir into a **3.11** process (git-stars venv, system Python311), the 3.11
import machinery finds no `cp311` binary there → `ModuleNotFoundError` for a module that
"exists". It is an ABI-shadowing failure, NOT a corrupt pydantic_core. Tells that
distinguish it: `ls <dir>/pydantic_core/` shows a `cpNNN` tag that doesn't match the
failing interpreter's `sys.version`, and the venv's OWN `pydantic_core` (correct ABI
tag) is present but never reached.

**Diagnose:** `echo "$PYTHONPATH"` — hermes-agent paths present = polluted.
**Where it lives (check in this order):** (1) Windows registry — `cmd //c "reg query
HKCU\Environment /v PYTHONPATH"` and the HKLM Session Manager equivalent; (2) bash
profiles (`~/.bashrc`, `~/.profile`, `/etc/profile`); (3) the **agent-process env**
(baked at Hermes/gateway launch — see 2d). On this box it is registry-clean and
profile-clean: it exists only in the agent process env, so a registry fix would be
pointless and the real fix is at the gateway/launch layer. Always confirm which layer
before editing anything.
**One-off test fix:** `env -u PYTHONPATH ./.venv/Scripts/python.exe ...` or pin
PYTHONPATH to ONLY the project venv's site-packages. (On this box, `env -u PYTHONPATH`
can trigger an intermittent `WinError 10106` on `import asyncio` — Winsock LSP flake;
retry 3-5x, or verify the app module imports instead of the transport, see below.)
**Config fix:** never use bare `python` as an MCP `command:` — it resolves to the broken
hermes `.venv`. Point at the project venv explicitly:
`command: E:\...\project\.venv\Scripts\python.exe`.

**In-process verification when transport tests fail:** if a subprocess/transport test
dies on a host-level flake, verify the app module itself loads with a clean env — a
clean import + pinned deps is strong evidence the fix landed:
```bash
cd <project> && env -u PYTHONPATH ./.venv/Scripts/python.exe -c \
  "import sys; sys.path.insert(0,'.'); import app.main; print('APP.MAIN OK')"
```

**Protocol-level verification for stdio MCP servers (stronger than import check):**
pipe a raw MCP `initialize` request into the server and look for `serverInfo` in the
response — proves the server boots AND completes the MCP handshake, which is exactly
what Hermes does at discovery:
```bash
cd <project> && echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}' | \
  env -u PYTHONPATH ./.venv/Scripts/python.exe -m app.main
# expect: {"jsonrpc":"2.0","id":1,"result":{...,"serverInfo":{"name":"<server>","version":"<ver>"}}}
```
**Why `env -u PYTHONPATH` is the right test env:** Hermes' documented stdio env-filtering
passes only PATH/HOME/USER/etc. to MCP subprocesses — PYTHONPATH is NOT inherited. So a
server that passes with `env -u PYTHONPATH` is production-representative; a server that
only fails WITH the polluted PYTHONPATH may already work under Hermes (the pollution is
an interactive/manual-run hazard, not necessarily a production MCP blocker). Verify
before assuming a config change is needed.

## 2d. Env-Overlay Propagation — Cron Scheduler / Gateway Blind-Append

Even with a clean interactive shell, a poisoned PYTHONPATH reproduces in every child
process when env-overlay builders blindly append the INHERITED PYTHONPATH. Confirmed
sites on this box: `cron/scheduler.py` `_windows_cron_python_invocation` (uv-venv
Windows path: base-python + env overlay) and `gateway/run.py` (~line 208, bakes
PYTHONPATH at gateway startup — persists until gateway restart). One stray `.venv`
entry in the gateway's env → every cron job overlay carries cp313 site-packages ahead
of the cp311 venv → fleet-wide ABI crashes that look like per-component corruption
(dashboard down, MCP servers failing, all with different symptoms).

**Fix pattern** — when building ANY child-process PYTHONPATH overlay, filter inherited
entries: drop `site-packages` entries whose venv root differs from the resolved venv;
keep repo roots and plain tool dirs:

```python
filtered = []
for entry in existing_pythonpath.split(os.pathsep):
    if not entry:
        continue
    p = Path(entry)
    if "site-packages" in p.parts:
        entry_venv = p.parents[1]  # <venv>/Lib/site-packages -> <venv>
        if os.path.normcase(str(entry_venv)) != os.path.normcase(str(venv_dir)):
            continue
    filtered.append(entry)
```

**Audit every blind-append site:** `grep -rn "PYTHONPATH" gateway/ cron/ hermes_bootstrap.py`
— each place that appends inherited PYTHONPATH to a child env is a recurrence point.

**Regression-test shape:** call the REAL overlay function with a deliberately polluted
PYTHONPATH in `os.environ` (assert: stray gone, own-venv kept, tool dirs kept,
empty-inherit edge), plus tmp_path fake venv trees (`pyvenv.cfg` with `uv`+`home`, base
`python.exe`, `Lib/site-packages/`) and `skipif sys.platform != "win32"`.

**Test-invocation trap:** bare `python` / `pytest` on PATH may resolve to the stray venv
or system Python. Use `venv/Scripts/python.exe -m pytest` or `venv/Scripts/pytest.exe`
explicitly and confirm `sys.executable` + `pytest.__version__`. `scripts/run_tests.sh`
probes `$VENV/bin/activate` (POSIX layout) — Windows uv venvs use `Scripts/`, so the
runner finds no venv and exits; don't rely on it on Windows.

## 2e. Native Python Rejects MSYS Script Paths (`/e/...` → `C:\e\...`)

When invoking a Python script from git-bash, the **script path argument** must be a
native Windows path, even though bash itself accepts MSYS paths:

```bash
python ${MY_REPOS}/.../script.py        # FAILS: can't open file 'C:\e\yourdata\...'
python "${MY_REPOS}/.../script.py"      # ✅ native drive-letter path
```

Bash happily expands `/e/...` for its own tools, but passes the literal string to
native Windows Python, which interprets the leading `/` as a root-relative path on the
current drive (`C:\e\...`). `Errno 2: No such file or directory` on a script that
visibly exists is the tell. Same rule as the `write_file`/`patch` MSYS-path pitfall
(hermes-agent-skill-authoring #14) — but applies to `terminal` too whenever the
command runs **native Python** rather than a bash builtin. Proven 2026-07-31
(Skillmate pulse, `append-digest.py`).

## 3. Corrupt Compiled Binary (Interrupted Upgrade)

A `.pyd` that loads fine ABI-wise can still be corrupt — truncated/partial writes from
interrupted `pip install` runs are common on Windows (AV scanning, power events, kill -9).

### Fix Pattern
Force-reinstall the exact version into the owning venv:
```bash
venv/Scripts/python.exe -m pip install --force-reinstall --no-deps "pydantic-core==2.46.4"
venv/Scripts/python.exe -c "import pydantic_core; print(pydantic_core.__version__)"
```
`--no-deps` keeps the repair surgical; matching the exact version avoids unrelated upgrades.

## Verification

After any fix, verify with the **same interpreter that will run the app**:
```bash
venv/Scripts/python.exe -c "import <pkg>; print(<pkg>.__version__)"
```
Then verify the real consumer imports (e.g. `import fastapi` or the app module) — a package
import is not proof the app boots.

Full worked example of sections 2b/2c (the git-stars MCP repair, all three stacked root
causes + in-process verification when transport tests hit `WinError 10106`): see
[references/git-stars-mcp-repair.md](references/git-stars-mcp-repair.md).

## Proven On

hermes-agent repo, dev-lead pulse 2026-07-31: `venv/` (3.11.9) had a corrupted pydantic_core
`.pyd` (partial write Jul 30) — every fastapi import died → web dashboard + Hermes One
endpoints silently down. The `ctypes.CDLL` ladder exposed the DLL failure; the "outside
environment" pip error exposed the two-venv split. Force-reinstall into `venv/` fixed it.
Follow-up (Sentry pulse 2026-07-31): the migration direction is `.venv/` (3.13) as the NEW
target — NOT a stray. It is incomplete: pytest + test deps not yet installed, and the
persistent `PYTHONPATH` still lists `venv/` before `.venv/`, which reproduces the ABI-mismatch
crash for the 3.13 interpreter. Tests currently run under `venv/` (3.11, has pytest) with
`PYTHONPATH=<repo-root>` only. Do not "fix" by declaring either venv stray — resolve the
PYTHONPATH ordering and finish the migration instead.

⚠️ Pulse logs disagree on which venv is canonical: dev-lead pulses treat `venv/` (3.11) as the
real venv and `.venv/` as stray; the qa-lead note above says `.venv/` is the migration target.
Check current state (`venv/Scripts/python.exe --version` vs `.venv/Scripts/python.exe
--version`, which one has pytest) before acting — don't trust either stale note.

Propagation fix (Forge pulse 2026-07-31, commit `89a03aafb`): `cron/scheduler.py`
`_windows_cron_python_invocation` now filters foreign-venv site-packages from the inherited
PYTHONPATH when building job env overlays (section 2d). 2 regression tests added;
`test_scheduler.py` 224/224. `gateway/run.py:208-210` still has the blind-append pattern —
fold into rebase notes; a gateway restart purges the baked-in PYTHONPATH for agent jobs.

Weaver pulse 2026-07-31 (same day): the git-stars repair from the morning pulse was
re-verified at protocol level with the stdio initialize handshake (serverInfo
`github-star-intelligence-mcp` v1.28.1) under `env -u PYTHONPATH` — confirms the exact
mechanism in 2c is ABI shadowing (cp313 vs cp311), the pollution is registry-clean /
profile-clean (agent-process env only), and Hermes' stdio env-filtering means the server
is production-ready despite the interactive-shell pollution.

## Related

- `windows-cross-platform-debugging` — code-level Windows compat (paths, CRLF, USERPROFILE).
  This skill is the environment-layer complement (venvs, compiled binaries).
- `windows-cron-msys-path-fix` — MSYS path mangling when invoking native Python from git-bash.
