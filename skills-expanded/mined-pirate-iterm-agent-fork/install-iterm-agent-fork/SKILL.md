---
name: install-iterm-agent-fork
description: Install and set up pirate/iterm-agent-fork locally for iTerm2 agent-session forking. Use when a user asks to install, configure, repair, update, or verify the iTerm Agent Fork repo, AutoLaunch script, iTerm Python API launch, Cmd+Shift+F/Cmd+Shift+G key bindings, or optional casr cross-agent handoff support.
---

# Install iTerm Agent Fork

## Overview

Set up `pirate/iterm-agent-fork` by cloning or reusing a normal repo checkout, enabling the iTerm2 Python API, installing `fork_agent_here.py` into the iTerm2 scripts `AutoLaunch` directory, launching it with the iTerm2 Python API, and installing `casr` when needed for cross-agent handoff.

Prefer the bundled setup script for repeatable installs:

```bash
skills/install-iterm-agent-fork/scripts/setup_iterm_agent_fork.sh
```

## Workflow

1. Read the repo `README.md` if the local checkout exists; otherwise inspect the upstream README before changing anything.
2. Preserve local state. Avoid destructive git commands, branch resets, or file-wide rewrites. If a checkout already exists, reuse it unless the user explicitly asks to reclone.
3. Let the setup script detect iTerm2's configured scripts directory. It should use an existing iTerm custom scripts directory when present, otherwise use `$HOME/Library/Application Support/iTerm2/Scripts`.
4. Enable the iTerm2 Python API by setting `EnableAPIServer=true` and `AITermAPI=2`; configure `UseCustomScriptsFolder` and `CustomScriptsFolder` only when the user explicitly supplies `--scripts-dir`.
5. Install `fork_agent_here.py` with executable permissions. If replacing an existing installed copy, keep a timestamped backup unless the files are identical.
6. Install `casr` if missing and Cargo is available. Same-agent forks do not require it, but cross-agent handoff does.
7. Launch the installed script through iTerm2. Use the actual `Installed script:` path printed by the setup script:

```bash
osascript -e 'tell application "iTerm2" to launch API script named "'"$INSTALLED_SCRIPT"'"'
```

8. Verify setup:
   - `python3 -m py_compile "$INSTALLED_SCRIPT"`
   - `defaults read com.googlecode.iterm2 EnableAPIServer` reports enabled
   - `~/.cargo/bin/casr --version` when `casr` was installed
   - `defaults read com.googlecode.iterm2 GlobalKeyMap` contains `fork_agent_here_v2()` and `handoff_agent_here_v2()` after the script has run
   - `ps ax -o pid=,command= | rg 'fork_agent_here.py'` shows the iTerm-managed script process when iTerm is running

## Automation Script

Use `scripts/setup_iterm_agent_fork.sh` for the standard local setup. It defaults to:

- repo: the current `iterm-agent-fork` checkout containing the skill
- iTerm scripts dir: iTerm2's existing custom scripts directory when configured, otherwise `$HOME/Library/Application Support/iTerm2/Scripts`
- upstream: `https://github.com/pirate/iterm-agent-fork.git`

Useful options:

```bash
scripts/setup_iterm_agent_fork.sh --help
scripts/setup_iterm_agent_fork.sh --dry-run
scripts/setup_iterm_agent_fork.sh --scripts-dir "$CUSTOM_ITERM_SCRIPTS_DIR"
scripts/setup_iterm_agent_fork.sh --no-casr
scripts/setup_iterm_agent_fork.sh --no-configure-iterm
scripts/setup_iterm_agent_fork.sh --no-launch
```

Only pass `--scripts-dir` when the user asks to use a custom scripts folder. Passing it configures iTerm2 to use that folder. Do not assume another user's machine has a pre-created custom scripts directory.

If iTerm2 reports that the Python runtime is still installing, wait for the runtime install to finish and rerun only the launch command or rerun the setup script.

## Manual Fallback

If the script cannot be used, run the core README-equivalent steps:

```bash
REPO_DIR="/path/to/iterm-agent-fork"
git clone https://github.com/pirate/iterm-agent-fork.git "$REPO_DIR"
mkdir -p "$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch"
install -m 755 "$REPO_DIR/fork_agent_here.py" "$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch/fork_agent_here.py"
defaults write com.googlecode.iterm2 EnableAPIServer -bool true
defaults write com.googlecode.iterm2 AITermAPI -int 2
cargo install --git https://github.com/Dicklesworthstone/cross_agent_session_resumer
osascript -e 'tell application "iTerm2" to launch API script named "'"$HOME"'/Library/Application Support/iTerm2/Scripts/AutoLaunch/fork_agent_here.py"'
```
