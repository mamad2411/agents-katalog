---
name: lean-context
description: Activate strict context-saving mode mid-conversation. Use when conversations are getting long, before starting large tasks, or when the user says /lean. Audits conversation state and creates a checkpoint summary.
---

# Lean Context Mode

Context efficiency rules are already enforced globally via CLAUDE.md. This skill adds conversation-specific actions when things are getting long.

## Actions (do all of these immediately)

1. **Checkpoint summary**: Write a 2-3 sentence summary of everything accomplished so far and what remains. This creates a "save point" that survives compaction.

2. **Stale context audit**: Identify any large tool outputs earlier in the conversation that are no longer needed (old file reads, long bash outputs, superseded diffs). Note them — they'll be compressed first.

3. **Remaining work estimate**: List what's left to do. If multiple independent tasks remain, suggest parallel agent delegation to keep the main context lean.

4. **Strict mode reminder**: For the rest of this conversation:
   - Re-read nothing — reference earlier checkpoint summaries instead
   - Delegate ANY research to Explore agents
   - Keep all responses to 1-3 sentences unless showing code

## Output

Respond with:
- The checkpoint summary
- "Lean mode active" confirmation
- Any specific suggestions for the current task
