---
name: translating-polish
description: Use when refining Polish translations for Poland, including address strategy, register, aspect, case government, collocations, agreement, and natural product or financial wording.
---

# Translating Polish

## Overview

Revise an approved `translating-core` draft into natural Polish for the
configured audience, surface, domain, and register. Preserve meaning, product
roles, glossary decisions, placeholders, resource syntax, and protected values
exactly.

This specialist provides practical guidance for Polish product copy, including
financial and institutional contexts. It is not an exhaustive grammar or a
substitute for project-specific terminology.

## Capabilities

- `language:polish`
- `locale:pl-PL`

## Entry Contract

Require the target locale or market whenever regional convention or regulatory
terminology could affect the result. Use `pl-PL` for Poland. Do not invent a
locale-neutral Polish target unless the approved project configuration permits
neutral variants.

Consume the core draft, exact target locale, audience, product surface,
domain, glossary, style guide, protected terms, semantic groups, verified
target-corpus evidence, placeholder contract, and structural constraints.
Do not generate before project setup and approval. Never install or download
another skill at runtime.

## Refine the Draft

1. Confirm the address strategy separately from the other register dimensions:
   institutional or personal voice, courtesy, directness, and the conventions
   for the current surface. Formal copy does not automatically require frequent
   direct address or personal language.
2. Preserve facts, intent, participant roles, obligations, glossary choices,
   product names, placeholders, links, markup, code, keys, and numbers.
3. Choose aspect, tense, case government, and prepositions from the event and
   sentence relationship, not by mapping an isolated English word. Check
   agreement after every change, including gender, number, case, and forms
   surrounding placeholders.
4. Prefer established Polish product and domain collocations. Interpret the
   action or state first—what happened, who initiated it, what changed, and how
   the product presents it—then choose the Polish verb or noun phrase.
5. Recast unnatural English inanimate agency with a natural Polish active,
   passive, impersonal, reflexive, or nominal construction while preserving who
   did what. Do not make an account, screen, or object perform a human action
   merely because the English subject occupies that position.
6. Keep protected terms unchanged while inflecting surrounding Polish
   naturally. When a protected form makes required grammar impossible, report
   the affected segment instead of corrupting either the term or the sentence.
7. Refine related semantic groups together so repeated events, assessment
   items, and multi-field messages use one coherent concept. Allow subject,
   title, body, label, and answer choices to realize it differently when Polish
   grammar or surface convention requires it.
8. Replace source-language noun stacks, calques, unnecessary possessives, and
   unexplained loanwords with idiomatic Polish structures without adding or
   deleting meaning.

## Terminology Resolution

Use approved glossary entries and project decisions first, then translation
memory and structurally aligned, verified target-product copy. Treat corpus
evidence as evidence of product usage, not automatic authority: reject stale,
semantically different, or known-defective examples.

When an unapproved term recurs across a semantic group or materially affects
domain meaning, legal meaning, participant roles, or whether an answer is true,
return it to `translating-products` for a standalone terminology decision
before it is propagated. Research only one concrete unresolved current or
market-specific terminology question when the orchestrator's research gate
allows it. Do not browse for routine Polish grammar, style, or wording.

## Product UI

Use concise Polish actions, labels, and states that sound native in their
actual interface role. Determine whether the product convention calls for an
imperative, infinitive, noun label, participle, or sentence; do not copy the
English grammatical shape by default. Keep parallel actions parallel and test
agreement and truncation with representative placeholder values.

For transactional messages, distinguish the user's action, the system's state,
and the resulting account or asset state. Keep related subject, preview, title,
and body fields conceptually aligned without forcing them to be literal copies.

## Long-Form and Institutional Copy

Maintain the approved relationship to the reader across headings,
explanations, instructions, notices, and calls to action. Separate politeness
from familiarity: an institutional voice may be courteous and clear without
becoming personal, conversational, or repetitive in its direct address.

Prefer natural Polish clause structure and collocation over source-driven
nominal chains. Preserve legal and financial distinctions exactly, and do not
strengthen certainty, responsibility, or authorization for fluency.

## Common Literal-Translation Failures

- choosing a familiar or personal voice merely because the source uses `you`
- selecting a dictionary-equivalent verb without checking the event frame or
  domain collocation
- personifying an account, screen, balance, or process in a way Polish would
  normally express impersonally or through a different participant
- copying English noun stacks, possessives, participles, or prepositions
- mixing aspect, case government, or agreement after local rewrites
- applying one wording to every field even when Polish surface grammar differs
- propagating an unresolved critical term because the first literal draft is
  superficially understandable
- changing answer truth, product roles, protected values, placeholders, URLs,
  code, markup, or numbers for naturalness

## QA Handoff

Pass the source, core draft, Polish revision, exact locale, audience, register
dimensions, surface, semantic groups, glossary, protected values, relevant
target-corpus evidence, and structural constraints to
`reviewing-translations`. Verify:

- meaning, facts, participant roles, answer truth, names, numbers, links,
  placeholders, and structure remain complete
- address, institutional or personal voice, courtesy, and directness match the
  approved product context
- aspect, case government, prepositions, agreement, collocations, and
  information order are idiomatic Polish
- recurring concepts remain coherent across their semantic groups while each
  field fits its surface
- no source-language calques, unjustified loanwords, accidental mixed language,
  or mechanically copied agency remain
- unresolved critical terminology is blocked or recorded as draft rather than
  silently treated as approved

Block only the affected segment or semantic group on missing material context,
semantic drift, role or truth changes, terminology ambiguity, register drift,
literal phrasing, broken agreement, structural damage, or protected-value
corruption. Return the smallest failing unit to the responsible specialist and
recheck it against its related group.
