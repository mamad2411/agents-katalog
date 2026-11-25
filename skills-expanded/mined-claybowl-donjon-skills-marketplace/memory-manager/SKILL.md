---
name: memory-manager
description: |
  Manual skill for memory management. Analyzes recent conversations, extracts key updates,
  and pushes them to Letta Cloud via MCP. No git required!
  
  Triggers when user mentions:
  - "analyze conversation"
  - "memory manager"
  - "extract key updates"
  - "commit memory"
  - "sync conversation to memory"
  - "save to memory"
---

# /memory-manager: Conversation Analysis & Memory Injection

Manually analyze conversations, extract key updates, and sync to Letta Cloud via MCP.

## Quick Start

```bash
# Analyze recent conversation and save to memory
/memory-manager

# Dry run (preview without saving)
/memory-manager --dry-run

# Custom number of messages to analyze
/memory-manager --span 50
```

## Agent ID

**DonDog's Letta agent ID:** `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`

---

## What It Does

1. **Pull Session History** - Get recent conversation messages
2. **Extract Key Updates** - Identify decisions, goals, constraints, knowledge, plans
3. **Push to Letta** - Write updates via MCP (no git!)

---

## Key Update Types

| Type | Description | Letta Block |
|------|-------------|-------------|
| `decision_log` | Critical decisions, pivots, strategy shifts | `dd_council_notes` or archival |
| `goal_change_log` | Goal additions, completions | `system/human` or archival |
| `constraint_risk_log` | New constraints, blockers | `escalation_board` |
| `knowledge_log` | New concepts, terminology | Archival memory |
| `plan_log` | Next steps, action items | `dd_council_notes` |

---

## Core Operations

### Push Session Summary to Archival Memory

```javascript
letta_memory_unified({
  operation: "insert_passage",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  text: "Session 2026-03-24: [summary of what happened, decisions made, next steps]"
})
```

### Update Specific Block

```javascript
// Update council notes after a decision
letta_memory_unified({
  operation: "update_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "dd_council_notes",
  value: "{\"last_council\": \"2026-03-24\", \"decisions\": [...], \"queue\": [...]}"
})

// Add to escalation board
letta_memory_unified({
  operation: "update_core_memory",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "escalation_board",
  value: "{\"blocked\": [{\"task\": \"S001\", \"reason\": \"needs phone numbers\"}]}"
})
```

### Create New Block (if needed)

```javascript
letta_memory_unified({
  operation: "create_block",
  agent_id: "agent-d436abf8-6057-44a6-8019-5f5dc0b22763",
  label: "my_new_block",
  value: "Initial content",
  description: "What this block tracks"
})
```

---

## Extraction Patterns

### Decision Detection
Phrases like:
- "we will", "decide to", "pivot to", "going with X"
- "I want to", "let's do", "commit to"

### Goal Changes
Phrases like:
- "target is now", "goal is to", "prioritize X"
- "completed", "finished", "done with"

### Constraints/Risks
Phrases like:
- "deadline", "budget", "can't do"
- "risk is", "concern is", "blocking issue"

---

## Usage Examples

### Example 1: End of Session
```
User: "Let's save what we did today"
→ Analyze conversation
→ letta_memory_unified insert_passage text="Session 2026-03-24: Reconnected DonDog, updated skills, planned heartbeat rebuild"
→ Memory updated instantly
```

### Example 2: After Council Decision
```
[Council with Chef + Alfie completed]
→ letta_memory_unified update_core_memory label="dd_council_notes" value="{...}"
→ Council state preserved
```

### Example 3: Track a Dispatch
```
[Dispatched task to Prospector]
→ letta_memory_unified update_core_memory label="dd_dispatch_state" value="{...}"
→ Dispatch tracked
```

---

## Safety

- **Dry run available** — Preview what would be saved before committing
- **Always verify** — Check that blocks updated correctly
- **Direct API** — No git, no merge conflicts, no local files

---

## Troubleshooting

### No messages found
- Check session history availability
- Try different --span value

### Block not updating
- Ensure correct `label` (case-sensitive)
- Check block exists: `letta_memory_unified list_blocks`
- Create if missing: `letta_memory_unified create_block`

### Agent not found
- Verify ID: `agent-d436abf8-6057-44a6-8019-5f5dc0b22763`
- Check `.letta/settings.local.json`

---

*Skill updated: 2026-03-24 | Converted from git-based to Letta MCP*
