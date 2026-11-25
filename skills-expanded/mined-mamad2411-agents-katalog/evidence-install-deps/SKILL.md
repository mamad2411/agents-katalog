---
name: evidence-install-deps
description: Use after environment-check reports missing tools — installs them, putting Python-based tools in a plugin-owned virtual environment instead of mutating the system Python. Triggers - "install evidence tools", "set up exiftool and ots", "fix missing forensics dependencies".
disable-model-invocation: true
allowed-tools: Bash(command *), Bash(brew *), Bash(uv *), Bash(mkdir *), Bash(test *), Bash(apt-get *), Bash(npm *), Read, Write
---

# Install Dependencies

Install the tools environment-check reported missing. Python-based tools go into a
virtual environment owned by this plugin, never into the system Python.

## When to use

- Immediately after environment-check reports something missing.
- On a fresh machine, as the second step of onboarding.

This skill is not invoked automatically. It changes the machine, so it runs only when
asked for by name.

## Resolve paths

```bash
PLUGIN_DATA_DIR="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/evidence-ops"
VENV_DIR="$PLUGIN_DATA_DIR/venv"
```

Every Python tool is afterwards invoked as `"$VENV_DIR/bin/<tool>"`. This keeps the
plugin working on systems where the system Python is externally managed and refuses
`pip install`.

## Procedure

### 1. Confirm what is missing

Run environment-check first if its results are not already at hand. Never install a
tool that is already present.

### 2. Get agreement

List exactly what will be installed, by which package manager, and where. Installing
software is a change to the user's machine — state it and wait for agreement before
running anything.

### 3. Install system packages

macOS:

```bash
brew install exiftool mediainfo rclone b3sum qpdf awscli
```

Debian or Ubuntu:

```bash
sudo apt-get update
sudo apt-get install -y libimage-exiftool-perl mediainfo rclone qpdf
```

`b3sum` is not in most distribution repositories; install it with `cargo install b3sum`
or from the project's release binaries. Treat it as optional and continue without it.

### 4. Install the Node tool

```bash
npm install -g single-file-cli
```

Only if web capture is wanted. Skip it otherwise and say so.

### 5. Create the plugin virtual environment

```bash
mkdir -p "$PLUGIN_DATA_DIR"
uv venv "$VENV_DIR"
uv pip install --python "$VENV_DIR/bin/python" opentimestamps-client bagit mat2
```

If `uv` is unavailable, fall back to `python3 -m venv "$VENV_DIR"` followed by
`"$VENV_DIR/bin/pip" install opentimestamps-client bagit mat2`.

### 6. Verify

Re-probe every tool that was just installed and confirm it now resolves. Report the
resolved path for each. If a tool still does not resolve, report the exact install
command and its exact error output — do not describe the install as successful.

## Output

- Tools installed on the system, and a virtual environment at `$VENV_DIR`.
- A summary listing each tool, its resolved path, and its version.

## Notes

- Never install with `sudo pip`. Never pass `--break-system-packages`.
- If the user declines an install, record which stages stay blocked and continue with
  the rest of the pipeline where possible.
