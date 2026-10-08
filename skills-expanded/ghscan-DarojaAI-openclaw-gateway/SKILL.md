---
name: session-commands
description: Session control commands (/reset, /compact, /stop). Use when user sends /reset, /compact, or /stop in any channel.
---

# Session Commands

These special commands control the session lifecycle. Execute them immediately without asking for confirmation.

## /reset

**Purpose:** Clear all conversation history and start fresh.

**Actions:**
1. Find and delete the session file: `/home/desktopuser/.openclaw/agents/*/sessions/*.jsonl` (for the current agent)
2. Confirm: "Session reset. Starting fresh."

## /compact

**Purpose:** Reduce context size by truncating conversation history.

**Actions:**
1. Find the session file: `/home/desktopuser/.openclaw/agents/*/sessions/*.jsonl`
2. Keep only the last 100 lines of the session file
3. Confirm: "Session compacted. Context reduced."

## /stop

**Purpose:** Stop any in-progress tool execution.

**Actions:**
1. Do not execute any more tools
2. Confirm: "Stopping. Let me know if you need anything else."

## Session File Location

The session file path follows this pattern:
```
/home/desktopuser/.openclaw/agents/{agent-id}/sessions/{session-id}.jsonl
```

To find the current session, use glob pattern: `/home/desktopuser/.openclaw/agents/*/sessions/*.jsonl`