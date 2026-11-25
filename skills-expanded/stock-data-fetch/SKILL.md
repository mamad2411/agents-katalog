---
name: stock-data-fetch
description: Fetch multi-market financial data — US (FMP→Finnhub), A/HK (Tencent→Sina), crypto (OKX→Hyperliquid), commodities (Hyperliquid+Finnhub), news (Marketaux), backup (Longbridge). Battle-tested in restricted network environments.
category: data-science
---

# Stock Data Fetch

> **关于 `snapshot` 命令**：下文的 `snapshot` 是一个**可选的本地封装脚本**（自己用 Python/shell 包一层多源 failover 即可），不是随仓库分发的二进制。不想写脚本也没关系——本文档把每个市场的**免 key 直连端点**都列出来了，直接 `curl` 就能用。所有需要 key 的源（FMP/Finnhub/Longbridge）请把 key 放进**环境变量**，不要写死在代码里。

## Quick Start

```bash
snapshot TICKER [--no-news] [--no-commit]
```

One command. All markets. Automatic failover.

## Data Sources

### US Stocks
1. **FMP** (primary) — quote, EV/EBITDA, FCF yield, growth rates, sector, beta, earnings
2. **Finnhub** (fallback) — PE/PB/ROE, 52-week range (fills gaps FMP free tier lacks)
3. **Longbridge** (backup) — 15min delayed, use only when FMP+Finnhub both fail

### A-Shares
1. **Tencent qt.gtimg.cn** — real-time, free, no key
2. **Sina hq.sinajs.cn** — fallback, needs Referer header

### HK Stocks
1. **Tencent qt.gtimg.cn** — real-time, free, no key
2. **Sina hq.sinajs.cn** — fallback
3. **Longbridge** (backup) — 15min delayed

### Cryptocurrency
1. **OKX** — real-time, 200+ pairs, no key
2. **Hyperliquid** — 7×24 perp prices, 230+ coins, no key
3. Binance blocked (HTTP 451) in this region — don't retry

### Commodities & Indices
1. **Hyperliquid** — PAXG (gold), SPX (S&P 500 perp)
2. **Finnhub futures** — CL=F (oil), SI=F (silver), NG=F (natgas), HG=F (copper)

### News
- **Marketaux** — entity-linked, sentiment-tagged

### Backup
- **Longbridge OpenAPI** — US/HK/China quotes, 15min delayed
- Keys: `LONGBRIDGE_APP_KEY`, `LONGBRIDGE_APP_SECRET`
- API base: `https://openapi.longbridge.cn`

## Verified Sources

| Source | Markets | Latency | Key Required |
|--------|---------|---------|-------------|
| FMP | US | Real-time | ✅ Free |
| Finnhub | US | Real-time | ✅ Free |
| Tencent qt | China A/HK | Real-time | ❌ None |
| Sina | China A/HK | Real-time | ❌ None |
| OKX | Crypto | Real-time | ❌ None |
| Hyperliquid | Crypto+Commodities | Real-time | ❌ None |
| Marketaux | News | Real-time | ✅ Free |
| Longbridge | US/HK/China | 15min delay | ✅ Account |

## Lessons Learned (Battle Scars)

### Never Use These (in this network)
- **yfinance** — rate limited + SSL errors. Hermes docs explicitly warn against it
- **akshare / akshare-one** — both call eastmoney.com which is proxy-blocked
- **Google News RSS** — guaranteed timeout
- **Binance** — HTTP 451 (legal block)

### API Format Pitfalls
- **FMP v3 API is DEPRECATED** since Aug 2025. Use `/stable/` endpoints. The error message is misleading
- **FMP key from before Aug 2025 is invalid** — must re-register for new key
- **Tencent qt returns GBK encoding**, not UTF-8. Must `decode("gbk")` or pipe through `iconv -f GBK`
- **HK stock codes on Tencent need 5 digits**: `zfill(5)` not `lstrip("0")`. `00700` → `hk00700` not `hk700`
- **Sina requires `Referer: https://finance.sina.com.cn`** header, or returns empty
- **Hyperliquid allMids uses PAXG for gold**, not HOLD/XAUT0. SPX exists but is a meme coin ticker
- **lark-oapi SDK requires builder pattern**: `CreateMessageRequest.builder()...build()`, direct construction silently fails

### Network Constraints
- `eastmoney.com` — proxy blocked (blocks akshare, akshare-one)
- `api.binance.com` — HTTP 451 (legal)
- `news.google.com` — timeout
- `yfinance` — SSL + rate limit
- `open.longbridge.com` — blocked; use `openapi.longbridge.cn` instead

### Performance
- `max_turns: 60` → agent loops forever. Reduce to 10 (research needs 4-6)
- `max_tokens: unlimited` → output too long. Cap at 8192
- Bot self-sent messages MUST be filtered by `sender_type in ("bot", "app")` or infinite echo loop

## CLI Commands

```bash
snapshot NVDA                    # Full: quote + fundamentals + earnings + news
snapshot NVDA --no-news          # Skip news (faster)
snapshot 600519.SH               # A-share
snapshot 00700.HK                # HK stock
snapshot BTC                     # Crypto
snapshot GOLD                    # Commodity
```

## Output Format

```json
{
  "ticker": "NVDA", "retrieved_at": "2026-04-29T10:00:00Z",
  "source_apis": ["fmp", "finnhub"],
  "data": {
    "quote": {"price": 213.17, "change_pct": 2.3},
    "fundamentals": {"pe_ttm": 42.7, "market_cap": 5181096612529},
    "earnings_latest": {"revenue": 215938000000, "net_income": 120067000000}
  }
}
```
