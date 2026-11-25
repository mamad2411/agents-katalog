---
name: meta-builder
description: Creates Claude Code primitives (skills, commands, agents) following official best practices. Use when user wants to add new capabilities, workflows, or specialists. Asks clarifying questions to determine the right primitive type.
---

# Meta Builder

Creates skills, slash commands, and agents for your workspace.

## Decision Tree

**Choose the right primitive:**

| If the user wants... | Create a... | Guide |
|---------------------|-------------|-------|
| Explicit trigger (`/command`) | Slash Command | [COMMAND-GUIDE.md](modules/COMMAND-GUIDE.md) |
| Auto-discovered capability | Skill | [SKILL-GUIDE.md](modules/SKILL-GUIDE.md) |
| Parallel specialist | Agent | [AGENT-GUIDE.md](modules/AGENT-GUIDE.md) |

See [DECISION-TREE.md](modules/DECISION-TREE.md) for detailed flowchart.

## Questions to Ask

Before creating a primitive, clarify:

1. **Trigger type**: "Will you trigger this explicitly (`/command`), or should I auto-detect when to use it?"
2. **Complexity**: "Is this a simple prompt or a complex multi-step workflow?"
3. **Context isolation**: "Should this run in its own context (parallel work)?"

## Quick Reference

### Slash Commands
- User-invoked only (explicit `/command`)
- Single markdown file in `.claude/commands/`
- Best for: daily routines, quick actions, explicit triggers

### Skills
- Model-invoked (Claude auto-detects when relevant)
- Directory with SKILL.md + optional modules/scripts
- Best for: complex workflows, reusable capabilities, domain expertise

### Agents
- Specialists that run in isolated context
- Single markdown file in `.claude/agents/`
- Best for: parallel work, deep research, task delegation

## Templates

Use templates from `templates/` folder:
- [skill-template.md](templates/skill-template.md)
- [command-template.md](templates/command-template.md)
- [agent-template.md](templates/agent-template.md)

## Official Reference

For Claude Code official documentation, see [CLAUDE-CODE-REFERENCE.md](CLAUDE-CODE-REFERENCE.md).

## Workflow

1. Ask clarifying questions (above)
2. Determine primitive type using decision tree
3. Read the appropriate guide
4. Use the template to create the primitive
5. Validate against official reference
