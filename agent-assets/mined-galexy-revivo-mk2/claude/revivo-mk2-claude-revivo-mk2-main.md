<!-- ox:prime-check -->
**BLOCKING**: Run `ox agent prime` NOW before ANY other action. Do NOT respond to the user first. Enables SageOx queries.

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Claude Code devcontainer starter template** — a blank project with a pre-configured development environment. There is no application source code yet; the repo provides the container infrastructure for developing with Claude Code.

## Environment

- **Container**: Debian Bookworm-slim devcontainer running as `vscode` user
- **Shell**: zsh (with fzf integration)
- **Editor**: Helix (`hx`) is the configured `$EDITOR`/`$VISUAL`
- **Workspace**: `/workspace` (bind-mounted from host)
- **Available tools**: git, gh (GitHub CLI), docker CLI, tmux, jq, curl, wget

## Devcontainer Details

- On start, a whitelist-only firewall is initialized (`init-firewall.sh`) that restricts outbound traffic to known services (GitHub, npm, PyPI, crates.io, Anthropic APIs, VS Code marketplace)
- A tmux session named `main` is auto-created on container start
- Docker socket is bind-mounted for container-in-container workflows
- VS Code extensions pre-installed: Claude Code, ESLint, Prettier, GitLens
- Prettier is the default formatter with format-on-save enabled

## Firewall

Outbound network access is restricted. Allowed destinations:
- GitHub (API + SSH)
- npm, PyPI, crates.io, Rust static assets
- Anthropic APIs, Claude update server
- VS Code marketplace
- Local/private networks (172.17.0.0/16, 192.168.0.0/16, 10.0.0.0/8)

To allow additional domains, edit `.devcontainer/init-firewall.sh` and add `allow_domain "example.com"` entries.

<!-- ox:prime --> Run SageOx `ox agent prime` on session start, after compaction, or clear. (DO NOT REMOVE)
