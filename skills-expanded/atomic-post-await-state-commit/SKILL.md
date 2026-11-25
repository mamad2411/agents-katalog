---
name: atomic-post-await-state-commit
description: "After awaiting persistence work, update the shared budget state for each `tool_use_id` exactly once so no concurrent reader ever sees a half-committed decision."
metadata:
  author: ychampion
---

# SKILL: Atomic Post-Await State Commit
**Domain:** tool-orchestration  
**Trigger:** Use this pattern when concurrently persisting large tool results and mutating `ContentReplacementState` once the awaited work completes, such as the `freshReplacements` loop inside `enforceToolResultBudget`.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
Await all selected persistence jobs, then in the same synchronous loop mark each `tool_use_id` as seen and, if persistence succeeded, place the preview string into both the local replacement map and the shared `ContentReplacementState.replacements`. The state mutation happens after the await so other threads or resumed contexts never observe the ID as seen without its replacement (or vice versa), keeping the decision atomic.

## Key Rules
- Never add a `tool_use_id` to `seenIds` before the persist promise resolves; doing so risks another thread classifying the ID as frozen while the replacement string has yet to materialize.
- Mark the ID as seen even when persistence fails so the failure case still freezes the original content and prevents reprocessing the same bytes later.
- When persistence succeeds, update `state.replacements` and `replacementMap` together so immediate replays see the cached preview string with the same bytes that triggered the log/event.
- Keep the loop synchronous after the await; avoid spreading the state updates across callbacks or other async code paths that might observe partial state.

## Example Application
Inside `enforceToolResultBudget`, `freshReplacements` combines each candidate with the result of `buildReplacement`. The for-loop that follows immediately adds every candidate to `state.seenIds`, then conditionally sets `state.replacements` if a preview exists. That ensures when the same `tool_use_id` reappears (for example during a resume or in a forked agent) the code re-applies the cached preview without re-persisting the file.

## Anti-Patterns (What NOT to do)
- Do not call `state.seenIds.add` before awaiting persistence; the race can produce `mustReapply` entries without a matching cached preview.
- Do not leave the replacements map empty after a successful persist; otherwise `applyToolResultBudget` will treat the ID as seen-but-unreplaced and may persist it again later.
- Do not split the success and failure branches across multiple awaits or microtasks; the observer must never see a `seen` entry without the corresponding replacement when one exists.
