---
name: aeo-audit
description: |
  AEO (Answer Engine Optimization / AI Visibility) audit skill. Checks 4 categories: AI bot
  access (robots.txt, GPTBot, ClaudeBot), structured data (Schema.org/JSON-LD), content
  structure, and technical factors (HTTPS, sitemap, llms.txt). Scores 0-100 with
  ROI-ranked recommendations and generates a print-ready HTML/PDF report.

  Use when a user:
  - Wants to audit, check, or score a website for AI/AEO/GEO/AIO visibility
  - Asks if ChatGPT, Claude, Perplexity, or Gemini can crawl or index their site
  - Asks whether specific AI bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) are
    blocked or allowed in robots.txt — even if phrased purely as a robots.txt question
  - Wants to check or add schema markup, JSON-LD, or structured data on a site for AI systems
  - Asks about AI bot access, AI SEO, structured data for AI, Schema.org, or llms.txt
  - Wants to know if their site is "visible to AI" or "optimized for AI search"
  - Requests an AEO report, AI visibility score, or AI audit PDF
  - Wants to compare 2+ websites and determine which is better optimized for AI (comparison mode)
  - Asks about AI indexing, GEO/AIO optimization, or AI crawler permissions
  - Russian-language requests: "аудит AI-видимости", "AI-оптимизация сайта", "AEO-аудит",
    "как сайт видит ChatGPT", "видимость для AI", "индексация ботами", "видит ли Claude сайт"
  Trigger even without the word "audit" — any question about a site's AI visibility,
  crawlability, or discoverability by AI systems qualifies.
---

# AEO Audit — AI Visibility Analysis

You are performing a professional AI Visibility audit. Your job is to check how well a website
is configured to be discovered, crawled, and cited by AI systems like ChatGPT, Claude, Perplexity,
and Google's AI features. Follow this workflow precisely and completely.

## Step 1: Get the URL

If the user hasn't provided a URL, ask for it. Normalize the URL:
- Strip leading/trailing whitespace
- If it doesn't start with `http://` or `https://`, prepend `https://`
- Extract the base URL (scheme + domain only, no path): `https://domain.com`

## Step 1.5: Ask User to Confirm URLs

**First, check if the user's message already contains all 4 required URLs** (robots.txt, homepage, sitemap_index.xml, llms.txt for the domain). If yes → skip this step and proceed directly to Step 2.

Otherwise, output this message **exactly** (replacing `{base_url}` with the actual URL) and **wait for the user's reply before proceeding**:

---
To run the audit I need to fetch 4 sources. Please copy and paste the following URLs into your next message so I can access them:

```
{base_url}/robots.txt
{base_url}
{base_url}/sitemap_index.xml
{base_url}/llms.txt
```
---

Once the user sends a message containing those URLs, proceed to Step 2.

## Step 2: Fetch Data (4 WebFetch requests)

Fetch all 4 sources in this order using the URLs provided by the user. Use the exact extraction prompts below.

### 2a. Fetch robots.txt

URL: `{base_url}/robots.txt`

Prompt: "Return the COMPLETE raw text of this robots.txt file without any changes, summarization, or omissions. If the page returns a 404 error or HTML (not a robots.txt file), say exactly: 'NOT FOUND'. Otherwise return the full content."

### 2b. Fetch Homepage HTML

URL: `{base_url}`

Prompt: "Analyze this HTML page and extract the following information. Be thorough and precise:

1. JSON-LD STRUCTURED DATA: Find ALL `<script type='application/ld+json'>` tags. Return the full JSON content of each one verbatim. List each @type value found.
2. TITLE TAG: The exact text inside `<title>...</title>` and its character count.
3. META DESCRIPTION: The exact value of `<meta name='description' content='...'>` and its character count. Say 'missing' if not found.
4. HEADINGS: Count of H1 tags (include text of first H1), count of H2 tags, count of H3 tags. Note if heading levels are skipped (e.g., H1 directly followed by H3).
5. SEMANTIC HTML: Which of these elements exist in the page: article, section, nav, header, footer, main, aside. Count how many exist.
6. IMAGES: Total count of <img> tags. How many have a non-empty alt attribute? How many are missing alt or have empty alt=''.
7. OPEN GRAPH: Do any `<meta property='og:...'>` tags exist? Yes/No.
8. TWITTER CARDS: Do any `<meta name='twitter:...'>` tags exist? Yes/No.
9. CANONICAL: Does `<link rel='canonical' href='...'>` exist? If yes, what is the href?
10. LINKS: Rough count of internal links (same domain) and external links."

### 2c. Fetch Sitemap

**First:** fetch `{base_url}/sitemap_index.xml` from the URLs provided by the user.
Prompt: "Is this a valid XML sitemap? If yes, how many `<url>` or `<sitemap>` entries does it contain? Return: 'FOUND: [N] URLs' or 'NOT FOUND'."

**If NOT FOUND:** scan the already-fetched robots.txt content for any line starting with
`Sitemap:` (e.g. `Sitemap: https://example.com/custom-sitemap.xml`). If found, record the URL
and note it as "Sitemap URL declared in robots.txt: [url] (not fetched)" — count this as a
partial positive for the Technical score (+8 pts instead of +15).

### 2d. Fetch llms.txt

URL: `{base_url}/llms.txt`

Prompt: "Does this URL return a valid text file (not an HTML error page)? Return 'FOUND' if yes, 'NOT FOUND' if it's a 404 or HTML error page."

## Step 2.5: Classify Fetch Results

After all fetches, classify each result and build a **data availability map**:

| Source | Status | Meaning |
|---|---|---|
| `NOT_FOUND` (404, empty, no robots.txt) | ✅ valid | No file = permissive default (robots.txt→score 100; sitemap/llms.txt→no bonus) |
| `BLOCKED` (403, 401, timeout, connection error) | ⚠️ excluded | Data unavailable — **exclude the dependent category from scoring** |
| `SUCCESS` | ✅ valid | Data available for scoring |

**Category dependency:**
- **AI Access** depends on: robots.txt
- **Structured Data** depends on: homepage HTML
- **Content Structure** depends on: homepage HTML
- **Technical** depends on: HTTPS (derived from URL itself — always available), sitemap, llms.txt

**Exclusion rule:** If a source is BLOCKED, mark its dependent category/categories as `EXCLUDED`.
Do **not** assign 0 — simply remove from the scoring calculation entirely.

**Reason classification** (for the report):
- 403 / 401 → "Access denied — the server blocks automated requests to this URL"
- Timeout / connection error → "Site unreachable — server did not respond in time"
- Returned HTML instead of expected format → "Server returned an unexpected response (possibly a login wall or anti-bot page)"
- JS-only page (no meaningful HTML) → "Page requires JavaScript rendering — static content not accessible"

**Workarounds by reason:**
- Access denied (robots.txt) → "Open [url] in your browser and paste the text directly into the chat"
- Access denied (homepage) → "Use your browser's View Source (Ctrl+U), copy the HTML, and paste it here"
- Site unreachable → "Verify the site is online, then retry"
- JS-rendered page → "Your site uses client-side rendering; consider adding server-side rendering or a static HTML fallback"

## Step 3: Score Each Category

For the exact scoring formulas and point values, read `references/scoring.md`.

Here is the summary:

### 3a. AI Access Score (final weight: 20%)

Parse robots.txt for these 8 bots (in order of importance):
GPTBot (weight 25), ClaudeBot (weight 25), PerplexityBot (weight 20),
Google-Extended (weight 15), CCBot (weight 10), anthropic-ai (weight 3),
Bytespider (weight 1), cohere-ai (weight 1).

**If robots.txt NOT FOUND:** Score = 100 (all bots allowed by default).

**For each bot:** Check its specific User-agent block first, then fall back to `User-agent: *`.
- No disallow rules, or only empty `Disallow:` → **full access (100 pts)**
- Only non-critical paths blocked (admin, wp-admin, search, feeds, cgi-bin) → **full access (95 pts)**
- Some paths blocked but not critical content → **partial access (70 pts)**
- Critical content paths blocked (/, /blog, /about, /services) → **limited access (40 pts)**
- `Disallow: /` without `Allow: /` override → **blocked (0 pts)**
- Apply crawl-delay penalty: delay≥10s → -15pts, delay 5-9s → -10pts, delay 1-4s → -5pts

Final AI Access Score = weighted average of all bot scores ÷ total weights (100).

### 3b. Technical Score (final weight: 20%)

- HTTPS (URL starts with https://): **+25 pts**
- HTTP Status 200: **+25 pts** (301/302 redirects: +15 pts)
- Response time: fast (<500ms) **+20**, ok (500-1000ms) **+15**, slow (1-2s) **+10**, very slow (2-3s) **+5**
  - When unknown from WebFetch, estimate based on site type (CDN-hosted → assume fast)
- Redirect count: 0 **+10**, 1 **+7**, 2 **+4**, 3+ **+0**
- Sitemap found + valid XML: **+15 pts** (found but invalid: +8 pts)
- llms.txt found: **+5 pts** bonus

Max: 100 pts.

### 3c. Structured Data Score (final weight: 25%)

- Any JSON-LD present: **+40 pts** base
- High-priority schemas found — 10pts each, max 30:
  Organization, WebSite, Article, FAQPage
- Medium-priority schemas found — 5pts each, max 15:
  HowTo, Product, Service, LocalBusiness
- Schema variety bonus: 2pts per unique @type, max 10
- Microdata (itemscope) or RDFa (typeof) present: **+5 pts** bonus

Max: 100 pts.

### 3d. Content Structure Score (final weight: 35%)

- H1 tag present: **+15 pts**
- Valid heading hierarchy (no skipped levels, e.g. H1→H3): **+10 pts**
- Title tag present: **+10 pts** (+5 bonus if 30-60 chars)
- Meta description present: **+10 pts** (+5 bonus if 70-160 chars)
- Image alt coverage ≥90%: **+15 pts** (≥70%: +10, ≥50%: +5, no images: full 15pts)
- Semantic HTML (3+ of: article/section/nav/header/footer/main/aside): **+10 pts**
- Open Graph tags present: **+5 pts** bonus
- Twitter Cards present: **+5 pts** bonus
- Internal links ≥5: **+5 pts** bonus

Max: 100 pts.

## Step 4: Calculate Overall Score

Use only the categories that are **not EXCLUDED**. Redistribute weights proportionally:

```
available_weight_sum = sum of original weights for non-excluded categories
adjusted_weight(C) = original_weight(C) / available_weight_sum

overall_score = round( sum of: score(C) × adjusted_weight(C) for each non-excluded C )
```

**Example:** If homepage is BLOCKED → Structured Data (25%) and Content Structure (35%) are excluded.
Remaining: AI Access (20%) + Technical (20%) → available_weight_sum = 0.40
→ adjusted: AI Access = 50%, Technical = 50%
→ overall_score = round(ai_access × 0.50 + technical × 0.50)

If **all 4 categories are excluded** (extreme case) → do not produce a numeric score;
instead state "Score unavailable — insufficient data" and focus entirely on the workaround section.

**Interpretation** (applies only when ≥2 categories are available):
- 80-100: Excellent AI visibility
- 65-79: Good, minor improvements needed
- 50-64: Needs significant work
- Below 50: Critical issues — site is poorly visible to AI systems

## Step 5: Generate Recommendations

For the full recommendations catalog, read `references/recommendations.md`.

Build a list of applicable recommendations based on what's missing or broken. Sort by ROI
(highest impact ÷ lowest effort first). Show maximum 8 recommendations in the report.

Always include:
- Priority: high / medium / low
- Title + description
- Code example (for robots.txt fixes, schema markup, meta tags)
- Time estimate

## Step 6: Generate Inline Visual Report

Read `assets/chat-report-template.html` — it is a working example of the exact visual format
and CSS structure to follow. Then generate a **new HTML visual** populated with the actual
audit data and output it **directly in the chat message** (NOT as an artifact, NOT in a side panel).

**Rules for the inline visual:**
- Use Claude's UI CSS variables for all colors and spacing — do NOT hardcode hex colors:
  `var(--color-text-primary)`, `var(--color-text-secondary)`, `var(--color-text-tertiary)`,
  `var(--color-background-primary)`, `var(--color-background-secondary)`, `var(--color-background-tertiary)`,
  `var(--color-border-tertiary)`, `var(--color-border-secondary)`,
  `var(--border-radius-lg)`, `var(--border-radius-md)`,
  `var(--font-sans)`, `var(--font-mono)`
- Exception: score-color pills and status indicators use fixed semantic colors:
  green `#22c55e`, yellow `#eab308`, orange `#f97316`, red `#ef4444`,
  pill backgrounds from the template (e.g. `#dcfce7`/`#15803d` for green pills)
- Do NOT include `<html>`, `<head>`, or `<body>` tags — output `<style>` + `<div class="wrap">` only
- Max width: `720px` (same as template)

**Sections to include (in order):**
1. **Header** — domain, audit date, score badge
2. **⚠️ Data Collection Limitations** *(only if any source was BLOCKED — omit if all data OK)*
   - Table: source | reason | affected categories | workaround
3. **Score Overview** — category bars with weights; EXCLUDED categories shown greyed-out with "Data unavailable" label
4. **AI Bot Access** — bot table with status pills; if EXCLUDED show reason+workaround banner
5. **Technical Checklist** — 2-column grid (HTTPS, HTTP status, response time, redirects, sitemap, llms.txt)
6. **Structured Data** — schemas found/missing table; if EXCLUDED show banner
7. **Content Structure** — 2-column checklist; if EXCLUDED show banner
8. **Top Recommendations** — ROI-sorted cards with priority pill, description, code block
9. **Footer** — "Generated by ICODA AI Visibility Checker · date"

## Step 7: Brief Text Summary + PDF Offer

After the inline visual, output a short text summary in the user's language:

```
**[Domain] — AI Visibility Score: [N]/100**
[One-sentence interpretation]

[Only if any sources were BLOCKED:]
⚠️ **Incomplete data:** [N] of 4 categories excluded — [reason]. [One-line workaround.]

**Top 2 quick wins:**
- [Highest-ROI fix — time estimate]
- [Second fix — time estimate]
```

Then ask:
> "Сгенерировать полный PDF-отчёт для печати?" / "Generate a full print-ready PDF report?"

## Step 8: Generate PDF Artifact (only if user says yes)

If the user replies affirmatively, read `assets/report-template.html` to understand the layout
and CSS. Generate a complete standalone HTML **artifact** (all CSS in `<style>` tags, no external
dependencies, ICODA brand colors #3C50E0 / #1D2A4D) with the same data as the inline visual.
The user prints it to PDF via browser Print → Save as PDF.

## Important notes

**Graceful degradation:** Distinguish between NOT_FOUND (valid, scoreable data) and BLOCKED
(inaccessible — exclude category from scoring, show reason + workaround in report).
Never assign 0 to a category just because data was inaccessible. Never fail the whole audit.

**Language:** Always respond in the same language the user wrote in. Russian request → Russian
response and Russian report. English request → English report.

**robots.txt parsing precision:**
- `Disallow:` (empty value) = allow everything
- `Disallow: /` = block everything (unless overridden by `Allow: /`)
- Case-insensitive user-agent matching
- Bot inherits wildcard (`*`) rules if no specific rule exists

**Comparison mode:** If user provides 2 URLs, run the full analysis for each and add a
side-by-side score comparison table at the top of the report.

**No live microservice needed:** This skill performs all analysis directly via WebFetch.
Do not try to call any local API endpoints.
