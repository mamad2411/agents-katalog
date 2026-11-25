---
name: claude-memory-system
description: How to use Claude Code's persistent memory system to carry context across sessions. Use when working across multiple sessions on the same project, or when the user asks Claude to remember something.
---

# Claude Memory System

Claude Code has a file-based memory system at `~/.claude/projects/<path-hash>/memory/`.

## Memory types

| Type | What to store | When to save |
|---|---|---|
| `user` | Role, preferences, expertise, working style | When you learn how the user thinks or what they care about |
| `feedback` | Corrections and confirmed approaches | Any time user says "no not that" or "yes exactly keep doing that" |
| `project` | Goals, decisions, deadlines, context behind the work | When you learn why something is being built or what constraint drives it |
| `reference` | Where to find things in external systems | When you learn about Linear projects, dashboards, Slack channels, etc. |

## File format

Each memory is its own file with frontmatter:

```markdown
---
name: short-kebab-case-slug
description: one-line summary used to decide relevance in future sessions
metadata:
  type: user | feedback | project | reference
---

Memory content here.
For feedback/project: lead with the rule/fact, then **Why:** and **How to apply:** lines.
Link related memories with [[their-name]].
```

`MEMORY.md` is the index — one line per entry, under 150 chars each. It is always loaded into context.

## When to save

- User explicitly asks to remember something → save immediately
- User corrects an approach → save the correction with why
- User confirms a non-obvious approach worked → save the validation too
- Project context emerges (deadlines, constraints, stakeholder requirements) → save it

## What NOT to save

- Code patterns derivable from reading the codebase
- Git history (use `git log`)
- Debugging solutions (the fix is in the code)
- Anything already in CLAUDE.md files
- Ephemeral task state (use TodoWrite instead)

## Verify before acting on memories

A memory naming a file, function, or flag is a claim about what existed when it was written — not what exists now.
Before recommending based on a memory: check the file exists, grep for the function, read current state.
