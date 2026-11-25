---
name: subagent-driven-development
description: Use when executing implementation plans with independent tasks in the current session
---

# subagent driven development

Use this skill when the task matches the description above.
Keep the initial response concise and only open bundled references or scripts when they are clearly needed.

## Quick cues

- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)
- `./implementer-prompt.md` - Dispatch implementer subagent
- `./spec-reviewer-prompt.md` - Dispatch spec compliance reviewer subagent
- `./code-quality-reviewer-prompt.md` - Dispatch code quality reviewer subagent
- Implemented install-hook command

## Available sections

- Subagent-Driven Development
- When to Use
- The Process
- Prompt Templates
- Example Workflow
- Advantages
- Red Flags
- Integration

## Bundled resources

- code-quality-reviewer-prompt.md
- implementer-prompt.md
- spec-reviewer-prompt.md

Open these resources only if the current task needs deeper detail or executable helpers.
