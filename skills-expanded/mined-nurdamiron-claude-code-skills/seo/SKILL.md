---
name: seo
description: "19 sub-skills: technical audit, E-E-A-T, schema, GEO, LLM optimization, brand AI tracking, intent classification, IndexNow, content rewrite, AI Overviews. Real data only."
user-invocable: true
argument-hint: "[command] [url]"
allowed-tools:
  - WebFetch
  - WebSearch
  - Bash
  - Read
  - Write
---

# SEO Analyzer v4.0 — Real Data Only

## BEFORE YOU START — Ask if unclear

If the user runs `/seo` without a URL or command, ask:
```
What would you like to analyze?
  1.  Full audit       — /seo audit [url]
  2.  Single page      — /seo page [url]
  3.  LLM readiness    — /seo llm [url]
  4.  Schema fix       — /seo schema [url]
  5.  Content/E-E-A-T  — /seo content [url]
  6.  Action plan      — /seo plan [url]
  7.  Brand AI check   — /seo brand [brand-name] [url]
  8.  Search intent    — /seo intent [url]
  9.  IndexNow check   — /seo indexnow [url]
  10. Content rewrite  — /seo rewrite [url]
  11. AI Overviews     — /seo aio [keyword] [url]

Which command and URL?
```

Never simulate, hallucinate, or estimate data you haven't fetched.
If a fetch fails — say so. If you can't check something — say so.

---

## Sub-skills (19 total)
```
/seo audit        — full site audit (runs all checks)
/seo page         — single page deep analysis
/seo content      — E-E-A-T quality scoring
/seo schema       — JSON-LD structured data
/seo images       — alt text + format audit
/seo sitemap      — XML sitemap generation
/seo hreflang     — international SEO
/seo local        — local business + GBP
/seo geo          — AI Overviews / GEO
/seo llm          — LLM / AI citation optimization
/seo plan         — strategic SEO roadmap
/seo competitor   — competitor gap analysis
/seo content-opt  — on-page optimization
/seo programmatic — pages at scale
/seo brand        — AI brand visibility tracking (NEW)
/seo intent       — search intent classification (NEW)
/seo indexnow     — IndexNow implementation check (NEW)
/seo rewrite      — AutoGEO content rewrite suggestions (NEW)
/seo aio          — AI Overviews presence check (NEW)
```

---

## STEP 1 — Real Data Collection (mandatory before any analysis)

When given a URL, run ALL of these in order. Never skip.

### 1a — Fetch live pages
```
WebFetch: [url]                   → parse HTML: title, meta, H1-H6, canonical,
                                    og tags, JSON-LD blocks, viewport, lang attr
WebFetch: [url]/robots.txt        → crawl rules, AI crawler allowances
WebFetch: [url]/sitemap.xml       → if 404, check robots.txt for Sitemap: line
WebFetch: [url]/llms.txt          → LLM accessibility file (note if missing)
```

Parse raw HTML directly. Extract all `<script type="application/ld+json">` blocks.
Check for client-side rendering: if HTML body has minimal content + heavy JS = CSR warning
(AI crawlers cannot execute JavaScript — CSR content is invisible to them).

### 1b — Core Web Vitals (PageSpeed Insights API, no key required)
```
WebFetch: https://www.googleapis.com/pagespeedonline/v5/runPagespeed
          ?url=[url_encoded]&strategy=mobile

WebFetch: https://www.googleapis.com/pagespeedonline/v5/runPagespeed
          ?url=[url_encoded]&strategy=desktop
```

Extract from JSON:
```
lighthouseResult.audits.largest-contentful-paint.displayValue  → LCP
lighthouseResult.audits.interaction-to-next-paint.displayValue → INP
lighthouseResult.audits.total-blocking-time.displayValue       → TBT
lighthouseResult.audits.cumulative-layout-shift.displayValue   → CLS
lighthouseResult.categories.performance.score × 100            → Perf score
lighthouseResult.categories.seo.score × 100                    → Lighthouse SEO
```

If API returns error or rate limit: state "CWV: fetch failed — check manually at
pagespeed.web.dev" and mark CWV score as N/A (do not guess).

### 1c — HTTP response headers
```
Bash: curl -sI "[url]" 2>/dev/null | head -40
```
Check: HTTPS redirect (301 from http://), Strict-Transport-Security,
X-Frame-Options, X-Content-Type-Options, Content-Security-Policy,
server/framework leakage in Server: header.

### 1d — Search index presence
```
WebSearch: site:[domain]
```
Note approximate indexed page count from snippet text.
Do NOT treat this number as exact — it is Google's estimate only.

---

## STEP 2 — What this skill CANNOT measure (always state in report)

Always include this block in the report:
```
-- DATA LIMITATIONS ──────────────────────────────────────────
  Backlinks            requires Ahrefs / Semrush / Moz
  Full site crawl      requires Screaming Frog / Sitebulb
  GSC impressions/CTR  requires Google Search Console access
  Real INP field data  requires Chrome UX Report (CrUX)
  Holistic CWV score   requires GSC Core Web Vitals report
  AI citation tracking requires Brandwatch / Mention / manual
──────────────────────────────────────────────────────────────
```

---

## STEP 3 — Scoring Weights (0-100 total)

```
Technical SEO       20 pts   (crawlability, HTTPS, architecture, CWV)
Content / E-E-A-T   20 pts   (depth, authorship, citations, freshness)
On-Page SEO         17 pts   (title, meta, headings, URL, internal links)
LLM Readiness       18 pts   (llms.txt, crawlers, structure, entity clarity)
Schema Markup        9 pts   (JSON-LD types, validity, rich snippet eligibility)
Core Web Vitals     10 pts   (LCP, INP, CLS — real PSI data only)
Images               6 pts   (alt text, WebP/AVIF, lazy loading, sizing)
```

Priority: CRITICAL > HIGH > MEDIUM > LOW

---

## STEP 4 — Technical SEO Checks

### Crawlability
- robots.txt present, valid syntax, no accidental Disallow: /
- sitemap.xml linked from robots.txt, all URLs return 200
- Canonical tags on all indexable pages (self-referencing + cross-page)
- No noindex on pages that should rank
- No redirect chains longer than 1 hop

### Client-Side Rendering (CRITICAL for AI + SEO)
- If HTML <body> has < 500 chars of text content → CSR detected
- CSR means AI crawlers see empty page — GPTBot, ClaudeBot, Google-Extended
  cannot execute JavaScript
- Fix: SSR / SSG / prerendering required

### Site Architecture
- Max crawl depth: 3 clicks from homepage to any page
- Internal links use descriptive anchor text (not "click here")
- No orphan pages (pages with zero internal links)

### HTTPS & Security Headers
- Redirects http:// → https:// (301)
- HSTS present: `Strict-Transport-Security: max-age=31536000`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY` or `SAMEORIGIN`
- No sensitive data in Server: header

### Core Web Vitals 2026 (75th percentile, holistic site-level scoring)
```
LCP  < 2.5s   good  |  2.5-4.0s  needs improvement  |  > 4.0s  poor
INP  < 200ms  good  |  200-500ms needs improvement  |  > 500ms  poor
CLS  < 0.1    good  |  0.1-0.25  needs improvement  |  > 0.25   poor
```
Note: Google March 2026 Core Update introduced holistic CWV scoring —
performance is now evaluated across the entire domain, not per-URL.
43% of sites fail the INP threshold (most common failure in 2026).

---

## STEP 5 — Content Quality (E-E-A-T)

### Experience
- First-hand knowledge signals: personal data, case studies, original research
- "We found that..." / "In our testing..." patterns
- Original statistics or surveys (highest AI citation value)

### Expertise
- Named author on every article (not "Admin" or "Staff Writer")
- Author bio page with: credentials, publication history, social links
- Topic depth: glossary, definitions, comprehensive coverage

### Authoritativeness
- Outbound citations to primary sources (studies, official docs, .gov/.edu)
- Year-tagged data — flag anything older than 2 years
- Numbers > adjectives: "42% faster" beats "much faster"

### Trustworthiness
- About + Contact + Privacy pages present and linked from footer
- Author sameAs links: LinkedIn, Google Scholar, ORCID, Twitter/X
- Organization sameAs: Wikidata, Crunchbase, LinkedIn Company

### Content Freshness (AI prefers recent content)
- 85% of Google AI Overview citations are from content < 2 years old
- 44% of citations are from 2025 content
- Visible "Last updated: YYYY-MM-DD" on pages
- `dateModified` in Article schema (not just `datePublished`)

---

## STEP 6 — On-Page SEO

- Title: 50-60 chars, primary keyword in first 3 words, unique per page
- Meta description: 150-160 chars, includes action verb + keyword, unique
- H1: exactly one per page, matches search intent directly
- Heading hierarchy: H1 > H2 > H3, no skipped levels
- URL: short, lowercase, hyphens only, keyword present, no query params
- Internal linking: 3-5 contextual links per page, descriptive anchors
- Open Graph: og:title, og:description, og:image (1200x630), og:url
- Twitter Card: twitter:card, twitter:title, twitter:image

---

## STEP 7 — LLM Optimization (GEO) — 18 points

### Why LLMs cite some content and not others (2026 research data)
- 44.2% of all LLM citations come from the first 30% of a page's text
- Definition-first openings get significantly higher AI impression scores
- Content depth + readability beat traffic + backlinks for AI citation
- Listicles (21.9%), articles (16.7%), product pages (13.7%) = most cited types
- Structured content (headings, lists, FAQ) = most effective format in AI search
- Perplexity inline citations convert at 11x the rate of traditional organic search
- Top-10 organic ranking strongly correlates with AI citation (Ahrefs/Semrush data)

### AI Platform Market Share (2026)
```
ChatGPT      55-60% of AI referral traffic
Perplexity   18-22% (but 11x conversion vs organic)
Gemini        ~8.7%
Others        ~13%
```

### 7.1 — llms.txt (3 pts)
Community standard (llmstxt.org), NOT yet IETF/W3C official.
Adopted by 600+ sites including Stripe, Cloudflare, Anthropic, Vercel.
Reduces AI hallucinations about your site by 30-70%.

Required format:
```markdown
# [Site Name]

> [One sentence describing what the site is and who it's for]

## Docs
- [Page Title](https://example.com/page): [one sentence description]
- [Page Title](https://example.com/page): [one sentence description]

## API Reference
- [Endpoint](https://example.com/api/v1): [description]

## Optional: pages not for LLMs
- /admin
- /checkout
- /user/settings
```

Score:
- 3 pts: llms.txt exists, valid format, covers key pages
- 1 pt:  llms.txt exists but incomplete
- 0 pts: missing

### 7.2 — AI Crawler Access in robots.txt (3 pts)

Complete list of AI crawlers to ALLOW (as of 2026):
```
# OpenAI
User-agent: GPTBot           # training data
User-agent: OAI-SearchBot    # ChatGPT search
User-agent: ChatGPT-User     # ChatGPT browsing (user-triggered)

# Anthropic
User-agent: ClaudeBot        # primary crawler
User-agent: Claude-SearchBot # Claude search
User-agent: Claude-User      # user-triggered

# Perplexity
User-agent: PerplexityBot    # primary crawler
# Note: Perplexity-User IGNORES robots.txt — user-triggered requests
# cannot be blocked via robots.txt. This is a known limitation.

# Google
User-agent: Google-Extended       # Gemini / AI Overviews training
User-agent: Google-CloudVertexBot # Vertex AI

# Others
User-agent: Applebot-Extended  # Apple AI
User-agent: DeepSeekBot        # DeepSeek
User-agent: DuckAssistBot      # DuckDuckGo AI
User-agent: Gemini-Deep-Research
User-agent: CCBot              # Common Crawl (used by many LLMs)
User-agent: YouBot             # You.com
```

IMPORTANT: Blocking these = invisible to that AI platform.
IMPORTANT: Perplexity-User ignores robots.txt by design (user-triggered).
Check each explicitly in robots.txt. Blanket `Allow: /` is NOT enough.

Score:
- 3 pts: all major crawlers explicitly allowed (or no blocks at all)
- 2 pts: main crawlers allowed, some minor ones missing
- 1 pt:  partial — some major crawlers blocked
- 0 pts: GPTBot or ClaudeBot blocked

### 7.3 — Answer-First Content Structure (3 pts)
- First paragraph must directly answer the primary query (inverted pyramid)
- "Definition pattern": "[Topic] is [definition]" in first 150 words
- No preamble: ban "In today's world", "It's important to understand", "Many people"
- First 30% of content carries 44.2% of all citation weight — make it count
- Every H2/H3 should be phrased as the question it answers

Score:
- 3 pts: clear answer in first 150 words, every section heading is a question
- 2 pts: answer present but buried after preamble
- 1 pt:  no clear answer structure
- 0 pts: heavy preamble, answer not findable in first 30%

### 7.4 — Structured Formatting (2 pts)
- H2/H3 headings for each key question
- Bullet/numbered lists for comparisons, features, steps
- Tables for specs, pricing, comparisons (AI extracts tabular data well)
- Bold on key terms at first use
- Code blocks for technical content

### 7.5 — FAQ / HowTo Schema (2 pts)
- FAQPage schema for question/answer sections
- HowTo schema for step-by-step content
- speakable schema on Article/WebPage for AI Overviews + voice
  (target 2-4 speakable sections per page)

### 7.6 — Entity Clarity (2 pts)
- Consistent entity naming (no ambiguous pronouns for brand/product)
- Organization schema with sameAs to Wikidata, LinkedIn, Crunchbase
- Person schema for all authors with sameAs to professional profiles
- Definitions for all acronyms and industry terms (use `<abbr>`)

### 7.7 — Data Density + Citation Worthiness (2 pts)
- Original statistics, surveys, or proprietary research = highest value
- Third-party data cited with direct source links
- Year tagged: "(2025 data)", "(as of March 2026)"
- Flag any stats older than 2 years as needing refresh

### 7.8 — No Client-Side Rendering (1 pt)
- Server renders full HTML — AI crawlers cannot execute JS
- Test: WebFetch the URL and check if meaningful text is in the raw HTML
- 0 pts if body text < 500 chars in raw HTML (CSR detected)

---

## STEP 8 — Schema Markup

JSON-LD only (never microdata or RDFa).

Required types by content:
```
All pages:    Organization, BreadcrumbList, WebSite (with SearchAction)
Articles:     Article (with author Person, datePublished, dateModified)
Products:     Product (with offers Offer, aggregateRating AggregateRating)
FAQ content:  FAQPage
How-to:       HowTo
Local biz:    LocalBusiness
Authors:      Person (with sameAs, jobTitle, affiliation)
```

Validate at:
- schema.org/validator
- search.google.com/test/rich-results
- validator.schema.org

Rich snippet eligibility check: FAQ, HowTo, Product, Review, Event, Recipe

---

## STEP 9 — NEW: Brand AI Visibility (/seo brand)

Track how AI search engines currently describe your brand. Uses WebSearch to simulate
what users see when they ask AI assistants about the brand.

### Process
Run these WebSearch queries (replace [brand] with actual brand name):
```
WebSearch: "[brand]" site:perplexity.ai OR inurl:perplexity
WebSearch: what is [brand] [industry]
WebSearch: [brand] review [year]
WebSearch: [brand] vs competitors
WebSearch: [brand] [core product/service]
```

Also check:
```
WebFetch: [url]/llms.txt           → brand description accuracy
WebSearch: site:[domain]           → index coverage
```

### What to analyze from results
- **Brand description accuracy**: Does Google/AI describe the brand correctly?
- **Sentiment**: Positive / neutral / negative signals in top results
- **Competitor co-mentions**: Which competitors appear alongside the brand?
- **Knowledge gap**: Is the brand absent from results for key queries?
- **Entity disambiguation**: Is the brand confused with other entities?

### Output format
```
╔══════════════════════════════════════════════════════════════╗
║  BRAND AI VISIBILITY  |  [brand]  |  [date]                  ║
╠══════════════════════════════════════════════════════════════╣
║  AI Visibility Score: [XX]/100                               ║
╚══════════════════════════════════════════════════════════════╝

  Query                          Result               Presence
  ─────────────────────────────────────────────────────────────
  "what is [brand]"              [found/not found]    [score]
  "[brand] vs competitors"       [found/not found]    [score]
  "[brand] [core product]"       [found/not found]    [score]
  ─────────────────────────────────────────────────────────────

  Brand description found:
  "[exact text AI currently shows about the brand]"

  Issues detected:
  [!] [specific inaccuracy or gap found]

  Fix recommendations:
  - Add Organization sameAs to Wikidata entry
  - Update llms.txt with accurate brand description
  - Create/update About page with clear entity signals
  - Add FAQ schema answering "What is [brand]?"
```

Scoring (0-100):
- 30 pts: Brand appears in top results for "[brand]" query
- 25 pts: Accurate description in search snippets
- 20 pts: Appears for "[brand] vs" or "[brand] review" queries
- 15 pts: Positive sentiment dominant
- 10 pts: No entity disambiguation issues

---

## STEP 10 — NEW: Search Intent Classification (/seo intent)

For every page analyzed, classify its search intent and check alignment.

### The 4 Intent Types
```
Navigational   — user wants a specific site/page (brand queries)
Informational  — user wants to learn (how, what, why, guide, tutorial)
Commercial     — user is researching before buying (best, top, review, compare)
Transactional  — user wants to act now (buy, get, download, sign up, price)
```

### Classification Process

1. **Fetch the page** — extract: title, H1, meta description, first 300 words, URL slug
2. **Identify primary keyword intent signals**:
   - URL contains: /blog/, /guide/, /how-to/, /what-is/ → Informational
   - URL contains: /buy/, /shop/, /pricing/, /checkout/ → Transactional
   - URL contains: /best-, /top-, /review/, /compare/ → Commercial
   - URL is homepage or brand name → Navigational
3. **Check content-intent alignment**:
   - Informational page should have: definitions, explanations, FAQs, no hard CTAs
   - Transactional page should have: price, Add to Cart, urgency signals, trust badges
   - Commercial page should have: comparison tables, pros/cons, ratings, "best for" summaries
   - Navigational page should have: clear brand identity, direct links to key sections

### Intent Mismatch Detection
Flag when:
- Transactional intent page lacks pricing info or CTA
- Informational page has aggressive sales CTAs (reduces E-E-A-T)
- Commercial page has no comparison data
- Title signals one intent but content delivers another

### Output format per page
```
  Page: [url]
  Detected intent:    [Navigational / Informational / Commercial / Transactional]
  Confidence:         [High / Medium / Low]
  Content alignment:  [Aligned / MISMATCH]

  Intent signals found:
  + [signal 1]
  + [signal 2]
  - [mismatch signal if any]

  Fix: [specific change to align content with intent]
```

---

## STEP 11 — NEW: IndexNow Check (/seo indexnow)

IndexNow lets sites instantly notify Bing, Yandex, Naver, and Seznam when content changes.
Google does NOT support IndexNow (uses its own crawl system).

### What to check

1. **IndexNow key file**:
```
WebFetch: [url]/[any-key].txt
```
Look for a plain-text file containing just the API key (alphanumeric, 8-128 chars).
Also check: `WebFetch: [url]/indexnow.txt`

2. **robots.txt hint**:
```
# robots.txt may contain:
# IndexNow: [key]
```

3. **Meta tag** (less common):
```html
<meta name="indexnow-verification" content="[key]">
```

4. **Sitemap ping test** (informational only — cannot verify from outside):
Check if site documentation mentions IndexNow integration.

### Supported search engines (2026)
```
Bing      → indexnow.org endpoint
Yandex    → yandex.com/indexnow
Naver     → searchadvisor.naver.com
Seznam    → seznam.cz
DuckDuckGo → via Bing partnership
```

### Output format
```
  IndexNow Status:
  ─────────────────────────────────────────────────
  Key file found:     [YES: /abc123.txt / NO]
  robots.txt hint:    [YES / NO]
  Meta tag:           [YES / NO]
  ─────────────────────────────────────────────────
  Status: [IMPLEMENTED / NOT IMPLEMENTED]

  If NOT IMPLEMENTED — fix:
  1. Generate a key: openssl rand -hex 32
  2. Create /[key].txt containing just the key
  3. Add to robots.txt: IndexNow: [key]
  4. On content publish: POST to https://api.indexnow.org/indexnow
     Body: {"host":"[domain]","key":"[key]","urlList":["[updated-url]"]}
  5. Bing propagates to DuckDuckGo automatically
```

---

## STEP 12 — NEW: AutoGEO Content Rewrite (/seo rewrite)

Based on AutoGEO (ICLR 2026) — automatically generate AI-optimized rewrites
of the most citation-critical sections of a page.

### Process

1. **Fetch the page** and extract:
   - First 300 words (highest citation weight zone)
   - All H2/H3 headings
   - First paragraph under each heading

2. **Analyze for AutoGEO failure patterns**:
   - Preamble before the answer ("In today's fast-paced world...")
   - Passive voice density > 20%
   - No definition in first 150 words
   - Headings that don't phrase a question
   - Missing statistics or data points
   - Long sentences > 25 words (LLMs prefer ≤ 20 words)
   - Jargon without inline definition

3. **Generate rewrites** for each failing section:

Show original → rewritten side by side:
```
  SECTION: [H2 heading]
  ─────────────────────────────────────────────────────────
  ORIGINAL:
  "[exact original text, first 2-3 sentences]"

  REWRITTEN (AutoGEO):
  "[rewritten version: definition-first, active voice, data added,
    question-phrased heading, ≤ 20 word sentences]"

  Changes made:
  + Added definition in sentence 1
  + Moved key stat to opening
  + Converted heading to question format
  + Shortened avg sentence: 31 → 18 words
  ─────────────────────────────────────────────────────────
```

### AutoGEO Rewrite Rules (apply in order)
1. **Definition first**: Open with "[Topic] is [definition]" — never with context-setting
2. **Active voice**: "We measured X" not "X was measured"
3. **Stat anchoring**: Include one number in first 2 sentences if topic allows
4. **Question headings**: Every H2/H3 = a question the section answers
5. **Short sentences**: Max 20 words. Split anything longer
6. **Bold key terms**: First use of every important term gets `**bold**`
7. **Inverted pyramid**: Most important → least important (journalism style)
8. **No throat-clearing**: Delete first sentence if it contains "In today's", "It is important", "Many people"

### Output: rewrite-suggestions.md
Write a file with all rewrite suggestions in diff-friendly format.

---

## STEP 13 — NEW: AI Overviews Presence Check (/seo aio)

Google AI Overviews (formerly SGE) appear for ~20% of queries in 2026.
Check whether your content is being cited or excluded.

### Process

1. **Identify target keywords** from the page (if not provided):
   - Extract H1, first H2, meta title → derive 3-5 informational queries

2. **Run presence checks via WebSearch**:
```
WebSearch: [keyword] — note if result snippet looks like an AI Overview summary
WebSearch: what is [topic from page]
WebSearch: how to [action from page]
WebSearch: best [product/service from page]
WebSearch: [brand] [core topic]
```

3. **Analyze SERP signals** from WebSearch results:
   - Are results informational or commercial? (AI Overviews favor informational)
   - Does the domain appear in any top-3 results?
   - Are competitors in results for these queries?
   - Is featured snippet present? (correlates strongly with AIO citations)

4. **AIO eligibility scoring**:
```
  Query: [keyword]
  ─────────────────────────────────────────────────────────
  SERP type:            [Informational / Commercial / Mixed]
  AIO likely:           [YES / NO / UNKNOWN]
  Your domain in top 3: [YES / NO]
  Featured snippet:     [YES — yours / YES — competitor / NO]
  AIO citation risk:    [Likely cited / Unlikely / Blocked by CSR]
  ─────────────────────────────────────────────────────────
```

### AIO Ranking Factors (2026 data)
- Top-10 organic position = strongest predictor of AIO inclusion
- 85% of AIO citations are from content < 2 years old
- FAQ schema + speakable schema significantly improve AIO appearance
- Content with statistics cited from primary sources = 3x more likely in AIO
- CSR pages = 0% AIO inclusion (AI cannot render JavaScript)
- Answer-first structure (STEP 7.3) = highest AIO correlation

### Output
```
╔══════════════════════════════════════════════════════════════╗
║  AI OVERVIEWS CHECK  |  [domain]  |  [date]                  ║
╠══════════════════════════════════════════════════════════════╣
║  AIO Readiness Score: [XX]/100                               ║
╚══════════════════════════════════════════════════════════════╝

  Keyword              SERP Type     Top-3?   AIO Eligible?
  ─────────────────────────────────────────────────────────
  [keyword 1]          Info          YES      LIKELY
  [keyword 2]          Commercial    NO       UNLIKELY
  [keyword 3]          Mixed         NO       POSSIBLE
  ─────────────────────────────────────────────────────────

  Blockers found:
  [!] CSR detected — AI cannot index content
  [!] No FAQ schema — missing AIO signal
  [~] Content age > 2 years on [page] — refresh needed

  Quick wins:
  - Add FAQPage schema to [url]
  - Add speakable markup to answer sections
  - Refresh publication date + add dateModified to schema
```

---

## STEP 14 — Terminal Output Format

### Phase 1 — Data collection log (show as you fetch)
```
╔══════════════════════════════════════════════════════════════╗
║  SEO ANALYZER v4.0  |  [domain]                              ║
╚══════════════════════════════════════════════════════════════╝

  Fetching data — no simulation, real results only

  [1/7]  HTML + meta + schema ......................... [status]
  [2/7]  robots.txt + sitemap.xml ..................... [status]
  [3/7]  llms.txt ..................................... [status]
  [4/7]  PageSpeed Insights (mobile + desktop) ........ [status]
  [5/7]  HTTP headers (curl -sI) ...................... [status]
  [6/7]  Search index (site:[domain]) ................. [status]
  [7/7]  IndexNow key file ............................ [status]

  [status] = "done" | "FAILED: [reason]" | "404 not found"
```

Show each line as it completes. Show real values, not placeholders.

### Phase 2 — Health Report
```
╔══════════════════════════════════════════════════════════════╗
║  SEO HEALTH REPORT  |  [domain]  |  [YYYY-MM-DD]             ║
╠══════════════════════════════════════════════════════════════╣
║  SCORE: [XX]/100   [progress_bar]   Grade: [letter]          ║
╚══════════════════════════════════════════════════════════════╝

  Category            Points    Bar              Weight
  ────────────────────────────────────────────────────
  Technical SEO       [x]/20   [██████████]      20%
  Content / E-E-A-T   [x]/20   [██████████]      20%
  LLM Readiness       [x]/18   [██████████]      18%   <- AI era
  On-Page SEO         [x]/17   [██████████]      17%
  Core Web Vitals     [x]/10   [██████████]      10%
  Schema Markup       [x]/ 9   [██████████]       9%
  Images              [x]/ 6   [██████████]       6%
  ────────────────────────────────────────────────────
  TOTAL               [x]/100  [██████████]

  Core Web Vitals (real PSI data):
  LCP [mobile]: [value]  [GOOD/NEEDS WORK/POOR]
  INP [mobile]: [value]  [GOOD/NEEDS WORK/POOR]
  CLS [mobile]: [value]  [GOOD/NEEDS WORK/POOR]
  Performance:  [score]% mobile  |  [score]% desktop

╔══════════════════════════════════════════════════════════════╗
║  CRITICAL [N]   HIGH [N]   MEDIUM [N]   LOW [N]              ║
╚══════════════════════════════════════════════════════════════╝

-- CRITICAL ─────────────────────────────────────────────────
  [!] [exact issue found from real data — never invented]

-- HIGH ──────────────────────────────────────────────────────
  [#] [exact issue found from real data]

-- MEDIUM ────────────────────────────────────────────────────
  [~] [exact issue found from real data]

-- LOW ───────────────────────────────────────────────────────
  [-] [exact issue found from real data]

-- DATA LIMITATIONS ──────────────────────────────────────────
  Backlinks           requires Ahrefs / Semrush / Moz
  Full site crawl     requires Screaming Frog / Sitebulb
  GSC data            requires Google Search Console access
  Real INP field data requires Chrome UX Report (CrUX)
  Holistic CWV score  requires GSC Core Web Vitals report
──────────────────────────────────────────────────────────────

╔══════════════════════════════════════════════════════════════╗
║  GENERATED FILES                                             ║
╠══════════════════════════════════════════════════════════════╣
║  sitemap.xml           — built from crawled URLs             ║
║  robots.txt            — all AI crawlers allowed             ║
║  llms.txt              — site map for LLMs                   ║
║  schema.json           — JSON-LD ready to paste              ║
║  seo-action-plan.md    — prioritized fixes with effort tags  ║
║  rewrite-suggestions.md — AutoGEO content rewrites           ║
╚══════════════════════════════════════════════════════════════╝
```

### Progress bar rule
`█` = filled, `░` = empty, always 10 chars.
`[████████░░]` = 80%  |  `[████░░░░░░]` = 40%  |  `[██████████]` = 100%

### Grade thresholds
```
90-100  A+   AI-citation-ready, excellent
80-89   A    Strong, minor gaps
70-79   B+   Good, LLM gaps need fixing
60-69   B    Fair, structural work needed
50-59   C    Weak, significant problems
< 50    D    Critical, rebuild fundamentals
```

---

## STEP 15 — Generated Artifacts

After every full audit, write these files using the Write tool:

**sitemap.xml**
- Include only URLs that returned 200 from WebFetch
- Add lastmod (today's date if unknown), priority, changefreq
- Never invent URLs

**robots.txt**
- Allow all AI crawlers listed in 7.2
- Keep existing disallow rules from original robots.txt
- Add Sitemap: [url]/sitemap.xml line
- Add IndexNow: [key] line if key was found

**llms.txt**
- Per llmstxt.org format
- Only include pages you actually fetched and verified
- Note pages not suitable for LLMs (admin, checkout, etc.)

**schema.json**
- JSON-LD based on actual page content
- Include Organization + WebSite + Article (if article) + FAQ (if FAQ content found)
- Add speakable on sections that directly answer questions

**seo-action-plan.md**
```
# SEO Action Plan — [domain] — [date]

## CRITICAL (fix today)
- [ ] [issue]: [exact fix] — effort: [low/medium/high]

## HIGH (fix this week)
- [ ] [issue]: [exact fix] — effort: [low/medium/high]

## MEDIUM (fix this month)
- [ ] [issue]: [exact fix] — effort: [low/medium/high]

## LOW (backlog)
- [ ] [issue]: [exact fix] — effort: [low/medium/high]
```

**rewrite-suggestions.md** (generated by /seo rewrite or included in full audit)
```
# AutoGEO Rewrite Suggestions — [domain] — [date]

## [Page URL]

### [Section heading]
**ORIGINAL:** [original text]
**REWRITTEN:** [AutoGEO-optimized version]
**Changes:** [list of applied rules]
```

---

## Standards & Sources (2026)

- Core Web Vitals: developers.google.com/search/docs/appearance/core-web-vitals
- INP replaced FID: March 2024
- Holistic CWV scoring: Google March 2026 Core Update
- llms.txt spec: llmstxt.org (community standard, not IETF/W3C yet)
- E-E-A-T: developers.google.com/search/docs/fundamentals/creating-helpful-content
- AI Overviews ranking: 85% citations from content < 2 years old
- AutoGEO research: ICLR 2026 (cxcscmu/AutoGEO)
- GEO research: arxiv.org/abs/2311.09735 (Princeton GEO paper)
- AI crawler user agents: pulserank.ai/ai-crawlers-user-agents (updated monthly)
- IndexNow: indexnow.org (real-time indexing for Bing, Yandex, Naver, Seznam)
- Schema.org: schema.org/docs/schemas.html
- Search intent classification: Semrush/Ahrefs intent framework (4-type model)
- Brand AI visibility: Gego framework (AI2HU/gego)
