---
name: i18n
description: Internationalize and localize user interfaces, APIs, documents, and formatting. Use for multilingual apps, locale-sensitive dates, numbers, currency, pluralization, translation keys, lang/dir attributes, RTL layouts, and avoiding hardcoded text.
---

# I18n

## Workflow

1. Identify target locales and fallback locale.
2. Externalize user-facing strings into the project's existing i18n system.
3. Use locale-aware formatting for dates, times, numbers, currency, units, and lists.
4. Handle pluralization and interpolation through i18n APIs.
5. Set `lang` and `dir` correctly for document or region when relevant.
6. Check layout for long translations and RTL if applicable.

## Rules

- Do not concatenate translated fragments when grammar may vary.
- Do not hardcode date, number, currency, or timezone formatting.
- Keep translation keys stable and meaningful.
- Avoid embedding HTML in translations unless the project has a safe pattern.

## Output

Report changed strings, formatting behavior, fallback behavior, and RTL or length risks.
