---
name: skill-creator
# prettier-ignore
description: "Design and create Agent Skills using progressive disclosure principles. Use when building new skills, planning skill architecture, or writing skill content."
metadata:
  last_updated: "2026-04-24"
  verified_against: "current local skill refresh"
---

# Skill Creator

Create effective Agent Skills using progressive disclosure. For choosing validation and distribution tooling around skills, use `ecosystem-guide`.

## When to Create a Skill

Create a skill when you notice:

- **Repeating context** across conversations
- **Domain expertise** needed repeatedly
- **Project-specific knowledge** the agent should know automatically

## Progressive Disclosure

Skills load in 3 levels:

1. **Metadata** (~27 tokens optimal, ~100 max) - YAML frontmatter for triggering
2. **Instructions** (<50 lines recommended, 500 max) - SKILL.md body with core patterns
3. **Resources** (unlimited) - references/ scripts/ assets/ loaded on demand

**Key**: Keep Levels 1 & 2 lean. Move details to Level 3. Use `npx claude-skills-cli validate` to check budgets.

## Structure

```
my-skill/
├── SKILL.md       # Core instructions + metadata
├── references/    # Detailed docs (loaded as needed)
├── scripts/       # Executable operations
└── assets/        # Templates, images, files
```

## References

- [quick-start.md](references/quick-start.md) - Creating your first skill
- [writing-guide.md](references/writing-guide.md) - Writing effective skills
- [development-process.md](references/development-process.md) - Step-by-step workflow
- [skill-examples.md](references/skill-examples.md) - Patterns and examples
- [cli-reference.md](references/cli-reference.md) - CLI tool usage
- [anthropic-resources.md](references/anthropic-resources.md) - Official best practices
- [mcp-integration.md](references/mcp-integration.md) - MCP server integration patterns
- [testing-guide.md](references/testing-guide.md) - Testing methodology and checklists
- [distribution.md](references/distribution.md) - Sharing and distributing skills
- [troubleshooting.md](references/troubleshooting.md) - Common issues and fixes
