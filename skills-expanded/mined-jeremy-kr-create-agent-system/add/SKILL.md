---
name: add
description: "Install agents/skills/presets from the community registry. Use to extend your project."
user-invocable: true
allowed-tools: Bash(npx:*), Read, Write, Glob
---

# /add

Search and install agents, skills, and presets from the community registry into your project.

## Usage

```bash
npx create-agent-system add <names...> [options]
```

Options:
- `--type <type>` — Filter by item type (agent, skill, preset)
- `--force` — Overwrite existing files
- `--yes, -y` — Skip confirmation prompts

## Examples

```bash
# Install by name
npx create-agent-system add security-reviewer

# Specify type
npx create-agent-system add --type agent security-reviewer

# Install multiple items at once
npx create-agent-system add security-reviewer tdd-workflow api-testing

# Force overwrite
npx create-agent-system add security-reviewer --force
```

## Dependency resolution

If an item has dependencies, they are automatically detected and you'll be prompted to install them together.
For example, if an agent references a specific skill, that skill will also be suggested for installation.

## Installation paths

| Type | Path |
|------|------|
| agent | `.claude/agents/<name>.md` |
| skill | `.claude/skills/<name>/SKILL.md` |
| preset | `presets/<name>.yaml` |
