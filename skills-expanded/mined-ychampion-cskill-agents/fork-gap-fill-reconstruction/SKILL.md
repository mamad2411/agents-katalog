---
name: fork-gap-fill-reconstruction
description: "Reconstruct child replacement state from local records first, then fill uncovered gaps from the parent's live map."
metadata:
  author: ychampion
---

# SKILL: Fork Gap-Fill Reconstruction
**Domain:** multi-agent  
**Trigger:** Apply when a forked or resumed child workflow must inherit prior replacement decisions even though its local transcript lacks full replacement records.
**Source Pattern:** Distilled from reviewed multi-agent coordination and child-runtime patterns.

## Core Method
Rebuild child state from the records the child actually persisted, then fill any uncovered IDs from the parent's live replacement map. This handles the fork-resume case where inherited replacements were applied during the original run but never written as new child records. The result is a child state that replays the same cached previews the model originally saw instead of freezing those IDs as unreplaced gaps.

## Key Rules
- Reconstruct from local records first so the child transcript remains the primary source of truth for what it explicitly persisted.
- Use parent replacements only as a gap-fill for IDs still present in the resumed messages and not already covered by child records.
- Preserve the `seenIds` freeze semantics while layering in inherited replacements so resumed children do not recalculate different decisions.
- Skip inherited mappings for IDs absent from the resumed message set; they are inert and should not pollute the child state.

## Example Application
When a forked review agent resumes from sidechain transcript records, rebuild its replacement state from those records and then copy any missing preview strings from the parent’s live replacement map so the resumed child continues using the exact previews it saw before the interruption.

## Anti-Patterns (What NOT to do)
- Do not rely on child records alone for fork-resume cases; inherited replacements may never have been persisted by the child.
- Do not blindly copy the entire parent replacement map into the child; only IDs present in the resumed messages should be imported.
