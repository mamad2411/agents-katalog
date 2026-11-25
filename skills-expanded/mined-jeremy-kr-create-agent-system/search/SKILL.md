---
name: search
description: "Search the community registry for agents/skills/presets."
user-invocable: true
allowed-tools: Bash(npx:*)
---

# /search

Search the community registry for agents, skills, and presets.

## Usage

```bash
npx create-agent-system search <query> [options]
```

Options:
- `--type <type>` — Filter by item type (agent, skill, preset)
- `--tag <tag>` — Filter by tag

## Examples

```bash
# Keyword search
npx create-agent-system search testing

# Filter by type
npx create-agent-system search --type skill testing

# Filter by tag
npx create-agent-system search --tag security

# Browse full listing
npx create-agent-system list
npx create-agent-system list --type agent
```

## Results

Search results include name, description, type, and tags, sorted by relevance.
Use the `/add` command to install any item you find.
