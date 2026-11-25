---
name: handoff
description: Create a compact continuation document for another agent or future session. Use when the user asks to hand off, summarize current work, continue later, create context, or preserve progress across sessions.
---

# Handoff

Use this skill to make work easy to resume.

## Handoff Contents

Include:

- Objective
- Current status
- Important decisions
- Files changed or inspected
- Commands run and results
- Known issues
- Next steps
- Risks and assumptions

## Workflow

1. Gather state
   - Inspect git status if in a repo.
   - Review recent files and command outputs available in the session.
   - Identify user requests that still matter.

2. Separate facts from guesses
   - Mark verified facts clearly.
   - Mark assumptions clearly.
   - Do not imply tests passed if they were not run.

3. Write for continuation
   - Make the next action obvious.
   - Include exact commands when useful.
   - Keep prose compact.

## Rules

- Do not omit failed commands.
- Do not say work is complete unless verification supports it.
- Keep unresolved user requests visible.
- Include branch, repository, or workspace context when relevant.

## Output Format

```markdown
# Handoff

## Objective

## Status

## Decisions

## Files

## Verification

## Next Steps

## Risks
```
