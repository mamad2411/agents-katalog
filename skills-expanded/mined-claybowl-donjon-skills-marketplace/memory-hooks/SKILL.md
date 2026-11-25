---
name: memory-hooks
description: |
  Memory automation with Letta MCP. No more git hooks needed! This skill
  explains the new MCP-based automation patterns for memory management.
  
  Triggers: "memory hooks", "memory automation", "auto sync", "auto save"
---

# /memory-hooks: Memory Automation (MCP Edition)

**No more git hooks!** Memory is now handled via direct MCP API calls.

## What Changed

| Old Way (Git) | New Way (MCP) |
|---------------|---------------|
| post-checkout hook → pull | `/memory-init` → `get_core_memory` |
| post-commit hook → push | Direct `update_core_memory` or `insert_passage` |
| pre-commit validation | API validates automatically |
| Merge conflicts | No merges — it's an API |
| Local git repo | No local repo needed |

---

## Automation Patterns (MCP)

### Pattern 1: Session Start Auto-Load

Add to your shell profile or OpenCode config:
```bash
# Automatically pull memory when starting a session
/memory-init
```

Or programmatically:
```javascript
// First thing in any session
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

### Pattern 2: Auto-Save on Significant Events

Instead of waiting for session end, save when things happen:

```javascript
// After a dispatch
letta_memory_unified({
  operation: "update_core_memory",
  label: "dd_dispatch_state",
  value: JSON.stringify(dispatch_log)
})

// After a council decision
letta_memory_unified({
  operation: "update_core_memory", 
  label: "dd_council_notes",
  value: JSON.stringify(council_decision)
})
```

### Pattern 3: Periodic Checkpoint

Schedule memory saves at intervals:

```javascript
// Every 30 minutes or after N exchanges
letta_memory_unified({
  operation: "insert_passage",
  text: "Checkpoint: [current state summary]"
})
```

### Pattern 4: Heartbeat Integration

The heartbeat can sync memory:

```javascript
// In heartbeat routine
function heartbeat() {
  // 1. Read soul.md priorities
  // 2. Check queue status
  // 3. Save state to Letta
  letta_memory_unified({
    operation: "update_core_memory",
    label: "dd_council_notes",
    value: JSON.stringify(current_state)
  })
  // 4. Continue heartbeat...
}
```

---

## No More Git Hooks!

The old system required:

```bash
# OLD: Git hooks in .git/hooks/
post-checkout  # Pull on checkout
post-commit    # Push after commit
pre-push       # Validate before push
```

**New system:**
```javascript
// NEW: Direct API calls
letta_memory_unified({ operation: "..." })
```

**Benefits:**
- ✅ No local git repo needed
- ✅ No Windows paths
- ✅ No merge conflicts
- ✅ Instant updates (no commit/push cycle)
- ✅ Works from any directory

---

## Recommended Save Points

| When | What to Save | Block |
|------|--------------|-------|
| Session start | Pull current state | `get_core_memory` |
| After dispatch | Dispatch log | `dd_dispatch_state` |
| After council | Council decision | `dd_council_notes` |
| Significant finding | Archival note | `insert_passage` |
| Session end | Session summary | `insert_passage` |

---

## Migration

**Old: Git hooks auto-push**
```bash
git commit -m "update"
# post-commit hook auto-pushes
```

**New: Direct save**
```javascript
letta_memory_unified({
  operation: "update_core_memory",
  label: "xxx",
  value: "xxx"
})
// Done. No commit, no push, no hooks.
```

---

*Skill updated: 2026-03-24 | Git hooks deprecated, MCP automation enabled*
