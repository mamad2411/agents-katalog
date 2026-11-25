---
name: easyskillz-add
description: Create a new skill and automatically wire it to all registered AI tools.
---
# easyskillz-add

Create a new skill and automatically wire it to all registered AI tools.

## When to Use This Skill

Use this skill when:
- User asks you to create a new skill
- User wants to add custom functionality
- User says "make a skill for X"
- You need to create reusable AI agent instructions
- User wants to share a workflow across multiple AI tools

**IMPORTANT:** ALWAYS use `easyskillz add` to create skills. Never manually create skill files.

## What This Skill Does

Runs `easyskillz add <skill-name>` which:
1. Creates `.easyskillz/skills/<skill-name>/SKILL.md`
2. Automatically wires the skill to ALL registered tools (Claude, Cursor, Codex, etc.)
3. Creates symlinks or stubs in each tool's skills directory
4. Ensures the skill is immediately available in all tools

## Instructions

**Step 1: Run add command**
```bash
easyskillz add <skill-name>
```

**Naming rules:**
- Use lowercase letters, numbers, hyphens, underscores
- Examples: `review-pr`, `commit-msg`, `debug-api`
- Invalid: `Review PR`, `commit/msg`, `../hack`

**Step 2: Edit the skill**

The command creates a template at `.easyskillz/skills/<skill-name>/SKILL.md`:

```markdown
# skill-name

<!-- Describe what this skill does -->

## Instructions

<!-- Step-by-step instructions for the AI agent -->
```

Edit this file to add your skill's instructions.

**Step 3: Verify**

The skill is automatically available in all your AI tools:
- `.claude/skills/skill-name` → symlink to `.easyskillz/skills/skill-name`
- `.cursor/skills/skill-name` → symlink to `.easyskillz/skills/skill-name`

## Example Workflow

```bash
# User: "Create a skill for reviewing pull requests"

# You run:
easyskillz add review-pr

# Output:
#   ✓ Created .easyskillz/skills/review-pr/SKILL.md
#   ✓ Wired → Claude Code
#   ✓ Wired → Cursor
#
# Skill "review-pr" added to: Claude Code, Cursor

# Then edit the skill:
# Open .easyskillz/skills/review-pr/SKILL.md and add instructions
```

## Expected Output

```
  ✓ Created .easyskillz/skills/my-skill/SKILL.md
  ✓ Wired → Claude Code
  ✓ Wired → Cursor
  ✓ Wired → Codex

Skill "my-skill" added to: Claude Code, Cursor, Codex
```

## Why Use This Command?

**DON'T do this:**
```bash
# ❌ WRONG - Manual creation
mkdir .easyskillz/skills/my-skill
echo "# my-skill" > .easyskillz/skills/my-skill/SKILL.md
```

**DO this:**
```bash
# ✓ CORRECT - Use easyskillz add
easyskillz add my-skill
```

**Why?**
- Automatically wires to ALL tools (Claude, Cursor, Codex, etc.)
- Creates proper directory structure
- Ensures symlinks/stubs are created correctly
- Maintains single source of truth
- Updates all tools instantly

## Skill Template

When you run `easyskillz add`, it creates this template:

```markdown
# skill-name

<!-- Describe what this skill does -->

## Instructions

<!-- Step-by-step instructions for the AI agent -->
```

**Fill in:**
1. **Description** - What does this skill do?
2. **Instructions** - Step-by-step guide for the AI
3. **Examples** - Show expected input/output (optional)
4. **Troubleshooting** - Common issues (optional)

## Best Practices

1. **One skill, one purpose** - Keep skills focused
2. **Clear instructions** - Write step-by-step guides
3. **Include examples** - Show what good output looks like
4. **Test in all tools** - Verify the skill works in Claude, Cursor, etc.
5. **Commit to git** - Skills in `.easyskillz/skills/` should be committed

## Troubleshooting

**Skill already exists?**
- The command will tell you and not overwrite
- Edit the existing skill at `.easyskillz/skills/<name>/SKILL.md`

**Skill not showing up in tools?**
- Run `easyskillz sync` to re-wire
- Check that symlinks were created in `.claude/skills/`, etc.

**Invalid skill name?**
- Use only letters, numbers, hyphens, underscores
- No spaces, slashes, or special characters

## Related Skills

- **easyskillz-setup** - Set up easyskillz after cloning
- **easyskillz-register** - Add a new AI tool to the project
- **easyskillz-reference** - Full easyskillz documentation
