---
name: backlink-monitoring
description: >
  Analyses outbound links for dofollow/nofollow strategy, domain diversity, anchor text
  quality, and sponsored/UGC attributes. Use when auditing link profiles or optimising
  outbound linking strategy.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Backlink Monitoring

Analyse outbound links on the page for SEO link strategy.

> **Note**: This skill owns **external/outbound link analysis**. For internal link counts and structure, see the [onpage-optimization](../onpage-optimization/SKILL.md) skill.

## 1. Identify external links

For each `<a href="...">` element:
- **External**: `href` starts with `http://` or `https://`
- Classify as **dofollow** (default) or **nofollow** (if `rel` contains `nofollow`)

Report: ✅ PASS "Found N external link(s): X dofollow, Y nofollow"

## 2. Nofollow strategy

| Condition | Status |
|---|---|
| All external links are dofollow, none nofollow | ⚠️ WARN "Consider adding `rel=nofollow` to untrusted or sponsored links" |
| Mix of dofollow and nofollow | ✅ PASS (healthy strategy) |

## 3. Sponsored and UGC attributes

- Links with `rel="sponsored"` → ✅ PASS "N link(s) properly marked as sponsored"
- Links with `rel="ugc"` → ✅ PASS "N link(s) marked as UGC (user-generated content)"

## 4. Anchor text quality

- External links with empty anchor text (and no child `<img>`) → ⚠️ WARN "Descriptive anchor text improves SEO"

## 5. Domain diversity

- Extract unique hostnames from all external link `href` values
- Report: ✅ PASS "Links point to N unique domain(s): [list domains]"

## 6. No external links

- If zero external links found → ⚠️ WARN "Linking to authoritative sources can boost SEO credibility"

## Best practices to suggest

- Use `rel="nofollow"` for untrusted, paid, or user-submitted links
- Use `rel="sponsored"` for paid/advertising links
- Use `rel="ugc"` for user-generated content (comments, forums)
- Write descriptive anchor text — avoid "click here" or empty links
- Link to authoritative, relevant external sources
- Maintain domain diversity — don't link excessively to one domain

## Edge cases

- Ignore `javascript:`, `mailto:`, and `tel:` hrefs — these are not external links
- Links with multiple `rel` values (e.g. `rel="nofollow sponsored"`) — check each value separately
- Links inside `<template>`, `<noscript>`, or hidden elements should still be audited but noted as potentially inactive
- Social media share buttons (Twitter, Facebook intents) are external but should not trigger nofollow warnings
- CDN links (e.g. `cdn.jsdelivr.net`, `fonts.googleapis.com`) are resource links, not editorial — exclude from domain diversity count
