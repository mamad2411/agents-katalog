---
name: dev-remember
description: Persist context across engineering sessions — save important decisions, gotchas, or patterns that should survive beyond the current conversation. For long-term workspace memory, prefer mempalace.
---

# Dev Remember

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Quick context persistence for engineering sessions. Save decisions, gotchas, or patterns that should survive the current conversation but don't deserve a full memory entry in mempalace.

## Use When
- A non-obvious decision was made that future-you needs to remember
- A gotcha was discovered (e.g., "this lib's v3 silently breaks auth")
- A pattern was confirmed (e.g., "we always use Result<T> not exceptions in this module")
- Quick "remember this for next session" notes

## Do Not Use When
- The note is already covered by an agent's memory folder → write to `.claude/agent-memory/{agent}/` instead
- The note is shared workspace knowledge → write to `memory/` (mempalace owns this)
- The note is ephemeral (current conversation only) → don't persist it

## Storage Location

Engineering layer notes go to the relevant agent's memory folder:
- Architecture decision → `.claude/agent-memory/apex-architect/`
- Bug pattern → `.claude/agent-memory/hawk-debugger/`
- Test idiom → `.claude/agent-memory/grid-tester/`
- etc.

If the note doesn't fit any single agent, save to `workspace/development/research/[C]remember-{topic}-{date}.md`.

## Format

Each note has:
- **Title** (1 line)
- **Why this matters** (1-2 sentences)
- **Context** (when does this apply?)
- **Reference** (file:line, commit, or external link)

## Mempalace Note

For long-term, cross-session, cross-agent shared memory, **prefer mempalace**:
- It has structured drawers, rooms, and wings
- It supports knowledge graph queries
- It survives across sessions natively

`dev-remember` is for **engineering-specific** quick saves. mempalace is for **everything else**.

## Pairs With
- All 19 engineering agents (each has its own memory folder)
- mempalace (for shared workspace memory)
- `prod-memory-management` (the Clawdia skill that owns shared memory)
