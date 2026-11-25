---
name: ai-concept-generation
description: Use when preparing landscape AI concept prompts, generating multiple visual directions from a measured base plan, logging generation batches, selecting variants, and protecting geometry from AI drift.
---

# AI Concept Generation

## Goal

Generate managed concepts from measured plan, brief, site analysis, and designer logic instead of random beautiful images.

## Before Generation

1. Check for AI-ready base in `02_base_plan/04_ai_ready_base`.
2. Check `03_client_context/BRIEF.md` and `03_client_context/SITE_ANALYSIS.md`.
3. Create 3-5 written concepts in `04_ai_concepts/01_concept_variants`.
4. Fill the structure from `04_ai_concepts/CONCEPT_BRIEF_TEMPLATE.md` for each concept.
5. Prepare common inputs in `04_ai_concepts/00_common_inputs`.

## Generation

1. Run a separate batch for each concept.
2. Use prompts from `90_prompt_library` as a base, but save the actual prompt.
3. Record each batch in `04_ai_concepts/GENERATION_LOG.md`: source files, exact prompt, service/model, settings, result files, selection reason, geometry risks.
4. Check: boundaries, house, entry, permanent structures, utilities, proportions.
5. Reject options where AI broke geometry even if they look attractive.

## Selection

In `04_ai_concepts/SHORTLIST.md`, record:

- what is shown to the client;
- which elements can be used in the project;
- which elements are mood-only;
- risks and caveats.

## Output

- 3-5 written concepts.
- Filled generation log.
- Shortlist of 5-7 client-facing options.
