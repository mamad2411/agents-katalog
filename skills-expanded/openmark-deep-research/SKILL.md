---
name: openmark-deep-research
description: Multi-angle deep-research workflow over Ahmad's OpenMark knowledge graph (13k+ bookmarks). Use whenever Ahmad asks anything that requires more than one search to answer well — "what's the landscape of X in my saves", "do a deep dive on Y", "research X across my bookmarks", "compare what I saved about X vs Y", "give me everything on X". Also use when fast-search returned thin results and Ahmad pushed back ("dig deeper", "more results", "actually research it"). Pairs Neo4j graph search with WebFetch on top picks to bring back fresh page content. Triggers on "deep research", "dig deeper", "research", "landscape", "everything on", "thorough", "comprehensive".
metadata:
  type: research
---

# OpenMark — Deep Research

Plan → fan out → expand → fetch → synthesize. Multi-tool, parallel where possible, citations only from observed URLs.

## The plan format (use TodoWrite first)

Before any tool call, write a TodoWrite list with these exact items, tailored to the query:

```
1. Multi-angle search: semantic + 2 of [category, tag, community, source] in parallel
2. Pick top 5–8 by similarity AND graph signal
3. Graph-expand 2–3 of them to surface SIMILAR_TO neighbors
4. WebFetch top 3 URLs to get fresh page content
5. Synthesize with citations (URL must appear in tool output to be cited)
```

Mark each todo `in_progress` when you start, `completed` when done. The user sees this and gets a sense of where you are.

## Step 1 — Multi-angle search (parallel)

Send these tool calls IN A SINGLE MESSAGE so they execute in parallel:

- `search_semantic(query=<user query>, n=15)` — always
- ONE of:
  - `search_by_category(category=<inferred>, query=<user query>, n=10)` if the query maps cleanly to one canonical category
  - `find_by_tag(tag=<core noun>, n=20)` if the query is a single concrete term
  - `search_by_community(query=<user query>, n=20)` if the user wants "everything about" a topic
- `find_by_source(source="linkedin", query=<user query>, n=8)` IF the query is about discourse/opinion/people — LinkedIn has the takes
- `search_youtube(query=<user query>, n=8)` IF query is about tutorials/talks/courses

Don't run all five. Pick 2–3 angles based on query shape. The point is variety, not volume.

## Step 2 — Rank + dedupe

Combine all hits into one list. Dedupe by URL. Sort by:

1. Hits appearing in ≥2 retrieval strategies → boost (cross-corroborated).
2. Then by `similarity` desc.
3. Then by `bm_score` desc.

Take the top 8 distinct URLs.

## Step 3 — Graph expansion (selective)

For the top 3 distinct URLs that have `community_id` set or that look like "anchor" pages (high similarity, broad title):

- `graph_expand(url=<that url>)` — gets SIMILAR_TO neighbors + community peers

Add any new URLs from these expansions to a "neighbor pool". Don't fetch them yet.

## Step 4 — WebFetch top picks (fresh content)

Pick the 3–5 most promising URLs (top of your ranked list). For each:

- `WebFetch(url=<url>, prompt="Extract: 1) the main claim or thesis, 2) the 2-3 most quotable lines, 3) any concrete numbers, names, or dates that ground it. Plain text, no headers.")`

Time-box: if a WebFetch fails (404, JS-only page, paywall), skip that URL and move on. Don't retry.

## Step 5 — Synthesize

Output sections:

### TL;DR
2–3 sentences. The headline finding across Ahmad's saves on this topic.

### What Ahmad has on this (ranked)
Numbered list, 5–8 items, in priority order. Each: `Title — URL — one-line why it matters here`.

### Fresh detail from top sources
For each WebFetch that returned content, a short paragraph: source title, what it actually says (key quote or stat). Cite URL inline.

### Threads to pull (optional)
2–3 follow-up directions Ahmad could chase — phrased as concrete search queries he could re-run, not as "consider exploring."

## Citation rule

Every URL you emit MUST have appeared in a tool result during this session. If you find yourself about to write a URL and you can't point to which tool call returned it, stop and don't write it.

## Speed budget

This skill should take 30–90 seconds of tool calls. If you've fired 12+ tool calls and still don't have enough to synthesize, stop, return what you have, and tell Ahmad which angle didn't pay off.
