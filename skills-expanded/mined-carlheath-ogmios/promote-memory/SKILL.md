---
name: promote-memory
description: |
  Weekly dual-memory flow: review project auto-memory (inbox) and promote to
  global memory, keep as ephemeral, or delete. Addresses the dual-memory tension
  in a layered memory system.

  [VAD] Structured walkthrough of `~/.claude/projects/.../memory/`. Classifies
  each entry as promote/keep/delete based on type and stability. Writes
  promotions to global memory. Writes a review report.

  [WHEN] Use when: promote memory, dual-memory, weekly memory review, memory
  promotion, review project memory, "is this memory stable?", "should this go
  global?", inbox cleanup of memory.

  [LANGUAGE] Configurable.

  [EXPERTISE] Memory architecture, ephemeral-vs-persistent classification,
  three-criteria evaluation (recurrence, generality, stability).
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Promote Memory

**Role:** dual-memory triage. Move stable insights from project auto-memory
to global memory. Keep ephemeral details where they belong.

## Memory architecture

Two layers:

1. **Project auto-memory** (`~/.claude/projects/{slug}/memory/`)
   - Auto-captured per project context
   - Volatile, often noisy
   - Useful for ongoing project context but doesn't accumulate cleanly

2. **Global memory** (`~/.claude/memory/`)
   - User-curated, structured
   - USER/, SYSTEM/, KNOWLEDGE/, WORK/, learnings/
   - Stable, intentional

The skill bridges between them: review the project inbox, promote what's stable.

## Three-criteria evaluation

For each memory entry:

| Criterion | Promote if... | Otherwise |
|-----------|---------------|-----------|
| **Recurrence** | Mentioned in 3+ contexts | Project-scoped only |
| **Generality** | Applies beyond this project | Keep ephemeral |
| **Stability** | Hasn't changed in last 30 days | Wait, may change |

If all three are yes: promote.
If any is no: keep or delete.

## Three actions

### 1. Promote
Move entry from project memory to a global memory file. Preserve provenance:

```yaml
---
promoted_from: project/{slug}/memory/{file}
promoted_on: {YYYY-MM-DD}
original_captured: {YYYY-MM-DD}
---
```

Target file in global memory depends on type:
- Personal facts → `USER/`
- Technical patterns → `SYSTEM/PATTERNS.md`
- Domain knowledge → `KNOWLEDGE/`
- Learnings → `learnings/`

### 2. Keep ephemeral
Leave in project memory. Add a `last_reviewed: {date}` marker so it doesn't get re-evaluated next week.

### 3. Delete
Remove if:
- Already captured better elsewhere
- One-off context with no general value
- Stale (>90 days, not promoted)

## Workflow

### 1. Scan project memory
List all files in `~/.claude/projects/{slug}/memory/` (or all projects if no specific one).

### 2. Per-file evaluation
Read each file. Apply the three criteria. Suggest action.

### 3. Present review
```
## Memory Review — {date}

### Recommended: PROMOTE (N)
- {file1} → {global path} — Reason: {recurrence + generality + stability}
- {file2} → {global path} — Reason: ...

### Recommended: KEEP EPHEMERAL (M)
- {file3} — Reason: project-scoped, not yet stable
- {file4} — Reason: may change, recheck in 2 weeks

### Recommended: DELETE (K)
- {file5} — Reason: superseded by {global file}
- {file6} — Reason: stale, never promoted

Approve? (y/all/per-row)
```

### 4. Execute approved actions
- For PROMOTE: copy to global, mark project file as promoted
- For KEEP: add `last_reviewed:` marker
- For DELETE: move to `_archived/` (don't hard delete)

### 5. Report
Write a review report to `~/.claude/memory/learnings/memory-reviews/{YYYY-MM-DD}.md`:

```markdown
# Memory review {YYYY-MM-DD}

Promoted: N
Kept ephemeral: M
Deleted: K
Total reviewed: N+M+K

## Promoted entries
[list]

## Notes
[anything notable about the review]
```

## Cadence

Recommended: weekly. Use `/loop 7d /promote-memory` if the user wants to schedule it.

## Anti-patterns

- Promoting unstable memory (gets superseded fast)
- Deleting without archive
- Promoting without provenance metadata
- Skipping the user-approval step

---

🎯 COMPLETED: [SKILL:promote-memory] [memory review for date X]
🗣️ CUSTOM COMPLETED: [SKILL:promote-memory] [Memory review done]
