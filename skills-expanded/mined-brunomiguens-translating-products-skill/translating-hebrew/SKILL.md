---
name: translating-hebrew
description: Use when refining Hebrew translations for the requested locale and register, including Hebrew wording, gender, number, construct forms, punctuation, and transliteration.
---

# Translating Hebrew

## Overview

Revise an approved `translating-core` draft into natural contemporary Hebrew for the configured locale, audience, and register. Preserve meaning, glossary decisions, placeholders, resource syntax, and protected values exactly.

This specialist provides focused product guidance, not exhaustive coverage of every community or register. Do not claim native-speaker review.

## Capabilities

- `language:hebrew`
- `locale:he`

## Entry Contract

Require an explicit target locale or variant, audience, and register. “Hebrew” alone is insufficient. If the locale or register is missing, return one focused question through the orchestrator and withhold target copy.

Consume the core draft, source context, surface, glossary, protected terms, placeholder types/examples, and the project's gender-inclusive language convention. Classify each string or segment before applying that convention:

- affected: reader address, actor gender, or another grammatical realization genuinely depends on the inclusive-language strategy
- unaffected: the segment remains grammatical and natural without choosing a gendered form or orthographic inclusion style

A goal such as “address readers inclusively” is not yet a convention: the context must name the accepted grammatical or orthographic strategy, such as neutral restructuring, doubled forms, separators, or a declared combination. If the strategy is absent and affected segments exist, continue translating unaffected segments, withhold only affected segments, and ask one focused strategy question through the orchestrator. Do not block neutral labels, messages, or protected values, and do not ask about an inclusion strategy when no segment depends on it.

Do not create target copy before project setup and approval. Never install or download another skill at runtime.

## Refine the Draft

1. Preserve facts, intent, approved terminology, placeholders, markup, URLs, product terms, and identifiers.
2. Choose direct contemporary Hebrew rather than source-language word order. Resolve the subject, action, and information focus in context.
3. Check grammatical gender and number across nouns, adjectives, verbs, pronouns, numerals, and placeholder-dependent words. Provide resource variants when runtime values change required agreement.
4. Use construct forms only where the relationship is idiomatic and unambiguous. Do not mechanically stack source noun phrases or attach definiteness twice.
5. Apply the configured inclusive-address convention consistently to affected segments without making compact UI unreadable or long-form prose repetitive. Leave unaffected segments independent of that choice.
6. Keep transliteration, translation, or an unchanged product term consistent with the approved glossary. Do not transliterate protected Latin names merely to make the line visually Hebrew.
7. Use contemporary punctuation and spacing for the locale. Route embedded LTR isolation, mirroring, and layout to `translating-rtl`.

Use project context and pinned knowledge first. Research only a specific unresolved current Israeli market term or usage question; record the source and decision through the orchestrator. Do not browse for routine Hebrew grammar or every string.

## Product UI

Prioritize a clear action or state. Once the inclusive convention is approved, choose an ordinary contemporary clause that preserves the actor and action. Use contextual infinitives, nouns, passive constructions, or sentence restructuring only when they remain natural in that exact UI context; do not replace a clear action with an awkward nominalization or erase who acted merely to avoid gender. Keep buttons short and parallel without treating English fragments as a template.

Counts require representative values. Do not place every `{count}` beside one fixed noun and plural verb: verify one, two, and other relevant values and the platform's message variants. Check prefixed prepositions and articles around placeholders without altering placeholder names or raw values.

## Long-Form Content

Use a consistent contemporary register across paragraphs. Restructure direct second-person address according to the approved inclusive convention, then check that references remain clear and prose does not become a sequence of heavy doubled forms. Maintain coherent transitions, construct relationships, terminology, and pronoun reference. Preserve code, links, examples, and protected Latin terms.

## Common Literal-Translation Failures

- copying English noun stacks instead of choosing an idiomatic construct or prepositional phrase
- losing the actor or changing active meaning solely to avoid gender
- applying one plural noun and verb to every numeric value
- mixing masculine-generic, feminine/masculine pairs, slashes, and neutral restructuring without an approved convention
- repeating paired gender forms until long-form prose becomes unnatural
- blocking neutral strings merely because a separate segment needs an inclusive-language decision
- adding or omitting the definite article incorrectly in a construct chain
- transliterating protected names or varying approved product terminology
- copying English punctuation, capitalization, or word order mechanically
- changing wording to solve bidirectional rendering instead of routing mechanics to `translating-rtl`

## QA Handoff

Pass source, core draft, revision, target locale, register and inclusive-language decisions, glossary, protected values, and surface constraints to `reviewing-translations`. Verify:

- meaning, agency, facts, names, numbers, links, placeholders, and structure remain complete
- gender and number agreement works for representative users, actors, and count values
- construct forms, articles, prepositions, and pronoun references are idiomatic and unambiguous
- the approved inclusive convention and contemporary register remain consistent across UI and long form
- glossary and transliteration choices do not drift; protected Latin terms remain exact
- UI labels are concise in context and long-form prose remains natural rather than mechanically doubled
- Hebrew punctuation and spacing are appropriate, with RTL mechanics validated separately by `translating-rtl`

Block the affected segment on missing locale/register, unresolved inclusive-language policy, broken agreement, semantic loss through neutralization, construct errors, glossary drift, literal phrasing, or protected-value corruption. Return only the smallest failing segment to the responsible specialist.
