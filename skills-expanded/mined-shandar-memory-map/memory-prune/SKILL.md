---
name: memory-prune
description: >
  Clean stale, outdated, or redundant entries from Claude's stored memory. Use this skill when
  the user says things like "clean up memory", "prune memory", "memory is getting cluttered",
  "remove old entries", "consolidate memory", or "trim the memory map". Also trigger proactively
  when memory approaches its limits — 30 entries on claude.ai, 200 lines on Claude Code — or
  when entries reference past events that have completed (an event date that has passed, a
  deliverable marked "upcoming" that is now shipped). Always propose changes for user
  confirmation before applying — never delete memory autonomously. Pairs with memory-map and
  memory-recall to form the complete memory loop.
---

# Memory Prune

Identify and remove stale, outdated, or redundant memory entries to keep the store clean
and decision-useful over time.

Works in **claude.ai** (uses `memory_user_edits`) and **Claude Code** (writes
`~/.claude/memory.md`). Detected automatically.

---

## Step 0 — Detect environment

| Signal | Environment | Load |
|--------|-------------|------|
| `memory_user_edits` tool is available | claude.ai | `references/claude-ai.md` |
| Not available / running in terminal | Claude Code | `references/claude-code.md` |

---

## Core Protocol

### Step 1 — Read all memory

Fetch every entry with the environment-appropriate read command.

### Step 2 — Audit for cleanup candidates

Categorise each entry into:

**Stale** — references past events or dates that have passed:
- Events with past dates that are not retrospectively meaningful
- "Upcoming" tags on things that have shipped
- Old "CURRENT STATE SNAPSHOT" entries that have been superseded but not replaced

**Redundant** — covered by another entry:
- Two entries with overlapping content (one is more current)
- Sub-entries that have been folded into a parent entry
- Duplicate category labels

**Outdated** — factually wrong now:
- Old contact details, links that no longer work
- Specs that have been revised
- Cohort numbers that have changed

**Mergeable** — could be consolidated to save space:
- Two related entries that are both under-character-limit could become one
- Multiple small notes about the same project

### Step 3 — Propose changes (do not apply yet)

Show the user a structured proposal:

```
MEMORY PRUNE — proposed changes

REMOVE (stale)
→ Entry 12: "P2P landing page draft v1" (superseded by v2 in entry 13)
→ Entry 18: "TIU registration link" (event closed)

REMOVE (redundant)
→ Entry 7: "Workshop tools" (covered by entry 14 — frameworks)

CONSOLIDATE
→ Entries 9 + 10 → single "V2V EDITIONS" entry (saves 1 slot)

KEEP (just confirming these are still current)
→ Entry 1-6: PWP and operating preferences
→ Entry 19: Current state snapshot

Apply these changes? [yes / modify / cancel]
```

### Step 4 — Wait for user confirmation

**Never apply changes without explicit user approval.** Memory is a user asset.
Wait for one of:
- "yes" / "apply" / "do it" → proceed to Step 5
- "modify" → ask which proposals to skip or change
- "cancel" / "no" → exit cleanly, no changes made

### Step 5 — Apply changes in safe order

Apply in this order to avoid line number shifts breaking subsequent operations:
1. **Replace** consolidations first (preserves line numbers)
2. **Remove** entries from highest line number to lowest (removing high first preserves low numbers)
3. **Verify** by re-reading memory after all changes

### Step 6 — Show the result

```
MEMORY PRUNE — complete

Before: 24 entries
After:  19 entries
Removed: 3 stale, 1 redundant
Consolidated: 2 → 1
```

---

## Hard rules

- **Never apply changes without user confirmation.** Always propose first.
- **Never remove `CURRENT STATE SNAPSHOT`** — it's the live anchor entry. If it's stale,
  ask the user to update via memory-map first.
- **Never remove operating preference entries** (PWP, design system, communication style)
  unless the user explicitly says so — these are foundational.
- **Always preserve a backup** before pruning Claude Code memory:
  ```bash
  cp ~/.claude/memory.md ~/.claude/memory.md.backup-$(date +%Y%m%d-%H%M%S)
  ```
- **One action at a time** for claude.ai memory — line numbers shift after every operation.

---

## When to trigger proactively

Run this skill without being asked when:
- claude.ai memory hits 28+ entries (out of 30 max)
- Claude Code `~/.claude/memory.md` exceeds 180 lines
- An entry references a past date that's clearly behind us (e.g. "event May 8" is now July)
- The user opens a session and the memory store has obvious bloat

When triggering proactively, frame it as: *"Your memory store is getting full. Want me to
propose a cleanup?"* — never just start pruning.

---

## Pairs with

- **memory-map** — writes new memory at session close
- **memory-recall** — loads stored memory at session start

Together: write → recall → prune. The full memory loop.
