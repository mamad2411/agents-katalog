---
name: translating-spanish
description: Use when refining Spanish translations for Spain, Latin America, or a named region, including regional vocabulary, pronouns, formality, and product register.
---

# Translating Spanish

## Overview

Revise an approved `translating-core` draft into natural Spanish for the configured locale, market, audience, surface, and register. Preserve meaning, glossary decisions, placeholders, resource syntax, and protected values exactly.

This specialist covers common product patterns for Spain, Latin America, and named markets, not every Spanish variety. `es-419` is a regional tag, not one uniform country dialect; do not claim exhaustive coverage.

## Capabilities

- `language:spanish`
- `locale:es-ES`
- `locale:es-419`

## Entry Contract

Require `es-ES`, `es-419`, or another explicit regional locale or market whenever vocabulary, pronouns, formality, or product convention could change the result. “Spanish” or `es` alone is insufficient. For `es-419`, require a named market when the requested wording or channel is market-sensitive; otherwise apply the project's documented Latin American register without pretending it represents every country.

If the required locale or market is missing, ask exactly one focused question through `translating-products`, withhold only the affected target copy, and return. Continue independent work whose locale is already configured. Do not accept urgency as permission to choose a default.

Neutral copy is allowed only when `.translation/locales.yaml` explicitly sets `neutral_variants_allowed: true`. Missing or false is not permission. Record its intended markets and avoid flattening meaningful regional differences merely to sound “universal.”

Consume the core draft, target locale, audience, product surface, glossary, style guide, protected terms, placeholder contract, and length constraints. Do not generate before project setup and approval. Never install or download another skill at runtime.

## Refine the Draft

1. Confirm the exact locale/market and the approved formality and address strategy.
2. Preserve facts, intent, glossary choices, product names, placeholders, links, markup, code, keys, and numbers.
3. Apply pronouns and forms of address consistently: `tú`, `usted`, `vos`, `vosotros`, `ustedes`, impersonal forms, and omitted subjects are market- and relationship-dependent.
4. Select regional vocabulary from product context. Treat terms such as computer, mobile phone, file, save, sign in, and checkout as locale-sensitive rather than interchangeable synonyms.
5. Rebuild sentences in natural Spanish information order. Prefer idiomatic verbal phrasing and omit source-driven pronouns or possessives when Spanish does not need them.
6. Maintain approved formality, terminology, punctuation, and product register across related screens and documents.

Use project context, glossary, and pinned knowledge first. Research only a concrete unresolved current market term or regional usage question; record the source and decision through the orchestrator. Do not browse for ordinary grammar or routine strings.

## Product UI

Use concise, idiomatic commands and states familiar in the target market. Resolve noun/verb ambiguity from screen context, keep adjacent actions parallel, and avoid importing long explanatory syntax into labels. Test expansion, truncation, accessibility speech, and agreement around placeholders with representative runtime values.

## Long-Form Content

Maintain the approved reader relationship and regional register across headings, explanations, instructions, and calls to action. Prefer cohesive Spanish prose over sentence-by-sentence English order. Avoid unnecessary subject pronouns, literal gerunds, stacked nouns, and repeated possessives. Allow long-form copy to express transitions and relationships that compact UI omits.

## Common Literal-Translation Failures

- silently selecting Spain, a single Latin American country, or invented “neutral Spanish” for an unresolved target
- treating `es-419` as one country dialect or claiming one wording is natural everywhere in Latin America
- mixing `tú`, `usted`, `vos`, `vosotros`, `ustedes`, or their verb forms
- carrying English pronouns, possessives, gerunds, noun stacks, or word order into unnatural Spanish
- switching regional vocabulary, formality, or product register between related strings
- using explanatory prose as a UI label or expanding terse fragments without context
- changing approved terminology, placeholders, names, URLs, code, or markup for fluency

## QA Handoff

Pass the source, core draft, revision, exact locale/market, formality, address strategy, surface, glossary, protected values, and constraints to `reviewing-translations`. Verify:

- meaning, facts, names, numbers, links, placeholders, and structure remain complete
- pronouns, address, verb forms, vocabulary, formality, and regionalisms are consistent with the configured market
- any `es-419` wording stays within documented project scope without unsupported country-wide claims
- UI copy is concise and unambiguous; long-form prose has natural regional flow
- placeholders remain exact and surrounding gender, number, and agreement work for representative values
- no unintended source-language fragments or cross-regional mixture remain

Block only the affected segment on a missing locale/market, unapproved neutralization, regional or address mixture, glossary drift, literal phrasing, broken agreement, or protected-value corruption. Return the smallest failing segment to the responsible specialist.
