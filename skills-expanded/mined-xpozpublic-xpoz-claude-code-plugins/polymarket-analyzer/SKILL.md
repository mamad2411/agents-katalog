---
name: polymarket-analyzer
version: 2026-03-20
description: Analyze Polymarket prediction market events with real-time social intelligence from XPOZ MCP. Compares market odds against social sentiment to find gaps. Supports binary (YES/NO) and multi-choice events. Use when asked to "analyze a Polymarket event", "polymarket sentiment", "prediction market analysis", or given a polymarket.com URL.
---

# Polymarket Event Analyzer

## Overview

This skill analyzes Polymarket prediction market events by combining on-chain market data with real-time social intelligence from Twitter/X, Reddit, and Instagram via XPOZ MCP. It identifies sentiment gaps between what bettors price and what the crowd actually says, surfaces top voices on each side, and highlights conversation catalysts. Output is a self-contained HTML report.

## When to Use

Activate this skill when the user asks about:
- "Analyze this Polymarket event: [URL]"
- "Polymarket analysis for [TOPIC]"
- "What does social say about [POLYMARKET EVENT]?"
- "Prediction market sentiment for [EVENT]"
- "Compare market odds vs social sentiment for [EVENT]"
- Any `polymarket.com` URL

## Prerequisites

- **XPOZ MCP server** configured (for Twitter, Reddit, Instagram data). Get an access key at [xpoz.ai](https://xpoz.ai).
- **Internet access** (for Polymarket gamma API via WebFetch)

## MCP Configuration

Ensure the XPOZ MCP server is configured in your Claude Code settings (`~/.claude.json`):

```json
{
  "mcpServers": {
    "xpoz-mcp": {
      "url": "https://mcp.xpoz.ai/mcp",
      "transport": "http-stream",
      "headers": {
        "Authorization": "Bearer YOUR_XPOZ_API_KEY"
      }
    }
  }
}
```

Replace `YOUR_XPOZ_API_KEY` with your key from [xpoz.ai/settings](https://www.xpoz.ai/settings).

---

## Steps

**IMPORTANT**: Run end-to-end without stopping for user input (unless keyword search returns multiple events). Do NOT ask for confirmation at any step.

### 1. Resolve the Event

Use WebFetch to get event data from the Polymarket gamma API.

**If the user provides a URL:**
Extract the slug (last path segment, e.g., `us-strikes-iran-by` from `https://polymarket.com/event/us-strikes-iran-by`) and fetch:
```
WebFetch: https://gamma-api.polymarket.com/events?slug=<SLUG>
```

**If the user provides a keyword:**
```
WebFetch: https://gamma-api.polymarket.com/events?title=<KEYWORD>&closed=false&limit=5
```
If multiple results, ask the user to choose. If one result, proceed automatically.

**Error handling:**
- If the API returns a 404, non-200 status, or an empty array `[]`: tell the user **"Event not found — check the URL or slug and try again."** Do not proceed.
- If keyword search returns 0 events: tell the user **"No events found for that keyword. Try a different keyword or provide a direct Polymarket URL."** Do not proceed.

**Parse the JSON response** (first element of the returned array):
- `id`, `title`, `description`
- `markets[]` — each has: `question`, `outcomePrices` (JSON string like `"[0.45, 0.55]"`), `volume`, `liquidity`, `active`, `closed`, `groupItemTitle`, `dayChange`, `weekChange`

**Detect event type:**
1. Filter to active, non-closed markets
2. Collect distinct `groupItemTitle` values (skip null/undefined)
3. If 2+ distinct titles → **multi-choice**; otherwise → **binary**

**For multi-choice:** Extract **exactly the top 6** candidates sorted by volume desc — **NEVER show more than 6**. For each:
- `name` = groupItemTitle
- `marketOdds` = Math.round(yesPrice * 100)
- `volume` = parseFloat(market.volume)
- `weekChange` = market.weekChange || 0

**Primary market:** Highest-volume market. Extract yesPrice, noPrice, volume, liquidity, dayChange, weekChange.

**Total volume:** Sum of all active market volumes.

Save: `SLUG`, `EVENT_TYPE`, `EVENT_TITLE`, `CANDIDATES` (if multi-choice), primary market data, total volume.

### 2. Extract Search Keywords

Derive automatically — do NOT ask for confirmation.

**Hard limit: 3-4 quoted multi-word phrases total. Never exceed 4.**

- **Binary events**: Extract **exactly 3** multi-word search phrases from the event title. Join with ` OR `.
  - Every phrase MUST be 2+ words and quoted. Never use a single generic word.
  - Bad: `"Oscar"` (matches F1 driver). Good: `"Best Actor Oscar 2026"`.
  - Example: "Will US strike Iran?" → `"US strikes Iran" OR "Iran military strike" OR "Trump Iran attack"`

- **Multi-choice events**: **1 topic phrase + top 3 candidate names = 4 total max.**
  - Topic phrase: core concept + year/context (e.g., `"World Cup 2026"` not just `"World Cup"`)
  - Candidate names: use **full names** for people, team/country names for sports
  - Do NOT add a keyword for every candidate — only the top 3 by volume
  - Example: "Oscars Best Actor" → `"Best Actor Oscar 2026" OR "Timothee Chalamet Oscar" OR "Adrien Brody Oscar" OR "Sebastian Stan Oscar"`

**Validation before proceeding:**
- [ ] Total keyword phrases: 3-4 (never more)
- [ ] Every phrase is 2+ words
- [ ] Every phrase is quoted
- [ ] No single generic words like "Oscar", "market", "war"

### 3. Gather Social Data with XPOZ MCP

First, discover the actual XPOZ tool names by running ToolSearch queries. The MCP server may be registered under different name prefixes depending on the user's configuration (e.g., `mcp__xpoz-mcp__*`, `mcp__claude_ai_XPOZ-MCP__*`, or something else entirely).

Run these ToolSearch queries to discover the real tool names:
```
ToolSearch: +xpoz-mcp twitter keywords
ToolSearch: +xpoz-mcp reddit keywords
ToolSearch: +xpoz-mcp instagram keywords
ToolSearch: +xpoz-mcp count
ToolSearch: +xpoz-mcp checkOperation
```

**Use the exact tool names returned by ToolSearch.** The examples below show the parameter patterns — substitute the actual tool names from ToolSearch results:

Use `startDate` = 7 days ago (YYYY-MM-DD), `endDate` = today (YYYY-MM-DD).

Run these in **parallel**:

**Twitter posts** (tool: `getTwitterPostsByKeywords`):
```
query: "phrase1 OR phrase2 OR phrase3",
fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount", "replyCount"],
startDate: "YYYY-MM-DD", endDate: "YYYY-MM-DD"
```

**Reddit posts** (tool: `getRedditPostsByKeywords`):
```
query: "phrase1 OR phrase2 OR phrase3",
fields: ["id", "title", "selftext", "authorUsername", "subredditName", "score", "commentsCount", "createdAtDate"],
startDate: "YYYY-MM-DD", endDate: "YYYY-MM-DD",
sort: "relevance"
```

**Instagram posts** (tool: `getInstagramPostsByKeywords`):
```
query: "phrase1 OR phrase2 OR phrase3",
fields: ["id", "caption", "username", "createdAtDate", "likeCount", "commentCount"],
startDate: "YYYY-MM-DD", endDate: "YYYY-MM-DD"
```

**Tweet count** (tool: `countTweets`, use the broadest single keyword):
```
phrase: "broadest keyword", startDate: "...", endDate: "..."
```

Poll async operations (countTweets) with the `checkOperationStatus` tool (use the exact name from ToolSearch).

If results are saved to files, read the files with the Read tool.

**Minimum post threshold — progressive date widening:**
After gathering data, count total **relevant** posts across all platforms. If the count is below 100, widen the date range and re-fetch:

1. **First attempt**: `startDate` = 7 days ago → count posts
2. **If < 100 posts**: Widen to `startDate` = 30 days ago → re-run all platform queries with the wider range → count again
3. **If still < 100 posts**: **STOP.** Tell the user: **"Too few posts to reach a meaningful presentation — only {N} relevant posts found across Twitter, Reddit, and Instagram over the past 30 days."** Do NOT generate a report. End here.

When widening the date range, update the "last 7 days" label in the report to match the actual range used (e.g., "last 30 days").

### 4. Analyze (Claude does this — no external scripts)

**4a. Collect all posts** into a unified list. For each post note:
- `text`: tweet text / reddit title + selftext / instagram caption
- `author`: username
- `platform`: twitter / reddit / instagram
- `engagement`: likes + retweets + replies (Twitter); score (Reddit); likes + comments (Instagram)
- `date`: formatted as "Mon DD" (e.g., "Mar 8")

**4b. Filter relevance**: Discard posts clearly unrelated to the event. Use your judgment — if a post about "Oscar Piastri" appears in an "Oscars Best Actor" search, discard it.

**Common issue — sparse social data**: If only 2-3 out of 6 candidates have any social mentions (many show 0%), this is normal for early/niche markets. In this case:
- Still show all 6 candidates in the table with 0% social bars
- In the gap narrative, note that "social data is sparse — most candidates lack dedicated online discussion this week"
- Focus the analysis on candidates that DO have social signal rather than drawing conclusions from 0% values

**4c. Classify sentiment:**

**Binary events:**
For each relevant post, classify as **YES** (supports the event happening), **NO** (opposes it), or **NEUTRAL**:
- Consider the full context of the post, not just keyword presence
- YES: explicit support, confidence it will happen, celebrating it, arguing for it
- NO: explicit opposition, doubt, arguing against it, dismissing it
- NEUTRAL: reporting facts, asking questions, tangentially related

Calculate percentages: `positive%` = YES/total, `negative%` = NO/total, `neutral%` = remainder

**Multi-choice events:**
For each post, identify which candidate(s) it mentions. Try matching by:
1. Full name (case-insensitive)
2. Last name only (for people) or short name (for countries/teams)
3. Common nicknames or abbreviations (e.g., "Messi" for Argentina in football)

Count total posts mentioning each candidate. **Compute `socialMentionPct` using ALL candidates discovered during analysis (not just the top 6 displayed).** The denominator is the total number of posts mentioning ANY candidate — including candidates ranked 7th and beyond. Then display only the top 6 candidates in the HTML report.
- `socialMentionPct` = candidate mentions / total posts mentioning ANY candidate * 100
- Round to integers, ensure they sum to ~100
- **If a candidate is clearly ineligible or their social mentions are pure noise** (e.g., Barack Obama can't run for a 3rd term, general topic mentions misattributed to a specific candidate), annotate them with "(noise)" and exclude from the social percentage denominator. Explain in the gap narrative why.

**IMPORTANT: Only include the top 6 candidates in the candidate table.** Even if you analyzed more candidates during classification, the HTML report must show exactly 6 rows maximum.

**4d. Sentiment gap:**
- **Binary:** `socialSentimentYes` = positive%. `gapPercent` = socialSentimentYes - (marketOddsYes * 100).
  - Direction: gap > 5 → "social-more-bullish", gap < -5 → "social-more-bearish", else → "aligned"
- **Multi-choice:** Use the front-runner (highest marketOdds). `gapPercent` = socialMentionPct - marketOdds.
  - Same direction logic.
- Write a 1-sentence narrative: e.g., "Social sentiment on [candidate/event] runs N points [above/below] market odds — the crowd is [more/less] confident than bettors."

**4e. Top voices:**
Select the 3 highest-engagement posts supporting the event/front-runner (YES camp) and 3 highest-engagement opposing (NO camp). For each:
- `handle`, `displayName` (same as handle if unknown), `platform`
- `quote`: post text, truncated to 200 characters
- `reactions`: total engagement
- `followers`: 0 (unless known)

**4f. Catalysts:**
Select the 4 highest-engagement posts overall. For each:
- `description`: text truncated to 120 characters
- `date`: formatted "Mon DD"
- `engagement`: total
- `type`: "tweet" for Twitter, "news" for Reddit/Instagram

### 5. Generate HTML Report

Write the report to `out/polymarket-event-{SLUG}/report.html`.

**IMPORTANT**: The HTML must be a single self-contained file with all CSS inline in a `<style>` tag. No external dependencies.

Use this exact template structure, filling in all `{{PLACEHOLDER}}` values with data from Steps 1-4:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Event Intelligence: {{EVENT_TITLE}}</title>
<style>
  :root {
    --bg: #0f172a; --surface: #1e293b; --accent: #06b6d4;
    --text: #e2e8f0; --muted: #94a3b8; --green: #22c55e;
    --red: #ef4444; --amber: #f59e0b; --radius: 16px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family:-apple-system,BlinkMacSystemFont,'Inter','Segoe UI',sans-serif; background:var(--bg); color:var(--text); padding:48px 24px; line-height:1.6; }
  .container { max-width:960px; margin:0 auto; }
  .header { text-align:center; margin-bottom:48px; }
  .header h1 { font-size:2.2rem; color:var(--text); margin-bottom:12px; letter-spacing:-0.02em; line-height:1.2; }
  .category-badge { display:inline-block; padding:4px 16px; border-radius:20px; background:rgba(6,182,212,0.15); color:var(--accent); font-size:0.8rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px; }
  .header-meta { color:var(--muted); font-size:0.9rem; }
  .header-meta a { color:var(--accent); text-decoration:none; }
  .section-title { font-size:1.4rem; color:var(--text); margin-bottom:20px; font-weight:700; display:flex; align-items:center; gap:10px; }
  .section-title::before { content:''; display:inline-block; width:4px; height:24px; background:var(--accent); border-radius:2px; }
  .stats-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; margin-bottom:48px; }
  .stat-card { background:var(--surface); border-radius:var(--radius); padding:24px; text-align:center; position:relative; overflow:hidden; }
  .stat-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
  .stat-card.yes::before { background:var(--green); }
  .stat-card.no::before { background:var(--red); }
  .stat-card.volume::before { background:var(--accent); }
  .stat-card.liquidity::before { background:var(--amber); }
  .stat-value { font-size:2.4rem; font-weight:800; line-height:1; }
  .stat-label { font-size:0.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.08em; margin-top:6px; }
  .stat-change { font-size:0.8rem; margin-top:4px; }
  .change-up { color:var(--green); } .change-down { color:var(--red); }

  /* Candidate table */
  .candidates-table { background:var(--surface); border-radius:var(--radius); overflow:hidden; margin-bottom:16px; }
  .candidates-header { display:grid; grid-template-columns:180px 1fr 80px; gap:12px; padding:12px 20px; font-size:0.75rem; font-weight:600; color:var(--muted); text-transform:uppercase; letter-spacing:0.05em; border-bottom:1px solid rgba(148,163,184,0.1); }
  .candidate-row { display:grid; grid-template-columns:180px 1fr 80px; gap:12px; padding:14px 20px; align-items:center; border-bottom:1px solid rgba(148,163,184,0.05); }
  .candidate-row.leader { background:rgba(6,182,212,0.06); border-left:3px solid var(--accent); }
  .cand-name { font-weight:600; font-size:0.95rem; }
  .cand-bars { flex:1; display:flex; flex-direction:column; gap:4px; }
  .cand-bar-row { display:flex; align-items:center; gap:8px; }
  .cand-bar-label { font-size:0.7rem; color:var(--muted); width:42px; text-align:right; }
  .cand-bar-track { flex:1; height:18px; background:rgba(148,163,184,0.08); border-radius:4px; overflow:visible; position:relative; }
  .cand-bar-fill { height:100%; border-radius:4px; display:flex; align-items:center; padding-left:8px; font-size:0.75rem; font-weight:600; color:white; min-width:36px; overflow:visible; white-space:nowrap; }
  .cand-gap { font-size:0.85rem; font-weight:700; min-width:48px; text-align:center; }
  .cand-bar-col { display:flex; align-items:center; gap:12px; }
  .cand-vol-col { font-size:0.85rem; color:var(--muted); text-align:right; font-weight:500; }

  /* Sentiment gap */
  .gap-container { margin-bottom:48px; }
  .gap-chart { background:var(--surface); border-radius:var(--radius); padding:28px 32px; margin-bottom:16px; }
  .gap-row { display:flex; align-items:center; gap:16px; margin-bottom:18px; }
  .gap-row:last-child { margin-bottom:0; }
  .gap-row-label { width:60px; font-size:0.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.06em; font-weight:700; flex-shrink:0; }
  .gap-track { flex:1; height:36px; background:var(--bg); border-radius:8px; position:relative; overflow:visible; }
  .gap-fill { height:100%; border-radius:8px; display:flex; align-items:center; justify-content:flex-end; padding-right:12px; font-weight:800; font-size:1rem; color:#fff; }
  .gap-marker { position:absolute; top:-6px; bottom:-6px; width:2px; border-left:2px dashed rgba(148,163,184,0.4); z-index:2; }
  .gap-zone { position:absolute; top:0; bottom:0; border-radius:0 8px 8px 0; background:rgba(245,158,11,0.12); border-right:2px solid var(--amber); }
  .gap-callout { background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.3); border-radius:var(--radius); padding:20px 24px; display:flex; align-items:flex-start; gap:20px; }
  .gap-number { font-size:2rem; font-weight:800; color:var(--amber); white-space:nowrap; min-width:90px; flex-shrink:0; padding-top:2px; }
  .gap-narrative { color:#cbd5e1; font-size:0.95rem; line-height:1.6; }

  /* Posts banner */
  .posts-banner { background:var(--surface); border-radius:var(--radius); padding:28px; display:flex; align-items:center; justify-content:center; gap:32px; margin-bottom:48px; flex-wrap:wrap; }
  .posts-total { font-size:2.8rem; font-weight:800; color:var(--accent); font-variant-numeric:tabular-nums; }
  .posts-label { color:var(--muted); font-size:0.9rem; }
  .posts-badges { display:flex; gap:12px; }
  .posts-badge { display:inline-flex; align-items:center; gap:6px; padding:6px 14px; border-radius:20px; font-size:0.85rem; font-weight:600; }
  .posts-badge.twitter { background:rgba(29,155,240,0.15); color:#1d9bf0; }
  .posts-badge.reddit { background:rgba(255,69,0,0.15); color:#ff4500; }
  .posts-badge.instagram { background:rgba(225,48,108,0.15); color:#e1306c; }

  /* Voice cards */
  .voices-columns { display:grid; grid-template-columns:1fr 1fr; gap:24px; margin-bottom:48px; }
  .voices-column h3 { font-size:1rem; font-weight:700; margin-bottom:14px; padding-bottom:8px; border-bottom:2px solid; }
  .voices-column.yes h3 { color:var(--green); border-color:var(--green); }
  .voices-column.no h3 { color:var(--red); border-color:var(--red); }
  .voice-card { background:var(--surface); border-radius:var(--radius); padding:20px; margin-bottom:12px; }
  .voice-top { display:flex; align-items:center; gap:12px; margin-bottom:12px; }
  .voice-avatar { width:40px; height:40px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; font-weight:800; color:var(--bg); }
  .voice-name { font-weight:700; font-size:0.95rem; }
  .voice-handle { color:var(--accent); font-size:0.8rem; }
  .voice-meta { color:var(--muted); font-size:0.75rem; }
  .voice-quote { padding:10px 14px; background:var(--bg); border-radius:10px; font-style:italic; color:#cbd5e1; font-size:0.85rem; line-height:1.5; border-left:2px solid var(--accent); }

  /* Catalysts */
  .catalysts { display:flex; flex-direction:column; gap:14px; margin-bottom:48px; }
  .catalyst-card { background:var(--surface); border-radius:var(--radius); padding:20px 24px; display:flex; align-items:center; gap:16px; border-left:4px solid var(--accent); }
  .catalyst-type { display:inline-block; padding:3px 10px; border-radius:8px; font-size:0.7rem; font-weight:700; letter-spacing:0.06em; white-space:nowrap; }
  .catalyst-body { flex:1; }
  .catalyst-desc { font-size:0.95rem; font-weight:600; margin-bottom:4px; }
  .catalyst-meta { font-size:0.8rem; color:var(--muted); }

  /* Risk callout */
  .risk-callout { background:linear-gradient(135deg,rgba(245,158,11,0.1),rgba(245,158,11,0.03)); border:1px solid rgba(245,158,11,0.25); border-radius:var(--radius); padding:28px; margin-bottom:48px; position:relative; overflow:hidden; }
  .risk-callout::before { content:''; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--amber); }
  .risk-label { color:var(--amber); font-size:0.75rem; text-transform:uppercase; letter-spacing:0.1em; font-weight:700; margin-bottom:10px; }
  .risk-text { font-size:1.1rem; color:var(--text); line-height:1.6; }

  footer { text-align:center; color:#475569; font-size:0.8rem; margin-top:40px; padding-top:20px; border-top:1px solid rgba(148,163,184,0.1); }
  footer a { color:var(--accent); text-decoration:none; }
  .disclaimer { margin-top:12px; font-size:0.72rem; color:#334155; max-width:600px; margin-left:auto; margin-right:auto; }

  @media (max-width:768px) {
    .stats-grid { grid-template-columns:repeat(2,1fr); }
    .voices-columns { grid-template-columns:1fr; }
    .candidates-header, .candidate-row { grid-template-columns:120px 1fr 60px; }
  }
</style>
</head>
<body>
<div class="container">

  <!-- Header -->
  <div class="header">
    <div class="category-badge">{{CATEGORY}}</div>
    <h1>{{EVENT_TITLE}}</h1>
    <div class="header-meta">
      <a href="{{EVENT_URL}}" target="_blank">View on Polymarket &#8599;</a>
      &middot; Snapshot: {{SNAPSHOT_DATE}}
    </div>
  </div>

  <!-- Market Snapshot -->
  <div class="section-title">Market Snapshot</div>
  <div class="stats-grid">
    <div class="stat-card yes">
      <div class="stat-value" style="color:var(--green)">{{YES_PCT}}%</div>
      <div class="stat-label">YES Odds</div>
    </div>
    <div class="stat-card no">
      <div class="stat-value" style="color:var(--red)">{{NO_PCT}}%</div>
      <div class="stat-label">NO Odds</div>
    </div>
    <div class="stat-card volume">
      <div class="stat-value" style="color:var(--accent)">{{VOLUME}}</div>
      <div class="stat-label">Volume</div>
    </div>
    <div class="stat-card liquidity">
      <div class="stat-value" style="color:var(--amber)">{{LIQUIDITY}}</div>
      <div class="stat-label">Liquidity</div>
    </div>
  </div>

  <!-- Candidate Field (ONLY for multi-choice — omit entire section for binary) -->
  {{CANDIDATE_SECTION}}

  <!-- Sentiment Gap -->
  <div class="section-title">Sentiment Gap</div>
  <div class="gap-container">
    <div class="gap-chart">
      <div class="gap-row">
        <div class="gap-row-label">Market</div>
        <div class="gap-track">
          <div class="gap-fill" style="width:{{MARKET_YES}}%;background:var(--accent)">{{MARKET_YES}}%</div>
        </div>
      </div>
      <div class="gap-row">
        <div class="gap-row-label">Social</div>
        <div class="gap-track">
          <div class="gap-fill" style="width:{{SOCIAL_YES}}%;background:{{SOCIAL_COLOR}}">{{SOCIAL_YES}}%</div>
          <div class="gap-marker" style="left:{{MARKET_YES}}%"></div>
          <div class="gap-zone" style="left:{{GAP_ZONE_LEFT}}%;width:{{GAP_ZONE_WIDTH}}%"></div>
        </div>
      </div>
    </div>
    <div class="gap-callout">
      <div class="gap-number">{{GAP_DISPLAY}}</div>
      <div>
        <div class="gap-narrative">{{GAP_NARRATIVE}}</div>
      </div>
    </div>
  </div>

  <!-- Posts Analyzed -->
  <div class="section-title">Posts Analyzed</div>
  <div class="posts-banner">
    <div>
      <div class="posts-total">{{TOTAL_POSTS}}</div>
      <div class="posts-label">posts analyzed &middot; last 7 days</div>
    </div>
    <div class="posts-badges">
      <span class="posts-badge twitter">&#x1D54F; {{TWITTER_COUNT}} tweets</span>
      <span class="posts-badge reddit">R {{REDDIT_COUNT}} posts</span>
      <span class="posts-badge instagram">&#128247; {{INSTAGRAM_COUNT}} posts</span>
    </div>
  </div>

  <!-- Top Voices -->
  <div class="section-title">Top Voices</div>
  <div class="voices-columns">
    <div class="voices-column yes">
      <h3>{{YES_COLUMN_TITLE}}</h3>
      {{YES_VOICE_CARDS}}
    </div>
    <div class="voices-column no">
      <h3>{{NO_COLUMN_TITLE}}</h3>
      {{NO_VOICE_CARDS}}
    </div>
  </div>

  <!-- Catalysts -->
  <div class="section-title">Catalysts</div>
  <div class="catalysts">
    {{CATALYST_CARDS}}
  </div>

  <!-- Risk/Opportunity -->
  <div class="risk-callout">
    <div class="risk-label">Risk / Opportunity Signal</div>
    <div class="risk-text">{{GAP_NARRATIVE}}</div>
  </div>

  <footer>
    Powered by <a href="https://xpoz.ai" target="_blank">XPOZ</a> Social Intelligence &mdash; <a href="https://xpoz.ai" target="_blank">visit xpoz.ai to see how you can use it</a><br>
    {{GENERATED_DATE}} &middot; <a href="{{EVENT_URL}}" target="_blank">{{EVENT_URL}}</a>
    <div class="disclaimer">This report is for informational purposes only and does not constitute financial advice.</div>
  </footer>

</div>
</body>
</html>
```

**Fill in placeholders:**

- `{{CATEGORY}}`: Event category (e.g., "politics", "entertainment", "crypto"). Infer from title if not in API response.
- `{{YES_PCT}}` / `{{NO_PCT}}`: Primary market yesPrice/noPrice x 100, rounded to integer
- `{{VOLUME}}`: Formatted (e.g., "$1.2M", "$450K")
- `{{LIQUIDITY}}`: Formatted same way
- `{{MARKET_YES}}`: Market YES percentage (0-100)
- `{{SOCIAL_YES}}`: Social sentiment YES percentage (0-100)
- `{{SOCIAL_COLOR}}`: `var(--green)` if social > market, `var(--red)` if social < market, `var(--muted)` if aligned
- `{{GAP_ZONE_LEFT}}`: `min(MARKET_YES, SOCIAL_YES)`
- `{{GAP_ZONE_WIDTH}}`: `abs(SOCIAL_YES - MARKET_YES)`
- `{{GAP_DISPLAY}}`: e.g., "+34pt" or "-12pt"
- `{{GAP_NARRATIVE}}`: The 1-sentence narrative from Step 4d

**For multi-choice `{{CANDIDATE_SECTION}}`** — generate rows for **at most 6 candidates** using this pattern per candidate:
```html
<div class="candidate-row {{LEADER_CLASS}}">
  <div><div class="cand-name">{{NAME}}</div></div>
  <div class="cand-bar-col">
    <div class="cand-bars">
      <div class="cand-bar-row">
        <span class="cand-bar-label">Market</span>
        <div class="cand-bar-track"><div class="cand-bar-fill" style="width:{{MARKET_W}}%;background:var(--accent)">{{MARKET_ODDS}}%</div></div>
      </div>
      <div class="cand-bar-row">
        <span class="cand-bar-label">Social</span>
        <div class="cand-bar-track"><div class="cand-bar-fill" style="width:{{SOCIAL_W}}%;background:{{BAR_COLOR}}">{{SOCIAL_PCT}}%</div></div>
      </div>
    </div>
    <div class="cand-gap" style="color:{{GAP_COLOR}}">{{GAP_PT}}</div>
  </div>
  <div class="cand-vol-col">{{VOL_FORMATTED}}</div>
</div>
```
Where `MARKET_W` and `SOCIAL_W` are **scaled relative to the max value across all 6 candidates** (so the longest bar fills ~90%). Use `min-width:36px` on bar fills so even 0% values show a small stub with the label visible.
First candidate gets class `leader`.
For **binary events**, set `{{CANDIDATE_SECTION}}` to empty string.

**Bar scaling example:** If the highest value is 50%, then 50% gets `width:90%`, 25% gets `width:45%`, etc. This makes small differences visually distinguishable. Never use raw percentages as widths (e.g., `width:1.4%` is invisible).

**Bar scaling edge case — all zeros:** If the maximum value across all candidates is 0 (no social data at all), set all social bar widths to `min-width` (36px / use `width:4%` as a floor) and display "0%". Do not attempt to divide by zero or leave bars with `width:0%`.

**Voice cards** — for each voice:
```html
<div class="voice-card" style="border-left:3px solid {{CAMP_COLOR}}">
  <div class="voice-top">
    <div class="voice-avatar" style="background:{{CAMP_COLOR}}">{{INITIAL}}</div>
    <div>
      <div class="voice-name">{{DISPLAY_NAME}}</div>
      <div class="voice-handle" style="color:var(--accent)">{{PLATFORM_ICON}} @{{HANDLE}}</div>
      <div class="voice-meta">{{REACTIONS}} reactions</div>
    </div>
  </div>
  <div class="voice-quote">"{{QUOTE}}"</div>
</div>
```

Platform icons: Twitter = `&#x1D54F;`, Reddit = `R`, Instagram = `&#128247;`.
YES camp: `{{CAMP_COLOR}}` = `var(--green)`. NO camp: `var(--red)`.
Column titles: Binary → "YES Camp" / "NO Camp". Multi-choice → "Supporters" / "Skeptics".

**Catalyst cards** — for each catalyst:
```html
<div class="catalyst-card">
  <span class="catalyst-type" style="background:{{TYPE_BG}};color:{{TYPE_COLOR}}">{{TYPE_LABEL}}</span>
  <div class="catalyst-body">
    <div class="catalyst-desc">{{DESCRIPTION}}</div>
    <div class="catalyst-meta">{{DATE}} &middot; {{ENGAGEMENT}} engagements</div>
  </div>
</div>
```

Type colors: tweet → `background:rgba(29,155,240,0.2); color:#1d9bf0`, news → `background:rgba(6,182,212,0.2); color:var(--accent)`.

### 6. Open Report & Print Summary

Open the report in the user's browser. Use `open` on macOS, `xdg-open` on Linux, or `start` on Windows. If unsure of the OS, just print the file path and let the user open it manually.

**Binary summary:**
```
+==================================================+
|  POLYMARKET EVENT ANALYSIS                       |
+==================================================+
|  Event:     {eventTitle}                         |
|  Type:      Binary (YES/NO)                      |
|  Odds:      {yes}% YES / {no}% NO               |
|  Volume:    ${volume}                            |
|  Gap:       {gap}pt ({direction})                |
|  Posts:     {total} analyzed                     |
+--------------------------------------------------+
|  Report: out/polymarket-event-{SLUG}/report.html |
+==================================================+
```

**Multi-choice summary:**
```
+==========================================================+
|  POLYMARKET EVENT ANALYSIS                               |
+==========================================================+
|  Event:     {eventTitle}                                 |
|  Type:      Multi-choice ({N} candidates)                |
|  Volume:    ${totalVolume}                               |
+----------------------------------------------------------+
|  Candidates:                                             |
|    1. {name} — {mkt}% mkt / {social}% social            |
|    2. {name} — {mkt}% mkt / {social}% social            |
|    ...                                                   |
+----------------------------------------------------------+
|  Gap:       {gap}pt ({direction})                        |
|  Posts:     {total} analyzed                             |
|  Report: out/polymarket-event-{SLUG}/report.html         |
+==========================================================+
```

## Example Prompts

- `/polymarket-analyzer https://polymarket.com/event/bitcoin-150k`
- `/polymarket-analyzer https://polymarket.com/event/2026-fifa-world-cup-winner`
- `/polymarket-analyzer Bitcoin ETF approval`
- `/polymarket-analyzer "Will Trump win 2028?"`
- `Analyze the Polymarket event for the next Fed rate decision`

## Critical Requirements

1. **FETCH REAL DATA** — You MUST call the XPOZ MCP tools and fetch real social posts. Do NOT generate fake data or skip API calls.

2. **ASYNC POLLING** — After calling `getTwitterPostsByKeywords`, `getRedditPostsByKeywords`, `getInstagramPostsByKeywords`, or `countTweets`, poll `checkOperationStatus` until status is "completed".

3. **REAL QUOTES** — The top voices `quote` field and catalyst `description` field must contain actual post text from the fetched data, not fabricated examples.

4. **MULTI-PLATFORM** — Always query Twitter, Reddit, AND Instagram. Do not skip platforms.

5. **MAX 6 CANDIDATES** — For multi-choice events, never show more than 6 candidates in the report, even if the event has more markets.

6. **REQUIRED FOOTER** — Every report must include: `Powered by XPOZ Social Intelligence — visit xpoz.ai to see how you can use it` (with link to https://xpoz.ai).

## Notes

- **XPOZ Credits**: Each platform query uses credits. A typical analysis uses ~4-6 queries (3 platforms + tweet count + possible date widening).
- **Date Range**: Default is 7 days. Automatically widens to 30 days if < 100 posts found.
- **Sparse Data**: Some niche markets may have very little social discussion. The skill handles this gracefully with floor values for bars and narrative noting sparsity.
- **Rate Limits**: If you hit rate limits, wait a few seconds and retry. Do not skip the platform.
