---
name: openmark-fast-search
description: Quick one-shot lookup over Ahmad's OpenMark bookmark knowledge graph (15k+ items from Edge, LinkedIn, YouTube, Raindrop). Use whenever Ahmad asks "find my bookmarks on X", "what did I save about X", "anything in OpenMark about X", or any single-topic search where he wants results in under 10 seconds. NOT for newsletter drafting or deep research — for those use openmark-deep-research or openmark-newsletter. Triggers on "find my", "what did I save", "openmark", "my bookmarks", "search bookmarks".
metadata:
  type: search
---

# OpenMark — Fast Search

Single-shot search over Ahmad's personal knowledge graph. Optimised for "I just want results, now."

## The recipe (in this exact order)

1. **One call**: `search_semantic(query=<user query>, n=12)`.
2. Inspect the returned `hits[]`. Each hit has `url`, `title`, `similarity`, `category`, `source`, `tags`, `community_id`.
3. **No second tool call unless** you see one of these failure signals:
   - `total_found == 0` → fall back to `find_by_tag` if the query looks like a single token, else `search_by_category` if you can map it to a canonical category.
   - First three hits all have `similarity < 0.55` → escalate to `search_by_community` (same query).
   - User explicitly named a source ("youtube", "linkedin") → use `search_youtube` or `search_linkedin` instead of `search_semantic` from the start.

## Output format

Numbered list. Each line is: `N. Title — URL — short why-relevant (one phrase, max 12 words)`.

The "why" comes from category, source, and tags — not invention. If a hit's title is bare/generic, lean on tags or source.

**Do not** add a leading "Here's what I found" or any preamble. Get to the list.

**Do not** invent URLs. Every URL you emit must appear in the hit you cite.

**Do not** truncate URLs. Full URL or nothing.

## When to bail out

If `search_semantic` returns 0 hits AND the fallback returns 0 hits, say so plainly:

> No matches in OpenMark for `<query>`. Try a broader term, or use openmark-deep-research for cross-source expansion.

Don't apologise. Don't recommend WebFetch — that's deep-research territory.

## Example

User: *"find my bookmarks on prompt caching"*

1. `search_semantic(query="prompt caching", n=12)` → 12 hits.
2. Render:

```
1. Prompt Caching with Claude 3.5 — https://docs.anthropic.com/.../prompt-caching — official docs, AI Tools
2. Reducing Cost with Prompt Caching — https://blog.anthropic.com/... — engineering blog post
3. How Vercel uses prompt caching — https://vercel.com/blog/... — production case study
...
```

That's it. Done in one tool call. Move on.
