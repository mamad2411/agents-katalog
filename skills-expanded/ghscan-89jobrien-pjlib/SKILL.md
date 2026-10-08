---
description: Create a new Claude Code skill with interactive template generator
allowed-tools: Bash, Read, Write
argument-hint: '[skill-name]'
---

# Create New Skill

Create a new Claude Code skill using the interactive template generator.

## Usage

If skill name provided in arguments:
```
/new-skill my-skill-name
```

Otherwise, run the interactive generator:
```
/new-skill
```

## Instructions

Run the skill generator script:

```bash
~/.claude/scripts/create-skill.py
```

The generator will:
1. Prompt for skill name (validated for proper format)
2. Ask for description with use cases and triggers
3. Let you select allowed tools from common options
4. Ask for related skills
5. Generate complete SKILL.md with frontmatter
6. Create directory structure with scripts/ and references/

After generation:
- Edit SKILL.md to customize sections
- Add helper scripts to scripts/
- Add documentation to references/
- Run validation: `~/.claude/scripts/validate-skills.py ~/.claude/skills`

## Template Structure

Generated skills include:
- YAML frontmatter (name, description, allowed-tools, skills)
- When to Use section
- What This Skill Does section
- How to Use with examples
- Best Practices
- Related Use Cases

## Validation

The generated skill will pass frontmatter validation with:
- Required fields (name, description)
- Proper naming convention (lowercase, hyphens)
- Valid tool references
- Consistent formatting
