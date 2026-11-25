---
name: international-seo
description: Implements and validates multilingual/multi-regional setup including hreflang. Use when launching locales or fixing wrong-language/region landing.
---

# International SEO

## Overview

Tell Google about language/region variants clearly and consistently.

## When to Use

- hreflang errors, locale subfolders/domains, regional targeting

**Not for:** Translation quality alone without URL/locale signals.

## Official sources

- https://developers.google.com/search/docs/specialty/international
- https://developers.google.com/search/docs/specialty/international/localized-versions

## Process

1. Map language-region → URL for each variant.
2. Add bidirectional `hreflang` annotations (HTML, HTTP headers, or sitemap).
3. Include `x-default` when a sensible default/chooser URL exists — treat absence as a **review signal**, not an automatic failure.
4. Ensure each locale page is self-canonical and returns 200.
5. Run `python skills/international-seo/scripts/hreflang_audit.py <url-or-file>`.
6. Avoid automatic redirection solely by IP that blocks locale choice.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "One language is enough; skip hreflang." | Without annotations, Google may show the wrong locale in Search. |
| "Missing x-default always fails." | Flag it for review; add x-default when you have a default/chooser URL. |
| "Auto-redirect by IP is fine." | It can block users (and crawlers) from choosing a locale — avoid hard IP-only locks. |

## Red Flags

- One-way hreflang (A→B without B→A)
- Locale URLs that 404 or canonicalize to another language
- Inventing geo-targeting rules not in Search Central

## Verification

- [ ] Locale map documented
- [ ] hreflang entries reciprocal or gaps listed
- [ ] `missing_x_default` reviewed (add or accept with rationale)
- [ ] Script JSON or manual table captured
