---
name: subprocess-hang-diagnostics
description: Diagnose and fix subprocess calls that hang indefinitely in cron scripts — detecting commands waiting for interactive terminal input that will never arrive, and applying the right non-interactive flags. Covers the WSL git credential gap and the split-operations pattern as a primary case study.
version: 1.0.0
author: Hermes Agent (cron recovery)
license: MIT
metadata:
  hermes:
    tags: [cron, subprocess, timeout, debugging, hang-detection, wsl, git-credentials]
    triggers:
      - subprocess.TimeoutExpired
      - command timed out
      - script hangs in cron
      - git push hangs
      - git credential prompt
      - WSL git no credential helper
      - radicle sync failure
      - split git operations
      - GIT_TERMINAL_PROMPT
      - exit code 15
      - SIGTERM
      - orphaned subprocess
      - process tree cleanup
      - Script exited with code 15
    related_skills:
      - windows-cross-platform-debugging
      - cron-watchdog
      - systematic-debugging
---

# Subprocess Hang Diagnostics

Diagnosing and fixing `subprocess.run()` calls that hang indefinitely in cron scripts, automation agents, or non-interactive contexts.

## Core Pattern: The Terminal-Prompt Hang

The single most common reason a subprocess call hangs is that the child process is **waiting for interactive terminal input** — a password prompt, a yes/no confirmation, a host-key verification, or a credential prompt — and no TTY is connected.

### Detection

The traceback always points at the hanging command:

```
subprocess.TimeoutExpired: Command '<the hanging command>' timed out after 120 seconds
```

Key fields to read from the traceback:

| Field | What to look for |
|---|---|
| `args` | The exact command that hung. This is your primary clue. |
| `timeout` | How long the caller waited. If every run hits this, it's a hang — not slow processing. |
| `stderr` | May contain partial output written before the hang — often the prompt text itself. |

### First-Aid Checklist

When a cron script (or any non-interactive context) fails with `TimeoutExpired`:

1. **Read the hanging command** from the traceback's `args` field. What tool is it running?
2. **Identify the expected interactive prompt** — common culprits:
   - `git push` / `git pull` on HTTPS remotes → waiting for username/password
   - `ssh` / `scp` → waiting for passphrase or `yes/no` host key confirmation
   - `apt-get` / `apt` → waiting for `[Y/n]` confirmation
   - `pip install` → waiting for confirmation
   - Any Python `input()` call → no stdin in subprocess
3. **Apply the tool's non-interactive flag**:
   - git: `export GIT_TERMINAL_PROMPT=0` (fail fast instead of hang)
   - SSH: `-o BatchMode=yes -o StrictHostKeyChecking=no`
   - apt: `DEBIAN_FRONTEND=noninteractive`
   - pip: `-y` or `--quiet`
4. **Verify in the execution environment** — if the command works in an interactive terminal but hangs in the cron/subprocess context, the difference is **TTY presence**. Don't try to fake a TTY; just add the safety flag.
5. **Bump the timeout only as a last resort** — a 120s timeout hit on *every* run means the command is *waiting*, not *working*. Fixing the prompt is the right fix. Extending the timeout just delays the same failure.

## Case Study: WSL Git Credential Gap

On this Windows host (WSL + git-bash), the most frequent subprocess hang involves `git push origin` on GitHub HTTPS remotes running inside WSL.

### Problem

WSL's git has **no credential helper configured** (empty `~/.gitconfig`). When `git push origin` runs against an HTTPS remote, it waits forever for a username/password prompt that has no TTY to read from:

```python
subprocess.run(["wsl", "bash", "--login", "-c", "git push origin"], timeout=120)
# → subprocess.TimeoutExpired after 120s
```

### Detection with GIT_TERMINAL_PROMPT=0

Adding the safety flag turns the silent hang into a clean, detectable failure:

```bash
export GIT_TERMINAL_PROMPT=0
git push origin
# → fatal: could not read Username for 'https://github.com': terminal prompts disabled
```

### Fix: Use Windows git.exe for GitHub

WSL can reach the Windows git binary, which has access to the Windows credential store:

```
/mnt/c/Program Files/Git/mingw64/bin/git.exe
```

```python
import subprocess
result = subprocess.run(
    ["wsl", "bash", "--login", "-c",
     f'"/mnt/c/Program Files/Git/mingw64/bin/git.exe" push origin'],
    capture_output=True, text=True, timeout=60
)
```

### Complementary Trap: ELF Remote Helpers

The reverse is also true — Windows `git.exe` **cannot** run WSL-native ELF binaries like `git-remote-rad` (Radicle P2P git transport). Attempting to push to a `rad://` remote via Windows git produces:

```
error: cannot spawn git-remote-rad: Exec format error
fatal: remote helper 'rad' aborted session
```

### Solution: Split Operations by Remote Type

When a repo has both GitHub (HTTPS) and a native-tool remote (Radicle, etc.), use the appropriate git for each:

```python
# GitHub → Windows git.exe (has credential store)
subprocess.run(["wsl", "bash", "--login", "-c",
    f'"/mnt/c/Program Files/Git/mingw64/bin/git.exe" push origin'],
    timeout=60)

# Radicle → WSL git (has ELF git-remote-rad binary)
subprocess.run(["wsl", "bash", "--login", "-c",
    "export PATH=\"$HOME/.radicle/bin:$PATH\" && "
    "export RAD_PASSPHRASE=\"...\" && "
    "git push rad --all"],
    timeout=60)
```

## Pitfalls

- **Silent false negative** — when a command that hangs also suppresses stderr (e.g., `git push 2>/dev/null` or `|| echo "issue"`), the hang causes `TimeoutExpired` but the error message that would explain *why* is lost. Always capture stderr separately for debugging.
- **Environment-specific** — the same `git push origin` command works from PowerShell/CMD (because Windows Git Credential Manager provides the credentials) but hangs in WSL. The fix is to use the right git binary for the context.
- **Cascade failures** — when the first command in a script hangs (e.g., `git push origin` before `git push rad`), the timeout kills the entire script and the second remote is never reached. Always process remotes independently with individual timeouts and error handling.
- **Wrong timeout diagnosis** — a script that ran in 30 seconds last week and now takes 180 seconds to timeout is likely hanging, not running slower. Check for environment changes (proxy, credential expiry, new prompt).
- **Non-git prompts** — `ssh -T git@github.com` can also hang if the host key isn't in `known_hosts` and `StrictHostKeyChecking` is `ask` (the default). Always set `StrictHostKeyChecking=no` (or `accept-new`) in cron contexts.

## Related Failure: Exit Code 15 — Orphaned Subprocess Killed by SIGTERM

This is distinct from the TTY-hang pattern above but frequently appears in the same cron/Python-wrapper environments.

**Symptom:** `Script exited with code 15` (SIGTERM) — the script or a child process was killed, not timed out.

**Root cause:** The Python wrapper spawns a subprocess (e.g. via `subprocess.Popen`), the wrapper finishes its main work and exits, but the child process is still running. When the parent's process tree is dismantled, the OS sends SIGTERM to the orphaned child. The child's exit code 15 appears in cron output *after* the wrapper's normal output, often interleaved.

**Key diagnostic: exit code 15 vs related codes**

| Exit Code | Meaning | Common Cause |
|-----------|---------|-------------|
| **15** | SIGTERM | Orphaned subprocess killed after parent exited |
| **124** | Timeout | Scheduler or `subprocess.run(timeout=N)` killed the process |
| **127** | Command not found | PATH issue in cron environment |
| **1+** | Explicit error | Python exception or `sys.exit(N)` |

**Fix patterns (in priority order):**

1. **Use `subprocess.run()` with `communicate()` instead of `Popen`** — synchronous subprocesses don't leak:

   ```python
   # SAFE: blocks until subprocess finishes
   result = subprocess.run([...], capture_output=True, timeout=120)
   ```

2. **If `Popen` is necessary, explicitly wait and clean up:**

   ```python
   procs = []
   try:
       p = subprocess.Popen([...], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
       procs.append(p)
       stdout, stderr = p.communicate(timeout=120)
   finally:
       for p in procs:
           if p.returncode is None:  # still running
               p.terminate()
               try:
                   p.wait(timeout=5)
               except subprocess.TimeoutExpired:
                   p.kill()
   ```

3. **Use `subprocess.Popen` as a context manager** (Python 3.12+):

   ```python
   with subprocess.Popen([...]) as p:
       try:
           p.wait(timeout=120)
       except subprocess.TimeoutExpired:
           p.kill()
           raise
   ```

4. **Flatten the process tree** — if the Python wrapper is shelling out to `bash -s` which then shells out to `python script.py`, call the target script's function directly (via `import` and `sys.path.insert`). Fewer layers = fewer orphan opportunities.

**Where this commonly appears:**
- Cron data-collection scripts that do `subprocess.run([...])` then `print(...)` before the subprocess finishes
- Wrappers that fire-and-forget a bash process to run in the background
- Scripts using `subprocess.Popen(...).communicate(timeout=N)` where the timeout fires but the cleanup code doesn't fully reap the process

## Related

- `windows-cross-platform-debugging` skill — broader Windows/WSL compatibility patterns (CRLF, MSYS path translation, USERPROFILE, `git -C` failures)
- `cron-watchdog` skill — monitoring cron job health and re-firing missed jobs
- `systematic-debugging` skill — general-purpose debugging methodology
