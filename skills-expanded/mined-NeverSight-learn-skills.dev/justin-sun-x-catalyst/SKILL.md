---
name: justin-sun-x-catalyst
description: >
  Decision-support lens for distilling Justin Sun's public X posts
  (@justinsuntron) into short-horizon crypto, crypto-equity, and related US-stock
  catalysts. This skill should be used when the user mentions Justin Sun, Sun
  Yuchen, @justinsuntron, TRON/TRX, JST, SUN, BTT, HTX, Poloniex, WBTC, WLFI,
  TRUMP memecoin links, Tron Inc. / NASDAQ:TRON, SunPump, or asks what a Justin
  Sun X post means for a ticker/token. Live-fetch or inspect the latest posts
  first. Decision-support only; never auto-trades and never places, amends, or
  cancels orders.
---

# Justin Sun X Catalyst

## Overview

Use this lens to turn **Justin Sun's public X posts** into a calibrated list of
tokens, crypto equities, and related US stocks that may react. Treat the output
as short-horizon market context, not a thesis, recommendation, or live order.

## Step 0 - Refresh First

Always refresh before analysis. X posts and crypto prices move quickly, and the
local archive is only useful after it has been updated.

1. Pull the latest `yan-labs/justin-sun-x-catalyst` repo or run
   `python3 update.py` from the repo root when maintaining the archive.
2. Inspect the latest posts from `https://x.com/justinsuntron` or the refreshed
   `data/justinsuntron_posts.json` archive.
3. Prefer `xreach`, an authenticated browser, or an installed X-to-markdown
   workflow when X blocks unauthenticated access.
4. If browser access fails, try public search for `from:justinsuntron` plus the
   topic/ticker, then verify any quoted post against the X permalink.
5. If fresh posts cannot be verified, say so plainly and analyze only the pasted
   post, screenshot, or user-provided link.
6. Never call a post "latest" unless the timestamp and permalink were observed
   in the current run.

## Core Workflow

1. Load `references/methodology.md` for the tier system and per-post checklist.
2. Load `references/ecosystem-map.md` to map the post topic into likely affected
   tokens, crypto equities, and US-listed names.
3. Load `references/track-record.md` to weight the signal by observed base rate.
4. Output each signal with timestamp, permalink, implicated asset(s), direction,
   reliability tier, expected duration, invalidation trigger, and data caveats.
5. Keep broker/account language separate: public X and public market data are
   market context only, never uSMART account truth or fill confirmation.

## Navigation

| File | Use it for |
|---|---|
| `references/methodology.md` | Classify each post into catalyst tiers, amplifiers, anti-patterns, and output fields |
| `references/ecosystem-map.md` | Translate topics into reaction baskets: TRON ecosystem, WLFI/TRUMP, WBTC, exchanges, crypto equities, Nasdaq TRON |
| `references/track-record.md` | Seed priors, live ledger template, and hit-rate calibration rules |
| `references/maintenance.md` | Scheduled refresh, dedupe, scoring, source hygiene, and commit convention |
| `../data/justinsuntron_posts.json` | Refreshed public X archive when using the full repo checkout |

## Risk Framing

- State that the analysis is decision support only and not financial advice.
- Flag Justin-linked assets as high manipulation/headline-risk instruments.
- Separate "post can move price" from "asset is good to hold."
- Prefer limit-order planning language if the user later discusses manual trades.
- Never place, amend, cancel, or size trades from this skill.
