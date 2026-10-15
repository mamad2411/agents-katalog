---
name: technical-analysis-chart-reading
description: Murphy-style technical analysis for secondary-market trading. Use when Codex needs to read charts/K-lines (K线), trendlines, support/resistance, chart patterns, volume, open interest, moving averages, oscillators, momentum, divergence, point-and-figure logic, cycles, or technical indicators for stocks, futures, crypto, FX, rates, commodities, ETFs, or any liquid market. Also use when asked to turn OHLCV/OHLCVI data into a technical analysis, build a chart-reading checklist, or synthesize signals from John J. Murphy's technical-analysis framework.
---

# Technical Analysis Chart Reading

## Overview

Use this skill to analyze market charts and OHLCV/OHLCVI data through the John J. Murphy technical-analysis stack: market philosophy, trend, price structure, patterns, volume/open interest, moving averages, oscillators, cycles, systems, and risk control.

Treat every output as probabilistic market analysis, not financial advice. State the timeframe, evidence, invalidation level, and risk controls before giving any directional trading conclusion.

## Core Workflow

1. Define the market, instrument, timeframe, and available evidence. If live or latest market data matters, fetch or verify current data before analyzing.
2. Establish market context with higher timeframe first: primary trend, intermediate trend, near-term trend, and whether the market is trending or ranging.
3. Read price structure before indicators: swing highs/lows, support/resistance, trendlines, channels, gaps, breakout/retest behavior, and where price sits in the range.
4. Identify chart patterns only when the structure is mature enough. Prefer conservative labeling over forcing a pattern.
5. Check confirmation: volume for equities/crypto, open interest for futures, breadth/intermarket evidence when available, and whether participation supports or contradicts the price move.
6. Apply indicators as secondary evidence. Moving averages and channels are trend tools; oscillators are most useful for range extremes, divergence, and momentum loss.
7. Synthesize with confluence: separate aligned evidence, conflicting evidence, and missing evidence.
8. Convert analysis into a scenario plan: bullish case, bearish case, trigger, invalidation, target/measurement if justified, position-sizing/risk note, and what would change the view.

## Use The Resources

- Read `references/murphy_knowledge_graph.json` when a request asks for a knowledge graph, comprehensive decomposition, teaching structure, or multi-domain synthesis.
- Read `references/indicator_playbook.md` when the request involves indicators, moving averages, oscillators, divergence, OBV, open interest, or signal interpretation.
- Read `references/patterns_and_structure.md` when the request involves chart images, K-line structure, trendlines, support/resistance, channels, gaps, reversals, continuations, point-and-figure, Elliott, Fibonacci, or cycles.
- Read `references/analysis_template.md` when the user asks for a report, trade plan, checklist, or structured output.
- Run `scripts/ta_signals.py` when the user provides CSV OHLCV/OHLCVI data and wants calculated indicators.

## OHLCV Script

The script uses only the Python standard library. It expects a CSV with at least close prices; high/low/open/volume/open_interest improve the analysis.

```bash
python scripts/ta_signals.py data.csv --json
python scripts/ta_signals.py data.csv --lookback 120
```

Accepted column names include common variants such as `date`, `time`, `timestamp`, `open`, `high`, `low`, `close`, `volume`, `vol`, `open_interest`, `oi`.

Use script output as evidence, then apply the skill workflow. Do not treat a raw indicator cross as a complete trading signal without trend, structure, participation, and risk context.

## Chart Image Protocol

When reading a chart image:

1. Describe only visible evidence first: instrument/timeframe if shown, candle direction, recent swings, range, trendline/channel, MAs, volume, oscillators, and annotations.
2. Mark uncertainty where labels, axes, or indicator settings are unreadable.
3. Infer pattern and indicator states only after visible evidence is listed.
4. Avoid precise price levels if the axis is unreadable; use relative levels such as "above prior swing high" or "near the lower channel."
5. Give a scenario tree rather than a single confident call.

## Guardrails

- Never claim certainty, guaranteed returns, or a deterministic prediction.
- Do not recommend oversized leverage or ignore stop/invalidation planning.
- Mention that technical analysis can fail in event-driven, illiquid, manipulated, or regime-shifting markets.
- For futures, treat open interest as participation evidence, not direction by itself.
- For oscillators, avoid calling every overbought reading bearish in a strong uptrend, or every oversold reading bullish in a strong downtrend.
