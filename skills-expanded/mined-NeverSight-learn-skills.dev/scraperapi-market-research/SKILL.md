---
name: scraperapi-market-research
description: >
  Market research powered by live web data. Use this skill when the user wants
  to understand a market, category, or customer segment — including consumer
  sentiment, demand and trend signals, price and category structure, or the
  competitive landscape. Trigger on requests like "research the [X] market,"
  "what do customers think about [category]," "how is [category] priced,"
  "what trends are shaping [industry]," "who are the players in [space],"
  or any request to understand a market before making a product, pricing,
  positioning, or investment decision.
metadata:
  openclaw:
    requires:
      env:
        - SCRAPERAPI_API_KEY
    emoji: "📊"
    homepage: https://docs.scraperapi.com/
---

# Market Research

Live market research powered by ScraperAPI's web scraping infrastructure. Pulls structured data from search engines, product platforms, review sites, job boards, and any public URL — then synthesizes it into research-grade analysis.

**You — Claude — execute the tool calls directly.** Do not generate code for the user or explain how they could run these calls themselves. Call the MCP tools, read the results, and report findings. The user wants research, not instructions.

**Start with the research question, not the data source.** Before collecting anything, identify what decision the user is trying to inform. The same market looks completely different depending on whether you're trying to enter it, price against it, or understand why customers leave it.

**Never answer market research questions from training knowledge alone.** Always gather live data first, then analyze and synthesize. Training data has a cutoff; markets don't.

---

## MCP Tools Available

| Tool | Best used for | Render needed? |
|------|--------------|---------------|
| `mcp__ScraperAPIRemote__google_search` | Discovering sources, mapping player presence, SERP analysis | No |
| `mcp__ScraperAPIRemote__google_news` | Trend signals, recent market moves, funding and launches | No |
| `mcp__ScraperAPIRemote__google_shopping` | Category pricing structure, product listings at scale | No |
| `mcp__ScraperAPIRemote__google_jobs` | Market-level hiring signals, technology bets, expansion patterns | No |
| `mcp__ScraperAPIRemote__scrape` | Any public URL — homepages, pricing pages, blog indexes, review pages | See note |
| `mcp__ScraperAPIRemote__amazon_product` | Product detail, ratings, review summaries | No |
| `mcp__ScraperAPIRemote__amazon_search` | Category structure, bestseller rankings, price distribution | No |
| `mcp__ScraperAPIRemote__amazon_offers` | Seller landscape, price variation across sellers | No |
| `mcp__ScraperAPIRemote__walmart_product` | Product detail and pricing | No |
| `mcp__ScraperAPIRemote__walmart_search` | Category structure and pricing on Walmart | No |
| `mcp__ScraperAPIRemote__walmart_review` | Consumer sentiment on physical products | No |
| `mcp__ScraperAPIRemote__ebay_product` | Secondary market pricing, product condition distribution | No |
| `mcp__ScraperAPIRemote__ebay_search` | Resale market structure and demand signals | No |
| `mcp__ScraperAPIRemote__crawler_job_start` | Deep research requiring many pages (blog indexes, full review sets) | — |
| `mcp__ScraperAPIRemote__crawler_job_status` | Check async crawl job status | — |

### Render guidance for `scrape`

When calling `mcp__ScraperAPIRemote__scrape`, set `render=true` and `premium=true` for any page that requires JavaScript to display content — LinkedIn profiles, Crunchbase, React/SPA-based sites (e.g. G2 grids, Glassdoor). Use standard (no render flags) for static HTML pages: news articles, Wikipedia, company homepages, GitHub, and most `/pricing` pages. JS-rendered calls cost significantly more credits — reserve them for pages where a standard fetch is known to return a shell.

### Async crawler workflow

Use `crawler_job_start` when a research task requires fetching many pages at once (e.g. scraping a full review index, a blog archive, or a large product category). Pattern:

1. Call `mcp__ScraperAPIRemote__crawler_job_start` with the target URL and crawl parameters.
2. Note the `job_id` returned.
3. Call `mcp__ScraperAPIRemote__crawler_job_status` with that `job_id` every 10–15 seconds until `status` is `"completed"` or `"failed"`.
4. On `"completed"`, retrieve and synthesize the results. On `"failed"`, log the failure and continue with whatever data you have.

Do not use the async crawler for single-page fetches — use `scrape` directly.

---

## Core Workflow

1. **Probe for missing parameters** — Before any research, check whether the request leaves critical parameters ambiguous. If any are unclear, ask in a single message before proceeding. Do not start gathering data until you have answers. See "Parameter Probing" below.
2. **Clarify the research question** — What decision does this research inform? Who is the audience? Select the right module(s).
3. **Announce before searching** — State what you already know and what you're looking for before the first tool call.
4. **Gather live data** — Call ScraperAPI MCP tools. Parallelize independent calls by issuing multiple tool calls in a single response turn.
5. **Analyze with the right framework** — Each module has a specific analytical method. Apply it.
6. **Deliver with honest uncertainty** — Distinguish what the data shows from what you're inferring. Flag sampling limitations. Close with specific, tiered recommendations.
7. **File a gap report** — After each module's output, list high-priority areas that weren't filled and suggest one concrete follow-up per gap.

---

## Parameter Probing

Check the user's request against the four parameters below. If a parameter is missing **and** the default would meaningfully change the scope or usefulness of the research, ask about it. Ask all unclear parameters in one message — never ask one at a time across multiple turns.

| Parameter | Default if not specified | When to ask |
|-----------|--------------------------|-------------|
| **Geography** | United States | Always ask if not stated. A market analysis scoped to the US looks very different from one scoped to the EU, UK, or global — and the wrong default wastes the research. |
| **Modules** | Full multi-module report (all four) | Ask if the user seems to want a specific angle (e.g. "how is this market priced?" → Price & Category only). Don't ask if the request is clearly broad ("research this market"). |
| **Decision context** | General market understanding | Ask if knowing the decision would materially change what to emphasize. E.g. "are you considering entering this market, pricing against it, or understanding why customers leave?" |
| **Time horizon / recency** | Last 12–24 months | Ask only if the category is known to change fast (e.g. AI tools, crypto) or if the user signals historical interest. Default to recent data otherwise. |

**Probing rules:**
- Ask only about parameters that are genuinely ambiguous. If the request says "research the UK organic dog food market," geography is answered — don't ask again.
- Keep the probe short. One sentence of context, then the question. No preamble.
- If two or more parameters need clarification, ask them together in a single message, not sequentially.
- If a parameter has a sensible default and getting it wrong would be easy to correct, proceed with the default and state your assumption: *"I'll scope this to the US — let me know if you want a different market."*

**Example probe (geography missing, decision context helpful):**

> Before I start: which market should I scope this to — US, UK, EU, or global? And is there a specific decision driving this — market entry, pricing, or general landscape?

**Example with stated assumption (minor ambiguity):**

> Scoping this to the US and running all four modules. Let me know if you'd like a different geography or a narrower focus.

---

## Data Collection Rules

- **Parallelize** — Issue independent MCP tool calls in a single response turn to save time.
- **Collect to saturation, not to exhaustion** — Stop when new sources are confirming existing findings, not adding new ones. A good snapshot uses 4–10 calls.
- **Prefer structured tools over scrape** — When a structured tool exists (amazon_search, walmart_review, google_shopping), use it. Structured data is cleaner than parsed HTML.
- **Handle failures honestly** — If a page is gated or returns empty, say so and try a fallback. Never fill gaps with training knowledge presented as live data.
- **Cite every data point** — Include source URLs. Users must be able to verify.
- **Date-stamp every report** — "Data collected on [YYYY-MM-DD]" so users know how fresh it is.

---

## Stop Conditions

Stop gathering data when any of the following is true:

- All high-priority fields for the active module are filled.
- You have made **10 or more tool calls** without discovering new information.
- **3 or more consecutive calls** returned errors, empty results, or gated content.
- The user explicitly asks you to stop or move to synthesis.

When you hit a stop condition, announce it: *"Stopping data collection: [reason]. Moving to synthesis with what I have."* Do not loop past these limits.

---

## Error Handling

| Response | What to do |
|----------|-----------|
| Empty result / no data returned | Try one alternative source (different query or URL). If still empty, log the gap and continue. |
| Gated / paywalled content | Note it. Try a Google search snippet for the same data instead. Never guess at gated content. |
| 429 rate limit | Wait 5 seconds, then retry once. If still 429, stop collecting and note the limit in the gap report. |
| 500 / 503 server error | Wait 3 seconds, retry once. Skip on second failure. Count against the 10-call stop condition. |
| Completely irrelevant result | Skip without retry. Do not count against the stop condition — query a different source instead. |

---

## Analysis Modules

### 1. Consumer Sentiment Analysis

**Research question answered:** What do people who publicly discuss this category want, fear, and complain about?

**When to use:** User wants to understand customer needs, pain points, unmet demands, or sentiment within a product category or market segment — not just about one company.

**Before gathering, announce:** *"Starting consumer sentiment research on [category]. Looking for: what the market values, recurring complaints, unmet needs, and switching mentions. Will search G2, Reddit, Capterra, and product review platforms."*

**Data gathering — call these tools, reading results as they return:**

Run these in parallel (first batch):
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] review site:g2.com OR site:capterra.com"` — surfaces software review pages
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] complaints OR problems OR wish site:reddit.com"` — surfaces Reddit discussions
- Call `mcp__ScraperAPIRemote__google_search` with `query = "best [category] [year] reviews"` — surfaces roundup content

From the URLs returned, select the 2–3 most information-dense sources and fetch them (second batch, run in parallel):
- Call `mcp__ScraperAPIRemote__scrape` with the G2 category grid URL (use `render=true, premium=true`)
- Call `mcp__ScraperAPIRemote__scrape` with the most relevant Reddit thread URL (standard fetch)
- Call `mcp__ScraperAPIRemote__scrape` with the Capterra category URL (standard fetch)

For physical product categories, add (run in parallel with above):
- Call `mcp__ScraperAPIRemote__amazon_search` with `query = "[category]"` — top products reveal what the market buys
- Call `mcp__ScraperAPIRemote__amazon_product` with the URL of the top-ranked product — for review summary and themes
- Call `mcp__ScraperAPIRemote__walmart_review` with a top product URL — for cross-platform sentiment

Then pull a recency pass:
- Call `mcp__ScraperAPIRemote__scrape` with `[g2-url]?order=recent` — recent vs. top-rated reviews often diverge meaningfully

**Analysis rules:**

- **Volume threshold:** Draw no conclusions from fewer than 15 distinct data points. Under 10 is directional only — flag it.
- **Thematic coding:** Don't list quotes. Identify recurring themes. A theme earns a place in the report when it appears independently across at least 2–3 sources or is mentioned by a meaningful share of reviewers.
- **Frequency vs. severity:** A complaint mentioned often but described mildly is different from one mentioned rarely but described as a dealbreaker. Note both dimensions.
- **Recency weighting:** Prioritize the past 12 months. If most data is older, say so — it may mean the market has shifted or reviews have stagnated.
- **Verified vs. unverified:** G2 and Capterra mark verified purchasers. Weight these more heavily. A sudden spike in review volume often signals a review campaign, not organic sentiment growth.
- **Complaint categorization:** Separate complaints by root cause — reliability/performance, pricing/value, support quality, documentation/onboarding, missing features. Each category points to a different kind of market gap.
- **Saturation check:** When new sources stop introducing new themes, you have enough data. Note this in the report.
- **Sampling caveat:** Review platforms over-represent customers with strong opinions. The silent majority — satisfied or indifferent — doesn't leave reviews. Flag this limitation in the output.

**Output format:**

```markdown
# Consumer Sentiment Analysis: [Category/Market]
*Data collected on [YYYY-MM-DD]*
*Sources: [list URLs] | Reviews analyzed: ~[N] | Date range: [oldest–newest]*

## Research question
[State what decision this analysis informs]

## Raw data collected
*Unfiltered — exactly what the tools returned before any interpretation.*

| Source | URL | Content type | Date | Notable raw finding |
|--------|-----|-------------|------|-------------------|
| [G2 / Reddit / Capterra / etc.] | [url] | [review page / thread / listing] | [date] | [verbatim snippet or data point as returned] |

---
*Analysis below is Claude's interpretation of the above sources. Raw sources above can be visited directly to verify.*

---

## What the market consistently values
[3–5 themes, each with representative verbatims and source links]

> "[Direct quote]" — G2, [Month YYYY] ([url])

## Where the market is underserved

### Reliability/Performance
[Theme + frequency signal + verbatims, or "No significant pattern found"]
> "[Direct quote]" — Reddit, [Month YYYY] ([url])

### Pricing/Value
[Theme + verbatims]

### Support
[Theme + verbatims]

### Documentation/Onboarding
[Theme + verbatims]

### Missing features
[Specific capabilities users name repeatedly, with verbatims]

## Conflicting signals
[Where positive and negative reviews contradict — note whether this correlates with recency, platform, or plan tier]

## Switching and comparison mentions
[Direct quotes where users name alternatives or describe switching — highest-signal data]
> "[We moved from X because...]" — [source, date, url]

## Data confidence notes
[Sampling limitations, review profile anomalies, any gaps in coverage]

## Implications
**Immediate:** [What this suggests to act on now]
**Near-term:** [Product, positioning, or messaging conclusions for this quarter]
**Strategic:** [What this suggests about where the market is heading]

## Gap report
| Gap | Why it wasn't filled | Suggested follow-up |
|-----|---------------------|-------------------|
| [e.g. Review data thin or old] | [e.g. G2 category has <20 reviews] | [e.g. Try scraping G2 sorted by most recent, or search `site:trustpilot.com [category]`] |
| [e.g. Reddit threads not found] | [e.g. No relevant subreddit surfaced] | [e.g. Search `[category] site:news.ycombinator.com` for HN discussion] |
```

---

### 2. Demand & Trend Signals

**Research question answered:** Is this market growing or shrinking, and where is consumer attention shifting?

**When to use:** User wants to understand market momentum, identify emerging sub-categories, time a product launch or market entry, or spot demand shifts before they're obvious.

**Before gathering, announce:** *"Starting demand and trend research on [category]. Looking for: funding and investment activity, content volume and recency, product market movement, and hiring patterns as a leading indicator."*

**Data gathering — call these tools, reading results as they return:**

Run these in parallel (first batch):
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] [year]"` — checks recency of discussion
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] growing OR declining OR trend"` — surfaces explicit trend claims
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[emerging sub-category or related term]"` — tests adjacent demand

Run these in parallel (second batch):
- Call `mcp__ScraperAPIRemote__google_news` with `query = "[category] funding OR launch OR acquisition"` — money movement signals
- Call `mcp__ScraperAPIRemote__google_news` with `query = "[category] trend OR forecast OR growth"` — analyst and press signals

Run these in parallel (third batch):
- Call `mcp__ScraperAPIRemote__amazon_search` with `query = "[category]"` — bestseller rankings reveal current demand shape
- Call `mcp__ScraperAPIRemote__google_shopping` with `query = "[category]"` — new entrants and price movement
- Call `mcp__ScraperAPIRemote__google_jobs` with `query = "[category] [key role]"` — hiring as a leading indicator of where companies are investing

**Analysis rules:**

- **Leading vs. lagging indicators:** News coverage of a trend is a lagging indicator — it confirms what's already happening. Hiring patterns and new product launches are leading indicators — they suggest where investment is going before outcomes are visible. Label them accordingly.
- **Signal triangulation:** A trend claim needs at least two independent signals. One news article is not a trend. Rising Amazon bestseller rank + hiring surge + funding news = a pattern.
- **Confidence levels:** Use explicit language — "strong signal" (3+ independent sources), "emerging signal" (2 sources), "single data point" (1 source, treat as directional only).
- **Sub-category emergence:** Look for adjacent queries gaining traction that didn't exist 12–24 months ago. These are often where market white space lives.
- **Uncertainty is honest:** Demand signals from public web data are probabilistic. Present them as such — "the data suggests momentum" not "the market is growing."

**Output format:**

```markdown
# Demand & Trend Signals: [Category/Market]
*Data collected on [YYYY-MM-DD]*

## Research question
[What decision does this inform — market entry timing, product investment, category expansion?]

## Raw data collected
*Unfiltered — exactly what the tools returned before any interpretation.*

| Source | URL | Date | Raw headline or snippet |
|--------|-----|------|------------------------|
| [Google News / Search / Jobs] | [url] | [date] | [exact title or snippet as returned] |

---
*Analysis below is Claude's interpretation of the above sources.*

---

## Overall market signal
[1–2 sentence read on whether evidence points to growth, decline, or fragmentation — with confidence level]

## Signal breakdown

### Funding and investment activity
[Recent rounds, acquisitions, or notable launches — each with source and date]
*Signal strength: [Strong / Emerging / Single data point]*

### Search and content demand
[SERP patterns, content volume, recency of discussion]
*Signal strength: [Strong / Emerging / Single data point]*

### Product market movement
[Amazon/Google Shopping rankings, new entrants, price movement]
*Signal strength: [Strong / Emerging / Single data point]*

### Hiring patterns (market-level)
[What companies across the space are hiring for — technology bets, new functions]
*Signal strength: [Strong / Emerging / Single data point]*

## Emerging sub-categories
[Adjacent areas gaining momentum that weren't prominent 12–24 months ago]

## Signals to watch
[Early indicators that haven't confirmed yet but warrant monitoring]

## Data confidence notes
[What this analysis can and can't tell you — leading vs. lagging signals, gaps]

## Implications
**Immediate:** [Time-sensitive actions based on these signals]
**Near-term:** [Product or positioning decisions for this quarter]
**Strategic:** [What this suggests about where to place long-term bets]

## Gap report
| Gap | Why it wasn't filled | Suggested follow-up |
|-----|---------------------|-------------------|
| [e.g. No funding news found] | [e.g. No results for funding queries] | [e.g. Search `[category] site:crunchbase.com` or `[category] series A OR seed 2024 2025`] |
| [e.g. Hiring signal weak] | [e.g. Google Jobs returned few results] | [e.g. Check `site:greenhouse.io [category]` or `site:lever.co [category]`] |
```

---

### 3. Price & Category Intelligence

**Research question answered:** How is this market structured on price, and what do customers actually get at each tier?

**When to use:** User wants to understand category pricing before setting or adjusting their own prices, identify underserved price tiers, or map how features correlate with price across a market.

**Important:** This module maps the market's price structure — it's not a competitor pricing comparison. The goal is to understand where the market clusters, where gaps exist, and what the price/value trade-offs are across the category.

**Before gathering, announce:** *"Starting price and category research on [category]. Looking for: price distribution, pricing models in use, feature/price correlation, and hidden costs. Will check product platforms and scrape pricing pages for the top players."*

**Data gathering — call these tools, reading results as they return:**

For physical product categories, run in parallel:
- Call `mcp__ScraperAPIRemote__amazon_search` with `query = "[category]"` — rankings and price spread
- Call `mcp__ScraperAPIRemote__google_shopping` with `query = "[category]"` — price distribution across sellers
- Call `mcp__ScraperAPIRemote__walmart_search` with `query = "[category]"` — mass-market price anchors
- Call `mcp__ScraperAPIRemote__ebay_search` with `query = "[category]"` — secondary market and price floor signals

For SaaS/software categories, first identify the top players:
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] pricing"` — find pricing pages for the top 4–6 players

Then scrape their pricing pages in parallel (most pricing pages are static HTML — use standard fetch):
- Call `mcp__ScraperAPIRemote__scrape` with `url = "[player-a]/pricing"`
- Call `mcp__ScraperAPIRemote__scrape` with `url = "[player-b]/pricing"`
- Call `mcp__ScraperAPIRemote__scrape` with `url = "[player-c]/pricing"`

Then gather third-party pricing commentary:
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] pricing review OR hidden costs OR expensive"`
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] affordable OR cheap OR free alternative"`

**Analysis rules:**

- **Map the distribution, not just the range:** Where does pricing cluster? A market with most products between $20–40 and a few outliers at $200+ tells a different story than a market evenly spread from $5–$500.
- **Identify the pricing model in use:** Per-seat, usage-based, flat-rate, freemium, enterprise-only. The model signals what the seller believes buyers optimize for.
- **Feature/price correlation:** What do you get at each tier? Which features are table stakes (present at every price point) vs. tier-defining (unlock at a specific price)?
- **Price anchors:** What's the cheapest credible option? What's the most expensive? These anchors define how buyers think about "normal."
- **Hidden cost signals:** Search and review data often surface costs not visible on pricing pages — overage fees, implementation costs, required add-ons. Include these.
- **Note what you can't see:** Enterprise pricing is almost always negotiated. Published prices are a floor, not the actual number. Flag this.

**Output format:**

```markdown
# Price & Category Intelligence: [Category/Market]
*Data collected on [YYYY-MM-DD]*

## Research question
[What pricing decision does this inform?]

## Raw data collected
*Unfiltered — prices, product listings, and page content exactly as returned.*

| Source | URL | Product / Plan | Price (as shown) | Raw detail |
|--------|-----|---------------|-----------------|-----------|
| [Amazon / Google Shopping / Pricing page] | [url] | [product or plan name] | [$X] | [limits, features, or notes as shown] |

---
*Analysis below is Claude's interpretation of the above data.*

---

## Market price structure

### Where the market clusters
[Describe the distribution — e.g., "the mass market sits between $X–$Y, with a premium tier above $Z"]

### Price anchors
- **Floor** (cheapest credible option): [price + what you get + source]
- **Midmarket median**: [price range + typical features at this tier]
- **Premium ceiling**: [price + what justifies it + source]

## Pricing model breakdown
| Player/Tier | Price | Model | Key features included | Notable limits |
|-------------|-------|-------|----------------------|---------------|
| [Name] | [$X/mo] | [usage/seat/flat] | [features] | [limits] |
| [Name] | [$X/mo] | [usage/seat/flat] | [features] | [limits] |
| [Name] | [Custom] | [enterprise] | [features] | [limits] |

*Sources: [URLs for each pricing page]*

## Table stakes vs. tier-defining features
- **Table stakes** (present at all price points): [features]
- **Mid-tier unlocks** (appear at $X+): [features]
- **Premium/enterprise only**: [features]

## Hidden and variable costs
[Overage fees, required add-ons, implementation costs, annual vs. monthly delta — sourced from reviews and search]

## Pricing model signals
[What the dominant model tells you about how buyers in this market make decisions]

## Gaps and opportunities
[Underserved price tiers, missing feature/price combinations, positioning gaps]

## Data confidence notes
[Enterprise pricing is negotiated and not visible here. Published prices are a floor. Flag any paywalled or incomplete pricing pages.]

## Implications
**Immediate:** [Pricing changes or tests warranted now]
**Near-term:** [Tier or packaging decisions for this quarter]
**Strategic:** [Long-term pricing model positioning]

## Gap report
| Gap | Why it wasn't filled | Suggested follow-up |
|-----|---------------------|-------------------|
| [e.g. Pricing page returned empty] | [e.g. Page appears JS-rendered] | [e.g. Retry `scrape` with `render=true, premium=true`, or check `[player] pricing site:g2.com`] |
| [e.g. Enterprise pricing not visible] | [e.g. Expected — enterprise is negotiated] | [e.g. Search `[player] pricing enterprise OR custom quote reviews` for buyer estimates] |
```

---

### 4. Competitive Landscape

**Research question answered:** Who are the significant players in this market, how do they position themselves, and where are the gaps?

**When to use:** User wants to map the market before making a positioning, entry, or investment decision. Run this module *after* Consumer Sentiment and Price & Category Intelligence when possible — positioning analysis is more useful when you already know what the market cares about and how it's priced.

**Before gathering, announce:** *"Starting competitive landscape research on [category]. Looking for: who the significant players are, how they're tiered, what they claim vs. what customers say, and where the white space is."*

**Data gathering — call these tools, reading results as they return:**

Run these in parallel (first batch — discover who's in the market):
- Call `mcp__ScraperAPIRemote__google_search` with `query = "best [category] tools [year]"` — surfaces comparison roundups
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[category] alternatives OR competitors"` — surfaces head-to-head comparisons
- Call `mcp__ScraperAPIRemote__google_search` with `query = "site:g2.com [category] grid OR leaders"` — surfaces analyst-style market maps
- Call `mcp__ScraperAPIRemote__google_news` with `query = "[category] funding OR acquisition OR launch"` — surfaces recent moves

From the results, identify the 6–8 most significant players. Then fetch their homepages in parallel (standard fetch — limit to top players):
- Call `mcp__ScraperAPIRemote__scrape` with `url = "[player-1-homepage]"`
- Call `mcp__ScraperAPIRemote__scrape` with `url = "[player-2-homepage]"`
- Call `mcp__ScraperAPIRemote__scrape` with `url = "[player-3-homepage]"`

Then validate stated positioning against customer perception:
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[player-1] review OR alternative OR vs"`
- Call `mcp__ScraperAPIRemote__google_search` with `query = "[player-2] review OR alternative OR vs"`

**Analysis rules:**

- **Tier players by market position, not by your familiarity with them.** Enterprise players (complex sales, high ACVs, broad feature sets), mid-market (self-serve or inside sales, mid-range pricing), SMB/startup (low friction, low price, narrow scope), open-source/free (community-led, no direct revenue model).
- **Distinguish stated positioning from perceived positioning.** What a company says on its homepage vs. what customers say in reviews are often different. Both matter. Note the gap when it exists.
- **Build a positioning map, not just a list.** Choose two dimensions that the market actually competes on (from Consumer Sentiment data if available) and place players on them.
- **Flag recent moves.** A company that raised a round six months ago or just launched a new product line is in a different position than its current homepage suggests.
- **Note what's absent.** White space — positions nobody occupies — is often more strategically valuable than knowing who's where.

**Output format:**

```markdown
# Competitive Landscape: [Category/Market]
*Data collected on [YYYY-MM-DD]*

## Research question
[What positioning, entry, or investment decision does this inform?]

## Raw data collected
*Unfiltered — search results, homepage content, and news exactly as returned.*

| Source | URL | Type | Raw title / snippet |
|--------|-----|------|-------------------|
| [Google Search / Scrape / News] | [url] | [SERP result / homepage / news article] | [exact title and snippet as returned] |

---
*Analysis below is Claude's interpretation of the above sources.*

---

## Market overview
[2–3 sentences: how many meaningful players, general market maturity, any notable recent consolidation or fragmentation]

## Player map

### Enterprise tier
| Player | Positioning (their words) | What customers say | Key differentiator | Funding/stage |
|--------|--------------------------|-------------------|-------------------|--------------|
| [Name] | "[tagline or claim]" | [1-line sentiment summary] | [what actually sets them apart] | [stage + last round] |

### Mid-market tier
| Player | Positioning | Customer perception | Key differentiator | Funding/stage |
|--------|------------|--------------------|--------------------|--------------|

### SMB / self-serve tier
| Player | Positioning | Customer perception | Key differentiator | Funding/stage |
|--------|------------|--------------------|--------------------|--------------|

### Open source / free
| Project | Positioning | Community signal | Key differentiator |
|---------|------------|-----------------|-------------------|


## Stated vs. perceived positioning gaps
[Players where homepage messaging diverges notably from customer reviews — these represent credibility opportunities]

## Recent moves to watch
[Funding, launches, acquisitions, or leadership changes from news data — with source and date]

## White space
[Positions on the map nobody occupies, underserved tiers, unmet needs from Consumer Sentiment that no player addresses well]

## Data confidence notes
[Positioning analysis reflects public-facing signals only. Private companies' financials, roadmaps, and enterprise pricing are not visible here.]

## Implications
**Immediate:** [Positioning or messaging actions warranted now]
**Near-term:** [Strategic moves to consider this quarter]
**Strategic:** [Long-term positioning based on where the landscape is heading]

## Gap report
| Gap | Why it wasn't filled | Suggested follow-up |
|-----|---------------------|-------------------|
| [e.g. Player funding/stage unknown] | [e.g. No Crunchbase page found] | [e.g. Search `[player] funding site:techcrunch.com` or `[player] crunchbase`] |
| [e.g. Customer perception unavailable] | [e.g. Player has few public reviews] | [e.g. Search `[player] review site:g2.com OR site:reddit.com`] |
| [e.g. White space hard to characterize] | [e.g. Consumer Sentiment not yet run] | [e.g. Run Consumer Sentiment Analysis first — gaps become clearer once you know what the market asks for] |
```

---

## Multi-Module: Full Market Research Report

When the user asks for a complete market analysis, full research brief, or board-level market overview, combine modules in this order:

1. **Consumer Sentiment Analysis** — what the market wants and where it's underserved
2. **Demand & Trend Signals** — whether the market is growing and where attention is shifting
3. **Price & Category Intelligence** — how the market is structured on price
4. **Competitive Landscape** — who the players are and how they position (informed by the above)

Open with a **Research Brief** section that states the research question, scope, and methodology. Close with a **Strategic Recommendations** section that synthesizes across all modules into tiered actions.

Complete each module fully — including its gap report — before moving to the next.

**Output structure:**

```markdown
# Market Research Report: [Market/Category]
*Data collected on [YYYY-MM-DD]*

## Research brief
- **Question:** [What decision does this inform?]
- **Scope:** [Category, geography, time horizon]
- **Methodology:** Live web data collected via ScraperAPI — search, product platforms, review sites, news, and job boards. Secondary research only; findings reflect public signals.
- **Confidence level:** [Overall assessment of data quality and coverage]

## Key findings
1. [Most important finding — one sentence, evidenced]
2. [Second finding]
3. [Third finding]

## Consumer sentiment
[Full Consumer Sentiment Analysis output, including gap report]

## Demand & trend signals
[Full Demand & Trend Signals output, including gap report]

## Price & category intelligence
[Full Price & Category Intelligence output, including gap report]

## Competitive landscape
[Full Competitive Landscape output, including gap report]

## Strategic recommendations
**Immediately actionable (this week):**
- [Specific action based on findings]

**Near-term (this quarter):**
- [Positioning, pricing, or product decisions]

**Strategic (this year):**
- [Market entry, investment, or long-term positioning moves]

## Sources
[Consolidated list of all URLs cited across modules]
```

---

## Module Selection Guide

| The user wants to know... | Module |
|---------------------------|--------|
| What customers want, need, or complain about in a category | Consumer Sentiment Analysis |
| Whether a market is growing, and where demand is shifting | Demand & Trend Signals |
| How a category is priced and what buyers get at each tier | Price & Category Intelligence |
| Who the players are and how they're positioned | Competitive Landscape |
| All of the above — full research brief | Multi-Module Report |

**Sequencing note:** When running multiple modules, always run Consumer Sentiment before Competitive Landscape. You can only build a meaningful positioning map if you know what dimensions the market actually competes on.

---

## Output Quality Standards

1. **Research question first** — state what decision the research informs before presenting any data.
2. **Announce before searching** — state what you're looking for before the first tool call in each module.
3. **Structured tools over scrape** — use amazon_search, walmart_review, google_shopping when they apply. They return cleaner data than parsing raw HTML.
4. **Separate data from inference** — "the data shows X" vs. "this suggests Y" are different claims. Use that language explicitly.
5. **Verbatims with sources** — every sentiment finding needs at least one direct quote with a source URL and approximate date.
6. **Confidence levels are mandatory** — flag when a finding is well-supported vs. directional. Never present a single data point as a pattern.
7. **Sampling caveats belong in the report** — reviews skew toward strong opinions; Reddit skews technical; published prices aren't enterprise prices. Say so.
8. **Gap report after every module** — list what wasn't found and one concrete follow-up per gap.
9. **Tiered recommendations** — Immediate / Near-term / Strategic. Generic recommendations are not recommendations.
10. **Date-stamp everything** — "Data collected on [YYYY-MM-DD]" in every report.
