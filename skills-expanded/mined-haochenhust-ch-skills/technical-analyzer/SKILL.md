---
name: technical-analyzer
description: "This skill should be used when the user asks '现在能买吗', '技术面怎么样', '支撑位在哪', '量能如何', or after stock-analyzer confirms a fundamental thesis and entry timing is needed. Provides MA trend, support/resistance levels, and volume analysis as a SECONDARY timing tool — never the primary decision basis."
version: 1.0.0
---

# Technical Analyzer

Auxiliary timing tool for entry/exit decisions. NEVER use as primary decision basis — fundamentals first.

## When to Use

- After stock-analyzer confirms a fundamental thesis, use this to time the entry
- When deciding specific buy/sell price levels
- When checking if a stock is overbought/oversold

## Prerequisites

Uses the sibling `tushare-data` / `stock-market-data` skills. Set once per shell:

```bash
export TUSHARE_TOKEN=<your Tushare Pro token>    # never hard-code; see the tushare-data skill
PY=python3                                       # a python3 with tushare/pandas/akshare (e.g. stock-market-data/.venv/bin/python3)
SKILLS=~/.claude/skills                          # where you installed these skills
TS=$SKILLS/tushare-data/scripts/fetch_tushare.py
AK=$SKILLS/stock-market-data/scripts
```

## Data Retrieval

```bash
# Primary: Tushare Pro — 近3个月日K（OHLCV + 复权因子）
$PY $TS --mode daily --symbols {CODE}.SZ --start {3_MONTHS_AGO_YYYYMMDD}
$PY $TS --mode adj_factor --symbols {CODE}.SZ --start {3_MONTHS_AGO_YYYYMMDD}

# PE/PB/换手率/市值（用于量价+估值辅助）
$PY $TS --mode daily_basic --symbols {CODE}.SZ --start {3_MONTHS_AGO_YYYYMMDD}

# 周K（看中期趋势）
$PY $TS --mode weekly --symbols {CODE}.SZ --start {6_MONTHS_AGO_YYYYMMDD}

# Fallback: AKShare
$PY $AK/fetch_market_data.py --mode evening --stocks {CODE}
```

### Data Processing

Use adj_factor to calculate 前复权价格: `adj_price = close * adj_factor / latest_adj_factor`
This ensures MA calculations reflect true price movements (not distorted by splits/dividends).

## Analysis Framework

### 1. Trend Assessment
- Compare current price to 5/10/20/60 day moving averages
- Price above all MAs = strong uptrend
- Price below all MAs = strong downtrend
- MAs converging = potential breakout

### 2. Support & Resistance
- Recent highs/lows as reference points
- Round numbers (e.g., 80, 100) as psychological levels
- Volume clusters as support/resistance zones

### 3. Volume Analysis
- Volume increasing with price up = healthy trend
- Volume decreasing with price up = potential exhaustion
- Volume spike on down day = possible capitulation/bottom

### 4. Entry/Exit Timing Signals
- **Good entry**: Price pulls back to MA support with decreasing volume, then rebounds
- **Avoid entry**: Price extended far above MAs (>15% above 20MA), volume fading
- **Exit signal**: Price breaks below key MA with increasing volume

## Output Format

```markdown
### 技术面辅助判断 — {stock name}({code})

- **趋势**: 上升/下降/震荡
- **位置**: 站上/跌破 {X}日均线
- **量能**: 放量/缩量/正常
- **支撑位**: {price1}, {price2}
- **阻力位**: {price1}, {price2}
- **技术建议**: 当前适合/不适合建仓 — {reason}
```

## Rules

1. **Technical analysis is SECONDARY** — never override a fundamental sell signal because "chart looks good"
2. **Keep it simple** — MA + volume + support/resistance is enough. No exotic indicators.
3. **Don't over-interpret** — A-share small/mid caps are heavily influenced by sentiment, not technicals
