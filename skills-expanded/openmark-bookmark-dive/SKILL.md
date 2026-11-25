---
name: openmark-bookmark-dive
description: Take ONE specific bookmark URL and explore the neighborhood around it — tags, SIMILAR_TO neighbors, community peers — plus optionally WebFetch the page itself to summarize it. Use whenever Ahmad pastes a single URL and asks "what's near this", "tell me about this one", "expand this bookmark", "dig into this", "what else did I save like this", "give me the context for this URL". Triggers on "expand", "neighbors of", "what else like this", "dig into this URL", "context for this", and any message that's just a URL plus a short prompt.
metadata:
  type: research
---

# OpenMark — Bookmark Deep Dive

Anchor on ONE URL. Surface its graph neighborhood. Optionally summarize the page itself. Output a compact briefing.

## When to use

User pastes a URL plus a short ask:

- "what else did I save like [https://example.com/agents]"
- "dig into [URL]"
- "expand this bookmark: [URL]"
- "give me the neighbors of [URL]"
- "what's around this in OpenMark"

If the user gives no URL, fall back to openmark-fast-search. If the user gives a URL AND a broad topic, use openmark-deep-research.

## Tool sequence

1. **Confirm the bookmark exists**:
   - `get_bookmark_full(url=<URL>)`
   - If `note == "Bookmark not found."`, say so and stop. Don't pretend.

2. **Graph expand** (this is the core call):
   - `graph_expand(url=<URL>)` — returns text describing tags, SIMILAR_TO list, community peers.

3. **WebFetch the URL itself** (parallel to step 2 if possible):
   - `WebFetch(url=<URL>, prompt="Summarize in 3-4 sentences. Then list 2-3 specific claims or numbers that are central to the page.")`
   - If fetch fails (paywall, JS-only, 404), skip and note "Could not fetch live page."

4. **Optional broaden — only if user explicitly asks "what else"**:
   - For top 2 tags from get_bookmark_full's `tags[]`, run `find_by_tag(tag=<tag>, n=10)`.
   - For the `community_id` if present, run `search_by_community(query=<title or first tag>, n=15)`.

## Output format

```
# {Title}
{URL}

**OpenMark metadata**
- Source: {source}  ·  Category: {category}  ·  Score: {score}
- Tags: {tag1, tag2, tag3, ...}
- Created: {created_at if available, else "—"}

**What the page says** (from WebFetch)
{3-4 sentence summary + 2-3 specific claims}

**Similar bookmarks** (from SIMILAR_TO)
1. {title} — {url}
2. {title} — {url}
3. {title} — {url}
...

**Community peers** (from IN_COMMUNITY)
1. {title}
2. {title}
...

**Broader neighborhood** (only if requested)
{Top 10 from tag/community expansion}
```

## Rules

- **The anchor URL appears at the top, exactly once, exactly as provided.** No normalisation in the output (even if normalised internally for lookup).
- **Similar/peer URLs come from tool output, never invented.** If the SIMILAR_TO list is empty, write "No SIMILAR_TO neighbors yet (run graph_hygiene if you just injected new items)."
- **WebFetch summary is the ONLY place free prose appears.** Everything else is structured.
- **Don't editorialize on the page content.** Just relay what WebFetch returned. Ahmad will form his own take.
- **If `community_id` is None on the node**, say so — "Not yet in a Louvain community (GDS plugin not installed / not re-run)."
