---
name: common-i18n
description: Internationalization and localization — string externalization, ICU MessageFormat, plurals, RTL, locale-aware formatting, translation workflow. Auto-invoked when adding locales, debugging localized bugs, or designing the i18n architecture.
---

# Internationalization

Internationalization done late is ten times the work: string concatenation,
hard-coded dates, and `if (plural)` branches accumulate into a localization tax that
only grows. The goal is an architecture where translation is a content problem, not
an engineering problem.

## When to reach for this

- Designing the i18n architecture: catalogs, extraction pipeline, fallback chain
- Adding a locale (especially a first RTL or CJK locale) to an existing product
- Debugging localized bugs — wrong plurals, broken BiDi, mis-formatted dates/currency
- Setting up or fixing the translation workflow (TMS, pseudo-locale CI)

## Principles

1. **Never concatenate user-visible strings.** `"Hello, " + name` is a localization
   bug — translators rearrange words; code can't. Use ICU parameters: `"Hello, {name}"`.
2. **ICU MessageFormat for every variable string.** Plurals, gender, select. Plain
   interpolation fails the moment a second locale arrives (many languages have more
   than two plural forms).
3. **Format via CLDR, never by hand.** Dates, times, numbers, currencies, relative
   time, and lists go through locale-aware APIs (`Intl.*`, ICU libraries) — never
   `toFixed()` + a hard-coded symbol.
4. **Logical CSS properties everywhere.** `margin-inline-start`, not `margin-left`;
   `padding-inline-end`, not `padding-right`. Icons that "point forward" need RTL
   variants or logical transforms.
5. **Pseudo-localize in CI.** Wrap every string with accents and ~50% expansion. Any
   plain-English text in the UI is an un-externalized string; any clipped text is a
   fixed-width bug — caught before a single translator is paid.
6. **Separate code locale from user locale.** Logs, error stacks, and analytics event
   names stay in English; only user-facing surfaces localize.
7. **Keep translation continuous.** Every PR that adds strings triggers extraction →
   TMS push → machine-translate → human review. Batch localization kills velocity.
8. **Detect locale in order:** explicit user preference → browser/device setting →
   geo → default, with an always-visible override UI.

## ICU patterns — required and forbidden

```text
✅ "You have {count, plural, one {# item} other {# items}} in your cart"
✅ "{name} commented on {gender, select, female {her} male {his} other {their}} post"
✅ "Last updated {when, time, short} on {when, date, medium}"

❌ "You have " + count + " item" + (count === 1 ? "" : "s")     // plural rules vary
❌ `${currencySymbol}${amount.toFixed(2)}`                       // CLDR placement/precision
❌ t("greeting_start") + name + t("greeting_end")                // word-order assumption
```

Catalog hygiene: one source-of-truth format (ARB/XLIFF/JSON), keys namespaced by
surface, a documented fallback chain (e.g. `fr-CA → fr → en`), and translator
comments on every ambiguous string.

## Launch-locale checklist

- [ ] Pseudo-locale pass clean (no raw English, no clipped layouts)
- [ ] RTL screenshot suite reviewed (if the locale is RTL)
- [ ] Font/script coverage verified (CJK weight, Arabic shaping, Thai line-breaking)
- [ ] Dates, numbers, currency spot-checked against CLDR expectations
- [ ] Legal/regulated copy reviewed for the jurisdiction
- [ ] Locale-override UI reachable and persistent

## Pitfalls

- Translating keys ("save_button") shipped to production as visible text
- Splitting a sentence across multiple HTML elements, making it untranslatable as a unit
- Sorting user-visible lists with code-point order instead of locale-aware collation
- Embedding directional punctuation around user input without BiDi isolation (`<bdi>`)
- Re-using one string in two contexts where target languages need different translations
- Hard-coding a 24-hour or MM/DD assumption anywhere near a formatter

---
*Related: `common-a11y` (RTL affects focus order), `ux-design` (text-expansion
layout), `common-notifications` (localized templates) · pulled by any domain agent ·
output/ADR format: `playbook-conventions`*
