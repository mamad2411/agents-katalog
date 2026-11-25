---
name: translating-german
description: Use when refining German translations for Germany, Austria, or Switzerland, including formality, terminology, compounds, capitalization, expansion, and UI constraints.
---

# Translating German

## Overview

Revise an approved `translating-core` draft into natural German for the configured locale, market, audience, surface, and register. Preserve meaning, glossary decisions, placeholders, resource syntax, and protected values exactly.

This specialist covers common product patterns for Germany, Austria, and Switzerland, not every German-speaking market or regional variety. Do not claim exhaustive regional coverage.

## Capabilities

- `language:german`
- `locale:de-DE`
- `locale:de-AT`
- `locale:de-CH`

## Entry Contract

Require `de-DE`, `de-AT`, `de-CH`, or another explicit locale or market whenever vocabulary, spelling, address, terminology, or product convention could change the result. “German” or `de` alone is insufficient.

If the locale is missing, ask exactly one focused question through `translating-products`, withhold only the affected target copy, and return. Continue independent work whose locale is already configured. Urgency is not permission to choose Germany as a default.

Neutral copy is allowed only when `.translation/locales.yaml` explicitly sets `neutral_variants_allowed: true`. Missing or false is not permission. Record its intended markets and do not erase meaningful regional conventions to create artificial universal German.

Consume the core draft, target locale, audience, product surface, glossary, style guide, protected terms, placeholder contract, and UI constraints. Do not generate before project setup and approval. Never install or download another skill at runtime.

## Refine the Draft

1. Confirm the exact locale/market, `du`/`Sie` or other address strategy, formality, and product register.
2. Preserve facts, intent, glossary choices, product names, placeholders, links, markup, code, keys, and numbers.
3. Apply region-correct vocabulary and spelling. Follow configured de-CH conventions such as `ss` instead of `ß`; validate Austrian and Swiss product terms against project usage rather than assuming de-DE wording transfers unchanged.
4. Form compounds only when they are idiomatic, readable, and consistent with the glossary. Use hyphens or verbal rephrasing where approved terminology, acronyms, or long noun stacks would become unclear.
5. Preserve required German noun capitalization and address capitalization. Do not capitalize from source layout alone or lowercase protected values.
6. Prefer direct verbal phrasing over source-driven nominalizations, passive chains, and stacked compounds when the product register permits it.
7. Check expansion against the actual UI. Do not silently abbreviate, omit meaning, alter a protected term, or create an unnatural compound merely to fit; report the affected constraint and offer the shortest meaning-faithful wording.

Use project context, glossary, and pinned knowledge first. Research only a concrete unresolved current market term or regional usage question; record the source and decision through the orchestrator. Do not browse for routine grammar, compounds, or capitalization.

## Product UI

Use concise, idiomatic action labels and states. Resolve infinitive, imperative, noun-label, and sentence patterns from adjacent controls and platform conventions. Keep related actions parallel. Test text expansion, wrapping, truncation, accessibility speech, and compounds on representative devices; flag a limit that cannot preserve meaning naturally.

## Long-Form Content

Maintain the approved address and register across headings, explanations, instructions, and calls to action. Prefer clear clauses and natural information order over dense noun compounds, abstract nominal style, or literal English modifier order. Use pronouns and connective words coherently without repeating formal address mechanically.

## Common Literal-Translation Failures

- silently selecting de-DE for an unresolved German target or inventing universal German
- mixing de-DE, de-AT, and de-CH vocabulary or spelling, especially `ß` in de-CH copy
- switching between `du` and `Sie` or their capitalization and verb forms
- copying English noun stacks into unreadable compounds or overusing nominalizations and passive constructions
- splitting an established compound incorrectly or joining terms despite ambiguity
- losing German noun capitalization or changing protected capitalization
- shortening UI copy by deleting meaning, inventing abbreviations, or changing glossary terms
- applying one terse UI phrase to long-form prose despite different register and information needs
- changing placeholders, names, URLs, code, markup, or numbers for fluency

## QA Handoff

Pass the source, core draft, revision, exact locale/market, address/formality choice, surface, glossary, protected values, and UI constraints to `reviewing-translations`. Verify:

- meaning, facts, names, numbers, links, placeholders, and structure remain complete
- de-DE, de-AT, or de-CH vocabulary, spelling, address, and terminology are internally consistent
- compounds are correct and readable; capitalization and agreement work around representative placeholder values
- UI copy preserves meaning within validated expansion constraints, or the constraint is explicitly flagged
- long-form prose uses natural verbal phrasing rather than source-driven noun stacks
- no unintended English fragments or cross-regional mixture remain

Block only the affected segment on a missing locale, unapproved neutralization, regional/address mixture, glossary drift, unreadable compounds, capitalization errors, semantic loss from UI shortening, literal phrasing, broken agreement, or protected-value corruption. Return the smallest failing segment to the responsible specialist.
