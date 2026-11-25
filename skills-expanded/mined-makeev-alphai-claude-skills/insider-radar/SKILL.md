---
name: insider-radar
description: Scan SEC Form 4 insider trades for a ticker, a watchlist or the whole market using the AlphAI MCP — open-market buys, cluster buying by several insiders, and discretionary sales told apart from pre-planned 10b5-1 ones. Use when the user asks about "insider buying", "insider selling", "Form 4 activity", "who's buying <ticker>", "are insiders buying", or wants an insider-activity sweep.
---

# Insider radar

Surface what company insiders do with their own stock: **SEC Form 4** trades by
officers, directors and 10% owners. AlphAI turns each filing into a
relevance-scored news row with a structured `insider` block (side, shares,
`total_value_usd`, `is_10b5_1`, role, `transaction_date`, `filed_at`, and on a
sale `decision` and `decision_reason`), so the numbers come from the filing,
not from a press rewrite.

## Steps

1. **Single ticker.** Call `alphai_insider_news(ticker="<SYM>")`. If the user
   wants only the largest trades, raise the floor with `min_relevance=6`: it
   keeps purchases from roughly $500k and sales from roughly $1M. A sale never
   scores above 6, so `min_relevance=7` or higher returns purchases only, and
   nothing at all together with `decision`.
2. **Discretionary trades only.** Every Form 4 sale carries a label,
   `insider.decision`, read from the whole filing and not only from the 10b5-1
   checkbox:
   - `discretionary`: no plan or paperwork in the filing explains the sale. The
     insider chose to sell.
   - `plan_like`: the sale follows from a 10b5-1 plan or from paperwork, such as
     shares sold to pay the tax on vesting or to cover an option exercise.
     Treat it as routine.
   - `unknown`: the filing does not say enough to tell.

   When the user asks "is anyone *choosing* to sell", pass
   `decision="discretionary"`. Do not use `is_10b5_1=false` for that question:
   a sale outside a plan can still be a tax sale or an exercise cover. The
   three values do not overlap: together with the events that hold no sale they
   add up to the unfiltered feed. `decision` combines with `ticker`,
   `is_10b5_1`, the dates and `sort="ingested"`. Only sales (`transaction_code`
   `S`) are labelled. Purchases, a sale to the issuer (`D`) and other codes
   carry `decision: null` and match none of the three values, so for "is anyone
   *choosing* to buy" keep `is_10b5_1=false`, which drops planned trades, and
   read the purchases (`side` is `buy`).
3. **Cluster buying.** For "are insiders buying" across a name or the market,
   call `alphai_insider_clusters()` (or `symbol="<SYM>"`): issuers where several
   different insiders bought on the open market in one run. IPO/PIPE allocations,
   ESPP and plan lots are already filtered out of the default `open_market` view.
   Free accounts reach 30 days back, Basic and Pro 90.
4. **Watchlist.** Call `alphai_insider_news(ticker=...)` once per name. If the
   user gave none, call `alphai_insider_news()` unfiltered for the broad tape.
5. **Time-box on request.** For "this week" / "since earnings", pass
   `from_date` (ISO, UTC). Paginate with `cursor` only if they ask for more.

## Reading `decision_reason`

`insider.decision_reason` names what decided the label. Say it in plain words.

- With `plan_like`: `plan_10b5_1` (the 10b5-1 checkbox, or a footnote that
  places the sale under a pre-arranged plan, so it can come with
  `is_10b5_1: false`), `tax_withholding` (shares sold to pay the tax on
  vesting), `exercise_cover` (the sale covers the cost of an option exercise
  and its tax), `stated_non_discretionary` (a footnote says the sale was
  automatic or outside the insider's discretion).
- With `discretionary`: `open_market` (no plan or paperwork explains the sale),
  `exercise_and_sell` (options exercised and the shares sold, beyond what
  covering the exercise needs), `sold_all_vested` (the shares sold plus those
  withheld for tax cover everything that vested).
- With `unknown`: `partial_vest_sale` (part of the newly vested shares sold,
  more than the tax alone would need or on top of tax already withheld),
  `cover_ambiguous` (the sale could be an exercise cover at a high tax rate or
  a choice), `mixed_acquisitions` (the filing both vests shares and exercises
  options, so the sale cannot be tied to either), `price_disputed` (the filed
  price failed a price check, so the arithmetic is not trusted), `no_lines`
  (AlphAI does not hold the rest of the filing).

## Output

- **Notable buys** — open-market purchases first: ticker · who/role · size ·
  relevance. These are what most users actually want.
- **Cluster buying** — if `alphai_insider_clusters` found any: ticker · number of
  independent buyers · total · the window.
- **Notable sells** — the seller's role and the label of each sale: chosen
  (`discretionary`), routine (`plan_like`, with its reason: a 10b5-1 plan, tax
  on vesting, an exercise cover) or not readable from the filing (`unknown`).
  Put the discretionary ones first.
- **Read** — one line: leaning accumulation, distribution, or just routine?

## Guardrails

- An insider sale is not automatically bearish (taxes, diversification, scheduled
  plans). `discretionary` says the insider chose to sell, not why. Say what the
  filing shows; don't over-read it.
- Call a sale chosen only when `decision` is `discretionary`. `plan_like` is
  routine, tax sales and exercise covers included, and does not count toward
  distribution. When the label is `unknown`, say plainly that the filing does
  not show whether the insider chose to sell, and do not sort the sale into
  either group.
- One filing can span several tranches sharing a row — report the *event*, not a
  count of line items. An event with several sales has one label:
  `discretionary` if any sale is, else `unknown` if any is, else `plan_like`.
  The reason comes from the largest sale that set the label.
- `decision_reason` can be `null` next to a label. Report the label and give no
  reason.
- If the tool rejects the `decision` argument, or every sale comes back with
  `decision: null`, the label is unavailable. Say so, fall back to `is_10b5_1`,
  and describe a sale outside a plan as "not under a 10b5-1 plan", never as
  chosen.
- `filed_at` can be days after `transaction_date`; say which date you mean.
- AlphAI does not carry fund-holdings filings (13F, 13G, 13D). If the user asks
  what a fund owns, say so plainly; press coverage of a stake may still turn up
  via `alphai_news_search(query="<fund> stake <company>")`.
- Lead with `relevance_score`; "no notable insider activity in the window" is a
  valid, useful answer.
- News, not advice.
