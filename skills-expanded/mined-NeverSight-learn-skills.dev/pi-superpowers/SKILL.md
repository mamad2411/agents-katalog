---
name: pi-superpowers
description: Use at the start of every conversation to establish skill-driven workflows. Ensures relevant skills are loaded before any action or response.
---

# Pi Superpowers

## The Rule

**Check for and load relevant skills BEFORE any implementation, debugging, or multi-step work.** When in doubt, load the skill.

## How to Load Skills

Use `read` to load the full SKILL.md for any skill, or the user can invoke `/skill:name`.

## Finding Skills

Refer to the `<available_skills>` block in the system prompt. Match the task against each skill's description. If a skill is relevant, load it with `read` before proceeding.

## When NOT to Load Skills

Skip the skill check for:
- Simple questions or explanations ("what does this function do?")
- Reading or exploring files without making changes
- One-liner fixes the user has already diagnosed
- Conversations where the user explicitly asks to skip skills

## Skill Priority

1. **Process skills first** (brainstorming, debugging) — determine HOW to approach
2. **Implementation skills second** (TDD, planning) — guide execution

"Build X" → brainstorming first, then planning, then TDD.
"Fix this bug" → systematic-debugging first, then TDD for the fix.

## Task Tracking

You have a `todo` tool. Use it to:
- Create checklists from plans (`batch` action with groups)
- Track task progress (`start`, `done`, `skip`, `block`)
- Report status (`summary` action)

**Create a todo list when starting any multi-step workflow.**

## Red Flags

These thoughts mean STOP — you're rationalizing skipping skills:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE gathering context. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |

## Skill Types

**Rigid** (TDD, debugging, verification): Follow exactly. No shortcuts.
**Flexible** (brainstorming, planning): Adapt principles to context.

The skill itself tells you which.
