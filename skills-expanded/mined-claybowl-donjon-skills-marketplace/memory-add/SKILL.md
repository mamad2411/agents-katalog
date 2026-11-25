---
name: memory-add
description: |
  Quickly add a new memory to Letta Cloud via MCP. One-shot memory capture
  without full session analysis. Just tell it what to remember.
  
  Triggers: "remember this", "add to memory", "save this", "note that",
            "log this", "make a note", "store this"
---

# /memory-add: Quick Memory Add

Add a single memory to Letta Cloud. Fast, simple, direct.

## Quick Start

```bash
# Add a quick note
/memory-add "Clay prefers CLI over GUI interfaces"

# Add with context
/memory-add "Decision: Using Letta MCP instead of git-based memory"
```

## Agent ID

**DonDog's Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

## Core Operation

### Add to Archival Memory

```javascript
letta_memory_unified({
  operation: "insert_passage",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  text: "Your memory text here"
})
```

That's it. One API call. Done.

---

## When to Use Each Operation

| What You're Saving | Operation | Example |
|--------------------|-----------|---------|
| Quick note/fact | `insert_passage` | "Clay prefers dark mode" |
| Update to identity | `update_core_memory` label="system/persona" | New voice trait |
| Update Clay's profile | `update_core_memory` label="system/human" | New preference |
| Council decision | `update_core_memory` label="dd_council_notes" | Beat decision |
| Dispatch tracking | `update_core_memory` label="dd_dispatch_state" | Task sent |
| New tracking block | `create_block` | Custom tracker |

---

## Examples

### Example 1: Remember a Preference
```
User: "Remember I prefer dark mode"
→ letta_memory_unified insert_passage text="Preference: Clay prefers dark mode interfaces"
→ Done.
```

### Example 2: Log a Decision
```
User: "Note that we decided to use Letta MCP instead of git"
→ letta_memory_unified insert_passage text="Decision: Switched from git-based memory to Letta MCP for all memory operations"
→ Done.
```

### Example 3: Update Clay's Profile
```
User: "Add that I'm a night owl to my profile"
→ letta_memory_unified get_block_by_label label="system/human"
→ Read current value
→ letta_memory_unified update_core_memory label="system/human" value="[current] + Night owl: prefers working late"
→ Done.
```

---

## Tips

1. **Keep it concise** — Archival memory is searchable, not just storage
2. **Use prefixes** — "Preference:", "Decision:", "Fact:", "Goal:" for easy searching
3. **Timestamp implicitly** — `insert_passage` timestamps automatically
4. **Use blocks for structured data** — Blocks for identity/profile, archival for history

---

## Troubleshooting

### "Agent not found"
- Verify ID: `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

### Want to verify it was saved
- Search: `letta_memory_unified search_archival query="[your text]"`
- Or check with: `/memory-search`

---

*Skill updated: 2026-03-24 | Quick memory capture via Letta MCP*
