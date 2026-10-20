---
name: windows-cron-msys-path-fix
description: Fix .sh scripts in cron jobs that fail on Windows due to MSYS backslash stripping. Cron resolves relative paths to C:\... and passes them to bash, which strips backslashes as escape characters.
version: 1.4.0
author: Hermes Agent
license: MIT
platforms: [windows]
metadata:
  hermes:
    tags: [cron, msys, path-fix, windows, bash]
    triggers:
      - cron job .sh script fails with "C:Users...No such file or directory"
      - MSYS path mangling in cron
      - bash script not found from cron
      - no_agent script fails with code 127
      - no_agent script times out after 120s
      - cron delivery encoding error emoji
      - cron Discord rate limit 429
      - "date: command not found / rm: command not found in cron"
      - backslash stripped in cron path
      - pythonw.exe subprocess hang capture_output
      - sys.executable resolves to pythonw.exe
      - subprocess.run captures output but hangs
      - subprocess timed out with zero stdout
      - MSYS2_ARG_CONV_EXCL
      - C:\c\ path doubled drive letter in cron
      - MSYS2_ENV_CONV_EXCL
    related_skills: [self-hosted-communication-server, kanban-worker]
---

# Windows Cron MSYS Path Fix

## Problem

When a cron job with `no_agent: true` runs a `.sh` script, the cron system resolves the relative script name (e.g. `start-browser.sh`) to a full Windows path: `${USER_HOME}\AppData\Local\hermes\scripts\start-browser.sh`. When this path is passed to git-bash/MSYS2 bash, MSYS interprets the backslashes as escape characters and strips them, producing `C:/Users/<you>/AppDataLocalhermesscriptsstart-browser.sh` which doesn't exist.

Error signature:
```
/bin/bash: C:/Users/<you>/AppDataLocalhermesscriptsmy-script.sh: No such file or directory
```

## Fix Steps

1. **Create a Python wrapper** in the scripts directory that reads the bash script and pipes it to `bash -s` via stdin:

```python
#!/usr/bin/env python3
"""Wrapper for my-script.sh — bypasses MSYS path mangling."""
import subprocess
import sys
import os

SCRIPT_PATH = r"${USER_HOME}\AppData\Local\hermes\scripts\my-script.sh"

def main():
    if not os.path.exists(SCRIPT_PATH):
        print(f"Script not found at {SCRIPT_PATH}")
        sys.exit(1)

    with open(SCRIPT_PATH, 'r', newline='\n') as f:
        script_content = f.read()

    result = subprocess.run(
        ["bash", "-s"],
        input=script_content.encode("utf-8"),  # bytes prevents Windows \n -> \r\n
        capture_output=True,
        text=False,  # must be False when passing bytes
        timeout=600  # adjust for your script
    )

    stdout = result.stdout.decode("utf-8", errors="replace")
    stderr = result.stderr.decode("utf-8", errors="replace")

    print(stdout)
    if stderr:
        print(f"STDERR: {stderr[:500]}")

    if result.returncode == 0:
        sys.exit(0)
    elif result.returncode == 124:
        # timeout — script likely started a long-lived process
        sys.exit(0)
    else:
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
```

2. **Update the cron job** to point to the Python wrapper instead of the .sh script:
   - `cronjob(action='update', job_id='...', script='my-wrapper.py')`

3. **Fix the .sh script itself** — convert CRLF to LF line endings:
   ```bash
   sed -i 's/\r$//' ${HERMES_HOME}/scripts/my-script.sh
   ```

4. **Test**:
   ```bash
   cronjob(action='run', job_id='...')
   ```

## Pitfall: Spawned subprocess can't find basic commands (exit code 127)

Even when the `bash -s` stdin piping works, the spawned bash process may lack a proper PATH to find basic commands like `date`, `rm`, `curl`, `unzip`, etc.

**Error signature:**
```
/usr/bin/bash: line N: date: command not found
/usr/bin/bash: line N: rm: command not found
```
Exit code 127 means the command is not on PATH.

**Root cause:** The cron sandbox environment has a minimal PATH that doesn't include `/usr/bin` or `/bin` — the git-bash/MSYS directories where common Unix tools live.

**Fix: Set the PATH in the subprocess `env` dict before spawning bash:**

```python
import os
import subprocess

SCRIPT_PATH = r"${USER_HOME}\AppData\Local\hermes\scripts\refresh-tax-roll.sh"
GIT_BASH = r"C:\Program Files\Git\usr\bin\bash.exe"

env = os.environ.copy()
env["PATH"] = (
    r"C:\Program Files\Git\usr\bin;"    # /usr/bin (date, rm, etc.)
    r"C:\Program Files\Git\bin;"        # /bin (curl, unzip, etc.)
    + env.get("PATH", "")
)

with open(SCRIPT_PATH, "rb") as fh:
    script_data = fh.read()

result = subprocess.run(
    [GIT_BASH, "-s"],
    input=script_data,
    capture_output=True,
    timeout=300,
    env=env          # <-- critical: pass the PATH-enhanced env
)
```

Without `env=env`, the subprocess inherits cron's minimal PATH and fails on the first Linux-native command (`date`, `rm`, `mkdir`, `curl`, `unzip`, `python`, `pip`).

**Also check whether `curl`, `unzip`, and `python` are available** at those MSYS paths. On a minimal git-bash install, `unzip` may need to be installed separately (`pacman -S unzip`).

## Pitfall: no_agent cron scripts default to 120s timeout

Scripts set as `no_agent: true` in cron jobs have a **hard default timeout of 120 seconds**. If the script exceeds this, it's killed with:
```
Script timed out after 120s: ${USER_HOME}\AppData\Local\hermes\scripts\my-script.py
```

**Workarounds (choose one):**

1. **Optimize the script to finish in under 120s.** Common slowdowns:
   - Multiple sequential API calls with sleeps between them (arXiv rate limiting is a common culprit — 8 queries × 3.5s = 28s of sleep alone)
   - Subprocess calls that themselves have long timeouts
   - Large file downloads over slow connections

2. **Reduce parallelism/depth.** Example: trimming arXiv searches from 8 categories to 4, reducing results per query from 5→4, shortening sleep from 3.5s→3.0s.

3. **Convert from no_agent to LLM-driven** (remove `no_agent: true`, add a `prompt`). LLM-driven jobs don't have the 120s constraint, though they consume tokens. Use for scripts that need network access across many endpoints.

## Pitfall: Delivery encoding failures with Unicode/emoji on Windows

When a cron job delivers to Discord (or other text channels) and the output contains emoji characters (🔴, ✅, ★, etc.), Windows' default console codec can fail:

```
'charmap' codec can't encode character '\U0001f534' in position 373: character maps to <undefined>
Discord API error (429): You are being rate limited.
```

**Causes:**
- Windows console uses a legacy codec (cp1252 or similar) that can't represent Unicode supplementary characters (emoji, some symbols)
- The delivery pipeline reroutes through a Windows-local encoding step

**Fixes:**
- **For LLM-driven jobs (no_agent=false):** Add a prompt instruction like "Avoid emoji — use ASCII markers (*, -, >) instead" or "Use only basic ASCII characters in your output"
- **For no_agent scripts:** Replace emoji in the script output with ASCII equivalents before printing:
  ```python
  # Replace emoji with ASCII equivalents for delivery
  output = output.replace("\U0001f534", "[RED]")   # red circle
  output = output.replace("\U00002705", "[OK]")     # check mark
  output = output.replace("\U00002b50", "[STAR]")   # star
  ```
- **Schedule staggering:** If multiple LLM-driven jobs fire at the same minute (e.g., 8:00am wave), Discord rate limits kick in even without emoji issues. Stagger to `:15` or `:30` past the hour.

## Pitfall: Wrapper subprocess timeout vs cron timeout — two independent constraints

When a Python wrapper script uses `subprocess.run(..., timeout=N)` to call `bash -s`, there are **two independent timeout layers**:

1. **Cron scheduler timeout** (120s for no_agent scripts) — kills the entire Python process if it exceeds this wall-clock time.
2. **Internal subprocess timeout** (whatever `N` you set in `subprocess.run()`) — kills just the bash subprocess but leaves the Python wrapper running.

**If the internal timeout is shorter than the cron timeout:**
- The subprocess times out → `subprocess.TimeoutExpired` is raised
- If NOT caught (no try/except), the Python wrapper crashes with an unhandled exception
- The cron scheduler waits for the remaining time before marking the job as error
- Error message says "Script timed out after 120s" but the actual failure was the subprocess timeout at 60s

**Fix pattern — increase internal timeout and add exception handling:**

```python
try:
    result = subprocess.run(
        [GIT_BASH, "-s"],
        input=script_content.encode("utf-8"),
        capture_output=True,
        text=False,
        timeout=120  # Match or slightly exceed the cron's 120s timeout
    )
    # ...handle normal result...
except subprocess.TimeoutExpired:
    print("Script timed out. Will retry next cycle.")
    sys.exit(0)  # Exit 0 = don't mark as cron error
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
```

Key decisions:
- Set `timeout=120` to match the cron's no_agent timeout (or just under it at 110s)
- Exit 0 on timeout so the cron doesn't alert — the script will retry next cycle
- Exit 1 on unexpected errors so the cron DOES alert
- Always `sys.exit()` with a clear code — don't let the script fall through

**Why exit 0 on timeout?** Timeouts for startup scripts (browser launchers, daemon checkers) are expected — the dependency (Camoufox, a headless browser, a remote service) may just be slow to start. Marking every timeout as a cron error creates noise. Only exit 1 for actual errors (missing files, parse failures).

## Pitfall: MSYS path translation does NOT work for Windows-native executables (Python, Node, etc.)

MSYS bash (git-bash) automatically translates MSYS-style paths (`/e/something`) to Windows-native paths (`E:/something`) when calling **shell commands** like `ls`, `cat`, `cd`, `cp`, etc. However, this translation **does NOT happen** when calling **Windows-native executables** like `python.exe`, `node.exe`, or any EXE not compiled for MSYS.

**Error signature:**
```
python ${MY_REPOS}/_project/scripts/append-digest.py
  → can't open file 'C:\e\yourdata\...': [Errno 2] No such file or directory
```
Python (a Windows-native process) receives `${MY_REPOS}/...` literally, and Windows has no `C:\e\` drive letter, so it fails.

**The fix: use Windows-native paths when calling Windows executables from MSYS:**
```bash
# WRONG — MSYS path, Python can't resolve it
python ${MY_REPOS}/_project/scripts/append-digest.py

# RIGHT — Windows-native path, Python (and Node, etc.) resolve it correctly
python "${MY_REPOS}/Documents/github/_project/scripts/append-digest.py"
# OR
python "E:\\yourdata\\Documents\\github\\_project\\scripts\\append-digest.py"
```

**Detection:** If a command works in the terminal shell with MSYS paths but fails when called from a Python wrapper or cron job, suspect path translation. The symptom is `No such file or directory` on `/drive/path` — the `/drive` prefix is being interpreted as a Windows filesystem root (e.g. `/e/...` → `C:\e\...`).

**Rule of thumb:**
- Shell builtins (cd, ls, cp, cat, echo, sed, grep) — MSYS paths work fine (MSYS translates them)
- Shell scripts (`.sh`) piped via `bash -s` — MSYS paths work inside the script body (bash is MSYS-aware)
- Windows-native EXEs (python.exe, node.exe, any .exe not compiled for MSYS) — use Windows-native paths with quotes
**Hermes tools** (`write_file`, `patch`, `read_file`, `search_files`) — these run inside the Hermes desktop (Python/Electron), which is a Windows-native process. `/e/foo` resolves to `C:\\\\e\\\\foo`, not `E:\\\\foo`. Use `E:/foo` (forward-slash, explicit drive letter) for cross-tool compatibility on Windows.

## Fix: MSYS2_ARG_CONV_EXCL when shell script calls Windows EXEs with MSYS paths

Even with the Python stdin-piping wrapper (`bash -s` with PATH fix), the **shell script itself** may call Windows-native executables (python.exe, node.exe) with MSYS paths stored in variables (e.g., `python "$SCRIPT_DIR/deep_scoring.py"` where `SCRIPT_DIR=${USER_HOME}/...`). MSYS2 translates MSYS paths when passing arguments to Windows EXEs, but it doubles the drive letter: `/c/...` → `C:\\c\\...`.

**Error signature:**
```
python.exe: can't open file 'C:\c\Users\<you>\...deep_scoring.py'
```
The doubled drive letter (`C:\c\`) is the key diagnostic. This differs from the bare `C:\e\` error in the previous pitfall — here MSYS2 IS doing path translation, but translating incorrectly (prepending the drive letter C: to the already translated `/c/`).

**Root cause:** When a `.sh` script under MSYS bash calls a Windows-native EXE with a path argument that expands from a variable containing an MSYS-style path, MSYS2 applies automatic path conversion but produces `C:\c\...` instead of `C:\...` because the path pattern `/c/` is being matched as a literal prefix rather than a recognized drive mount.

**Fix: Set MSYS2_ARG_CONV_EXCL=* in the subprocess env:**

```python
env = os.environ.copy()
env["PATH"] = r"C:\Program Files\Git\usr\bin;C:\Program Files\Git\bin;" + env.get("PATH", "")
env["MSYS2_ARG_CONV_EXCL"] = "*"    # Stop MSYS2 from converting /c/foo → C:\c\foo
env["MSYS2_ENV_CONV_EXCL"] = "*"    # Same for env var expansion inside the shell script

result = subprocess.run(
    [GIT_BASH, "-s"],
    input=script_data,
    capture_output=True,
    timeout=300,
    env=env
)
```

- `MSYS2_ARG_CONV_EXCL=*` disables all automatic path argument translation for subprocess calls made by bash.
- `MSYS2_ENV_CONV_EXCL=*` does the same for environment variable values that look like paths.

**When to use this:** Only when the Python wrapper + PATH fix are in place but the shell script still fails with `C:\c\...` on calls to Windows-native EXEs. If your script doesn't call `python`, `node`, or other Windows-native executables, you don't need it.

**Caveat:** With `MSYS2_ARG_CONV_EXCL=*`, ALL path translation is disabled — even for shell builtins that previously relied on it. If the script uses MSYS paths with shell commands (e.g., `ls /c/Users/...`), those pass through untranslated. Safe when all paths in the script are either Windows-native already, or used only with the shell (echo, redirection). Use `cygpath` explicitly where conversion is still needed.

**Pitfall: Workspace guard blocks cross-repo writes.**

**Escape hatch for files outside any workspace** (e.g., `${USER_HOME}\AppData\Local\hermes\...`): When the target is a system path `patch()` can't reach, use Python pathlib:
```python
from pathlib import Path
p = Path(r'${USER_HOME}\AppData\Local\hermes\profiles\docs-lead\PULSE.md')
text = p.read_text(encoding='utf-8')
# ... modify text ...
p.write_text(text + new_content, encoding='utf-8')
```
`read_file` with `~` works for reading outside the workspace (resolves against user home). But `patch()` and `write_file` do NOT expand `~` — only `E:/foo` or Python pathlib work for cross-workspace writes.

## Pitfall: WSL Bash Shadows Git-Bash

Even the `["bash", "-s"]` stdin piping pattern can fail on Windows systems that also have WSL installed. WSL installs its own `bash.exe` in `C:\Windows\System32\`, which often appears earlier in the system PATH than git-bash's `bash.exe`. When `subprocess.run(["bash", ...])` resolves, it picks WSL bash — which cannot access MSYS-style paths like `${MY_REPOS}/...` (only `/mnt/e/...` works in WSL).

**Error signature:**
```
wsl: Failed to start the systemd user session for 'user'.
/bin/bash: line 18: cd: ${MY_REPOS}/...: No such file or directory
```

The `wsl:` prefix in stderr and the `/e/` path failure are the key diagnostic clues.

**Fix: Use explicit git-bash path in the Python wrapper:**

```python
GIT_BASH = r"C:\Program Files\Git\usr\bin\bash.exe"
if not os.path.exists(GIT_BASH):
    GIT_BASH = "bash"  # fallback to PATH lookup

result = subprocess.run(
    [GIT_BASH, "-s"],
    input=script_content.encode("utf-8"),
    ...
)
```

**Also fix your .sh scripts** to handle both MSYS and WSL paths:

```bash
CAMOFOX_DIR="${MY_REPOS}/camofox-browser"
cd "$CAMOFOX_DIR" 2>/dev/null || {
    echo "Trying WSL path..."
    cd "/mnt${MY_REPOS}/camofox-browser" 2>/dev/null || {
        echo "ERROR: Cannot find directory."
        exit 1
    }
}
```

## Pitfall: `pythonw.exe` Subprocess Hang with `capture_output=True`

**When a Python wrapper script uses `subprocess.run([sys.executable, ...], capture_output=True)` and the subprocess hangs until timeout with zero output.**

Root cause: `sys.executable` may resolve to `pythonw.exe` (the GUI-mode Python variant that runs without a console window) when the parent process is itself a `pythonw.exe` process — common when cron jobs run inside the Hermes desktop app. `pythonw.exe` detaches from the parent console at spawn and never properly connects its stdout/stderr pipes. `subprocess.run(capture_output=True)` blocks indefinitely waiting for the pipes to close.

**Signature:** timeout fires with zero stdout/stderr from the child, even for scripts that `print("hello", flush=True)` at the top.

**Diagnose:** `python -c "import sys; print(sys.executable)"` — if it ends with `pythonw.exe`, the hang is confirmed.

**Fix:** Strip `pythonw.exe` to `python.exe` before subprocess calls:

```python
def get_python_exe():
    exe = sys.executable or "python"
    if exe.endswith("pythonw.exe"):
        exe = exe.replace("pythonw.exe", "python.exe")
        if not os.path.exists(exe):
            exe = "python"
    return exe

result = subprocess.run(
    [get_python_exe(), SCRIPT_PATH],
    capture_output=True, text=True, timeout=300
)
```

**Alternative:** Import and call the target script directly instead of spawning a subprocess, which avoids the pipe issue entirely:
```python
sys.path.insert(0, os.path.dirname(script_path))
from my_script import main as child_main
child_main()
```

**Cues:**
- Subprocess with `capture_output=True` hangs on Windows, works on Linux/macOS
- `sys.executable` ends with `pythonw.exe`
- Zero stdout/stderr output before timeout, even from scripts that print immediately
- Script works in terminal (where `python.exe` is used) but hangs from cron/daemon

## Detection

To check which `bash` Python's subprocess resolves to:

```bash
# Check if WSL bash would shadow git-bash
ls -la /c/Windows/System32/bash.exe    # WSL bash (if installed)
ls -la "/c/Program Files/Git/usr/bin/bash.exe"  # git-bash
which bash   # Which one is active in your current session
```

## Why This Works (stdin piping)

- `subprocess.run(["bash", "-s"])` or `subprocess.run([GIT_BASH, "-s"])` starts bash and tells it to read from stdin
- `input=script_content.encode("utf-8")` sends the script content as bytes
- With `text=False`, Python doesn't convert `\n` to `\r\n` on Windows
- bash receives clean LF-only script content with no path arguments at all
- No MSYS path translation occurs because no paths are passed as CLI arguments

## Alternative (for .py scripts)

Python scripts work fine with cron on Windows — no MSYS translation occurs. Use `.py` instead of `.sh` when possible.

## Creating Cron Jobs for External Python Projects

When you need to run an external Python project (not in `~/.hermes/scripts/`) as a cron job, the project's own scripts often fail because they use **relative imports** (`from .database import init_db`) that only work when the project is run as a package, not as a standalone script.

### The Wrapper Pattern

Create a wrapper script in `~/.hermes/scripts/` that:
1. Adds the project directory to `sys.path`
2. Calls `os.chdir()` to the project root (needed by packages that read relative config/data files)
3. Imports and runs the project's own functions directly (avoiding the broken entry-point script)
4. Prints results to stdout (captured and delivered by cron)

```python
#!/usr/bin/env python3
"""Wrapper script — runs a function from an external project.

Deploy to ~/.hermes/scripts/ and register with:
  hermes cron create --script this-script.py --no-agent --deliver origin "0 8 * * 1"
"""

import sys
import os

PROJECT_DIR = r"${MY_REPOS}\Documents\github\finance-team\insider-trading"

sys.path.insert(0, PROJECT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, "src"))
os.chdir(PROJECT_DIR)

# Import the project's own modules (they use relative imports internally)
from src.main import init_system, run_scout

init_system()
signals = run_scout("admin")

print(f"Scout — {len(signals)} signal(s)")
for s in signals:
    print(f"  {s.ticker}: {s.action} ({s.confidence:.0f}%) | {s.reasoning[:120]}")
```

**Why this works:** By importing the project's modules directly (not running its scripts), Python resolves relative imports correctly because `src/main.py` is loaded as `src.main` — a package member — not as a top-level script. The `sys.path.insert(0, ...)` ensures the project root is discoverable, and `os.chdir()` mirrors the working directory the project expects.

### Deployment Steps

1. **Write the wrapper** to `~/.hermes/scripts/<name>.py`
2. **Test it** by running `python "C:/Users/<user>/AppData/Local/hermes/scripts/<name>.py"`
3. **Create the cron job** with no-agent mode:
   ```bash
   hermes cron create "<schedule>" \
     --name "Descriptive name" \
     --script <name>.py \
     --no-agent \
     --deliver origin \
     --repeat 52
   ```
4. **Verify** the job appears in `hermes cron list` with the correct schedule

### Pitfall: MSYS paths don't resolve for Windows Python

When the PROJECT_DIR uses an MSYS-style path (`${MY_REPOS}/...`), Python (a Windows-native process) can't find it:

```python
# WRONG — Python receives "/e/..." literally, interpreted as "C:\e\..."
PROJECT_DIR = "${MY_REPOS}/my-project"

# RIGHT — Windows-native path (forward-slash or double-backslash)
PROJECT_DIR = r"${MY_REPOS}\Documents\github\my-project"
# OR
PROJECT_DIR = "${MY_REPOS}/Documents/github/my-project"
```

See the "MSYS path translation does NOT work for Windows-native executables" pitfall above for the full diagnosis.

### Pitfall: Dependencies not installed in the Hermes venv

The cron job runs under the Hermes venv Python. If the external project needs packages not in the venv (pandas, textblob, etc.), they must be installed into the venv:

```bash
pip install pandas textblob yfinance
```

### Pitfall: no_agent timeout (120s)

No-agent scripts have a 120s hard timeout. If the project startup is slow (import time, API warmup, large DB init), the script may be killed. See the "no_agent cron scripts default to 120s timeout" section above for mitigation strategies.

## Additional gotchas found in practice

### pipefail syntax
`set -uo pipefail` is NOT valid bash — `pipefail` is a shell option, not a flag. It must be set with `-o`:
- WRONG: `set -uo pipefail` (bash errors: "pipefail: invalid option name")
- RIGHT: `set -u -o pipefail` OR `set -o pipefail` on its own line

### CRLF line endings (.sh scripts created on Windows)
Bash scripts created or last-edited on Windows often have CRLF (`\r\n`) line endings. When piped via `bash -s` stdin, the `\r` characters cause silent failures:
- `$'\r': command not found`
- `cd: $'path\r': No such file or directory`
- `sleep: invalid time interval '1\r'`

Fix with: `sed -i 's/\r$//' /path/to/script.sh`

Verify with: `file /path/to/script.sh` (should say "ASCII text", not "ASCII text, with CRLF line terminators")

### Shell pipeline inflates byte count on Windows (bytes_written assertion mismatch)

When testing `bytes_written` from a shell pipeline helper (e.g., `_atomic_write()` that uses `cat > "$tmp"`), the assertion can fail on git-bash with an off-by-N byte count:

```python
# WRONG — fails on git-bash: 7 != 6
assert result.get("bytes_written") == len("after\n")
# actual: bytes_written=7, len("after\\n")=6
```

**Root cause:** `cat > "$tmp"` in a shell pipeline converts `\n` to `\r\n` on git-bash (MSYS). `wc -c` (used internally by helpers like `_atomic_write`) returns **actual disk bytes** (7: `a f t e r \r \n`), while `len(content.encode())` returns **logical bytes** (6: `a f t e r \n`). Same root cause as CRLF line-ending issues above, but manifests in test assertions rather than script execution.

**Fix: assert against `os.path.getsize(target)` instead of `len(content)`:**

```python
import os

# RIGHT — uses actual disk byte count from filesystem metadata
assert result.get("bytes_written") == os.path.getsize(target)
assert target.read_text(encoding="utf-8") == "after\n"
```

**Why `os.path.getsize` works:** It reads the file's actual size on disk — the same number `wc -c` computed. `len(content)` counts logical characters, which differ after shell pipeline CRLF conversion.

**Caveat:** Only matters when the write path goes through a shell pipeline (git-bash `cat >`, `echo >`, `tee`, etc.). Pure Python writes (`Path.write_text()`, `open().write()`) bypass MSYS and are not affected. Check if the helper under test uses `subprocess.run(["bash", "-c", ...])` or equivalents — if yes, use `os.path.getsize`; if no, `len(content)` is fine.

**Detection:** Error reads `assert 7 == 6` (or similar) where left side = `len(content) + number_of_newlines` — extra bytes come from `\r` prepended before each `\n`.

### Python subprocess \\n -> \\r\\n conversion on Windows
When passing script content to `subprocess.run(input=...)` with `text=True`, Windows Python converts `\n` to `\r\n` before writing to the pipe. This re-introduces CRLF that you just removed from the file. **Always use `text=False` and pass bytes:**
```python
result = subprocess.run(
    ["bash", "-s"],
    input=script_content.encode("utf-8"),  # bytes, not str
    capture_output=True,
    text=False,  # must be False with bytes input
)
```

Non-default filesystem paths in subprocess
The wrapper's subprocess runs in the cron sandbox which may not have:
- Secondary drives mounted (E:\, F:\)
- All PATH entries available (python may resolve as "python3" or not at all)
- Firefox/Chrome installations at expected portable paths

For scripts that need these, either:
- Convert the cron job from `no_agent: true` to an LLM-driven job (inherits the full agent environment)
- Configure the sandbox env vars in the wrapper before calling bash

## Reference files in this skill
- `references/watchdog-browser.py` — Working stealth browser watchdog wrapper
- `references/run-pim-ingestion.py` — PIM ingestion wrapper (paused due to env deps)
- `references/import-firefox-cookies-graceful.py` — Firefox cookie import that handles Camoufox being down gracefully (don't error the cron when the dependency is off)
