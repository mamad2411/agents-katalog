---
name: meta-data-optimization
description: >
  Validates title tags, meta descriptions, Open Graph tags, and Twitter Cards.
  Use when auditing or fixing meta data for search engine and social media optimisation.
  For canonical URLs and robots directives, see the technical-seo skill.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Meta Data Optimization

Audit title, description, Open Graph, and Twitter Card meta tags.

> **Note**: Canonical URLs, robots directives, and indexability checks are handled by the [technical-seo](../technical-seo/SKILL.md) skill. Do not duplicate those checks here.

## 1. Title tag

| Check | Rule | Status |
|---|---|---|
| Missing `<title>` | Critical for SEO | ❌ FAIL |
| Title < 30 characters | Too short | ⚠️ WARN |
| Title > 60 characters | May be truncated in SERPs | ⚠️ WARN |
| Title 30–60 characters | Optimal length | ✅ PASS |
| Title is ALL CAPS (and > 5 chars) | Perceived as spammy | ⚠️ WARN |

### Title quality checks

- **Keyword at start** (position 0): ✅ PASS "Best placement"
- **Keyword near start** (position ≤ 20): ✅ PASS
- **Keyword late** (position > 20): ⚠️ WARN "Place keyword earlier"
- **Separator present** (`|`, `-`, `–`, `—`, `:`): ✅ PASS "Good brand + keyword pattern"
- **Power words** (best, guide, ultimate, how to, tips, review, top, free, new, proven): ✅ PASS "May improve CTR"
- **Contains number**: ✅ PASS "Numbers in titles can boost CTR"

## 2. Meta description

| Check | Rule | Status |
|---|---|---|
| Missing `<meta name="description">` | Needs one for SERP snippets | ❌ FAIL |
| Description < 120 characters | Too short | ⚠️ WARN |
| Description > 160 characters | May be truncated | ⚠️ WARN |
| Description 120–160 characters | Optimal | ✅ PASS |

## 3. Character encoding

| Check | Status |
|---|---|
| `<meta charset="utf-8">` or `<meta http-equiv="Content-Type">` present | ✅ PASS |
| Neither present | ⚠️ WARN "Add charset meta tag" |

## 4. Open Graph tags

Check for these required OG tags:

| Tag | Missing = |
|---|---|
| `og:title` | ⚠️ WARN |
| `og:description` | ⚠️ WARN |
| `og:image` | ⚠️ WARN |
| `og:url` | ⚠️ WARN |
| `og:type` | ⚠️ WARN |

- All present → ✅ PASS "All required Open Graph tags present"
- All missing → ❌ FAIL "No Open Graph tags found — social sharing will use defaults"

### OG image dimensions

If `og:image` exists, check for `og:image:width` and `og:image:height`:
- Both present → ✅ PASS
- Missing → ⚠️ WARN "Missing og:image:width / og:image:height"

## 5. Twitter Card tags

Check for these required tags:

| Tag | Missing = |
|---|---|
| `twitter:card` | ⚠️ WARN |
| `twitter:title` | ⚠️ WARN |
| `twitter:description` | ⚠️ WARN |

- All present → ✅ PASS
- All missing → ⚠️ WARN "No Twitter Card tags found"

Note: Twitter tags can be in either `<meta name="twitter:*">` or `<meta property="twitter:*">` format.

## Edge cases

- Next.js generates `<title>` and meta tags via the `metadata` export or `generateMetadata()` — audit the rendered HTML, not the source code
- Some sites use `<meta property="title">` instead of `<title>` — flag as ⚠️ WARN "Use standard `<title>` tag"
- Duplicate `<title>` tags in the document → ❌ FAIL "Only one `<title>` allowed"
- If OG tags exist but `<title>` / `<meta description>` are missing, flag both — OG tags do not substitute for standard meta tags
- Twitter falls back to OG tags when `twitter:*` tags are absent — note this but still recommend explicit Twitter tags for full control
