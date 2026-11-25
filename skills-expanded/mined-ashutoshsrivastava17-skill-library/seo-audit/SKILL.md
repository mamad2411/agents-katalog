---
name: seo-audit
description: >
  Audit a website or page for SEO issues: technical SEO, on-page optimization,
  content quality, backlink profile, and keyword strategy.
  TRIGGER when: user says /seo-audit, "SEO review", "audit my site", "check SEO", "search optimization".
argument-hint: "[URL or domain to audit]"
user-invocable: true
---

# SEO Audit

Perform a structured SEO audit covering technical health, on-page optimization, content quality, backlink profile, and keyword strategy. Produces a prioritized list of findings with actionable recommendations.

---

## Process

### Step 1 — Gather Inputs and Scope

Determine the scope of the audit before beginning.

| Input | Required? | Notes |
|---|---|---|
| URL or domain | Yes | Single page, subdomain, or full domain |
| Target keywords | Recommended | 5-20 primary keywords to evaluate against |
| Competitor domains | Optional | 2-3 competitors for benchmarking |
| Google Search Console data | Optional | Crawl errors, indexing stats, query data |
| Google Analytics / traffic data | Optional | Organic traffic trends, landing pages |
| Current sitemap URL | Optional | Usually at /sitemap.xml |
| robots.txt URL | Optional | Usually at /robots.txt |

If the user provides only a URL, proceed with what can be inferred and note where additional data would strengthen the audit.

### Step 2 — Technical SEO Audit

Evaluate the technical foundation that search engines need to crawl and index the site.

| Check | What to Look For | Severity |
|---|---|---|
| **Crawlability** | robots.txt blocking important pages, noindex tags on key pages | Critical |
| **Indexation** | Pages missing from index, duplicate content indexed, index bloat | Critical |
| **Site speed** | Core Web Vitals (LCP > 2.5s, FID > 100ms, CLS > 0.1) | High |
| **Mobile-friendliness** | Viewport meta tag, responsive layout, tap target sizing | High |
| **HTTPS** | Mixed content warnings, HTTP pages, certificate issues | High |
| **XML Sitemap** | Missing, outdated, includes non-200 URLs, exceeds 50K URLs | Medium |
| **Canonical tags** | Missing, self-referencing, conflicting with other signals | Medium |
| **Structured data** | Missing schema markup, validation errors | Medium |
| **Hreflang** | Incorrect language/region codes, missing return tags | Medium (if international) |
| **Redirect chains** | More than 2 hops, redirect loops, 302 instead of 301 | Medium |
| **404 errors** | Broken internal links, high-authority pages returning 404 | Medium |
| **URL structure** | Non-descriptive URLs, excessive parameters, duplicate paths | Low |

For each issue found, record:
- **Issue**: What is wrong
- **Location**: Specific URL(s) affected
- **Impact**: How it affects rankings or crawl efficiency
- **Fix**: Concrete remediation steps
- **Priority**: Critical / High / Medium / Low

### Step 3 — On-Page SEO Audit

Evaluate how well individual pages are optimized for their target keywords.

| Element | Best Practice | Common Issues |
|---|---|---|
| **Title tag** | 50-60 chars, primary keyword near front, unique per page | Too long, duplicate across pages, missing keyword |
| **Meta description** | 150-160 chars, includes keyword, compelling CTA | Missing, duplicate, no call to action |
| **H1 tag** | One per page, includes primary keyword, matches search intent | Multiple H1s, missing H1, generic text |
| **Header hierarchy** | Logical H2-H6 nesting, keywords in H2s | Skipped levels, keyword stuffing |
| **URL slug** | Short, descriptive, hyphenated, includes keyword | Long parameter strings, underscores, no keyword |
| **Image alt text** | Descriptive, includes keyword where natural | Missing, generic ("image1.jpg"), keyword-stuffed |
| **Internal linking** | Relevant anchor text, links to related pages, reasonable count | Orphan pages, generic anchors ("click here") |
| **Keyword placement** | In first 100 words, naturally distributed, semantic variants | Keyword stuffing, missing from body entirely |
| **Content length** | Competitive with top-ranking pages for target query | Thin content (< 300 words for informational queries) |

### Step 4 — Content Quality Assessment

Evaluate content against what search engines reward.

| Factor | Evaluation Criteria |
|---|---|
| **Search intent match** | Does the content format match what ranks? (listicle vs. guide vs. tool vs. product page) |
| **E-E-A-T signals** | Author bylines, credentials, citations, first-hand experience, editorial standards |
| **Freshness** | Last updated date, outdated statistics or references, stale examples |
| **Comprehensiveness** | Covers subtopics that top-ranking competitors cover, answers related questions |
| **Uniqueness** | Original research, unique angle, not just rewritten competitor content |
| **Readability** | Short paragraphs, clear headings, bullet points, appropriate reading level |
| **Multimedia** | Relevant images, videos, diagrams, interactive elements |
| **User engagement signals** | Bounce rate, time on page, scroll depth (if analytics available) |

### Step 5 — Backlink Profile Analysis

Assess the quantity, quality, and risk of the site's backlink profile.

| Metric | What to Evaluate |
|---|---|
| **Total referring domains** | Trend over time (growing, flat, declining) |
| **Domain authority / rating** | Compared to competitors |
| **Link quality distribution** | % from high-authority vs. low-quality domains |
| **Anchor text distribution** | Over-optimized exact-match vs. natural/branded mix |
| **Toxic / spammy links** | Links from PBNs, link farms, irrelevant foreign-language sites |
| **Lost links** | Recently lost high-value links that could be reclaimed |
| **Competitor link gap** | Domains linking to competitors but not to the audited site |
| **Content linkability** | Does the site have assets that naturally attract links? |

Recommended anchor text distribution for a healthy profile:

| Anchor Type | Healthy Range |
|---|---|
| Branded (company name) | 30-50% |
| URL / naked link | 15-25% |
| Generic ("click here", "learn more") | 10-20% |
| Topical / partial match | 10-20% |
| Exact match keyword | 1-5% |

### Step 6 — Keyword Strategy Review

Evaluate the current keyword targeting approach.

| Analysis | Method |
|---|---|
| **Keyword coverage** | Map existing pages to target keywords — identify gaps and cannibalization |
| **Search intent alignment** | For each target keyword, verify the page type matches SERP intent (informational, commercial, transactional, navigational) |
| **Keyword difficulty vs. authority** | Flag keywords where site authority is too low to realistically compete |
| **Quick wins** | Pages ranking positions 4-20 that could move up with optimization |
| **Cannibalization** | Multiple pages targeting the same keyword, diluting authority |
| **Long-tail opportunities** | Related queries with lower competition and clear intent |
| **SERP feature opportunities** | Featured snippets, People Also Ask, image packs the site could capture |

---

## Output Format

Structure the audit report as follows:

1. **Executive Summary** — Overall SEO health score (Critical / Needs Work / Good / Excellent), top 3 wins, top 3 risks.
2. **Technical SEO Findings** — Table of issues sorted by priority.
3. **On-Page Optimization Findings** — Page-by-page or pattern-based findings.
4. **Content Quality Assessment** — Strengths and weaknesses with examples.
5. **Backlink Profile Summary** — Key metrics, risk assessment, opportunities.
6. **Keyword Strategy Gaps** — Coverage map, cannibalization issues, quick wins.
7. **Prioritized Action Plan** — Ranked list of recommendations with estimated effort (Low / Medium / High) and expected impact (Low / Medium / High).

Use an **Impact vs. Effort matrix** to help the user prioritize:

| | Low Effort | Medium Effort | High Effort |
|---|---|---|---|
| **High Impact** | DO FIRST | PLAN NEXT | STRATEGIC BET |
| **Medium Impact** | QUICK WIN | SCHEDULE | CONSIDER |
| **Low Impact** | IF TIME ALLOWS | BACKLOG | SKIP |

---

## Quality Checklist

- [ ] Every finding has a specific location (URL or pattern), not just a general observation
- [ ] Recommendations are actionable — the user knows exactly what to change
- [ ] Priority is assigned based on impact, not just best practice
- [ ] Technical issues are verified, not assumed (e.g., confirm noindex is present, not just possible)
- [ ] Content recommendations reference actual competitor content, not generic advice
- [ ] Backlink analysis distinguishes between correlation and causation
- [ ] Quick wins are genuinely quick (can be done in under a day)
- [ ] The report avoids jargon without explanation — assume the reader may not be an SEO expert
- [ ] Metrics include benchmarks or competitor comparisons for context
- [ ] The action plan has a clear sequence, not just a flat list

---

## Edge Cases

- **Single page audit** (not full site): Focus on on-page and content quality. Note that technical and backlink analysis is limited without site-wide context.
- **Brand new site** (< 6 months): Backlink profile will be thin — focus on technical foundation and content strategy rather than link metrics. Set expectations for timeline to results.
- **Site migration in progress**: Flag that audit results may be temporary. Prioritize redirect mapping, canonical tags, and indexation monitoring.
- **JavaScript-heavy / SPA site**: Emphasize crawlability concerns — check if content is rendered for Googlebot, test with URL Inspection Tool, look for hydration issues.
- **Local business**: Add local SEO checks — Google Business Profile, NAP consistency, local schema, review signals, local pack rankings.
- **E-commerce site**: Add product-specific checks — product schema, faceted navigation crawl traps, out-of-stock page handling, review markup.
- **No access to Search Console or Analytics**: Clearly state which parts of the audit are limited and recommend the user grant access for a more complete picture.
- **Penalized or de-indexed site**: Check for manual actions in Search Console, review for thin/duplicate content at scale, examine backlink profile for spam patterns. Recommend a recovery plan rather than a standard optimization plan.
