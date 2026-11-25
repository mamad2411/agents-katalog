---
name: Crypto Market Data
description: No API KEY needed for free tier. Professional-grade cryptocurrency market data integration for real-time prices, historical charts, and global analytics.
---

# 🪙 Crypto Market Data Skill

A comprehensive suite of tools for retrieving real-time and historical cryptocurrency market data. This skill interfaces with a dedicated market data server to provide high-performance, authenticated access to global crypto statistics.

## ✨ Key Capabilities

| Category | Description |
| :--- | :--- |
| **📉 Real-time Prices** | Fetch current valuations, market caps, 24h volumes, and price changes. |
| **🚀 Market Discovery** | Track trending assets and top-performing coins by market capitalization. |
| **🔍 Smart Search** | Quickly find coin IDs by searching names or ticker symbols. |
| **📑 Deep Details** | Access exhaustive asset information, from community links to developer metrics. |
| **📊 Precise Charts** | Retrieve OHLC candlestick data and historical price/volume time-series. |
| **🌍 Global Metrics** | Monitor total market capitalization and public company treasury holdings. |

## 🛠 Tool Reference

| Script Name | Primary Function | Command Example |
| :--- | :--- | :--- |
| `get_crypto_price.py` | Multi-coin price fetch | `python3 scripts/get_crypto_price.py bitcoin ethereum` |
| `get_trending_coins.py` | 24h trending assets | `python3 scripts/get_trending_coins.py` |
| `get_top_coins.py` | Market leaderboards | `python3 scripts/get_top_coins.py --per_page=20` |
| `search_coins.py` | Asset discovery | `python3 scripts/search_coins.py solana` |
| `get_coin_details.py` | Comprehensive metadata | `python3 scripts/get_coin_details.py ethereum` |
| `get_coin_ohlc_chart.py` | Candlestick data | `python3 scripts/get_coin_ohlc_chart.py bitcoin --days=7` |
| `get_coin_historical_chart.py` | Time-series data | `python3 scripts/get_coin_historical_chart.py bitcoin --days=30` |
| `get_global_market_data.py` | Macro market stats | `python3 scripts/get_global_market_data.py` |
| `get_public_companies_holdings.py` | Treasury holdings | `python3 scripts/get_public_companies_holdings.py bitcoin` |
| `get_supported_currencies.py` | Valuation options | `python3 scripts/get_supported_currencies.py` |
| `check_api_status.py` | Health monitoring | `python3 scripts/check_api_status.py` |

---

## 📖 Usage Details

### 1. `get_crypto_price.py`
Fetch real-time pricing and basic market metrics for one or more cryptocurrencies.

**Syntax:**
```bash
python3 scripts/get_crypto_price.py <coin_id_1> [coin_id_2] ... [--currency=usd]
```

**Parameters:**
- `coin_id`: The unique identifier for the coin (e.g., `bitcoin`, `solana`).
- `--currency`: The target currency for valuation (default: `usd`).

**Example:**
```bash
python3 scripts/get_crypto_price.py bitcoin ethereum cardano --currency=jpy
```

---

### 2. `get_top_coins.py`
Retrieve a list of the top cryptocurrencies ranked by market capitalization.

**Syntax:**
```bash
python3 scripts/get_top_coins.py [--currency=usd] [--per_page=10] [--page=1] [--order=market_cap_desc]
```

**Parameters:**
- `--currency`: Valuation currency (default: `usd`).
- `--per_page`: Number of results (1-250, default: `10`).
- `--order`: Sorting logic (e.g., `market_cap_desc`, `volume_desc`).

---

### 3. `get_coin_ohlc_chart.py`
Get Open, High, Low, Close (candlestick) data for technical analysis.

**Syntax:**
```bash
python3 scripts/get_coin_ohlc_chart.py <coin_id> [--currency=usd] [--days=7]
```

**Allowed `days` values:** `1, 7, 14, 30, 90, 180, 365`.

| Range | Resolution |
| :--- | :--- |
| 1-2 Days | 30 Minute intervals |
| 3-30 Days | 4 Hour intervals |
| 31+ Days | 4 Day intervals |

---

### 4. `get_coin_historical_chart.py`
Retrieve detailed historical time-series data for price, market cap, and volume.

**Syntax:**
```bash
python3 scripts/get_coin_historical_chart.py <coin_id> [--currency=usd] [--days=30]
```

---

## 💡 Important Guidelines

### 🆔 Use Coin IDs
Always use **Coin IDs** (slugs) instead of ticker symbols for accuracy:
- ✅ `bitcoin` (Not `BTC`)
- ✅ `ethereum` (Not `ETH`)
- ✅ `polkadot` (Not `DOT`)

Use `search_coins.py` if you are unsure of the correct ID.

### 🔐 Authentication
Authentication is handled **automatically** by the internal `api_client.py`. No manual API keys are required as the system manages short-lived session tokens internally to ensure optimal rate-limiting and security.

### 🚦 Rate Limiting
While the system is robust, please avoid burst requests (more than 30 per minute) to maintain service stability for all users.

### 🤖 Agent Integration
This skill is fully compatible with OpenClaw and other agents using the **AgentSkills** standard. Execute scripts directly from the `scripts/` directory.
