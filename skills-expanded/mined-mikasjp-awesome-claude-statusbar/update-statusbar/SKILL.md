---
name: update-statusbar
description: Update the awesome-claude-statusbar installation by pulling the latest version from GitHub and running the installer.
disable-model-invocation: true
allowed-tools: Bash(bash:*), Bash(sh:*), Bash(git:*), Bash(pwsh:*), Read
---

# Update Awesome Claude Statusbar

Pull the latest version of awesome-claude-statusbar and reinstall it.

## Steps

1. **Update the local clone**
   - If `~/.claude/awesome-claude-statusbar` does not exist, clone it:
     `git clone https://github.com/mikasjp/awesome-claude-statusbar.git ~/.claude/awesome-claude-statusbar`
   - Otherwise pull the latest changes:
     `git -C ~/.claude/awesome-claude-statusbar pull`

2. **Run the installer**
   - On macOS/Linux: `bash ~/.claude/awesome-claude-statusbar/install.sh`
   - On Windows: `pwsh -NoProfile -File ~/.claude/awesome-claude-statusbar/install.ps1`

3. **Report the result** to the user and remind them to restart Claude Code if the update succeeded.
