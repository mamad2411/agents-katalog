---
name: stock-market-data
description: "A股/美股行情数据获取工具集 — 交易日检查、指数/板块/涨停池/北向资金数据拉取，基于 AKShare（免费、无需 token）。Use when the user needs free A-share/US market snapshots: trading-day checks, index/sector/limit-up-pool/northbound data, or per-stock daily OHLCV."
version: 1.0.0
effort: medium
---

# 股票行情数据工具集

通用的 A 股 / 美股市场数据获取能力。数据源为 [AKShare](https://akshare.akfamily.xyz)，免费、无需 API token。

## Python 环境（首次安装）

```bash
cd stock-market-data          # this skill's directory
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt   # akshare>=1.18.0, pandas>=2.0.0
```

之后所有脚本通过该 venv 执行：

```bash
PY=.venv/bin/python3
SCRIPTS=scripts
```

### 检查交易日

```bash
$PY $SCRIPTS/check_trading_day.py [--date YYYYMMDD]
```

- 默认检查今天，`--date` 指定其他日期
- 输出: `{"date": "20260317", "is_trading_day": true}`
- 退出码: 0 = 交易日, 1 = 非交易日
- 交易日历自动缓存到脚本同目录，同一年内不重复请求

### 拉取行情数据

```bash
# 晨间: A股20日趋势 + 美股5日 + 板块 + 涨停池 + 北向资金
$PY $SCRIPTS/fetch_market_data.py --mode morning

# 盘后: A股5日 + 板块 + 涨停池 + 北向 + 可选个股追踪
$PY $SCRIPTS/fetch_market_data.py --mode evening --stocks 000001,600519

# 周度: A股20日 + 美股10日 + 板块10日 + 北向10日
$PY $SCRIPTS/fetch_market_data.py --mode weekly
```

## 输出 JSON 结构

各 mode 返回的 JSON 包含以下字段（缺失的字段表示该 mode 不返回）:

| 字段 | morning | evening | weekly | 说明 |
|------|---------|---------|--------|------|
| `us_indices` | Y | — | Y | 美股三大指数 (道琼斯/纳斯达克/标普500) |
| `a_share_indices` | Y | Y | Y | A股四大指数 (上证/深证/沪深300/创业板) |
| `sectors` | Y | Y | Y | 同花顺15大行业板块，按涨跌幅降序 |
| `limit_pool` | Y | Y | — | 涨停池 (前10只，含连板数、所属行业) |
| `northbound` | Y | Y | Y | 北向资金 (沪股通) |
| `tracked_stocks` | — | 需传 --stocks | — | 指定个股日线数据 |

### 关键字段示例

**指数** (`a_share_indices` / `us_indices`):
```json
{"name": "上证指数", "symbol": "sh000001", "close": 3250.12, "change_pct": -0.82, "volume": 79205476400, "trend_5d": "震荡 -0.03%", "trend_20d": "上涨 2.5%", "date": "2026-03-13"}
```

**板块** (`sectors`):
```json
{"name": "半导体", "close": 1580.33, "change_pct": 2.15, "volume": 3847460300, "date": "2026-03-13"}
```

**涨停池** (`limit_pool`):
```json
{"date": "20260313", "count": 23, "top_stocks": [{"code": "000001", "name": "平安银行", "change_pct": 10.02, "industry": "银行", "consecutive": 2}]}
```

**个股** (`tracked_stocks`, 仅 evening 模式):
```json
{"code": "600519", "name": "600519", "close": 1459.02, "change_pct": 3.21, "volume": 12345678, "turnover": 1.25, "date": "2026-03-13"}
```

## 数据覆盖范围

- **A 股指数**: 上证指数、深证成指、沪深300、创业板指
- **美股指数**: 道琼斯、纳斯达克、标普500
- **行业板块** (同花顺): 半导体、白酒、电池、光伏设备、汽车整车、医疗器械、软件开发、房地产、银行、证券、消费电子、军工装备、钢铁、煤炭开采加工、电力
- **涨停池**: 当日涨停股票列表（前10只）
- **北向资金**: 沪股通历史数据
- **个股日线**: 任意 A 股代码的前复权日线数据

## 错误处理

- 单个数据源失败不影响其他数据，失败项返回 `{"name": "...", "error": "错误信息"}`
- 板块/个股找不到数据时静默跳过（不出现在结果中）
- 涨停池/北向资金失败时返回带 `error` 字段的对象
- 脚本总是输出合法 JSON 到 stdout，即使部分数据失败

## 相关 skill

- `tushare-data` — 结构化财务/估值数据（更稳更全，需 Tushare token）
- `financial-data-fetcher` — 财务报表 + ETF 数据（Tushare 优先，AKShare 兜底）
