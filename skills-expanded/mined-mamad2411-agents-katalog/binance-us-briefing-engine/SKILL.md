---
name: binance-us-briefing-engine
description: Personalized Binance.US market, portfolio, and watchlist briefings using account balances, recent trading history, watchlists, market data, recent news headlines, market context, and catalyst watch tied to the user's relevant assets. Use when the user asks for a market summary, personalized crypto brief, portfolio update, capital readiness check, watchlist recap, opportunity alert, or weekly reset for Binance.US.
metadata:
  version: 0.3.0
  author: Binance.US
  openclaw:
    skillKey: binance-us-briefing-engine
    requires:
      bins:
        - python3
    homepage: https://skills.sh
license: MIT
---

# Deprecated: Binance.US Briefing Engine

This repository is deprecated.

Use the new skill-family repository instead:

- `cmeiliu/binance-us-skills`

Preferred install flow:

```bash
npx skills add cmeiliu/binance-us-skills --list --full-depth
```

To install the updated briefing skill:

```bash
npx skills add cmeiliu/binance-us-skills --skill binance-us-briefing-engine --full-depth
```

The content below is preserved only so existing installs keep functioning while users migrate.

# Binance.US Briefing Engine

Generate account-aware Binance.US briefings. This skill is only valuable when it ties the market back to the user's own account.

## When Not To Use

- explicit funding workflows
- spot-trade execution reviews
- account-status troubleshooting
- deep single-asset diligence after the user already picked a coin

The bundled script should prefer:

- price-anchored output over percent-only output
- 24h plus 7-day framing over single-window commentary
- market context before portfolio-specific conclusions
- upcoming catalysts, not just backward-looking news
- ranked, de-duplicated news tied to held or watched assets
- a concrete next step over generic portfolio CTA text
- a conversational advisor tone over compliance-report wording
- explicit watchlist gaps and idle-cash framing when those would prompt action

## Use This Skill For

- "Give me a personalized market summary"
- "What matters for my Binance.US account today?"
- "Summarize my watchlist"
- "Give me a portfolio brief"
- "Do I have idle cash or concentration risk?"
- "What changed since my recent trades?"
- "Give me a capital readiness check"
- "Give me a weekly reset"

## Core Rule

Prefer account-aware output over generic market commentary.

When credentials are available, use:

- current balances
- recent trading history
- watchlist or configured priority assets
- deposit history when useful
- recent headlines for owned, watched, or recently traded assets

If credentials are unavailable, the script can still produce a limited market-only brief, but it should say so clearly.

## How To Run

Run the bundled script:

```bash
python3 scripts/binance_us_brief.py --mode daily_brief --format both
```

Common variants:

```bash
python3 scripts/binance_us_brief.py --mode portfolio_brief --format text
python3 scripts/binance_us_brief.py --mode watchlist_brief --watchlist BTC,ETH,SOL
python3 scripts/binance_us_brief.py --mode opportunity_alert --alert-threshold-pct 5
python3 scripts/binance_us_brief.py --mode capital_readiness --format text
python3 scripts/binance_us_brief.py --mode asset_research --asset BTC --format text
python3 scripts/binance_us_brief.py init-config
```

## Install Behavior

- For local development, prefer the default install behavior without `--copy` so OpenClaw uses a symlink and picks up local repo changes immediately.
- For GitHub or copied installs, use `npx skills update` to pull the latest published version.
- The rendered brief includes a version/update nudge for copied installs so stale snapshots are easier to spot.

## Credentials

The script will look for Binance.US credentials in this order:

1. Environment variables:
   - `BINANCE_US_API_KEY`
   - `BINANCE_US_SECRET_KEY`
2. `~/.openclaw/secrets.env`
3. `~/.env`
4. `.env` in the current workspace

The script reads only specific keys and does not print raw secrets.

## Optional Config

The script supports a small JSON config at:

`~/.openclaw/binance-us-briefing-engine.json`

Create it with:

```bash
python3 scripts/binance_us_brief.py init-config
```

Useful fields:

- `watchlist`
- `quote_assets`
- `quiet_hours`
- `recent_days`
- `portfolio_currency`
- `alert_threshold_pct`

## Recommended Workflow

1. Run `daily_brief` for a broad summary tied to balances and recent trades.
2. Run `portfolio_brief` when the user wants account impact, concentration, or idle cash context.
3. Run `watchlist_brief` when the user asks about tracked assets.
4. Use recent news headlines to explain why those assets matter today.
5. Run `capital_readiness` to connect market setup to account readiness without sounding like a product push.
6. Run `opportunity_alert` for trigger-style checks on owned, watched, or recently traded assets.
7. Run `weekly_reset` for a slower, portfolio-aware recap.
8. Run `asset_research` when a brief surfaces a setup that needs deeper, structured follow-up.
9. Hand off to `binance-us-fund-account`, `binance-us-spot-trade`, or `binance-us-account-status` when the user is past the briefing stage and needs an operational workflow.

## Output Contract

The script returns:

- JSON only
- text only
- or both

The JSON output is the source of truth. The text output is the delivery-ready rendering.

## Guardrails

- Treat the brief as informational, not financial advice.
- Never claim certainty or guaranteed returns.
- Do not place trades automatically.
- If the user requests an action after reading the brief, handle that as a separate explicit step.
- This skill is read-only. It does not place orders, move funds, or change account settings.
- Allowed outbound domains are limited to:
  - `api.binance.us`
  - `news.google.com`
