---
name: claude-praetorian
description: Cross-session memory — save insights after research, restore prior context before planning or research. Restore first, compact second.
---

# Claude Praetorian

Context preservation across sessions. Restore before work, compact after valuable findings.

## Workflow: restore → work → compact

### 1. Restore Before Work

Check compactions BEFORE planning, research, or subagents:

```
praetorian_restore(query="topic")              # search — summary mode, ~50 tokens/result
praetorian_restore(query="topic", detail="full") # full detail when summary hit looks relevant
praetorian_restore()                            # recent compactions
praetorian_restore(project="current")           # only this project
```

**When to restore:**
- Before planning sessions or architectural decisions
- Before web research — you may already know this
- Before launching subagents — prior context exists
- At session start on a familiar project
- After `/clear` — reload lost context

### 2. Compact After Valuable Findings

Update existing compactions — reuse title to merge, don't create duplicates:

```
praetorian_compact(type="web_research", title="auth JWT research",
  key_insights=[...], refs=[...])
```

**When to compact:**
- After research with findings NOT already in compactions
- After decisions worth preserving across sessions
- After subagent results with new insights
- Always reuse existing title to merge — check first

**When NOT to compact:**
- Routine work, trivial discoveries
- Information already saved in an existing compaction
- Every single web search (only genuinely valuable ones)

### 3. Manage Storage

```
praetorian_manage(action="status")              # per-project counts, disk size
praetorian_manage(action="prune", count=3)      # remove 3 oldest
praetorian_manage(action="prune", project="/path") # prune specific project
```

Per-project limit: 13. Auto-prunes oldest when exceeded (merges are free).
Only mention cleanup to user when >50 total or >500KB.

## Tools

| Tool | Purpose |
|------|---------|
| `praetorian_restore` | Search/load past context. Summary mode by default (cheap). |
| `praetorian_compact` | Save insights. Auto-merges same title+type (>70% Jaccard). |
| `praetorian_manage` | Storage health: status and prune. |

## Token Discipline

- Restore summaries first — only load full detail for relevant hits
- One well-maintained compaction > five stale ones
- Compact selectively — key decisions, hard-won findings, patterns that save time
- Don't flood context with full restores when summaries suffice
