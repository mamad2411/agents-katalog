---
name: summarize
description: Summarize the current chat in 10 lines covering decisions, open questions, and the next step.
disable-model-invocation: true
---

# Summarize

Summarize this chat in exactly 10 lines: what we decided, what is still open, and the next step.

## Steps

1. Read the available conversation. Identify settled decisions, unresolved questions or blockers, and the next action. Treat the latest corrections as authoritative and keep proposals distinct from decisions. Done when each summary item has support in the chat.
2. Write exactly 10 numbered lines, one concise sentence per line. Put decisions first, open items next, and the next step on line 10. Include owners or dependencies when the chat names them. If no open items or next step are established, say so. Use remaining lines for relevant context or completed work when needed. Done when all three requested topics appear without invented facts or repeated filler.
3. Count the lines and check each claim against the conversation. Return only the 10 numbered lines. Done when there are no headings, blank lines, or extra commentary.
