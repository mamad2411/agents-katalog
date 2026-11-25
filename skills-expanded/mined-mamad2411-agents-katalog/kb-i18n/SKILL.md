---
name: kb-i18n
last-verified: 2026-04-23
description: Portable reference for internationalization and localization — not grounded in this repo (single-locale starter). Invoke when a derived project adds i18n to Next.js, React, or Python, audits translation-key discipline, handles RTL layout, or plans pluralization and date/number formatting. Covers locale vs language, `Intl.*`, ICU MessageFormat, logical CSS properties.
---

# i18n & Localization

> **Scope:** stack-agnostic i18n principles + pointers for Next.js / React / Python.
> **Not grounded in this repo.** TimeKast Factory starter is single-locale — this skill activates in projects that add i18n.
> For Flutter ARB — see `kb-flutter §10`.

---

## 1. Core concepts

| Term       | Meaning                                           |
| ---------- | ------------------------------------------------- |
| **i18n**   | Internationalization — making an app translatable |
| **L10n**   | Localization — the actual translations            |
| **Locale** | Language + region (`en-US`, `tr-TR`, `es-419`)    |
| **RTL**    | Right-to-left languages (Arabic, Hebrew)          |

---

## 2. When to use i18n

| Project type      | i18n needed?       |
| ----------------- | ------------------ |
| Public web app    | ✅ Yes             |
| SaaS product      | ✅ Yes             |
| Internal tool     | ⚠️ Maybe           |
| Single-region app | ⚠️ Plan for future |
| Personal / MVP    | ❌ Optional        |

> **Rule:** if you're not sure yet, _still_ use translation keys from day one. The cost of adding `t('title')` is minimal; retrofitting hardcoded strings is painful.

---

## 3. Implementation patterns

### Next.js 16+ — `next-intl` (App Router)

```ts-example
import { useTranslations } from 'next-intl';

export default function Page() {
  const t = useTranslations('Home');
  return <h1>{t('title')}</h1>;
}
```

`next-intl` integrates with App Router routing (`[locale]` segment), Server Components, and middleware-based locale detection. Prefer over `next-i18next` for new projects.

### React (non-Next) — `react-i18next`

```ts-example
import { useTranslation } from 'react-i18next';

function Welcome() {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
}
```

### Python — `gettext`

```python
from gettext import gettext as _
print(_("Welcome to our app"))
```

---

## 4. File structure

Split by feature (namespace), one file per locale:

```
locales/
├── en/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
├── tr/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
└── ar/                 # RTL
    └── ...
```

> Namespacing by feature keeps each translator focused and avoids merge conflicts on a single giant file.

---

## 5. Pluralization & complex strings — ICU MessageFormat

For anything beyond a simple string, use ICU syntax:

```json
{
  "items": "{count, plural, =0 {No items} one {# item} other {# items}}"
}
```

Both `next-intl` and `react-i18next` support ICU. **Never** build strings via concatenation — it breaks grammar in most languages.

---

## 6. Date / number formatting — `Intl` API

```ts
new Intl.DateTimeFormat('es-ES', { dateStyle: 'long' }).format(new Date());
new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR' }).format(1234.56);
```

> **Rule:** never hand-format dates or numbers. Use `Intl` — it's built-in and locale-aware.

---

## 7. RTL support

Use CSS logical properties, not left/right:

```css
.container {
  margin-inline-start: 1rem; /* NOT margin-left */
  padding-inline-end: 1rem; /* NOT padding-right */
  border-inline-start: 1px solid; /* NOT border-left */
}

[dir='rtl'] .icon {
  transform: scaleX(-1);
}
```

Set `<html dir="rtl">` or `<html dir="ltr">` based on locale. Tailwind v4 supports logical properties natively (`ms-4` = `margin-inline-start`).

---

## 8. Best practices

### DO ✅

- Translation keys, never raw text in components
- Namespace by feature (not by screen — screens change)
- Support pluralization via ICU
- Use `Intl` for dates/numbers
- Plan for RTL from day one (CSS logical properties)
- Configure a fallback language (usually `en`)

### DON'T ❌

- Hardcode strings in components
- Concatenate translated strings (`t('hello') + ' ' + name` → use ICU `{name}` interpolation)
- Assume text length (German is ~30% longer than English; layouts must flex)
- Forget RTL layout for Arabic / Hebrew locales
- Mix multiple languages in the same JSON file

---

## 9. Common issues + solutions

| Issue               | Solution                                         |
| ------------------- | ------------------------------------------------ |
| Missing translation | Fallback to default language                     |
| Hardcoded strings   | Linter / CI check (e.g. `eslint-plugin-i18next`) |
| Date format         | `Intl.DateTimeFormat`                            |
| Number format       | `Intl.NumberFormat`                              |
| Pluralization       | ICU MessageFormat                                |
| Text overflow       | Flex layouts + truncation fallback               |

---

## 10. Pre-ship checklist

- [ ] All user-facing strings use translation keys
- [ ] Locale files exist for all supported languages
- [ ] Date/number formatting uses `Intl` API
- [ ] RTL layout tested (if applicable)
- [ ] Fallback language configured
- [ ] No hardcoded strings in components (verify via linter)
- [ ] Pluralization uses ICU (not string concatenation)
- [ ] Dynamic text boundaries flex for +30% length

---

## 11. Anti-patterns

| ❌ Don't                                         | ✅ Do                                     |
| ------------------------------------------------ | ----------------------------------------- |
| `<h1>Welcome</h1>`                               | `<h1>{t('welcome')}</h1>`                 |
| `t('msg') + ' ' + name`                          | `t('msg', { name })` with ICU placeholder |
| `new Date().toLocaleDateString()` without locale | `Intl.DateTimeFormat(locale, ...)`        |
| `margin-left: 1rem`                              | `margin-inline-start: 1rem`               |
| Screen-based namespaces                          | Feature-based namespaces                  |
| Ship without fallback                            | Configure fallback language               |

---

_Cross-reference: `kb-flutter §10` for Flutter ARB localization. `kb-design-system` for how tokens + RTL interact._
