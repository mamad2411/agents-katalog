# /backup — Claude Code Settings Backup

Back up all Claude Code settings to GitHub. Scans every scope (global + all projects), exports memories, skills, rules, MCP configs, settings, plans, agents, commands, sessions, and plugins. Then commits and pushes to your configured backup repo. On Windows it also backs up your WSL distros' stores as separate environments.

## Usage

- `/backup` — Run a backup now (Windows + any WSL distros)
- `/backup init` — First-time setup (create repo via `gh`, configure remote, install scheduler)
- `/backup status` — Show last backup time, environments, and scheduler status
- `/backup restore` — Preview restoring from backup (dry-run); add `--apply` to write

## What it does

1. **Discovers** environments (Windows-native + WSL distros, or a single native store)
2. **Scans** all Claude Code customizations across every scope, per environment
3. **Exports** 10 categories: memory, skill, mcp, config, rule, agent, command, plan, session, plugin — under `latest/<envId>/` when more than one environment exists
4. **Commits** changes to `~/.claude-backups/` git repo and **pushes** to your private GitHub repo

## Restore

`/backup restore` previews (dry-run) restoring every backed-up file to its real location on the current machine; `--apply` performs it. Handles new usernames, cross-OS restores (path re-encoding), and restoring into WSL from Windows.

## Setup (first time only)

```bash
npx @seangsisg/claude-code-backup init
```

This creates `~/.claude-backups/`, creates a private GitHub repo (via the `gh` CLI, if available) or asks for a repo URL, and installs a systemd timer (Linux), LaunchAgent (macOS), or Task Scheduler task (Windows) for automatic backups.

## Requirements

- Node.js 18+
- A GitHub repo (auto-created via the `gh` CLI, or provide a URL)
- `@seangsisg/claude-code-backup` installed (`npm i -g @seangsisg/claude-code-backup`)
