---
name: stock-analyzer
description: "This skill should be used when the user asks to '分析一下XX股票', '研究一下XX', '这只股票能不能买', or when a research task identifies a stock candidate for deep analysis. Produces structured research notes covering 5 dimensions: business model, financials, valuation, catalysts, and risks — with a clear buy/sell/hold thesis and falsification conditions."
version: 1.0.0
---

# Stock Analyzer

Standardized deep-dive analysis for individual stocks, producing a structured research note.

## When to Use

- User asks to analyze a specific stock
- A research task identifies a potential trading candidate
- Updating analysis for a stock already in your research notes

## Prerequisites

Data commands below use the sibling `tushare-data` and `stock-market-data` skills. Install them, then set once per shell:

```bash
export TUSHARE_TOKEN=<your Tushare Pro token>    # never hard-code; see the tushare-data skill
PY=python3                                       # a python3 with tushare/pandas/akshare (e.g. stock-market-data/.venv/bin/python3)
SKILLS=~/.claude/skills                          # where you installed these skills
TS=$SKILLS/tushare-data/scripts/fetch_tushare.py
AK=$SKILLS/stock-market-data/scripts
```

## Analysis Workflow

### Step 1: Gather Data

```bash
# Primary: Tushare Pro (richer, more stable)
$PY $TS --mode fina_indicator --symbols {CODE}.SZ
$PY $TS --mode daily_basic --symbols {CODE}.SZ --start 20260101
$PY $TS --mode income --symbols {CODE}.SZ
$PY $TS --mode forecast --symbols {CODE}.SZ
$PY $TS --mode top10_holders --symbols {CODE}.SZ
$PY $TS --mode daily --symbols {CODE}.SZ --start {3_MONTHS_AGO}
$PY $TS --mode adj_factor --symbols {CODE}.SZ --start {3_MONTHS_AGO}

# Fallback: AKShare
$PY $AK/fetch_financial_data.py --mode stock --symbols {CODE}
```

### Step 2: Web Research

Search for recent news, analyst reports, and industry developments:
- Use WebSearch for "{stock name} 券商研报 一致预期" (analyst consensus, earnings forecasts)
- Use WebSearch for "{stock name} 最新研报 2026"
- Use WebSearch for "{stock name} {industry keyword} 进展"
- Check Xueqiu/Eastmoney for recent discussions

### Step 2.5: Price & Volume Analysis (近3个月日K)

Using the daily OHLCV + adj_factor data from Step 1:
- **走势形态**: 上升趋势/下降趋势/震荡盘整？近3个月涨跌幅？
- **均线位置**: 当前价格相对5/10/20/60日均线的位置
- **量价关系**: 近期量能变化趋势（放量上涨？缩量回调？）
- **关键价位**: 近3个月高点/低点，支撑位/阻力位
- **波动率**: 近期日均振幅，判断当前波动是否正常

This step bridges fundamentals (Step 1-2) and the 5-dimension analysis (Step 3), providing price context for valuation and entry timing.

### Step 3: Analyze & Synthesize

Evaluate across 5 dimensions:

1. **Business Model Quality**
   - What does the company do? Revenue composition?
   - Competitive advantages (moat)? Barriers to entry?
   - Customer concentration risk?

2. **Financial Quality**
   - Revenue growth trend (YoY)
   - Profit margin trend (gross margin, net margin)
   - ROE level and trend
   - Balance sheet health (debt ratio, current ratio)
   - Cash flow quality (operating cash flow vs net profit)

3. **Valuation**
   - Current PE/PB vs historical range
   - PE/PB vs peers
   - Target price derivation (if applicable)
   - Is the current price pricing in good news or bad news?

4. **Catalysts**
   - What events could trigger re-rating?
   - Timeline for each catalyst
   - Probability assessment

5. **Risks**
   - What could go wrong?
   - Sector/market risks
   - Company-specific risks

### Step 4: Output Research Note

Save to `research-{stock_code}-{stock_name}.md` in your research notes directory.

## Output Template

```markdown
# {Stock Name}({Stock Code}) — 研究笔记

> 分析日期：{date}
> 数据截止：{latest financial period}

## 一句话结论

{做多/做空/观望} | 置信度 {X}% | 目标涨幅 {X}%

## 核心逻辑（≤3条）

1. {logic 1}
2. {logic 2}
3. {logic 3}

## 关键数据

### 财务概况
- 营收（TTM）：{X} 亿 | 同比 {X}%
- 净利润（TTM）：{X} 亿 | 同比 {X}%
- 毛利率：{X}% | 净利率：{X}%
- ROE：{X}%
- 资产负债率：{X}%

### 估值
- 当前股价：{X} 元
- PE(TTM)：{X}x | 历史分位 {X}%
- PB：{X}x
- 目标价：{X} 元（推导逻辑：...）

## 催化剂

- {date}: {event} — {expected impact}

## 风险点

1. {risk 1}
2. {risk 2}

## 证伪条件

出现以下任一信号则论点失效，需重新评估：
1. {condition 1}
2. {condition 2}

## 交易建议

- **建仓价位**：{X} 元附近
- **目标价位**：{X} 元
- **止损价位**：{X} 元（-12%）
- **建议仓位**：{X}%（根据置信度）
```

## Quality Checklist

Before saving the research note, verify:
- [ ] Conclusion has clear direction (做多/做空/观望), not "可能涨也可能跌"
- [ ] Confidence level is justified by evidence
- [ ] All financial data cites source and reporting period
- [ ] At least 1 catalyst with specific timeline
- [ ] At least 2 risk points identified
- [ ] At least 1 falsification condition that is measurable
- [ ] Trading suggestion includes entry, target, stop-loss
