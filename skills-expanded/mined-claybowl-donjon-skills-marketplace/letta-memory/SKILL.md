---
name: letta-memory
description: |
  Core Letta memory integration via MCP. Read/write memory blocks, search archival,
  manage agent memory. Direct API — no git, no local files.
  
  Triggers when:
  - "update letta memory"
  - "sync memory"
  - "read letta memory"
  - "letta memory"
  - "memory blocks"
---

# /letta-memory: Letta MCP Memory Integration

Core integration with Letta Cloud memory via the `letta_memory_unified` MCP tool.

## Quick Reference

| Action | MCP Tool | Operation |
|--------|----------|-----------|
| Read all core memory | `letta_memory_unified` | `get_core_memory` |
| Get specific block | `letta_memory_unified` | `get_block_by_label` |
| Update a block | `letta_memory_unified` | `update_core_memory` |
| Create new block | `letta_memory_unified` | `create_block` |
| Search history | `letta_memory_unified` | `search_archival` |
| List all blocks | `letta_memory_unified` | `list_blocks` |
| Save session | `letta_memory_unified` | `create_passage` |
| Attach block to agent | `letta_memory_unified` | `attach_block` |

---

## Agent ID

**DonDog's Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

⚠️ Update in `.letta/settings.local.json` if agent is recreated.

---

## Memory Architecture (MCP-Based)

```
┌─────────────────────────────────────────────────────────┐
│              LETTA CLOUD (agent-d436abf8...)            │
│                                                         │
│  CORE MEMORY BLOCKS                                     │
│  ├── system/persona         (DonDog identity)          │
│  ├── system/human           (Clay's profile)           │
│  ├── dd_council_notes       (council decisions)        │
│  ├── dd_gremlin_manifest    (24 gremlin IDs)           │
│  ├── dd_dispatch_state      (dispatch tracking)        │
│  ├── linear_task_queue      (Kitchen Queue)            │
│  ├── kitchen_status         (queue health)             │
│  └── escalation_board       (blocked items)            │
│                                                         │
│  ARCHIVAL MEMORY                                        │
│  └── Session logs, history, searchable text            │
│                                                         │
│  SHARED BLOCKS                                          │
│  └── Blocks shared with Chef, Alfie, Tower Keeper      │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**All access via MCP. No git. No local files.**

---

## Core Operations

### 1. Read Core Memory (Get Everything)

```javascript
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

### 2. Get Specific Block

```javascript
letta_memory_unified({
  operation: "get_block_by_label",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "dd_gremlin_manifest"  // or "system/human", etc.
})
```

### 3. Update Core Memory Block

```javascript
letta_memory_unified({
  operation: "update_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "system/persona",
  value: "Updated content here..."
})
```

### 4. Create New Block

```javascript
letta_memory_unified({
  operation: "create_block",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "my_custom_block",
  value: "Initial content",
  description: "What this block tracks"
})
```

### 5. Save to Archival Memory (Session Log)

```javascript
letta_memory_unified({
  operation: "create_passage",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  text: "Session 2026-03-24: What happened, decisions made, next steps"
})
```

### 6. Search Archival Memory

```javascript
letta_memory_unified({
  operation: "search_archival",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  query: "Clay preferences communication"
})
```

### 7. List All Blocks

```javascript
letta_memory_unified({
  operation: "list_blocks",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

### 8. Attach Block to Another Agent

```javascript
// Share a block with Chef or Alfie
letta_memory_unified({
  operation: "attach_block",
  block_id: "block-xxx-xxx",
  agent_id: "agent-xxx-xxx"  // Chef's or Alfie's agent ID
})
```

### 9. List Agents Using a Block

```javascript
letta_memory_unified({
  operation: "list_agents_using_block",
  block_id: "block-xxx-xxx"
})
```

---

## DonDog's Block Reference

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

## Workflow Examples

### Session Start
```javascript
// Pull everything DonDog needs to know
letta_memory_unified({ operation: "get_core_memory", agent_id: AGENT_ID })
```

### Mid-Session Update
```javascript
// Learned something new about Clay
letta_memory_unified({ 
  operation: "update_core_memory",
  label: "system/human",
  value: updated_content
})
```

### After Council
```javascript
// Record council decision
letta_memory_unified({
  operation: "update_core_memory",
  label: "dd_council_notes",
  value: JSON.stringify(council_state)
})
```

### Session End
```javascript
// Archive session summary
letta_memory_unified({
  operation: "create_passage",
  text: "Session [date]: [summary]"
})
```

---

## Migration from Old (Git-Based)

**OLD:**
```bash
cd /c/Users/clayb/.letta/agents/agent-48c8.../memory
git add system/
git commit -m "update"
git push
```

**NEW:**
```javascript
letta_memory_unified({ operation: "update_core_memory", label: "xxx", value: "xxx" })
```

---

## Environment

Required env var:
```
LETTA_API_KEY=sk-let-...
```

Already set in `.env` ✅

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Agent not found" | Check agent ID in `.letta/settings.local.json` |
| "Invalid operation" | Check operation name (see Quick Reference) |
| "Block not found" | Use `list_blocks` to see available blocks |
| "Label already exists" | Use `update_core_memory` instead of `create_block` |

---

*Skill updated: 2026-04-29 | Core Letta MCP integration*
