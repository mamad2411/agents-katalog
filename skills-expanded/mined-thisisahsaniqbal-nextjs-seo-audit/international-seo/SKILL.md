---
name: international-seo
description: >
  Validates hreflang tags, multi-language configuration, regional targeting, and
  internationalisation best practices. Use when auditing sites with multiple languages,
  regions, or localised content.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# International SEO

Audit the page for multi-language and regional targeting issues.

> **When to activate**: Only relevant if the site serves multiple languages, regions, or has localised content. If a page is monolingual with no internationalisation signals, report ✅ PASS "No internationalisation issues (single-language site)".

## 1. Hreflang tags

Look for `<link rel="alternate" hreflang="...">` in `<head>`:

| Check | Status |
|---|---|
| No hreflang tags on a multi-language site | ❌ FAIL "Add hreflang tags to indicate language/region variants" |
| Hreflang tags present | ✅ PASS — list all language-region codes found |

### Hreflang validation rules

| Rule | Violation = |
|---|---|
| Self-referencing hreflang missing (page must include itself) | ❌ FAIL |
| `x-default` fallback missing | ⚠️ WARN "Add `hreflang=\"x-default\"` for the default/fallback page" |
| Invalid language code (must be ISO 639-1, e.g. `en`, `fr`, `de`) | ❌ FAIL |
| Invalid region code (must be ISO 3166-1 alpha-2, e.g. `en-US`, `fr-CA`) | ⚠️ WARN |
| Hreflang URLs return 4xx or 5xx | ❌ FAIL "Hreflang points to broken URL" |
| Duplicate hreflang entries for same language-region | ⚠️ WARN |

## 2. HTML lang attribute

| Check | Status |
|---|---|
| `<html lang="...">` missing | ❌ FAIL |
| `lang` value doesn't match hreflang self-reference | ⚠️ WARN "Mismatch between html lang and hreflang" |
| Properly set | ✅ PASS |

## 3. Content-Language header (meta)

- `<meta http-equiv="Content-Language" content="...">` → check if present
- If present, verify it matches the `lang` attribute → ⚠️ WARN if mismatch

## 4. URL structure for internationalisation

Detect URL pattern used:

| Pattern | Example | Assessment |
|---|---|---|
| Subdirectory | `/en/`, `/fr/`, `/de/` | ✅ Recommended |
| Subdomain | `en.example.com` | ✅ Acceptable |
| ccTLD | `example.fr`, `example.de` | ✅ Strong geo-targeting |
| URL parameter | `?lang=en` | ⚠️ WARN "Not recommended — search engines may ignore parameters" |

## 5. Translated content checks

| Check | Status |
|---|---|
| Page has `lang="en"` but content appears in another language | ⚠️ WARN "Language mismatch detected" |
| `<title>` and `<meta description>` not translated (same across language variants) | ⚠️ WARN |
| Images with alt text not translated | ⚠️ WARN |

## 6. Regional targeting

- Check for `<meta name="geo.region">`, `<meta name="geo.placename">`, `<meta name="geo.position">` → ✅ PASS if present
- Google Search Console geographic targeting hint: check for `<link rel="canonical">` pointing to regional variant

## Edge cases

- A monolingual site with no internationalisation signals → skip all checks, report "Not applicable"
- A site with `hreflang` on some pages but not others → flag inconsistency
- Right-to-left languages (Arabic, Hebrew) → check for `dir="rtl"` attribute on `<html>` or `<body>`
