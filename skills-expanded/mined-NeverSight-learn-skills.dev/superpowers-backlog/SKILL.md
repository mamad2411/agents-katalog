---
name: superpowers-backlog
description: Use when the user wants to see the backlog, asks what to work on next, searches for specific epics, or asks whether something has been captured — including "what's highest priority", "show me epics about X", "what's next for Y", or "do we have anything for Z".
---

# superpowers-backlog Commands

The script `epics.mjs` lives **in the same directory as this SKILL.md file**. It runs in any project directory — no installation needed. It manages epic data in the current working directory (`process.cwd()`).

**NEVER read or modify `EPICS.json` directly.** The file is an internal implementation detail of the script and its format may change at any time. Always use the commands below. When the script modifies `EPICS.json`, commit the changes as part of your work.

## Locating the script

`epics.mjs` is always a sibling of this skill file. Determine the absolute path from this SKILL.md's location:

```
EPICS_SCRIPT="<directory containing this SKILL.md>/epics.mjs"
```

All commands below use `$EPICS_SCRIPT` as a placeholder — substitute the resolved absolute path.

## Commands

```bash
# List top incomplete epics with context and inlined references
node $EPICS_SCRIPT --pending --limit 5 --with-context

# All incomplete epics (no context)
node $EPICS_SCRIPT --pending

# Search by keyword (read-only — searches id, description, and context)
node $EPICS_SCRIPT --search <term>
node $EPICS_SCRIPT --search <term> --with-context

# Mark an epic in-progress
node $EPICS_SCRIPT --start <id-or-search>

# Mark an epic completed
node $EPICS_SCRIPT --complete <id-or-search>

# Show completed epics
node $EPICS_SCRIPT --filter-completed

# Add a new epic
node $EPICS_SCRIPT --add --description "Description" [--id <id>] \
  [--context "..."] [--complexity 0.3] [--user-impact 0.7] \
  [--code-quality-impact 0.4] [--extensibility-impact 0.6] [--ref "path:1-10"] ...
```

`<id-or-search>` matches exact `id` first, then falls back to case-insensitive substring of the epic description.

## Answering topic-filtered queries

When the user asks "what's next for X?" or "what's highest priority for the Y area?", use `--search <keyword>` to narrow candidates, then `--pending` with judgement applied. There is no built-in topic filter.

## `--with-context` flag

When picking an epic to implement, always use `--with-context`. It inlines:
- The `context` field (free-form background text)
- All `references` — file ranges are read and inlined; URLs are listed but not fetched

This output is the primary spec input for brainstorming and planning.

## First-time project setup

If the project has no epics yet, the script creates the backing store automatically on first `--add`. No manual setup is required.

Optionally add to `CLAUDE.md`:
```
Never read or modify EPICS.json directly. All epic state is managed through the superpowers-backlog skill.
```

## Epic fields

| Field | Type | Meaning |
|-------|------|---------|
| `id` | kebab-case string | Stable identifier for `--start` / `--complete` / `--search` |
| `epic` | string | Human-readable description |
| `status` | `null` / `"in-progress"` / `"completed"` | Lifecycle state |
| `context` | string (optional) | Free-form background, constraints, or notes |
| `references` | string[] (optional) | Files (`path:start-end`, `path:line`, `path`) or URLs |
| `user_impact` | 0–1 | End-user value (scoring weight 0.50) |
| `code_quality_impact` | 0–1 | Correctness / tech debt (weight 0.30) |
| `extensibility_impact` | 0–1 | Future development leverage (weight 0.20) |
| `complexity` | 0–1 | Technical difficulty — penalises score via `complexity^1.5 × 0.30` |
