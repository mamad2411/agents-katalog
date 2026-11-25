---
name: skill-dashboard-for-kimi
url: https://github.com/ktkarchive/skill-dashboard-for-kimi
category: system
---

# skill-dashboard-for-kimi

A web dashboard for managing CLI skills and MCP servers. Originally developed for Kimi CLI, but compatible with Claude Code, Codex CLI, OpenCode CLI, and any CLI that stores skills as markdown files with YAML frontmatter.

## What it does

- Scans your skills directory and MCP config
- Displays all skills and MCP servers in a sortable, filterable table
- Shows health status, categories, descriptions, and links
- Supports activation/deactivation (registry-based toggle)
- Supports inline editing of category, description, and URL
- Supports permanent deletion of skills with confirmation
- Runs a local web server (default port 8080)

## Installation

### Option A: Kimi CLI Skill (Recommended)

```bash
cd ~/.kimi/skills/
git clone https://github.com/ktkarchive/skill-dashboard-for-kimi.git
```

Then tell Kimi: **"Launch the skill dashboard"**

### Option B: Standalone

```bash
git clone https://github.com/ktkarchive/skill-dashboard-for-kimi.git
cd skill-dashboard-for-kimi
python3 scripts/skill_dashboard.py --port 8080 --open
```

## Cross-CLI Compatibility

The script defaults to Kimi CLI paths (`~/.kimi/skills/` and `~/.kimi/mcp.json`). To use with another CLI, edit the paths at the top of `scripts/skill_dashboard.py`:

| CLI | Skills Dir | MCP Config |
|-----|-----------|------------|
| Kimi (default) | `~/.kimi/skills/` | `~/.kimi/mcp.json` |
| Claude Code | `~/.claude/skills/` | `~/.claude/mcp.json` |
| Codex CLI | `~/.codex/skills/` | `~/.codex/mcp.json` |
| OpenCode | `~/.opencodes/skills/` | `~/.opencodes/mcp.json` |

## Dashboard Features

| Feature | Description |
|---------|-------------|
| Sort | Click any table header to sort |
| Filter | Search by name, category, status, or type |
| Toggle | Enable/disable skills or MCP servers |
| Edit | Click Detail to edit category, description, and URL |
| Remove | Click Remove and type "remove" to permanently delete a skill |
| Health | Automatic health check for SKILL.md and YAML frontmatter |

## License

MIT
