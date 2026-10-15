---
name: weekly-financial-report
description: "Produces a comprehensive weekly cross-asset financial report (Word document) covering commodities, equity indices, China/US bond yields, and FX. Fetches live data from yfinance and akshare; 5 matplotlib charts embedded; 8-item macro news section from Tavily search."
version: 1.0.0
author: tommycui1234
platforms: [macos, linux]
tools:
  - bash
  - tavily
metadata: {"hermes": {"tags": ["finance", "python", "reporting", "cross-asset", "chinese"], "category": "finance", "requires_toolsets": ["terminal"]}, "openclaw": {"requires": {"bins": ["python3"]}}}
---

# Global Macro and Cross-Asset Weekly
## 环球宏观与多资产周度观察

## When to Use

Use this skill when the user types `/weekly-financial-report` or asks for a cross-asset weekly market summary report. The report covers:

- Commodity futures (Brent crude, Gold, SHFE Copper/Aluminium/Rebar, DCE Coking Coal)
- Equity indices (Nasdaq, Dow Jones, S&P 500, Hang Seng, Shanghai Composite)
- China government bond yields (1Y / 5Y / 10Y / 30Y)
- US Treasury yields (2Y / 5Y / 10Y / 30Y)
- FX (USD/CNY, DXY, EUR/USD, USD/JPY)

Output: a Word document (`.docx`) with 7-column tables, 5 embedded PNG charts, and Chinese-language analysis text.

---

## First-Time Setup

Ensure Python dependencies are installed:

```bash
pip install yfinance akshare python-docx matplotlib numpy
```

Clone the scripts (one-time):

```bash
git clone https://github.com/tommycui1234/weekly-financial-report.git ~/weekly-financial-report
```

Output defaults to `~/weekly-report-output/` (created automatically). Override via env var:

```bash
export WEEKLY_REPORT_DIR=~/my/custom/output/path
```

---

## Procedure

### Step 1 — Auto-calculate dates

Run this snippet to derive the report window. Proceed immediately; do not ask the user for dates.

```python
from datetime import date, timedelta

today = date.today()
# Mon–Fri: use today as WEEK_END (WTD or full week)
# Sat–Sun: roll back to the Friday that just passed
if today.weekday() < 5:       # Mon=0 … Fri=4
    WEEK_END = today
else:                          # Sat=5, Sun=6
    WEEK_END = today - timedelta(days=today.weekday() - 4)

WEEK_START  = WEEK_END - timedelta(days=WEEK_END.weekday())  # Monday of WEEK_END's week
PREV_FRIDAY = WEEK_START - timedelta(days=3)                  # Friday of the preceding week (change baseline)
YTD_START   = date(WEEK_END.year - 1, 12, 31)

print(WEEK_START, WEEK_END, PREV_FRIDAY, YTD_START)
```

**What each variable means:**

| Variable | Mon Apr 28 example | Fri May 1 example | Sat/Sun Apr 26–27 example |
|----------|--------------------|-------------------|---------------------------|
| `WEEK_END` | Apr 28 (today) | May 1 (today) | Apr 25 (Friday just passed) |
| `WEEK_START` | Apr 28 (Monday) | Apr 27 (Monday) | Apr 21 (Monday) |
| `PREV_FRIDAY` | Apr 25 (Friday before this week) | Apr 24 (Friday before this week) | Apr 18 (Friday before that week) |
| Change formula | Apr 28 vs Apr 25 | May 1 vs Apr 24 | Apr 25 vs Apr 18 |
| Label | `WTD涨跌幅` | `周涨跌幅` | `周涨跌幅` |

The user may override any date by passing them explicitly after the command.

**Cross-market note (Option A):** Each asset uses its own last available close. On mid-week runs, Asian and US markets may have different last-close dates — this is by design. The Word subtitle reads "数据截至各市场最新收盘". Column label: `WTD涨跌幅` (Mon–Thu) or `周涨跌幅` (Fri–Sun).

### Step 2 — Collect macro news (Tavily)

Search for **8 news items from `WEEK_START`–`WEEK_END`**, strictly split as China 5, International 3.

Run these 3 searches:
1. `"中国经济金融政策 {WEEK_START} {WEEK_END}"`
2. `"Hong Kong Macau economy news {WEEK_START} {WEEK_END}"`
3. `"US Fed economy geopolitics {WEEK_START} {WEEK_END}"`

**China 5 items** (priority order):
1. China economy & finance: PBOC, NFRA, CSRC, SAFE, SASAC, MoF
2. Real estate: MOHURD, major developer news
3. Tech & industry: semiconductors, AI, new energy
4. Construction & infrastructure: SOE headlines
5. Hong Kong & Macau

**International 3 items** (priority order):
1. US economy: Fed, key data releases, tariff policy
2. Geopolitics: Middle East / Russia-Ukraine / Taiwan Strait
3. Other major economies

Writing rules: title ≤ 16 Chinese characters; body ~200 chars; cite authoritative source; no 重磅/震撼/炸裂; all 8 items must be from the current report week; distinct topics, no overlap.

Insert the 8 news items into the `macro_events` list at the top of `build_full_report.py` before running.

### Step 3 — Run the build script

```bash
python ~/weekly-financial-report/scripts/build_full_report.py \
  {WEEK_START} {WEEK_END} {PREV_FRIDAY} {YTD_START}
```

Optional: override output directories via argv[5] and argv[6]:

```bash
python ~/weekly-financial-report/scripts/build_full_report.py \
  {WEEK_START} {WEEK_END} {PREV_FRIDAY} {YTD_START} \
  ~/my/charts/dir ~/my/docs/dir
```

The script runs in ~1–2 minutes (yfinance ~30s + akshare ~20s + charts ~10s + docx ~10s).

### Step 4 — Report output location

```
~/weekly-report-output/
├── docs/
│   ├── {WEEK_END}_综合周度报告.docx    ← Word report
│   └── {WEEK_END}_综合周度报告.pdf     ← PDF (auto-converted from docx)
└── charts/
    ├── commodity_weekly_cumulative.png
    ├── index_weekly_cumulative.png
    ├── china_bond_yield_change.png
    ├── us_bond_yield_change.png
    └── fx_combined.png
```

Confirm the output path to the user when done.

---

## Pitfalls

- `akshare` bond `close` values are already in % (1.764 = 1.764%) — **never multiply by 100**
- Domestic futures (`cu0`, `al0`, `rb0`, `jm0`) must be fetched **unconditionally**, not inside an `if not comm_all:` branch
- All 4 FX pairs must appear in both chart and table: USD/CNY, DXY, EUR/USD, USD/JPY
- Bond/FX chart Y-axes must **not** start at 0 (auto-focus enabled)
- Commodity/equity chart Y-axes use cumulative % from YTD_START, starting at 0
- `BZ=F`: the `=F` suffix is Yahoo Finance's futures identifier — not a math operator
- Chart titles must be empty strings (captions go in Word, not in the image)
- matplotlib font: `Arial Unicode MS` (fallback: `Noto CJK`) for Chinese character support
- Analysis text must only reference instruments present in the table — no silver, no STOXX 600, no individual stocks
- All 8 macro news items must be from `WEEK_START`–`WEEK_END` — no stale news

---

## Verification

- [ ] Script exits with `✅ Report saved to:` message and no Python tracebacks
- [ ] Word document opens and contains 5 sections with tables and charts
- [ ] 5 PNG chart files exist in the charts output directory
- [ ] All table values are non-zero and reflect the current week's data
- [ ] 8 macro news items are present in Section 0, all dated within the report week
- [ ] FX chart shows 4 series (USD/CNY, DXY, EUR/USD, USD/JPY)
- [ ] Column label is `WTD涨跌幅` mid-week or `周涨跌幅` on Friday/weekend
