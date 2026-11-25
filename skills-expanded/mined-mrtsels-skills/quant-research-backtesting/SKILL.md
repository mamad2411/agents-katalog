---
name: quant-research-backtesting
description: End-to-end quantitative research workflow — data provisioning (yfinance), MongoDB storage, correlation/clustering, cointegration testing, and rolling backtest with no look-ahead bias. Covers Asian market quirks (SSE ticker format, proxy issues).
version: 1.1.0
---

# Quant Research & Backtesting Workflow

Patterns for building and backtesting quantitative trading strategies on Asian equity markets (SSE, SZSE). Written for the specific quirks of the China A-share market.

## Data Provisioning

### yfinance for SSE Stocks

SSE tickers require `.SS` suffix (e.g. `600000.SS`). SZSE uses `.SZ`.

**Proxy issue on macOS:** The shell environment often has `http_proxy` / `https_proxy` set. yfinance's requests library will try to route through the proxy and fail silently. **Always clear proxies at the top of the script:**

```python
import os
os.environ.pop('http_proxy', None)
os.environ.pop('https_proxy', None)
```

**Batch download (fast, preferred):**

```python
import yfinance as yf

tickers = ['600000.SS', '600004.SS', ...]
data = yf.download(tickers, start="2010-01-01", group_by="ticker",
                   threads=False, progress=False)
# Columns: MultiIndex (Ticker, Price)
# Access: data.get(('600000.SS', 'Close'), pd.Series(dtype=float))
```

**Single ticker (fallback for clean extraction):**

```python
hist = yf.Ticker(yf_ticker).history(start="2010-01-01")
# Returns single-level columns: Open, High, Low, Close, Volume, Dividends, Stock Splits
```

**SSE stock list** — yfinance has no stock screening. Use AKShare once and cache:

```python
import akshare as ak
all_stocks = ak.stock_info_a_code_name()
sse = all_stocks[all_stocks['code'].str.startswith('6')]
sse['yf_ticker'] = sse['code'] + '.SS'
sse.to_csv('sse_stocks.csv', index=False)
```

### Reshape yfinance returns to flat records

```python
records = []
for date, row in hist.iterrows():
    records.append({
        "code": code, "date": date.strftime("%Y-%m-%d"),
        "open": float(row.get("Open", 0)),
        "high": float(row.get("High", 0)),
        "low": float(row.get("Low", 0)),
        "close": float(row.get("Close", 0)),
        "volume": int(row.get("Volume", 0)),
    })
```

## MongoDB Storage Patterns

### Batch insert with ordered=False (skip duplicates)

```python
from pymongo import MongoClient, InsertOne

ops = [InsertOne({"_id": f"{code}_{date}", **r}) for r in records]
col.bulk_write(ops, ordered=False)
# ordered=False: skips duplicates, continues on error
```

### Bulk update (for incremental updates)

```python
from pymongo import UpdateOne

ops = [UpdateOne({"_id": f"{code}_{date}"}, {"$set": r}, upsert=True) for r in records]
col.bulk_write(ops, ordered=False)
```

### Efficient price matrix loading

**Don't query one stock at a time** — use aggregation pipeline:

```python
pipeline = [
    {"$match": {"code": {"$in": codes}, "date": {"$gte": start, "$lte": end}}},
    {"$sort": {"code": 1, "date": 1}},
    {"$project": {"code": 1, "date": 1, "close": 1, "_id": 0}},
]
data = list(col.aggregate(pipeline, allowDiskUse=True))
df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])
pivot = df.pivot_table(index="date", columns="code", values="close")
```

### Column type pitfall

pivot_table with int codes returns **int64 columns**, not strings. Access via integer key:

```python
# CORRECT:
y1 = pivot[600000].values

# WRONG — KeyError:
y1 = pivot["600000"].values

# When column keys come from CSV or variable, ensure type consistency:
col_map = {c: pivot.columns.get_loc(c) for c in codes}
value = pivot.iloc[t, col_map[c1]]
```

## Correlation & Clustering

### Pearson correlation on log returns

```python
returns = np.log(prices / prices.shift(1)).dropna()
corr = returns.corr().values
```

### Distance matrix for clustering

```python
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import linkage, fcluster

dist = squareform(np.clip(1 - corr, 0, 2))  # d = 1 - r, clamped to [0, 2]
Z = linkage(dist, method="ward")
labels = fcluster(Z, t=K, criterion="maxclust")
```

### Cointegration threshold

Correlation > 0.3 for filtering before cointegration test. Lower threshold (0.3) finds more pairs than default 0.5. Two-year training window with 485+ data points is usually sufficient for ADF.

## Rolling Backtest (no look-ahead bias)

### Structure

```
for each year (2017, 2018, ..., 2025):
    train: 2 years prior  (fit alpha, beta, find cointegrated pairs)
    test:  1 year forward  (execute trades)
```

### Trade logic

- Entry: Z-score crosses ±2.0
- Exit: Z-score returns within ±1.0, OR |Z| > 3.0 for 5+ days (stop-loss)
- Position sizing: 2% of capital per pair, max 20 concurrent pairs
- Cost: 0.13% per trade (commission 0.03% + stamp tax 0.1%, SSE-only sell side)

### PnL calculation for pair trades

```python
# Spread return from entry to exit:
spread_return = ((y1_exit - beta * y2_exit) - (y1_entry - beta * y2_entry)) / y1_entry

# Multiply by position direction and capital:
trade_pnl = per_pair * spread_return * direction - per_pair * COST
```

### Risk management pitfalls

- **Look-ahead bias:** Never train and test on overlapping data. Use rolling windows.
- **Parameter overfitting:** Fix Z-score thresholds at ±2.0 (Lecture 13 standard), do not optimize.
- **Zero-crossing filter:** Among cointegrated pairs, prefer those with higher zero-crossings (more trading opportunities).
- **SSE short-selling constraints:** Real-world SSE has limited short-selling availability. The backtest assumes full short access.

## Known Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| yfinance hangs | Script hangs at `yf.download()` | Clear http_proxy/https_proxy env vars |
| MongoDB aggregation fails | `Unrecognized pipeline stage name: ''` | Avoid `$` inside f-strings; use raw dicts |
| pandas 3.x iloc bracket order | SyntaxError | `iloc[row_range, col_idx]` not `iloc[row_range, col_idx)` |
| Code stored as int in MongoDB, queried as string | `/api/daily` returns 0 records | `code = int(request.args.get("code"))` |
| Column mismatch in pivot table | KeyError with int vs string key | Use `col_map` dict + `iloc` positional access |
