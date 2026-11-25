---
name: canon-meta-og
description: Use when implementing Open Graph tags, Twitter Card tags, and social sharing metadata — the tags that control how URLs appear when shared on social media, messaging apps, and link previews. Trigger when the user mentions OG tags, Open Graph, Twitter card, social sharing, link preview, or og:image.
---

# CANON · Meta / Open Graph

When someone shares your URL on Slack, Twitter, LinkedIn, iMessage, or WhatsApp, these tags control what they see. Without them, the preview is a bare URL or a random scraped snippet.

## Essential Open Graph tags

```html
<meta property="og:title" content="Page Title">
<meta property="og:description" content="Concise summary of the page.">
<meta property="og:image" content="https://example.com/og-image.png">
<meta property="og:url" content="https://example.com/page">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Site Name">
```

## Twitter Card tags

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Page Title">
<meta name="twitter:description" content="Concise summary.">
<meta name="twitter:image" content="https://example.com/og-image.png">
```

`summary_large_image` shows a large preview. `summary` shows a small thumbnail. Large image gets more clicks.

## OG image spec

| Property | Value |
|---|---|
| Recommended size | 1200×630px |
| Minimum size | 600×315px |
| Format | PNG or JPEG (PNG for text-heavy, JPEG for photos) |
| File size | ≤ 1MB (smaller is better for fast preview) |
| Text safety zone | Keep text 60px from edges (platforms crop differently) |

Every page should have a unique og:image. Fallback to a site-wide default if page-specific isn't available.

## Dynamic OG images

For pages with user-generated content (blog posts, profiles), generate OG images dynamically:

```
https://example.com/api/og?title=My+Post&author=Deep
```

Use `@vercel/og`, Satori, or Puppeteer to render HTML → image server-side.

## Validation tools

- Facebook: `https://developers.facebook.com/tools/debug/`
- Twitter: `https://cards-dev.twitter.com/validator`
- LinkedIn: `https://www.linkedin.com/post-inspector/`
- Open Graph debugger: `https://www.opengraph.xyz/`

Test after every change — platforms cache aggressively.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| No og:image | Preview is text-only, low engagement |
| Same og:image for every page | Every share looks identical |
| og:image with text cut off at edges | Platforms crop differently |
| og:title longer than 60 characters | Truncated in most previews |
| HTTP (not HTTPS) og:image URL | Some platforms reject it |
| Missing og:url (or wrong URL) | Canonical confusion |

## Audit checklist

- [ ] `og:title`, `og:description`, `og:image`, `og:url` on every page
- [ ] `twitter:card` = `summary_large_image`
- [ ] OG image 1200×630px, ≤ 1MB
- [ ] Text in OG image within safe zone (60px margins)
- [ ] Unique og:image per page (or dynamic generation)
- [ ] Validated with Facebook debugger
- [ ] HTTPS URLs for all meta content

## Sources

- Open Graph Protocol · ogp.me
- Twitter · Cards documentation
- Facebook · Sharing best practices
