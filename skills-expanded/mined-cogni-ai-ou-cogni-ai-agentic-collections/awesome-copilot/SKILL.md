---
name: awesome-copilot
description: >
  Community-contributed instructions, agents, skills, and configurations to help you make the most of GitHub Copilot.
  You MUST load this skill when dealing with Awesome GitHub Copilot.
license: MIT
---

# awesome-copilot

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- When looking for community-contributed instructions, agents, skills, and configurations for GitHub Copilot.
- When needing to install plugins or agentic workflows from the Awesome Copilot marketplace.
- When seeking examples of Copilot hooks, skills, or recipes for working with Copilot APIs.

## WHEN NOT TO USE

- When configuring built-in Copilot features unrelated to community plugins or awesome-copilot resources.

## Project Overview

The Awesome GitHub Copilot repository is a community-driven collection of custom agents and instructions designed to enhance GitHub Copilot experiences across various domains, languages, and use cases. The project includes:

- **Agents** - Specialized GitHub Copilot agents that integrate with MCP servers.
- **Instructions** - Coding standards and best practices applied to specific file patterns.
- **Skills** - Self-contained folders with instructions and bundled resources for specialized tasks.
- **Hooks** - Automated workflows triggered by specific events during development.
- **Workflows** - Agentic Workflows for AI-powered repository automation in GitHub Actions.
- **Plugins** - Installable packages that group related agents, commands, and skills around specific themes.

## Repository Structure

[Awesome Copilot Repository](https://github.com/github/awesome-copilot) structure:

```text
.
├── agents/           # Custom GitHub Copilot agent definitions (.agent.md files)
├── instructions/     # Coding standards and guidelines (.instructions.md files)
├── skills/           # Agent Skills folders (each with SKILL.md and optional bundled assets)
├── hooks/            # Automated workflow hooks (folders with README.md + hooks.json)
├── workflows/        # Agentic Workflows (.md files for GitHub Actions automation)
├── plugins/          # Installable plugin packages (folders with plugin.json)
├── docs/             # Documentation for different resource types
├── eng/              # Build and automation scripts
└── scripts/          # Utility scripts
```

## Core Process

### Install a Plugin

1. **Attempt direct installation**. For most users, the Awesome Copilot marketplace is already registered:
   ```bash
   copilot plugin install <plugin-name>@awesome-copilot
   ```

2. **Fallback for older versions or custom setups**. If the marketplace is unknown, register it first:
   ```bash
   copilot plugin marketplace add github/awesome-copilot
   copilot plugin install <plugin-name>@awesome-copilot
   ```

## Resources

| Resource | Description |
| -------- | ----------- |
| 🤖 **Agents** | Specialized Copilot agents that integrate with MCP servers |
| 📋 **Instructions** | Coding standards applied automatically by file pattern |
| 🎯 **Skills** | Self-contained folders with instructions and bundled assets |
| 🔌 **Plugins** | Curated bundles of agents and skills for specific workflows |
| 🪝 **Hooks** | Automated actions triggered during Copilot agent sessions |
| ⚡ **Agentic Workflows** | AI-powered GitHub Actions automations written in markdown |
| 🍳 **Cookbook** | Copy-paste-ready recipes for working with Copilot APIs |

## References

- [Awesome Copilot llms.txt](https://awesome-copilot.github.com/llms.txt) (Overview, Learning Hub, Agents, Instructions, Skills)
- [awesome-copilot's AGENTS.md](https://raw.githubusercontent.com/github/awesome-copilot/refs/heads/main/AGENTS.md)

## Related skills

- **copilot-cli**:
  Use this skill to interact with GitHub Copilot CLI for command execution and automation.
