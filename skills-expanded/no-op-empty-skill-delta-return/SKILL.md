---
name: no-op-empty-skill-delta-return
description: "Return no attachment when an incremental skill delta has no unseen items instead of emitting a formally empty update payload."
metadata:
  author: ychampion
---

# SKILL: No-Op Empty Skill Delta Return
**Domain:** command-surfaces  
**Trigger:** Apply when an incremental attachment or announcement pass recomputes a delta set and discovers there is nothing new to send.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Treat an empty delta as the absence of an event, not as an event with empty contents. After filtering the candidate set down to unseen items, return immediately with no attachment if that delta set is empty. This keeps the downstream stream free of meaningless no-op payloads, avoids forcing consumers to special-case empty updates, and preserves the semantic distinction between "nothing changed" and "something changed but happened to serialize to an empty-looking object."

## Key Rules
- Compute the delta set first, then check for emptiness before doing any formatting or payload construction.
- Return no attachment at all when the delta is empty; do not emit placeholder objects, zero-count events, or empty content strings.
- Keep the no-op return close to the delta filter so future refactors cannot accidentally reintroduce formatting work for empty updates.
- Preserve the difference between empty delta and initial/dynamic batch metadata; batch semantics only exist when something is actually emitted.

## Example Application
If a command-listing attachment runs after a plugin reload but every visible command was already announced earlier in the session, detect that `newCommands` is empty and return `[]`. The caller sees no update event because the actionable surface did not change.

## Anti-Patterns (What NOT to do)
- Do not emit an empty delta object just so the pipeline has a uniform shape; that creates noise consumers must ignore.
- Do not continue into expensive formatting or logging after discovering the unseen set is empty.
