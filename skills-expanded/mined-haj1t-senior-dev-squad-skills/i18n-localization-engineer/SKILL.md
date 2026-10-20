---
name: i18n-localization-engineer
description: "ICU MessageFormat, RTL/bidi layout, Intl API, locale fallback chains, pseudo-localization, TMS handoff, plural/gender rules. Use when internationalizing or localizing a UI."
---

# I18n Localization Engineer

## Overview

Internationalization (i18n) is the engineering discipline of structuring code so every user-facing string, number, date, currency, and layout adapts to any locale without changing source code. Localization (l10n) is the act of producing those locale-specific assets. Done well, the two are invisible to users and seamless for translators. Done poorly, they produce garbled text, broken layouts, untranslatable strings, and shipping delays every release.

This skill covers the full pipeline: externalizing strings, writing ICU MessageFormat messages, wiring the `Intl` API for dates/numbers/currencies, handling RTL and bidi layout, designing locale fallback chains, generating pseudo-locales for early testing, and handing off catalogs to a translation management system (TMS).

**Core principle:** Every user-visible string is a locale resource. If it lives in source code, it is a bug.

## The Iron Law

```
NO HARDCODED UI TEXT — EVERY STRING LIVES IN A LOCALE CATALOG
```

If a string is rendered to the user and is not looked up through the i18n layer, the feature is not shippable to non-English locales.

## When to Use

**Use this when:**
- Adding any new UI text, labels, error messages, tooltips, or notifications
- Implementing date, time, number, or currency display
- Supporting a new locale or language in the product
- Designing the initial i18n architecture for a frontend or backend service
- Auditing an existing codebase for hardcoded strings

**Use this ESPECIALLY when:**
- The product is expanding to a new region or language for the first time
- A feature contains plural forms ("1 item" vs "2 items"), gender-inflected strings, or ordinals
- The layout must support right-to-left scripts (Arabic, Hebrew, Persian, Urdu)
- Translators report missing context, broken interpolations, or strings they cannot translate
- The CI pipeline does not yet catch new hardcoded strings

**Don't skip when:**
- The feature "is just for English for now" — retrofitting i18n is 5× the work of doing it upfront
- Strings are generated dynamically or concatenated from parts — these are the hardest to localize later
- A design uses absolute pixel positioning — RTL will break it

## Workflow

**String Externalization.** Extract every user-facing string to a locale catalog before the feature ships, using ICU MessageFormat as the canonical message format. Never concatenate translated strings — always use a single message key with named placeholders. See [REFERENCE.md](REFERENCE.md) for directory layout, bad/good code examples, and the concatenation rule.

**ICU MessageFormat Patterns.** Use ICU to handle plurals, gender selects, nested combinations, and date/time annotations in a single string that translators can reorder freely. Always include a `_comment` context note next to each key. See [REFERENCE.md](REFERENCE.md) for plural, select, nested, and date/time pattern examples with translator comment conventions.

**Intl API for Dates, Numbers, and Currencies.** Never format dates or numbers with hand-rolled logic — use the ECMA-402 `Intl` API available in every modern runtime. Never call `Date.toLocaleString()` without an explicit locale argument. See [REFERENCE.md](REFERENCE.md) for `Intl.DateTimeFormat`, `RelativeTimeFormat`, `NumberFormat`, and `ListFormat` usage examples.

**RTL and Bidi Layout.** RTL support is a layout concern, not just a text concern. Every directional CSS property must use logical-property equivalents (`inline-start/end`, `block-start/end`). Set `dir` and `lang` on `<html>` at runtime. For inline bidi text use `<bdi>` or `unicode-bidi: isolate`. See [REFERENCE.md](REFERENCE.md) for CSS logical-property patterns, runtime `dir`/`lang` wiring, the RTL locale set, and bidi isolation guidance.

**Locale Fallback Chains and Bundle Loading.** Define fallback chains explicitly (e.g. `zh-Hant-TW` → `zh-Hant` → `zh` → `en`); do not rely on browser behavior. Lazy-load locale bundles per chain candidate to avoid shipping all translations to every user. See [REFERENCE.md](REFERENCE.md) for `buildFallbackChain` and `loadMessages` implementations.

**Pseudo-Localization for Early Testing.** Generate a synthetic pseudo-locale that expands strings ~30–40%, replaces ASCII with accented equivalents, wraps strings in `[` `]` brackets, and preserves ICU placeholders intact. Run it in CI visual regression to catch overflow and hardcoded strings every sprint, not just at launch. See [REFERENCE.md](REFERENCE.md) for the complete `pseudoLocalize` function and CI integration guidance.

**TMS Handoff and Translator Context.** When exporting to a TMS (Lokalise, Phrase, Crowdin, Transifex), use hierarchical noun-first key names, include screenshots or context URLs, set max-length hints, and mark non-translatable tokens as named placeholders. Verify ICU support before export; convert to platform-native plural categories if not supported. See [REFERENCE.md](REFERENCE.md) for key naming conventions, TMS metadata fields, and the non-translatable token pattern.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "I'll just hardcode this label, it's a one-off" — every hardcoded string blocks a locale
- "The translator will figure out the word order" — concatenated strings are untranslatable
- "We can add RTL support later, we don't have Arabic users yet" — logical-property CSS costs nothing upfront; retrofitting costs days
- "I'll use `toLocaleDateString()` without a locale argument, it'll be fine" — it produces undefined behavior in server-side rendering and CI
- "The plural rule for Chinese is simple, I won't bother with ICU" — Chinese has one plural category, but adding ICU upfront costs nothing and prevents rework if the product adds Polish, Arabic, or Russian (which have 3–6 categories)
- Missing translator context on any key
- A new feature ships with zero entries in the locale catalog

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "English only for now, we'll i18n later" | Retrofitting i18n into an existing codebase takes weeks and touches every component. Do it first. |
| "It's just a number, I'll format it inline" | `1,234.56` vs `1.234,56` vs `1 234,56` — number formats differ by locale and break trust. |
| "Translators don't need context, the string is obvious" | "Order" is a noun in one place and a verb in another. Without context, translators guess wrong. |
| "We don't have RTL locales in our user base" | CSS logical properties are a zero-cost habit. Skipping them creates a weeks-long migration when you do expand. |
| "Pseudo-localization is only needed before launch" | New strings are added every sprint. Pseudo-locale CI catches overflow continuously, not just at launch. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "The Arabic layout looks like a mirror image only in some places" — you used physical CSS properties (`left`, `right`, `margin-left`) instead of logical ones
- "Translators are asking what this string is for" — you shipped keys without context comments
- "Some strings in production are still in English" — your CI does not enforce full catalog coverage, or a string was added after the translation freeze
- "The date looks wrong in Germany" — you formatted with `Date.toLocaleString()` without a locale, or used `MM/DD/YYYY` directly

**When you see these:** STOP. Return to the relevant phase and fix the root cause — do not patch individual strings.

## Related Skills

- **frontend-senior-engineer** — component architecture that the i18n layer must integrate with; use together for new feature builds
- **accessibility-optimizer** — `lang` attributes, bidi markup, and screen-reader announcements overlap with i18n concerns
- **content-strategist** — source string quality and tone directly affect translatability; coordinate on key naming and content guidelines
- **responsive-layout-engine** — RTL layout work belongs in the responsive system; logical properties must be enforced at the design-system level

## Verification

- [ ] Zero hardcoded user-visible strings in new or modified components (grep for string literals in JSX/templates)
- [ ] All new message keys use ICU MessageFormat for plural, select, and interpolation
- [ ] Every new key has a `_comment` or TMS context note explaining usage and any non-translatable tokens
- [ ] Dates, times, numbers, and currencies use `Intl` API with an explicit locale argument
- [ ] CSS uses logical properties (`inline-start/end`, `block-start/end`) — no `left`, `right`, `margin-left`, `padding-right` in new styles
- [ ] `<html>` element receives `lang` and `dir` attributes at runtime based on active locale
- [ ] Locale fallback chain is defined and tested for all supported locales
- [ ] Locale bundles are lazy-loaded; no single bundle contains all locales
- [ ] Pseudo-locale build passes without layout overflow in visual regression
- [ ] TMS export includes max-length hints and non-translatable token markers
- [ ] CI lint rule (e.g., `eslint-plugin-i18next` or equivalent) blocks new hardcoded strings in PRs
