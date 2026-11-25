# Price Monitor & Alert Agent

Real-time stock price monitoring with configurable stop-loss, take-profit alerts, and market hours awareness. Sends alerts via Telegram.

## What it does

- Monitors stock prices during market hours (pre-market, regular, after-hours)
- Triggers alerts when stop-loss or take-profit levels are hit
- 30-minute cooldown deduplication (no alert spam)
- Automatic market hours detection (skips weekends/closed hours)
- Telegram bot integration for instant mobile alerts

## Configuration

```
Monitor these positions:
- IREN: stop-loss $39.00, take-profit $75.00
- TEM:  stop-loss $49.75, take-profit $65.00
- RXRX: stop-loss $2.85,  take-profit $5.00
- KTOS: stop-loss $52.00, take-profit $70.00

Alert me via Telegram. Check every 5 minutes during market hours.
```

## Example Output (terminal)

```
[Monitor] PRE-MARKET — checking prices...
📊 Price Check — 2026-05-13 08:47 ET

  IREN: $56.93 (+3.23%) | stop $39.00  | distance +46.0% ✅
  TEM:  $47.19 (-2.62%) | stop $49.75  | distance  -5.1% 🚨 ALERT
  RXRX: $3.15  (-3.37%) | stop $2.85   | distance +10.5% ✅
  KTOS: $57.47 (+0.84%) | stop $52.00  | distance +10.5% ✅

[Monitor] ALERT sent → Telegram: TEM $47.19 below stop $49.75. Review at open.
[Monitor] Next check: 09:02 ET
```

## Example Telegram Alert

```
🚨 STOP-LOSS ALERT

TEM  $47.19  ▼ -2.62%
Stop: $49.75 | Breach: -$2.56 (-5.1%)

Pre-market. Consider reviewing at open.
Not financial advice.
```

## Features

- Pre-market (4:00–9:30 ET), Regular (9:30–16:00), After-hours (16:00–20:00)
- Price fetch via Yahoo Finance API (free, no API key needed)
- 30-minute cooldown deduplication (no repeat alerts)
- Auto-skips weekends and market holidays

## Requirements

- Bash tool access (for running the monitor script)
- Telegram bot token and chat ID (for alerts)

## Pricing

Free: Monitor up to 3 tickers (included in GitHub repo)
**Full bundle — $29 one-time**: Unlimited tickers + options flow alerts + all investment skills
→ https://jaehyunpark.gumroad.com/l/tcyahy

## Author

Production-tested monitoring system that caught real stop-loss triggers ($TEM $47.44, $IREN $50 support) and prevented losses.
