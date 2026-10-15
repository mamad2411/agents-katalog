---
name: finhay-market
description: "Stock prices, commodities, macro indicators, charts, and company financials. Use for market analysis, price lookups, and corporate performance data."
license: MIT
metadata:
  author: Finhay Securities
  version: "2.0.0"
---

# Finhay Market

Read-only market data via the Finhay Securities Open API.

> **MANDATORY**: Ensure credentials are set (via environment variables `FINHAY_API_KEY`/`FINHAY_API_SECRET` or via `./finhay.sh auth`). Run `./finhay.sh doctor` to verify.

## Usage Examples

```bash
# Get real-time stock quote
./finhay.sh request GET /market/stock-realtime "symbol=VNM"

# Get gold spot price
./finhay.sh request GET /market/financial-data/gold

# Get historical OHLCV chart data
./finhay.sh request GET /market/price-histories-chart "symbol=VNM&resolution=1D&from=1609459200&to=1704067200"
```

## CLI Command Reference

| Command | Description |
|---------|-------------|
| `auth` | Configure API credentials interactively |
| `doctor` | Verify system dependencies and setup status |
| `request` | Execute signed API requests |
| `sync` | Update local skill definitions from source |

## Endpoints

| Endpoint | Description | Params |
|----------|-------------|--------|
| `/market/stock-realtime` | **Stock Quotes**: Real-time pricing for symbols or exchanges. | `symbol`, `symbols`, or `exchange` |
| `/market/news` | **Market News**: Corporate events, dividends, and AGM dates. | `stock`, `from_date`, `to_date` |
| `/market/financial-data/gold` | **Gold Prices**: Real-time SJC and global gold spot prices. | — |
| `/market/financial-data/silver` | **Silver Prices**: Real-time silver spot prices. | — |
| `/market/financial-data/gold-chart` | **Gold Charts**: Historical gold price data for N days. | `days` |
| `/market/financial-data/silver-chart` | **Silver Charts**: Historical silver price data for N days. | `days` |
| `/market/financial-data/gold-providers` | **Gold by Provider**: Gold prices from PNJ, DOJI, SJC, etc. | — |
| `/market/financial-data/metal-providers` | **Metals by Provider**: Silver and other metal prices by provider. | — |
| `/market/financial-data/bank-interest-rates` | **Interest Rates**: Current bank deposit rates. | — |
| `/market/financial-data/cryptos/top-trending` | **Crypto Trends**: List of trending cryptocurrencies. | — |
| `/market/financial-data/macro` | **Macro Indicators**: CPI, PMI, and national interest rates. | `type`, `country` (`VN`,`US`; `JP`,`DE` only for `GOVERNMENT_10Y_BOND_YIELD`), `period` |
| `/market/financial-data/trading-economics` | **Trading Economics**: Historical economic indicators by country and category. | `country` (**required**: `China`, `Euro Area`, `Japan`, `United States`, `United Kingdom`, `Vietnam`), `category` (`GDP`, `Labour`, `Prices`, `Money`, `Trade`, `Government`, `Business`, `Consumer`, `Housing`), `year` |
| `/market/financial-data/economic-calendar-events` | **Economic Calendar**: Upcoming events for CN/EU/JP/US/UK/VN (CPI, Fed meetings). | `weeks` (default 1), `country` (e.g. `China`, `Vietnam`, `United States`) |
| `/market/financial-data/market` | **Global Indices**: Historical price for global indices, Mag7 stocks, commodities, forex — returns `[{date, value}]` desc. | `type` (SP500, NASDAQ, APPLE, GOLD, EURUSD…), `limit` (default 50, max 500) |
| `/market/funds` | **Fund List**: Available mutual funds and their basic info. | — |
| `/market/funds/:fund/portfolio` | **Fund Portfolio**: Holdings breakdown for a specific fund. | `:fund` (path), `month` |
| `/market/funds/:fund/months` | **Fund Months**: Available portfolio reporting months. | `:fund` (path) |
| `/market/recommendation-reports/:symbol` | **Analyst Reports**: Professional stock recommendation reports. | `:symbol` (path) |
| `/market/price-histories-chart` | **Historical Data**: OHLCV data. | `symbol`, `resolution` (`1D`,`1H`,`4H`,`30`,`15`,`5`), `from`, `to` (seconds) |
| `/market/company-financial/overview` | **Corporate Ratios**: Key metrics (PE, PB, ROE, EPS). | `symbol` |
| `/market/company-financial/analysis` | **Financial Analysis**: Ratio trends. | `symbol`, `period` (`annual`,`quarterly`) |
| `/market/v2/financial-statement/statement` | **Financial Reports**: Income/Balance/Cash flow. | `symbol`, `type` (`income-statement`,`balance-sheet`,`cash-flow`), `period` (`annual`,`quarterly`) |

## Constraints

- **Read-only**: Execute `GET` requests only.
- **Privacy**: Mask sensitive credentials in all output.
- **Credentials**: If `FINHAY_API_KEY` or `FINHAY_API_SECRET` are missing, stop and ask the user to provide them or run `./finhay.sh auth`.
- **Parameters**: Pass exactly one identifier for stock quotes (symbol, symbols, or exchange).
- **Timeframes**: Price history timestamps must be in **seconds**. Default to the last 5 years if range is not provided.
