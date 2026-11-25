---
name: internationalization
description: Makes applications ready for multiple languages and regions with externalized strings, ICU MessageFormat plurals, locale-aware dates, numbers and currencies, time zones, RTL layouts, Unicode-safe text handling and pseudo-localization. Use when adding i18n or l10n support, a new language or market, fixing concatenated or hard-coded strings, wrong date or number formats, plural bugs, or right-to-left layout issues. Not for writing the translations themselves.
license: MIT
---

# Internationalization

Every user-visible string, number, date, currency and sort order goes through a locale-aware API. Never build sentences by concatenation, never hard-code formats, and never assume text is short, left-to-right, or ASCII.

Internationalization (i18n) is the engineering that makes software adaptable; localization (l10n) is the translation and adaptation for each locale. This skill is the engineering part.

## When to use

- Adding multi-language support, or a new language or market.
- Hard-coded strings, string concatenation with variables, `+ "s"` pluralization.
- Dates, numbers or currencies shown in the wrong format; time-zone bugs.
- Arabic, Hebrew, Persian or Urdu support (right-to-left).
- Sorting, searching or length limits that break on non-English text.

Not for: translating content itself, or choosing a translation vendor.

## Workflow

1. **Audit.** Search the codebase for user-facing string literals in UI and error messages, manual date formatting (`MM/DD/YYYY`, `strftime` with fixed patterns), `toLocaleString()` without a locale argument, concatenation around variables, and ternaries that pluralize.
2. **Pick the stack** (table below) and set up message catalogs per locale, ICU MessageFormat, locale negotiation and fallback.
3. **Externalize strings** with stable keys and translator descriptions.
4. **Replace formatting** with locale-aware APIs.
5. **Make layout flexible** for text expansion and RTL.
6. **Pseudo-localize and test** (below), plus one real RTL locale and one language with complex plurals.
7. **Wire the translation workflow**: automatic extraction, CI checks for missing or unused keys, review before release.

## Libraries by stack

| Stack | Common choices |
| --- | --- |
| JavaScript / TypeScript | FormatJS (react-intl), i18next (ICU via a plugin), Lingui; built-in `Intl` APIs for formatting |
| Java / Kotlin | ICU4J, `ResourceBundle`, `java.time.format` |
| .NET | `.resx` resources with `IStringLocalizer`, `CultureInfo` for formatting |
| Python | `gettext` with Babel |
| Mozilla-style projects | Fluent |
| Mobile | Platform string catalogs and formatters (iOS Foundation formatters, Android resources and `android.icu`) |

Pick one message syntax for the whole product. ICU MessageFormat is the most widely supported.

## Messages

Bad:

```js
"You have " + n + " new messages"
n + " item" + (n === 1 ? "" : "s")
```

Good (ICU MessageFormat):

```
{count, plural,
  =0 {You have no new messages}
  one {You have # new message}
  other {You have # new messages}}
```

Rules:

- Languages have up to six plural categories (CLDR: `zero`, `one`, `two`, `few`, `many`, `other`). Always include `other`. Use `=0` for special zero text. Never decide plurals in code.
- Use `select` for grammatical variants: `{gender, select, female {She replied} male {He replied} other {They replied}}`.
- One complete sentence per message. Word order differs between languages, so don't split a sentence into fragments. For inline links or bold text, use rich-text placeholders such as `Read the <link>terms</link>` if your library supports tags.
- Named placeholders (`{userName}`), never positional fragments.
- Give translators context: a description per message, where it appears, maximum length, and a screenshot when possible.
- Don't reuse a string just because the English matches. "Open" as a button verb and "Open" as a status are different messages.
- Keys: stable semantic keys (`checkout.payButton.label`) survive copy edits. If the meaning changes, create a new key so old translations are not reused wrongly.
- No text inside images. Don't use flags for languages; list language names in their own language ("Deutsch", "日本語", "العربية").

Read [references/message-format.md](references/message-format.md) when writing ICU messages with plurals, ordinals, selects, nested arguments, or apostrophes.

## Locale-aware formatting

| Need | JavaScript `Intl` |
| --- | --- |
| Dates and times | `new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short", timeZone })` |
| Numbers | `new Intl.NumberFormat(locale)` |
| Currency | `new Intl.NumberFormat(locale, { style: "currency", currency: "EUR" })` |
| Percent, units, compact | `style: "percent"`, `style: "unit"`, `notation: "compact"` |
| Lists ("A, B and C") | `new Intl.ListFormat(locale, { type: "conjunction" })` |
| Relative time ("3 days ago") | `new Intl.RelativeTimeFormat(locale, { numeric: "auto" })` |
| Plural category | `new Intl.PluralRules(locale)` |
| Sorting | `new Intl.Collator(locale).compare` |
| User-perceived characters | `new Intl.Segmenter(locale, { granularity: "grapheme" })` |
| Language and region names | `new Intl.DisplayNames(locale, { type: "language" })` |

Other platforms have equivalents (ICU4J, `java.time.format`, .NET `CultureInfo` with standard format strings, Babel). Rules:

- Store money as an amount plus an ISO 4217 currency code. The locale decides how it is displayed; it does not decide the currency.
- Machine formats stay locale-neutral: ISO 8601 dates and plain decimal numbers in APIs, logs, CSV exports for systems, and database columns.
- Parsing user input is locale-sensitive too (decimal comma, date order). Prefer locale-aware date pickers and number inputs.
- Cache formatter instances; constructing `Intl` objects is relatively expensive in hot loops.

## Time zones

- Store instants in UTC (`timestamptz`, ISO 8601 with offset) and display them in the user's zone.
- Use IANA zone IDs (`Europe/Berlin`), never fixed offsets or abbreviations like "EST", which are ambiguous and ignore DST.
- Future events in local time (a 09:00 meeting in Berlin next year): store the local date-time plus the IANA zone, because DST rules can change before the event.
- Date-only values (birthdays, due dates) are not instants. Store them as dates, not as midnight UTC, or they shift by a day for users west of UTC.
- First day of the week, weekends and calendars differ by locale; take them from locale data, not constants.
- Test across DST transitions and the date line.

## Layout and text expansion

- Translations are often much longer than English, and short labels can double. Don't give text containers fixed widths; allow wrapping; test with pseudo-localization.
- Some scripts need more line height (Thai, Devanagari, Arabic). Make sure fonts cover every supported script, with fallbacks.
- Truncate on grapheme boundaries and prefer CSS truncation (`text-overflow: ellipsis`) over cutting strings in code.

## Right-to-left

- Set `<html lang="ar" dir="rtl">`. Use `dir="auto"` on user-generated content and `<bdi>` around embedded names or values whose direction is unknown.
- Use CSS logical properties: `margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `border-inline-start`, `text-align: start`. Avoid `left`/`right` in layout styles.
- Flexbox and grid follow the writing direction automatically when you use logical values.
- Mirror icons that imply direction (back/forward arrows, progress, "next"). Don't mirror logos, checkmarks, or media playback controls.
- Numbers and Latin-script fragments inside RTL text still render left to right; the bidi algorithm handles this when markup is correct.

## Locale negotiation

- Use BCP 47 tags: `en-US`, `pt-BR`, `zh-Hant-TW`, `sr-Latn`.
- Priority: explicit user choice saved on the profile, then the locale in the URL (`/de/...`), then the `Accept-Language` header, then the default. Don't pick the language from IP geolocation; at most suggest it.
- Fallback chain: `pt-BR` → `pt` → default language, per message. Log missing keys so they are fixed rather than silently shown in the default language forever.
- Keep language, formatting region and currency as separate settings where users may need them to differ.
- Always set the `lang` attribute; screen readers, hyphenation and font selection depend on it.

## Unicode and text handling

- UTF-8 end to end. In MySQL use `utf8mb4`; the legacy `utf8` charset cannot store all characters (for example most emoji).
- Length is not characters: in JavaScript `"👍🏽".length` is 4 (UTF-16 code units). Count graphemes with `Intl.Segmenter` for user-facing limits, and know whether database limits count characters or bytes.
- Normalize (NFC) before comparing or storing identifiers: `s.normalize("NFC")` in JS, `unicodedata.normalize("NFC", s)` in Python.
- Case mapping is locale-sensitive (Turkish dotted and dotless i). For case-insensitive matching use a collator or case folding (`str.casefold()` in Python), not `toLowerCase()` for identity checks.
- Sort with a collator (`Intl.Collator`, ICU) and set the database collation for `ORDER BY` on user-visible text.
- Names, addresses and phone numbers: don't require first/last name, don't validate names against `[A-Za-z]`, use a library such as libphonenumber for phone numbers, and let address formats vary by country.

## Pseudo-localization

Generate a fake locale that accents every character, pads text and wraps it in markers, for example `[Ŝàvé ĉĥàñĝéš ~~~~]`:

- Unaccented text on screen is a hard-coded string.
- A missing closing bracket is truncation.
- Broken words around a variable reveal concatenation.

Also run with a pseudo-RTL locale (Android ships `en-XA` for accented text and `ar-XB` for RTL) and with a real RTL language. Include a language with complex plurals (Arabic, Polish or Russian) in tests.

## Anti-patterns

- **Concatenating sentences** or pluralizing with `n === 1`.
- **Splitting one sentence into several messages.**
- **Hard-coded formats**: `MM/DD/YYYY`, `$` prefixes, `,` thousand separators.
- **`toLocaleString()` without an explicit locale**, which uses the server's or browser's default instead of the user's choice.
- **Storing local times without a zone**, or date-only values as midnight UTC.
- **`left`/`right` CSS** in components that must support RTL.
- **Fixed-width buttons and labels.**
- **Language chosen by IP address.**
- **Translating keys directly in code** instead of through the catalog, so they are never extracted.

## Done when

- No user-facing literals remain in code (pseudo-locale shows every string accented).
- All plurals and gender variants use ICU (or equivalent) messages with `other` cases.
- Dates, numbers, currencies, lists and sorting go through locale-aware APIs with the user's locale.
- Instants are stored in UTC; future local events store an IANA zone.
- The UI works in a pseudo-locale, a real RTL locale and a complex-plural locale without clipping or mirrored-layout bugs.
- CI fails on missing keys in the source locale and reports untranslated keys per locale.

## References

- [references/message-format.md](references/message-format.md) — read when writing or reviewing ICU MessageFormat strings.
