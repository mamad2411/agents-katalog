---
name: pandas-datareader
description: "Multi-source financial data reader: FRED, World Bank, OECD, Eurostat, St. Louis Fed, Yahoo, Google, and more. Standard interface for economic and financial time series data ingestion."
tags: [financial-data, economic-data, fred, world-bank, time-series, python, zorai]
---
## Overview

pandas-datareader provides a unified interface for reading economic and financial time series from multiple sources: FRED (Federal Reserve), World Bank, OECD, Eurostat, Yahoo Finance, and St. Louis Fed. Standard tool for macroeconomic data ingestion.

## Installation

```bash
uv pip install pandas-datareader
```

## FRED Data

```python
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020, 1, 1)
gdp = web.DataReader("GDP", "fred", start)
unemp = web.DataReader("UNRATE", "fred", start)
cpi = web.DataReader("CPIAUCSL", "fred", start)
fedfunds = web.DataReader("FEDFUNDS", "fred", start)
ten_year = web.DataReader("DGS10", "fred", start)

import pandas as pd
combined = pd.DataFrame({"GDP": gdp["GDP"], "CPI": cpi["CPIAUCSL"], "FedFunds": fedfunds["FEDFUNDS"]})
print(combined.tail())
```

## World Bank

```python
gdp_pc = web.DataReader("NY.GDP.PCAP.CD", "worldbank", start=2015)
```

## References
- [pandas-datareader docs](https://pandas-datareader.readthedocs.io/)
- [FRED API](https://fred.stlouisfed.org/docs/api/fred/)