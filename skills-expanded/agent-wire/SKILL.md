---
name: agent-wire
description: Automatically use this skill whenever the user asks for live web information, wants to know what people said about a topic recently (last 30 days, trends, X vs Y), shares any URL, asks about social media posts/comments (Reddit, X/Twitter, HackerNews, LinkedIn, YouTube, Bilibili, Xiaohongshu), inspects GitHub repositories/issues, checks market/stock prices, or asks about their own social account activity (e.g., "check my Twitter likes", "my GitHub notifications"). Never ask the user to run a slash command.
---

# Agent-Wire Execution Protocol

You have direct live internet and platform access through the `agent_wire` MCP server (`wire_read`, `wire_search`, `wire_feed`, `wire_me`, `wire_research`, `wire_cite`, `wire_run`, `wire_status`).

## Routing Rules (Zero-Turn Overhead)

1. **Never probe health first:** Do NOT call `wire_status` before reading or searching unless the user explicitly asks to diagnose connections. Call `wire_read`, `wire_search`, `wire_feed`, or `wire_me` immediately on Turn 1.

2. **Reading 1-2 URLs:** Call `wire_read(urls=[...], query="<what you need>")` directly. Pass `query` so `agent-wire`'s BM25 engine slices the most relevant sections and comments.

3. **Reading 3+ URLs or Deep Multi-Source Research (Tiered Sub-Agent Fan-Out):**

   - If your environment supports sub-agents (`Task` / `wire-worker`), do NOT dump 5+ raw URLs into your main context. Spawn parallel `wire-worker` sub-agents (fast model tier: Haiku / Luna / Soul) to call `wire_read` and return a 150-word factual synthesis each.

   - If sub-agents are unavailable, pass all URLs in a single batched list: `wire_read(urls=["url1", "url2", "url3"], max_tokens=3000)`.

4. **Searching:** Call `wire_search(query="...", platforms=[...])`. Note that `wire_search` automatically expands the full text of the top 2 results, so you rarely need a follow-up `wire_read` call.

5. **Several calls, or only part of the results (Code Mode):** When a task needs 2+ wire calls (search then read the hits, read 5 threads, compare feeds) or you only need specific fields (titles, scores, the top 3 comments, links that mention X), call `wire_run(code="...")` once instead of chaining tools. The code is the body of an async JavaScript function: call `wire.read`, `wire.search`, `wire.feed`, `wire.research` and `wire.cite` (they return plain objects), run independent calls together with `Promise.all`, and `return` only what you need. Intermediate pages never enter your context. Example:

   ```js
   const hits = await wire.search('bun 1.3 release', {platforms: ['hn', 'reddit'], limit: 5});
   const docs = await wire.read(hits.slice(0, 4).map(h => h.url), {query: 'performance'});
   return docs.filter(d => !d.error).map(d => ({url: d.url, title: d.title, top: d.comments.slice(0, 3).map(c => c.text.slice(0, 200))}));
   ```

   Use `wire-worker` sub-agents instead when the pages need a model to read and summarize them rather than fields picked out by code. If `wire_run` is the only wire tool you have besides `wire_status` (the server runs with `--code-mode`), use it for everything, including single reads. A failed call rejects its promise; wrap it in `try/catch` to keep going. Scripts cannot reach the user's own account (`wire_me`).

6. **"What's new / what do people think / last N days / X vs Y / what's trending":** Call `wire_research(topic="...", days=30)` once instead of many searches. It searches Reddit, Hacker News, YouTube, GitHub, news, Bluesky, Mastodon, Polymarket and the web in parallel, merges duplicates, and returns a cited brief with top comments. Use `topic="A vs B"` to compare, an empty topic for what's trending, `github_user=` for a person's GitHub activity, `depth="quick"` when speed matters. Cite the links it returns; don't present its quoted comments as facts.

7. **User's Own Account ("my latest post", "my likes", "my notifications"):** Immediately call `wire_me(platform="...", target="...")` which uses the session the user saved with `wire auth login <site>`. If it reports no saved session, tell the user to run that command; never ask for passwords or cookies.

8. **Citations (no made-up sources):**

   - Cite only links you read or that a wire tool returned. Never invent a URL, outlet, author or quote.
   - If you have no source for a claim, write `[[UNSOURCED]]` right after it. It is a reserved marker: `wire_cite` lists those claims so you either find a source (`wire_search`) or tell the user plainly that the claim is unverified.
   - Before sending any answer that cites sources, call `wire_cite(text="<your answer>")`. It opens every link and reports `OK`, `DEAD`, `ARCHIVED` (use the Wayback copy it gives and say the original is gone), `SOFT_404`, `BLOCKED` (exists but unverified, keep it and say so), `QUOTE_MISSING` (the quoted words are not on the page), and links agent-wire never returned this session (read them before citing).
   - For a dead link, run the `wire_search` it suggests, or ask the user or a sub-agent for an alternative. Do not silently drop or keep a dead citation.
   - `wire_research` briefs already check their web and news links and mark failures with ⚠.
   - Links a `wire_run` script read count as returned by agent-wire; inside a script, `wire.cite(text)` returns the same verdicts as data.
