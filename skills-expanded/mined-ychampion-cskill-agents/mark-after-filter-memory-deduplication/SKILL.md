---
name: mark-after-filter-memory-deduplication
description: "Filter prefetched memory attachments against cumulative read state before mutating that state, so async surfacing does not dedupe itself away."
metadata:
  author: ychampion
---

# SKILL: Mark-After-Filter Memory Deduplication
**Domain:** context-management  
**Trigger:** Apply when asynchronously prefetched memories or file attachments must be deduplicated against a cumulative read-state cache that they will also update after surviving the filter.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
When prefetch results need to consult a cumulative "already seen" index, treat that index as read-only during selection. First filter the candidate attachments against the existing state, then write only the survivors into the shared cache. This breaks the self-referential cycle where a prefetch marks everything as seen before dedupe runs, causing the filter to delete the very data it just found. Keep the dedupe state cumulative across the whole turn so later iterations and future turns still suppress genuine repeats.

## Key Rules
- Read from the shared dedupe state during filtering, but do not mutate it until the final survivor set is known.
- Update the shared cache only for attachments that actually survive the filter and remain eligible for surfacing.
- Use a cumulative state store that includes earlier loop iterations and prior surfaced memories, not just the current batch.
- Keep the mutation step adjacent to the filter so future maintainers cannot reintroduce self-poisoning writes inside the prefetch path.

## Example Application
If a background document selector prefetches five candidate help files while the main agent is still running tools, first drop any files already present in the session's read-state map. Only after that should you record the surviving files in the map, ensuring they surface once now and stay suppressed on later retries.

## Anti-Patterns (What NOT to do)
- Do not mark prefetched files as read before duplicate filtering; the filter will see its own writes and erase the whole batch.
- Do not dedupe only against the current iteration's attachments; you need cumulative session state to avoid resurfacing files already read by tools or earlier turns.
