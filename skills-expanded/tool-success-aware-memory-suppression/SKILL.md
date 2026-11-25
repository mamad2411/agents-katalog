---
name: tool-success-aware-memory-suppression
description: "Suppress context docs for tools that already succeeded in the current turn while keeping help available for failures or unresolved runs."
metadata:
  author: ychampion
---

# SKILL: Tool Success Aware Memory Suppression
**Domain:** memory-selection
**Trigger:** Apply when contextual docs or memories should stay hidden for tools that are already working, but remain available for tools that failed or have unknown outcomes.
**Source Pattern:** Distilled from reviewed turn-local memory selection and tool-outcome suppression implementations.

## Core Method
Scan the current human-turn window, pair tool invocations with their results, and suppress context only for tools that show clear success with no failures in that window. If any call failed or no result arrived yet, keep that tool eligible for docs or memories so the runtime spends budget on unresolved problems instead of re-explaining tools that are already working. This keeps context targeted at the model's current points of friction.

## Key Rules
- Bound the scan to the current human-turn window so old successes do not suppress guidance for a new problem.
- Match invocations to results through stable IDs before resolving suppression by tool name.
- Treat any failure as a reason to keep that tool's docs available, even if other calls succeeded.
- Do not suppress tools with missing results; unresolved work should remain eligible for help.

## Example Application
If the model successfully uses file-reading tools several times while still struggling with shell execution, suppress context docs for the file-reading tools during this turn and keep shell guidance eligible because the failures show it still needs help there.

## Anti-Patterns (What NOT to do)
- Do not suppress docs just because a tool was invoked; invocation without a result says nothing about whether the tool is understood.
- Do not let one earlier success hide docs after a later failure for the same tool; the failure reopens the need for guidance.
