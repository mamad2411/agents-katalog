---
name: skill-helper
description: Create, validate, audit, review, refactor, optimize, and improve Agent Skills. Works with YAML frontmatter, SKILL.md docs, trigger-rich descriptions, slash commands, and automated validation + grading to keep skills consistent and discoverable.
license: MIT
metadata:
  version: 2.0.0
  replaces: [skill-creator, skill-validator]
  audience: developers, agents
  workflow: skill-development
---

## Quick Start

**Prerequisites:**
- Write access to skill directory (.opencode/skill/ or .claude/skills/)
- Bash for validation script
- Git configured (for author metadata)

**Tools Used:** Read, Write, Edit, Bash, Grep, Glob

**Three Primary Workflows:**

1. **Create a New Skill**
   ```
   User: "Create a skill for [task]"
   Agent: Follows 8-step creation workflow
   ```
   See: [references/creation-workflow.md](references/creation-workflow.md)

2. **Validate & Grade Existing Skill**
   ```bash
   ./scripts/validate-skill.sh path/to/skill
   # Returns: 34 validation checks + 100-point grade
   ```
   See: [references/validation-guide.md](references/validation-guide.md)
   
   Rubric: [references/grading-rubric.md](references/grading-rubric.md)

3. **Optimize for Discoverability**
   ```
   User: "Make [skill-name] more discoverable"
   Agent: Analyzes description, adds verbs/keywords
   ```
   See: [references/optimization-patterns.md](references/optimization-patterns.md)

## What I Do

- Create new skills from scratch with templates
- Validate skills against 34-check system (9 errors, 17 warnings, 8 suggestions)
- Grade skills using 100-point rubric (A/B/C/D/F scale)
- Optimize descriptions for auto-activation (5+ verbs, 10+ keywords)
- Generate slash commands with proper naming (ak- prefix for agent-kit)
- Audit existing skills for quality and compliance
- Refactor skills for token efficiency (1000-2000 token sweet spot)
- Bundle resources (assets/, references/, scripts/)
- Provide skill templates and patterns

## When to Use Me

Use this skill when you:
- Create, write, or generate new Agent Skills
- Validate, audit, or review existing skills
- Grade or score skills using rubric
- Optimize descriptions for trigger-richness
- Fix validation errors (placeholders, XML, format issues)
- Refactor skills that are too small (<1000 tokens) or too large (>3500 tokens)
- Generate or fix slash commands
- Check Context7 integration format
- Prepare skills for publishing
- Need skill templates or patterns
- Convert documentation to skills

## Core Principles

**Auto-Activation:** 5+ action verbs, 10+ keywords, "Use when" triggers, parenthetical grouping, task-centric framing

**Progressive Loading:** L1 (frontmatter ~100 tokens) → L2 (SKILL.md 1000-2000 tokens) → L3 (references/ unlimited)

**Token Targets:** Sweet spot 1000-2000 tokens; warn <500 or >3500

**Validation + Grading:** 34 checks + 100-point rubric; grade calculated first, used as validation input

Run: `./scripts/validate-skill.sh path/to/skill`

## Validation Overview

**34 checks across 3 tiers:**
- 🔴 **Errors (9):** Must fix to publish
- 🟡 **Warnings (17):** Should fix for effectiveness  
- 🟢 **Suggestions (8):** Polish & best practices

See [references/validation-guide.md](references/validation-guide.md) for complete details.

## Grading Overview

**100-point rubric:** Description Quality (35%), Structure (25%), Content (20%), Technical (15%), Compliance (5%)

**Grades:** A (90-100), B (80-89), C (70-79), D (60-69), F (0-59)

See [references/grading-rubric.md](references/grading-rubric.md) for scoring details.

## Skill Patterns

**Workflow Skills:** Multi-step processes with phases (planning, deployment)
**Reference Skills:** Domain knowledge with quick references (testing, security)
**Tool Skills:** Specific operations with clear input/output (validation, formatting)

See [references/creation-workflow.md](references/creation-workflow.md) for pattern details.

## Quick Reference

| Element | Rule | Example |
|---------|------|---------|
| **Name** | `^[a-z0-9-]+$` (max 64) | `spring-boot-core` |
| **Description** | 50-1024 chars, 5+ verbs, 10+ keywords | See frontmatter above |
| **Tokens** | 1000-2000 ideal, >500 min, <3500 warn | ~200-400 lines |
| **Sections** | What I Do, When to Use Me, Quick Start | Required |
| **Resources** | assets/, references/, scripts/ | Optional |
| **Command** | `{name}.md` or `ak-{name}.md` | Matches skill name |
| **Grade** | A-F scale (100 points) | Target: B+ (85+) minimum |

## Examples

**Create new skill:**
```
User: "Create a skill for API validation"
→ 8-step workflow → Grade B+ (87/100)
```

**Validate existing skill:**
```bash
./scripts/validate-skill.sh .opencode/skill/my-skill
→ 0 errors, Grade A (92/100)
```

**Optimize description:**
```
User: "Make skill more discoverable"
→ Add verbs + keywords → Grade improves C (75) to A (93)
```

See [references/creation-workflow.md](references/creation-workflow.md) for detailed examples.

## Common Errors

| Error | Solution |
|-------|----------|
| "Invalid name format" | Use lowercase, hyphens only |
| "Description too short" | Add action verbs + keywords |
| "SKILL.md too large" | Move content to references/ |
| "No slash command" | Create command file |

See [references/validation-guide.md](references/validation-guide.md) for complete error catalog.

## References

Load detailed guidance as needed:

| Reference | Use When | Content |
|-----------|----------|---------|
| [creation-workflow.md](references/creation-workflow.md) | Creating new skills | 8-step process, patterns, examples |
| [validation-guide.md](references/validation-guide.md) | Understanding validation | 34 checks explained, fixes |
| [optimization-patterns.md](references/optimization-patterns.md) | Improving descriptions | Trigger-rich patterns, testing |
| [grading-rubric.md](references/grading-rubric.md) | Understanding grades | 100-point scoring breakdown |

## Related Skills

- `markdown-editor` - For creating and editing SKILL.md markdown files
- `github-actions` - For CI/CD integration of validation
- `github-project-manager` - For tracking skill development tasks

## Next Steps

**Complete workflows & resources:**
- [references/creation-workflow.md](references/creation-workflow.md) - 8-step creation process
- [references/validation-guide.md](references/validation-guide.md) - 34 validation rules
- [references/optimization-patterns.md](references/optimization-patterns.md) - Trigger patterns + testing
- [references/grading-rubric.md](references/grading-rubric.md) - 100-point scoring system

**Templates:**
- [assets/skill-template.md](assets/skill-template.md) - Ready-to-use starter template
- [assets/command-template.md](assets/command-template.md) - Slash command template

**Automation:**
- `./scripts/validate-skill.sh` - Validation + grading in one command
