---
name: codex-implementation
description: Delegate bounded mechanical implementation, migrations, bulk edits, or isolated fixes to Cursor Agent with GPT-5.5, usually in a worktree.
---

# Codex Implementation

Use this skill for clear-spec implementation, migrations, bulk edits, simple data analysis, or isolated fixes. Do not use it as the final authority for public API design, UI polish, or taste-heavy work unless Fable or Opus reviews the result afterward.

## Workflow

1. Make the task bounded and self-contained.
2. Prefer a worktree for anything that might conflict with current work.
3. Give Cursor Agent the relevant repo instructions in the prompt; it does not inherit Claude's global `CLAUDE.md`.
4. Require a concise summary of files changed and checks run.
5. Review the patch before final acceptance.

## Command Pattern

```sh
agent -p --trust --workspace "$WORKTREE" --model gpt-5.5-high --force "<bounded implementation prompt>"
```

## Guardrails

- Use `--force` only when intentionally delegating edits.
- Keep the prompt plain and specific.
- Ask for the smallest working change.
- If the delegated agent touches too much, stop and review before continuing.
