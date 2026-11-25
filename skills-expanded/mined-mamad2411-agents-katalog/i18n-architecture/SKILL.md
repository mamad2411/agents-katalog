---
name: i18n-architecture
version: 1.0.0
min_mindforge_version: 0.3.0
status: stable
triggers: i18n architecture, message catalog, pluralization rule, ICU message format, RTL layout, locale detection, translation loading, internationalization setup, language fallback, number formatting, date locale, translation management
---

# Skill — Internationalization Architecture

## When this skill activates
Any task involving multi-language support, locale handling, message catalogs,
RTL layouts, number/date formatting, or translation infrastructure.

## Mandatory actions when this skill is active

### Before implementing i18n
1. Audit all user-facing strings in the codebase.
2. Define the locale detection strategy.
3. Choose a message format that handles plurals and gender.

### Message format (ICU MessageFormat)

**Why ICU:**
- Handles plurals correctly across languages (some have 6 plural forms).
- Handles gender agreement.
- Handles select/choice patterns.
- Industry standard supported by most i18n libraries.

**Examples:**
```
{count, plural,
  =0 {No items}
  one {# item}
  other {# items}
}

{gender, select,
  male {He liked your post}
  female {She liked your post}
  other {They liked your post}
}
```

**Critical rule:** NEVER concatenate strings for messages.
- BAD: `"Hello " + name + ", you have " + count + " messages"`
- GOOD: `"Hello {name}, you have {count, plural, one {# message} other {# messages}}"`

### Catalog structure

**One file per locale, namespaced by feature:**
```
locales/
  en/
    common.json
    auth.json
    dashboard.json
  fr/
    common.json
    auth.json
    dashboard.json
```

**Rules:**
- Keys are semantic, not the English text (`auth.loginButton` not `"Log in"`).
- Flat keys with dot notation or nested objects — pick one, be consistent.
- Never store HTML in translation strings (use interpolation components).
- Keep a "base" locale (usually en) as the source of truth.

### Loading strategy

**Lazy-load per route/namespace:**
- Do NOT load all locales upfront — only the active locale.
- Do NOT load all namespaces — only what the current route needs.
- Prefetch the next likely namespace on navigation intent.

**Implementation:**
```javascript
// Load only when needed
const messages = await import(`./locales/${locale}/${namespace}.json`);
```

**Fallback chain:**
- Specific locale (fr-CA) → base locale (fr) → default locale (en).
- Missing key in active locale → fall back, log warning in development.

### Locale detection

**Priority order:**
1. User explicit preference (stored in profile/cookie).
2. Accept-Language header (server-side).
3. Navigator.language (client-side).
4. Geo-IP lookup (least reliable).
5. Default locale (en).

**Rules:**
- Let users override detected locale at any time.
- Persist user choice across sessions.
- URL strategy: subdomain (fr.app.com) or path prefix (/fr/dashboard).

### RTL layout support

**CSS logical properties (mandatory):**
- Use `margin-inline-start` not `margin-left`.
- Use `padding-inline-end` not `padding-right`.
- Use `inset-inline-start` not `left`.
- Use `border-inline-start` not `border-left`.

**HTML:**
- Set `dir="rtl"` on the `<html>` element based on locale.
- Use `dir="auto"` on user-generated content.

**Icons and images:**
- Mirror directional icons (arrows, progress indicators) in RTL.
- Do NOT mirror: logos, clocks, phone icons, checkmarks.

### Number and date formatting

**Always use Intl APIs:**
```javascript
// Numbers
new Intl.NumberFormat(locale, { style: 'currency', currency: 'USD' }).format(amount);

// Dates
new Intl.DateTimeFormat(locale, { dateStyle: 'long', timeStyle: 'short' }).format(date);

// Relative time
new Intl.RelativeTimeFormat(locale, { numeric: 'auto' }).format(-1, 'day');
```

**Rules:**
- Never manually format numbers or dates with string templates.
- Store dates in UTC, display in user's timezone.
- Currency display must respect locale (symbol position, separator).

### Translation management

- Use a translation management system (Crowdin, Lokalise, Phrase) for professional translations.
- Extract new keys automatically from code (i18next-parser, formatjs extract).
- CI check: fail if base locale has keys missing from other locales.
- Pseudo-localization in development to catch hardcoded strings and layout overflow.

## Self-check before task completion
- [ ] Did I follow the mandatory actions for this skill?
- [ ] Did I apply the patterns appropriate to the context?
- [ ] Did I verify the implementation meets the criteria above?
- [ ] Did I document decisions and trade-offs made?
