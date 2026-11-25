---
name: proof-cooker
description: Synthesize source-indexed proof-material items into the final proof-usage playbook. Use when Codex needs to cluster proof items by proof shape, de-duplicate across sources, design reusable taxonomy entries, update proof-usage indexes and source maps, or preserve material-ID links from cooked proof entries.
---

# Proof Cooker

## Overview

Use this skill after `proof-material` contains enough indexed material to justify reusable categories. The job is synthesis: cluster source-local items, identify transferable proof shapes, merge or distinguish near-duplicates, and write concise cooked entries into `proof-usage`.

Do not copy every material item into `proof-usage`. Prefer fewer, clearer entries that a future proof agent can actually find and adapt.

## Pipeline Position

`proof-cooker` is the synthesis stage:

```text
proof-material -> proof-cooker -> proof-usage
```

Its job is judgment. It reads source-indexed evidence, decides which items share a reusable proof shape, preserves differences that matter, and updates the final playbook without erasing material IDs.

## Inputs And Outputs

- Input: one or more `proof-material/references/<source-slug>.md` files plus the material index.
- Output: `proof-usage/references/index.md`, category files, and `proof-usage/references/source-map.md`.
- Reference templates: [references/taxonomy-template.md](references/taxonomy-template.md) and [references/cooking-checklist.md](references/cooking-checklist.md).

## Cooking Workflow

1. Load candidate material.
   - Read the relevant material files and their local indexes.
   - Track each source ID that may become part of a cooked entry.
2. Cluster by transferable shape.
   - Compare proof object, assumptions, mathematical mechanism, failure modes, and adaptation path.
   - Keep source-local differences visible when they matter.
3. Decide taxonomy placement.
   - Use `local-moves/` for reusable lemmas, estimates, inequalities, localization steps, and parameter balances.
   - Use `strategies/` for macro proof decompositions, auxiliary models, algorithm-analysis templates, or multi-phase arguments.
   - Add a new category only when existing files would make discovery worse.
4. Write cooked entries.
   - Use the cooked entry contract from [references/taxonomy-template.md](references/taxonomy-template.md).
   - Include `Material sources` with stable IDs and `Public attribution`.
   - State assumptions and failure modes explicitly.
5. Update discovery aids.
   - Add task-shape, assumptions, desired-move, tag, and source-ID routes to `proof-usage/references/index.md`.
   - Update `proof-usage/references/source-map.md` so every cooked entry can be traced back to material IDs.
6. Preserve legacy value.
   - If old `techniques.md` or `strategies.md` entries are superseded, leave a compatibility note or link them from the source map.
   - Do not delete useful old cards unless their replacements are already indexed.

## De-Duplication Rules

- Merge items only when they share the same reusable proof shape and compatible assumptions.
- Split items when the same high-level idea has materially different prerequisites, rates, objects, or failure modes.
- Compare near-duplicates in the entry instead of forcing one source to fit another source's conditions.
- Keep source attribution public and compact.

## Quality Bar

- A cooked entry must be usable without reopening the original paper for the first adaptation attempt.
- A cooked entry must still let a future agent reopen source material when details matter.
- The final `proof-usage` index must support search by task shape, assumptions, tags, desired proof move, and material ID.
- Public files must not contain private paths, account names, raw transcripts, or unpublished project details.
