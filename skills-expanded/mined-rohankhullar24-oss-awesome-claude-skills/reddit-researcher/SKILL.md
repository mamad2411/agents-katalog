---
name: reddit-researcher
description: "Deep research engine covering the last 30 days across 7 sources — Reddit, X/Twitter, YouTube, LinkedIn, Hacker News, Web, TechCrunch. Uses Apify actors. Synthesizes findings into grounded, cited reports with deduplication, relevance scoring, and cross-source signal detection."
argument-hint: "Claude vs GPT-4o, best AI coding tools, latest news on OpenAI"
license: MIT
user-invocable: true
---
# Reddit Researcher

Research ANY topic across Reddit, X/Twitter, YouTube, LinkedIn, Hacker News, the web, and TechCrunch. Surface what people are actually discussing, recommending, and debating right now — sourced from the last 30 days.

---

## Step 0 — Parse User Intent

Before doing anything, parse the user's input for:

**1\. TOPIC** — What they want to research.

**2\. QUERY\_TYPE** — Classify using these patterns (check in priority order):

| QUERY\_TYPE | Trigger patterns |
| :---- | :---- |
| comparison | "vs", "versus", "compared to", "better than", "difference between", "switch from" |
| how\_to | "how to", "tutorial", "best practices", "tips", "examples", "setup", "build a" |
| product | "price", "pricing", "buy", "alternative", "prompts", "template", "subscription" |
| opinion | "worth it", "thoughts on", "review", "should I", "pros and cons", "recommend" |
| prediction | "predict", "forecast", "odds", "chance", "probability", "outcome" |
| concept | "what is", "what are", "explain", "how does", "overview", "introduction" |
| breaking\_news | "latest", "breaking", "just announced", "launched", "new", "update", "news" |
| breaking\_news | (default if nothing matches) |

**3\. Source priority by QUERY\_TYPE** — use this to weight results during synthesis:

| QUERY\_TYPE | Highest priority sources |
| :---- | :---- |
| product | Reddit, X, YouTube |
| concept | HN, Reddit, Web |
| opinion | Reddit, X |
| how\_to | YouTube, Reddit, HN |
| comparison | Reddit, HN, YouTube |
| breaking\_news | X, Reddit, Web |
| prediction | X, Reddit |

Store:

- TOPIC \= \[extracted topic\]  
- QUERY\_TYPE \= \[detected type\]  
- TOPIC\_A / TOPIC\_B (only for comparison)  
- DATE\_30\_DAYS\_AGO \= \[today minus 30 days, YYYY-MM-DD\]  
- UNIX\_30\_DAYS\_AGO \= \[DATE\_30\_DAYS\_AGO as Unix timestamp\]

**Before calling any tools, display this to the user:**

Researching "{TOPIC}" across Reddit, X, YouTube, LinkedIn, Hacker News, Web, and TechCrunch.

Covering the last 30 days ({DATE\_30\_DAYS\_AGO} → today).

Topic: {TOPIC}

Query type: {QUERY\_TYPE}

Launching all agents now...

---

## Step 1 — Run All 7 Source Agents in Parallel

Launch all 7 agents simultaneously using the Agent tool — do NOT wait for one before starting the next. Pass TOPIC, DATE\_30\_DAYS\_AGO, and UNIX\_30\_DAYS\_AGO to each.

Use the agent instructions below for each source. Each agent returns a plain text summary.

---

### Agent A — Reddit

Call the Apify actor trudax/reddit-scraper-lite via the Apify MCP tool with this input:

{

  "searches": \["{TOPIC}"\],

  "searchPosts": true,

  "sort": "relevance",

  "time": "month",

  "maxItems": 20,

  "maxPostCount": 20,

  "maxComments": 0,

  "skipComments": true,

  "includeNSFW": false,

  "proxy": {

    "useApifyProxy": true,

    "apifyProxyGroups": \["RESIDENTIAL"\]

  }

}

Wait for the run to complete and retrieve dataset results. For each post return:

- Post title and URL  
- Subreddit  
- Upvotes, upvote ratio, comment count  
- Post date  
- Post body (first 300 chars if long)

Lead with highest-upvote posts. Group by subreddit if patterns emerge. If 0 results: write "Reddit: No results found."

---

### Agent B — X/Twitter

Call the Apify actor apidojo/tweet-scraper via the Apify MCP tool with this input:

{

  "searchTerms": \["{TOPIC}"\],

  "maxItems": 20,

  "sort": "Top",

  "tweetLanguage": "en",

  "start": "{DATE\_30\_DAYS\_AGO}"

}

Wait for the run to complete and retrieve dataset results. For each tweet return:

- Author handle and display name  
- Tweet text  
- URL  
- Likes, reposts, replies, quotes  
- Date posted

Lead with highest-liked tweets. Note any viral threads. If 0 results: write "X: No results found."

---

### Agent C — YouTube

Call the Apify actor streamers/youtube-scraper via the Apify MCP tool with this input:

{

  "searchQueries": \["{TOPIC}"\],

  "maxResults": 10,

  "maxResultsShorts": 0,

  "maxResultStreams": 0,

  "sortingOrder": "date",

  "dateFilter": "month",

  "downloadSubtitles": true

}

Wait for the run to complete and retrieve dataset results. For each video return:

- Video title and URL  
- Channel name  
- View count, like count  
- Date published  
- **Transcript highlights** — extract 3-5 key quotes directly from the subtitle/transcript text. These are the most valuable part: treat them like Reddit top comments. Quote them verbatim and attribute to the channel name.  
- If no transcript is available, fall back to the description (first 200 chars)

Lead with most-viewed videos. **Always include transcript quotes in your output** — the orchestrator will use these directly in synthesis. Note any channels covering the topic repeatedly. If 0 results: write "YouTube: No results found."

---

### Agent D — LinkedIn

Call the Apify actor harvestapi/linkedin-post-search via the Apify MCP tool with this input:

{

  "searchQueries": \["{TOPIC}"\],

  "maxPosts": 20,

  "postedLimit": "month",

  "sortBy": "date",

  "profileScraperMode": "short",

  "scrapeReactions": false,

  "scrapeComments": false

}

Wait for the run to complete and retrieve dataset results. For each post return:

- Author name and job title/company  
- Post text or key quote  
- URL  
- Likes, comments, shares  
- Date posted

Group by professional angle if patterns emerge. Lead with highest-engagement posts. If 0 results: write "LinkedIn: No results found."

---

### Agent E — Hacker News

Use WebFetch to call the Algolia HN API (free, no auth required):

https://hn.algolia.com/api/v1/search\_by\_date?query={TOPIC\_URL\_ENCODED}\&tags=story\&numericFilters=created\_at\_i\>{UNIX\_30\_DAYS\_AGO}\&hitsPerPage=30

Replace {TOPIC\_URL\_ENCODED} with the URL-encoded topic and {UNIX\_30\_DAYS\_AGO} with the actual Unix timestamp.

For each story return:

- Story title and URL (use url field, or https://news.ycombinator.com/item?id=\<objectID\>)  
- Points (upvotes) and comment count  
- Date posted

Lead with highest-points stories. Note any that sparked large comment threads. If 0 results: write "Hacker News: No results found."

---

### Agent F — Web

Use WebSearch to find recent web content. Run 2–3 searches with different angle variations:

- "{TOPIC}" after:{DATE\_30\_DAYS\_AGO}  
- "{TOPIC}" news latest  
- "{TOPIC}" analysis 2026

Then use WebFetch to read the full content of the top 5–10 most relevant URLs.

For each page return:

- Title and source/publication name  
- URL  
- Key points, findings, or quotes  
- Date published (if available)

Group by theme. Lead with most authoritative and recent sources. Only include content from the last 30 days. If no results: write "Web: No relevant results found."

---

### Agent G — TechCrunch

Use WebSearch to find recent TechCrunch articles:

site:techcrunch.com {TOPIC} after:{DATE\_30\_DAYS\_AGO}

Collect the top 5–8 TechCrunch article URLs. Then use WebFetch on each URL to read the full article content.

For each article return:

- Article title and URL  
- Key points, findings, or direct quotes  
- Date published  
- Author (if available)

Lead with most relevant and recent articles. Only include articles from techcrunch.com. If no articles found: write "TechCrunch: No relevant articles found."

---

## Step 2 — Relevance Filtering

Before scoring, filter out items that are not relevant to the topic.

For each item returned by any agent:

1. **Tokenize** the item's title/text: lowercase, remove punctuation, remove stopwords (the, a, an, to, for, is, in, of, on, and, with, from, by, at, this, that, it, i, we, you, are, do, can, be, or, not, so, if, but).  
     
2. **Tokenize** the topic query the same way.  
     
3. **Check overlap**: What fraction of the topic's meaningful tokens appear in the item's text?  
     
   - Exact phrase match anywhere → strong relevance signal (+bonus)  
   - 70%+ token overlap → relevant, keep  
   - 40–69% overlap → borderline, keep but lower weight  
   - Under 40% overlap → likely off-topic, discard unless very high engagement

   

4. **Generic tokens** ("best", "tips", "news", "update", "review", "vs") do NOT count as relevance on their own. An item must match at least one specific topic token to be kept.  
     
5. **Synonym expansion**: treat these as equivalent:  
     
   - js ↔ javascript, ts ↔ typescript, ai ↔ artificial intelligence, ml ↔ machine learning, react ↔ reactjs, rap ↔ hip hop

---

## Step 3 — Deduplication

### Within each source (same-source dedupe)

For each source's results independently:

- Compare item titles/text pairwise  
- If two items share 70%+ of their meaningful words (excluding stopwords), they are near-duplicates  
- Keep only the higher-engagement one, discard the other

### Across sources (cross-source linking)

Compare items across ALL sources to find the same story appearing in multiple places:

- Strip "Show HN:" / "Ask HN:" prefixes from HN titles before comparing  
- Truncate X/Twitter posts to first 100 characters before comparing  
- If two items from different sources share 40%+ meaningful word overlap → they are the same story  
- Tag both with \[CROSS-SOURCE: also on Reddit, HN\] — do NOT delete either  
- **Cross-source items are the strongest signals in the entire report.** Lead with them.

---

## Step 4 — Scoring

Score every item 0–100 using these formulas:

### Score weights by source type:

**Reddit** (has engagement data):

- Relevance: 45%  
- Recency: 25%  
- Engagement: 30%  
- Engagement formula: 0.50 × log(upvotes+1) \+ 0.35 × log(comments+1) \+ 0.15 × upvote\_ratio

**X/Twitter** (has engagement data):

- Relevance: 45%  
- Recency: 25%  
- Engagement: 30%  
- Engagement formula: 0.55 × log(likes+1) \+ 0.25 × log(reposts+1) \+ 0.15 × log(replies+1) \+ 0.05 × log(quotes+1)

**YouTube** (has engagement data):

- Relevance: 45%  
- Recency: 25%  
- Engagement: 30%  
- Engagement formula: 0.70 × log(views+1) \+ 0.30 × log(likes+1)

**LinkedIn** (has engagement data):

- Relevance: 45%  
- Recency: 25%  
- Engagement: 30%  
- Engagement formula: 0.50 × log(likes+1) \+ 0.30 × log(comments+1) \+ 0.20 × log(shares+1)

**Hacker News** (has engagement data):

- Relevance: 45%  
- Recency: 25%  
- Engagement: 30%  
- Engagement formula: 0.60 × log(points+1) \+ 0.40 × log(comments+1)

**Web / TechCrunch** (NO engagement data — apply source penalty):

- Relevance: 55%  
- Recency: 45%  
- Subtract 10–15 points from final score (web sources have no crowd validation)  
- Exception: concept and how\_to queries → no web penalty (authoritative docs are valuable)

### Recency score:

- Last 7 days: 100  
- 8–14 days ago: 80  
- 15–21 days ago: 60  
- 22–30 days ago: 40  
- Older than 30 days: discard

### Cross-source bonus:

- Item appears on 2 sources: \+10 points  
- Item appears on 3+ sources: \+20 points

---

## Step 5 — Synthesize Into Report

**CRITICAL: Ground your synthesis in what the agents ACTUALLY returned. Do not fill gaps with your own pre-existing knowledge.**

Structure based on QUERY\_TYPE:

---

### If QUERY\_TYPE \= comparison

Run agents TWICE in parallel — once for TOPIC\_A, once for TOPIC\_B — then a third pass for "{TOPIC\_A} vs {TOPIC\_B}". Synthesize all three:

\# {TOPIC\_A} vs {TOPIC\_B}: What the Community Says (Last 30 Days)

\#\# Quick Verdict

\[1-2 sentences: which the community prefers and why, with source counts\]

\#\# {TOPIC\_A}

Community sentiment: \[Positive / Mixed / Negative\] ({N} mentions across {sources})

Strengths: \[bullet points with source attribution\]

Weaknesses: \[bullet points with source attribution\]

\#\# {TOPIC\_B}

Community sentiment: \[Positive / Mixed / Negative\]

Strengths: \[bullet points with source attribution\]

Weaknesses: \[bullet points with source attribution\]

\#\# Head-to-Head

| Dimension | {TOPIC\_A} | {TOPIC\_B} |

|-----------|-----------|-----------|

| \[dim 1\]   | ...       | ...       |

\#\# Bottom Line

Choose {TOPIC\_A} if... | Choose {TOPIC\_B} if...

(based on actual community data, not assumptions)

---

### If QUERY\_TYPE \= product or opinion (RECOMMENDATIONS)

Most mentioned: {TOPIC}

\[Item Name\] — {N}x mentions

What it is: \[1 sentence\]

Why people recommend it: \[key reasons\]

Sources: @handle, r/subreddit, \[publication\]

\[Item Name\] — {N}x mentions

...

Notable mentions: \[items with 1-2 mentions\]

---

### If QUERY\_TYPE \= breaking\_news, concept, how\_to, or prediction

What I learned about {TOPIC}:

\*\*\[Finding 1\]\*\* — \[1-2 sentences on what people are saying, cite source\]

\*\*\[Finding 2\]\*\* — \[1-2 sentences, cite source\]

\*\*\[Finding 3\]\*\* — \[1-2 sentences, cite source\]

KEY PATTERNS from the research:

1\. \[Pattern\] — per @handle or r/subreddit

2\. \[Pattern\] — per source

3\. \[Pattern\] — per source

---

## Citation Rules

**Priority order — use the highest available:**

1. @handles from X — "per @handle"  
2. r/subreddits — "per r/subreddit" (prefer quoting top comments over thread titles)  
3. YouTube channels — "per \[Channel Name\] on YouTube"  
4. LinkedIn authors — "per \[Name\] on LinkedIn"  
5. HN — "per HN"  
6. TechCrunch — "per TechCrunch"  
7. Web — only when other sources don't cover that specific fact

**Rules:**

- 1-2 citations per finding — never chain multiple ("per @x, @y, @z" → pick the strongest one)  
- Never paste raw URLs — use source names only  
- Lead with people, not publications — the value is what real people are saying

---

## Step 6 — Stats Block

After synthesis, display this. **Calculate actual totals from what agents returned. Omit any line with 0 results.**

\---

✅ Research complete\!

├─ 🟠 Reddit: {N} posts │ {N} upvotes │ {N} comments

├─ 🔵 X: {N} posts │ {N} likes │ {N} reposts

├─ 🔴 YouTube: {N} videos │ {N} views

├─ 💼 LinkedIn: {N} posts │ {N} likes │ {N} comments

├─ 🟡 HN: {N} stories │ {N} points │ {N} comments

├─ 🌐 Web: {N} pages — Source, Source, Source

├─ 📰 TechCrunch: {N} articles

├─ 🔗 Cross-source signals: {N} stories appeared on 2+ platforms

└─ 🗣️ Top voices: @{handle} ({N} likes), r/{sub}, \[LinkedIn name\]

\---

For the Web line — strip protocol/path, use readable publication name only (e.g. techcrunch.com/... → TechCrunch, buffer.com/... → Buffer). Never paste URLs.

---

## Step 7 — Follow-Up Invitation

End with an invitation referencing **specific things you actually found** — not generic suggestions:

I'm now up to date on {TOPIC} from the last 30 days.

Want me to go deeper on anything? For example:

\- \[Specific finding \#1 from research\]

\- \[Specific finding \#2 from research\]

\- \[Specific finding \#3 from research\]

---

## Rules

- Never fabricate findings — only synthesize what the agents actually returned  
- Cross-source signals are the strongest evidence — always lead with them  
- If all sources return no results, say so clearly and suggest the user refine the topic  
- Keep the report focused — prioritize signal over volume  
- Self-check before publishing: does your synthesis match what the research ACTUALLY says? Rewrite if you catch yourself using prior knowledge instead of the research output.

---

## Anti-Hallucination Guardrails

**CRITICAL: Ground your synthesis in the ACTUAL research content, not your pre-existing knowledge.**

Read the research output carefully. Pay attention to:

- **Exact product/tool names** mentioned — if research mentions "ToolX", that is a DIFFERENT product than something similar you already know. Don't conflate them.  
- **Specific quotes and insights** from the sources — use THESE, not generic knowledge  
- **What the sources actually say**, not what you assume the topic is about

**ANTI-PATTERN TO AVOID**: If user asks about "topic A" and research returns content about "topic A variant", do NOT synthesize as a different but related topic just because they sound similar. Read what the research actually says.

**SELF-CHECK before displaying**: Re-read your "What I learned" section. Does it match what the research ACTUALLY says? If you catch yourself projecting your own knowledge instead of the research, rewrite it.

---

## WAIT FOR USER RESPONSE

**After displaying the report and follow-up invitation — STOP.**

Do NOT call any more tools. Do NOT keep writing. Wait for the user to respond.

---

## Context Memory

After research is complete, store these for the rest of the conversation:

- **TOPIC**: {topic}  
- **QUERY\_TYPE**: {type}  
- **KEY PATTERNS**: {top 3-5 patterns you actually found}  
- **TOP SOURCES**: {highest-engagement @handles, subreddits, channels}  
- **RESEARCH FINDINGS**: {key facts and insights from the research}

**Treat yourself as an EXPERT on this topic for the rest of the conversation.**

When the user asks follow-up questions:

- **DO NOT run new searches** — you already have the research  
- **Answer from what you learned** — cite the Reddit threads, X posts, YouTube channels, LinkedIn authors  
- **Only do new research** if the user explicitly asks about a DIFFERENT topic

---

## When User Responds

Read their response and match the intent:

- If they ask a **QUESTION** about the topic → Answer from your research (no new searches)  
- If they ask to **GO DEEPER** on a subtopic → Elaborate using your research findings  
- If they describe something they want to **CREATE** → Write one tailored prompt (see below)  
- If they ask for a **PROMPT** explicitly → Write one tailored prompt (see below)

**Only write a prompt when the user wants one.** Don't force a prompt on someone who asked a question.

---

## Writing a Prompt

When the user wants a prompt, write a **single, highly-tailored prompt** using your research expertise.

**CRITICAL: Match the FORMAT the research recommends.** If research says to use a specific structure, style, or format — use it. Don't write generic prose when research found that structured prompts work better, or vice versa.

**Quality checklist before delivering:**

- [ ] Format matches what the research actually recommended  
- [ ] Directly addresses what the user said they want to create  
- [ ] Uses specific patterns/keywords discovered in research  
- [ ] Ready to paste with zero edits (or minimal \[PLACEHOLDERS\] clearly marked)

**Output format:**

Here's your prompt:

\---

\[The actual prompt\]

\---

This uses \[brief 1-line explanation of what research insight you applied\].

---

## After Each Prompt

End with a footer showing what the research was based on, then offer more:

\---

📚 Expert in: {TOPIC}

📊 Based on: {N} Reddit posts ({N} upvotes) \+ {N} X posts ({N} likes) \+ {N} YouTube videos ({N} views) \+ {N} LinkedIn posts \+ {N} HN stories \+ {N} web pages \+ {N} TechCrunch articles

Want another prompt? Just tell me what you're creating next.

Omit any source line that returned 0 results.

---

## Query-Type Follow-Up Invitations

Use the matching format based on QUERY\_TYPE (Step 7):

**If product or opinion (RECOMMENDATIONS):**

\---

I'm now an expert on {TOPIC}. Want me to go deeper? For example:

\- \[Compare specific item A vs item B from the results\]

\- \[Explain why item C is trending right now\]

\- \[Help you get started with item D\]

**If breaking\_news or concept (NEWS/GENERAL):**

\---

I'm now an expert on {TOPIC}. Some things you could ask:

\- \[Specific follow-up question about the biggest story from research\]

\- \[Question about implications of a key development\]

\- \[Question about what might happen next based on current trajectory\]

**If how\_to (HOW-TO):**

\---

I'm now an expert on {TOPIC}. Want me to go deeper? For example:

\- \[Step-by-step breakdown of the most recommended approach\]

\- \[Common pitfall people mention and how to avoid it\]

\- \[Write you a ready-to-use prompt/template based on the research\]

**If comparison (COMPARISON):**

\---

I've compared {TOPIC\_A} vs {TOPIC\_B} using the latest community data. Some things you could ask:

\- \[Deep dive into {TOPIC\_A} strengths based on what the research found\]

\- \[Deep dive into {TOPIC\_B} strengths based on what the research found\]

\- \[Focus on a specific dimension from the comparison table\]

**If prediction (PREDICTION):**

\---

I'm now up to date on {TOPIC} predictions from the last 30 days. Some things you could ask:

\- \[Most cited reason for the leading outcome, per research\]

\- \[The biggest dissenting view from the research\]

\- \[What signal to watch next based on what sources are tracking\]

---

## Security & Permissions

**What this skill does:**

- Calls Apify actors (trudax/reddit-scraper-lite, apidojo/tweet-scraper, streamers/youtube-scraper, harvestapi/linkedin-post-search) via Apify MCP — requires Apify account and Apify MCP connected to Claude Code  
- Queries the Algolia Hacker News Search API (hn.algolia.com) — free, no auth required  
- Uses Claude's native WebSearch for web and TechCrunch results  
- Uses Claude's native WebFetch to read full page/article content

**What this skill does NOT do:**

- Does not post, like, or modify content on any platform  
- Does not access your Reddit, X, YouTube, or LinkedIn accounts  
- Does not store or log any API keys  
- Does not send data to any endpoint not listed above

**Estimated cost per run:** \~$0.10–$0.20 on Apify Starter plan ($29/month).

---

## Requirements

This skill requires an **Apify account** with the Apify MCP server connected to Claude Code.

**Apify actors used:**

- trudax/reddit-scraper-lite — Reddit posts  
- apidojo/tweet-scraper — X/Twitter posts  
- streamers/youtube-scraper — YouTube videos  
- harvestapi/linkedin-post-search — LinkedIn posts

**No API keys needed** for Hacker News (Algolia API is free) or Web/TechCrunch (Claude native WebSearch \+ WebFetch).

**Estimated cost per run:** \~$0.10–$0.20 on Apify Starter plan ($29/month).  
