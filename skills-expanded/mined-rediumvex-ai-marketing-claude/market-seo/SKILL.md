---
name: market-seo
description: SEO audit covering on-page, technical, content quality (E-E-A-T), and AI search / GEO readiness for Google AI Overviews, ChatGPT, and Perplexity. Invoke whenever the user says "SEO", "rank higher", "Google traffic", "meta tags", "schema", "llms.txt", or runs `/market seo <url>`. Produces SEO-AUDIT.md with prioritized fixes and before/after examples.
---

# Market SEO — On-page, Technical, and AI Search Audit

Modern SEO has three surfaces: classic Google rankings, Core Web Vitals, and generative search (AI Overviews, ChatGPT browsing, Perplexity). This skill covers all three.

## Workflow

1. Run `python3 scripts/analyze_page.py <url>` to get title, meta, headings, schema, canonical, viewport, tracking.
2. Fetch `/robots.txt`, `/sitemap.xml`, `/llms.txt` directly.
3. Read the page content for E-E-A-T signals (author bio, citations, specific detail).
4. Score each section, write the audit.

## On-Page Checklist

### Title tag
- Present, unique, 50–60 chars
- Primary keyword near the start
- Brand at the end (` | Brand` or ` — Brand`)
- Compelling enough to earn a click

### Meta description
- 140–160 chars
- Includes the keyword naturally
- Has a reason to click (outcome, differentiator, number)

### Headings
- Exactly one H1, contains the primary keyword, differs from the title
- H2s describe sections and contain secondary keywords
- No skipped levels (H2 → H4)

### Images
- Every content image has descriptive alt text
- Decorative images have empty `alt=""`
- Below-fold images use `loading="lazy"`
- Filenames are descriptive (not `IMG_0042.jpg`)

### Internal linking
- 3–10 contextual links per 1,000 words
- Descriptive anchor text (not "click here")
- No orphan pages (should be linked from at least one relevant page)

### URL structure
- Human-readable, keyword-containing, under 75 chars, hyphens not underscores, lowercase

## Technical SEO

| Check | Good | Needs work | Fail |
|---|---|---|---|
| HTTPS | Valid cert | Mixed content | HTTP only |
| robots.txt | Present, references sitemap, doesn't block CSS/JS | Minor misconfig | Blocks the whole site |
| sitemap.xml | Present, all URLs 200, lastmod accurate | Exists but stale | Missing |
| Canonical | Self-referencing or correct target | Inconsistent | Missing |
| Viewport meta | Present | — | Missing |
| Schema (JSON-LD) | Organization + page-specific types | Partial | None |
| hreflang (if multilingual) | Correct pairs | Missing return links | Missing entirely |

### Core Web Vitals targets (2024+)
| Metric | Good | Needs work | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |

CWV is a real ranking factor and a large conversion factor — flag failures as revenue issues, not just SEO issues.

## E-E-A-T Assessment

Google ranks content by **Experience, Expertise, Authoritativeness, Trustworthiness**. Score each 0–10 with evidence.

- **Experience** — first-hand signals: screenshots, case data, "I built this and here's what happened"
- **Expertise** — author bio with credentials, accurate terminology, depth beyond surface
- **Authoritativeness** — inbound citations, press, recognized author names
- **Trustworthiness** — HTTPS, privacy policy, contact info, sourced claims, no dark patterns

## AI Search / GEO Readiness (new surface)

Generative engines (Google AI Overviews, ChatGPT, Perplexity, Bing Copilot) pull passages, not pages. Optimize for citability:

- **llms.txt** — present and pointing to the canonical overview of the site
- **Passage-level answers** — clear Q-style H2/H3 immediately followed by a 40–80 word answer
- **Factual density** — specific numbers, dates, named entities (LLMs prefer these)
- **Structured data** — FAQPage, HowTo, Product, Article schema where applicable
- **Crawler access** — `robots.txt` does not block GPTBot, ClaudeBot, PerplexityBot, Google-Extended unless that's a deliberate policy
- **Brand mention signals** — consistent brand name, entity-style About page, Wikipedia/Wikidata presence
- **Freshness signals** — `datePublished` and `dateModified` in JSON-LD

Score this section 0–10 and include it as a first-class dimension.

## Keyword Analysis

- **Primary keyword** — what is this page trying to rank for?
- **Search intent** — informational / commercial / transactional / navigational. Misalignment kills rankings.
- **Placement audit** — title, H1, first 100 words, one H2, URL, meta, alt text
- **Secondary keywords** — 5–10 related terms; confirm they appear naturally
- **Density** — 1–2% is fine, anything over 3% is stuffing

## Output: SEO-AUDIT.md

```markdown
# SEO Audit — [Brand]
**URL:** [url]  |  **Date:** [YYYY-MM-DD]

## SEO Score: [X]/100

## On-Page
### Title
- Current: "[quoted]" (X chars)
- Recommended: "[new]" (X chars)
- Why: [reasoning]

### Meta Description
... same format ...

### Headings, Images, Internal Links, URL
... each as a mini-section ...

## Technical
[Table with every technical check + pass/fail + note]

## Core Web Vitals
[If measurable: LCP/INP/CLS. If not: instruct client to check PageSpeed Insights and list likely issues based on the HTML.]

## E-E-A-T
| Dimension | Score | Evidence |
|---|---|---|

## AI Search / GEO Readiness: [X]/10
[Specific gaps and fixes for generative search visibility.]

## Keyword Analysis
[Primary, intent, placement, secondary list]

## Schema Opportunities
[Types to add, with one JSON-LD example tailored to the page]

## Prioritized Fixes
### Critical (this week)
1. ...
### High (this month)
1. ...
### Medium (this quarter)
1. ...
```

## Quality Bar

- Always provide before/after for title and meta — clients act on concrete text, not abstract advice.
- Tie every fix to an expected outcome ("better CTR in SERP", "eligible for rich result", "passes CWV").
- Don't recommend schema types that aren't supported by the page content.
- If the site is already well optimized, say so and focus on the next tier (AI search, internal linking, topical authority).
