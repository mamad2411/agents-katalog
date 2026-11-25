---
name: localization-copy
description: Localization and translation of product copy — l10n and i18n, translation vs transcreation vs localisation, tone and register preservation, glossary and termbase, do-not-translate list, placeholder and variable safety, ICU pluralisation and gender, string interpolation, text expansion and contraction and layout breakage, locale conventions for dates numbers currency and name order, cultural adaptation and taboo check, native-speaker review, LQA linguistic quality assurance pass, and verifying numbers and facts survive translation unchanged.
---

# Localization Copy (translating product and marketing text safely)

## Pick the right mode per string

```
translation   → preserve meaning, sentence by sentence      (legal, docs, UI labels)
localisation  → meaning plus locale conventions/references  (most product UI, help)
transcreation → preserve intent and effect, rewrite freely   (taglines, ads, names)
```

The commonest failure is applying translation where transcreation was needed: a wordplay headline
rendered literally is not wrong word-by-word and still fails completely. Mark the mode on each string
before it leaves, and brief transcreation with intent, audience and constraint (character limit, brand
line), not with the source sentence alone.

## Tone and register are part of the spec

Formality is grammatical in many languages (T–V distinction, honorific levels), so "friendly" is not
portable — specify register per locale explicitly, including how the product addresses the user and
whether imperatives read as rude, and hold it constant product-wide.

## Glossary and do-not-translate

Keep a termbase with, per term: source term, approved target per locale, part of speech, short
definition, forbidden alternatives. Keep a separate do-not-translate list: product and feature names,
brands, trademarks, code identifiers, API field names, third-party UI labels seen verbatim, and units
the market uses in source form. Without it, translators localise your own feature name and UI, docs
and support macros diverge permanently.

## Placeholder, variable and plural safety

Placeholders must reach the translator intact, reorderable and documented — state what `{count}`, `%1$s`
or `{name}` will hold, since the target may need a different word order. Never concatenate sentence
fragments in code: fragments cannot be reordered or inflected. Use ICU-style plural categories rather
than `if n == 1`; locales use different category sets (zero, one, two, few, many, other) that a
two-branch string cannot express — likewise gender and select variants. Validate mechanically:
identical placeholder set source-vs-target, no renamed tokens, no dropped markup.

## Length, layout and locale conventions

Text length changes substantially in both directions and string-dependently — short UI labels expand
proportionally more than paragraphs. Design for reflow, not a length budget: no truncation-sensitive
fixed widths, no text in images, pseudo-localisation in CI to surface overflow early. Check line
breaking for spaceless languages, font coverage, and RTL mirroring of layout and directional icons.

Never format by hand; delegate to a locale-aware library for date and time (order, calendar, 12/24h),
numbers (separators differ, and a comma decimal misread as a thousands separator is a silent
thousand-fold error), currency (symbol position, and whether to convert prices at all), name order and
family-name field, address shape, phone formats, collation and units.

## Cultural adaptation and taboo check

Screen imagery, colour, gesture and number connotations, humour that does not transfer, holiday and
seasonal references, pop-culture analogies, maps and territory naming, religious references, and
anything legally sensitive (health, financial, comparative claims) — an in-market review step.

## Review, LQA and fact integrity

Two distinct passes. **Native-speaker review** checks meaning, register, naturalness and terminology
compliance, performed by someone other than the translator. **LQA** checks strings in the running product
in context: truncation, wrong plural branch, placeholder leakage, mismatched screenshots, untranslated
fallbacks, mixed-language screens. Separately verify facts survive unchanged — prices, percentages,
dates, versions, legal thresholds, URLs, contacts — compared mechanically, never by reading.

## Failure modes

- Machine translation shipped without review, especially for priced or legal user-facing copy.
- Strings sent without screenshots, so ambiguous source words get the wrong sense; the same string
  rendered differently in UI, help centre and store listing; the translator acting as own reviewer.
- Locale treated as language; hardcoded source fallbacks masking missing translations in production.

## Reviewer checklist

- [ ] Mode marked per string (translation / localisation / transcreation), with briefs for the last
- [ ] Register and address form specified per locale; termbase and DNT list current and enforced
- [ ] Placeholders validated source-vs-target; no concatenated sentence fragments
- [ ] Plural and gender handled via locale category sets, not `n == 1`
- [ ] Pseudo-localisation run; no fixed widths, no text in images; RTL mirroring checked
- [ ] Dates, numbers, currency, names and sorting produced by locale-aware code
- [ ] In-market cultural and legal-claim review done; independent native-speaker review plus
      in-context LQA pass, both signed off
- [ ] Numbers, prices, dates, URLs and contacts diffed against source and unchanged

## Provenance

Standard localisation-industry practice (mode selection, termbase and DNT discipline, ICU plural
categories, pseudo-localisation, separate review and LQA passes). No expansion percentage, quality
score or vendor benchmark is quoted, because none was verified; any figure introduced later is
**derived, unverified** and must be replaced with the project's own measured values before treating it
as a target. Verify locale formatting against CLDR/ICU data, not assumption.
