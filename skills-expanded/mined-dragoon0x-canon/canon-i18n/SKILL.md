---
name: canon-i18n
description: Use when designing or implementing internationalization — string externalization, locale-aware formatting, pluralization, text expansion, concatenation avoidance, and layout adaptation for multiple languages. Trigger when the user mentions i18n, internationalization, localization, translation, locale, or multi-language.
---

# CANON · Internationalization

I18n is preparing the codebase so that adding a new language doesn't require rewriting the UI. L10n is the act of adding one.

## Externalize all strings

No user-visible string lives in source code. Every string goes through a translation function.

```jsx
// Bad
<button>Save changes</button>

// Good
<button>{t('actions.save_changes')}</button>
```

Keys are structured, not sequential: `actions.save_changes` not `string_47`.

## Text expansion

German is 30–40% longer than English. Finnish, Russian, and Arabic can be longer still. Japanese and Chinese are often shorter.

| Language | Expansion vs English |
|---|---|
| German | +30–40% |
| French | +15–25% |
| Russian | +20–30% |
| Japanese | -20–30% |
| Arabic | +20–30% |

Design for 40% expansion. If a label barely fits in English, it breaks in German.

Test with pseudo-localization: replace strings with accented, expanded versions (`[Ŝàvé çhàñgéŝ!!!!]`) to catch overflow before real translations arrive.

## Never concatenate strings

```js
// Bad — word order varies by language
`Welcome, ${name}. You have ${count} messages.`

// Good — use ICU message format
t('welcome', { name, count })
// en: "Welcome, {name}. You have {count, plural, one {# message} other {# messages}}."
// ja: "{name}さん、{count}件のメッセージがあります。"
```

Concatenation assumes English word order. Interpolation with named variables lets translators reorder.

## Pluralization — ICU MessageFormat

English has 2 plural forms (singular, plural). Arabic has 6. Polish has 4. Use ICU `{count, plural, ...}` for every countable string.

```
{count, plural,
  =0 {No messages}
  one {# message}
  other {# messages}
}
```

Libraries: `intl-messageformat`, `i18next` with ICU plugin, `FormatJS`.

## Date, time, number formatting

Use `Intl` APIs. Never manually format.

```js
new Intl.DateTimeFormat('de-DE', { dateStyle: 'long' }).format(date);
// "18. April 2026"

new Intl.NumberFormat('en-IN').format(1234567);
// "12,34,567"
```

- Dates: `Intl.DateTimeFormat`. Month/day order varies by locale.
- Numbers: `Intl.NumberFormat`. Thousands/decimal separators vary.
- Currency: `Intl.NumberFormat` with `style: 'currency'`. Symbol position varies.
- Relative time: `Intl.RelativeTimeFormat`. "3 days ago" / "vor 3 Tagen".

## Font considerations

- Latin fonts don't cover CJK, Arabic, Devanagari, etc. Define font stacks per script family.
- CJK characters need larger line-height (1.6–1.8 for body) than Latin.
- Arabic is a connected script; ligatures and shaping are mandatory (`font-feature-settings` won't break Arabic, but custom letter-spacing will).
- Don't letter-space Arabic, Hebrew, or Devanagari. Tracking rules from `canon-typography` apply to Latin/Cyrillic only.

## Layout considerations

- Buttons must accommodate 40% text expansion without wrapping or truncating.
- Tables need flexible column widths.
- Navigation labels in German are long. Plan for wrapping or abbreviation.
- Fixed-width containers with translated text will overflow. Use `min-width`, not `width`.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Hardcoded strings in JSX/HTML | Untranslatable |
| String concatenation for sentences | Word order varies by language |
| `count === 1 ? 'item' : 'items'` | Wrong for Arabic, Polish, Russian, etc. |
| Manual date formatting | Month/day order varies |
| Fixed-width buttons with English text | German breaks them |
| Letter-spacing on Arabic text | Breaks connected script |
| One font stack for all scripts | Missing glyphs |
| Using flags for language switcher | Flags represent countries, not languages (Spanish is spoken in 20+ countries) |

## Audit checklist

- [ ] All user-visible strings externalized through a translation function
- [ ] Keys are structured and descriptive
- [ ] Pluralization uses ICU MessageFormat or equivalent
- [ ] Dates/numbers use `Intl` APIs
- [ ] Layout tested at 40% text expansion
- [ ] No string concatenation for sentences
- [ ] Font stacks cover target scripts
- [ ] No letter-spacing on connected scripts (Arabic, Hebrew, Devanagari)
- [ ] Language switcher uses language names, not flags
- [ ] RTL support via `canon-rtl` if targeting Arabic/Hebrew

## Sources

- W3C · Internationalization Best Practices
- Unicode CLDR · Plural rules by language
- ICU MessageFormat · Specification
- MDN · Intl API
- Material Design 3 · Internationalization
