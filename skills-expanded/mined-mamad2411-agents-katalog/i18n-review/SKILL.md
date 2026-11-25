---
name: i18n-review
description: Audit code and UI for internationalization correctness - string extraction, pluralization, dates/numbers/currencies, RTL support, and locale-aware sorting. Use when the user asks for an i18n review, localization audit, or wants to make an app translation-ready.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [i18n, l10n, localization, review]
---

# i18n Review

The goal: a translator can ship a new locale **without touching code**, and the result is correct for native speakers, not "English with words swapped."

## When to use

- "Review X for i18n / localization"
- "Audit translation readiness"
- "Make this app translatable"
- "Add support for <locale>"

## Procedure

1. **Identify the framework** — `i18next`, `react-intl`, `vue-i18n`, `Laravel __()`, `gettext`, `Rails I18n`, custom? Match existing conventions.
2. **Walk the checklist** below
3. **Group findings by severity**

## Checklist

### String extraction

- [ ] **No hardcoded user-facing strings** in templates, components, or controllers
- [ ] Strings live in translation files (`en.json`, `messages.po`, `lang/en/…`)
- [ ] Translation keys are **stable identifiers**, not the English text itself (`auth.login.title` not `"Sign in"`)
- [ ] Keys aren't constructed dynamically (`t('errors.' + code)` defeats static extraction — use a switch with explicit keys instead)
- [ ] No concatenated sentences: `t('hello') + ' ' + name` → use interpolation: `t('hello_name', {name})`
- [ ] No HTML embedded in translatable strings — use placeholders or rich-text helpers
- [ ] Plurals use the framework's plural helper, not `if (n === 1)`

### Plurals

Plural rules vary wildly. English has 2 forms; Polish has 4; Arabic has 6. Don't fake it:

```js
// ❌ Don't
const msg = count === 1 ? '1 item' : `${count} items`;

// ✅ Do
t('item_count', { count })
// en.json: { "item_count_one": "{{count}} item", "item_count_other": "{{count}} items" }
// pl.json: { "item_count_one": "...", "item_count_few": "...", "item_count_many": "...", "item_count_other": "..." }
```

### Dates, numbers, currencies

- [ ] No hardcoded date formats (`YYYY-MM-DD`) for display — use `Intl.DateTimeFormat` or framework helper
- [ ] Numbers formatted with locale separators (`1,234.56` vs `1.234,56` vs `1 234,56`)
- [ ] Currencies formatted with `Intl.NumberFormat(locale, {style:'currency', currency})`, **never** by string concat (`'$' + amount`)
- [ ] Currency *code* stored, locale-formatted on display
- [ ] Time zones explicit — store UTC, display in user's TZ
- [ ] Week start day not hardcoded (Sunday vs Monday vs Saturday varies)

### Text direction (RTL)

- [ ] Layout uses **logical properties**: `margin-inline-start` not `margin-left`, `padding-inline-end` not `padding-right`
- [ ] `dir="rtl"` flips the layout correctly (test with Arabic, Hebrew, or `?dir=rtl`)
- [ ] Icons that imply direction (arrows, back/forward) flip in RTL
- [ ] Numbers and code blocks stay LTR even in RTL contexts
- [ ] No `text-align: left` when you mean "start" — use `text-align: start`

### Sorting & collation

- [ ] Lists sorted with `Intl.Collator(locale)`, not byte-wise / `Array.sort()`
- [ ] Case-insensitive comparisons use `localeCompare` with proper options
- [ ] Search/filter is accent-insensitive where appropriate (`sensitivity: 'base'`)

### Input

- [ ] Name fields accept unicode (no `[a-zA-Z]+` validation)
- [ ] Email validation allows internationalized domains
- [ ] Phone number format not hardcoded to one country (use `libphonenumber` or similar)
- [ ] Address forms don't assume US-style state/zip
- [ ] Long words / long translations don't break layout (German is famously verbose)

### Tooling

- [ ] Linter / extractor rule prevents new hardcoded strings (`eslint-plugin-i18next`, `i18n-ally`, `phpcs` rules, …)
- [ ] CI fails if translations are missing keys (or warns with a baseline)
- [ ] Locale fallback chain is explicit (`fr-CA → fr → en`)
- [ ] Language switching doesn't require full reload (where the framework supports it)

## Quick greps

```bash
# Hardcoded English strings in templates (heuristic)
grep -RInE '>[A-Z][a-z]+ [a-z]+' --include='*.{vue,jsx,tsx,blade.php,erb}' . | head

# Concatenated translations
grep -RInE "t\([^)]+\)\s*\+|i18n\.[a-z]+\([^)]+\)\s*\+" --include='*.{js,ts,jsx,tsx,vue}' .

# Hardcoded currency symbols
grep -RInE "['\"\`]\\\$\{|\\\$[0-9]|'\\\$'" --include='*.{js,ts,jsx,tsx,vue,blade.php}' .

# Physical CSS properties that should be logical
grep -RInE 'margin-(left|right)|padding-(left|right)|text-align:\s*(left|right)' \
  --include='*.{css,scss,vue,jsx,tsx}' .

# Date format strings that look hardcoded
grep -RInE "format\(['\"](YYYY|DD|MM)" --include='*.{js,ts,jsx,tsx,vue}' .
```

## Output format

```markdown
## i18n review: <scope>

**Framework:** <i18next / vue-i18n / Laravel / …>
**Locales in use:** <en, no, ar, …>

### 🔴 Blockers
- `path/file.tsx:42` — <issue>. **Impact:** <breaks for which locales/users>. **Fix:** <what>.

### 🟠 Major
- …

### 🟡 Minor
- …

### ✅ What's working
- <category> — <one sentence>
```

### Severity rubric

| Tag | Meaning |
|---|---|
| 🔴 **Blocker** | Cannot be translated correctly (hardcoded strings, broken plurals, broken RTL layout) |
| 🟠 **Major** | Renders incorrectly for many locales (date/number format, sorting, address forms) |
| 🟡 **Minor** | Polish (long-text overflow, missing locale fallback) |

## Anti-patterns

- ❌ `t('You have ' + count + ' messages')` — broken in every language with grammatical agreement
- ❌ Translating button text but baking in `width: 80px` (German "Einstellungen" doesn't fit)
- ❌ Storing formatted currency in DB (`"$10.00"`)
- ❌ Sorting names with `Array.sort()` instead of `Intl.Collator`
- ❌ Right-aligned designs that "just work" in LTR
- ❌ Assuming names have a first and a last name with a space between
- ❌ Validating names with `[a-zA-Z\s]+`
- ❌ Mirror-flipping all icons in RTL (don't flip clocks, logos, media controls)

## Useful references

- [Unicode CLDR](https://cldr.unicode.org/) — locale data the world relies on
- [W3C Internationalization Activity](https://www.w3.org/International/) — specs and guides
- [MDN: Intl](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl) — browser-native locale APIs
- [Falsehoods Programmers Believe About Names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/)
- [Falsehoods Programmers Believe About Time](https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca)
