---
description: "Show available skills, plugins, and commands organized by category. Use when starting work, unsure which tool fits, or need a quick reference. Triggers on: 'what tools do I have', 'which skill', 'what commands', '/tool-suggest'."
---

# Tool Suggest: Skill and Plugin Quick Reference

Scan the user's installed plugins and skills, then recommend which ones are relevant to the current task.

## What to do

1. **Discover what's installed.** Check:
   - `~/.claude/skills/` for user-level skills
   - `~/.claude/commands/` for user-level commands
   - `~/.claude/plugins/` for installed plugins and their skills/commands

2. **Read the task context.** What is the user trying to do? Match against skill descriptions and names.

3. **Recommend by category.** Group recommendations into: Session/Workflow, Review/Quality, and any domain-specific categories that match installed plugins (Marketing, Sales, Data, etc).

4. **Be specific.** Don't list everything. Recommend the 3-5 most relevant tools for the current task with a one-line explanation of why each fits.

## Format

```
## Relevant tools for: [task summary]

**Best fit:**
- `/skill-name` - why it fits this specific task

**Also consider:**
- `/other-skill` - secondary fit

**Reference:**
- `/tool-suggest` again any time to re-scan
```

## Core skills in this plugin (always available)

| Command | When to suggest |
|---------|----------------|
| `/plan` | Starting any non-trivial project. Interview-style, produces phased plan with completion promises. |
| `/dispatch` | Background work that doesn't need to block the session. |
| `/jobs` | Checking status of dispatched background tasks. |
| `/plan-review` | After writing a plan. Adversarial review in 4 modes (expand/selective/hold/reduce). |
| `/preflight` | Before a long autonomous session. Verifies Keychain, env, MCP, GCP, GitHub. |
| `/captain-opus` | Opening a complex session. Sets senior PM posture with full tool authority. |
