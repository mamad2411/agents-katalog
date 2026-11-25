---
name: stock-brief
description: Produce a situational brief on a single stock/ticker — its recent high-relevance news, earnings reads, insider activity, and what to watch next — using the AlphAI MCP. Use when the user asks to "brief me on <ticker>", "what's going on with <company>", "catch me up on NVDA", or wants a quick read on one name.
---

# Stock brief

Give a tight, decision-useful read on **one ticker** from AlphAI's enriched
feed. Not a price quote — a *news* brief: what's been happening, what the last
earnings filing actually said, who's buying or selling, and what to keep an eye
on.

## Steps

1. **Resolve the ticker.** If the user gave a company name, not a symbol, call
   `alphai_tickers(q=...)` to find it. If `alphai_ticker_news` returns
   `unknown_ticker=true`, tell the user and stop — don't invent coverage.
2. **Pull the ticker feed.** Call `alphai_ticker_news(ticker, collapse_stories=true)`.
   `collapse_stories` folds syndicated reprints into one row each and adds a
   `sources_count` corroboration signal — prefer it for a clean brief. Insider
   news is included by default; keep it.
3. **Earnings read.** Call `alphai_earnings(ticker)` for AlphAI's own
   filing-verified reads (8-K item 2.02 / 6-K earnings release, every figure
   checked against the filing). The feed tools return articles *about* a
   quarter; this returns the filing's numbers. An empty `reports` list is a
   normal answer, not an error. If non-empty, lead from the newest read —
   `fiscal_period`, `verdict` (strong/solid/mixed/weak), a headline
   `analysis.key_metrics`, guidance; `next_report_date` is company-confirmed
   (never an estimate) and `null` means none held.
4. **Corporate events.** Rows that come from an SEC 8-K, a 6-K earnings release
   or a PR Newswire release carry an `event` block: a `type`, the company's
   `role`, and `facts` quoted from the document. Take amounts, dates and names
   from `event.facts`, not from the title, and read `event.also` too: a
   dividend, a buyback or new guidance announced inside an earnings release is
   listed there with its own facts. If the user asks about one kind of event
   (buybacks, dividends, offerings, M&A, management changes, guidance), filter
   for it: `alphai_ticker_news(ticker, event_type=["buyback"])`. The types for
   those questions are `buyback`, `dividend`, `offering` and `debt_financing`,
   `m_and_a`, `exec_change` and `guidance_update`. Several types are OR-matched,
   and an event listed in `event.also` counts. Leave `collapse_stories` off on
   that call, because with it on only the row that leads its story is matched.
   Press coverage and Form 4 rows have no `event` and never match.
5. **Optional context.** If the user wants the wider tape, call
   `alphai_trending(limit=5)` and note any market-level story that touches this
   name or its sector.
6. **Deep-dive on demand.** If one story clearly drives the brief and the user
   wants detail, fetch it with `alphai_article(uid)` for the full enrichment
   (ticker analysis, key entities). The article *body* is not served — work from
   the enrichment and summary.

## Output

Keep it to a screen. Structure:

- **One-line read** — the single most important thing about this name right now.
- **Top stories** — 3–5 bullets, each: headline · relevance score · one-clause
  "why it matters". Lead with the highest `relevance_score`. For a row with an
  `event` block, state the amount, date or counterparty from `event.facts`.
- **Earnings** — the newest `alphai_earnings` read if there is one: period ·
  verdict · 1–2 metrics · guidance line. Otherwise one line ("no published
  AlphAI earnings read yet").
- **Insider activity** — any SEC Form 4 rows from the feed: who, buy or sell,
  size, and whether a sale ran under a 10b5-1 plan (`insider.is_10b5_1`). A
  sale outside a plan is not yet a choice: `alphai_insider_news(ticker)` labels
  each sale in `insider.decision` as `discretionary` (the insider chose to
  sell), `plan_like` (a 10b5-1 plan, a tax sale on vesting, an exercise cover)
  or `unknown`, so call a sale chosen only when the label says so. "No
  notable insider activity in the window" is a valid line.
- **Watch next** — 1–2 concrete things that would change the picture, incl. the
  `next_report_date` when set.

## Guardrails

- Every story carries a 1–10 `relevance_score`; lead with the high ones and say
  the score so the user can calibrate.
- This is news, not advice. Don't issue buy/sell calls or price targets —
  summarize what the reporting says and let the user decide.
- Event facts are quotes: for an amount, a date or a name, `value` is the
  document's own wording, and `number`, `unit` and `scale` are parsed from it.
  `event.verified` is false when a fact was left out because its quote was not
  found in the document, or while the facts are still being read. The facts
  that are present passed the check. Say which detail is missing instead of
  filling it in from the headline.
- If the feed is thin, say so plainly rather than padding. A short honest brief
  beats a long speculative one.
