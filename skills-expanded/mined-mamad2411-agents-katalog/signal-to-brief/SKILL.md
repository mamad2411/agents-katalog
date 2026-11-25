---
name: signal-to-brief
description: Transforms real-time social signal from Reddit and other communities into structured product opportunity briefs. Use this skill whenever the user wants to find product ideas from Reddit, analyze pain points in a market, scan subreddits for opportunities, turn community complaints into product concepts, or do any form of social-signal-driven product research. Also triggers on phrases like "what are people complaining about in X", "find product ideas in X space", "scan Reddit for opportunities", or "what problems exist in X market". Always use this skill for these tasks — do not attempt them without it.
---

# Signal-to-Brief

Converts raw community signal from Reddit (and optionally Hacker News, Product Hunt, Dev.to) into structured product opportunity briefs using a 3-stage extraction chain.

## Prerequisites

Install both free MCP servers before running:

**RivalSearchMCP** (Reddit + HN + Product Hunt + Dev.to + Medium):
```bash
claude mcp add --transport http RivalSearchMCP https://RivalSearchMCP.fastmcp.app/mcp
```

**Reddit MCP Buddy** (deep Reddit — subreddit browsing, hot posts, search, comments):
```bash
claude mcp add --transport stdio reddit-mcp-buddy -s user -- npx -y reddit-mcp-buddy
```

---

## The 3-Stage Chain

### Stage 1: Subreddit Mapping

Given a topic/vertical, derive the 4-6 most signal-rich subreddits. Prioritize communities where users self-report problems, not communities where users discuss the topic academically.

**Prompt template:**
```
Topic: [USER_TOPIC]

Identify 4-6 subreddits where people who experience this problem domain are most likely to:
- Complain about specific failures
- Ask for help with workarounds
- Share frustrating experiences
- Request tools or solutions that don't exist

Return: subreddit names only, one per line, no r/ prefix.
Exclude: news/discussion subreddits where users analyze the topic rather than live it.
```

---

### Stage 2: Signal Ingestion

Pull signal using both MCP servers in parallel. They have distinct roles — do not use them interchangeably.

**MCP division of labor:**
- **reddit-mcp-buddy** — all Reddit signal. Use this for every Reddit query.
- **RivalSearchMCP** — cross-platform only: Hacker News, Product Hunt, Dev.to, Medium. Do not run RivalSearchMCP against Reddit subreddits — it duplicates reddit-mcp-buddy at extra cost.

---

**reddit-mcp-buddy — search first, browse second:**

Search produces higher-signal results than hot-feed browsing. Run 2–3 targeted queries with pain language before any browse calls. Keep subreddits to **2 per search call** — larger batches fail silently with no partial result.

```
search_reddit(
  query="[pain language] [topic]",
  subreddits=["sub1", "sub2"],
  sort="top",
  time="year",
  limit=25
)
```

Browse is a secondary pass. Always set `limit: 25` — the default (50) produces outputs too large to read in a single pass.

```
browse_subreddit(subreddit="[subreddit]", sort="hot", limit=25)
```

**Run in two sequential waves to avoid rate limits (10 req/min unauthenticated):**
1. Wave 1 — run all search calls in parallel. Wait for results.
2. Wave 2 — run browse calls in parallel after search completes. Limit to 2–3 subreddits max.

If search results are already high-density (strong signal, clear workarounds), skip Wave 2 entirely.

---

**RivalSearchMCP — cross-platform signal (optional, strongest for B2B verticals):**

```
social_search(
  query="[topic] [pain language]",
  platforms=["hackernews", "devto", "producthunt"]
)
```

**Signal language to flag and collect:**
- "I have to manually..."
- "I've been using [X] as a workaround but..."
- "Why doesn't [product] just..."
- "Anyone else dealing with..."
- "I wish someone would build..."
- "I've given up trying to..."
- "I pay for [X] but it still doesn't..."
- "Every time I have to [task] I want to..."

Collect raw signal in this format — consistent structure feeds Stage 3 cleanly:
- [r/subreddit · ~N upvotes] "exact quote or close paraphrase"
- [HN/Dev.to/etc · N points] "quote or paraphrase"

One line per signal instance. Keep the source tag and engagement count — Stage 3 uses them to score frequency and validate cross-community spread.

---

### Stage 3: Brief Extraction

Feed all collected signal into this extraction prompt. Run once after all signal is collected.

**Extraction system prompt:**
```
You are a product researcher extracting validated opportunity signals from community data.

INPUT: Raw signal from Reddit and social communities about [TOPIC].

TASK: Identify distinct product opportunities. Each opportunity must be grounded in multiple signal instances — do not invent opportunities not present in the data.

For each opportunity, extract:

{
  "problem_statement": "One sentence in the user's register, not product language",
  "target_user": "Behavioral description — what they're doing, not who they are demographically",
  "frequency_signal": "rare | moderate | high — based on distinct post/comment count",
  "workaround_evidence": "Exactly what people are doing instead. This is required. If no workaround is described, mark as 'none documented — validate before proceeding'",
  "incumbent_gap": "Why current tools fail this user — be specific, not generic",
  "product_hypothesis": "One sentence. What would you build. Start with a verb.",
  "validation_questions": ["2-3 questions to run in follow-up research before building"],
  "signal_strength": "weak | moderate | strong — based on: frequency + workaround evidence + engagement on related posts",
  "raw_signal_count": number,
  "source_subreddits": ["list"]
}

SCORING RULES:
- signal_strength = strong only if: frequency is high AND workaround evidence exists AND multiple subreddits surface the same signal
- signal_strength = moderate if: frequency is moderate OR workaround exists but signal is isolated to one community
- signal_strength = weak if: frequency is rare OR no workaround documented

Sort output: strong → moderate → weak.
Return as JSON array.
```

---

## Output Format

Before rendering output, check what write tools are available — in this priority order:

- **mcp__obsidian__write_note available:** Write briefs to the vault at `signal-to-brief/briefs/[topic-slug]-[YYYY-MM-DD].md`. Confirm the vault path to the user after writing. Do not print the full briefs to chat.
- **Write tool (Claude Code) or write_file tool (Gemini CLI) available, no Obsidian MCP:** Write briefs to a markdown file in the current working directory. Filename: `signal-brief-[topic-slug]-[YYYY-MM-DD].md`. Confirm the file path to the user after writing. Do not print the full briefs to chat.
- **Neither available:** Render briefs directly in chat as a structured list.

The markdown file format for each brief:

```
## [problem_statement]

**Who:** [target_user]
**Signal:** [frequency_signal] · [raw_signal_count] instances · [source_subreddits]
**Workaround:** [workaround_evidence]
**Gap:** [incumbent_gap]

**Build:** [product_hypothesis]

**Validate first:**
- [validation_questions[0]]
- [validation_questions[1]]
- [validation_questions[2]]

Signal strength: [signal_strength]
---
```

Deliver all strong briefs first, then moderate, then weak. Do not editorialize or add commentary between briefs — let the signal speak.

---

## Usage Examples

```bash
# Scan a vertical
"Run signal-to-brief on the indie SaaS / bootstrapped founder tooling space"

# Specific problem area
"signal-to-brief: what are the biggest pain points in Shopify app development"

# Competitive research angle
"Use signal-to-brief to find gaps in the project management tool space"
```

---

## Notes

- Workaround evidence is the strongest validation signal in the dataset. A community describing a workaround is a community that has already validated demand and found no satisfying solution.
- Re-run against the same vertical every 4–6 weeks. Signal shifts. What's "no solution" today may have an incumbent next month.
- For B2B verticals, supplement Reddit with Hacker News via RivalSearchMCP — HN comments on relevant Show HN posts are dense with product feedback.
