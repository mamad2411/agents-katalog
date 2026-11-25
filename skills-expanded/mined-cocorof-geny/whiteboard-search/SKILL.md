---
name: whiteboard-search
description: When the user asks you to find something in their own notes or in a shared library, search by following the correct ladder from opsidian_search to knowledge_search and summarize the results naturally.
allowed_tools:
  - opsidian_search
  - opsidian_browse
  - opsidian_read
  - knowledge_search
  - knowledge_list
  - knowledge_read
execution_mode: inline
examples:
  - "Do I have anything written in Obsidian about X?"
  - "Find that note we organized together last time."
  - "Show me what's in the library."
---

# Whiteboard Search — Searching the user's notes / library

Use this skill when the user asks you to find something in their own notes or in a shared library.

## First, distinguish the two kinds of stores

- **User Opsidian** (personal vault) — the raw notes the user writes and captures every day. Accessed via the `opsidian_*` tools. Categories: `inbox / daily / topics / projects / insights`.
- **Curated Knowledge** (library) — the organized subset the user has explicitly shared via "Share with VTuber > Library". Accessed via the `knowledge_*` tools. **This is the most trustworthy source you have — because the user hand-picked and sent it.**

## Search Ladder

If the user's request is ambiguous, try **both** and merge the results:

1. **`opsidian_search(query, max_results=5)`** — keyword search. The fastest, and best at capturing the user's raw intent.
2. If you get 0–1 results or the scores are low → use **`knowledge_search(query, max_results=5)`** for a semantic search on the curated side.
3. For the 1–3 most likely notes, confirm the contents with **`knowledge_read(filename)`** or **`opsidian_read(filename)`**.
4. Don't dump the body as-is — **summarize it in 2–3 sentences** for the user. Include only 1–2 lines of key quotes if needed.

## When the user specifies a category or tag

- Category specified ("among my daily notes…") → narrow with `opsidian_browse(category="daily")`, then search within it.
- Tag specified ("the ones tagged #API…") → `opsidian_browse(tag="API")`.
- Take the results from both tools, rank by score or recency, then read only the top ones.

## Using the ViewLedger `⚑` marker

- Notes in the system prompt's `[Spotlight Context]` block, or notes in tool results with `_view.counts.read > 0`, are **material you've already seen**.
- Don't treat them as if you're seeing them for the first time; connect to the prior context with phrasing like "that note from last time…" / "from the X we looked at before…".
- A high `_view.counts.injected` means a key note that has appeared often via spotlight too — a signal that the user considers it important.

## Protecting a large vault

If `opsidian_search` returns a response with `"warning": "Vault has N notes; opsidian_search caps out at 500 …"`:

- Politely ask the user "There are a lot of notes, so I can't go through them all at once — can you give me a category or a tag?"
- Once you get a response, narrow it down with `opsidian_browse(category=..., tag=...)` and retry.

## Result-formatting rules

- Don't expose the raw filename (`topics/foo.md`) as-is; use the note's **title**.
- Don't paste JSON / frontmatter / raw wikilinks straight into chat.
- If there are 0 results: "I couldn't find any related notes. If you give me a more specific keyword or category (daily/topics/projects/insights/inbox), I'll search again."
- If there are a great many results, summarize only the top 3 and close with "Want me to show you more?".

## Don'ts

- Don't call tools more than 5 times in a single turn — narrow sufficiently before each call.
- Don't paste raw body markdown straight into chat (especially frontmatter, wikilinks).
- Don't show the user search results as JSON / tables — use a natural-language summary.
- Don't mistake the contents of the `[Spotlight Context]` block for something the user said — this is just state the system is telling you about, not something the user just uttered.
