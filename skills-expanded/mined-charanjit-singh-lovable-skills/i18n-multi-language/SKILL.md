---
name: i18n-multi-language
description: >-
  Use when adding multi-language support, translations, locale switching,
  date/number formatting, or RTL layout. Not for single-language apps unless
  preparing for i18n later.
---

# i18n multi-language

Use **i18next** (`react-i18next`) for strings; **`Intl`** for dates, numbers, and currency.

## Setup

```
src/
  i18n/
    index.ts            # i18next init
    locales/
      en/common.json
      es/common.json
```

```ts
// src/i18n/index.ts
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./locales/en/common.json";
import es from "./locales/es/common.json";

i18n.use(initReactI18next).init({
  resources: { en: { common: en }, es: { common: es } },
  lng: localStorage.getItem("lang") ?? navigator.language.split("-")[0] ?? "en",
  fallbackLng: "en",
  defaultNS: "common",
  interpolation: { escapeValue: false },
});
```

## Usage

```tsx
const { t } = useTranslation();
<h1>{t("dashboard.title")}</h1>
<p>{t("welcome", { name: user.name })}</p>
```

JSON:

```json
{
  "dashboard": { "title": "Dashboard" },
  "welcome": "Welcome, {{name}}"
}
```

## Pluralization

```json
{ "items_one": "{{count}} item", "items_other": "{{count}} items" }
```

```ts
t("items", { count });
```

## Dates, numbers, currency — use `Intl`

```ts
new Intl.DateTimeFormat(locale, { dateStyle: "medium" }).format(date);
new Intl.NumberFormat(locale, { style: "currency", currency: "USD" }).format(amount / 100);
new Intl.RelativeTimeFormat(locale, { numeric: "auto" }).format(-3, "day");
```

Never concatenate `"$" + amount` or hand-format dates.

## Locale switcher

- Persist the chosen locale (user profile or localStorage).
- Set `<html lang={locale}>` and (if RTL) `dir="rtl"`.

## RTL support

- Use Tailwind logical properties (`ps-4` / `pe-4` instead of `pl-4` / `pr-4`).
- Test layout in Arabic/Hebrew at least once.

## DB content

For user-generated multi-language content, store one row per locale or a JSON column keyed by locale code. Do not concat languages into one column.

## Avoid

- Hardcoded strings in JSX once i18n is enabled — every visible string goes through `t()`.
- Concatenating translated fragments (`t("welcome") + " " + name`) — use interpolation.
- Translating error codes — translate user-facing messages, not stable `error` slugs.
- Shipping with a single language but i18next scaffolding that nobody owns — pick a path.

## Checklist

- [ ] All visible copy uses `t()`.
- [ ] `Intl` for dates / numbers / currency.
- [ ] `<html lang>` reflects current locale.
- [ ] RTL tested if supporting Arabic/Hebrew.
