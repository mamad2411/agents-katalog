---
name: explain-skill
description: Explain what a skill does, when to use it, and its triggers
---

# /explain-skill [skill-name]

Explain a skill's purpose, usage, and auto-invoke triggers.

> **No arguments?** Describe this skill and stop. Do not execute.

## On Invoke

1. **Find the skill** in `.claude/skills/[skill-name]/SKILL.md`
   - If not found, check `workflow-skills/[skill-name]/SKILL.md`
   - If still not found, report "Skill not found: [name]"

2. **Read and summarize** the skill file, extracting:
   - **Purpose**: What does this skill do? (1-2 sentences)
   - **When to use**: Trigger contexts from CLAUDE.md auto-invoke table
   - **Key principles**: Main ideas/rules (3-5 bullets max)
   - **Example**: One concrete usage example if available

3. **Output format**:

```
═══════════════════════════════════════════
 /[skill-name]
═══════════════════════════════════════════

 Purpose:
   [1-2 sentence description]

 When to use:
   [Auto-invoke context from CLAUDE.md, or "Manual invoke only"]

 Key principles:
   • [principle 1]
   • [principle 2]
   • [principle 3]

 Example:
   [Brief usage example]

═══════════════════════════════════════════
```

## Rules

- Keep it concise—summarize, don't dump the whole file
- If skill has no SKILL.md, report the issue
- For workflow skills, focus on the command usage
- For canon skills, focus on the mental model/principles
