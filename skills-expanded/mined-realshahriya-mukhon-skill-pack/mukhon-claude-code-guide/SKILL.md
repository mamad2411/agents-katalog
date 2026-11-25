---
name: mukhon-claude-code-guide
description: Comprehensive reference, CLI cheat sheet, and architectural guide for Anthropic Claude Code. Covers interactive terminal workflows, headless automation (claude -p), CLAUDE.md project context design, Model Context Protocol (MCP) tool integration, custom slash commands, thinking modes, and autonomous agent safety. Use when setting up, configuring, or pairing with Claude Code.
license: MIT
---

# Anthropic Claude Code Guide & Architecture

Claude Code is Anthropic's agentic command-line interface and AI coding assistant designed to operate directly in local development environments with terminal, git, and filesystem autonomy.

## When to Use This Skill

- Configuring and running Claude Code for terminal-based pair programming.
- Authoring high-impact `CLAUDE.md` repository instruction and style files.
- Configuring Model Context Protocol (MCP) servers (`claude mcp add`).
- Integrating Claude Code into CI/CD pipelines and shell scripts (`claude -p`).
- Managing context window limits, extended thinking tokens, and permissions.

## Architectural Components

```
[ Developer Terminal ] ◄──► [ Claude Code CLI Runtime ]
                                     │
       ┌─────────────────────────────┼─────────────────────────────┐
       ▼                             ▼                             ▼
[ CLAUDE.md Memory ]       [ MCP Tool Ecosystem ]       [ Shell & Git Engine ]
 - Architecture rules       - Local DB / DevTools        - Bash execution
 - Build / test commands    - Documentation servers      - File read / write / edit
 - Code formatting norms    - Web browsing               - Multi-file atomic diffs
```

## Detailed Reference Subdocs

1. [CLI Workflows & Flags](references/cli.md): Interactive shell commands, flags, compacting context (/compact), and custom slash commands.
2. [CLAUDE.md Architecture](references/claude-md.md): Standard layout for repository instructions, code conventions, memory persistence, and monorepo configurations.
3. [MCP Server Integration](references/mcp.md): Adding, inspecting, and managing Model Context Protocol servers in `~/.claude.json` and project settings.
4. [Safety & Permissions](references/safety.md): Tool allowlisting, execution sandboxing, and non-interactive CI safeguards.
