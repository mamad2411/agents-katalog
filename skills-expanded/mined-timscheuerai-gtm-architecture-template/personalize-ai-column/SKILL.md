---
name: personalize-ai-column
description: Configure and preview the kit's generated first-touch callable using cited row evidence, a frozen experiment and an explicit credit ceiling.
---

# Generate grounded copy per row

Read [the runtime contract](../../../docs/runtime-contract.md), [composition](../../../docs/composition.md), `functions/generate_first_touch/function.json` and its prompt.

Use the installed `generate_first_touch` callable as the default implementation. Map company_evidence, person_evidence, scoring_reasons, offer and the assigned copy/test metadata from the actual working table. A prompt filename does not automatically load external sources; evidence must be in the mapped inputs.

Use `npm run example -- --function generate_first_touch` only for synthetic fixture rows. Use `npm run preview -- --function generate_first_touch` to inspect rendering and estimated cost. For a real caller table, follow the exact binding example and preview that table's chosen row.

Check missing facts, unresolved merge tags, invented observations, stale titles and whether the output respects the assigned variant. Thin evidence should create an explicit hold or a clearly qualified draft; do not invent a personal detail.

A dry run renders and estimates; it does not demonstrate model output quality. Run a live sample only within the user's authorized row set and credit cap. Report actual run status and cost separately from estimates. Review the sample before scaling, then hand off to `prepare_sequence`. No fixed provider price or BYOK saving is assumed.
