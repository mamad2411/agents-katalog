---
name: usync
description: Sync Claude/OpenCode/Codex/Gemini/Kiro/Qoder/Cursor settings and skills to GitHub Gist. Migrate MCP configs and skills between AI coding tools with format conversion.
---

# usync - AI CLI Config Sync

Sync configurations and skills from Claude, OpenCode, Codex, Gemini, Kiro, Qoder, and Cursor to GitHub Gist for backup and cross-machine sync. Migrate MCP configs between tools with automatic format conversion.

## When to Use

- Backing up AI CLI tool settings and skills to the cloud
- Syncing configurations across multiple machines
- Restoring AI CLI configs on a new machine
- Auto-syncing config changes with watch mode
- Managing settings for multiple AI CLI tools in one place
- Migrating MCP configs and skills between different AI coding tools
- Converting MCP config formats (JSON mcpServers, OpenCode mcp, Codex TOML)

## Quick Start

```bash
# Install
pnpm add -g usync-cli

# Initialize → verify token and create a Gist
usync init

# Scan → list all discovered config files
usync scan

# Upload → sync local configs to Gist
usync upload --gist-id <id>

# Download → restore configs from Gist
usync download --gist-id <id>

# Watch mode → auto-upload on changes
usync upload --gist-id <id> --watch
```

## Supported Providers

| Provider | Global Config | Project Config |
|----------|---------------|----------------|
| Claude | `~/.claude.json`, `~/.claude/settings.json`, `~/.claude/skills/` | `.mcp.json`, `.claude/settings.json`, `.claude/skills/` |
| OpenCode | `~/.config/opencode/opencode.json(.jsonc)`, `~/.config/opencode/skills/` | `opencode.json(.jsonc)`, `.opencode/skills/` |
| Codex | `~/.codex/config.toml`, `~/.codex/config.json`, `~/.codex/skills/` | `.codex/config.toml`, `.codex/skills/` |
| Gemini | `~/.gemini/settings.json`, `~/.gemini/extensions/`, `~/.gemini/skills/` | `.gemini/settings.json`, `.gemini/skills/` |
| Kiro | `~/.kiro/settings/mcp.json`, `~/.kiro/skills/` | `.kiro/settings/mcp.json`, `.kiro/steering/` |
| Qoder | `~/.qoder/mcp.json`, `~/.qoder/skills/` | `.qoder/mcp.json`, `.qoder/skills/` |
| Cursor | `~/.cursor/mcp.json`, `~/.cursor/rules/`, `~/.cursor/skills/` | `.cursor/mcp.json`, `.cursor/rules/`, `.cursor/skills/` |

## Commands

| Command | Description | Reference |
|---------|-------------|-----------|
| `usync init` | Verify token, create or validate Gist | [command-init](references/command-init.md) |
| `usync scan` | List discovered local config files | [command-scan](references/command-scan.md) |
| `usync upload` | Upload configs to GitHub Gist | [command-upload](references/command-upload.md) |
| `usync download` | Download and restore configs from Gist | [command-download](references/command-download.md) |
| `usync migrate` | Migrate MCP configs and skills between tools | [command-migrate](references/command-migrate.md) |

## References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Getting Started | Setup, token creation, first sync | [guide-getting-started](references/guide-getting-started.md) |
| Providers | All supported providers and config paths | [reference-providers](references/reference-providers.md) |
| Architecture | Template paths, manifest, incremental sync | [reference-architecture](references/reference-architecture.md) |

## Token Setup

usync-cli requires a GitHub Personal Access Token with `gist` scope:

1. Go to https://github.com/settings/tokens/new
2. Select scope: **gist**
3. Generate and save the token

Token resolution order:
1. `--token <PAT>` flag
2. Environment variable (default: `GITHUB_TOKEN`, or custom via `--token-env`)
3. `GH_TOKEN` fallback

## Common Patterns

### First-time setup

```bash
# Set token in environment
export GITHUB_TOKEN=ghp_xxx

# Initialize and create a new Gist
usync-cli init

# Upload all configs
usync-cli upload --gist-id <id-from-init>
```

### Restore on new machine

```bash
export GITHUB_TOKEN=ghp_xxx
usync-cli download --gist-id <id>
```

### Watch mode for continuous sync

```bash
usync-cli upload --gist-id <id> --watch --interval 30
```

### Filter specific providers

```bash
usync scan --providers Claude,opencode
usync upload --gist-id <id> --providers Claude
```

### Migrate between tools

```bash
# Migrate from Claude Code to Kiro
usync migrate --from claude --to kiro

# Dry-run preview
usync migrate --from codex --to claude --dry-run

# Force overwrite existing files
usync migrate --from claude --to kiro --yes --overwrite

# Migrate project-level configs
usync migrate --from claude --to kiro --scope project
```

## Security

- Sensitive files are auto-excluded: `.env*`, `.key`, `.pem`, `.p12`
- File contents are base64-encoded in the Gist
- Use private Gists (default) for security
- Tokens are never stored locally → use env vars

## Tech Stack

- **CLI Framework**: citty (unjs)
- **Interactive Prompts**: @clack/prompts
- **Logging**: consola + colorette
- **Build**: tsdown
- **Path Handling**: pathe (cross-platform)
- **Package Manager**: pnpm
- **Versioning**: changesets
