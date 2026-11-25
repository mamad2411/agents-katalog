---
name: translating-web
description: Use when localizing websites while preserving markup, metadata, accessibility, links, and locale signals for HTML, Markdown, or web-content translation.
---

# Translating Web

## Overview

Define the web surface contract around a translation. Preserve executable structure and verified destinations while exposing only human-readable content for translation.

## Capabilities

- `surface:web`
- `html`
- `markdown`
- `accessibility`
- `hreflang`

## Input Inspection

Inspect the complete artifact before requesting translation:

- identify HTML, Markdown, templates, embedded data, and generated regions
- record source and target locales, page purpose, route, canonical URL, and alternate pages
- enumerate visible copy, metadata, structured-data strings, accessibility text, and media captions
- identify approved localized routes, assets, SEO terms, length limits, and protected spans
- note mixed-language content and whether each retained source-language span is deliberate

Return an unresolved field to its owner when its role is ambiguous; do not guess whether syntax or data is prose.

## Translation Surface

Send human-readable content to `translating-core`: headings, paragraphs, navigation labels, calls to action, title and description metadata, meaningful alt text, captions, accessible names, and user-facing strings inside structured data.

Provide the artifact context and field purpose with each segment. Keep tags and field boundaries around the returned text; this skill does not generate target-language wording or decide language mechanics.

## Non-Translatable Elements

Preserve byte-for-byte unless an approved configuration supplies a replacement:

- HTML and Markdown syntax, tag names, attribute names, frontmatter keys, template delimiters, and comments marked as protected
- URLs, paths, fragments, query parameters, canonical targets, asset locations, IDs, analytics values, CSS classes, and `data-*` values
- code, commands, variables, identifiers, schema keys, product codes, and protected brand terms
- `hreflang` and language-tag syntax; change values only to approved normalized locale tags

Translate link labels, not destinations. A localized URL is configuration supplied by routing or SEO ownership, never a translation inferred from its words.

## Web Constraints

- Preserve valid nesting, escaping, whitespace-sensitive regions, link/image counts, heading order, and Markdown reference relationships.
- Keep each locale page internally coherent: visible copy, metadata, accessibility text, and user-facing structured data belong to the same target locale.
- Pair an approved localized canonical with the page it identifies. Treat `hreflang` alternates as a reciprocal set whose destinations must exist; do not manufacture missing alternates or `x-default`.
- Preserve the meaning and qualification of claims. Route a request to strengthen, omit, or invent a promise back to the explicit user or approved content owner.
- Mark untranslated customer-facing text as deliberate or as a mixed-language defect. For indexable localized pages, unresolved fallback-language copy blocks release.
- Keep accessibility purpose intact: translate accessible names and meaningful alt text through core, preserve decorative empty alt text, and avoid duplicating visible labels without evidence.

## Targeted Research

Research only facts that may have changed and materially affect this artifact: current search-platform locale-tag rules, platform metadata behavior, or current market keyword usage. Prefer authoritative platform documentation and dated market evidence. Do not research ordinary wording, grammar, or stable HTML/Markdown syntax, and do not convert unverified research into a route or product claim.

## Authority and Conflict Boundary

Follow explicit user requirements, approved project configuration, and core semantic fidelity before web formatting preferences. Product, legal, routing, analytics, SEO, and accessibility owners remain authoritative for their configured values.

This skill owns web field classification, protected structures, surface constraints, and web QA checks. `translating-core` owns meaning and target copy; installed language or script specialists own locale mechanics; `reviewing-translations` owns the final review. If a web constraint conflicts with an approved term or meaning, name the affected field and conflict instead of rewriting either side.

## QA Handoff

Pass the source artifact, translated artifact, locale pair, approved route map, protected-span inventory, and these checks to `reviewing-translations`:

- syntax parses and tags, attributes, templates, code, IDs, URLs, and relationships retain parity
- visible copy, metadata, accessibility text, and structured-data strings contain no accidental mixed-language content
- canonical and `hreflang` values match approved configuration, resolve as intended, and are reciprocal where required
- accessible names, alt semantics, heading structure, and keyboard/link purpose remain equivalent
- claims, numbers, placeholders, protected terms, and link destinations preserve source intent
- rendered pages do not introduce truncation, overflow, broken markup, or locale-routing regressions

Block release for corrupted protected structure, an invented or broken destination, a materially altered claim, accidental mixed-language indexable content, or a failed accessibility purpose. Route each defect with the smallest unchanged affected segment to the responsible installed skill.
