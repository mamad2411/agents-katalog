---
name: semantic-layout
description: >
  Validates HTML5 semantic elements, ARIA landmarks, skip navigation, and page structure.
  Use when auditing semantic HTML, accessibility, or content structure for SEO.
  For the lang attribute, see the international-seo skill.
license: MIT
metadata:
  author: Muhammad Ahsan Iqbal (https://muhammadahsaniqbal.com)
  linkedin: https://www.linkedin.com/in/ahsan-iqbal-digitalmarketingexpert/
  version: "1.0"
---

# Semantic Layout

Audit the page for proper use of HTML5 semantic elements and accessibility.

> **Note**: The `lang` attribute check is handled by the [international-seo](../international-seo/SKILL.md) skill. Do not duplicate it here.

## 1. Required semantic elements

These elements **must** be present:

| Element | Missing = |
|---|---|
| `<header>` | ❌ FAIL |
| `<main>` | ❌ FAIL |
| `<footer>` | ❌ FAIL |
| `<nav>` | ❌ FAIL |

Report count if present: ✅ PASS "`<tag>` element found (N instance(s))"

## 2. Recommended semantic elements

These elements **should** be present:

| Element | Missing = |
|---|---|
| `<article>` | ⚠️ WARN "Consider using for content structure" |
| `<section>` | ⚠️ WARN |
| `<aside>` | ⚠️ WARN |
| `<figure>` | ⚠️ WARN |

## 3. Skip-navigation link

Check for accessibility skip links: `<a href="#main-content">`, `<a href="#content">`, or `<a href="#main">`

- Found → ✅ PASS
- Missing → ⚠️ WARN "Add skip-navigation link for accessibility"

## 4. Div-soup detection

Count `<div>` elements vs semantic elements (`header`, `main`, `footer`, `nav`, `article`, `section`, `aside`, `figure`):

| Condition | Status |
|---|---|
| Divs > 0 but zero semantic elements | ❌ FAIL "Restructure with semantic HTML" |
| Divs > 5× semantic element count | ⚠️ WARN "High div-to-semantic ratio" |

## 5. ARIA landmark roles

Check for these roles: `banner`, `navigation`, `main`, `contentinfo`, `search`

- Any found → ✅ PASS — list which roles are present

## 6. Layout suggestions

### Single `<main>`
- 0 `<main>` elements → ⚠️ WARN "Wrap primary content in `<main>`"
- Multiple `<main>` → ⚠️ WARN "Should have only one"

### Headings inside semantic containers
- Count `<h2>`, `<h3>`, `<h4>` that are NOT inside `<section>`, `<article>`, `<aside>`, or `<main>`
- If any found → ⚠️ WARN "Wrap content blocks in `<section>` or `<article>`"

### Images without `<figure>`
- If > 3 images not wrapped in `<figure>` → ⚠️ WARN "Use `<figure>`/`<figcaption>`"

### Date markup
- If `<time>` elements found → ✅ PASS
- If date patterns found in text but no `<time>` elements → ⚠️ WARN "Wrap dates in `<time datetime=\"...\">`"

### List elements
- No `<ul>` or `<ol>` found → ⚠️ WARN "Use lists for list-type content (improves featured snippet eligibility)"

### Tables without captions
- Tables missing `<caption>` → ⚠️ WARN "Add captions for accessibility"

## Edge cases

- Next.js and React apps render into a root `<div id="__next">` or `<div id="root">` — this does not count as "div-soup"; evaluate the semantic elements inside it
- Server-rendered HTML may differ from client-rendered HTML — audit the initial SSR output when possible
- Components rendered inside `<template>` or `<slot>` elements are not visible in static HTML — note this limitation
- Email-style pages (e.g. unsubscribe pages) may legitimately lack `<article>`, `<section>`, or `<aside>` — do not flag as WARN
- If a page uses Web Components or Shadow DOM, semantic elements inside the shadow tree may not be visible — note as limitation
