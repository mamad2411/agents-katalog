---
name: openmark-newsletter-roundup
description: Compose a categorical news-roundup newsletter from Ahmad's OpenMark saves. Use when Ahmad wants a scannable "what happened in AI / tools / research / discourse" recap rather than a single-thesis essay. Trigger phrases include "roundup", "news roundup", "this week in AI", "weekly news", "what dropped this week", "category recap", "/newsletter-roundup". Output is bucketed by topic with 3–5 items per bucket, short blurbs, source-tagged for at-a-glance scanning.
metadata:
  type: composition
---

# OpenMark — Newsletter Roundup

Categorical news-roundup format. NOT thesis-driven — this is a scannable recap of what happened, organized by topic bucket. Reader skims headers, dives into 1-2 items.

## When to use vs other newsletter skills

| User intent | Skill |
|---|---|
| "What's happening in AI this week" | this one (roundup) |
| "Make me a newsletter on context engineering" | openmark-newsletter (analytical) |
| "Write me a thoughtful essay on X" | openmark-newsletter-essay |
| "Compare A vs B" | openmark-newsletter-comparison |
| "I want a LinkedIn-style post" | openmark-newsletter-thread |

## Tool sequence

1. **Get time window.** Default last 7 days. Ahmad can override.
2. **Pull recent fresh:** `find_recent(days=N, n=30)` — empty query.
3. **Cross-source angle:** `search_semantic(query="<broad area>", n=20)` (whatever broad area Ahmad named, e.g. "AI tooling, models, research").
4. **Source-specific gems (parallel):** `search_linkedin(query=..., n=10)` for hot takes, `search_youtube(query=..., n=10)` for video drops.
5. **Cluster.** Bucket the deduped hits into 3–6 topical groups:
   - "Models & research" — papers, model releases
   - "Tooling & open source" — github repos, libraries, frameworks
   - "Industry & business" — funding, partnerships, strategy
   - "Discourse & takes" — LinkedIn posts, opinions
   - "Tutorials & courses" — YouTube videos, blog tutorials
   - "Off-topic but interesting" — wildcards worth a click

Don't force all 6 — only use buckets that have ≥2 items.

## Output format — NON-NEGOTIABLE

```
# {Week of YYYY-MM-DD} — {Punchy 4-word headline}

_Quick recap of {N} items I saved {window}. {1-sentence pulse on the week.}_

## {Bucket 1 name}  ({count})

1. **{Title}** — [{domain}]({URL})

   {1-sentence so-what. Why this matters.}

2. **{Title}** — [{domain}]({URL})

   {1-sentence so-what.}

(repeat 3–5 items per bucket)

## {Bucket 2 name}  ({count})

(same pattern)

## Sources cited

1. [{title}]({URL})
2. [{title}]({URL})
...

_{N} items · {hours} of content · feed pulled {window}_
```

### Formatting rules — strictly enforced

- **One blank line between every numbered item.** Otherwise the chat collapses them into one wrapped paragraph.
- Each item: title in bold, then `—`, then a short clickable `[{domain}]({URL})` link (NOT the full URL pasted as text), then a blank line, then a single-sentence so-what indented or as its own line.
- Bucket headers are `##` — never `###` or bold-only.
- The trailing `## Sources cited` is mandatory so the chat auto-saves the draft.

## Voice

Tight, declarative, no hedging. Each so-what is ONE sentence. No "this could be useful," no "I found this interesting." Examples:

| Generic | Roundup voice |
|---|---|
| "This is an interesting paper about RAG." | "Argues every production RAG should use cross-encoder rerank. Has numbers." |
| "A new library for agents was released." | "Drop-in replacement for LangChain's `create_agent`. 40% fewer LOC, same hooks." |
| "Worth checking out." | "Skip unless you're shipping agents this week." |

## What NOT to do

- Don't editorialize ("the week was interesting") — let the items speak.
- Don't pick more than 5 items per bucket. If a bucket has 10, split into two sub-buckets or drop the bottom 5.
- Don't include URLs you didn't see in a tool result.
- Don't summarize at the end. The buckets ARE the summary.
