# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a dotfiles repository containing zsh configuration for development containers. It's a single-file version of [Amabel/dotfiles](https://github.com/Amabel/dotfiles) designed for easy use in dev-containers.

## Repository Structure

- `.zshrc` - Main zsh configuration file with oh-my-zsh setup, aliases, and peco history search
- `README.md` - Basic repository description
- `.claude/` - Claude Code configuration directory (synced from local ~/.claude)
- `sync-claude-config.sh` - Script to sync Claude configuration from local machine

## Shell Configuration Details

The `.zshrc` file configures:
- oh-my-zsh with "ys" theme
- Git plugins (git, git-open)
- Common aliases for file operations and utilities
- Peco-based history search functionality (Ctrl+R)

## Dependencies

The configuration expects these tools to be available:
- oh-my-zsh framework
- peco (for history search functionality)
- git-open plugin (needs manual installation)

## Claude Configuration

The `.claude/` directory contains Claude Code configuration including:
- `commands/` - Custom slash commands for common development tasks
- `templates/` - Code templates and conventions
- `agents/` - Custom agents for specialized development tasks
- `settings.json` - Claude Code settings and preferences

### Syncing Claude Configuration

Use the `sync-claude-config.sh` script to sync your local Claude configuration:

```bash
./sync-claude-config.sh
```

This script will copy the following from `~/.claude/` to the repository's `.claude/` directory:
- commands/ directory
- templates/ directory
- agents/ directory
- settings.json file

## Usage in Development Containers

This dotfiles setup is designed to be copied into development containers to provide a consistent shell environment. The single `.zshrc` file contains all necessary configuration without requiring complex directory structures. The Claude configuration can be copied to `~/.claude/` in containers to maintain consistent Claude Code settings.