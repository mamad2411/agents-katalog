---
name: finflow
description: Query financial market data using the finflow CLI tool. Supports A-shares, HK stocks, US stocks, futures, and macro data. Use this skill whenever the user asks about stock quotes (SH600519, 00700, AAPL), market indices, financial news, capital flow, sector rankings, macro calendar, futures, or any financial data. Also trigger when the user mentions stock codes, ticker symbols (e.g. 茅台, NVDA, 腾讯), asks about market sentiment, wants to check portfolio, or needs real-time financial information for investment decisions.
---

# Finflow — Chinese Financial Data CLI

Finflow (`@openduo/finflow`) aggregates real-time data from four Chinese financial platforms: CLS (财联社), Jin10 (金十), Xueqiu (雪球), and Gelonghui (格隆汇).

## Core Principles

1. **Run via Bash**: `finflow <command>` — if not found, install first with `npm install -g @openduo/finflow`
2. **Stock code formats are flexible**: `sh600519`, `SH600519`, `600519` all work — the CLI normalizes internally
3. **Global markets supported**: A-shares (`SH600519`), HK stocks (`00700`, `09988`), US stocks (`AAPL`, `NVDA`, `.DJI`)
4. Default output is JSON with `{ data, meta }` envelope. Use `-f text` only when the user wants human-readable tables. Use `-f raw` for debugging.

## Global Options (apply to all commands)

| Flag | Default | Description |
|------|---------|-------------|
| `-n <num>` | `10` | Number of items |
| `-f json\|text\|raw` | `json` | Output format |
| `-h` | — | Show help |

## Command Reference

### Stock Quotes — `quote`

**`quote <code>`** — Single stock quote (CLS)

**`quote batch <codes...>`** — Batch quotes (Xueqiu). Auto-prefixes `SH`/`SZ` for 6-digit A-share codes. Supports HK/US stocks.
```
quote batch sh600519 sz000858        # A股
quote batch 00700 09988               # 港股（纯数字代码）
quote batch AAPL NVDA TSLA .DJI     # 美股
```

**`quote search <keyword>`** — Search stocks (Xueqiu)
```
quote search 白酒
```

**`quote related <code>`** — Related stocks (Xueqiu)

**`quote kline <code>`** — K-line data

| Flag | Alias | Default | Values | Description |
|------|-------|---------|--------|-------------|
| `--period` | `-p` | `d` | `d` `w` `m` `y` `5d` `1m` `5m` `15m` `30m` `60m` `120m` | Period |
| `--number` | `-n` | `120` | number | Number of candles |
| `--src` | — | auto | `cls` `xq` | Data source |

Source auto-selection: minute periods (`1m` `5m` `15m` `30m` `60m` `120m`) auto-use xueqiu; daily+ default to cls. For US/HK stocks, always use `--src xq`.
```
quote kline sh600519 -p d -n 120     # 日K 120根 (cls)
quote kline sh600519 -p 5m -n 48     # 5分钟K线 (xueqiu, auto)
quote kline sh600519 -p w            # 周K (cls)
quote kline sh600519 -p d --src xq   # 强制用雪球
```

**`quote depth <code>`** — 5-level order book

| Flag | Default | Values | Description |
|------|---------|--------|-------------|
| `--src` | `cls` | `cls` `xq` | Data source |

**`quote ticks <code>`** — Tick-by-tick trades. Options same as `depth`.

**`quote timeline <code>`** — Intraday timeline. Options same as `depth`.

**`quote sector`** — Sector/plate data

| Subcommand | Args | Options | Description |
|---|---|---|---|
| `sector rank` | — | `-t <type>` (default: `industry`) | Plate ranking. Type: `industry` `concept` |
| `sector plate <code>` | code | — | Stock's associated plates |
| `sector industry <code>` | code | — | Industry info (xueqiu) |

Default (no subcommand): with code → `plate`, without → `rank -t industry`.

### Capital Flow — `quote flow`

| Subcommand | Args | Options | Source | Description |
|---|---|---|---|---|
| (default) | code | — | cls | Per-stock fund flow (main in/out, super/large/medium/small) |
| `flow market` | — | — | glh | Northbound/southbound capital |
| `flow history <code>` | code | `-c <num>` (default: 20) | xq | Historical flow + 3d/5d/10d/20d net |
| `flow margin <code>` | code | — | xq | Margin trading data |
| `flow intraday <code>` | code | — | xq | Intraday capital flow |
| `flow xq <code>` | code | — | xq | Xueqiu capital flow |

Default without code → shows market flow (same as `flow market`).

### Fundamentals — `quote f10` / `quote finance`

**`quote f10`** subcommands (all require xueqiu login):

| Subcommand | Description |
|---|---|
| `f10 indicator <code>` | Key indicators: ROE, EPS, gross margin, revenue growth |
| `f10 holders <code>` | Top 10 shareholders |
| `f10 bonus <code>` | Dividend history (up to 15 items) |
| `f10 event <code>` | Corporate events (up to 20 items) |

**`quote finance <code>`** — Financial statements (xueqiu login):

| Flag | Alias | Default | Values | Description |
|------|-------|---------|--------|-------------|
| `--type` | `-t` | `indicator` | `indicator` `cashflow` `income` `balance` | Report type |

| Type | Content |
|---|---|
| `indicator` | ROE, EPS, gross margin, revenue YoY |
| `income` | Revenue, net profit, attributable net profit |
| `balance` | Total assets, liabilities, debt ratio, equity |
| `cashflow` | Operating, investing, financing, net increase |

### News & Flash — `info`

**`info flash`** — Flash/breaking news

| Flag | Alias | Default | Values | Description |
|------|-------|---------|--------|-------------|
| `--src` | `-s` | `cls` | `cls` `jin10` `glh` | Data source |
| `--category` | `-c` | varies | varies by source | Category/channel filter |

CLS categories (`-s cls`): `all` `red` `announcement` `watch` `hk_us` `fund` `remind`
GLH categories (`-s glh`): `all` `popular` `AStock` `HKStock` `USStock` `fundLive` `ai` `international` `chineseMainland` `hongkongMacaoTaiwan` `virtualAssets` `exchangeCommodity` `house` `debenture`

| Subcommand | Args | Extra Options | Notes |
|---|---|---|---|
| `flash important` | — | `--channel <glh_channel>` | Important news (glh) |
| `flash popular` | — | — | Popular flash (glh) |
| `flash detail <id>` | id | — | Flash detail (jin10, tries browser cookie) |
| `flash date <date>` | date | — | Historical flash (jin10, **requires login**) |
| `flash live [channel]` | channel | `--interval <sec>` (default: 10) | Real-time monitoring (glh, infinite loop) |

**`info news`** — Articles

| Subcommand | Args | Description |
|---|---|---|
| (default) | — | CLS headline news |
| `news depth [channel]` | channel | CLS deep articles. Channels: `headline` `ashare` `world` `company` `realestate` `finance_ch` `hkstock` `fund` `broker` `auto` `tech` `pinjian` |
| `news slide` | — | Important events slideshow (jin10) |
| `news feature` | — | Featured articles (jin10) |
| `news hot` | — | Hot articles ranking (cls) |
| `news stock <code>` | code | Per-stock news (cls) |

**`info report <code>`** — Institutional research reports (xueqiu, **requires login**)

**`info topic`** — Topics

| Subcommand | Args | Description |
|---|---|---|
| (default) | — | List all topics (jin10) |
| `topic search <keyword>` | keyword | Search topics |
| `topic groups` | — | Topic category groups |
| `topic hot` | — | Hot CLS subjects |
| `topic show <id>` | id | Articles in topic (jin10, tries browser cookie) |

### Market Overview — `market`

| Subcommand | Args/Options | Source | Description |
|---|---|---|---|
| (default) | — | glh | Major indices + Shanghai/Shenzhen capital flow |
| `market emotion` | — | cls | Market sentiment: limit-up/down, seal rate, turnover, distribution |
| `market rank [type]` | type: `change` `volume` `amount` `turnover` `amplitude` (default: `change`) | cls | Stock ranking |
| `market index` | — | glh | Major market indices |
| `market hk [sort]` | sort: `netChange` `turnoverValue` `turnVolume` (default: `netChange`). `-o asc\|desc` (default: `desc`) | glh | HK stock ranking |
| `market flow` | — | glh | Northbound/southbound capital flow |
| `market rates` | — | jin10 | Global central bank interest rates |

### Macro Calendar — `calendar`

All subcommands accept an optional `<date>` argument (defaults to today).

| Subcommand | Source | Description |
|---|---|---|
| `calendar invest [date]` | cls | A-share investment calendar |
| `calendar macro [date]` | jin10 | Global macro data releases |
| `calendar event [date]` | jin10 | Macro events (speeches, decisions) |
| `calendar holiday [date]` | jin10 | Global holidays |
| `calendar ashare` | jin10 (WS) | A-share major events |
| `calendar hk [date]` | jin10 (WS) | HK stock data calendar |
| `calendar us [date]` | jin10 (WS) | US stock data calendar |
| `calendar future-event [date]` | jin10 | Futures calendar events |
| `calendar future-holiday [date]` | jin10 | Futures calendar holidays |

All dates default to today, format: `YYYY-MM-DD`.

Default (no subcommand): same as `calendar invest` with today.

### Futures — `future`

Top-level `--channel` / `-c` applies to all subcommands:

| Channel | Description |
|---|---|
| `all` | 全部 (default) |
| `oil` | 原油 |
| `steel` | 钢铁 |
| `coal` | 煤炭 |
| `gas` | 天然气 |
| `metal` | 金属 |
| `nonferrous` | 有色金属 |
| `chemical` | 化工 |
| `sugar` | 白糖 |
| `grain` | 粮食 |
| `pig` | 生猪 |
| `macro` | 宏观 |

| Subcommand | Description |
|---|---|
| (default) | Futures flash news (paginated) |
| `future headline` | Futures headlines |
| `future basis [date]` | Spot-futures basis. `-g <group>`: `黑色系` `金属` `农产品` `能源化工` `金融` |
| `future calendar [date]` | Futures data calendar |
| `future event [date]` | Futures calendar events |
| `future holiday [date]` | Futures calendar holidays |

### Portfolio — `portfolio` (requires xueqiu login)

| Subcommand | Args | Options | Description |
|---|---|---|---|
| (default) | — | — | List all groups (stocks/cubes/funds) |
| `portfolio stocks <pid>` | pid: `-1`=all, `-5`=沪深 | — | View stocks with live quotes |
| `portfolio stocks add <symbol>` | symbol | `-c <gid>` (default: 1) | Add stock to group |
| `portfolio stocks remove <symbol>` | symbol | `-c <gid>` (default: 1) | Remove stock from group |
| `portfolio cube <code>` | code | — | Cube NAV trend (up to 20) |
| `portfolio cube holding <code>` | code | — | Cube holdings with weight/price |

### Config — `config`

| Subcommand | Args | Description |
|---|---|---|
| `config cookie [value]` | value | Set/show xueqiu cookie. Without value: shows masked current cookie |
| `config login` | — | Auto-extract from macOS Chrome (Keychain + AES-128-CBC) |

## Cookie Requirements

Most commands work without login. These **require xueqiu cookie** (`finflow config login`):
- `quote f10`, `quote finance`, `quote flow history/margin/intraday/xq`
- `portfolio` (all subcommands), `info report`
- `quote depth/timeline --src xq`, `quote kline --src xq`

Jin10 commands (`info flash detail`, `info flash date`, `info topic show`, `calendar macro/event/holiday`) try browser cookie automatically, work without it but with less data.

## Data Interpretation Tips

- **`meta.source`** tells you which platform the data came from — useful context for freshness
- **CLS flash** is fastest for A-share breaking news
- **`market emotion`** shows limit-up/down counts, seal rates — key sentiment indicators
- **`quote flow market`** shows northbound (沪港通/深港通) capital — important for A-share trend
- **Non-trading hours**: some commands return empty data (emotion, timeline)
- **CLS flash with jin10 source** auto-paginates up to 50 pages (slow for large `-n`)

## Common Workflows

**"茅台现在多少钱？"** → `quote sh600519`
**"帮我看看今天大盘怎么样"** → `market emotion` + `market index`
**"今天有什么财经新闻"** → `info flash -n 20`
**"美股那边有什么重要新闻"** → `info flash -s glh -c USStock`
**"白酒板块怎么样"** → `quote sector rank -t concept` (filter by name for 白酒)
**"北向资金今天流入多少"** → `quote flow market`
**"帮我看看贵州茅台的财务数据"** → `quote f10 indicator sh600519` + `quote finance sh600519 -t income`
**"今天有什么宏观事件"** → `calendar macro`
**"今晚美国有什么CPI数据"** → `calendar macro 2026-04-10` (filter by country=美国)
**"期货方面有什么消息"** → `future headline` or `future -c oil`
**"最近的原油期现基差"** → `future basis -g 能源化工`
**"今天涨停板排行"** → `market rank change`
**"港股成交额排行"** → `market hk turnoverValue`
