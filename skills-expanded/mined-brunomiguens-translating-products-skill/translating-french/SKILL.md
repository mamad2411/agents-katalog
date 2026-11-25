---
name: translating-french
description: Use when refining French translations for France or Canada, including regional vocabulary, formality, typography, spacing, anglicisms, and product register.
---

# Translating French

## Overview

Revise an approved `translating-core` draft into natural French for the configured locale, market, audience, surface, and register. Preserve meaning, glossary decisions, placeholders, resource syntax, and protected values exactly.

This specialist covers common product patterns for France and Canada, not every Francophone market or regional variety. Do not claim exhaustive regional coverage.

## Capabilities

- `language:french`
- `locale:fr-FR`
- `locale:fr-CA`

## Entry Contract

Require `fr-FR`, `fr-CA`, or another explicit locale or market whenever vocabulary, formality, terminology, typography, or product convention could change the result. “French” or `fr` alone is insufficient.

If the locale is missing, ask exactly one focused question through `translating-products`, withhold only the affected target copy, and return. Continue independent work whose locale is already configured. Urgency is not permission to choose France as a default.

Neutral copy is allowed only when `.translation/locales.yaml` explicitly sets `neutral_variants_allowed: true`. Missing or false is not permission. Record its intended markets and do not present neutralized copy as native to every Francophone audience.

Consume the core draft, target locale, audience, product surface and platform, glossary, style guide, protected terms, placeholder contract, and length constraints. Do not generate before project setup and approval. Never install or download another skill at runtime.

## Refine the Draft

1. Confirm the exact locale/market, `tu`/`vous` or other address strategy, formality, and product register.
2. Preserve facts, intent, glossary choices, product names, placeholders, links, markup, code, keys, and numbers.
3. Select region-correct vocabulary and terminology. Evaluate anglicisms by approved product usage and target-market familiarity; neither retain nor replace them mechanically.
4. Rebuild English noun stacks, verbal patterns, and modifier order into idiomatic French. Maintain natural articles, prepositions, agreement, and reference chains around placeholders.
5. Apply punctuation, quotation marks, capitalization, and spacing for the configured locale and medium. Follow platform rendering rules for nonbreaking spaces and narrow spaces; do not blindly impose print typography on constrained UI, plain-text fields, code-like resources, or systems that normalize whitespace.
6. Keep approved terminology, formality, and address consistent across related content.

Use project context, glossary, and pinned knowledge first. Research only a concrete unresolved current market term, anglicism, or usage question; record the source and decision through the orchestrator. Do not browse for ordinary grammar or routine punctuation.

## Product UI

Use compact, idiomatic labels and states familiar in the target market. Resolve noun/verb ambiguity from the screen context and keep adjacent actions parallel. Prefer established product wording over a literal English cognate. Validate expansion, truncation, whitespace rendering, accessibility speech, and agreement around placeholders on the actual surface.

## Long-Form Content

Maintain the approved address and register across headings, explanations, instructions, and calls to action. Prefer cohesive French prose over English sentence order, excessive noun strings, or repeated possessives. Apply locale-appropriate typography when the output medium supports it; preserve protected syntax and let explanatory prose breathe beyond UI constraints.

## Common Literal-Translation Failures

- silently selecting fr-FR for an unresolved French target or inventing universal French
- mixing fr-FR and fr-CA vocabulary, address, terminology, spelling conventions, or product register
- switching between `tu` and `vous` or their agreement across related content
- retaining an unfamiliar anglicism because the source uses English, or replacing an established product term mechanically
- copying English noun stacks, cognates, possessives, or word order into awkward French
- imposing print punctuation spacing on a constrained platform without checking rendering behavior
- using a long explanatory phrase as a compact UI label
- changing glossary terms, placeholders, names, URLs, code, markup, or meaningful whitespace

## QA Handoff

Pass the source, core draft, revision, exact locale/market, address/formality choice, surface/platform, glossary, protected values, and constraints to `reviewing-translations`. Verify:

- meaning, facts, names, numbers, links, placeholders, and structure remain complete
- regional vocabulary, formality, address, terminology, anglicisms, and product register are consistent
- punctuation, quotation marks, typography, and spacing fit both locale and actual platform behavior
- UI copy is concise and unambiguous; long-form prose has natural French flow
- placeholders remain exact and surrounding gender, number, elision, and agreement work for representative values
- no unintended English fragments, false cognates, or cross-regional mixture remain

Block only the affected segment on a missing locale, unapproved neutralization, regional/address mixture, unsuitable anglicism, typography corruption, literal phrasing, broken agreement, glossary drift, or protected-value corruption. Return the smallest failing segment to the responsible specialist.
