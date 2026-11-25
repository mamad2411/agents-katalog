---
name: financial-data-provisioning
description: >-
  Provision financial market datasets — S&P 500 fundamentals, A-share (SSE/SZSE)
  daily data, intraday Nifty 50 tick data, stock lists, sector maps, and
  financial KPIs. Covers yfinance fallback, KaggleHub download, AKShare for
  Chinese markets, and multiple storage backends: MongoDB (NoSQL document) and
  DuckDB (columnar time-series).
category: data-science
triggers:
  - Kaggle dataset not accessible / blocked / 403
  - need S&P 500 financial data with sector and EBITDA
  - quant assignment requiring financial CSV
  - yfinance data extraction for fundamentals
  - Chinese A-share / SSE / SZSE stock data needed
  - AKShare data retrieval
  - MongoDB financial data pipeline
  - multi-market index overview / 大盘走势 query (A-shares, HK, US, Korea)
  - US tech sector sub-sector drill-down
  - last trading day market snapshot for any major market
  - intraday market data infrastructure (1-min OHLCV)
  - time-series vs NoSQL database performance comparison
  - DuckDB for market data storage and querying
  - rates data needed (fed funds / SOFR / treasury yields / policy path)
  - market outlook or rates deck requiring current data
  - FedWatch-style meeting probabilities (Fed or ECB)
  - EURIBOR / €STR / ECB deposit rate levels
  - futures contract specs, quotes or margin levels (SOFR, EURIBOR, €STR)
---

# Financial Data Provisioning for Quant Assignments

## S&P 500 Data

### Option 1 — KaggleHub (preferred, no auth needed)

```bash
pip install kagglehub
```

```python
import kagglehub
path = kagglehub.dataset_download('paytonfisher/sp-500-companies-with-financial-information')
# => /Users/.../.cache/kagglehub/.../financials.csv (505 rows, 14 columns)
```

Columns: `Symbol`, `Name`, `Sector`, `Price`, `Price/Earnings`, `Dividend Yield`,
`Earnings/Share`, `52 Week Low`, `52 Week High`, `Market Cap`, `EBITDA`,
`Price/Sales`, `Price/Book`, `SEC Filings`

### Option 2 — yfinance fallback

When Kaggle is blocked, build from constituents.csv + yfinance. See the original
skill content below for the full fallback procedure.

## Chinese A-Share Data

### Source — yfinance (assignments that require it)

**SSE ticker format:** `600000.SS` (stock code + `.SS` suffix)

```bash
pip install yfinance
```

```python
import yfinance as yf

# Single stock
hist = yf.Ticker('600000.SS').history(start='2010-01-01')

# Batch download (50 stocks per batch — reliable rate limit)
tickers = ['600000.SS', '600004.SS', ...]
data = yf.download(tickers, start='2010-01-01', group_by='ticker',
                   threads=False, progress=False)
```

**CRITICAL — proxy issue:** If the shell has `http_proxy` / `https_proxy` set (common in corporate/campus environments), yfinance fails with `Remote end closed connection without response`. Fix at the top of the script:

```python
import os
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
os.environ.pop('HTTP_PROXY', None)
os.environ.pop('HTTPS_PROXY', None)
```

**yfinance MultiIndex parsing** — `yf.download()` returns columns `(Ticker, Price)`:

```python
# Access single stock's data from batch result
df = pd.DataFrame({
    'Open':   data.get(('600000.SS', 'Open'),   pd.Series(dtype=float)),
    'Close':  data.get(('600000.SS', 'Close'),  pd.Series(dtype=float)),
    'Volume': data.get(('600000.SS', 'Volume'), pd.Series(dtype=float)),
}).dropna(subset=['Close'])
```

**⚠️ CRITICAL: `yf.Ticker.history()` with `progress=False` inside background jobs** — subprocess shells (Hermes `background=true`, cron, tmux) often lose network proxy config and can't reach Yahoo Finance. Always test in foreground before backgrounding. Add `os.environ.pop('http_proxy', None)` at the top of the script to force direct connection.

### Source — AKShare (verified, free, no API key)

Use for stock list ONLY when yfinance can't provide it. Cache results to CSV to avoid repeated unreliable network calls.

```bash
pip install akshare
```

```python
import akshare as ak

# 1. Get all A-share stock list (~5530 stocks)
all_stocks = ak.stock_info_a_code_name()
# Columns: code, name

# 2. Filter by exchange
sse = all_stocks[all_stocks['code'].str.startswith('6')]  # Shanghai ~2308
sse['yf_ticker'] = sse['code'] + '.SS'

# 3. Cache to CSV (avoid re-calling AKShare)
sse.to_csv('sse_stocks.csv', index=False)

# 4. Later runs: load from cache
import pandas as pd
sse = pd.read_csv('sse_stocks.csv')
```

**AKShare reliability:** The `stock_info_a_code_name()` function queries SH/SZ/BJ exchanges. The BSE endpoint sometimes drops connections (`Remote end closed`). Add retry logic:

```python
for attempt in range(3):
    try:
        all_stocks = ak.stock_info_a_code_name()
        break
    except Exception:
        time.sleep(3)
else:
    raise  # all 3 failed
```

## Rates & Policy Data — USD/EUR (free, no API key)

For policy rates, treasury yields, SOFR/EFFR and futures-implied expectations — fetch live, never from memory (user has zero tolerance for fabricated numbers).

### FRED CSV endpoints (no key needed)

```bash
curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SERIES_ID" -o id.csv
```

Key series IDs: `EFFR` (daily effective fed funds), `SOFR`, `DFF`, `DFEDTARU`/`DFEDTARL` (target-range upper/lower — the authoritative policy path), `DGS3MO`/`DGS6MO`/`DGS1`/`DGS2`/`DGS5`/`DGS10`/`DGS30` (constant-maturity treasury yields), `T10Y2Y` (10Y−2Y spread), `ECBDFR` (ECB deposit facility rate), `WFII10` (ACM 10y term premium).

- Reconstruct the policy path with pandas: `df["value"].diff().ne(0)` on DFEDTARU — awk change-detection over a daily series is error-prone (easily prints ancient history).
- EFFR/SOFR **daily volume** is not in FRED — take it from the NY Fed pages (below).
- A wrong series ID returns an HTML page; sanity-check `tail -1` is a `date,value` pair before trusting anything.

### Known-good free sources

| Need | Source |
|---|---|
| Meeting-by-meeting hike/cut probabilities (Fed & ECB) | `rateprobability.com/fed` and `rateprobability.com/ecb` — implied post-meeting rate, hike/cut probability, # of hikes, Δbp per meeting. Best free FedWatch alternative. |
| EFFR / SOFR latest print + volume | `newyorkfed.org/markets/reference-rates/effr` (…`/sofr`) — table has a VOLUME column |
| EURIBOR fixings (1W–12M) | `euribor-rates.eu/en/current-euribor-rates` |
| CME futures specs / quotes / settlements | `cmegroup.com/markets/interest-rates/stirs/three-month-sofr.contractSpecs.html`, `.quotes.html`, `.settlements.html` — fetch via `r.jina.ai/<url>` |
| Futures margin estimates | broker help pages (e.g. `help.metrotrade.com/kb/three-month-sofr-futures-sr3-contract-specifications` gives IM/MM ranges). CME's own margin API (`CmeWS`) returns HTTP 422 — don't rely on it. |
| FOMC statement + SEP projections | `federalreserve.gov/monetarypolicy/fomcprojtablYYYYMMDD.htm` — grep the tables (`| Federal funds rate | 3.8 | ...`), note medians 2026/2027/2028/longer-run |
| CPI / payrolls | `bls.gov/news.release/cpi.nr0.htm` — grep `"increased X percent over the last 12 months"` for the y/y |
| ECB statements & pressers | `ecb.europa.eu/press/govcdec/mopo/html/ecb.mpYYMMDD.en.html` via r.jina.ai |

Routing quirks: the ECB data portal / SDW often blocks automated curl (HTTP 400 security block) — use aggregators instead; investing.com blocks anonymous fetches (403 abuse) — avoid; JS-heavy pages (Barchart, TradingView) are unreliable even via r.jina.ai.

### Parallel research subagents (news / outlook layer)

Dispatch 2–3 leaf subagents for the qualitative layer (central-bank decisions, sell-side views, market pricing) and give each: today's date, the **already-verified baseline facts** (so they don't re-derive or contradict you), exact questions, and the hard rule *"every number MUST come from a URL you actually fetched; mark anything unverifiable UNVERIFIED; never guess from memory"*. Ask for a compact markdown brief with source URLs. Delegate the futures-quotes/margins task and the policy/outlook tasks separately so one slow fetch doesn't block the rest.

**Timeout recovery**: a research subagent can hit the 600s timeout and still have done the work — its fetched files persist in `/tmp/` and its tool results stream to `~/.hermes/cache/delegation/live/<id>/task-N.log`. Grep/tail those to recover quotes, specs and margins instead of re-fetching.

## Intraday Market Data (1-min OHLCV)

### Data Format

CSV files with columns: `date`, `open`, `high`, `low`, `close`, `volume`
- date format: `YYYY-MM-DD HH:MM:SS` (1-minute bars)
- Data range: typically 2015-01 to 2024-01 for Nifty 50 stocks
- ~76M rows for 96 tickers × 9 years × 375 bars/day

### Recommended Storage: Dual-DB Architecture

Use two databases for comparison: **DuckDB** (time-series columnar) and **MongoDB** (NoSQL document).

This creates a clean benchmark structure for assignments that ask for performance analysis.

#### DuckDB Schema

```sql
CREATE TABLE intraday (
    ticker    VARCHAR,
    timestamp TIMESTAMP,
    open      DOUBLE,
    high      DOUBLE,
    low       DOUBLE,
    close     DOUBLE,
    volume    BIGINT
);
-- Compound index for ticker+time range scans
CREATE INDEX idx_ticker_ts ON intraday (ticker, timestamp);
CREATE INDEX idx_ts ON intraday (timestamp);
```

#### MongoDB Document

```json
{
  "_id": "RELIANCE_2023-06-01 09:15:00",
  "ticker": "RELIANCE",
  "timestamp": "2023-06-01 09:15:00",
  "open": 2348.5, "high": 2352.3, "low": 2347.1, "close": 2350.6, "volume": 104030
}
```

Indexes:
```python
col.create_index([("ticker", 1), ("timestamp", 1)], unique=True)
col.create_index("timestamp")
```

### Ingestion Optimization (Large Datasets ~76M rows)

**CRITICAL — do NOT insert row-by-row with Python loops.** The naive approach takes 10+ minutes per DB.

#### DuckDB: Use native CSV reader (fastest path)

Extract CSV from zip → use DuckDB's `read_csv_auto` directly:

```python
import duckdb, zipfile, tempfile
from pathlib import Path

con = duckdb.connect("intraday.duckdb")

# Create table first, then bulk insert from CSV
con.execute("""
    INSERT INTO intraday
    SELECT '{ticker}', CAST(date AS TIMESTAMP),
           CAST(open AS DOUBLE), CAST(high AS DOUBLE),
           CAST(low AS DOUBLE), CAST(close AS DOUBLE),
           CAST(volume AS BIGINT)
    FROM read_csv_auto('{csv_path}', header=true)
""")
```

This processes ~800K rows per file in ~1 second vs 10+ seconds with Python executemany.

**⚠️ DuckDB memory tuning** — When creating indexes on 76M rows, the default config may OOM:

```python
con.execute("PRAGMA memory_limit='6GB'")
con.execute("PRAGMA threads=4")
con.execute("CREATE INDEX idx_ticker_ts ON intraday (ticker, timestamp)")
```

If still OOM: reduce threads further (`PRAGMA threads=2`) and set `PRAGMA preserve_insertion_order=false`.

#### MongoDB: Bulk writes with large batches

Use `bulk_write` with `ordered=False` and batch size of 20,000:

```python
from pymongo import InsertOne

BATCH_SIZE = 20000
batch = []
for row in reader:
    batch.append(InsertOne({...}))
    if len(batch) >= BATCH_SIZE:
        col.bulk_write(batch, ordered=False)
        batch = []
if batch:
    col.bulk_write(batch, ordered=False)
```

### Performance Benchmarking

#### Typical Results (76M rows, Apple M1, 16GB)

| Query Pattern | DuckDB | MongoDB | Ratio |
|---------------|--------|---------|-------|
| 15-min slice (16 rows) | 0.7 ms | 0.7 ms | 1.0x |
| 1 day (375 rows) | 0.9 ms | 1.7 ms | 1.9x |
| 1 month (7,875 rows) | 5.1 ms | 23.4 ms | 4.6x |
| 1 year (92K rows) | 40.8 ms | 149.6 ms | 3.7x |
| 5 tickers × 1 day | 2.2 ms | 10.6 ms | 4.9x |
| 10 tickers × 1 day | 4.2 ms | 14.0 ms | 3.3x |

DuckDB is 1–5x faster for time-series range queries. The gap widens with data volume.

#### Benchmark Methodology

1. Warm cache (query once before timing)
2. Each query: 5 runs, report avg/min/max
3. Measure server-side wall clock time
4. Cover: single/multi-ticker, narrow/broad time ranges, field subsetting

See `references/intraday-dual-db-benchmark.md` for the full benchmark script and results.

### REST API (FastAPI)

Unified query endpoint for both databases:

```http
GET /api/{duckdb|mongodb}/query?tickers=RELIANCE,HDFCBANK&start=2023-06-01 09:15:00&end=2023-06-30 15:30:00&fields=close,volume
```

Response:
```json
{
  "db": "duckdb",
  "tickers": ["RELIANCE"],
  "start": "2023-06-01 09:15:00",
  "end": "2023-06-01 15:30:00",
  "fields": ["close", "volume"],
  "count": 375,
  "elapsed_ms": 0.9,
  "data": [{"ticker": "RELIANCE", "timestamp": "2023-06-01T09:15:00", "close": 2350.6, "volume": 104030}]
}
```

## MongoDB Pipeline (for large-scale daily data storage)

Document schema:
```json
{
  "_id": "600000_2020-01-02",
  "code": 600000,
  "date": "2020-01-02",
  "open": 12.47,
  "high": 12.64,
  "low": 12.35,
  "close": 12.47,
  "volume": 51984000
}
```

**⚠️ CRITICAL — code type:** yfinance stores `code` as `int` in MongoDB, not `string`. When querying from Flask API, the query param comes as string — convert explicitly:

```python
code = int(request.args.get("code"))  # not str
```

Indexes:
```python
collection.create_index([("code", 1), ("date", -1)], unique=True)
collection.create_index("code")
collection.create_index("date")
```

### REST API (Flask + MongoDB)

```python
@app.route("/api/daily")
def query():
    code = int(request.args.get("code"))
    start = request.args.get("start")
    end = request.args.get("end")
    cursor = col.find(
        {"code": code, "date": {"$gte": start, "$lte": end}},
        {"_id": 0},
        sort=[("date", 1)],
    )
    return jsonify({"code": code, "count": len(data), "data": data})
```

### Update Script Pattern

**DO NOT** iterate 2308 stocks one-by-one with `find_one`. Use MongoDB aggregation to find stale stocks in one query:

```python
pipeline = [
    {"$group": {"_id": "$code", "last_date": {"$max": "$date"}}},
    {"$match": {"last_date": {"$lt": today}}},
]
need_update = [doc["_id"] for doc in col.aggregate(pipeline)]
```

Then batch-download only stale stocks with `yf.download(need_update_tickers, ...)`. This completes in seconds instead of minutes.

## Multi-Market Index & Stock Data (AKShare)

For quick market overviews across A-shares, Hong Kong, US, and Korea — where precision matters more than latency — use AKShare directly. It is more reliable than the thsdk guest account for multi-market cross-sections.

### A-Share Indices

```python
import akshare as ak

indices = {
    "上证指数": "sh000001",
    "深证成指": "sz399001",
    "沪深300": "sh000300",
    "创业板指": "sz399006",
}
for name, code in indices.items():
    df = ak.stock_zh_index_daily(symbol=code)
    df = df.reset_index()
    last = df.iloc[-1]
    prev = df.iloc[-2]
    close = float(last["close"])
    chg = close - float(prev["close"])
    pct = (chg / float(prev["close"])) * 100
    print(f"{name}: {close:.2f}  {chg:+.2f} ({pct:+.2f}%)")
```

Returns DataFrame with columns: `date`, `open`, `high`, `low`, `close`, `volume`.

### Hong Kong Indices

```python
# 恒生指数
df = ak.stock_hk_index_daily_em(symbol="HSI")
# 国企指数
df = ak.stock_hk_index_daily_em(symbol="HSCEI")
# Returns: index, date, open, high, low, latest
```

### US Indices

```python
df = ak.index_global_spot_em()  # all global indices in one query
us = df[df["名称"].isin(["标普500", "纳斯达克", "道琼斯"])]
# Columns: 名称, 最新价, 涨跌额, 涨跌幅, 开盘价, 最高价, 最低价, 昨收价
```

For individual US stock daily history:
```python
df = ak.stock_us_daily(symbol="AAPL", adjust="qfq")
```

### Korea KOSPI

```python
df = ak.index_global_spot_em()
kos = df[df["名称"] == "韩国KOSPI"]
```

### US Tech Sector Basket (sub-sector drill-down)

```python
import time
for ticker in ["NVDA", "AMD", "TSM", "INTC", "MU", "QCOM"]:
    df = ak.stock_us_daily(symbol=ticker, adjust="qfq").reset_index()
    last, prev = df.iloc[-1], df.iloc[-2]
    close, prev_close = float(last["close"]), float(prev["close"])
    print(f"{ticker}: ${close:.2f}  {close-prev_close:+.2f} ({(close/prev_close-1)*100:+.2f}%)")
    time.sleep(0.5)

# AVOID stock_us_spot_em() for bulk — loads 5500+ stocks via tqdm, times out
# in non-interactive shells.
```

See `references/akshare-multi-market-apis.md` for the full market → function → symbol → columns mapping.

## Pitfalls

| Pitfall | Mitigation |
|---|---|
| Kaggle 403 / empty page | Use yfinance fallback or KaggleHub (no browser required) |
| Conda/python path interference in background jobs | Use explicit `/usr/local/bin/python3` or `CONDA_NO_PLUGINS=true` |
| yfinance missing EBITDA for Financials sector | Filter NaN before returning; don't error out |
| CSV filename with `&` breaks shell quoting | Wrap filename in double quotes or escape |
| yfinance `financials` may be None for delisted/ETF symbols | Wrap in try/except and assign empty string |
| AKShare rate limit on bulk historical fetch | Add `time.sleep(0.3)` between stock queries; expect ~12 min for 2308 stocks |
| MongoDB not installed | `brew install mongodb-community` or `docker run -d -p 27017:27017 --name mongo mongo:7` |
| AKShare API changes | Verify with `python -c "import akshare; print(akshare.__version__)"` before heavy runs |
| **yfinance `Remote end closed connection`** | Shell `http_proxy` breaks yfinance. Add `os.environ.pop('http_proxy', None)` at script top |
| **MongoDB code stored as int, API param is string** | Flask API needs `code = int(request.args.get("code"))` |
| **2308 sequential find_one queries timeout** | Use MongoDB `aggregate` with `$group` + `$max` instead |
| **thsdk guest account: market_data_index returns empty, market_data_us returns "?"** | Fall back to AKShare for index-level data and US stocks. thsdk guest (no login) cannot read US stock data or most indices — only basic A-share klines work. |
| **AKShare `stock_us_spot_em()` times out in headless env** | Use `stock_us_daily(symbol=..., adjust="qfq")` per ticker instead; add `time.sleep(0.5)` between calls. |
| **AKShare `stock_hk_index_daily_em` has tqdm progress bar** | Non-blocking in foreground; set generous timeout (30s+). |
| **DuckDB OOM on large index creation** | Set `PRAGMA memory_limit='6GB'; PRAGMA threads=4` before CREATE INDEX. If still OOM: reduce to 2 threads, set `preserve_insertion_order=false`. |
| **DuckDB row-by-row insert is slow for 76M rows** | Use `read_csv_auto` for bulk import from CSV files — 100x faster than Python executemany. |
| **Background processes use different Python than foreground** | Always use explicit `/usr/local/bin/python3` (or system Python path) in `background=true` commands, never rely on `python3` resolving to the same binary. |
| **Wrong FRED series ID returns an HTML page** | Check `tail -1` is `date,value`; use exact IDs (EFFR, SOFR, DFEDTARU/L, DGS*, T10Y2Y, ECBDFR, WFII10) |
| **ECB data portal / SDW blocks automated curl** | Route to rateprobability.com, euribor-rates.eu, tradingeconomics, or ECB press pages via r.jina.ai |
| **investing.com 403 on anonymous fetch** | Use euribor-rates.eu / BLS / rateprobability instead |
| **CME margin API (CmeWS) returns 422** | Use broker help pages for IM/MM estimates; label them as broker estimates, not exchange figures |
| **Research subagent timeout ≠ lost work** | Recover from `/tmp` files + `~/.hermes/cache/delegation/live/<id>/task-N.log` transcripts |

## References

- [S&P 500 constituents dataset (GitHub)](https://github.com/datasets/s-and-p-500-companies)
- [yfinance documentation](https://github.com/ranaroussi/yfinance)
- [GICS sector classification](https://www.msci.com/our-solutions/indexes/gics)
- [AKShare documentation](https://akshare.akfamily.xyz/)
- [KaggleHub](https://github.com/Kaggle/kagglehub)
- [DuckDB documentation](https://duckdb.org/docs/)
- [references/akshare-multi-market-apis.md](references/akshare-multi-market-apis.md)
- [references/intraday-dual-db-benchmark.md](references/intraday-dual-db-benchmark.md)
- [references/rates-data-sources.md](references/rates-data-sources.md) — full rates source playbook: exact URLs, series IDs, what each returns, fetch quirks
