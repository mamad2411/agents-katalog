---
name: strategic-partner-firehose
description: Real-time SEC 8-K + SC 13D strategic-partner monitor. Detects PIPE deals, joint ventures, and strategic investments from Tier-1 corporate names (NVIDIA, Microsoft, SK Telecom, Samsung, TSMC, Oracle) and sovereign wealth funds (MGX, Saudi PIF, Mubadala, Temasek) BEFORE Substack/Twitter covers them. Filters: US-listed only, market cap ≥ $50M, deal size ≥ $50M. Auto-scores 0-10 ("Strategic Partner Score") via the same enrichment pipeline as insider-firehose. Triggers in English ("strategic investor", "8-K partnership", "find next PENG", "PIPE deal", "13D filing") or Chinese ("战略投资人", "8-K 合作公告", "找下一个 PENG", "PIPE 增发", "13D 申报").
---

# Strategic Partner Firehose — Real-Time 8-K + SC 13D Monitor

Pulls the SEC EDGAR atom feeds for 8-K and SC 13D, detects high-signal strategic-partner filings (PIPE deals, JVs, master supply agreements with Tier-1 names) and pushes enriched Telegram alerts.

**Companion to `insider-firehose`** — they share the same Telegram bot, the same `enrichment/` pipeline, and the same SEC EDGAR data source. The difference is what they watch for:

| Skill | What it monitors | Best signal type |
|---|---|---|
| `insider-firehose` | Form 4 (officer/director open-market buys) | Founder/CEO buying at $200k+ |
| `strategic-partner-firehose` | **8-K Item 1.01 / 3.02 + SC 13D** | **NVIDIA/MSFT/SKT $50M+ strategic investment** |

## Why this exists

Substack/Twitter shillers (`@KadunaBull`, `@crux_capital_`, etc.) typically discover these stories **6-18 months after the SEC 8-K filing**. Real example: SK Telecom's $200M strategic investment in SMART Global Holdings (now PENG) was disclosed on 8-K dated **2024-07-15**. Twitter chatter peaked **2026-05-12 — 22 months later**.

If you read the 8-K the day it filed, you bought at ~$20. The Twitter pump fired at $44 (+120%).

This skill watches the same SEC firehose **so you don't need to follow Twitter to find these stories**.

## How you interact with this skill — important

**This skill is cron-driven, not natural-language-driven.**

```
You don't ask it anything.    ←  unlike analyze-stock or earnings-prep
You enable it once.           ←  one click in GitHub Actions
Then it runs forever.         ←  every 30 min weekdays
You receive Telegram alerts.  ←  whenever the SEC has news
```

The NL triggers in this skill's frontmatter (`"find next PENG"`, `"8-K partnership"`, etc.) are for **conversational lookup** — they let you ask Claude things like:

| You ask Claude (NL) | Skill does |
|---|---|
| "show me last 7 days of strategic-partner alerts" | reads `scripts/recent_alerts.json` |
| "find next PENG" | summarizes recent high-score alerts |
| "what is 8-K Item 3.02" | reads `README.md` to explain |
| "is filing X a partnership signal" | runs `classifier.compute_theme_score` on the text |
| "explain Partner Score 7/10 for TICKR" | runs `analysis.compute_partner_score` |

**The real-time monitoring** is the GitHub Actions cron (`.github/workflows/strategic-partner-firehose.yml`), not Claude Code on your laptop.

## Architecture

```
SEC EDGAR atom feeds (8-K + SC 13D, every 60 min cron, weekdays 9 AM - 7 PM ET)
   │
   ▼
partner_firehose.py
   │
   ├── parse_atom_feed (XML parsing)
   ├── fetch_filing_text (combine 8-K cover + exhibits)
   ├── is_noise_filing (skip routine 5.02 officer changes)
   ├── find_strategic_investors (regex match TIER_1/TIER_2/SOVEREIGN/SMART_VC)
   ├── extract Items, amount ($M), conversion price, ticker, deal type
   │
   ├── FILTERS (fast-fail order):
   │    ✓ Amount ≥ $50M
   │    ✓ Valid ticker
   │    ✓ US-listed (NYSE/NASDAQ/AMEX)
   │    ✓ Market cap ≥ $50M
   │
   ├── enrichment/ (reused from insider-firehose):
   │    business one-liner + valuation + 52W price + Smart Money Score
   │
   ├── analysis.compute_partner_score → 0-10 verdict
   ▼
Telegram bot ($TELEGRAM_BOT_TOKEN, shared with all firehoses)
   │
   ▼
🤝🟢 STRATEGIC PARTNER INVESTMENT — $X.XB
$TICKER (Company)
🐉 Tier-1 Investor (tier_1)
...
```

## Files

- `scripts/partner_firehose.py` — main entry: fetch + parse + filter + enrich + send
- `scripts/investor_registry.py` — curated Tier-1/Tier-2/Sovereign/SmartVC names (35+ entities, multi-alias)
- `scripts/parsers.py` — 8-K + 13D regex extractors (Items, $, conversion price, ticker, deal type)
- `scripts/filters.py` — mcap + US-listed + amount filters with in-memory caching
- `scripts/analysis.py` — Partner Score 0-10 (companion to insider score)
- `scripts/tests/test_all.py` — 32 unit tests covering parser + filter + analysis + end-to-end
- `scripts/tests/fixtures/` — real-shape 8-K bodies (PENG/SGH SK Telecom, NVIDIA, sovereign cluster, noise)
- `scripts/strategic_state.json` — accession-number dedup ledger
- `strategic_config.json` — on/off toggle
- `.github/workflows/strategic-partner-firehose.yml` — cron + state commit

## Tuning knobs

| Env var | Default | Meaning |
|---|---|---|
| `STRATEGIC_MIN_MCAP` | `50000000` | Skip companies below $50M market cap |
| `STRATEGIC_MIN_AMOUNT_M` | `50` | Skip deals below $50M |
| `TEST_MODE` | `0` | `1` prints to log, doesn't send Telegram |
| `DRY_RUN_LIMIT` | `0` | Cap filings processed (0 = no cap) |
| `ENRICH` | (uses config) | `0` disables Tier-2 enrichment |

## What this skill does NOT do

- **Backtest historical alpha** — we have a fixture-based unit test framework, but no full 10-year EDGAR replay. Possible v2.3.
- **Real-time WebSocket** — SEC EDGAR doesn't offer streaming; we poll atom feeds hourly.
- **Foreign filings** — companies that file only with HKEX, LSE, JPX are not in scope (US-listed only).
- **Routine 8-Ks** — Items 5.02 (officer changes), 2.02 (earnings releases), 5.07 (shareholder votes) intentionally filtered. Use other tools.
- **Crypto IPOs / SPACs** — these often have weird filing patterns; not in initial scope.

## Real backtest signals (would have triggered)

| 8-K Date | Ticker | Strategic Investor | Type | Then-Price | 1Y Later |
|---|---|---|---|---|---|
| 2024-07-15 | SGH → PENG | SK Telecom $200M | PIPE Preferred | $20 | **$44 (+120%)** ✅ |
| 2025-01-21 | ORCL | OpenAI Stargate JV | JV Agreement | $158 | $193 (+22%) ✅ |
| 2025-09-05 | CRWV | OpenAI $11.9B contract | Master Supply | $115 | (tracking) ✅ |
| 2024-11 | RXRX | NVIDIA $50M | Item 3.02 | $5.50 | (tracking) ✅ |

## Companion skills

- `insider-firehose` — Form 4 buys (this skill's sibling, uses same enrichment)
- `review-investment-screenshot` — when an alert fires, run for fundamental cross-check
- `analyze-stock` — when alert + you don't recognize the ticker, this pulls company context
- `macro-warning` — gate any conviction buy by current regime
- `option-wall-analysis` — check the option flow positioning before sizing in
