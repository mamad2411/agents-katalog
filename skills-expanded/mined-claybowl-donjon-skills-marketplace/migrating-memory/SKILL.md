---
name: migrating-memory
description: |
  Migrate or copy memory blocks between Letta agents using MCP.
  Useful when setting up new agents or sharing memory across agents.
  
  Triggers: "migrate memory", "copy memory", "share memory between agents"
---

# /migrating-memory: Agent Memory Migration

Copy memory blocks between Letta agents via MCP.

## Agent ID

**DonDog's Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

## How It Works

```
Source Agent (read blocks) → Copy content → Target Agent (create/update blocks)
```

All via MCP. No git. No local files.

---

## Operations

### 1. Read Source Agent's Blocks

```javascript
// Get all blocks from source agent
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-source-id"
})

// Or get specific block
letta_memory_unified({
  operation: "get_block_by_label",
  agent_id: "agent-source-id",
  label: "system/persona"
})
```

### 2. Create Block in Target Agent

```javascript
// Create new block in target
letta_memory_unified({
  operation: "create_block",
  agent_id: "agent-target-id",
  label: "system/persona",  // or "migrated_block" to avoid conflicts
  value: "content from source...",
  description: "Migrated from agent-source-id"
})
```

### 3. Update Existing Block in Target

```javascript
// If block already exists, update it
letta_memory_unified({
  operation: "update_core_memory",
  agent_id: "agent-target-id",
  label: "system/persona",
  value: "updated content..."
})
```

---

## Common Scenarios

### Scenario 1: Set Up New Agent with DonDog's Memory

```javascript
// 1. Get DonDog's blocks
letta_memory_unified({ operation: "get_core_memory", agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763" })

// 2. Create in new agent
letta_memory_unified({
  operation: "create_block",
  agent_id: "agent-new-id",
  label: "system/persona",
  value: "[persona content from DonDog]"
})
```

### Scenario 2: Share Block Across Agents (Attach)

```javascript
// Attach existing block to another agent
letta_memory_unified({
  operation: "attach_block",
  block_id: "block-xxx-xxx",
  agent_id: "agent-other-id"
})
```

### Scenario 3: Clone Specific Knowledge

```javascript
// 1. Search source for specific topic
letta_memory_unified({
  operation: "search_archival",
  agent_id: "agent-source-id",
  query: "project X decisions"
})

// 2. Create new block in target with that content
letta_memory_unified({
  operation: "create_block",
  agent_id: "agent-target-id",
  label: "knowledge/project-x",
  value: "relevant content from search results..."
})
```

---

## Handling Duplicate Labels

If target agent already has a block with that label:

| Option | How |
|--------|-----|
| **Rename** | Use different label: `migrated_system/persona` |
| **Override** | Use `update_core_memory` instead of `create_block` |
| **Attach** | Use `attach_block` to share (not copy) the block |

---

## Block Reference

| Block Label | What It Contains |
|-------------|------------------|
| `system/persona` | Agent identity, voice, values |
| `system/human` | User profile, preferences |
| `dd_council_notes` | DonDog council decisions |
| `dd_gremlin_manifest` | 24 gremlin agent IDs |
| `dd_dispatch_state` | Dispatch tracking |
| `linear_task_queue` | Kitchen Queue |
| `kitchen_status` | Queue health |
| `escalation_board` | Blocked tasks |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "Agent not found" | Verify source/target agent ID |
| "Block already exists" | Use `update_core_memory` or different label |
| "Invalid label" | Labels are case-sensitive, no special chars |
| "Block not found" | Use `list_blocks` to see available blocks |

---

*Skill updated: 2026-03-24 | MCP-based agent migration*
