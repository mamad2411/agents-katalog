---
description: Create a new project context skill from scratch
argument-hint: [skill-name]
---

# Create New Project Skill

Create a comprehensive project context skill to preserve all session knowledge and prevent context loss between sessions.

## CRITICAL: Follow the Meta Skill-Generator Instructions

You MUST read and meticulously follow the instructions in the skill-generator meta-skill:

**Primary instruction file:** `~/.claude\skills\skill-generator\SKILL.md`

**Detailed phase procedures:** `~/.claude\skills\skill-generator\Reference\phase-procedures.md`

**Formatting standards:** `~/.claude\skills\skill-generator\Reference\formatting-standards.md`

## Templates to Use

Copy and customize these templates from `~/.claude\skills\skill-generator\Templates\`:

| Template | Use For |
|----------|---------|
| `project-skill-template.md` | Creating SKILL.md |
| `maintenance-template.md` | Creating Reference/skill-maintenance.md |
| `entity-template.md` | Creating entity files (if tracking entities) |

## Skill Name

Use: $ARGUMENTS

If no name provided, derive from the current project name or ask user.

## Output Location

Create all skill files in the current working project directory at:
```
.claude/skills/[skill-name]/
├── SKILL.md
├── Reference/
│   ├── skill-maintenance.md
│   └── [domain-specific files]
└── Templates/ (if needed)
```

## Required Workflow

Follow the 6-phase workflow exactly as documented in the meta-skill:

1. **Analyze** - Domain, knowledge categories, complexity assessment
2. **Plan** - Structure determination, content mapping, get user confirmation
3. **Extract** - Apply context loss test, white-paper ready standard
4. **Build** - Create files using templates, add cross-references
5. **Verify** - Complete 25-point verification checklist, all must pass
6. **Deliver** - Present summary with file list and what was captured

Do NOT skip phases. Do NOT deliver without passing verification.
