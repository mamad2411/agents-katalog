---
name: translating-flutter
description: Use when localizing Flutter applications for ARB, generated localization, ICU messages, flutter_localizations, accessibility, and responsive layout checks.
---

# Translating Flutter

## Overview

Define the ARB, generated-localization, and Flutter UI contract around localized copy. Preserve message identity and executable ICU structure while routing target wording to core and installed language or script specialists.

Do not create target copy until the orchestrator confirms project setup and approval. This skill owns Flutter engineering semantics, not linguistic decisions.

## Capabilities

- `platform:flutter`
- `arb`
- `flutter-localizations`
- `icu`

## Inspect Project and ARB State

Inspect `l10n.yaml` or equivalent project localization configuration, the template and target ARB files, generated localization output, application wiring, and consuming widgets together:

- record template locale, exact target locales, ARB directory/files, generated output policy, fallback behavior, and every shipping app/package target
- inventory message key, source/default message, its companion ARB metadata entry, description, placeholders, ICU arguments and branches, protected values, and target coverage
- record screen, widget, state, grammatical purpose, length/layout constraint, accessibility role, and placeholder meaning/type/example
- find user-facing literals and runtime concatenation in widgets, routes, dialogs, notifications, tests, and `Semantics`
- identify the generated localization API and every file or directory owned by the generator

If project localization setup is absent or unresolved, return the missing configuration to the orchestrator. Never infer target wording or resource semantics from a generated getter name.

## ARB Message Contract

Treat source ARB and approved project configuration as the editable source of truth. Keep message keys, placeholder names/types, ICU selector semantics, protected identifiers, URLs, facts, and runtime values stable.

For every user-facing message, provide its companion ARB metadata entry with a contextual description. For every placeholder, provide metadata supported by the project's generator: semantic description, declared type, representative example, and required format or optional parameters when applicable. Comments must explain what a count measures, what a select argument represents, whether a value is opaque, and whether reordering is allowed.

Send complete messages and metadata to `translating-core`. Allow installed language specialists to reorder placeholders and choose grammar inside the preserved ICU topology. Never translate message keys or placeholder names, split a sentence into concatenated getters, or hardcode a source-locale formatted value.

Keep ARB valid JSON and ICU syntax valid for the pinned generator. Preserve required escaping and apostrophe behavior. Compile representative messages rather than trusting visual inspection of braces and commas.

## ICU Plurals and Selects

Use ICU `plural` for grammatical quantity messages and `select` for a closed, product-defined choice. Keep a valid `other` branch. The value selecting a plural is separate from any formatted value displayed in its branches; include the placeholder where the message needs it.

Provide the target-locale plural categories required by the project's generated localization runtime. Do not mirror English categories, concatenate count plus noun, or hand-code `count == 1`. Preserve placeholder schema in every applicable branch and test target-locale boundary values, including zero and larger counts.

Keep `select` keys aligned with stable runtime enum/value semantics. Do not translate selectors, invent target-only product states, or use grammatical gender as a proxy for a person's identity without an explicit product contract. Unknown values must follow the approved `other` behavior.

## Generated Localization Boundary

Edit ARB and localization configuration, then run the project's pinned generation workflow. Never edit generated Dart manually. Whether generated files are committed is a repository policy: if committed, regenerate and verify a clean deterministic diff; if ignored, generate in CI/build and verify availability there.

Use the generated typed localization API from the active context. Add the required `flutter_localizations` dependency and Flutter/App localization delegates according to project configuration, and derive or verify `supportedLocales` against the generated locale inventory. Do not maintain a contradictory hand-written locale list.

Fail generation or CI on invalid ICU, unresolved or mismatched placeholders, missing source metadata required by policy, target key drift, or generated-output drift.

## Formatting, Accessibility, and Layout

- Format numbers, dates, currency, units, and lists through locale-aware project/Flutter APIs with a business-owned currency or unit contract. A locale changes presentation, not the underlying value or charged currency.
- Keep formatted values inside one complete localized message. Do not concatenate a currency symbol, label, count, or accessibility phrase around generated getters.
- Resource `Semantics` labels, values, hints, live-region announcements, and other user-facing accessibility copy. Reuse visible text only when it fully communicates the same spoken purpose.
- Test screen-reader name, role, state, value, hint, announcement timing, traversal/focus order, and dynamic updates on each supported platform.
- Use directional layout primitives such as `EdgeInsetsDirectional` and `AlignmentDirectional` where locale direction owns placement. Test `Directionality`, navigation and selectively mirrored imagery, mixed-direction placeholders, punctuation, and formatted values under RTL.
- Test smallest and largest supported phones, tablets/foldables or desktop/web windows when shipped, portrait/landscape, text scaling, safe areas, keyboard states, and long plural/select branches. Required content must wrap or adapt without clipping, overlap, hidden controls, or ambiguous truncation.

## Fallback and Mixed Language

Do not copy source-language text into target ARB files merely to satisfy completeness checks. A deliberate protected/source-equal value must be allowlisted with context; otherwise source-equal customer copy remains detectable.

Exercise missing locale, missing message, partial locale, and unsupported locale behavior. Unintended fallback, raw keys/getter names, or accidental mixed-language customer output blocks release.

## Targeted Research

Use project configuration and pinned Flutter-derived knowledge first. Research only a specific unresolved current Flutter localization behavior that materially affects the artifact, using authoritative Flutter/Dart documentation and recording the decision through the orchestrator. Do not browse for routine wording or grammar, and never install another skill at runtime.

## Authority Boundary

Explicit user requirements, approved project configuration, and semantic fidelity outrank generator convenience. Product owns meaning and selector states; engineering owns ARB/generator, value, layout, and fallback contracts; accessibility ownership supplies interaction intent.

This skill owns Flutter resource classification, generation boundaries, ICU/runtime integration, layout, and platform QA. `translating-core` owns target copy; language and script specialists own linguistic mechanics; `translating-mobile` owns shared mobile constraints; `reviewing-translations` owns final review.

## QA Handoff and Release Gates

Always perform file and structural checks, including:

- validate JSON and compile generated localizations; compare keys, metadata, placeholders, ICU selectors/branches, protected values, and target coverage
- exercise every target plural category, select key, formatted value, missing/partial locale path, and fallback path
- verify delegate and supported-locale wiring in every shipped target and reject manual generated-code edits
- detect source-equal targets outside the allowlist, raw identifiers, invalid ICU, and accidental mixed-language target files

Perform the following runtime checks only after the orchestrator supplies a resolved `run` decision. Use the smallest relevant runtime scope for the affected resources and states; do not independently choose the runtime-review budget or expand it to the whole application:

- run long-text, text-scale, screen-reader, RTL/directional, target-locale, and responsive window/device tests
- detect unintended fallback, accidental mixed language, clipping, overlap, or inaccessible controls in rendered states

Pass template and target ARBs, localization configuration, generated-output policy/diff, key/placeholder/ICU inventory, locale/build/device matrix, available screenshots, accessibility intent, and applicable results to `reviewing-translations` and CI.

Always block release on invalid ARB/ICU or generation failure; key, metadata, placeholder, plural, or select corruption; generated-code drift or manual edits; missing delegate/locale wiring; or hardcoded or incorrectly formatted copy. When runtime review runs, also block on unintended fallback or mixed language, accessibility meaning loss, RTL defects, or required content hidden by layout. Route the exact key, consumer, locale, configuration, and evidence to its responsible installed skill.
