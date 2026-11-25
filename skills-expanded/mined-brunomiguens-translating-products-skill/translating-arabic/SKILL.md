---
name: translating-arabic
description: Use when refining Arabic translations for the requested locale and register, including Arabic wording, agreement, terminology, punctuation, and product naturalness.
---

# Translating Arabic

## Overview

Revise an approved `translating-core` draft into natural, culturally appropriate Arabic for the configured locale, market, audience, and register. Preserve meaning, approved glossary decisions, placeholders, markup, and protected values.

This specialist covers useful Arabic product patterns, not every dialect or market. Do not claim exhaustive dialect coverage or native-speaker review.

## Capabilities

- `language:arabic`
- `locale:ar`

## Entry Contract

Require an explicit target locale or market and an approved register choice: Modern Standard Arabic (MSA), a named regional variety, or a documented blend appropriate to the product. “Arabic” alone is insufficient.

Resolve setup one missing decision at a time without re-asking known values:

1. If the market or locale is missing, ask only for the target market or locale through the orchestrator, withhold affected target copy, and return.
2. Once the market is known, if the register is missing, ask only whether to use MSA, a named regional variety, or a documented blend, withhold affected target copy, and return.
3. If the register is already known but the market is missing, ask only for the market. Do not ask for the known register again.

Do not combine both decisions into one question. Urgency is not permission to choose a default silently. Begin revision only when both required decisions are complete.

Consume the core draft, source context, audience, surface, glossary, protected terms, placeholder contract, and length constraints. Do not translate before project setup and approval. Never install another skill at runtime.

## Refine the Draft

1. Confirm the target locale, market, register, and whether the content is product UI or long form.
2. Preserve facts, intent, glossary choices, product names, links, markup, resource syntax, and placeholder names exactly.
3. Resolve grammar around the full sentence: gender, person, definiteness, adjective and verb agreement, number agreement, dual forms, and Arabic plural behavior.
4. Prefer natural Arabic information flow over source-language word order. Keep terminology stable across related screens and documents.
5. Apply locale-appropriate punctuation and spacing without changing executable syntax. Route embedded LTR runs, mirroring, and layout mechanics to `translating-rtl`.
6. Return the revision with the locale/register decision and language-specific QA evidence.

Use project context, glossary, and pinned knowledge first. Research only a concrete unresolved current market term or regional usage that affects this artifact; record the source and decision through the orchestrator, then resume. Do not browse for routine grammar or every string.

## Product UI

Write concise Arabic that states the action or state clearly rather than mirroring terse English fragments. Use complete context for ambiguous commands, distinguish noun from verb senses, and avoid unnecessary pronouns or formal padding. Keep related labels parallel and ensure compactness does not break agreement or meaning.

For counts, define what is counted and preserve the platform's plural-message structure. Arabic may require zero, singular, dual, and multiple plural forms; do not assume every surface exposes the same categories or that an English singular/other split is sufficient. Keep placeholders reorderable and grammatically integrated without renaming them.

## Long-Form Content

Maintain a consistent MSA or approved regional register across headings, explanations, examples, and calls to action. Prefer connected Arabic discourse over sentence-by-sentence calques. Check reference chains, transitions, pronoun gender, terminology, and rhetorical tone across paragraphs. Preserve code, URLs, commands, and quoted protected values.

## Common Literal-Translation Failures

- shipping generic MSA as a “temporary” default when the market or register is unresolved
- copying English noun stacks, passive constructions, pronouns, or word order into unnatural Arabic
- treating all plurals as singular versus plural and omitting dual or required agreement
- mixing MSA and regional wording without an approved register strategy
- changing glossary terminology for stylistic variety
- translating placeholders, product names, IDs, URLs, code, or markup
- solving bidirectional layout by changing Arabic wording or inserting controls without evidence
- using identical terse wording for UI actions and explanatory prose despite different functions

## QA Handoff

Pass the source, core draft, revision, locale/market, register decision, glossary, protected values, and surface constraints to `reviewing-translations`. Verify:

- meaning, facts, names, numbers, links, placeholders, and structure remain complete and unchanged
- gender, number, dual, plural, person, definiteness, and agreement work for representative runtime values
- approved terminology and register remain consistent; no unexplained MSA/regional mixture appears
- punctuation, spacing, and sentence flow are natural for the configured locale
- compact UI copy remains clear in context, while long-form copy reads coherently across paragraphs
- no accidental source-language fragments remain outside approved protected values
- RTL mechanics, embedded LTR values, focus order, and device behavior are separately validated by `translating-rtl` and the surface specialist

Block the affected segment on missing locale/register, broken agreement, wrong plural or dual behavior, glossary drift, literal or unnatural phrasing, structural corruption, or unapproved register mixing. Route only the failing segment back to the responsible specialist.
