---
name: reddit-harvest
description: >
  Playwright-driven Reddit quote harvester for the "From the Wild" content pipeline.
  Uses a logged-in browser session to search subreddits, extract pain quotes with full
  metadata, score them using wild-scan's rubric, and export in wild-scan format. Feeds
  directly into wild-scan Phase 3+ (scoring, clustering, briefs).
license: MIT
metadata:
  context: fork
  openclaw:
    emoji: "\U0001F4E1"
    requires:
      mcp: ["playwright"]
---

# Reddit Harvest

Drive a logged-in Reddit browser session via Playwright MCP to harvest pain quotes that web search can't reach. Output conforms to wild-scan format — drop it straight into the content pipeline.

## Step 0: Load Conventions

Before doing ANYTHING, read the shared conventions file:

```
Read ${SKILLS_DIR}/_conventions.md
```

This file defines: canonical vault path, folder-to-type mapping, frontmatter contract, valid statuses, tag hierarchy, cross-reference syntax, and the PipelineEnvelope schema. All output from this skill MUST conform to those conventions. If there is a conflict between this SKILL.md and `_conventions.md`, the conventions file wins.

## When to Use

- wild-scan's web search can't reliably access Reddit (`site:reddit.com` queries get blocked)
- You need a targeted harvest from specific subreddits
- You want deeper comment extraction than search snippets provide
- Supplementing a wild-scan run with Reddit-specific quotes
- Building a Reddit-only quote index for a topic

## Trigger Phrases

- "Harvest Reddit for [topic] pain"
- "Reddit scan for [topic]"
- "Scrape Reddit for [topic] quotes"
- "Run reddit-harvest on [topic]"
- "/reddit-harvest [topic]"
- "Get me Reddit quotes about [topic]"

---

## Prerequisites

Before starting, establish with the user:

1. **Topic focus** — What specific area to harvest (e.g., "Kubernetes deployment pain", "Terraform state management")
2. **Target subreddits** — Specific subreddits to search, or use defaults from [references/subreddit-targets.md](references/subreddit-targets.md)
3. **Min engagement threshold** — Minimum upvotes to consider a post worth drilling into (default: 10)
4. **Pain queries** — Specific search terms, or use defaults from wild-scan's [search-playbook.md](${SKILLS_DIR}/wild-scan/references/search-playbook.md)
5. **Posts per subreddit** — How many top posts to drill into per subreddit (default: 10)

If the user says "just go" with a topic, use these defaults:
- **Subreddits**: Top 3-5 from the topic's domain in subreddit-targets.md
- **Engagement threshold**: 10 upvotes
- **Pain queries**: Frustration + help-seeking + gap queries from search-playbook.md
- **Posts per subreddit**: 10

### Browser Session Requirement

**The user MUST be logged into Reddit in the Playwright browser before this skill runs.** The skill does not handle login — it assumes an authenticated session.

To verify, the skill checks login state at the start of Phase 1 (see below). If not logged in, stop and ask the user to log in.

---

## Workflow

```
User logs into Reddit in Playwright browser
    |
Skill receives: topic + subreddits + pain queries
    |
Phase 1: Search — Navigate to subreddit search URLs
    |
Phase 2: Scan — Snapshot pages, identify high-signal posts
    |
Phase 3: Harvest — Click into threads, extract quotes + metadata
    |
Phase 4: Score — Apply wild-scan 4-dimension rubric
    |
Phase 5: Export — Write vault Markdown + JSON in wild-scan format
```

---

## Phase 1: Search

### Load References

Read these files before starting:

```
Read ${SKILLS_DIR}/reddit-harvest/references/selectors.md
Read ${SKILLS_DIR}/reddit-harvest/references/subreddit-targets.md
Read ${SKILLS_DIR}/wild-scan/references/scoring-rubric.md
Read ${SKILLS_DIR}/wild-scan/references/search-playbook.md
```

### Verify Login

Navigate to Reddit and check login state:

1. `browser_navigate` to `https://www.reddit.com`
2. `browser_evaluate` with the login-check snippet from selectors.md
3. If not logged in → **STOP**. Tell the user: "Please log into Reddit in the browser window. I'll wait."
4. If logged in → proceed

### Build Search URLs

For each subreddit + pain query combination, construct:

```
https://www.reddit.com/r/{subreddit}/search/?q={pain_query}&sort=top&t=year
```

Pain query categories (from search-playbook.md, adapted for direct Reddit search):

**Frustration signals:**
```
"I hate" OR "I'm frustrated" OR "nightmare"
"why is it so hard" OR "am I dumb" OR "what am I missing"
"wasted hours" OR "wasted days" OR "spent all weekend"
```

**Help-seeking signals:**
```
"how do I actually" OR "serious question"
"I finished the tutorial" OR "tutorial hell"
"where do I start" OR "overwhelmed"
```

**Gap signals (tutorial-to-production):**
```
"nobody teaches" OR "no one explains"
"real world" OR "production" OR "not hello world"
```

**Wish signals (latent demand):**
```
"I wish" OR "if only" OR "someone should make"
```

### Execute Searches

For each search URL:

1. `browser_navigate` to the URL
2. Wait for results to load: `browser_wait_for` with a reasonable selector (e.g., any post link)
3. `browser_evaluate` with the search results extraction script from selectors.md
4. Collect all post data into a master list

**Pace yourself.** Wait 1-2 seconds between navigations to avoid rate limiting. If Reddit shows a rate-limit page, pause for 30 seconds and retry.

---

## Phase 2: Scan

### Filter and Rank

From the master post list:

1. **Deduplicate** — same post may appear in multiple query results (match by `postId`)
2. **Filter** — remove posts below the engagement threshold
3. **Rank** — sort by comment count descending (more comments = more quote potential)
4. **Select** — take top N per subreddit (default: 10)

### Present Scan Summary

Show the user a summary before drilling into threads:

```
## Scan Summary

Searched: r/devops, r/kubernetes, r/terraform
Queries: 4 pain-query categories x 3 subreddits = 12 searches
Posts found: 87 (after dedup)
Posts above threshold (10+ upvotes): 43
Selected for harvest: 30 (top 10 per subreddit)

Top posts by engagement:
1. "Why does nobody teach real CI/CD?" — r/devops, 342 upvotes, 89 comments
2. "Terraform state is a nightmare" — r/terraform, 256 upvotes, 67 comments
...
```

If the user wants to adjust (add/remove posts, change subreddits), do so before proceeding.

---

## Phase 3: Harvest

For each selected post, extract quotes:

### Thread Extraction Flow

1. `browser_navigate` to the post URL
2. `browser_run_code` with the scroll-and-load script from selectors.md (loads lazy comments)
3. `browser_evaluate` with the post metadata extraction script
4. `browser_evaluate` with the comment extraction script

### Quote Selection

Not every comment is a harvestable quote. From the extracted comments, select those that:

- **Are pain statements** — frustration, struggle, help-seeking, wishing (not advice-giving, not jokes, not meta-discussion)
- **Have substance** — minimum ~50 characters of meaningful content (not just "same" or "+1")
- **Have engagement** — prioritize comments with upvotes (use the engagement threshold, but can be lower than the post threshold — even 5+ upvotes on a comment is signal)

### For Each Harvestable Quote, Capture:

| Field | Source |
|-------|--------|
| `quote` | Exact comment text from extraction |
| `author` | `u/{author}` from extraction |
| `platform` | `"reddit"` (hardcoded) |
| `community` | `r/{subreddit}` from post metadata |
| `url` | Comment permalink from extraction |
| `date` | Comment timestamp from extraction |
| `engagement.metric` | `"upvotes"` |
| `engagement.value` | Comment upvote count |
| `engagement.replies` | Reply count from extraction |
| `engagement.same_here_count` | Run same-here detection script from selectors.md |
| `context` | Post title + parent comment text (if the quote is a reply) |
| `pain_category` | Run pain-category matcher from selectors.md, then verify manually |

### Same-Here Detection

For high-value comments (20+ upvotes), run the same-here detection script from selectors.md to count agreement replies. This feeds the engagement scoring dimension.

### Progress Updates

After every 5 threads, update the user:

```
Harvested 5/30 threads. 23 quotes so far. Continuing...
```

---

## Phase 4: Score

Apply wild-scan's 4-dimension scoring rubric to every harvested quote. See the full rubric at:

```
${SKILLS_DIR}/wild-scan/references/scoring-rubric.md
```

### Scoring Summary

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Specificity | 2x | Names tools, versions, exact scenarios vs. vague complaints |
| Intensity | 2x | Emotional language, time/effort wasted, desperation level |
| Solvability | 2x | Can we build a repo that demolishes this? |
| Engagement | 1x | Social proof — upvotes calibrated by platform |

### Reddit-Specific Engagement Calibration

From the scoring rubric's platform table:

| Type | Low (1-3) | Medium (4-6) | High (7-8) | Extreme (9-10) |
|------|-----------|--------------|------------|----------------|
| Reddit comment | 0-10 upvotes | 10-50 upvotes | 50-200 upvotes | 200+ upvotes |
| Reddit post | 0-20 upvotes | 20-100 upvotes | 100-500 upvotes | 500+ upvotes |

**Niche subreddit adjustment:** If harvesting from a small subreddit (<100K members), boost engagement score by +1 for the same upvote counts. 30 upvotes on r/terraform is worth more than 30 on r/programming.

### Overall Score

```
overall = (specificity * 2 + intensity * 2 + solvability * 2 + engagement * 1) / 7
```

### Scoring Discipline

Every score MUST have a one-sentence justification. Example:

```
specificity: 8 — "Calls out the exact gap: passing secrets from GitHub Actions to EKS."
intensity: 7 — "Used 'losing my mind', described 3 days of debugging."
solvability: 9 — "A secrets-management tutorial with working GHA + EKS config would directly solve this."
engagement: 6 — "47 upvotes, 12 replies including 3 'same here' responses."
overall: 7.7
```

---

## Phase 5: Export

Produce two output files matching wild-scan's format exactly.

**Vault path:** `${VAULT}/`

### 1. Markdown Quote Index

**Path:** `{vault}/Writing/From-The-Wild/{topic-slug}-reddit-{YYYY-MM-DD}.md`

```markdown
---
type: wild-index
date: YYYY-MM-DD
status: active
topic: "[topic focus]"
source: reddit-harvest
platforms_searched:
  - reddit
subreddits: [list of subreddits searched]
quote_count: N
tags:
  - content/from-the-wild
  - hunter/domain/{domain-slug}
---

# Reddit Harvest: [Topic]

**Date**: YYYY-MM-DD
**Source**: reddit-harvest (Playwright MCP)
**Subreddits**: r/sub1, r/sub2, r/sub3
**Quotes harvested**: N
**Engagement threshold**: X upvotes

## Summary Stats

| Metric | Value |
|--------|-------|
| Subreddits searched | N |
| Posts scanned | N |
| Quotes harvested | N |
| Avg overall score | X.X |
| Quotes scoring 7+ | N |
| Top pain category | [category] |

## Top Quotes (Score 7+)

### 1. (Score: X.X)
> "[Full quote text]"
> — u/[author], r/[subreddit], [upvotes] upvotes

- **Pain category**: [category]
- **URL**: [permalink]
- **Context**: [post title / parent comment]
- **Scoring**: specificity X, intensity X, solvability X, engagement X

### 2. (Score: X.X)
[repeat for all quotes scoring 7+]

## All Quotes by Subreddit

### r/[subreddit1]

| Score | Quote (truncated) | Author | Upvotes | Category |
|-------|-------------------|--------|---------|----------|
| X.X | "[first 80 chars]..." | u/name | N | [cat] |

### r/[subreddit2]
[repeat]

## Full Quote Log

### Quote 1 (Score: X.X)
> "[Full quote text]"

- **Author**: u/[username]
- **Platform**: reddit
- **Community**: r/[subreddit]
- **URL**: [permalink]
- **Date**: [timestamp]
- **Engagement**: [upvotes] upvotes, [replies] replies, [same_here] "same here"
- **Context**: [post title]
- **Pain category**: [category]
- **Scoring**:
  - specificity: X — "[justification]"
  - intensity: X — "[justification]"
  - solvability: X — "[justification]"
  - engagement: X — "[justification]"

### Quote 2 (Score: X.X)
[repeat for all quotes]
```

### 2. JSON Index

**Path:** `{vault}/Writing/From-The-Wild/wild-scan-{topic-slug}-reddit-{YYYY-MM-DD}.json`

Conforms to wild-scan's `output-schema.json`. The JSON structure:

```json
{
  "scan_metadata": {
    "topic": "[topic]",
    "date": "YYYY-MM-DD",
    "learning_stage": "[stage from user or inferred]",
    "repo_angle": "[angle from user or inferred]",
    "platforms_searched": ["reddit"],
    "total_quotes": N
  },
  "quotes": [
    {
      "quote": "[exact text]",
      "author": "u/[username]",
      "platform": "reddit",
      "community": "r/[subreddit]",
      "url": "[permalink]",
      "date": "[timestamp]",
      "engagement": {
        "metric": "upvotes",
        "value": N,
        "replies": N,
        "same_here_count": N
      },
      "context": "[post title + parent if reply]",
      "pain_category": "[category]",
      "scores": {
        "specificity": { "value": N, "justification": "..." },
        "intensity": { "value": N, "justification": "..." },
        "solvability": { "value": N, "justification": "..." },
        "engagement": { "value": N, "justification": "..." }
      },
      "overall_score": N,
      "theme_id": "[assigned during wild-scan Phase 4]"
    }
  ],
  "themes": [],
  "content_briefs": []
}
```

**Note on `themes` and `content_briefs`:** reddit-harvest exports these as empty arrays. Theme clustering and brief generation happen in wild-scan Phases 4-6. The JSON is valid against the schema with empty arrays — the `minItems: 15` constraint applies to `quotes`, not themes or briefs.

If the operator wants to run a complete pipeline (harvest + cluster + brief) in one session, they can invoke wild-scan after reddit-harvest finishes, pointing it at the exported JSON.

### Pipeline Integration

After export, the output is ready for:

1. **wild-scan Phase 4** — Feed the JSON into theme clustering. wild-scan reads quotes from the JSON and clusters them.
2. **content-planner** — The Markdown file lands in `Writing/From-The-Wild/` where content-planner picks it up on its next scan.
3. **Manual review** — The Markdown file is readable in Obsidian for direct browsing and editing.

---

## Rate Limiting & Etiquette

- **Navigation pace**: Wait 1-2 seconds between page loads
- **Comment loading**: The scroll script has built-in 750ms pauses
- **If rate-limited**: Reddit shows an interstitial. Pause 30-60 seconds, then retry the same URL
- **Session length**: A typical harvest (3 subreddits, 10 posts each) takes 15-25 minutes of browser time
- **Don't overdo it**: One harvest session per topic per day is plenty. Reddit may flag accounts with excessive automated browsing.

---

## Quality Checklist

Run this before delivering results:

- [ ] Browser session verified as logged in before starting
- [ ] All target subreddits searched with pain queries
- [ ] Posts filtered by engagement threshold and ranked by comment count
- [ ] Minimum 15 quotes harvested (aim for 20-30)
- [ ] Every quote has: exact text, author, r/subreddit, permalink, upvotes, timestamp, context
- [ ] Same-here detection run on high-value comments (20+ upvotes)
- [ ] Pain category auto-suggested and verified for each quote
- [ ] Every quote scored on 4 dimensions with one-sentence justifications
- [ ] Engagement scores use Reddit-specific calibration from scoring rubric
- [ ] Niche subreddit adjustment applied where appropriate
- [ ] Markdown file has correct frontmatter (type: wild-index, source: reddit-harvest)
- [ ] JSON file conforms to wild-scan output-schema.json
- [ ] Both files written to `{vault}/Writing/From-The-Wild/`
- [ ] No duplicate quotes from previous wild-scan or reddit-harvest runs (check existing indices)
- [ ] User shown summary stats before and after harvest

---

## Resources

### Internal References
- `references/selectors.md` — Reddit DOM selectors and extraction JavaScript
- `references/subreddit-targets.md` — Priority subreddits by domain

### Wild-Scan References (consumed, not duplicated)
- `${SKILLS_DIR}/wild-scan/references/scoring-rubric.md` — 4-dimension scoring calibration
- `${SKILLS_DIR}/wild-scan/references/search-playbook.md` — Pain query templates
- `${SKILLS_DIR}/wild-scan/references/output-schema.json` — JSON output schema

### Playwright MCP Tools Used
- `browser_navigate` — Load Reddit URLs
- `browser_wait_for` — Wait for page elements
- `browser_snapshot` — Accessibility tree for debugging
- `browser_evaluate` — Run extraction JavaScript (returns data)
- `browser_run_code` — Run scroll/interaction scripts (side effects)
- `browser_click` — Click into threads, load more comments
