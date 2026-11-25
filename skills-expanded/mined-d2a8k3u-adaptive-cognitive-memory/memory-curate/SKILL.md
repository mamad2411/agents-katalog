---
name: memory-curate
description: >
  Review this project's memories with the user and clean them up: hypotheses,
  duplicates, stale facts, wrong scope and recall keys. Use when the user asks to curate,
  review, audit or tidy the memory, or when memory_status shows many hypotheses.
---

# Memory curation

Propose every change and wait for the user's confirmation before you delete, supersede or update a memory; never run this unattended. Present the proposals as a short list with each memory's id and title.

1. **Status.** Call `memory_status` and keep its counts by state and kind for the end.
2. **Hypotheses.** `memory_list` with `state: "hypothesis"`; read each with `memory_get`. Propose to keep it (a `used` verdict through `memory_feedback` brings it back), correct it with `memory_update` or delete it with `memory_delete`.
3. **Duplicates.** For each hypothesis and each memory on the listed pages, `memory_search` its title; it finds active and hypothesis memories alike. A different memory that teaches the same lesson is a duplicate. Propose one merge per pair: keep the more complete one (an active one before a hypothesis), fold anything only the other says into it with `memory_update`, then `memory_delete` the other; for a changed single-valued fact use `memory_store` with resolution `SUPERSEDE` instead.
4. **Stale facts.** `memory_list` with `kind: "fact"`, newest first; pass `next_cursor` as `before` for the next page. A changed value is a `memory_store` with resolution `SUPERSEDE`; a fact that no longer holds is a `memory_delete`.
5. **Wrong scope.** Scope and kind cannot change in place: store the memory again with the right scope or kind (`memory_store`), then delete the old one (`memory_delete`).
6. **Recall keys.** Fix keywords and anchors with `memory_update`, following [the authoring standard](../memory/references/authoring.md) (`memory/references/authoring.md`); each replaces the stored value whole. A memory without `questions` is found less often: propose 3–6, in English and in the user's language, and add them with `memory_update`.
7. **Before and after.** Call `memory_status` again and report both sets of counts.

A memory that `memory_list` finds only with `project: "all"` belongs to another project: it is read-only here and can be changed only from a session in its own project.
