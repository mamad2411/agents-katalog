---
name: time-based-microcompact-trigger
description: "Fall back to time-based microcompaction when the idle gap exceeds the configured threshold and directly clear the oldest compactable tool results."
metadata:
  author: ychampion
---

# SKILL: Time-Based Microcompact Trigger
**Domain:** context-management  
**Trigger:** Apply when the interval since the last assistant response exceeds the threshold and cached microcompact cannot run.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Measure the minutes since the last main-thread assistant message, compare it to `gapThresholdMinutes`, and only fire when the configured trigger is enabled and the caller is the main thread. When triggered, keep the last `keepRecent` tool results and content-clear the rest by replacing their content with the `[Old tool result content cleared]` marker. Log the elapsed gap, tokens saved, and retained count so operators can tune the gap threshold.

## Key Rules
- Require a specific `querySource` (main thread) before firing so external helpers do not misinterpret delays as triggers.
- Return `null` unless the gap exceeds the threshold, ensuring callers only run the clearing logic when necessary.
- Always keep at least one tool result so the model retains some recent state after the purge.
- Reset cached microcompact state and notify cache deletion after the clearing to keep downstream cache tracking in sync.
- Emit analytics and debug logs describing the gap, tokens saved, and how many tools were cleared.

## Example Application
When a session sits idle longer than `gapThresholdMinutes`, apply this trigger to replace outdated tool results with `[Old tool result content cleared]`, log the 12-minute gap, and still leave the last tool result so future summaries have some fresh context.

## Anti-Patterns (What NOT to do)
- Do not run this trigger for non-main-thread sources; the clearing assumes global cache edits.
- Do not drop all cached tools (keep at least one), or the next turn loses every tool reference and can exceed budget on the first message.
