---
name: memory-init
description: |
  Initialize memory at the start of every session. Pulls latest core memory from 
  Letta Cloud via MCP, loads identity and context, and prepares session state.
  MUST be run at the beginning of each OpenCode session.
  
  Triggers: "init memory", "start session", "load memory", "pull memories", "session start"
---

# /memory-init: Session Start Protocol

Run this skill at the **beginning of every OpenCode session** to pull from Letta Cloud.

## Quick Start

```bash
# At session start, ALWAYS run:
/memory-init
```

## What It Does

1. **Pull Core Memory** - Fetches all memory blocks from Letta via MCP
2. **Load Identity** - Restores DonDog persona, Clay profile, gremlin manifest
3. **Check Kitchen** - Reads task queue, dispatch state, escalations
4. **Session Ready** - Displays current context and active work

## Agent ID

**DonDog's Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

## Workflow

```
Session Start → /memory-init → Pull from Letta → Load Context → Ready to Work
```

**No git. No local files. Direct MCP API.**

---

## Core Memory Pulled

| Block Label | What It Contains |
|-------------|------------------|
| `system/persona` | DonDog identity, voice, values |
| `system/human` | Clay's profile and preferences |
| `dd_gremlin_manifest` | All 24 gremlin agent IDs |
| `dd_council_notes` | Recent council decisions |
| `dd_dispatch_state` | What's been sent, to whom |
| `linear_task_queue` | Live Kitchen Queue |
| `kitchen_status` | Queue health metrics |
| `escalation_board` | Blocked tasks, alerts |

---

## Commands

### Initialize Session (Full Pull)

```javascript
// Pull all core memory blocks
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

### Get Specific Block

```javascript
// Example: Get gremlin manifest
letta_memory_unified({
  operation: "get_block_by_label",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "dd_gremlin_manifest"
})
```

### Search Archival Memory

```javascript
// Find past sessions about a topic
letta_memory_unified({
  operation: "search_archival",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  query: "recent sessions"
})
```

---

## Output Format

After running `/memory-init`, display:

```
=== MEMORY INITIALIZED ===

🔄 Source: Letta Cloud (MCP)
🆔 Agent: agent-d436abf8-6057-44a6-8019-5f5dc0b22763

📋 Core Memory Blocks:
   ✓ system/persona (DonDog identity)
   ✓ system/human (Clay's profile)
   ✓ dd_gremlin_manifest (24 gremlins)
   ✓ dd_council_notes (council state)
   ✓ dd_dispatch_state (dispatch tracking)
   ✓ linear_task_queue (Kitchen Queue)
   ✓ kitchen_status (queue health)
   ✓ escalation_board (blocked items)

🎯 Current Context:
   [From soul.md priorities]
   [From linear_task_queue]
   [From dd_council_notes]

💡 Next Steps:
   [Based on current priorities]

=========================
```

---

## Troubleshooting

### "Agent not found" error
- Verify agent ID: `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`
- Check `.letta/settings.local.json` for current ID
- Test connection: `letta_memory_unified get_core_memory agent_id=<id>`

### Memory seems stale
- This shouldn't happen — MCP is always current
- If blocks are missing, check with `letta_memory_unified list_blocks`
- Search archival for older info: `letta_memory_unified search_archival`

### Blocks not loading
- Ensure `LETTA_API_KEY` is set in environment
- Check Letta API status

---

## Important Notes

- **ALWAYS run at session start** — This is non-negotiable
- **No git involved** — Direct API calls to Letta Cloud
- **No conflict resolution needed** — It's an API, not a repo
- **Letta Cloud is source of truth** — Always

---

*Skill updated: 2026-03-24 | Converted from git-based to Letta MCP*
