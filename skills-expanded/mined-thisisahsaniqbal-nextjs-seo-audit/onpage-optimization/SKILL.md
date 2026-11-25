---
name: onpage-optimization
description: >
  Validates heading hierarchy, keyword density and placement, and internal/external link
  structure. Use when auditing on-page SEO factors for an HTML page.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# On-Page Optimization

Analyse the HTML page for heading structure, keyword usage, and link health.

> **Note**: This skill owns **internal link analysis**. For external/outbound link strategy (dofollow/nofollow, anchor text quality, domain diversity), see the [backlink-monitoring](../backlink-monitoring/SKILL.md) skill.

## 1. Heading validation

Check all `<h1>` through `<h6>` elements:

| Check | Status | Rule |
|---|---|---|
| No headings at all | ❌ FAIL | Every page must have at least one heading |
| No `<h1>` tag | ❌ FAIL | Every page must have exactly one `<h1>` |
| Multiple `<h1>` tags | ⚠️ WARN | Recommend a single `<h1>` per page |
| Hierarchy skipped (e.g. H2 → H4) | ⚠️ WARN | Headings should follow sequential order: H1 → H2 → H3 |
| Empty heading (no text content) | ❌ FAIL | All headings must have descriptive text |
| Single H1, proper hierarchy | ✅ PASS | Heading structure is correct |

## 2. Keyword analysis

If a target keyword is provided, check its usage across the page:

### Keyword density

- Calculate: `(keyword_count / total_words) × 100`
- **Ideal range**: 1.0–3.0%
- Below 1.0% → ⚠️ WARN "Keyword density is low"
- Above 3.0% → ❌ FAIL "Keyword stuffing detected"
- Within range → ✅ PASS

### Keyword placement — check all of these:

| Location | How to check | Missing = |
|---|---|---|
| `<title>` tag | Does the title contain the keyword? | ⚠️ WARN |
| `<h1>` tag | Does the H1 text contain the keyword? | ⚠️ WARN |
| Meta description | Does `<meta name="description">` contain the keyword? | ⚠️ WARN |
| First `<p>` tag | Does the first paragraph contain the keyword? | ⚠️ WARN |
| Image alt text | Does any `<img alt="...">` contain the keyword? | ⚠️ WARN |

### Title keyword position

- Keyword at position 0 (start of title) → ✅ PASS "Best placement"
- Keyword at position ≤ 20 → ✅ PASS "Near the start"
- Keyword at position > 20 → ⚠️ WARN "Place it earlier for better ranking"

## 3. Link analysis

Examine all `<a href="...">` elements:

### Classify links

- **Internal**: `href` starts with `/`, `./`, `../`, or `#`
- **External**: `href` starts with `http://` or `https://`

### Checks

| Check | Threshold | Status |
|---|---|---|
| Internal link count ≥ 3 | Minimum 3 per page | ⚠️ WARN if below |
| Links with no anchor text (and no child `<img>`) | Any count > 0 | ⚠️ WARN |
| Internal links with `rel="nofollow"` | Any count > 0 | ⚠️ WARN "Prevents PageRank flow within your site" |

Always report the count of internal and external links found.

## Edge cases

- If no keyword is supplied, skip keyword analysis and note: "No target keyword supplied — skipping keyword analysis"
- Count words by splitting text on whitespace; keyword matching is case-insensitive
- For link classification, ignore `javascript:`, `mailto:`, and `tel:` hrefs
- Single-page applications (SPAs) with hash-based routing (`#/page`) — treat `#`-prefixed hrefs as internal links
- Next.js `<Link>` components render as standard `<a>` tags in HTML output — audit the rendered HTML, not the JSX
- Pages with zero links (e.g. legal/privacy pages) should receive ⚠️ WARN, not ❌ FAIL
