---
name: update-dotfiles
description: Update Cursor and environment from the user's dotfiles repo. Use when the user wants to pull the latest dotfiles and re-run the install script (e.g. after pushing changes, or to refresh skills/commands/agents/extensions/MCP in this codespace).
---
# Update from dotfiles

When the user asks to update from their dotfiles, pull the latest version and re-run the install script so Cursor picks up new or changed skills, commands, subagents, extensions, MCP config, and settings.

## Steps

1. **Go to the dotfiles repo**
   In GitHub Codespaces the dotfiles repo is always at: `/workspaces/.codespaces/.persistedshare/dotfiles`

2. **Pull latest**
   - `cd /workspaces/.codespaces/.persistedshare/dotfiles` then `git pull`.
   - If there are local changes or merge conflicts, report and ask how to proceed (e.g. stash, reset, or merge).
   - If there are NO new changes pulled, then stop here.

3. **Re-run install**
   - If there are new changes pulled, then from that directory run: `bash install.sh`
   - Report success or any errors (e.g. missing `code`, `jq`, or permission issues).

4. **Remind the user**
   If they added or changed skills, commands, or subagents, they may need to reload Cursor or start a new chat for the agent to see the updates.
