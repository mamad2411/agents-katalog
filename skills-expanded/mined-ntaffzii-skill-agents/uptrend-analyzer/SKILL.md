---
name: uptrend-analyzer
description: Use this skill to score how many stocks in a universe are in an established "stage 2" uptrend (price above the 50-day MA, 50-day MA above the 200-day MA) from a plain CSV, no market-data API required. Trigger on "uptrend participation", "stage 2 stocks", "how many stocks are in an uptrend", "50 MA above 200 MA screen". Pairs with [market-breadth-analyzer](../market-breadth-analyzer/SKILL.md) for a fuller market-regime read.
---

# Uptrend Analyzer

## Overview

[market-breadth-analyzer](../market-breadth-analyzer/SKILL.md) asks "is price above one moving average?" This skill asks a stricter question: is the stock in an **established uptrend structure** — price above its 50-day MA, and the 50-day MA itself above the 200-day MA. That two-part test (a well-known heuristic associated with Stan Weinstein's stage analysis, also used in CANSLIM/Minervini-style trend approaches) filters out stocks that are merely bouncing from a downtrend but haven't structurally turned yet.

**Not financial advice.** This is a descriptive screen over data you supply, not a buy signal.

## When to use

- คัดหุ้นที่อยู่ใน uptrend จริงๆ (ไม่ใช่แค่ราคาสูงกว่า MA เส้นเดียว)
- Scoring what fraction of a watchlist/index is in a "stage 2" structure
- Part of a market-regime or swing-candidate pre-screen (combine with a fundamental/technical screener like [dividend-value-screener](../dividend-value-screener/SKILL.md) for the value side, or a breakout screener for the momentum side)

## When NOT to use

- The user wants a short-term momentum/breakout signal — this skill measures structural trend state, not entry timing
- Only one moving average is available (no 50-day and 200-day both) — this test specifically needs both; use market-breadth-analyzer instead with whatever single MA is available

## Core knowledge

**Definition**: `price > 50-day MA AND 50-day MA > 200-day MA`. Both legs matter — price above a declining or flat 50-day MA that hasn't yet crossed above the 200-day MA is typically still a base or early recovery, not an established uptrend by this definition.

This is one of several published trend-classification heuristics (Weinstein's four-stage model is the origin; CANSLIM and Minervini-style trend templates use variations with additional legs — e.g. price also above the 150-day MA, MAs in the correct order, price a meaningful distance above a 52-week low). This skill implements the simplified two-leg version; treat the result as a starting filter, not a complete trend-template screen.

## Common mistakes

1. Screening only on "price above 50-day MA" and calling it an uptrend — that alone doesn't distinguish an established uptrend from a stock still recovering inside a longer downtrend (missing the "50MA > 200MA" leg).
2. Treating this as a complete trend-template screen — real trend-template methodologies (e.g. Minervini's 8-point template) add more conditions (distance from 52-week high/low, relative strength rank) that this simplified skill does not implement.
3. Using the uptrend percentage as a timing signal for individual entries rather than a market-wide participation read.

## Code

`uptrend.py` — no dependencies:

- `is_in_uptrend(price, ma50, ma200)` → `bool`
- `compute_uptrend_participation(rows)` → `UptrendResult(total, in_uptrend, excluded, pct_uptrend)`

Run `python3 uptrend.py` for the self-test.

## Known limitations

- Implements the simplified two-leg heuristic only — not a full multi-criterion trend template.
- Does not fetch data; accuracy depends entirely on the CSV the user supplies.
- "Uptrend by this test" is a structural classification, not a prediction — a stock can satisfy the test and still decline from here.
