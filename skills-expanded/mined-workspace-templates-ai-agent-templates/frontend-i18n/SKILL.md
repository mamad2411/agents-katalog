---
name: frontend-i18n
description: Extracts hard-coded UI text into translation files and handles plurals, dates, numbers and right-to-left layout for a multi-language frontend.
---

# Frontend i18n

Never translate by hand-editing the UI. Extract, key, format, then verify with a pseudo-locale.

## Steps

1. Detect the existing setup (react-i18next, vue-i18n, next-intl, Angular i18n, FormatJS). Use it. Only if none exists, recommend one that supports ICU messages and ask before installing.
2. Extract strings component by component. Keys are namespaced by feature and describe the role, not the English text: `checkout.submit.label`, not `place_your_order`. Add a short note for translators wherever the meaning is ambiguous ("Save" as a verb, "Order" as a noun).
3. Never concatenate. One whole sentence per message with placeholders: `"Welcome back, {name}"`. Word order differs by language.
4. Plurals use ICU: `"{count, plural, one {# file} other {# files}}"`. Some languages have up to six forms, so never write `count === 1 ? ... : ...`.
5. Format with Intl, not by hand: `Intl.DateTimeFormat`, `Intl.NumberFormat` (currency needs the currency code, not a symbol), `Intl.RelativeTimeFormat`, `Intl.ListFormat`. Store dates in UTC ISO and format at render time.
6. Layout. Use logical CSS properties (`margin-inline-start`, `padding-inline`, `text-align: start`), set `dir` and `lang` on the html element, and mirror directional icons, not logos or numerals.
7. Verify with a pseudo-locale that expands text by 40 percent and adds accents. Fix every clipped or overflowing label.
8. Fallbacks: missing keys fall back to the default language and are logged in development, never shown as raw keys.

## Report

Keys added per file, files with remaining hard-coded text, and anything that needs a translator's judgment.
