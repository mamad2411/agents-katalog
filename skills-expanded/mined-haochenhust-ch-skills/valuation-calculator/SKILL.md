---
name: valuation-calculator
description: "This skill should be used when the user asks '这只股票贵不贵', '估值合理吗', '目标价多少', '跟同行比怎么样', or during a stock-analyzer valuation step. Calculates PE/PB/PS historical percentiles, builds peer-comparison tables, and derives target prices via PE-based or PB-based methods. Quantitative/relative valuation — distinct from the DCF-style intrinsic-value-analysis skill."
version: 1.0.0
---

# Valuation Calculator

Quantitative, relative valuation for investment decisions (PE/PB percentiles + peer comparison + target price). For absolute DCF-style intrinsic value, use the `intrinsic-value-analysis` skill instead.

## When to Use

- During stock analysis (the valuation step)
- When deciding a target price for a trade
- When comparing multiple candidates in the same sector

## Prerequisites

Uses the sibling `tushare-data` / `stock-market-data` skills. Set once per shell:

```bash
export TUSHARE_TOKEN=<your Tushare Pro token>    # never hard-code; see the tushare-data skill
PY=python3                                       # a python3 with tushare/pandas/akshare (e.g. stock-market-data/.venv/bin/python3)
SKILLS=~/.claude/skills                          # where you installed these skills
TS=$SKILLS/tushare-data/scripts/fetch_tushare.py
AK=$SKILLS/stock-market-data/scripts
```

## Methods

### 1. Historical Percentile

Use Tushare `daily_basic` for direct PE/PB/PS time series (no manual calculation needed):

```bash
# Get 3-year PE/PB/PS history for percentile calculation
$PY $TS --mode daily_basic --symbols {CODE}.SZ --start 20230101
```

From the returned data:
- Calculate PE_TTM percentile over available history
- Calculate PB percentile over available history
- Identify current position in historical range

### 2. Peer Comparison

```bash
# Tushare: valuation + financial ratios for each peer
$PY $TS --mode daily_basic --symbols {code1}.SZ --start 20260301
$PY $TS --mode fina_indicator --symbols {code1}.SZ
# Repeat for each peer...

# Fallback: AKShare (batch)
$PY $AK/fetch_financial_data.py --mode stock --symbols {code1},{code2},{code3}
```

Compare: PE, PB, ROE, revenue growth, net margin across peers.
Identify: who is cheapest relative to growth? (PEG ratio)

Supplement with WebSearch for analyst consensus (券商一致预期), forecasts, and cross-sector peer comparison data:

```bash
WebSearch: "{stock name} 一致预期 估值 目标价"
```

### 3. Target Price Derivation

Methods available:
- **PE-based**: Target PE × Expected EPS = Target Price
- **PB-based**: Target PB × Book Value = Target Price
- **DCF-simplified**: skip here; use the `intrinsic-value-analysis` skill for a proper DCF-style approach

## Output Format

```markdown
### 估值分析 — {stock}({code})

**当前估值**
- PE(TTM): {X}x
- PB: {X}x
- 市值: {X} 亿

**同行对比**
| 公司 | PE | PB | ROE | 净利率 | 营收增速 |
|------|----|----|-----|--------|----------|

**估值判断**: 偏贵/合理/偏低 — {reasoning}

**目标价推导**
- 方法: {PE-based / PB-based}
- 假设: {key assumption}
- 目标PE: {X}x → 目标价: {X} 元 → 上行空间: {X}%
```

## Rules

1. **Valuation is relative, not absolute** — always compare to peers and history
2. **Growth justifies premium** — high PE is OK if growth is higher
3. **State assumptions explicitly** — target price is only as good as its assumptions
