---
name: nested-memory-trigger-consume-and-clear
description: "Process every nested-memory trigger before wiping the trigger set so subsequent iterations only see new paths."
metadata:
  author: ychampion
---

# SKILL: Nested Memory Trigger Consume and Clear
**Domain:** context-management  
**Trigger:** Apply when a worker must fetch nested memory attachments whose trigger list can be cleared only after all paths are handled.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Treat the trigger set as authoritative input, not a mutable queue that shrinks mid-processing. First return with an empty list if no triggers exist so render-bound helpers like `getAppState()` never run unnecessarily. Once you know work is required, snapshot the triggers, iterate over every path to gather nested attachments holding onto shared app state, append all results to the response, and only after the loop completes clear the trigger set. This prevents stale triggers from re-running in future turns while ensuring concurrent iterations do not drop paths that were just discovered.

## Key Rules
- Guard the expensive `getAppState()` call with an early return whenever `nestedMemoryAttachmentTriggers` is empty.
- Iterate through every trigger before clearing the set so no pending path disappears mid-loop.
- Collect nested attachments with the shared `appState` object to avoid repeated renders.
- Clear the trigger set explicitly after collecting results, not before, so next invocations start fresh.

## Example Application
When multiple nested memories are queued while a thread is still running, fetch them all inside a single `getNestedMemoryAttachments` call, clear the triggers afterward, and then hand the flattened attachment list to the caller.

## Anti-Patterns (What NOT to do)
- Do not clear the trigger set before iterating; that can make the next call think the paths were already handled.
- Do not call `getAppState()` when there are no triggers, which wastes React render cycles.
