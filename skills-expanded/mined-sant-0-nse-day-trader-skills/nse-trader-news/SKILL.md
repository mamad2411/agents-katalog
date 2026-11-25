---
name: nse-trader-news
description: News Monitor for Indian stocks. Tracks official NSE corporate announcements and public Indian news headlines for every ticker you watch, tags results, dividends, orders, regulation, ratings, fund-raises and management changes, and never repeats an item. Use when the user says "any news on RELIANCE", "why is this NSE stock moving", "pre-market India news", "check company announcements", "koi news hai?", or after nse-trader-scanner.
---

# nse-trader-news

Checks two sources for an NSE watchlist:

1. **NSE corporate announcements** — primary-source exchange filings and
   attached PDFs.
2. **Google News RSS** — public media headlines; open the original article
   before relying on it.

It tags and remembers each item so repeated checks do not spam you. No API key
is required and no order is placed.

## Run it

```bash
python scripts/news.py --tickers RELIANCE,TCS,HDFCBANK --hours 24
```

After the first run, request only items after the previous successful check:

```bash
python scripts/news.py --tickers RELIANCE,TCS --since
```

Example output:

```text
NEWS  RELIANCE, TCS  3 new item(s)
  11-01 10:12  RELIANCE     [results] Financial results for the quarter...
  11-01 09:45  TCS          [order-win] TCS wins multi-year contract...
```

## Tags

`results` · `board-meeting` · `dividend` · `order-win` · `regulatory` ·
`rating` · `fund-raise` · `management` · `other`

Tags are keyword routing aids, not sentiment. A positive-looking headline can
still be old, expected, immaterial or already priced in.

## Rules

- NSE filing timestamp is converted and shown in IST
- hashes `title + URL` and remembers up to 5,000 IDs
- newest first; duplicate IDs are omitted
- source failures are isolated: NSE can still work if RSS fails and
  vice versa; errors are written to JSON
- does not scrape paywalls or summarize text it did not fetch
- never calls media coverage an official filing

## Files

| File | What |
|---|---|
| `nse-trader/watchlist.json` | optional source of ticker ideas (pass them via `--tickers`) |
| `nse-trader/news.json` | current new items, tags and source errors |
| `nse-trader/news_seen.json` | IDs and last successful run time |

After checking catalysts, use `nse-trader-entry` for a selected setup. News by
itself is not an entry signal. Educational tooling only, not financial advice.
