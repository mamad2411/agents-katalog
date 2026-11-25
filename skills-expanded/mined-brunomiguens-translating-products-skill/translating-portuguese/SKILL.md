---
name: translating-portuguese
description: Use when refining Portuguese translations for Brazil or Portugal, including regional grammar, vocabulary, spelling, formality, and product register.
---

# Translating Portuguese

## Overview

Revise an approved `translating-core` draft into natural Portuguese for the configured locale, audience, surface, and register. Preserve meaning, glossary decisions, placeholders, resource syntax, and protected values exactly.

This specialist covers practical product patterns for Brazil and Portugal, not every Portuguese-speaking market or regional variety. Do not claim exhaustive regional coverage.

## Capabilities

- `language:portuguese`
- `locale:pt-BR`
- `locale:pt-PT`

## Entry Contract

Require an explicit target locale or market whenever regional grammar, vocabulary, spelling, formality, or product register could change the result. “Portuguese” or `pt` alone is insufficient.

If the locale is missing, ask exactly one focused question through `translating-products`, withhold only the affected target copy, and return. Continue independent work whose locale is already configured. Urgency is not permission to choose a default.

Neutral Portuguese is allowed only when `.translation/locales.yaml` explicitly sets `neutral_variants_allowed: true`. Missing or false is not permission. Even then, record the intended markets and avoid presenting neutral copy as a native regional variety.

Consume the core draft, target locale, audience, product surface, glossary, style guide, protected terms, placeholder contract, and length constraints. Do not generate before project setup and approval. Never install or download another skill at runtime.

## Refine the Draft

1. Confirm `pt-BR`, `pt-PT`, another named locale, or explicitly permitted neutral scope.
2. Preserve facts, intent, glossary choices, product names, placeholders, links, markup, code, keys, and numbers.
3. Apply the configured pronouns and form of address consistently; do not switch between `você`, `tu`, impersonal forms, or Portugal-specific address strategies without project approval.
4. Choose region-correct vocabulary and spelling. Treat common product terms such as save, file, screen, mobile phone, login, and checkout as context-sensitive, not interchangeable pan-Portuguese synonyms.
5. Rebuild progressive constructions naturally: Brazilian usage may favor `estar + gerúndio`, while European usage often favors `estar a + infinitivo`; follow the locale and product register rather than mechanically replacing morphology.
6. Keep terminology consistent while allowing required agreement, contractions, clitics, and sentence reordering around protected values.

Use project context, glossary, and pinned knowledge first. Research only a concrete unresolved current market term or usage question; record the source and decision through the orchestrator. Do not browse for ordinary grammar or routine copy.

## Product UI

Prefer compact, idiomatic action labels and status text used in the target market. Distinguish nouns from commands and choose verb forms that match adjacent controls. Do not force identical wording between pt-BR and pt-PT when product convention differs. Test text expansion, truncation, accessibility speech, and placeholder agreement with representative runtime values.

## Long-Form Content

Use natural sentence flow and cohesive reference chains for the configured locale. Maintain the approved degree of formality and reader address across instructions, help content, and marketing prose. Avoid source-language noun stacks, repeated explicit subjects, and literal progressive or modal constructions. Allow longer prose to explain relationships that a concise UI label leaves implicit.

## Common Literal-Translation Failures

- shipping ambiguous `pt` copy by silently mixing Brazilian and European vocabulary
- creating artificial pan-Portuguese wording when neutral variants are not explicitly allowed
- translating English progressives into the wrong regional construction
- carrying English pronouns, possessives, noun stacks, or word order into unnatural Portuguese
- switching address, formality, vocabulary, spelling, or product register between related strings
- using a long-form sentence as a button label or expanding terse UI fragments into unnatural prose
- changing glossary terms, placeholders, product names, URLs, code, or markup for fluency

## QA Handoff

Pass the source, core draft, revision, exact locale, register, surface, glossary, protected values, and constraints to `reviewing-translations`. Verify:

- meaning, facts, names, numbers, links, placeholders, and structure remain complete
- pt-BR or pt-PT grammar, pronouns, address, vocabulary, spelling, and progressive forms are internally consistent
- product register and terminology match the configured market without unsupported pan-Portuguese claims
- UI copy is concise and unambiguous; long-form prose has natural regional flow
- placeholders remain exact and surrounding agreement works for representative values
- no unintended source-language fragments or cross-regional mixture remain

Block only the affected segment on a missing locale, unapproved neutralization, regional mixture, glossary drift, literal phrasing, broken agreement, or protected-value corruption. Return the smallest failing segment to the responsible specialist.
