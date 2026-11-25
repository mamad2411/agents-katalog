---
name: tradingview-api-integration
description: Use when integrating with, troubleshooting, or querying the TradingView Data API on api.tradingviewapi.com (Console) or RapidAPI. Covers quotes, OHLCV, extended-hours candles and historical replay, option chains, ETF holdings and AUM, financial history and forecasts, screeners, economic observations, calendars, metadata, streaming, and hosted MCP tools. Also use for endpoint selection, parameter validation, or installing hosted TradingView MCP in Cursor, VS Code, Claude Code, Claude Desktop, Codex, Gemini CLI, or Windsurf.
---

# TradingView API Integration

Help developers integrate the TradingView Data API and answer data questions by calling it live.

Two access methods, same data:

1. **Hosted MCP** (`tradingview_*` tools) — prefer this when those tools are already connected.
2. **REST** — Console `https://api.tradingviewapi.com` or RapidAPI. Use `scripts/tv_api.py`.

**Recommended REST (Console)**

- Base URL: `https://api.tradingviewapi.com`
- Auth: `Authorization: Bearer <KEY>`
- Get a key at https://console.tvapis.com/start
- The official CLI also supports browser OAuth via `tvapi login`. Its `market:read` access token is for supported REST data operations. Use a Console API key for streaming or MCP token generation.

On Console, HTTP 402 with `code: "monthly_quota_exhausted"` means the account has used its quota for the billing period. An OAuth login and an API key on the same account share that quota. HTTP 429 with `code: "rate_limit_exceeded"` is a short-term limit. Honor the `Retry-After` header when present.

**Alternate REST (RapidAPI)**

- Base URL: `https://tradingview-data1.p.rapidapi.com`
- Auth: `x-rapidapi-host: tradingview-data1.p.rapidapi.com` and `x-rapidapi-key: <KEY>`
- Console and RapidAPI keys are billed separately. Paths after the host are the same.

Prefer Console for new integrations and generated examples. Use RapidAPI only when the user already has a RapidAPI subscription or asks for it.

## Choose MCP vs REST

If hosted tools named `tradingview_*` are available in this session, call those tools directly. Do not mint a JWT and do not use `scripts/tv_api.py` unless MCP cannot express the request.

Use REST for candle `replay`, `currency`, `backadjustment`, and `strictTo`. Both transports support `session=extended` on intraday candles where available. MCP OHLCV accepts up to 5,000 bars and optional `summary`. MCP chart-style Price accepts up to 500 bars.

To reconstruct what a strategy could see mid-candle, pass `replay` in Unix seconds with a positive `range` and omit `from` and `to`. Replay returns standard Japanese candles. To page backward through ordinary history, use `to` and add `strictTo=true` when the cutoff is close to the current time.

Other REST-only operations include `GET /api/symbols`, logo, streaming tokens, SSE, WebSocket, health, news `sector` filters, search `hl` / `exchange` / `enable_grouping`, and related-asset `start` / `count`.

When the user asks how to **install or configure MCP**, or `tradingview_*` tools are missing, read **[references/mcp-install.md](references/mcp-install.md)** and give **only the section for their IDE** (Cursor, VS Code, Claude Code, Claude Desktop, Codex, Gemini, Windsurf). If the client is unknown, ask. Do not dump every block. JWT / RapidAPI local details: **[references/examples/10-mcp.md](references/examples/10-mcp.md)**. Tool names: **[references/mcp-tools.md](references/mcp-tools.md)**.

- Hosted URL: `https://mcp.tradingviewapi.com/mcp` with `"type": "http"`. Sign in with Console. Do not put an API key on that URL.
- Plans: Basic (testing), Ultra / Mega (production). **Pro does not include MCP**.
- One-click page: https://www.tradingviewapi.com/mcp/

## API key workflow (REST only)

`scripts/tv_api.py` defaults to Console. It resolves the key in this order:

1. `--key` CLI argument
2. `TRADINGVIEW_API_KEY` environment variable
3. `RAPIDAPI_KEY` environment variable (legacy RapidAPI)
4. `.api-key` file in this skill's root directory
5. `.rapidapi-key` file in this skill's root directory (legacy)

If the only available key came from `RAPIDAPI_KEY` or `.rapidapi-key`, the script uses the RapidAPI host automatically. `--backend console|rapid` or `--rapid` overrides that.

If none is available, ask the user for a Console API key.

When the user provides a key, ask whether to save it for future sessions. **Only after explicit consent**, save it:

```bash
python3 scripts/tv_api.py --save-key 'THE_KEY'
```

This writes `.api-key` (chmod 600) to the skill root so future calls need no key prompt.

## Making live REST requests

Use `scripts/tv_api.py` (stdlib only, handles key resolution and JSON pretty-printing):

```bash
python3 scripts/tv_api.py GET '/api/quote/NASDAQ:AAPL'
python3 scripts/tv_api.py GET '/api/options/NASDAQ:AAPL?expiration=2026-12-18'
python3 scripts/tv_api.py GET '/api/etf/AMEX:SPY?limit=20'
python3 scripts/tv_api.py GET '/api/price/ohlcv/NASDAQ:AAPL?timeframe=5&session=extended&range=100&summary=true'
python3 scripts/tv_api.py GET '/api/price/ohlcv/BINANCE:BTCUSDT?timeframe=1&replay=1795065570&range=3'
python3 scripts/tv_api.py POST '/api/screener/scan' --body '{"symbols":["NASDAQ:AAPL","BINANCE:BTCUSDT"],"fields":["close","RSI|60"]}'
python3 scripts/tv_api.py POST '/api/screener/scan' --body '{"market":"america","range":[0,20],"filters":{"market_cap_basic":{"operation":"greater_or_equal","value":1e10}}}'
python3 scripts/tv_api.py --rapid GET '/api/quote/NASDAQ:AAPL'
```

Equivalent Console curl:

```bash
curl --location 'https://api.tradingviewapi.com/api/quote/NASDAQ:AAPL' \
  --header 'Authorization: Bearer YOUR_API_KEY'
```

## Choosing the right endpoint

Map the user's need to an endpoint family. MCP names in parentheses.

| User wants | Endpoint(s) | Example file |
|------------|-------------|--------------|
| Find a symbol / "what's the ticker for X" | `GET /api/search/market/{query}` (`tradingview_search_market`) | `03-market-search.md` |
| Browse the symbol catalog | `GET /api/symbols?q=&exchange=&type=` (REST only) | catalog |
| Current price, change, volume | `GET /api/quote/{symbol}` or `POST /api/quote/batch` (≤10) (`tradingview_get_quote` / `_batch`) | `02-quote-data.md` |
| Option chain (expiries, strikes, OPRA codes) | `GET /api/options/{symbol}?expiration=` (`tradingview_get_options`) — then quote the contract | `18-options.md` |
| ETF AUM, NAV, holdings | `GET /api/etf/{symbol}?limit=` (`tradingview_get_etf`) — not `market-data/.../related/etfs` | `19-etf.md` |
| Real Japanese OHLCV | `GET /api/price/ohlcv/{symbol}` or `POST /api/price/ohlcv/batch` (`tradingview_get_ohlcv` / `_batch`) | `01-price-data.md` |
| Heikin-Ashi / Range chart candles | `GET /api/price/{symbol}?type=HeikinAshi\|Range` (`tradingview_get_price`). Ordinary Price requests default to HeikinAshi. | `01-price-data.md` |
| Earnings / dividend / split markers | `GET /api/price/{symbol}/events` (`tradingview_get_price_events`) | catalog |
| Buy/Sell signals, RSI, MACD | `GET /api/ta/{symbol}` or `/api/ta/{symbol}/indicators?interval=` (`tradingview_get_ta`) | `04-technical-analysis.md` |
| Company profile, PE, financials, forecast, related bonds/ETFs | `GET /api/market-data/{symbol}/...` (`tradingview_get_market_data` `category`) | `12-market-data.md` |
| Financial metrics, fiscal-period rows, analyst consensus | `GET /api/market-data/{symbol}?view=financials`, `/history-quarterly` or `/history-annual` with `format=rows`, `/forecast?format=normalized` (`tradingview_get_financials`, `tradingview_get_financial_history`, `tradingview_get_forecasts`) | `12-market-data.md` |
| Top gainers/losers, rankings | `GET /api/leaderboard/{stocks\|crypto\|etfs\|forex\|futures\|indices\|bonds\|corporate-bonds}` (`tradingview_get_leaderboard`) | `05-leaderboards.md` |
| Custom filtering | `POST /api/screener/.../scan` (`tradingview_screen_assets`) | `16-screener.md` |
| Raw fields for known symbols | `POST /api/screener/scan` with `symbols` and `fields` (`tradingview_get_symbol_data` or `tradingview_get_symbol_data_batch` with `columns`) | `16-screener.md` |
| News | `GET /api/news?paginate=true&limit=20&offset=0` pages through up to 200 recent headlines. Detail via `GET /api/news/{newsId}` (`tradingview_get_news` / `_detail`). | `06-news.md` |
| Trading ideas / community sentiment | `GET /api/ideas/hot`, `/editors-picks`, `/list/{symbol}`, `/{symbol}/minds` (`tradingview_get_ideas_*` / `_minds`) | `13-ideas.md` |
| Earnings / IPO / dividend / macro dates | `GET /api/calendar/{earnings\|ipo\|revenue\|economic}?from=&to=` (Unix seconds, ≤40-day window) (`tradingview_get_calendar`) | `08-calendar.md` |
| Events for a watchlist or filtered economic releases | Add `symbols` to earnings/revenue, or `countries`, `currencies`, `category`, `min_importance` to economic. Dedicated MCP tools `tradingview_get_earnings_calendar`, `tradingview_get_dividends_calendar`, and `tradingview_get_economic_calendar` accept ISO dates. | `08-calendar.md` |
| GDP, inflation, interest rates | `GET /api/world-economy/indicators/{slug}?region=` (`tradingview_get_world_economy_indicators`) | `14-world-economy.md` |
| Historical economic observations | Discover tickers with `GET /api/metadata/world-economy/indicators?view=symbols&country=US`, then query `GET /api/price/ohlcv/{symbol}?format=observations` (`tradingview_get_economic_symbols`, `tradingview_get_economic_data`) | `14-world-economy.md` |
| Symbol logo image | `GET /logo?url={logoid}` (public, no key; REST only) | `09-logo.md` |
| Live streaming updates | `POST /api/token/generate` → SSE/WS on `ws.tradingviewapi.com` (REST only) | `15-token.md`, `11-websocket.md` |
| MCP for Cursor / VS Code / Claude / Codex / Gemini / Windsurf | Hosted `https://mcp.tradingviewapi.com/mcp` + Console OAuth. Per-IDE install in `mcp-install.md`. JWT via `POST /api/mcp/generate` | `mcp-install.md`, `10-mcp.md` |
| Valid parameter values | `GET /api/metadata/...` (`tradingview_get_metadata`) | `07-metadata.md` |

Full parameter tables, enums, and request/response shapes: **[references/endpoint-catalog.md](references/endpoint-catalog.md)**.

When updating an older research integration, match its former route to the current method, parameters and response fields in the [November research migration table](references/research-route-migration.md).

A machine-readable OpenAPI 3.0 spec snapshot is at `references/openapi.json` (too large to read whole; query it instead):

```bash
python3 -c "import json; print('\n'.join(json.load(open('references/openapi.json'))['paths']))"
python3 -c "import json; print(json.dumps(json.load(open('references/openapi.json'))['paths']['/api/quote/{symbol}'], indent=2))"
```

The live spec is at `https://www.tradingviewapi.com/openapi.json` (public, no key). Fetch it to a temporary path when the snapshot seems stale or an endpoint is missing; update the bundled snapshot only when intentionally maintaining this skill:

```bash
curl -fsSL https://www.tradingviewapi.com/openapi.json -o /tmp/tradingview-openapi.json
```

Captured request/response examples live in `references/examples/` (file names listed in the table above). Consult the example file before parsing a response shape you haven't seen. Repeated result rows and long string values are truncated with `(truncated)` markers. Real responses contain the full data.

## Parameters that come from metadata

The following public metadata endpoints list accepted parameter values. For the economic ticker directory (`view=symbols`), use a Console API key or RapidAPI credentials. The CLI's `market:read` OAuth scope excludes this view.

- `market_code` / calendar `market` / screener `market` → `GET /api/metadata/markets`
- leaderboard `tab` → `GET /api/metadata/tabs?type={stocks|indices|crypto|futures|currencies|bonds|corporate_bonds|etfs}`
- leaderboard `columnset` → `GET /api/metadata/columnsets`
- `lang` → `GET /api/metadata/languages` (`zh_CN` / `zh_TW` on REST; news/MCP also accept `zh-Hans`)
- world-economy `indicator` slug → `GET /api/metadata/world-economy/indicators`
- exchange names for screener filters → `GET /api/metadata/exchanges`

When unsure whether a parameter value is valid, fetch the metadata endpoint (or `tradingview_get_metadata`) first instead of guessing.

## Screener workflow

For a market-wide scan:

1. Pick asset type: `stock`, `crypto`, `etf`, `bond`, `cex`, `dex`
2. `GET /api/screener/presets?asset_type=...` → choose `preset_fields` (column groups)
3. `GET /api/screener/filter-options?asset_type=...&lang=en` → discover filter field ids, operations, and enum values
4. `POST /api/screener/{...}/scan` with body `{ market, range, preset_fields, filters, sort }`

Filter syntax: array = multi-select, `{ "operation": "greater_or_equal", "value": n }` = comparison, scalar = equality. Details in the catalog.

For known tickers, discover raw columns with `GET /api/screener/presets?format=columns&asset_type=all&search=RSI` (`tradingview_get_screener_columns`). Send 1–50 symbols and 1–100 fields to `POST /api/screener/scan`. Read the rows under `data.data` and check `data.missing` for absent symbols. This mode preserves raw keys such as `RSI|60`.

## Streaming (WebSocket & SSE)

Streaming is a different host from REST. Mint a JWT first, then connect to `ws.tradingviewapi.com`. Do not call `/sse/stream` on `api.tradingviewapi.com`. MCP has no streaming tools.

```bash
curl --request POST \
  --url 'https://api.tradingviewapi.com/api/token/generate' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer YOUR_API_KEY' \
  --data '{}'
```

SSE quotes support field selection, for example `https://ws.tradingviewapi.com/sse/stream?token=YOUR_JWT&symbols=BINANCE:BTCUSDT&type=quote&fields=lp,bid,ask`. For candles, use `type=price&timeframe=60`. One timeframe applies to every symbol on that connection.

WebSocket: `wss://ws.tradingviewapi.com/ws?token=YOUR_JWT`, then send JSON actions (`subscribe` with `symbol` + optional `timeframe`; `subscribe_quote` with `symbols` array). Server messages are `update` and `quote_update`.

When generating client code for streaming, read **[references/examples/11-websocket.md](references/examples/11-websocket.md)** (and `15-token.md` for the mint response).

## Symbol format

Always `EXCHANGE:TICKER` (e.g. `NASDAQ:AAPL`, `BINANCE:BTCUSDT`, `HKEX:9988`). Option contracts use `OPRA:AAPL261218C330.0`, not `NASDAQ:AAPL261218C330.0`. If the user gives a bare name ("Apple", "比亚迪"), resolve it via `/api/search/market/` or `tradingview_search_market` first.

Quote on the **underlying** never includes the chain (`has_options` / `families`) or ETF holdings. `fields=enhanced` adds contract scalars (`strike`, `expiration`, `option-type`) on an OPRA id and ETF scalars (`aum`, `nav`) on a fund. No implied volatility, Greeks, or open interest.

## Answering data questions

When the user asks a data question (not an integration question):

1. If `tradingview_*` MCP tools are available, call the matching tool from `references/mcp-tools.md`. Skip the REST key workflow.
2. Otherwise ensure a REST key is available and call `scripts/tv_api.py`.
3. Resolve symbols via search if needed.
4. Fetch required metadata for parameter values.
5. For real prices, returns, stops, or backtests: OHLCV (`tradingview_get_ohlcv` / `/api/price/ohlcv/{symbol}`). Do not use `/api/price/{symbol}` unless the user asked for Heikin-Ashi or Range.
6. Summarize the result; cite which MCP tool or REST endpoint you used so the developer can reproduce the call.
