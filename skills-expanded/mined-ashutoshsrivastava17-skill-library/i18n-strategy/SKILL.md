---
name: i18n-strategy
description: >
  Plan internationalization — string extraction, locale management, RTL support,
  date/number formatting, pluralization, and translation workflows.
  TRIGGER when: user says /i18n-strategy, needs to internationalize an application,
  or asks about localization, translation, or multi-language support.
argument-hint: "[application or feature to internationalize]"
user-invocable: true
---

# Internationalization Strategy

You are a software engineer specializing in i18n/l10n. Plan a comprehensive internationalization strategy.

## Process

### Step 1: Assess Scope

| Element | Questions |
|---------|----------|
| Target locales | Which languages/regions? (e.g., en-US, fr-FR, ja-JP, ar-SA) |
| Content types | UI strings, emails, docs, legal, marketing? |
| Current state | Any existing i18n? Hardcoded strings? |
| RTL support | Arabic, Hebrew, or other RTL languages needed? |
| Timeline | All locales at once or phased? |

### Step 2: Design String Management

| Practice | Details |
|----------|---------|
| Externalization | All user-facing strings in resource files, never hardcoded |
| Key naming | Hierarchical: `page.section.element` (e.g., `settings.profile.title`) |
| Pluralization | Use ICU MessageFormat for plural rules (not if/else) |
| Interpolation | `"Hello, {name}"` — never concatenate translated strings |
| Context | Provide translator notes for ambiguous strings |
| No string reuse | Same English word can translate differently in context |

**String file format:**
```json
{
  "settings.profile.title": "Profile Settings",
  "orders.count": "{count, plural, one {# order} other {# orders}}",
  "welcome.greeting": "Hello, {name}!"
}
```

### Step 3: Handle Formatting

| Type | Approach | Example |
|------|---------|---------|
| Dates | `Intl.DateTimeFormat` / locale-aware library | 03/15/2025 (US) vs 15/03/2025 (EU) |
| Numbers | `Intl.NumberFormat` | 1,000.50 (US) vs 1.000,50 (DE) |
| Currency | Currency code + locale formatting | $1,000 vs 1.000 € |
| Time zones | Store UTC, display in user's timezone | — |
| Addresses | Locale-specific format templates | — |
| Phone numbers | E.164 storage, locale-specific display | — |

### Step 4: Plan RTL Support

| Concern | Solution |
|---------|---------|
| Text direction | `dir="rtl"` attribute, CSS `direction` property |
| Layout mirroring | Use CSS logical properties (`margin-inline-start` not `margin-left`) |
| Icons | Mirror directional icons (arrows, progress bars) |
| Bidirectional text | Handle mixed LTR/RTL content (usernames, code) |
| Testing | Visual regression tests with RTL locale |

### Step 5: Design Translation Workflow

| Phase | Activity | Tools |
|-------|----------|-------|
| Extract | Pull new/changed strings from code | i18n CLI tool |
| Export | Send strings to translators (XLIFF, JSON) | Crowdin, Phrase, Lokalise |
| Translate | Professional translation or community | TMS platform |
| Review | Native speaker QA | In-context review tool |
| Import | Merge translations back to codebase | CI automation |
| Validate | Check completeness, placeholders, length | Automated checks |

### Step 6: Test and Validate

| Test | Method |
|------|--------|
| Pseudo-localization | Replace strings with accented versions (Ĥëľľö) to catch hardcoded text |
| String expansion | Verify UI handles 30-40% longer text (German, Finnish) |
| RTL layout | Visual check all pages in RTL locale |
| Placeholder validation | All `{variables}` present in translations |
| Missing translations | CI check for untranslated strings |
| Screenshot testing | Visual regression per locale |

## Output Format

```markdown
## i18n Strategy: [Application]

### Locales: [Supported languages and regions]
### String Management: [Format, naming, tooling]
### Formatting: [Date, number, currency approach]
### RTL: [Support plan if applicable]
### Translation Workflow: [Process and tools]
### Testing: [Validation approach]
```

## Quality Checklist

- [ ] All user-facing strings externalized
- [ ] Pluralization uses ICU MessageFormat
- [ ] Dates, numbers, and currency use locale-aware formatting
- [ ] RTL support implemented (if applicable)
- [ ] Translation workflow is automated
- [ ] Pseudo-localization catches hardcoded strings
- [ ] String expansion tested for long translations

## Edge Cases

- For user-generated content, don't translate — but handle display direction
- For legal/compliance text, use professional translators (never machine translation)
- If adding i18n to an existing app, extract strings incrementally by feature area
- For email templates, internationalize subject lines and body separately
- For SEO, implement hreflang tags and locale-specific URLs
