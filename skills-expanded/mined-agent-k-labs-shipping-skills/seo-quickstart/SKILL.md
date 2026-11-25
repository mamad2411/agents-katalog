---
name: seo-quickstart
description: Set up minimum viable SEO for a vibe-coded app — technical essentials (meta tags, OG image, sitemap, robots.txt, Search Console), keyword targeting, use-case/comparison/glossary pages, and llms.txt for AI search. Use when the user asks to "add SEO to my app," "set up basic SEO," "how do I rank on Google," "my site isn't showing up in search," or wants the minimum SEO that compounds.
license: MIT
metadata:
  author: agent-k-labs
  version: "1.0"
---

# SEO Quickstart

Most vibe-coded apps ship with zero SEO. This skill gives you the minimum setup that will compound over months — the technical essentials, the one content strategy that works for solo founders, and how to set it up without an SEO expert.

## Context

Read `product-context.md` if present. Also ask for:
1. Product URL and tech stack (Next.js / Webflow / Framer / etc.)
2. Whether the site is live and indexed (check: `site:yourdomain.com` on Google)
3. Monetization model (free / freemium / paid) — affects content strategy priority

## Process

### 1. Technical SEO (do this in one session — 2–4 hours)

If the site is live, first audit the current state:

```bash
bash scripts/audit_page.sh https://yourdomain.com
```

It reports title/description lengths, H1s, OG tags, canonical, robots.txt (including AI crawler rules), sitemap, and llms.txt — fix its 🔴 items using the snippets below. These are the non-negotiables. Each one takes 5–30 minutes.

**Meta tags:**
Every public page needs a unique `<title>` and `<meta name="description">`:
```html
<!-- title: 50–60 characters -->
<title>[Feature/Page] | [ProductName] — [Keyword phrase]</title>

<!-- description: 120–160 characters — this is what appears in Google -->
<meta name="description" content="[Pain or promise in one line]. [ProductName] [does what] for [who]. Free to try.">
```

**OG tags (for sharing on X, LinkedIn, Slack):**
```html
<meta property="og:title" content="..." />
<meta property="og:description" content="..." />
<meta property="og:image" content="https://yourdomain.com/og.png" />
<meta property="og:url" content="https://yourdomain.com" />
```
OG image: 1200×630. Product name + tagline. Simple is fine.

**Canonical URLs:** Every page should have `<link rel="canonical" href="https://yourdomain.com/[path]">`. Prevents duplicate content issues.

**Sitemap:** Create `sitemap.xml` listing all public pages. In Next.js, add a `sitemap.ts` route. Then submit it to Google Search Console.

**robots.txt:** Create a `robots.txt` at your domain root. Minimum:
```
User-agent: *
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml
```
Block: `/api`, `/studio`, `/dashboard`, `/sign-in`, `/sign-up` (anything authenticated or internal).

**Google Search Console:** Add your domain. Verify it. Submit your sitemap. This is how Google discovers your pages. Free, 30 minutes to set up.

**Page speed:** Run your URL through [PageSpeed Insights](https://pagespeed.web.dev/). Fix any red items. Common issues with vibe-coded apps: unoptimized images (use Next.js `<Image>`), no caching headers, large JavaScript bundles.

### 2. Keyword targeting (don't skip this)

SEO without keywords is noise. Pick the right keywords before writing any content.

**The vibe-coder SEO shortcut:**
Your target users are googling one of these three things:
1. The problem: `"how to [do the thing your app does]"`
2. The alternative: `"[competitor name] alternative"` / `"[tool they use] vs [option]"`
3. The category: `"[type of app] for [audience]"` / `"best [tool type] 2026"`

Find 5–10 keywords in each bucket using free tools:
- **Google autocomplete** — type your core phrase and screenshot the suggestions
- **"People also ask"** — the question blocks in Google results
- **Google Search Console** (after 2 weeks) — what queries are you already appearing for?

Prioritize keywords with: lower competition (no big domains on page 1) + clear intent + direct match to your product.

### 3. The minimum viable content strategy

For a solo founder, SEO content is not blog posts — it's **landing pages for specific use cases**.

The highest-ROI SEO pages for a vibe-coded app:

**a) Use-case pages** (one per audience × job-to-be-done):
`/use-cases/[specific-use-case]`

Example: If your app is a time tracker:
- `/use-cases/time-tracking-for-freelancers`
- `/use-cases/billable-hours-tracker`
- `/use-cases/project-time-tracking`

Each page: 400–600 words answering "how do I [use case]" with your product as the answer. See the H1 structure below.

**b) Comparison pages** (one per major alternative):
`/alternatives/[competitor-name]`

These capture high-intent searchers who are already evaluating options. Your app doesn't have to "win" — it just has to be relevant.

**c) Glossary pages** (one per jargon term your users search):
`/glossary/[term]`

These earn long-tail traffic and build topical authority. Easy to generate with AI. Each entry: 200–400 words defining the term and linking to related features.

### 4. On-page structure (template)

For every page you create for SEO:

```
H1: [Primary keyword phrase] — exact match, conversational
H2: [The problem or context]
H2: How [ProductName] solves [problem]
H2: Who this is for
H2: [Feature X] explained
H2: FAQs about [topic]
```

- Page length: 600–1000 words for most use-case pages
- Include: your keyword in H1, first paragraph, one H2, and the URL slug
- Internal links: each page links to 2–3 related pages
- CTA at the bottom: link to sign-up or free trial

### 5. llms.txt (for AI search / GEO)

AI search engines (ChatGPT, Claude, Perplexity) increasingly refer to products by crawling websites. Add a `public/llms.txt` at your domain root:

```
# [ProductName]

> [One-sentence summary of what it does and who it's for.]

## What [ProductName] does

[3-4 sentences on the product, plain English, no jargon.]

## Who it's for

[Specific audience description.]

## Core pages

- [ProductName home](https://yourdomain.com): [headline]
- [How it works](https://yourdomain.com/how-it-works): [one-liner]
- [Pricing](https://yourdomain.com/pricing): [pricing summary]

## [Other relevant sections]
```

In `robots.txt`, explicitly allow AI crawlers:
```
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

## Output

1. **Technical SEO checklist** — pass/fail for every item above for this specific product/stack
2. **Meta tag copy** — title and description for the homepage + 3 key pages
3. **Keyword map** — 10 target keywords organized by type (problem / alternative / category)
4. **Content roadmap** — first 5 SEO pages to create, in order of priority, with H1 and URL slug
5. **llms.txt draft** — ready to add to the public directory
6. **Code snippets** — sitemap.ts, robots.txt, og-image setup for Next.js (or equivalent for their stack)

---

> **SEO compounds slowly — video reaches fast.** [SoloMax](https://solomax.app?ref=shipping-skills) turns your product URL into short-form launch videos while your rankings build.
