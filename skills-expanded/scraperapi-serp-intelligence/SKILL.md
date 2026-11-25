---
name: scraperapi-serp-intelligence
description: >
  SERP landscape analysis for SEO strategy decisions. Use this skill when the
  user wants to understand what a search results page actually looks like for
  their target keywords — including AI Overview presence and attribution, SERP
  feature composition, how Google is interpreting query intent, which competitors
  dominate specific keyword sets, and where organic rankings actually translate
  to visible traffic. Trigger on requests like "analyze the SERP for [keyword],"
  "why isn't my content getting traffic even though it ranks," "what does Google
  show for [keyword]," "which keywords are worth targeting," "is [keyword]
  dominated by AI Overviews," "who owns the SERP for [topic]," "SERP analysis,"
  or "keyword landscape."

  Note: Transmits user-supplied queries, URLs, and content to ScraperAPI.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "🎯"
    homepage: https://docs.scraperapi.com/
---

# SERP Intelligence

Live SERP landscape analysis powered by ScraperAPI's real-time search data. Answers the question rank trackers can't: *what does this SERP actually look like, and what does my position within it mean?*

**You — Claude — execute the tool calls directly.** Do not generate code for the user or explain how they could run these calls themselves. Call the MCP tools, read the results, and report findings. The user wants SERP analysis, not instructions.

**Never answer SERP questions from training knowledge.** SERP features change constantly by query, location, and device. Always gather live data first, then analyze and synthesize.

---

## MCP Tools Available

| Tool | What it returns |
|------|----------------|
| `mcp__ScraperAPIRemote__google_search` | Full structured SERP — organic results, featured snippets, PAA, shopping, knowledge panels, related searches |
| `mcp__ScraperAPIRemote__google_news` | News results for a query — useful for understanding news pack presence and freshness signals |
| `mcp__ScraperAPIRemote__google_shopping` | Shopping results and pricing — confirms transactional intent and commercial SERP structure |
| `mcp__ScraperAPIRemote__scrape` | Full page content for a specific URL — use to read AI Overview citations or examine top-ranking content structure |

### Render guidance for `scrape`
When calling `mcp__ScraperAPIRemote__scrape`, set `render=true` and `premium=true` for any page that requires JavaScript to display content — Google search result pages, LinkedIn profiles, Crunchbase, React/SPA-based sites (e.g. G2 grids). Use standard (no render flags) for static HTML pages: news articles, Wikipedia, company homepages, GitHub, and most `/pricing` pages.

### Structured parser limitations for `google_search`
The `google_search` tool returns parsed JSON, not raw HTML. Its parser does not reliably handle all SERP result types. Known gaps:

- **Sitelinks blocks** — A result with sitelinks (sub-links to Careers, About, Contact, etc.) is typically the #1 organic result for a brand query. The parser often drops it entirely, causing organic positions to start at #4 or #5. This does NOT mean positions 1–3 are occupied by a knowledge panel or other feature — they may simply have been dropped by the parser.
- **Knowledge panels** — May be partially or fully absent from structured output.
- **AI Overviews** — May be detected but with empty content (use the scrape fallback in this case).

**When organic results don't start at position 1, always follow up with a rendered scrape of the Google search URL to confirm what is actually above the fold:**

```
mcp__ScraperAPIRemote__scrape  url="https://www.google.com/search?q=[url-encoded-query]"  render=true  premium=true
```

Read the returned HTML visually to identify any results the structured parser missed. Never assume missing positions are explained by SERP features — verify first.

---

## Core Workflow

For every SERP intelligence request:

1. **Select mode** — Keyword Scan (1–5 keywords) or Keyword Set Analysis (6–20). If the user provides more than 20 keywords, ask them to prioritize or group by topic cluster.
2. **Clarify the decision** — What is the user trying to decide? This shapes which analysis to foreground.
3. **Gather live SERP data** — Call `google_search` for each keyword. Parallelize all calls.
4. **Read each SERP** — Extract features, classify intent, assess effective visibility.
5. **Synthesize** — Classify keywords as open / contested / closed. Map competitive presence. Signal content format.

## Data Collection Rules

- **Parallelize** — Issue all independent `google_search` calls in a single response turn, not sequentially.
- **Be efficient** — A Keyword Scan uses 1 call per keyword plus up to 2 follow-up calls. A Keyword Set Analysis uses 1 per keyword plus up to 3 follow-up calls for the highest-signal findings.
- **Handle failures honestly** — If a SERP returns empty or features are unconfirmed, say so. Never infer SERP state from training knowledge.
- **Cite every data point** — Include the exact query run. Users must be able to trace every claim.
- **Date-stamp every report** — Include "Data collected on [date]" so users know freshness.

---

## Scan Modes

### 1. Keyword Scan (1–5 keywords)

**When to use**: User supplies a small number of specific keywords, asks about a single SERP, or wants to understand one query in depth.

**Data gathering**:
```
# Run one search per keyword (run in parallel)
mcp__ScraperAPIRemote__google_search  query="[keyword 1]"
mcp__ScraperAPIRemote__google_search  query="[keyword 2]"

# If shopping signals appear in organic results, confirm with:
mcp__ScraperAPIRemote__google_shopping  query="[keyword]"

# If a news pack appears, confirm freshness signal with:
mcp__ScraperAPIRemote__google_news  query="[keyword]"

# If an AI Overview appears and citations are visible, scrape a cited source:
mcp__ScraperAPIRemote__scrape  url="[cited-source-url]"

# AI Overview fallback — if ai_box is detected but content is empty:
mcp__ScraperAPIRemote__scrape  url="https://www.google.com/search?q=[url-encoded-keyword]"  render=true  premium=true
# Parse returned HTML for AI Overview text and source citations.
# If still unrecoverable, flag as "AI Overview detected, content unconfirmed" — never assume absent.
```

**Analysis**: For every keyword, extract and assess:

*SERP features present* (mark each Y/N, note position):
- AI Overview — Y/N. If Y: how many sources cited? Are source URLs visible?
- Featured snippet — Y/N. If Y: which domain? Format (paragraph, list, table)?
- People Also Ask — Y/N. If Y: what are the exact questions? These reveal adjacent intent gaps.
- Local pack — Y/N. If Y: geo-modified intent, even if no location was typed.
- Shopping carousel — Y/N. If Y: strong transactional signal regardless of query phrasing.
- Video results — Y/N. If Y: Google favors video answers for this intent.
- Knowledge panel — Y/N. If Y: entity-based query; brand authority matters more than links.
- News pack — Y/N. If Y: freshness is a ranking factor for this topic.

*Organic results (top 5)*: domain, URL, title, snippet, content format signal (guide, product page, comparison, definition, news, tool).

*Intent classification* — derive from SERP composition, not query text:
- *Informational* — user wants to learn
- *Transactional* — user wants to buy or act
- *Navigational* — user wants a specific site or resource
- *Commercial investigation* — researching before a decision
- *Mixed* — Google serves multiple intents; usually means the query is ambiguous and harder to rank for

*Effective visibility* — translate rank into realistic traffic given page context:
- *High* — No AI Overview, no shopping carousel. Organic positions 1–3 above the fold.
- *Medium* — AI Overview present but compact, or one major feature above organic. Position 1–2 still visible.
- *Low* — Full AI Overview plus additional features. Organic results below the fold.
- *Very low* — AI Overview fully answers the query with attributed citations. Unless cited, this SERP is largely closed to organic traffic regardless of rank.

**Output format**:

```
# SERP Intelligence: [Keyword(s)]
*Data collected on [YYYY-MM-DD]*

## Decision context
[What the user is trying to decide, stated explicitly]

---

## [Keyword 1]

**Query run:** `[exact query string]`

### Raw SERP data
*Exactly as returned by the tool — no interpretation applied.*

**SERP features detected:**
| Feature | Present | Raw detail |
|---------|---------|-----------|
| AI Overview | Yes/No | [Content and citations if captured; "detected, content unconfirmed" if empty] |
| Featured snippet | Yes/No | [Exact snippet text and source URL if present] |
| People Also Ask | Yes/No | [Exact questions as shown] |
| Local pack | Yes/No | — |
| Shopping carousel | Yes/No | — |
| Video results | Yes/No | — |
| News pack | Yes/No | — |

**Organic results (as returned):**
| # | Title | URL | Snippet |
|---|-------|-----|---------|
| 1 | [exact title as shown in SERP] | [full URL] | [snippet text] |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |

---

### Analysis
*Claude's interpretation — clearly separated from raw results.*

#### AI Overview
[If confirmed: sources cited, content type, what earning citation likely required.
If detected but unconfirmed: note the limitation.
If absent: note that organic results are unobstructed.]

#### Intent read
**Classification:** [Informational / Transactional / Commercial investigation / Navigational / Mixed]
**Basis:** [What the SERP composition — not the query text — tells you about how Google reads this query]

#### Effective visibility
**Level:** [High / Medium / Low / Very low]
**Basis:** [Which confirmed features sit above organic and what this means for traffic at each position]

---

[Repeat for each keyword]

---

## Synthesis

### Where to focus
[Which keywords are open for organic investment vs. contested vs. effectively closed — with reasoning]

### Content format signal
[What format Google consistently favors across these keywords]

### Competitive presence
[Which domains recur across these SERPs and what that means]

## Implications
**Immediately actionable:** [Specific next step based on findings]
**Near-term:** [Content or strategy decisions for this quarter]
**To monitor:** [Signals that haven't resolved yet but are worth watching]

## Data notes
[Any queries with thin results, geo-variation warnings, or features that couldn't be confirmed from structured data alone]
```

---

### 2. Keyword Set Analysis (6–20 keywords)

**When to use**: User supplies a topic cluster, a list of target keywords, or asks for a landscape read across a content strategy. Deliver per-keyword breakdowns plus a cross-set synthesis.

**Data gathering**:
```
# Run all keyword queries in parallel
mcp__ScraperAPIRemote__google_search  query="[keyword 1]"
mcp__ScraperAPIRemote__google_search  query="[keyword 2]"
mcp__ScraperAPIRemote__google_search  query="[keyword 3]"
# ... (one call per keyword)

# Follow-up calls (up to 3) for the highest-signal findings:

# If shopping signals appear in organic results:
mcp__ScraperAPIRemote__google_shopping  query="[keyword]"

# If a news pack appears:
mcp__ScraperAPIRemote__google_news  query="[keyword]"

# If an AI Overview is detected and a cited source warrants deeper inspection:
mcp__ScraperAPIRemote__scrape  url="[cited-source-url]"
```

**Analysis**: Apply the same per-keyword analysis as Keyword Scan (features, intent, effective visibility). Then add cross-set synthesis:

*AI absorption rate* — What share of the keyword set triggers AI Overviews? High absorption means the topic is being captured by AI answers. The user may need to shift from targeting these queries with content to targeting adjacent queries or focusing on being cited rather than ranked.

*Open / Contested / Closed classification*:
- *Open* — Clean SERP, informational intent, no AI Overview, organic results in formats the user can compete with.
- *Contested* — Established competitor presence in organic, but no AI Overview or featured snippet lock-in. Competitive but worth playing.
- *Closed* — AI Overview fully answers the query, featured snippet held by a source unlikely to be displaced, or transactional SERP where the user's site doesn't sell the product.

*Competitive SERP map* — Build a domain frequency count across the keyword set. The top 3–5 recurring domains are the real SEO competitors on this topic, regardless of who shows up in a traditional competitor search.

*Content format signal* — What format does Google consistently favor across the set? Mismatching format to intent is one of the most common reasons well-written content fails to rank.

**Output format**:

```
# SERP Intelligence Report: [Topic / Keyword Set]
*Data collected on [YYYY-MM-DD] | [N] keywords analyzed*

## Decision context
[What the user is trying to decide]

## Keyword landscape overview

| Keyword | AI Overview | Top feature | Intent | Dominant domain | Visibility for organic |
|---------|-------------|------------|--------|-----------------|----------------------|
| [kw 1] | Yes/No | [feature] | [intent type] | [domain] | High/Med/Low/Very low |
| [kw 2] | | | | | |

## Keyword classification
**Open for organic investment:** [list]
**Contested but worth pursuing:** [list]
**Effectively closed to organic:** [list]

---

## Per-keyword SERP breakdowns
[Full breakdown for each keyword — same format as Keyword Scan output]

---

## Cross-set synthesis

### AI absorption summary
[What share of the set triggers AI Overviews, which topic areas are most absorbed, what this means for strategy]

### Competitive SERP map
| Domain | Appearances | Positions held | Featured snippets | AI Overview citations |
|--------|-------------|---------------|-------------------|----------------------|
| [domain] | [N/total] | [e.g., 1–3 across 6 keywords] | [N] | [N] |

### Content format signal
[What formats Google consistently favors — guides, product pages, comparisons, definitions, videos]

### Where the real opportunity is
[Specific keywords or sub-topics where the SERP is open and the content format is one the user can execute]

## Implications
**Immediately actionable:** [Highest-confidence next step]
**Near-term:** [Content planning decisions for this quarter]
**Strategic:** [What this keyword set tells you about the broader content territory]

## Data notes
[Anything that couldn't be confirmed, geo-variation, thin results, features that required inference]
```

---

## Scan Mode Selection Guide

| User says... | Mode |
|---|---|
| "Analyze this keyword" / "What does the SERP look like for [keyword]" | Keyword Scan |
| "Why isn't my content getting traffic even though it ranks" | Keyword Scan |
| "Is [keyword] dominated by AI Overviews" | Keyword Scan |
| "Should I create content for [keyword]" | Keyword Scan |
| "Which keywords in this set are worth prioritizing" | Keyword Set Analysis |
| "SERP landscape for this topic cluster" / "keyword landscape" | Keyword Set Analysis |
| "Who are my real SEO competitors on these topics" | Keyword Set Analysis |
| "Full content strategy audit across these keywords" | Keyword Set Analysis |

---

## Output Quality Standards

1. **Every SERP claim cites the query.** If the output states "an AI Overview appears for [keyword]," the query that produced that result must be named. No findings from memory or inference.
2. **AI Overview presence is the first thing to check.** For every keyword, determine AI Overview presence before commenting on organic rank. Rank without this context is incomplete.
3. **Intent comes from what the SERP shows, not the query text.** Read the evidence — features present, content formats in top results — before classifying. Do not guess from keyword phrasing alone.
4. **Effective visibility is not the same as rank.** Always translate position into a visibility level given the features above organic. A practitioner who sees "you rank #2" without knowing there's a full-viewport AI Overview above position one is making decisions with incomplete information.
5. **What the data can't tell you belongs in Data Notes.** Historical trends, CTR, impressions, backlinks, Core Web Vitals — none are derivable from SERP scraping. Say so, and point to the right tool: Search Console for CTR and impressions, Ahrefs/Semrush for historical rank and backlinks, PageSpeed Insights for CWV.
6. **Don't run unbounded queries.** For keyword sets over 20, ask the user to prioritize. Document the keyword budget used in every report.
7. **Separate data from interpretation.** Clearly distinguish what was returned by the tool from what Claude inferred.
