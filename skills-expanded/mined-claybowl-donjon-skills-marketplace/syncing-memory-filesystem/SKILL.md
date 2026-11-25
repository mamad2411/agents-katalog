---
name: syncing-memory-filesystem
description: |
  DEPRECATED: This skill covered git-backed memory repos which are no longer used.
  Memory now uses Letta MCP directly. See letta-memory skill for current approach.
  
  Kept for reference only. All git-based operations are obsolete.
---

# Git-Backed Memory — DEPRECATED

⚠️ **This skill is obsolete.** Memory is now managed via Letta MCP, not git.

---

## What Changed

| Old System | New System |
|------------|------------|
| Git repo at `~/.letta/agents/<id>/memory/` | Direct API via `letta_memory_unified` |
| `git push` to sync | `update_core_memory` / `insert_passage` |
| `git pull` to fetch | `get_core_memory` / `search_archival` |
| Merge conflicts possible | No conflicts — it's an API |
| Local filesystem required | No local files needed |
| Windows paths (`C:\Users\...`) | Works from anywhere |

---

## Current Approach: Letta MCP

See the **letta-memory** skill for the current system.

### Quick Reference

```javascript
// Read memory
letta_memory_unified({ operation: "get_core_memory", agent_id: "..." })

// Write memory
letta_memory_unified({ operation: "update_core_memory", label: "xxx", value: "xxx" })

// Search history
letta_memory_unified({ operation: "search_archival", query: "xxx" })
```

### Agent ID
`agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

## Why We Switched

1. **No more merge conflicts** — API is atomic
2. **Instant updates** — No commit/push cycle
3. **No local files** — Works from any context
4. **Simpler** — One API call vs. git workflow
5. **More reliable** — No credential helpers, no clone issues

---

*This skill is archived. Use letta-memory or memory-sync instead.*
