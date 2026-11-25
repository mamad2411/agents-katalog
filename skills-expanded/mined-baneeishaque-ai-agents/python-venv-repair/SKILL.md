---
name: python-venv-repair
description: Industrial protocol for detecting, diagnosing, and repairing broken Python virtual environments including circular symlinks, missing interpreters, and orphaned package installations.
category: Environment-Management
---

# Python Virtual Environment Repair Skill

This skill defines the protocol for repairing broken Python virtual environments (`venv`).
A venv is considered broken when its interpreter symlinks resolve to non-existent targets,
creating circular chains or dead references (commonly caused by Homebrew upgrades, Python
version removals, or filesystem moves).

```text
Layer 1: Symlink & Interpreter Diagnosis   (base — identifies what is broken)
└── Layer 2: Python Interpreter Discovery   (finds available replacement interpreters)
    └── Layer 3: Decision Gate              (fix symlink / recreate venv / install Python)
        └── Layer 4: Reconstruction          (rebuilds venv and reinstalls packages)
            └── Layer 5: Verification        (confirms tool works end-to-end)
```

***

## 1. Layer 1 — Symlink & Interpreter Diagnosis

When a `venv/bin/` command fails with a shebang error (e.g., `bad interpreter: ... no such
file or directory`), the agent MUST audit the entire `bin/` directory before proposing
any fix.

### 1.1 Broken Symlink Scan

```bash
# Find ALL symlinks in the venv bin directory and show their targets
find /path/to/venv/bin -type l -exec ls -la {} \;
```

- `find /path/to/venv/bin -type l` — Locates every symlink under `bin/`.
- `-exec ls -la {} \;` — Prints each symlink with its raw target (before resolution).

### 1.2 Broken Symlink Detection

```bash
# List ONLY symlinks whose targets do not exist
find /path/to/venv/bin -type l ! -exec test -e {} \; -print
```

- `-type l` — Match only symlinks.
- `! -exec test -e {} \;` — Filter to those where the target file does **not** exist.
- `-print` — Output the broken symlink paths.

### 1.3 Circular Symlink Detection

```bash
# Attempt to execute the venv's python — reveals circular chains
/path/to/venv/bin/python --version 2>&1
/path/to/venv/bin/python3 --version 2>&1
```

If the output contains `too many levels of symbolic links` or `no such file or directory`,
the venv's interpreter chain is broken.

### 1.4 Pyvenv Config Check

```bash
# Read the venv's metadata — shows the original base Python path
cat /path/to/venv/pyvenv.cfg
```

Key fields:
- `home` — The original directory of the base Python interpreter.
- `version` — The Python version the venv was created with.
- `executable` — The absolute path to the original Python binary.

Compare the `home`/`executable` values against the current filesystem. If the path no
longer exists, the venv is orphaned and MUST be recreated (not just symlink-fixed).

### 1.5 Diagnosis Summary

After running all checks, the agent MUST present a summary:

```text
Venv              : /path/to/venv
Created with      : python 3.14 (from /opt/homebrew/opt/python@3.14/bin/python3.14)
Base interpreter   : MISSING (path no longer exists)
Broken symlinks   : 3 of 12 (python, python3, python3.14)
Circular chain    : YES (python → python3 → python)
Venv packages     : Orphaned (cannot be recovered)
```

***

## 2. Layer 2 — Python Interpreter Discovery

Before proposing a repair, the agent MUST discover all available Python interpreters on
the system.

### 2.1 System PATH Search

```bash
# Find all python3 interpreters reachable on PATH
which -a python3 2>/dev/null
which -a python3.11 2>/dev/null
which -a python3.12 2>/dev/null
which -a python3.13 2>/dev/null
which -a python3.14 2>/dev/null
```

- `which -a` — Lists **all** matches on `PATH`, not just the first one.
- `2>/dev/null` — Suppresses "not found" errors for versions that don't exist.

### 2.2 Mise-Managed Interpreters

```bash
# List all Python versions installed under mise
mise ls python --json 2>/dev/null
```

Each JSON element contains:
- `version` — Installed version string.
- `install_path` — Filesystem path to the installation.
- `active` — Whether it is the currently active version.
- `source.path` — Which `mise.toml` declared it.

### 2.3 Homebrew Interpreters

```bash
# List all Python versions installed via Homebrew
ls /opt/homebrew/Cellar/python*/ 2>/dev/null
ls /opt/homebrew/opt/python*/bin/python* 2>/dev/null
```

### 2.4 Available Interpreter Summary

The agent MUST compile all findings into a table:

```text
Available Python interpreters:
  ① python 3.11.9  (mise, active) → /Users/dk/.local/share/mise/installs/python/3.11.9/bin/python3
  ② python 3.12.3  (homebrew)     → /opt/homebrew/bin/python3.12
  ③ python 3.14.0  (MISSING)      → /opt/homebrew/opt/python@3.14/bin/python3.14
```

***

## 3. Layer 3 — Decision Gate

Based on the diagnosis (§1) and available interpreters (§2), the agent MUST present
repair options sorted by priority and ask the user to choose.

### 3.1 Option Priority

| Priority | Option | When to Recommend |
| :--- | :--- | :--- |
| **1st** | Recreate venv with available Python | Base interpreter is completely gone (removed Homebrew, uninstalled version) |
| **2nd** | Fix root symlink to local `python3` | The venv's `lib/` and `site-packages/` are intact; only symlinks are broken |
| **3rd** | Install missing Python version | The venv has irreplaceable compiled extensions or version-locked dependencies |

### 3.2 Presentation to User

The agent MUST present the analysis and ask:

```text
Diagnosis: Python 3.14 (base interpreter) was removed. The venv's lib/ packages
           are orphaned and cannot be used with a different Python version.

Available: python 3.11.9 (mise, active)

Option 1 (Recommended): Recreate venv with python 3.11.9 and reinstall bashhub.
  → Clean, guaranteed to work. Previous packages will need reinstallation.

Option 2: Install Python 3.14 and fix symlinks.
  → Preserves original setup. Requires installing Python 3.14 first.

Which would you prefer? (1 / 2)
```

### 3.3 User Decision Gate

- **Option 1** → proceed to Layer 4 (Recreation).
- **Option 2** → install Python via [Mise Tool Management Skill](../../../.agents/skills/mise-tool-management/SKILL.md) or
  `brew install python@3.14`, then proceed to §4.2 (Symlink Fix).

***

## 4. Layer 4 — Reconstruction

### 4.1 Venv Recreation (Primary Path)

```bash
# Remove the broken venv entirely
rm -rf /path/to/venv

# Create a new venv using the available Python interpreter
/absolute/path/to/python3 -m venv /path/to/venv
```

- `rm -rf /path/to/venv` — Deletes the entire broken environment. No recovery is
  possible for `site-packages/` when the base Python version changes.
- `/absolute/path/to/python3 -m venv` — Uses the `venv` module from a known-good
  Python to create a fresh environment at the same path.

### 4.2 Symlink Fix Only (When lib/ is salvageable)

**Only use this path when the base Python version still exists on disk but the symlink
chain is corrupted.** If the base interpreter is gone, §4.1 MUST be used instead.

```bash
# Remove all broken python symlinks in bin/
find /path/to/venv/bin -maxdepth 1 -name 'python*' -type l ! -exec test -e {} \; -delete

# Create fresh symlinks pointing to the working local python3
ln -s python3 /path/to/venv/bin/python
```

- `find ... -maxdepth 1 -name 'python*' -type l ! -exec test -e {} \; -delete` — Removes
  only the broken `python*` symlinks in `bin/`, leaving all other venv scripts untouched.
- `ln -s python3 ...` — Creates a relative symlink from `python` to `python3` within
  the same directory, avoiding absolute path brittleness.

### 4.3 Package Reinstallation

If a `requirements.txt` or `pip freeze` snapshot is available from the old venv:

```bash
# Attempt to recover package list from the broken venv (if lib/ is intact)
/path/to/venv/lib/pythonX.Y/site-packages/  # inspect manually

# Or reinstall known packages into the new venv
/path/to/venv/bin/pip install <package-name>
```

If the old venv's `site-packages/` is unusable (different Python version), the agent
MUST ask the user which packages need reinstalling.

### 4.4 Installation Verification

```bash
# Confirm the tool works and reports the correct version
/path/to/venv/bin/<tool> --version
```

***

## 5. Layer 5 — End-to-End Verification

After reconstruction, the agent MUST run a full verification suite:

### 5.1 Interpreter Check

```bash
# Verify the venv's python resolves correctly
/path/to/venv/bin/python --version
/path/to/venv/bin/python3 --version
```

Both MUST return the same version without errors.

### 5.2 Symlink Audit

```bash
# Confirm no broken symlinks remain in bin/
find /path/to/venv/bin -type l ! -exec test -e {} \; -print
```

Expected output: **empty** (no broken symlinks).

### 5.3 Tool Execution Test

```bash
# Run the actual tool that triggered the repair
/path/to/venv/bin/<tool> --help 2>&1 | head -5
```

This confirms the shebang line works and the tool's dependencies are resolvable.

### 5.4 User Notification

If the user needs to restart their shell for changes to take effect (e.g., bashhub
shell init scripts), the agent MUST notify them:

```text
Venv repaired successfully. Restart your shell (or run `exec zsh` / `exec bash`)
for the fix to take effect.
```

***

## 6. Prohibited Actions

The agent is FORBIDDEN from:

- **Creating symlinks to absolute Homebrew paths** — always use relative symlinks
  (`ln -s python3 ...`) to avoid path brittleness across upgrades.
- **Recreating a venv without user approval** — the agent MUST present the diagnosis
  and available interpreters first, then ask for confirmation.
- **Attempting to use `site-packages/` from a different Python version** — compiled
  extensions (`.so` / `.dylib`) are version-specific and will crash silently.
- **Running `pip install` into a broken venv** — the interpreter must be verified
  working (§5.1) before any package operations.
- **Assuming `python` symlink exists** — since Python 3.11+, `python3` is the default;
  `python` may be absent in newly created venvs. The agent MUST check for both.
