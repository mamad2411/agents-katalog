---
name: memory-sync
description: |
  Synchronize memory with Letta Cloud via MCP. Push new memories, pull current state,
  and manage memory blocks directly through the Letta API. No more git-based memory!
  
  Triggers: "sync memory", "push memory", "commit memory", "save to letta", 
            "sync with letta", "update memory", "remember this", "checkpoint"
---

# /memory-sync: Letta MCP Memory Synchronization

Sync memory directly to Letta Cloud using the `letta_memory_unified` MCP tool.

## Quick Start

```bash
# Save session summary to archival memory
/memory-sync "Worked on X, decided Y, next steps Z"

# Update core memory block
/memory-sync --update-block <label> "new content"

# Pull current memory state
/memory-sync --pull

# Search memory for something specific
/memory-sync --search "Clay's preferences"
```

---

## Agent ID

**DonDog's current Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

⚠️ Update this in `.letta/settings.local.json` if the agent is recreated.

---

## How It Works Now (MCP, Not Git!)

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR SESSION                        │
│         (ephemeral context, conversation)               │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│               letta_memory_unified (MCP)                │
│         Direct API calls to Letta Cloud                 │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              LETTA CLOUD (agent-d436abf8...)            │
│  ├── Core Memory Blocks (identity, persona, custom)    │
│  ├── Archival Memory (session logs, history)           │
│  └── Shared Blocks (kitchen queue, dispatch state)     │
└─────────────────────────────────────────────────────────┘
```

**No git. No local files. Direct API.**

---

## Core Operations

### 1. Save Session to Archival Memory

Use at session end or after significant work:

```javascript
letta_memory_unified({
  operation: "insert_passage",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  text: "Session 2026-03-24: Reconnected DonDog to Letta after rogue AI incident. Updated memory-sync skill. Memories intact. Next: rebuild heartbeat system."
})
```

### 2. Update Core Memory Block

```javascript
letta_memory_unified({
  operation: "update_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "system/persona",  // or "dd_council_notes", "dd_gremlin_manifest", etc.
  value: "Updated content here..."
})
```

### 3. Create New Memory Block

```javascript
letta_memory_unified({
  operation: "create_block",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "my_custom_block",
  value: "Initial content",
  description: "What this block tracks"
})
```

### 4. Read Current Memory State

```javascript
// Get all core memory blocks
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})

// Get specific block
letta_memory_unified({
  operation: "get_block_by_label",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "dd_gremlin_manifest"
})

// Search archival memory
letta_memory_unified({
  operation: "search_archival",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  query: "Clayton preferences"
})
```

### 5. List All Blocks

```javascript
letta_memory_unified({
  operation: "list_blocks",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

---

## DonDog's Memory Blocks

These are the blocks DonDog uses:

| Block Label | Purpose | Updated By |
|-------------|---------|------------|
| `system/persona` | Core identity, voice, values | DonDog |
| `system/human` | What we know about Clay | DonDog |
| `dd_council_notes` | End-of-beat council decisions | DonDog |
| `dd_gremlin_manifest` | All 24 gremlin agent IDs | DonDog |
| `dd_dispatch_state` | What's been sent, to whom, when | DonDog |
| `linear_task_queue` | Live Kitchen Queue from Linear | Tower Keeper |
| `kitchen_status` | Queue health metrics | Tower Keeper |
| `escalation_board` | Blocked tasks, alerts | DonDog/Chef |

---

## Sync Scenarios

### Scenario 1: Session Checkpoint (Mid-Session)
```
User: "Remember that Clay prefers CLI over GUI"
→ letta_memory_unified update_core_memory label="system/human" 
    value="...Clay prefers CLI over GUI..."
→ Memory updated instantly
```

### Scenario 2: Session End Archive
```
User: "That's all for today"
→ letta_memory_unified insert_passage text="Session 2026-03-24: [summary]"
→ Session logged to archival memory
```

### Scenario 3: After Council Decision
```
[After beat council with Chef + Alfie]
→ letta_memory_unified update_core_memory label="dd_council_notes"
    value="{\"beat\": \"2026-03-24\", \"decisions\": [...], \"queue\": [...]}"
→ Council state preserved
```

### Scenario 4: After Gremlin Dispatch
```
[Dispatched task to Prospector]
→ letta_memory_unified update_core_memory label="dd_dispatch_state"
    value="{\"task\": \"S001\", \"gremlin\": \"Prospector\", \"sent\": \"2026-03-24T14:30:00Z\"}"
→ Dispatch tracked
```

---

## Pulling Fresh Memory

At session start, DonDog's boot sequence pulls core memory:

```javascript
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

To refresh mid-session:
```bash
/memory-sync --pull
# or
/memory-sync --refresh
```

---

## Shared Blocks (Multi-Agent Memory)

DonDog shares blocks with Chef, Alfie, and Tower Keeper:

```javascript
// Attach a block to another agent
letta_memory_unified({
  operation: "attach_block",
  block_id: "block-xxx-xxx",
  agent_id: "agent-xxx-xxx"  // Chef's or Alfie's agent ID
})

// List agents using a block
letta_memory_unified({
  operation: "list_agents_using_block",
  block_id: "block-xxx-xxx"
})
```

---

## Troubleshooting

### "Agent not found" error
- Check agent ID in `.letta/settings.local.json`
- Current valid ID: `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`
- Verify with: `letta_memory_unified get_core_memory agent_id=<id>`

### Memory seems stale
- Pull fresh: `letta_memory_unified get_core_memory`
- Search archival: `letta_memory_unified search_archival query=<topic>`

### Block not updating
- Ensure you're using the correct `label` (case-sensitive)
- Check block exists: `letta_memory_unified list_blocks`

---

## Migration Notes

**OLD (git-based):**
```bash
cd /c/Users/clayb/.letta/agents/agent-48c8.../memory
git add system/
git commit -m "update"
git push
```

**NEW (MCP-based):**
```javascript
letta_memory_unified update_core_memory label="xxx" value="xxx"
```

No more:
- ❌ Git commits for memory
- ❌ Local memory directories
- ❌ Windows paths
- ❌ Old agent IDs
- ❌ Conflict resolution

---

*Skill updated: 2026-03-24 | Converted from git-based to Letta MCP*
