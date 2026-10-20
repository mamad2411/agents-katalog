---
name: skill-localization
description: Internationalization (i18n) and localization (l10n) strategy, string externalization, plural and gender handling, right-to-left text support, cultural adaptation, translation workflow, locale-specific testing. Use when adding multi-language support, managing translations, or expanding to new locales.
version: 1.0.0
---

# Skill: Localization (i18n/l10n)

String externalization + translation workflow + cultural adaptation = global product.

## String Externalization

**Don't embed strings in code**:
```python
# ✗ Bad
message = "Hello, " + user.name

# ✓ Good (externalizable)
message = t("greeting", name=user.name)
```

## Translation File Format

```yaml
# locales/en.yaml
greeting: "Hello, {name}"
hello_world: "Hello, World!"

# locales/es.yaml
greeting: "Hola, {name}"
hello_world: "¡Hola, Mundo!"

# locales/fr.yaml
greeting: "Bonjour, {name}"
hello_world: "Bonjour, le monde!"
```

## Pluralization

```
messages:
  en:
    item_count:
      one: "You have 1 item"
      other: "You have {count} items"
  es:
    item_count:
      one: "Tienes 1 artículo"
      other: "Tienes {count} artículos"
```

## Right-to-Left (RTL) Support

```html
<!-- Auto-detect -->
<html dir="auto">
  ...
</html>

<!-- or explicit -->
<html lang="ar" dir="rtl">
  <!-- Arabic content -->
</html>

<!-- CSS -->
body {
  direction: rtl;
  text-align: right;
}
```

## Dates & Times

```
en-US: 01/15/2024
en-GB: 15/01/2024
de-DE: 15.01.2024
```

Use locale-aware formatting:
```python
from babel.dates import format_date
format_date(date, format='medium', locale='de_DE')
```

## Translation Workflow

1. **Extract**: Find translatable strings
2. **Upload**: To translation platform (Crowdin, Transifex)
3. **Translate**: Humans + review
4. **Download**: Translated files
5. **Test**: Each locale
6. **Deploy**: With fallback to English

---

**Status**: Ready for localization work  
**Best for**: i18n implementation, translation management, global expansion
