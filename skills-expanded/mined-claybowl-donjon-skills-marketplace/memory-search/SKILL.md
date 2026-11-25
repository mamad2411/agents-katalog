---
name: memory-search
description: |
  Search across all Letta memory (core blocks + archival) for specific information.
  Uses MCP API calls instead of grep. Smart, fast, cloud-powered.
  
  Triggers: "search memory", "find in memory", "remember when", "what did we say about",
            "look up memory", "find memory", "what do I know about"
---

# /memory-search: Search Letta Memory

Search across all Letta memory via MCP — core blocks and archival history.

## Quick Start

```bash
# Search archival memory
/memory-search "vibe native"

# Search for decisions
/memory-search "decided to pivot"

# Search Clay's preferences
/memory-search "Clay prefers"
```

## Agent ID

**DonDog's Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

## What It Does

1. **Query Parse** - Understand what to search for
2. **Search Archival** - Scan session history and past memories
3. **Read Blocks** - Check relevant core memory blocks
4. **Rank** - Order results by relevance
5. **Present** - Show findings with context

**No grep. No local files. Direct MCP API.**

---

## Core Operations

### Search Archival Memory

```javascript
letta_memory_unified({
  operation: "search_archival",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  query: "vibe native launch"
})
```

### Get All Core Memory (then search locally)

```javascript
// Pull all blocks, then scan
letta_memory_unified({
  operation: "get_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

### Get Specific Block

```javascript
// Direct block access
letta_memory_unified({
  operation: "get_block_by_label",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "system/human"
})
```

### List All Blocks (see what's available)

```javascript
letta_memory_unified({
  operation: "list_blocks",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763"
})
```

---

## Search Strategies

### Strategy 1: Archival First (Historical)
```javascript
// Best for: "remember when", "what did we say about X"
letta_memory_unified({
  operation: "search_archival",
  query: "whatever you're looking for"
})
```

### Strategy 2: Block-Specific (Current State)
```javascript
// Best for: "what's my current queue", "show me gremlin manifest"
letta_memory_unified({
  operation: "get_block_by_label",
  label: "dd_gremlin_manifest"  // or "linear_task_queue", "system/human", etc.
})
```

### Strategy 3: Broad Pull (Everything)
```javascript
// Best for: "show me everything I know"
letta_memory_unified({
  operation: "get_core_memory"
})
```

---

## Common Search Patterns

### Find Preferences
```
/memory-search "Clay prefers"
/memory-search "communication style"
→ search_archival query="Clay preferences communication"
```

### Find Decisions
```
/memory-search "what did we decide"
/memory-search "pivot"
→ search_archival query="decisions pivot strategy"
```

### Find Goals
```
/memory-search "current goals"
/memory-search "what are we working on"
→ get_block_by_label label="dd_council_notes"
```

### Find Technical Context
```
/memory-search "MCP setup"
/memory-search "Letta configuration"
→ search_archival query="MCP Letta configuration"
```

### Find People/Contacts
```
/memory-search "Clay's email"
/memory-search "who is"
→ get_block_by_label label="system/human"
```

---

## Output Format

Present results clearly:

```
=== MEMORY SEARCH RESULTS ===

Query: "vibe native"

📦 Core Blocks (2 matches):
   system/human: "Building Vibe Native - AI PM tool"
   dd_council_notes: "Vibe Native MVP target: March 15"

📜 Archival Memory (5 matches):
   Session 2026-03-15: "Launched Vibe Native beta"
   Session 2026-03-10: "Vibe Native milestone: 100 users"
   Session 2026-03-05: "Pricing decision: $49/mo"
   Session 2026-02-28: "Vibe Native MVP completed"
   Session 2026-02-20: "Started Vibe Native development"

💡 Summary:
   - Project: Vibe Native (AI PM tool)
   - Status: Beta, 100 users
   - Pricing: $49/mo
   - Last update: March 15, 2026

=============================
```

---

## When to Use

| Scenario | Search Approach |
|----------|----------------|
| "What did we decide about X?" | `search_archival query="decided X"` |
| "When is the launch?" | `search_archival query="launch date"` |
| "What do I prefer?" | `get_block_by_label label="system/human"` |
| "What are we working on?" | `get_block_by_label label="linear_task_queue"` |
| "Tell me about Y" | `search_archival query="Y"` (broad) |

---

## Tips

1. **Try archival first** for historical questions
2. **Check specific blocks** for current state
3. **Use natural language** — search understands context
4. **Combine approaches** — archival + blocks = complete picture
5. **No file system access needed** — everything via MCP

---

## Troubleshooting

### No results found
- Try different search terms
- Broader query: use simpler keywords
- Check if block exists: `list_blocks`

### Memory seems stale
- Archival is always current
- Pull fresh core: `get_core_memory`

### Agent not found
- Verify ID: `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

*Skill updated: 2026-03-24 | Converted from grep-based to Letta MCP*
