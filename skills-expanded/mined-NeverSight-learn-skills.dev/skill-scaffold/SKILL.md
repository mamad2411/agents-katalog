---
name: skill-scaffold
description: AI agent skill scaffolding CLI. Create Clawdbot, Moltbot, Claude, and MCP skills instantly. Perfect for vibe coding.
author: tytaninc7
version: 1.0.0
keywords:
  - ai
  - agent
  - skill
  - scaffold
  - generator
  - clawdbot
  - moltbot
  - mcp
  - claude
  - cursor
  - vibe-coding
---

# Skill Scaffold

Create AI agent skills in seconds. Supports Clawdbot/Moltbot, MCP servers, and generic skill structures.

## Trigger Words

Use this skill when the user mentions:
- "create a skill"
- "scaffold a skill"
- "new skill template"
- "skill generator"
- "make a clawdbot skill"
- "mcp server template"

## Quick Start

```bash
# Install globally
npm install -g skill-scaffold

# Create a Clawdbot skill
skill-scaffold my-awesome-skill

# Create an MCP server
skill-scaffold my-api --template mcp

# With all options
skill-scaffold weather-bot --template clawdbot --cli --description "Weather alerts for agents"
```

## Commands

| Command | Description |
|---------|-------------|
| `skill-scaffold <name>` | Create skill with default (clawdbot) template |
| `skill-scaffold <name> --template mcp` | Create MCP server scaffold |
| `skill-scaffold <name> --template generic` | Create minimal skill |
| `skill-scaffold <name> --cli` | Include CLI binary scaffold |
| `skill-scaffold --help` | Show help |

## Templates

### Clawdbot (default)
Full skill structure for Clawdbot/Moltbot agents:
- SKILL.md with YAML frontmatter, trigger words, commands table
- README.md with badges, installation, features
- scripts/ folder for helpers

### MCP
Model Context Protocol server scaffold:
- SKILL.md with MCP config examples
- Tools and resources documentation
- Ready for Claude Desktop/Cursor integration

### Generic
Minimal structure:
- Basic SKILL.md
- Simple README.md

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--template <type>` | Template: clawdbot, mcp, generic | clawdbot |
| `--author <name>` | Author name | NextFrontierBuilds |
| `--description <text>` | Skill description | Auto-generated |
| `--dir <path>` | Output directory | Current directory |
| `--cli` | Include CLI binary scaffold | false |
| `--no-scripts` | Skip scripts folder | false |

## Usage Examples

```bash
# Create in current directory
skill-scaffold my-skill

# Create in specific directory
skill-scaffold my-skill --dir ~/clawd/skills

# MCP server with custom author
skill-scaffold github-mcp --template mcp --author "YourName"

# Full CLI tool
skill-scaffold awesome-cli --cli --description "Does awesome things"
```

## Output Structure

```
my-skill/
├── SKILL.md       # Main documentation (Clawdbot reads this)
├── README.md      # GitHub/npm readme
├── scripts/       # Helper scripts (optional)
└── bin/           # CLI binary (if --cli flag used)
    └── my-skill.js
```

## After Creating

1. `cd my-skill`
2. Edit SKILL.md with your actual documentation
3. Add implementation (scripts or bin/)
4. Test locally
5. Publish: `clawdhub publish .` or `npm publish`

## Notes

- Skill names must be lowercase with hyphens only
- SEO keywords are auto-included in generated files
- Works with Clawdbot, Moltbot, and any agent that reads SKILL.md
