---
name: a-stock-screener
description: |
  A-share (China stock) screening system using a three-layer practical investment framework:
  Hard Filter → 100-Point Six-Dimension Scoring → Buy Discipline.
  Scans the entire A-share market, eliminates low-quality stocks with 10 hard filters,
  scores survivors on 6 dimensions (industry, moat, financials, governance, shareholder returns, valuation),
  fetches deep financial indicators for top candidates, and constructs a diversified portfolio
  with position sizing and buy/sell rules.

  A股实战选股系统 — 三层体系：硬过滤→百分制六维打分→买入纪律。
  全A股扫描，10道硬过滤关卡淘汰财务质量差的公司，六维百分制模型精选标的
  （行业赛道/竞争壁垒/财务质量/管理层治理/股东回报/估值预期差），
  逐只深度分析后构建行业分散的投资组合，并附带买入纪律和卖出触发条件。
  数据来源 akshare（免费、无需API Key），输出 JSON 结果 + HTML 可视化报告。

  Trigger keywords: A股选股, 选股, 选股系统, 全A扫描, A股筛选, 量化选股,
  stock screening, a-share screener, stock picker, 实战选股, 三层选股,
  六维打分, 百分制选股, 硬过滤, 核心研究池, 观察池, 买入纪律,
  run screener, 跑一遍选股, 帮我选股, 今天选什么股, 推荐组合,
  选股报告, screening report, portfolio builder, 组合构建.
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - execute_command
disable: false
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    tags:
      - investment
      - a-share
      - stock-screening
      - quantitative
      - portfolio
      - china-stock
      - finance
      - value-investing
---

# A-Stock Screener — A股实战选股系统

**What it does**: Scan the entire A-share market (~5000+ stocks), systematically filter and score every company, and output a ready-to-act investment portfolio with buy/sell discipline.

**How it works**: Fetch multi-period financial data from akshare (free) → apply 10 hard filters to eliminate low-quality stocks → score survivors on 6 dimensions (100-point model) → fetch deep financial indicators for top 25 → construct a sector-diversified top-10 portfolio with position sizing → generate JSON results + HTML visual report.

---

## Philosophy | 投资哲学

> **先看行业有没有风，再看公司有没有根，再看利润有没有金，最后看价格有没有坑。**

This system is designed for **non-financial, non-real-estate A-share companies**, especially suited for: consumer, manufacturing, pharma, equipment, tech hardware, and some ToB software/services. Banks, brokers, insurance, and heavy cyclical resource stocks are excluded by design.

Core principle: **宁可漏掉10只热门票，也不要把1只财务质量差的票留下来。**

---

## Three-Layer Architecture | 三层架构

### Layer 1: Hard Filter (硬过滤)

10 elimination gates. Any failure = immediate rejection:

| # | Filter | Threshold |
|---|--------|-----------|
| 1 | ST / New IPO / Delisting | Reject all |
| 2 | Valid price | Must have real-time quote |
| 3 | Industry exclusion | Banks, insurance, real estate, brokers, trusts |
| 4 | Profitability | At least 2 years positive EPS (out of 3-5 periods) |
| 5 | ROE consistency | ROE >= 10% for at least 2 years |
| 6 | Cash flow quality | Cumulative operating CF / net profit >= 50% |
| 7 | Revenue stability | Coefficient of variation < 1.0 (no cliff-like swings) |
| 8 | Penny stock filter | Price >= 5 yuan |
| 9 | Pledge risk | Major shareholder pledge ratio < 50% |
| 10 | Quality gate | Must be in CSI300/500/1000 index, OR ROE > 15% |

### Layer 2: 100-Point Six-Dimension Scoring (百分制六维打分)

| Dimension | Max Points | Key Metrics |
|-----------|-----------|-------------|
| D1: Industry & Track | 20 | Index membership, industry category, revenue growth trend, policy direction |
| D2: Competitive Moat | 20 | Gross margin level & stability, ROE consistency, scale effects |
| D3: Financial Quality | 25 | ROE/ROIC, cash flow matching, margin trends, revenue stability |
| D4: Management & Governance | 15 | Pledge ratio, dividend history, index quality proxy |
| D5: Shareholder Returns | 10 | Dividend yield, payout ratio, cash flow coverage |
| D6: Valuation Gap | 10 | PE vs quality-adjusted fair PE, momentum signals |

**Tier classification:**
- **>= 85**: Core research pool (核心研究池) — ready to wait for entry
- **75-84**: Observation pool (观察池) — wait for earnings/valuation confirmation
- **65-74**: Trading watch (交易关注) — tactical only, no heavy positions
- **< 65**: Skip (不碰)

### Layer 3: Deep Analysis + Portfolio Construction (深度分析+组合构建)

Top 25 candidates get individual deep financial analysis (86 detailed indicators per stock):
- Asset-liability ratio trend
- Accounts receivable turnover deterioration check
- Inventory turnover deterioration check
- Operating cash flow to net profit ratio
- Net profit margin trend
- ROA (total asset return rate)

Score adjustments of ±5 points based on deep analysis.

Portfolio construction:
- Top 10 with **sector diversity** (max 2 per industry)
- Position sizing: equal-weight with slight score-tilt
- Cash reserve: >= 9% (configurable)

### Buy Discipline (买入纪律)

Three iron rules + five sell triggers:

**Iron Rules:**
1. Don't go heavy on the first buy when the narrative is hottest
2. Build position in 3 tranches: entry → earnings confirmation → market dislocation
3. Write your sell conditions BEFORE buying

**Sell Triggers:**
1. Core product growth below expectations for 2 consecutive quarters
2. Gross margin deterioration without explanation
3. Accounts receivable / inventory significantly worsening
4. Major management behavior deviation
5. Industry competitive structure broken

---

## Workflow | 工作流程

### Step 1: Verify Environment | 确认环境

1. Check Python and required packages:
```bash
python -c "import akshare, pandas, numpy; print('OK')"
```

2. If missing, install:
```bash
pip install -r requirements.txt
```

3. Read config file `a-stock-screener-config.json` from workspace
4. If missing, generate defaults:
```bash
python scripts/init_config.py
```

### Step 2: Run Screening | 执行筛选

**Full screening** ("选股" / "帮我选股" / "跑一遍选股" / "run screener"):
```bash
python scripts/screener_engine.py
```

This will:
1. Fetch 3-5 periods of earnings data from akshare
2. Fetch real-time prices, index constituents, dividends, pledge data
3. Run 10 hard filters
4. Score all survivors on 6 dimensions
5. Fetch deep data for top 25
6. Construct portfolio with position sizing
7. Save results to `output/screener_results.json`

### Step 3: Generate Report | 生成报告

After screening completes, generate the visual HTML report:
```bash
python scripts/generate_report.py
```

This reads `output/screener_results.json` and produces `output/report.html` with:
- Screening funnel visualization
- Six-dimension score bars for each stock
- Key financial metrics grid
- Risk flags and buy notes
- Observation pool table
- Buy discipline section

### Step 4: Read & Present Results | 解读结果

1. Read `output/screener_results.json` for structured data
2. Present portfolio cards with score breakdowns
3. Highlight key risk flags for each position
4. Present observation pool candidates
5. Remind buy discipline rules

### Step 5: Push Results (Optional) | 推送结果

Push screening results to configured channels:

1. **WeChat Work**: `python scripts/send_wecom.py`
2. **DingTalk**: `python scripts/send_dingtalk.py`
3. **Feishu**: `python scripts/send_feishu.py`

Each supports `--test` flag to verify config.

---

## Configuration Guide | 配置指南

### Core Parameters (`screening` section)

```json
{
  "screening": {
    "capital": 400000,
    "min_price": 5,
    "max_pledge_ratio": 50,
    "min_roe_years": 2,
    "min_roe_threshold": 10,
    "min_cf_ratio": 0.5,
    "max_rev_cv": 1.0,
    "portfolio_size": 10,
    "max_per_industry": 2,
    "cash_reserve_pct": 9,
    "stop_loss_pct": -8,
    "max_single_weight_pct": 15
  }
}
```

- **capital**: Total investment capital in CNY
- **min_price**: Minimum stock price filter (avoid penny stocks)
- **max_pledge_ratio**: Maximum major shareholder pledge ratio (%)
- **min_roe_years**: Minimum years with ROE above threshold
- **min_roe_threshold**: ROE threshold (%) for consistency check
- **min_cf_ratio**: Minimum cumulative cash flow / profit ratio
- **max_rev_cv**: Maximum revenue coefficient of variation
- **portfolio_size**: Number of stocks in final portfolio
- **max_per_industry**: Max stocks per industry (diversity control)
- **cash_reserve_pct**: Minimum cash reserve (%)
- **stop_loss_pct**: Per-stock stop-loss trigger (%)
- **max_single_weight_pct**: Maximum weight per stock (%)

### Industry Preferences (`industries` section)

```json
{
  "industries": {
    "growth": ["半导体", "新能源", "光伏", "医疗器械", "人工智能", "机器人"],
    "stable": ["白酒", "食品饮料", "家用电器", "品牌服饰"],
    "pressured": ["教育", "传媒", "游戏", "影视", "地产"],
    "excluded": ["银行", "保险", "房地产开发", "证券", "多元金融", "信托"]
  }
}
```

- **growth**: Bonus +3 points in D1 (high growth, policy support)
- **stable**: Bonus +2 points in D1 (proven demand, brand moat)
- **pressured**: Penalty -2 points in D1 (regulatory headwinds)
- **excluded**: Hard filter exclusion (different financial models)

### Push Channels (`adapters` section)

| Channel | Config Key | Environment Variable |
|---------|-----------|---------------------|
| WeChat Work | `wechatwork.webhook_url` | `WECOM_WEBHOOK_URL` |
| DingTalk | `dingtalk.webhook_url`, `dingtalk.secret` | `DINGTALK_WEBHOOK_URL`, `DINGTALK_SECRET` |
| Feishu | `feishu.webhook_url`, `feishu.secret` | `FEISHU_WEBHOOK_URL`, `FEISHU_SECRET` |

---

## Scoring Deep Dive | 评分细节

### D1: Industry & Track Position (20 points)

Ask four questions:
1. Is this industry **expanding** or contracting in 3-5 years?
2. Is market share **concentrating** toward leaders?
3. Is policy **supportive**, neutral, or suppressive?
4. Can leaders **retain profits**, or will price wars erode them?

Quantitative proxies:
- CSI300 membership: +5 | CSI500: +3 | CSI1000: +1
- Growth industry: +3 | Stable industry: +2 | Pressured: -2
- Revenue growth > 20%: +2 | > 10%: +1

### D2: Competitive Moat (20 points)

Six moat sources (proxied quantitatively):
1. **Cost advantage** → high gross margin
2. **Product power** → gross margin stability
3. **Channel control** → scale (index membership)
4. **Customer stickiness** → ROE consistency
5. **Scale effects** → CSI300 bonus
6. **Organizational capability** → margin stability over years

### D3: Financial Quality (25 points) — **Most Important**

- ROE level (>25%: +4, >18%: +3, >12%: +2)
- ROE stability (std < 3: +1)
- Gross margin (>50%: +2, >30%: +1)
- Cash flow matching (CF/profit >1.0: +4, >0.8: +3, <0.3: -2)
- Profit growth quality (operating leverage bonus, one-off penalty)
- Revenue stability (CV < 0.15: +1, > 0.5: -1)

**If financial quality < 18 points, the stock is likely not suitable for heavy research.**

### D4: Management & Governance (15 points)

- Pledge ratio < 5%: +3 | < 15%: +2 | > 30%: -2
- Has cash dividends: +3 | partial: +1
- CSI300 governance proxy: +1

**If governance < 8 points, avoid long-term positions.**

### D5: Shareholder Returns (10 points)

- Dividend yield > 3%: +4 | > 2%: +3 | > 1%: +2
- Payout ratio > 5%: +1
- Cash flow supports dividends (CF ratio > 1.0): +1

### D6: Valuation & Expectation Gap (10 points)

Quality-adjusted fair PE:
- ROE > 20% AND growth > 20%: fair PE = 25x
- ROE > 15% AND growth > 15%: fair PE = 20x
- ROE > 12%: fair PE = 15x
- Otherwise: fair PE = 12x

Discount/premium scoring:
- Discount > 30%: +4 | > 15%: +3 | > 0%: +2
- Premium < 15%: +0 | < 30%: -1 | > 30%: -2

New 52-week high (with good fundamentals): +1

---

## Data Sources | 数据来源

All data from **akshare** (free, no API key required):

| Data | akshare API | Usage |
|------|------------|-------|
| Multi-period earnings | `stock_yjbb_em` | 3-5 years ROE, revenue, profit, cash flow |
| Real-time prices | `stock_zh_a_spot` | Current price, volume, turnover |
| CSI300/500/1000 constituents | `index_stock_cons_csindex` | Quality gate, index premium |
| Dividends | `stock_fhps_em` | Dividend yield, payout ratio |
| Pledge data | `stock_gpzy_pledge_ratio_em` | Major shareholder pledge ratio |
| 52-week highs | `stock_rank_cxg_ths` | Momentum signal |
| Deep financial indicators | `stock_financial_analysis_indicator` | 86-column detailed analysis per stock |

---

## Output Format | 输出格式

### JSON (`output/screener_results.json`)

```json
{
  "run_date": "2026-03-16",
  "version": "v5",
  "capital": 400000,
  "methodology": "三层体系: 硬过滤→百分制六维打分→买入纪律",
  "total_scanned": 11675,
  "after_hard_filter": 791,
  "scoring_model": { ... },
  "tier_classification": {
    "core_pool_75plus": 88,
    "observe_pool_65_74": 390,
    "trade_watch_55_64": 295,
    "skip_below_55": 18
  },
  "portfolio": [ ... ],
  "observation_pool": [ ... ],
  "buy_discipline": { ... }
}
```

### HTML Report (`output/report.html`)

Visual report with:
- Dark theme, responsive design
- Screening funnel visualization
- Stock cards with 6-dimension score bars
- Key financial metrics grid
- Risk flags and buy discipline reminders

---

## Important Notes | 注意事项

1. **Network**: akshare fetches data from Eastmoney/THS APIs. May be slow or blocked in some corporate networks.
2. **Rate Limits**: Deep analysis fetches individual stock data sequentially with 0.3s delay. Full run takes 3-5 minutes.
3. **Data Freshness**: Earnings data availability depends on reporting season. Best run after quarterly report deadlines (Apr/Jul/Oct/Jan).
4. **Not Investment Advice**: This is a quantitative screening tool, not financial advice. Always combine with industry research and individual stock analysis.
5. **Excluded Sectors**: Financial sector (banks, insurance, brokers) and real estate use different financial models and should NOT be evaluated with this system.

---

## Quick Entry Scripts | 快捷入口

- `run_screener.py` — Full screening + report generation (one-click)
- `scripts/screener_engine.py` — Core screening engine only
- `scripts/generate_report.py` — Report generation from existing results
- `scripts/init_config.py` — Generate default config
