---
name: schema-markup
description: When the user wants to add, fix, or optimize schema markup and structured data on their site. Also trigger on "schema markup", "structured data", "JSON-LD", "rich snippets", "schema.org", "FAQ schema", "product schema", "review schema", "breadcrumb schema", "rich results", "structured data errors". For broader SEO, see seo-audit. For AI search optimization, see ai-seo.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

You are a structured data expert helping solopreneurs implement schema markup that earns rich results, improves click-through rates, and signals entity clarity to both Google and AI search engines.

---

## When to Use This Skill

Trigger this skill when the user wants to:

- Add schema markup to a page for the first time
- Fix schema validation errors flagged in Google Search Console
- Understand which schema types to prioritize for their site
- Improve click-through rates through rich results
- Make their content more legible to AI search engines (Perplexity, ChatGPT, Google AI Overviews)
- Audit existing structured data for gaps or mistakes
- Implement schema via code, CMS plugin, or Google Tag Manager

---

## Context Check

Before diving into implementation, ask or confirm:

1. **What CMS or platform are they on?** (WordPress, Webflow, Framer, custom code, Shopify, etc.)
2. **What type of site is it?** (SaaS, blog, local service, e-commerce, personal brand, course site)
3. **Do they already have schema markup?** If yes, have they checked GSC for errors?
4. **What pages are the priority?** (Homepage, product pages, blog posts, landing pages)
5. **Have they validated their markup?** (Rich Results Test, Schema Markup Validator)

Do not recommend a schema type before knowing what the page is actually about. Schema must reflect visible page content — not aspirational content.

---

## What Schema Markup Does (and Does Not Do)

### What it DOES:
- Enables **rich results** in Google SERP (star ratings, price, breadcrumbs, sitelinks, etc.)
- Improves **click-through rate** — rich results see 20–40% higher CTR vs. plain listings
- Sends **entity clarity signals** to Google's Knowledge Graph
- Makes content more parseable by **AI search engines** (Perplexity, Bing Copilot, ChatGPT)
- Helps AI Overviews and AI Mode cite your content more reliably
- Supports **GEO (Generative Engine Optimization)** — 81% of AI-cited pages have schema markup

### What it DOES NOT:
- **Does not directly improve rankings.** Google has confirmed this repeatedly. Schema is a visibility tool, not a ranking signal.
- Does not substitute for good content or technical SEO
- Does not guarantee rich results — Google decides whether to display them
- Does not help if the schema doesn't match the visible page content

> Bottom line: schema is a CTR and entity-recognition tool. Treat it as such.

---

## JSON-LD vs. Microdata vs. RDFa

**Always use JSON-LD. No exceptions.**

| Format | Recommendation |
|---|---|
| **JSON-LD** | Google's recommended format. Lives in `<script>` tags, separate from HTML, easy to update, easy to validate. |
| Microdata | Embedded in HTML attributes. Harder to maintain. Do not use for new implementations. |
| RDFa | Similar drawbacks to Microdata. Legacy format. Avoid. |

JSON-LD can be placed in the `<head>` (preferred) or `<body>`. It does not require touching your existing HTML structure. This makes it safe, portable, and CMS-friendly.

---

## Priority Schema Types for Solopreneurs

Focus on the types that match your actual content. Do not add schema for content that doesn't exist on the page.

### Tier 1 — Implement First

**Organization**
- Every site should have this on the homepage or about page.
- Establishes your brand as a named entity in Google's Knowledge Graph.
- Include: `name`, `url`, `logo`, `sameAs` (link to LinkedIn, Twitter, Crunchbase, etc.).

**BreadcrumbList**
- Appears in SERPs as navigational trail under your title.
- Low effort, high payoff. Works on almost any multi-page site.
- Essential for SEO on sites with clear hierarchy.

**Article / BlogPosting**
- For blog posts and editorial content.
- Required fields: `headline`, `author`, `datePublished`, `image`.
- Helps Google News inclusion for publishers.

### Tier 2 — High Impact for Specific Site Types

**Product** (SaaS, e-commerce, tools)
- Enables price, availability, and review stars in SERP.
- Required: `name`, `image`, `offers` (with `price`, `priceCurrency`, `availability`).
- For SaaS, pair with `SoftwareApplication`.

**SoftwareApplication** (SaaS / apps)
- Displays app category, operating system, price, and aggregate rating.
- Required: `name`, `operatingSystem`, `applicationCategory`, `offers`.
- Combine with `AggregateRating` for star display.

**Review / AggregateRating**
- Enables star ratings in SERP — one of the highest CTR lifts available.
- Only add if reviews are actually visible on the page.
- Do NOT fabricate or aggregate from off-site reviews.

**LocalBusiness** (service businesses, consultants with a location)
- Critical for local SEO and Google Maps integration.
- Required: `name`, `address`, `telephone`, `openingHours`.
- Use the most specific subtype available (e.g., `ProfessionalService`, `MedicalBusiness`).

### Tier 3 — Situational

**HowTo**
- Google deprecated HowTo rich results in September 2023 (desktop) and 2024 (mobile).
- No longer generates rich results on Google. Still useful for Bing and AI engines.
- Keep if already implemented; not worth building from scratch for Google traffic.

**FAQPage**
- Google restricted FAQ rich results in August 2023.
- FAQ rich results now only show for authoritative government and health sites.
- Still useful for Bing, Perplexity, and AI engine entity parsing.
- Keep existing FAQ schema; do not prioritize for new builds targeting Google rich results.

**VideoObject** (for pages with embedded video)
- Enables video carousels and thumbnails in SERP.
- Required: `name`, `description`, `thumbnailUrl`, `uploadDate`.
- High value for YouTube-embedded content on landing pages.

---

## Google's FAQ and HowTo Deprecation (August 2023)

In August 2023, Google announced significant changes to FAQ and HowTo rich results:

- **HowTo rich results:** Removed from mobile in August 2023, then from desktop in September 2023. Fully deprecated.
- **FAQ rich results:** Now restricted to well-known, authoritative **government and health websites only**. Most sites will not see FAQ rich results regardless of how correctly the schema is implemented.

**What this means for you:**
- Do not spend time building new FAQPage or HowTo schema primarily to earn Google rich results.
- If you already have it deployed, leave it — it does no harm and still helps Bing and AI parsing.
- Redirect that effort to Product, Review, BreadcrumbList, and Organization schema instead.

In 2025, Google also retired support for: Course Info, Claim Review, Estimated Salary, Learning Video, Special Announcement, and Vehicle Listing structured data types in Search Console reporting.

---

## Schema Markup for AI Search (GEO)

AI search engines process schema differently from traditional crawlers, but schema still matters — for different reasons.

**Perplexity AI:** Explicitly uses structured data to identify reliable, machine-readable sources. Pages with valid, well-typed schema appear more frequently in Perplexity's citations because the platform prioritizes well-defined entity information.

**Google AI Overviews / AI Mode:** Google confirmed in April 2025 that structured data gives an advantage in AI-generated search results.

**ChatGPT:** Confirmed in early 2025 that structured data influences which products and pages appear in its results.

**The GEO impact:**
- An AccuraCast study of 2,000+ prompts across ChatGPT, Google AI Overviews, and Perplexity found that **81% of cited web pages had schema markup**.
- Content with proper schema shows **30–40% higher AI visibility**.

**Key schema types for AI engines:**
- `Organization` with `sameAs` links — establishes entity identity across the web
- `Person` — for personal brands, founders, authors
- `Product` and `SoftwareApplication` — for commercial entities
- `Article` with `author` entity — for content authority signals

The mechanism: AI systems need to understand, verify, and attribute information. Schema provides machine-readable signals that reduce ambiguity — especially when your brand or topic name is shared by others.

---

## Implementation Methods

### Option 1: Hand-coded JSON-LD (Recommended for developers)
Place a `<script type="application/ld+json">` block in the `<head>` of each relevant page. Best for precision and control.

```json
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Your Brand Name",
  "url": "https://yourdomain.com",
  "logo": "https://yourdomain.com/logo.png",
  "sameAs": [
    "https://twitter.com/yourbrand",
    "https://linkedin.com/company/yourbrand"
  ]
}
</script>
```

### Option 2: CMS Plugins (Recommended for WordPress / Shopify)
- **WordPress:** Yoast SEO, Rank Math, Schema Pro, All in One SEO
- **Shopify:** JSON-LD for SEO, Schema Plus
- **Webflow / Framer:** Custom code embeds using JSON-LD blocks

Plugin approach is fast but review the output — many plugins generate bloated or incorrect schema by default.

### Option 3: Google Tag Manager
Inject JSON-LD via a Custom HTML tag. Useful for sites where you cannot edit the `<head>` directly. Fire the tag on specific page types using GTM triggers.

Caveat: Some crawlers may not execute GTM-loaded JavaScript. Test with the Rich Results Test to confirm the schema is being read.

---

## Validation Checklist

Run every schema implementation through these tools before considering it done:

- [ ] **Rich Results Test** (`search.google.com/test/rich-results`) — confirms Google can read your schema and whether it qualifies for rich results
- [ ] **Schema Markup Validator** (`validator.schema.org`) — validates against Schema.org specification, independent of Google
- [ ] **Google Search Console > Enhancements report** — monitors live performance, errors, and warnings at scale across your site
- [ ] **Check for "missing required property" warnings** — these block rich result eligibility
- [ ] **Verify schema matches visible page content** — mismatches are a policy violation and can trigger manual actions

---

## Common Errors to Fix

| Error | What It Means | Fix |
|---|---|---|
| Missing required property | A field Google requires for rich result eligibility is absent | Add the missing field (`image`, `author`, `datePublished`, etc.) |
| Incorrect `@type` | Using a generic type where a specific one is needed | Use `Restaurant` not `Organization`, `BlogPosting` not `Article` when appropriate |
| Schema doesn't match page content | Markup describes content not visible to users | Align schema with what is actually on the page |
| Duplicate schemas | Multiple conflicting schemas of the same type on one page | Consolidate into one block or use `@graph` to combine |
| Invalid date format | `datePublished` uses human-readable format instead of ISO 8601 | Use `"2025-04-18"` or `"2025-04-18T09:00:00+05:30"` |
| Syntax errors in JSON-LD | Missing commas, unclosed brackets, unescaped quotes | Run through a JSON linter before deploying |
| Using deprecated properties | Properties removed from Schema.org spec | Check schema.org for current vocabulary; remove or replace deprecated fields |
| Adding reviews without review content | AggregateRating added but no reviews on the page | Only add review schema when reviews are actually visible on the page |

---

## Common Mistakes (Beyond Errors)

- **Treating schema as a ranking hack.** It is not. If your content ranks poorly, schema will not save it.
- **Implementing schema on every page indiscriminately.** Priority matters. Focus on pages with the highest commercial or traffic value first.
- **Not monitoring GSC Enhancements.** Schema degrades silently — new templates, plugin updates, and CMS changes break it regularly.
- **Adding FAQ schema hoping for rich results in 2025.** That ship has sailed for most sites. Redirect the effort.
- **Ignoring `sameAs` on Organization/Person schema.** This is one of the most underused fields — it directly connects your entity to external sources Google trusts.
- **Stacking schema types aggressively** without ensuring all required fields are present. An incomplete schema is worse than no schema.

---

## Contrarian Takes

**"More schema = better SEO."**
No. Incomplete schema actively hurts you — it signals to Google that your page doesn't qualify for rich results. One complete, accurate schema block outperforms five sloppy ones.

**"Schema will get you into AI Overviews."**
Schema improves your odds, but it doesn't guarantee inclusion. AI Overviews prioritize content quality, topical authority, and E-E-A-T. Schema is a supporting signal, not the main driver.

**"AI engines need your schema to understand your content."**
If your content is well-written, clearly structured, and semantically consistent, AI engines will parse it fine without schema. Schema accelerates understanding and reduces ambiguity — it does not compensate for unclear writing or weak content.

**"FAQPage schema is dead."**
For Google rich results, yes — for most sites. For Bing, Perplexity, and AI entity parsing, it still adds value. Dead is an overstatement. Deprioritized is accurate.

---

## Quick Wins: 3 Schema Types to Add This Week

If you are starting from zero, implement these in order:

1. **Organization** on your homepage — establishes your brand as a named entity. Takes 10 minutes.
2. **BreadcrumbList** on all interior pages — immediate SERP appearance benefit, works on nearly every site type.
3. **Article / BlogPosting** on your top 5 blog posts — adds author and date signals, supports news indexing and AI attribution.

Once these are validated and live, move to Product or SoftwareApplication (for SaaS), or AggregateRating (if you have real reviews on-page).

---

## Related Skills

- **seo-audit** — Full technical and on-page SEO review; use before or alongside schema implementation
- **ai-seo** — Optimizing content for AI-generated answers, AI Overviews, and GEO
- **programmatic-seo** — Scaling schema markup across hundreds or thousands of programmatically generated pages
- **site-architecture** — Ensuring your site hierarchy supports BreadcrumbList and internal linking schema

---

*Generated using the schema-markup skill from Solopreneur Skills*
