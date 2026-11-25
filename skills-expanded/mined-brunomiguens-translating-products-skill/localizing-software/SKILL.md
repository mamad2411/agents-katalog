---
name: localizing-software
description: Use when localizing software resources while preserving ICU syntax, placeholders, plurals, keys, and locale formatting for application resource files and UI strings.
---

# Localizing Software

## Overview

Define the executable contract around software strings. Expose message prose to translation while keeping resource identity, parameters, selection logic, and runtime formatting testable.

## Capabilities

- `surface:software`
- `icu`
- `placeholders`
- `plurals`
- `locale-formatting`

## Input Inspection

Inspect the complete source and its consumption sites when available:

- identify resource format, encoding, namespaces, key context, comments, and fallback chain
- inventory keys, placeholders, types, escapes, markup, ICU arguments, plural/select branches, and exact-number selectors
- record where each string renders, length or line limits, concatenated neighbors, and accessibility role
- identify source and target locales, runtime formatter and version, supported plural categories, and date/number/currency ownership
- flag user data, opaque identifiers, directional symbols, and mixed RTL/LTR content

Do not infer undocumented parser behavior. When the production runtime is unknown, preserve source topology and request its contract from engineering.

## Translation Surface

Send only user-facing prose from each message and every branch to `translating-core`, together with key context, placeholder meaning and type, UI location, and constraints. Reinsert returned text without changing syntax.

This skill does not author target strings, choose terminology, inflect values, or decide language-specific plural categories. Those decisions belong to core and installed language or script specialists.

## Non-Translatable Elements

Preserve exactly unless engineering supplies a changed resource contract:

- resource keys, namespaces, object structure, ordering when significant, encoding declarations, comments marked as protected, and escapes
- placeholder names, case, types, delimiters, and branch scope; compare occurrence counts only within corresponding retained or fixed branches, not as whole-message totals across a changed plural category set
- ICU argument syntax, `plural` and `select` controls, exact-number selectors, fixed `select` keys, `other`, number signs, offsets, skeletons, and required fallback branches
- markup, code, commands, identifiers, URLs, product codes, analytics values, and opaque runtime data

Translate prose inside required branches independently. Never translate a key or placeholder because its identifier resembles an English word, collapse branches because their current wording matches, or hardcode a runtime date, number, price, or user value.

## Software Constraints

- Preserve source/target key parity and reject duplicate, renamed, missing, or unexpected keys according to the approved catalog policy.
- Preserve placeholder set, type, multiplicity, and scope within every retained exact-number branch and fixed `select` branch. For plural categories, define the required nested-placeholder schema per target branch: adding or removing valid locale categories may change whole-message occurrence totals, but each retained or added target branch must contain its required placeholders and number signs without omission, renaming, duplication, or cross-branch substitution.
- Derive plural category branches from the target locale and production runtime, not exact source parity. Add categories such as `few` or `many` when required, omit category labels invalid for the target contract, and retain `other` plus every exact-number selector. Branch completeness means every category required by the target runtime has a non-empty target branch.
- Preserve fixed `select` keys exactly because they are application values rather than locale plural categories. Change them only when engineering changes the application contract.
- Keep values typed through runtime locale formats for numbers, dates, times, units, lists, and currency. Product owners decide the underlying value or currency; language specialists decide linguistic surroundings.
- Treat fallbacks as product configuration. Record any fallback-language text that reaches a localized UI as deliberate or defective; do not silently fill it.
- For RTL or bidirectional strings, supply direction-sensitive meaning and data types to an installed script specialist. Preserve opaque IDs and phone numbers; engineering owns isolation and mirroring behavior.
- Use pseudo-localization that expands text, exercises diacritics and direction where supported, and preserves keys, placeholders, ICU syntax, and protected spans.

## Targeted Research

Research only volatile facts required by the actual project: current runtime syntax, supported ICU features, framework locale behavior, or current CLDR/platform behavior. Prefer the installed dependency's documentation and authoritative standards. Do not recommend libraries, versions, or migration work unless the request asks for them and current project constraints have been verified.

## Authority and Conflict Boundary

Follow explicit user requirements, approved project configuration, and core semantic fidelity before product/platform formatting. Engineering owns executable resource contracts; product owns message intent and business values.

This skill owns software field classification, protected syntax, runtime constraints, and test gates. `translating-core` owns meaning and target copy; installed language and script specialists own linguistic, plural, locale-format, and RTL mechanics; `reviewing-translations` owns final review. Reject instructions to bypass or mutate an executable contract for speed. If approved wording conflicts with a hard runtime constraint, report the key, branch, and constraint without silently rewriting either.

## QA and CI Handoff

Pass source and target catalogs, locale pair, runtime/version, key and placeholder inventories, resource comments, rendering context, fallback policy, and these gates to `reviewing-translations` and CI:

- parse or compile every catalog and ICU message with the production runtime
- compare exact key, argument, fixed `select` key, exact-number selector, `other`, markup, escape, protected-span parity, and branch-scoped nested-placeholder schemas
- validate plural category labels against the target locale and production runtime, require complete target branches, and reject source-parity checks that would block required target categories
- execute representative values for every target plural category and fixed `select` key, including boundaries and exact-number selectors present in source
- render controlled dates, numbers, currency, units, and user/opaque data under the explicit target locale
- test missing/null argument and missing-key behavior according to the documented contract
- run pseudo-localization plus long-text, accessibility, truncation, and supported viewport checks
- run RTL/bidirectional cases for placeholders, punctuation, controls, directional symbols, and identifiers when applicable

Block CI or release on parse failure; key, argument, or ICU syntax drift; missing or changed exact-number selectors, fixed `select` keys, or required `other`; invalid or incomplete target-locale plural categories; branch-scoped placeholder-schema violations outside valid category additions/removals; hardcoded runtime values; unintended fallback-language text; unresolved direction semantics; or rendering that hides required content. Route each defect with its exact key and smallest unchanged message to the responsible installed skill.
