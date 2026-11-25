---
name: openmark-weekly-digest
description: Produce a weekly digest of what Ahmad saved in OpenMark over a given time window, clustered by topic. Use whenever Ahmad asks "what did I save this week", "what's new in OpenMark", "last week's saves", "this week's bookmarks", "what happened in my feed", "weekly recap", or any temporal summary of saved content. Faster than full newsletter — output is a scannable digest, not a published post. Triggers on "this week", "last week", "what's new", "weekly digest", "recent saves", "recap".
metadata:
  type: composition
---

# OpenMark — Weekly Digest

What Ahmad saved in the last N days, clustered by topic, scannable in 60 seconds. NOT a newsletter — this is internal recon: "what should I pay attention to from my own saves."

## When to use vs newsletter

| Asker says | Skill |
|---|---|
| "what did I save this week" | weekly-digest (this) |
| "give me a recap of last week" | weekly-digest |
| "write me a newsletter on this week's AI saves" | openmark-newsletter |
| "what's new in OpenMark" | weekly-digest |

Digest is private notes. Newsletter is a publishable post.

## Tool sequence

1. **Get window.** Default: last 7 days. Ahmad can override ("last 30 days", "since yesterday", "this month").
2. **Pull recent:** `find_recent(days=N, n=40)` — empty query, just get everything fresh.
3. **If thin (< 10 results):** the time filter only matches nodes with `created_at` set, which today is only LinkedIn. Fall back to `find_by_source(source="linkedin", n=30)` and warn Ahmad: "Only LinkedIn nodes have timestamps. Edge/Raindrop/YouTube need backfill before they show up in time queries."
4. **Cluster.** Read the categories of returned hits. Group into 3–6 topical buckets by category + tag overlap. Examples:
   - "Agent frameworks" (LangChain, LangGraph, Agent Development)
   - "RAG patterns" (RAG & Vector Search)
   - "Models + research" (Data Science & ML, AI Tools)
   - "Tooling I want to try" (GitHub Repos & OSS with score ≥ 6)
   - "LinkedIn discourse" (LinkedIn posts, often with takes)

## Output format

```
# OpenMark digest — last {N} days
**{total_count} new items · {bucket_count} clusters**

## {Bucket 1 name}  ({count})
- {Title} — {URL} — {one-line so-what}
- {Title} — {URL} — {one-line so-what}
- ... (max 6 per bucket)

## {Bucket 2 name}  ({count})
...

---
**Quick stats**
- By source: {raindrop: N, linkedin: M, edge: K, ...}
- Top tags: {tag1 (n), tag2 (n), tag3 (n)}
- Highest similarity in window: {Title} — {URL} ({sim:.2f})
```

## Rules

- **Buckets must be inferred from the data**, not preset. If everything is one topic, output one bucket — don't fake variety.
- **No "key takeaways" section.** Ahmad scans this, he doesn't need conclusions.
- **Order buckets by count desc** so the heavy stuff is on top.
- **Within a bucket, sort by similarity if a query was provided, else by `bm_score` desc.**
- Cap each bucket at 6 items. If more, append `... and N more` with a follow-up suggestion: `(run: search_by_category('X') for the full list)`.

## What NOT to do

- Don't editorialize ("this is interesting because…"). Ahmad makes those calls.
- Don't fetch full page content (no WebFetch) — this is a fast digest, not deep research.
- Don't drop items just because the title is bare. The URL is the value; render whatever title exists or use `(no title)` as fallback.
