---
name: market-pulse
description: Summarize what's moving in the market right now using the AlphAI MCP. Use when the user asks "what's moving?", "what's the big story today?", "anything breaking?", "market pulse", or wants a fast read on the current tape rather than one specific ticker.
---

# Market pulse

Answer "what's happening *right now*?" from AlphAI's feed. Three tools cover three
different questions — pick the right one:

- **`alphai_actionable_now`** — breaking, *decision-grade* news from the last few
  hours. The gate is strict: by default only `actionability='high'` (something to
  act on TODAY — guidance cut, halted trading, breaking M&A, surprise print).
- **`alphai_stories`** — the events of the last 48h that two or more publishers
  reported, each summarised from its articles (title, lead, importance, publisher
  count). The "big picture" with independent coverage behind it.
- **`alphai_trending`** — top single articles of the last 48h by relevance. Catches
  movers only one outlet has covered so far; not necessarily urgent.

## Steps

1. **Start narrow, with `alphai_actionable_now()`** (defaults: last 6h,
   high-actionability). This is the real "is anything breaking" signal.
2. **Read an empty result correctly.** Outside major market hours (nights,
   weekends — crypto trades 24/7, but high-actionability prints still cluster in
   US/European/Asian sessions) an empty list is *expected* — it means no
   high-actionability prints in the window, **not** that the tool failed. Before
   concluding "nothing happened", widen once: `alphai_actionable_now(hours=24, min_actionability='medium')`.
3. **Add the backdrop with `alphai_stories(list="top", limit=10)`.** Each card is
   an event with two or more publishers behind it and a summary written from them;
   `importance` is the feed's 1–10 scale (7 and up), `publishers` says how broad the
   coverage is. For depth on one event call `alphai_story(story_id)`: key facts
   with their sources, the per-ticker read, open questions. Then
   `alphai_trending(limit=10)` for single-outlet movers the stories list does not
   carry yet.
4. **Optional focus.** If the user named a sector or theme, search for it:
   `alphai_news_search(query="<theme words>", min_relevance=7, collapse_stories=true)`.
   The query matches titles, named entities and summaries; read
   `query_interpretation` to see how it was understood. To pin it to companies,
   resolve them with `alphai_tickers(q=...)` and pass `tickers=[...]` as well.
5. **Optional event focus.** If the user asks about one kind of corporate event
   across the market (buybacks, dividends, offerings, M&A, management changes,
   guidance), filter by type instead of searching:
   `alphai_news_search(event_type=["buyback", "dividend"], from_date="<YYYY-MM-DD>")`.
   The types for those questions are `buyback`, `dividend`, `offering` and
   `debt_financing`, `m_and_a`, `exec_change` and `guidance_update`. Several
   types are OR-matched, and an event listed in `event.also` counts.
   `event_type` combines with `tickers`, `category` and dates, but not with
   `query`. Leave `collapse_stories` off here, because with it on only the item
   that leads its story is matched. Only SEC 8-K filings, 6-K earnings releases
   and PR Newswire releases carry an `event`, so press coverage never matches.

## Output

- **Breaking now** — the high-actionability items, if any. Each: headline ·
  ticker(s) · one clause on the decision it forces. If none, say so in one line
  and note the window you checked.
- **Big picture** — 3–5 stories from `alphai_stories`, each a one-liner with its
  publisher count; add a trending single-outlet item only when it is not already
  one of them (compare `story_id`).
- **So what** — one or two sentences tying it together (risk-on/off, a sector in
  focus, an event everyone's positioning around).

## Guardrails

- Don't conflate "trending" with "actionable". A story can dominate the tape
  (trending) without being something to act on today (actionable). Label which
  layer each item came from if it matters.
- Report relevance / actionability honestly; don't upgrade a medium item to
  "breaking".
- In an event-focus answer, take amounts, dates and names from `event.facts`
  and `event.also`, not from titles. `event.verified` is false when a fact was
  left out because its quote was not found in the document, or while the facts
  are still being read. Say which detail is missing instead of guessing it.
- News, not advice — no trade calls.
