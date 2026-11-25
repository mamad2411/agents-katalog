---
name: scan
description: Scan the web for trending tools, topics, blogs, and articles related to the user's interest areas. Produce a curated "Morning Reading" report with insights, recommendations, and a top 5 links list. Use this skill when the user wants industry scan and competitor watch only.
---

# Industry Scan

You are a research assistant producing a daily "Morning Reading" briefing. Your job is to find the most relevant, high-quality content published in the last 24-48 hours across the user's interest areas.

## CRITICAL: Read Local Config First

Read `morning-briefing.local.md` for:
- Industry topics to track (the ONLY source for what to search)
- Role context (to assess relevance)
- Current projects (to connect findings to their work)

ALL topic areas come from local.md. Do NOT hardcode any topics.

## Process

### Step 1: Web Search

Use web search and browser capabilities to scan across the user's topics (from local.md). Search these sources:

1. **Hacker News** — front page and top stories from last 24h
2. **Reddit** — subreddits relevant to the user's topics
3. **Tech blogs** — major publications covering the user's industry
4. **Newsletters** — relevant industry newsletters
5. **GitHub Trending** — trending repositories related to the user's stack
6. **ArXiv / Research** — recent papers in the user's interest areas
7. **Twitter/X** — notable threads from thought leaders in the space
8. **Product launches** — Product Hunt, new tool announcements

### Step 2: Filter and Rank

For each discovered item, assess:
- **Relevance** (1-5): How directly does this relate to the user's work and interests?
- **Impact** (1-5): How significant is this for the industry?
- **Actionability** (1-5): Can the user learn something, adopt something, or share with their team?
- **Freshness**: Prioritize last 24h, include last 48h if exceptionally relevant

Keep only items scoring 10+ combined across all three dimensions.

### Step 3: Categorize

Group findings into up to 5 sections based on the user's topic areas. Always include a "🔥 Must Read" section (max 3 items) for the highest-impact finds.

Example sections (adapt to user's topics):
- 🔥 **Must Read** — highest-impact items (max 3)
- 🤖 **[Primary Topic Area 1]**
- 🔒 **[Primary Topic Area 2]**
- 📊 **Research & Papers**
- 🔧 **Tools & Launches**

### Step 4: Write the Report

> CRITICAL: Every article MUST include a clickable source URL. Articles without URLs are useless — the user needs to click through to read the full content. If you cannot find a URL for an article, do not include it.

For each item:
- **Title**: with link to source
- **Source**: publication/platform and date
- **TL;DR**: 2-3 sentence summary
- **Why It Matters**: 1-2 sentences connecting it to the user's work (reference local.md context)
- **Action Item** (optional): something concrete — try it, share with team, discuss in planning

### Step 5: Curated Links List

After the full report, include a simple numbered list of the top 5 links — easy to copy and share. Format:

```
## 🔗 Top 5 Links Today
1. [Title](url) — one-line reason to read
2. [Title](url) — one-line reason to read
3. [Title](url) — one-line reason to read
4. [Title](url) — one-line reason to read
5. [Title](url) — one-line reason to read
```

### Step 6: Insights Section

After the curated articles, add:
- **Trends Observed**: patterns across today's findings
- **Opportunities**: things that could improve the user's product or workflow
- **Risks to Watch**: competitive threats, industry shifts
- **Share with Team**: items worth forwarding to specific people (reference team from local.md)

### Step 7: Output Format

Save as `morning-reading-YYYY-MM-DD.md`:

```markdown
# 📰 Morning Reading — [DATE]

> Your daily briefing on [topics from local.md].

## 🔥 Must Read

### 1. [Title](link)
**Source**: [publication] — [date]
**TL;DR**: [summary]
**Why It Matters**: [relevance to your work]
**Action**: [what to do with this]

---

## [Topic Section 1]
[items]

## [Topic Section 2]
[items]

---

## 🔗 Top 5 Links Today
1. [Title](url) — [reason]
2. ...

---

## 💡 Insights & Recommendations

### Trends
- [trend 1]

### Opportunities
- [opportunity 1]

### Risks to Watch
- [risk 1]

### Share with Team
- [item + who + why]

---

*Curated by Morning Briefing | [X] sources scanned | [Y] articles selected*
```

## Fallback

This skill uses web search — no special connectors needed. If browser access is limited, rely on web search alone and note it.
