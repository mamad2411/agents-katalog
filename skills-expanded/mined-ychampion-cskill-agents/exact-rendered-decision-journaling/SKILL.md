---
name: exact-rendered-decision-journaling
description: "Journal each per-message tool result replacement so resume logic replays the exact preview the model saw."
metadata:
  author: ychampion
---

# SKILL: Exact Rendered Decision Journaling
**Domain:** tool-orchestration  
**Trigger:** Apply whenever per-message budgeting rewrites tool_result content so transcripts capture the preview string and resume logic can reapply the same decisions.
**Source Pattern:** Distilled from reviewed tool-loop and result-shaping patterns.

## Core Method
After `enforceToolResultBudget` persists a candidate, produce a `ToolResultReplacementRecord` (`kind: 'tool-result'`, `toolUseId`, `replacement`) that stores the literal preview returned by `buildLargeToolResultMessage`. Pass `newlyReplaced` to the `writeToTranscript` callback so every replacement is serialized in the conversation transcript; later, `reconstructContentReplacementState(messages, records, inheritedReplacements)` can rebuild the same `seenIds`/`replacements` map, and `provisionContentReplacementState` gates the feature flag (`tengu_hawthorn_steeple`) so journaling stays optional.

## Key Rules
- Persist the exact preview string the model consumed—the replacement record must not approximate or trim the visible content, or prompt-cache alignment breaks.
- Include `toolUseId` with each record so resume enforcement can quickly look up replacements without re-running persistence.
- Forward `parentState.replacements` into `reconstructForSubagentResume` when resuming forks so inherited decisions reapply exactly.
- Guard `writeToTranscript`; it may be undefined in ephemeral contexts, so only call it when provided.
- When the flag is disabled, `provisionContentReplacementState` should return `undefined` and journaling remains inert.

## Example Application
In the query loop pass the transcript writer to `applyToolResultBudget`; the callback serializes `newlyReplaced` records, which are later replayed by `provisionContentReplacementState(initialMessages, records)` during resume so the budget enforces the same replacements it originally made.

## Anti-Patterns (What NOT to do)
- Do not journal before `persistToolResult` succeeds and the preview is built—the replacement string must exist before you write it down.
- Do not drop `kind: 'tool-result'` or the `toolUseId` fields; `reconstructContentReplacementState` relies on them to filter and lookup.
- Avoid journaling duplicates (e.g., from re-applied replacements); only persist what is new so transcripts stay minimal.
