---
name: translating-ios
description: Use when localizing Apple-platform resources and UI copy for String Catalogs, SwiftUI, UIKit, VoiceOver, and Apple locale behavior.
---

# Translating iOS

## Overview

Define the Apple-platform resource and runtime contract around localized copy. Preserve catalog identity, substitutions, and UI behavior while routing wording to core and installed language or script specialists.

Do not produce target copy until the orchestrator confirms project setup and approval. This skill owns Apple engineering semantics, not linguistic decisions.

## Capabilities

- `platform:ios`
- `xcstrings`
- `swiftui`
- `apple-locales`

## Inspect the Shipped Configuration

Inspect source, String Catalogs (`.xcstrings`), build settings, targets, and consuming UI together:

- record target and source locales, development language, catalog membership, fallback behavior, and every shipped app, extension, widget, or package target
- inventory stable resource keys, source/default values, comments, catalog state, extraction state, substitutions, variations, and protected values
- classify each call site: SwiftUI localization inferred through `LocalizedStringKey`, explicit localized resolution such as `String(localized:)`, UIKit lookup, accessibility API, or verbatim runtime `String`
- record screen, component, state, grammatical purpose, placeholder type, example, layout constraint, and accessibility intent

A string literal accepted as `LocalizedStringKey` can participate in localization and interpolation; a runtime `String` does not become localized merely because it is shown by SwiftUI. Confirm the actual initializer and catalog extraction rather than relying on visual similarity.

Do not delete a stale catalog entry automatically. Reconcile it with call sites, key migrations, and retained translations. Treat new, untranslated, stale, or review-needed state according to the project's explicit release policy, and block raw keys or unintended fallback values in shipped UI.

## Preserve Resource Identity

Follow the project's established key strategy. Keep semantic keys, table or catalog selection, bundle, placeholder types, protected identifiers, and source meaning stable. When migrating an English-as-key entry to a semantic key, map existing translations deliberately and verify the old entry is no longer live; do not create duplicate identities or discard approved work.

Send complete phrases and their comments to `translating-core`. Allow translators to reorder typed substitutions inside the complete phrase. Never assemble target sentences from localized fragments or translate resource keys, placeholder names, receipt IDs, URLs, or code.

## Interpolation and Locale Formatting

- Keep interpolation inside the localizable message so target grammar can reorder values.
- Use typed substitutions and Apple `FormatStyle` APIs for numbers, dates, currency, measurements, and lists under the explicit target locale and business-owned value/currency contract.
- Do not use string concatenation, `String(describing:)`, hard-coded currency symbols, manual separators, or preformatted source-locale values as localization.
- Use `String(localized:)` or the project's resource-oriented API when a resolved `String` is required outside a localization-aware SwiftUI initializer. Avoid resolving early when a view or API can retain localized resource context.
- Preserve opaque runtime identifiers exactly. Test their punctuation and bidirectional placement rather than translating or reformatting them.

## Pluralization and Variations

Model a count as one localizable message with a typed count substitution and String Catalog plural variation. Do not concatenate a count and noun, branch only on English singular/other, or require target categories to mirror the source.

Use the target locale categories supported by the shipped Apple runtime. Preserve required substitutions in every applicable variation and exercise representative boundary values, including zero and larger counts. Product context must say what is being counted.

Use device, platform, or other catalog variations only when product meaning or platform presentation truly differs. Variants must remain one coherent resource contract rather than unrelated translations hidden under the same key.

## Comments and Accessibility

Developer comments must explain the screen, component, state, action meaning, grammatical role, placeholder meaning/type, count semantics, protected spans, and meaningful length constraint. Split identical English source text into separate resources when its meaning or grammatical context differs.

Let visible labels provide default accessibility names when they are complete. Create a distinct localized VoiceOver label, hint, value, or announcement resource when spoken purpose differs. Keep visible, spoken, and executed values consistent; never build accessibility prose by runtime concatenation.

Test VoiceOver role, name, value, hint, announcement timing, pronunciation, reading order, focus movement, and updates after state changes. Do not claim human or native-speaker review that did not occur.

## Layout and RTL

Use leading/trailing semantics and adaptable SwiftUI or Auto Layout behavior. Test iPhone and iPad, compact and regular widths, rotation or multitasking where supported, safe areas, and all supported Dynamic Type sizes. Required actions, facts, and status must not clip, overlap, disappear, or truncate into ambiguity.

For RTL locales, test actual RTL layout, navigation and directional imagery, mixed Arabic/Hebrew with numbers, currency, punctuation, and opaque LTR identifiers. Route language mechanics and bidirectional decisions to installed specialists; do not insert direction marks by guesswork.

## Targeted Research

Use project configuration and pinned knowledge first. Research only a specific unresolved current Apple API or platform behavior that materially affects the artifact. Prefer Apple documentation, record the decision through the orchestrator, and do not browse for routine wording or grammar. Never download another skill at runtime.

## Authority Boundary

Explicit user requirements, approved project configuration, and semantic fidelity outrank platform convenience. Product owns meaning and state; engineering owns targets, resource APIs, value contracts, and fallback; accessibility ownership supplies interaction intent.

This skill owns Apple resource classification, catalog/extraction state, formatting and platform QA. `translating-core` owns target copy; language and script specialists own linguistic mechanics; `translating-mobile` owns shared mobile constraints; `reviewing-translations` owns final review.

## QA Handoff and Release Gates

Always perform file and structural checks, including:

- build and extract every shipped target; reconcile missing, duplicate, stale, untranslated, and review-needed entries under the approved policy
- preserve resource keys, tables/catalogs, substitutions, variation topology, protected identifiers, and source meaning
- compile catalogs and validate plural, number, date, currency, and identifier substitutions
- reject raw keys, runtime concatenation, hard-coded formatting, and accidental mixed-language target resources

Perform the following runtime checks only after the orchestrator supplies a resolved `run` decision. Use the smallest relevant runtime scope for the affected resources and states; do not independently choose the runtime-review budget or expand it to the whole application:

- execute localized strings with representative plural, number, date, currency, and identifier values
- verify no raw key, source-language fallback, hard-coded formatting, or accidental mixed-language output reaches visible or VoiceOver content
- test screenshots and interaction on required iPhone/iPad sizes, Dynamic Type ranges, VoiceOver, and RTL layouts
- confirm visible, spoken, formatted, and business-executed values remain consistent

Pass catalogs, source and target resources, target/build matrix, call-site inventory, available screenshots, accessibility intent, and applicable results to `reviewing-translations` and CI.

Always block release on catalog or extraction drift without disposition, resource-key or substitution corruption, incomplete target plural behavior, raw keys, or invalid locale formatting. When runtime review runs, also block on unintended fallback, misleading VoiceOver output, RTL ordering defects, or required content hidden by layout. Route the exact key, call site, state, and evidence to its responsible installed skill.
