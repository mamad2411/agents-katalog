---
name: global-stock-data
description: 美股港股数据工具包 — 覆盖行情(新浪+腾讯+东财push2)、K线(新浪美股日K)、技术指标(MA/MACD/RSI/KDJ/布林带)、基本面中文版(东财datacenter三表+GMAININDICATOR)、资金面(东财push2his日级资金流)、搜索与全市场列表(东财)六层数据源，内嵌全部调用代码，自包含零依赖外部文件。官方稳定的数据源（Yahoo Finance、SEC EDGAR：实时行情/历史K线/财报英文版/分析师预期/机构持仓/期权链/新闻/SEC Filing/XBRL）已迁移为 finance-mcp-server 的原生工具，直接调用即可，不需要本 skill。适用于美股港股个股行情、K线技术分析、中文财报解读、资金流追踪、全市场筛选等场景。
origin: custom
version: 1.2
---

> **本地定制说明（2026-06-20）：** 原版工具包覆盖 8 层数据源，其中 Yahoo Finance 与 SEC EDGAR 这两个官方、稳定的数据源已被迁移为 `finance-mcp-server` 的原生 TypeScript 工具（见下方「官方数据源已迁移为原生工具」），不再需要本 skill 写 Python 调用。本 skill 现在只保留新浪/腾讯/东财这类非官方抓取接口，以及零依赖的纯计算技术指标——这些源字段格式可能随时变化，更适合用 Python 灵活调用、出错时随手改两行代码，而不是编译成固定的工具。

# 美股港股数据工具包 V1.2（本地简化版）

六层数据架构，全部零鉴权。

```
行情层（实时/延时）
├── 新浪财经     → 美股 gb_XXXX 36字段 / 港股 rt_hkXXXXX 25字段
├── 腾讯财经     → 美股 usXXXX 71字段 / 港股 r_hkXXXXX 78字段
└── 东财 push2   → 美股/港股 secid 实时行情，含中文名/涨跌幅/换手率

K线层（仅美股日K）
└── 新浪          → 美股日K (回溯至1984年)
    周线/月线/分钟线，以及港股K线 → 用 get_historical_prices 工具（Yahoo Finance，多周期通用）

技术指标层（纯计算，零额外依赖）
└── MA/EMA + MACD + RSI + KDJ + 布林带    基于K线OHLCV，纯Python计算

基本面层（中文版）
├── 东财 datacenter → 美股/港股三表(资产负债+利润+现金流)
└── GMAININDICATOR  → 关键指标(中文字段，ROE/ROA/EPS/毛利率等)
    英文版关键指标/分析师预期/机构持仓 → 用 get_fundamentals / get_analyst_estimates / get_institutional_holders 工具

资金面层
└── 东财 push2his → 日级资金流(主力/大单/中单/小单) 美股+港股

工具层
├── 东财 search    → 股票搜索(中英文, 含市场代码映射)
└── 东财 push2     → 全市场股票列表(涨跌幅/成交量排名, 美股5925只+港股18000+只)
```

---

## 官方数据源已迁移为原生工具

以下能力不再需要本 skill 写 Python，直接调用 `finance-mcp-server` 的工具即可（数据更规整，无需手动解析 Yahoo 的 `{raw, fmt}` 结构）：

| 能力 | 原生工具 |
|------|---------|
| 实时行情（美股/日股） | `get_quote` |
| 历史K线（任意周期，美股/港股/日股） | `get_historical_prices` |
| 基本面/估值指标（英文版） | `get_fundamentals` |
| 股票搜索 | `search_symbols` |
| 市场概览 | `get_market_overview` |
| 预定义选股器 | `screen_stocks` |
| 热门股票 | `get_trending` |
| 机构持仓 | `get_institutional_holders` |
| 分析师EPS预测+评级升降级 | `get_analyst_estimates` |
| 财报明细（年度/季度，income/balance-sheet/cash-flow） | `get_financial_statements` |
| 期权链(calls/puts) | `get_options_chain` |
| 新闻 | `get_stock_news` |
| SEC Filing列表(10-K/10-Q/8-K) | `get_sec_filings` |
| SEC XBRL结构化财务数据 | `get_sec_xbrl_facts` |

**`get_sec_xbrl_facts` 常用 XBRL 指标名速查：**

| 指标 | XBRL 名 |
|------|---------|
| 营业收入 | `RevenueFromContractWithCustomerExcludingAssessedTax` 或 `Revenues` |
| 净利润 | `NetIncomeLoss` |
| 稀释 EPS | `EarningsPerShareDiluted` |
| 基本 EPS | `EarningsPerShareBasic` |
| 总资产 | `Assets` |
| 总负债 | `Liabilities` |
| 股东权益 | `StockholdersEquity` |
| 经营现金流 | `NetCashProvidedByOperatingActivities` |
| 研发费用 | `ResearchAndDevelopmentExpense` |
| 股份回购 | `PaymentsForRepurchaseOfCommonStock` |
| 股息支付 | `PaymentsOfDividends` |

---

## ⚠️ 实测说明（2026-06-16 验证）

使用前请阅读，避免踩坑。

### ✅ 稳定可用

| 功能 | 说明 |
|------|------|
| 新浪美股日K线 | 可用，回溯至1984年。**注意：`num` 参数会被忽略，始终返回全量历史数据（可能数千根）。** 请在代码中手动截取所需数量，例如 `klines = us_stock_kline_sina("AAPL")[-60:]` |
| 技术指标（MACD/RSI/KDJ/布林带） | 纯Python计算，无网络依赖，稳定可用 |
| 东财 search API | 股票搜索可用，`MktNum` 字段可映射 105/106/107/116 前缀 |
| 东财 push2（实时行情）| 可用 |

### ⚠️ 受网络环境限制

| 功能 | 状态 | 说明 |
|------|------|------|
| 东财 push2his 美股资金流 | **在国际/非中国大陆网络环境下连接被拒绝（RemoteDisconnected）** | `push2his.eastmoney.com` 对来自境外IP的请求会直接断开连接，不返回数据。如需使用，须在中国大陆网络环境或通过代理访问。调用时务必用 `try/except` 包裹，不要让错误中断整个脚本 |

### 实测代码模式（处理上述限制）

```python
# ✅ 新浪K线：忽略 num 参数，手动截取
all_klines = us_stock_kline_sina("AAPL")   # 返回全量历史
klines = all_klines[-60:]                   # 取最近60根

# ✅ push2his：加 try/except 防止崩溃
try:
    flow = fund_flow_daily("AAPL", 105, limit=30)
except Exception as e:
    print(f"资金流数据不可用（可能需要国内网络）: {e}")
    flow = []
```

---

## 💡 典型工作流（推荐用法）

### 工作流 A：个股技术分析（最常用）

```python
import requests, re, json

# 1. 搜索确认市场代码（避免 105/106/107 搞错）
result = stock_search("WDC")
# → MktNum=105 (NASDAQ)

# 2. 拉K线（注意手动截取！）
all_klines = us_stock_kline_sina("WDC")
klines = all_klines[-60:]   # 最近60根足够计算所有指标

# 3. 计算技术指标
macd = calc_macd(klines)
rsi  = calc_rsi(klines)
kdj  = calc_kdj(klines)
boll = calc_boll(klines)

# 4. 读取最后一根
last_macd = macd[-1]
last_rsi  = rsi[-1]
last_kdj  = [x for x in kdj if x["k"] is not None][-1]
last_boll = boll[-1]

# 5. 判断信号
print(f"MACD: DIF={last_macd['dif']:+.3f}, DEA={last_macd['dea']:+.3f}")
print(f"RSI6={last_rsi['rsi6']:.1f}, RSI14={last_rsi['rsi14']:.1f}")
print(f"布林带位置: {(klines[-1]['close']-last_boll['lower'])/(last_boll['upper']-last_boll['lower'])*100:.1f}%")
```

### 工作流 B：完整个股分析（组合调用，技术面用 Python + 基本面用原生工具）

```python
# 技术面：拉K线 + 算指标（本 skill 提供）
klines = us_stock_kline_sina("AAPL")[-120:]
quote  = us_stock_quote_sina("AAPL")
macd   = calc_macd(klines)
boll   = calc_boll(klines)
# → 行情 + 技术面
```

估值、机构持仓、分析师评级改用原生工具直接调用，不需要写 Python：
`get_fundamentals("AAPL")` + `get_institutional_holders("AAPL")` + `get_analyst_estimates("AAPL")`

---

## When to Activate

- 用户要查**美股/港股**行情（价格/涨跌幅/成交量）
- 用户要拉**美股日K线**（新浪，回溯至1984年）；如需周线/月线/分钟线或港股K线，直接用 `get_historical_prices` 工具，不需要本 skill
- 用户要看**财报中文版**（资产负债表/利润表/现金流量表，东财）
- 用户要看**关键财务指标中文版**（营收/净利/EPS/ROE/ROA/资产负债率，东财 GMAININDICATOR）
- 用户要看**资金流向**（主力/大单/中单/小单净流入）
- 用户要**搜索股票**（中英文均可）
- 用户要看**全市场涨跌幅排名**（当日涨幅/跌幅最大的股票）
- 用户要做**全市场筛选**（遍历美股/港股列表做初筛）
- 用户要看**技术指标**（MACD/RSI/KDJ/布林带/均线）
- 用户要判断**金叉死叉/超买超卖/变盘信号**
- 关键词：美股、港股、AAPL、苹果、腾讯、00700、TSLA、特斯拉、BABA、阿里巴巴、行情、K线、财报、PE、PB、ROE、资金流、主力、新闻、涨幅排名、全市场、筛选、关键指标、MACD、RSI、KDJ、布林带、均线、金叉、死叉、超买、超卖、技术分析

> 查英文财报/分析师预期/机构持仓/期权链/新闻/SEC Filing/XBRL，直接用对应原生工具（见上方表格），不需要触发本 skill。

---

## Prerequisites

```bash
pip install requests
```

| 依赖 | 版本要求 | 用途 |
|------|---------|------|
| requests | any | 所有 HTTP API 直连 |

> **极简依赖：** 仅需 requests，所有数据源均为直连 HTTP API，零第三方数据封装。

---

## 市场代码规则

### 东财 secid 前缀（push2/push2his 用）

| 前缀 | 市场 | 示例 |
|------|------|------|
| 105 | 美股 NASDAQ | `105.AAPL`, `105.TSLA` |
| 106 | 美股 NYSE | `106.BABA`, `106.JD` |
| 107 | 美股 ETF/其他 | `107.CRSH` |
| 116 | 港股 | `116.00700`, `116.09988` |

> **如何判断 105/106/107？** 调 `stock_search()` 获取 `MktNum` 字段自动映射。

### Yahoo Finance 代码格式（原生工具同样适用）

调用 `get_quote`/`get_historical_prices`/`get_options_chain` 等原生工具时使用：

| 市场 | 格式 | 示例 |
|------|------|------|
| 美股 | 直接 ticker | `AAPL`, `TSLA`, `BABA` |
| 港股 | 四/五位数字 + `.HK` | `0700.HK`, `9988.HK` |
| 日股 | 4位数字 + `.T` | `7203.T` |

### 东财 datacenter SECUCODE 格式

| 市场 | 格式 | 示例 |
|------|------|------|
| 美股 NASDAQ | `TICKER.O` | `AAPL.O`, `TSLA.O` |
| 美股 NYSE | `TICKER.N` | `BABA.N`, `JD.N` |
| 港股 | `CODE.HK` | `00700.HK`, `09988.HK` |

---

## 共用 Helper 函数

### 东财数据中心统一查询

```python
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
DATACENTER_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"

def eastmoney_datacenter(report_name: str, columns: str = "ALL",
                          filter_str: str = "", page_size: int = 50,
                          sort_columns: str = "", sort_types: str = "-1") -> list[dict]:
    """东财数据中心统一查询"""
    params = {
        "reportName": report_name, "columns": columns,
        "filter": filter_str, "pageNumber": "1", "pageSize": str(page_size),
        "sortColumns": sort_columns, "sortTypes": sort_types,
        "source": "WEB", "client": "WEB",
    }
    r = requests.get(DATACENTER_URL, params=params, headers={"User-Agent": UA}, timeout=15)
    d = r.json()
    if d.get("result") and d["result"].get("data"):
        return d["result"]["data"]
    return []
```

---

## Layer 1: 行情层

### 1.1 美股实时行情 — 新浪 + 腾讯

两个独立数据源，任一可用即可。新浪字段侧重价格成交，腾讯字段更全（含52周高低/市值/PE）。

```python
import requests, re

def us_stock_quote_sina(ticker: str) -> dict:
    """
    新浪美股行情 — 36字段
    ticker: 纯字母，如 "AAPL", "TSLA", "BABA"
    """
    url = f"https://hq.sinajs.cn/list=gb_{ticker.lower()}"
    r = requests.get(url, headers={
        "Referer": "https://finance.sina.com.cn/",
        "User-Agent": UA,
    }, timeout=10)
    r.encoding = "gbk"
    text = r.text
    
    m = re.search(r'"(.+)"', text)
    if not m:
        return {}
    
    fields = m.group(1).split(",")
    if len(fields) < 30:
        return {}
    
    return {
        "name": fields[0],           # 中文名
        "price": float(fields[1]),    # 最新价
        "change_pct": float(fields[2]),  # 涨跌幅 %
        "timestamp": fields[3],       # 时间
        "prev_close": float(fields[26]),  # 昨收
        "open": float(fields[5]),     # 开盘
        "high": float(fields[6]),     # 最高
        "low": float(fields[7]),      # 最低
        "volume": float(fields[10]) if fields[10] else 0,  # 成交量
        "high_52w": float(fields[8]) if fields[8] else 0,  # 52周最高
        "low_52w": float(fields[9]) if fields[9] else 0,   # 52周最低
        "market_cap": float(fields[12]) if fields[12] else 0,  # 市值
        "eps": float(fields[13]) if fields[13] else 0,  # EPS
        "pe": float(fields[14]) if fields[14] else 0,   # PE
    }


def us_stock_quote_tencent(ticker: str) -> dict:
    """
    腾讯美股行情 — 71字段
    ticker: 纯字母，如 "AAPL"
    """
    url = f"https://qt.gtimg.cn/q=us{ticker.upper()}"
    r = requests.get(url, timeout=10)
    r.encoding = "gbk"
    text = r.text
    
    m = re.search(r'"(.+)"', text)
    if not m:
        return {}
    
    fields = m.group(1).split("~")
    if len(fields) < 50:
        return {}
    
    return {
        "name": fields[1],           # 中文名
        "name_en": fields[27],       # 英文名
        "price": float(fields[3]) if fields[3] else 0,
        "prev_close": float(fields[4]) if fields[4] else 0,
        "open": float(fields[5]) if fields[5] else 0,
        "volume": int(fields[6]) if fields[6] else 0,
        "high": float(fields[33]) if fields[33] else 0,
        "low": float(fields[34]) if fields[34] else 0,
        "high_52w": float(fields[35]) if fields[35] else 0,
        "low_52w": float(fields[36]) if fields[36] else 0,
        "change_pct": float(fields[32]) if fields[32] else 0,
        "market_cap": float(fields[44]) if fields[44] else 0,  # 亿美元
        "pe": float(fields[53]) if fields[53] else 0,
        "pb": float(fields[56]) if fields[56] else 0,
        "timestamp": fields[30],
    }
```

### 1.2 港股实时行情 — 腾讯 + 新浪

```python
def hk_stock_quote_tencent(code: str) -> dict:
    """
    腾讯港股行情 — 78字段（最全）
    code: 五位数字，如 "00700", "09988"
    """
    url = f"https://qt.gtimg.cn/q=r_hk{code}"
    r = requests.get(url, timeout=10)
    r.encoding = "gbk"
    text = r.text
    
    m = re.search(r'"(.+)"', text)
    if not m:
        return {}
    
    fields = m.group(1).split("~")
    if len(fields) < 50:
        return {}
    
    return {
        "name": fields[1],           # 中文名
        "name_en": fields[2],        # 英文名
        "price": float(fields[3]) if fields[3] else 0,
        "prev_close": float(fields[4]) if fields[4] else 0,
        "open": float(fields[5]) if fields[5] else 0,
        "high": float(fields[33]) if fields[33] else 0,
        "low": float(fields[34]) if fields[34] else 0,
        "volume": int(fields[6]) if fields[6] else 0,    # 成交量(股)
        "amount": float(fields[37]) if fields[37] else 0,  # 成交额
        "change_pct": float(fields[32]) if fields[32] else 0,
        "pe": float(fields[39]) if fields[39] else 0,
        "pb": float(fields[56]) if fields[56] else 0,
        "high_52w": float(fields[35]) if fields[35] else 0,
        "low_52w": float(fields[36]) if fields[36] else 0,
        "market_cap": float(fields[44]) if fields[44] else 0,  # 亿港元
        "timestamp": fields[30],
    }


def hk_stock_quote_sina(code: str) -> dict:
    """
    新浪港股行情 — 25字段
    code: 五位数字，如 "00700"
    """
    url = f"https://hq.sinajs.cn/list=rt_hk{code}"
    r = requests.get(url, headers={
        "Referer": "https://finance.sina.com.cn/",
        "User-Agent": UA,
    }, timeout=10)
    r.encoding = "gbk"
    text = r.text
    
    m = re.search(r'"(.+)"', text)
    if not m:
        return {}
    
    fields = m.group(1).split(",")
    if len(fields) < 15:
        return {}
    
    return {
        "name_en": fields[0],
        "name": fields[1],           # 中文名
        "open": float(fields[2]) if fields[2] else 0,
        "prev_close": float(fields[3]) if fields[3] else 0,
        "high": float(fields[4]) if fields[4] else 0,
        "low": float(fields[5]) if fields[5] else 0,
        "price": float(fields[6]) if fields[6] else 0,
        "change": float(fields[7]) if fields[7] else 0,
        "change_pct": float(fields[8]) if fields[8] else 0,
        "volume": float(fields[12]) if fields[12] else 0,
        "amount": float(fields[11]) if fields[11] else 0,
    }
```

### 1.3 东财 push2 实时行情 — 美股 + 港股

东财 push2 接口，通过 secid 统一查询美股/港股实时行情。优点：有中文名、换手率、涨跌幅，且 secid 可由 `stock_search()` 自动获取。

```python
def stock_quote_eastmoney(ticker_or_code: str, secid_prefix: int = 105) -> dict:
    """
    东财 push2 实时行情 — 美股+港股统一接口
    美股: stock_quote_eastmoney("AAPL", 105)  # NASDAQ
          stock_quote_eastmoney("BABA", 106)  # NYSE
    港股: stock_quote_eastmoney("00700", 116)
    返回: 最新价/开高低收/成交量/成交额/换手率/涨跌幅/中文名
    
    secid_prefix 说明: 105=NASDAQ, 106=NYSE, 107=US_ETF, 116=港股
    如不确定前缀，先调 stock_search() 获取 mkt_num
    """
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": f"{secid_prefix}.{ticker_or_code}",
        "fields": "f43,f44,f45,f46,f47,f48,f55,f57,f58,f59,f60,f170",
    }
    r = requests.get(url, timeout=10)
    d = r.json().get("data")
    if not d:
        return {}
    
    # f59 = 小数位数, 价格字段需除以 10^f59 还原真实值
    dec = d.get("f59", 3)
    divisor = 10 ** dec
    
    def _p(key):
        v = d.get(key)
        if v is None or v == "-":
            return None
        return round(v / divisor, dec)
    
    return {
        "code": d.get("f57"),           # 股票代码
        "name": d.get("f58"),           # 中文名
        "price": _p("f43"),             # 最新价
        "high": _p("f44"),              # 最高
        "low": _p("f45"),               # 最低
        "open": _p("f46"),              # 开盘
        "volume": d.get("f47"),         # 成交量(股)
        "amount": d.get("f48"),         # 成交额
        "turnover_rate": d.get("f55"),  # 换手率(%)
        "prev_close": _p("f60"),        # 昨收
        "change_pct": round(d["f170"] / 100, 2) if d.get("f170") is not None else None,  # 涨跌幅(%)
    }
```

---

## Layer 2: K线层（仅美股日K，新浪）

> 周线/月线/分钟线，以及港股K线，请直接用 `get_historical_prices` 工具（Yahoo Finance 多周期通用，不需要本 skill）。

### 2.1 美股日K — 新浪

新浪可回溯到 1984 年，比 Yahoo 覆盖的历史更长，这是它仍留在本 skill 里的原因。

```python
def us_stock_kline_sina(ticker: str, num: int = 120) -> list[dict]:
    """
    新浪美股日K — 可回溯到1984年
    ticker: 如 "AAPL"
    返回: [{date, open, high, low, close, volume}, ...]

    ⚠️ 重要：num 参数实测会被服务器忽略，始终返回全量历史数据（可能数千根）。
    请调用后手动截取，例如：klines = us_stock_kline_sina("AAPL")[-60:]
    """
    url = "https://stock.finance.sina.com.cn/usstock/api/jsonp.php/var/US_MinKService.getDailyK"
    params = {"symbol": ticker.upper(), "num": num}
    r = requests.get(url, params=params, headers={"Referer": "https://finance.sina.com.cn/"}, timeout=15)
    text = r.text
    
    # 解析 JSONP: var=([{...},...])
    import json
    m = re.search(r'\((\[.+\])\)', text)
    if not m:
        return []
    
    items = json.loads(m.group(1))
    result = []
    for item in items:
        result.append({
            "date": item.get("d"),
            "open": float(item.get("o", 0)),
            "high": float(item.get("h", 0)),
            "low": float(item.get("l", 0)),
            "close": float(item.get("c", 0)),
            "volume": int(item.get("v", 0)),
        })
    return result
```

---

## Layer 3: 技术指标层

基于 K 线 OHLCV 数据的纯 Python 技术指标计算，零额外依赖。

**使用方式：** 先调 K 线函数获取数据，再传入技术指标函数：
```python
klines = us_stock_kline_sina("AAPL", 120)
macd = calc_macd(klines)
rsi = calc_rsi(klines)
```

### 3.1 移动平均线 MA / EMA

```python
def _ema(values: list[float], period: int) -> list[float]:
    """EMA 指数移动平均（内部辅助）"""
    result = [values[0]]
    k = 2 / (period + 1)
    for v in values[1:]:
        result.append(v * k + result[-1] * (1 - k))
    return result


def calc_ma(klines: list[dict], periods: list[int] = None) -> list[dict]:
    """
    移动平均线 MA + EMA
    klines: K线数据 [{date, open, high, low, close, volume}, ...]
    periods: 周期列表，默认 [5, 10, 20, 60]
    返回: [{date, close, ma5, ma10, ma20, ma60, ema12, ema26}, ...]
    """
    if periods is None:
        periods = [5, 10, 20, 60]
    closes = [k["close"] for k in klines]
    
    # EMA 12/26（MACD 常用）
    ema12 = _ema(closes, 12)
    ema26 = _ema(closes, 26)
    
    result = []
    for i, k in enumerate(klines):
        row = {"date": k["date"], "close": k["close"]}
        for p in periods:
            if i >= p - 1:
                row[f"ma{p}"] = round(sum(closes[i - p + 1:i + 1]) / p, 4)
            else:
                row[f"ma{p}"] = None
        row["ema12"] = round(ema12[i], 4)
        row["ema26"] = round(ema26[i], 4)
        result.append(row)
    return result
```

### 3.2 MACD

```python
def calc_macd(klines: list[dict], fast: int = 12, slow: int = 26,
              signal: int = 9) -> list[dict]:
    """
    MACD (Moving Average Convergence Divergence)
    klines: K线数据
    fast/slow/signal: 快线/慢线/信号线周期（默认 12/26/9）
    返回: [{date, close, dif, dea, macd_hist}, ...]
    
    dif = EMA(fast) - EMA(slow)        金叉/死叉看 dif 穿越 dea
    dea = EMA(signal) of dif           信号线
    macd_hist = (dif - dea) * 2        柱状图（红涨绿跌）
    """
    closes = [k["close"] for k in klines]
    ema_fast = _ema(closes, fast)
    ema_slow = _ema(closes, slow)
    
    dif = [round(f - s, 4) for f, s in zip(ema_fast, ema_slow)]
    dea = _ema(dif, signal)
    
    result = []
    for i, k in enumerate(klines):
        result.append({
            "date": k["date"],
            "close": k["close"],
            "dif": round(dif[i], 4),
            "dea": round(dea[i], 4),
            "macd_hist": round((dif[i] - dea[i]) * 2, 4),
        })
    return result
```

### 3.3 RSI

```python
def calc_rsi(klines: list[dict],
             periods: list[int] = None) -> list[dict]:
    """
    RSI (Relative Strength Index)
    klines: K线数据
    periods: 周期列表（默认 [6, 12, 24]）
    返回: [{date, close, rsi6, rsi12, rsi24}, ...]
    
    RSI > 70 超买区（可能回调）
    RSI < 30 超卖区（可能反弹）
    """
    if periods is None:
        periods = [6, 12, 24]
    closes = [k["close"] for k in klines]
    
    # 涨跌额序列
    changes = [0.0] + [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [max(c, 0) for c in changes]
    losses = [max(-c, 0) for c in changes]
    
    result = []
    for i, k in enumerate(klines):
        row = {"date": k["date"], "close": k["close"]}
        for p in periods:
            if i < p:
                row[f"rsi{p}"] = None
                continue
            avg_gain = sum(gains[i - p + 1:i + 1]) / p
            avg_loss = sum(losses[i - p + 1:i + 1]) / p
            if avg_loss == 0:
                row[f"rsi{p}"] = 100.0
            else:
                rs = avg_gain / avg_loss
                row[f"rsi{p}"] = round(100 - 100 / (1 + rs), 2)
        result.append(row)
    return result
```

### 3.4 KDJ

```python
def calc_kdj(klines: list[dict], n: int = 9,
             m1: int = 3, m2: int = 3) -> list[dict]:
    """
    KDJ 随机指标
    klines: K线数据
    n: RSV 周期（默认9）
    m1/m2: K/D 平滑系数（默认3/3）
    返回: [{date, close, k, d, j}, ...]
    
    K/D > 80 超买，K/D < 20 超卖
    J > 100 或 J < 0 为极端信号
    金叉: K 上穿 D；死叉: K 下穿 D
    """
    k_val, d_val = 50.0, 50.0
    result = []
    
    for i, kline in enumerate(klines):
        if i < n - 1:
            result.append({"date": kline["date"], "close": kline["close"],
                           "k": None, "d": None, "j": None})
            continue
        
        window = klines[i - n + 1:i + 1]
        high_n = max(w["high"] for w in window)
        low_n = min(w["low"] for w in window)
        
        rsv = (kline["close"] - low_n) / (high_n - low_n) * 100 if high_n != low_n else 50.0
        k_val = (1 / m1) * rsv + (1 - 1 / m1) * k_val
        d_val = (1 / m2) * k_val + (1 - 1 / m2) * d_val
        j_val = 3 * k_val - 2 * d_val
        
        result.append({
            "date": kline["date"],
            "close": kline["close"],
            "k": round(k_val, 2),
            "d": round(d_val, 2),
            "j": round(j_val, 2),
        })
    return result
```

### 3.5 布林带

```python
def calc_boll(klines: list[dict], period: int = 20,
              num_std: float = 2.0) -> list[dict]:
    """
    布林带 (Bollinger Bands)
    klines: K线数据
    period: 中轨 MA 周期（默认20）
    num_std: 标准差倍数（默认2）
    返回: [{date, close, upper, middle, lower, bandwidth}, ...]
    
    价格触及 upper → 可能超买
    价格触及 lower → 可能超卖
    bandwidth 收窄 → 即将变盘
    """
    closes = [k["close"] for k in klines]
    result = []
    
    for i, k in enumerate(klines):
        if i < period - 1:
            result.append({"date": k["date"], "close": k["close"],
                           "upper": None, "middle": None, "lower": None,
                           "bandwidth": None})
            continue
        
        window = closes[i - period + 1:i + 1]
        ma = sum(window) / period
        std = (sum((x - ma) ** 2 for x in window) / period) ** 0.5
        upper = ma + num_std * std
        lower = ma - num_std * std
        
        result.append({
            "date": k["date"],
            "close": k["close"],
            "upper": round(upper, 4),
            "middle": round(ma, 4),
            "lower": round(lower, 4),
            "bandwidth": round((upper - lower) / ma * 100, 2) if ma else None,
        })
    return result
```

---

## Layer 4: 基本面层（中文版）

> 英文版关键财务指标、分析师预期、机构持仓、年度/季度财报明细已迁移为原生工具：`get_fundamentals`、`get_analyst_estimates`、`get_institutional_holders`、`get_financial_statements`。这里保留的是东财的中文版数据，字段名和侧重点都不同，两者互补。

### 4.1 财报三表 — 东财 datacenter

东财 datacenter 提供美股/港股的资产负债表、利润表、现金流量表，中文字段名，按科目行展开。

```python
def financial_statements_eastmoney(secucode: str, statement: str = "balance",
                                     page_size: int = 200) -> list[dict]:
    """
    东财 datacenter 财报三表
    secucode: "AAPL.O" (NASDAQ) / "BABA.N" (NYSE) / "00700.HK" (港股)
    statement: "balance" / "income" / "cashflow"
    返回: [{ITEM_NAME, AMOUNT, YOY_RATIO, REPORT, REPORT_DATE, ...}, ...]
    
    注意: 数据按科目行展开，每行一个科目（如"流动资产合计"、"营业收入"等），
    同一期报告有多行。用 REPORT_DATE 分组可还原整张报表。
    """
    # 报表名映射（注意命名不统一：balance/income 用 F10，cashflow 用 SK）
    report_map = {
        "balance": {"us": "RPT_USF10_FN_BALANCE", "hk": "RPT_HKF10_FN_BALANCE"},
        "income":  {"us": "RPT_USF10_FN_INCOME",  "hk": "RPT_HKF10_FN_INCOME"},
        "cashflow": {"us": "RPT_USSK_FN_CASHFLOW", "hk": "RPT_HKSK_FN_CASHFLOW"},
    }
    
    market = "hk" if secucode.endswith(".HK") else "us"
    report_name = report_map[statement][market]
    
    return eastmoney_datacenter(
        report_name=report_name,
        filter_str=f'(SECUCODE="{secucode}")',
        page_size=page_size,
        sort_columns="REPORT_DATE",
        sort_types="-1",
    )
    # 每行字段:
    # SECUCODE, SECURITY_CODE, SECURITY_NAME_ABBR, REPORT_DATE,
    # STD_ITEM_CODE, ITEM_NAME (科目名), AMOUNT (金额),
    # YOY_RATIO (同比%), REPORT (如 "2026/Q2"), REPORT_TYPE,
    # ACCOUNT_STANDARD (如 "美国会计准则"/"国际会计准则"),
    # CURRENCY (如 "美元"/"人民币")
```

### 4.2 关键财务指标(中文) — 东财 GMAININDICATOR

东财 datacenter 的 GMAININDICATOR 报表，提供中文关键财务指标概览。美股 49 字段、港股 75 字段，包含 ROE/ROA/EPS/毛利率/资产负债率/流动比率等，按季度报告。

```python
def key_indicators_eastmoney(secucode: str, page_size: int = 4) -> list[dict]:
    """
    东财 GMAININDICATOR 关键财务指标（中文）
    secucode: "AAPL.O" (NASDAQ) / "BABA.N" (NYSE) / "00700.HK" (港股)
    page_size: 返回最近几期报告（默认4期=一年）
    返回: [{REPORT_DATE, OPERATE_INCOME, BASIC_EPS, ROE_AVG, ROA, ...}, ...]
    
    美股核心字段(49): OPERATE_INCOME(营收), GROSS_PROFIT(毛利), GROSS_PROFIT_RATIO(毛利率%),
      PARENT_HOLDER_NETPROFIT(归母净利), NET_PROFIT_RATIO(净利率%), BASIC_EPS, DILUTED_EPS,
      ROE_AVG(平均ROE%), ROA(%), CURRENT_RATIO(流动比率), DEBT_ASSET_RATIO(资产负债率%),
      OPERATE_INCOME_YOY(营收同比%), BASIC_EPS_YOY(EPS同比%)
    
    港股额外字段(75): BPS(每股净资产), ROIC(投入资本回报率), EQUITY_RATIO(产权比率),
      HOLDER_PROFIT(股东应占溢利), OCF_SALES(经营现金流/营收%), DPS_HKD(每股股息),
      DIVI_RATIO(股息率%), PER_NETCASH_OPERATE(每股经营现金流)
    """
    market = "hk" if secucode.endswith(".HK") else "us"
    report_name = f"RPT_{'HK' if market == 'hk' else 'US'}F10_FN_GMAININDICATOR"
    
    return eastmoney_datacenter(
        report_name=report_name,
        filter_str=f'(SECUCODE="{secucode}")',
        page_size=page_size,
        sort_columns="REPORT_DATE",
        sort_types="-1",
    )
```

---

## Layer 5: 资金面层

### 5.1 日级资金流 — 东财 push2his

```python
def fund_flow_daily(ticker_or_code: str, secid_prefix: int = 105,
                      limit: int = 100) -> list[dict]:
    """
    东财 push2his 日级资金流 — 主力/大单/中单/小单净流入
    美股: fund_flow_daily("AAPL", 105)  # NASDAQ
          fund_flow_daily("BABA", 106)  # NYSE
    港股: fund_flow_daily("00700", 116)
    返回: [{date, main_net, big_net, mid_net, small_net, main_pct, ...}, ...]

    ⚠️ 网络限制：push2his.eastmoney.com 在非中国大陆网络环境下会拒绝连接
    （RemoteDisconnected，不返回数据）。务必用 try/except 包裹调用：
        try:
            flow = fund_flow_daily("AAPL", 105)
        except Exception as e:
            print(f"资金流不可用（需国内网络）: {e}")
            flow = []
    """
    url = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    params = {
        "secid": f"{secid_prefix}.{ticker_or_code}",
        "klt": 101,
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57",
        "lmt": limit,
    }
    r = requests.get(url, timeout=15)
    d = r.json()
    data = d.get("data")
    if not data or not data.get("klines"):
        return []
    
    result = []
    for line in data["klines"]:
        parts = line.split(",")
        # f51=日期, f52=主力净流入, f53=小单净流入, f54=中单净流入, f55=大单净流入, f56=超大单净流入
        result.append({
            "date": parts[0],
            "main_net": float(parts[1]),       # 主力净流入（元）
            "small_net": float(parts[2]),       # 小单净流入
            "mid_net": float(parts[3]),         # 中单净流入
            "big_net": float(parts[4]),         # 大单净流入
            "super_big_net": float(parts[5]),   # 超大单净流入
            "main_pct": float(parts[6]) if len(parts) > 6 and parts[6] else 0,  # 主力净占比%
        })
    return result
```

---

## Layer 6: 工具层

### 6.1 股票搜索 — 东财 search API

```python
def stock_search(keyword: str, count: int = 10) -> list[dict]:
    """
    东财股票搜索 — 支持中英文，返回代码+市场+中文名
    keyword: "AAPL" / "苹果" / "Tencent" / "00700" / "特斯拉"
    返回: [{code, name, mkt_num, market_name, security_type}, ...]
    
    mkt_num 即 push2/push2his 的 secid 前缀:
    105=NASDAQ, 106=NYSE, 107=美股ETF, 116=港股
    """
    url = "https://searchapi.eastmoney.com/api/suggest/get"
    params = {
        "input": keyword,
        "type": 14,  # 14=全球市场
        "token": "D43BF722C8E33BDC906FB84D85E326E8",
        "count": count,
    }
    r = requests.get(url, timeout=10)
    d = r.json()
    
    suggestions = d.get("QuotationCodeTable", {}).get("Data", [])
    result = []
    for s in suggestions:
        mkt = s.get("MktNum", "")
        # 只保留美股和港股
        if str(mkt) not in ("105", "106", "107", "116"):
            continue
        
        market_map = {"105": "NASDAQ", "106": "NYSE", "107": "US_OTHER", "116": "HK"}
        result.append({
            "code": s.get("Code"),
            "name": s.get("Name"),
            "mkt_num": int(mkt),
            "market_name": market_map.get(str(mkt), str(mkt)),
            "security_type": s.get("SecurityTypeName"),
        })
    return result
```

### 6.2 全市场股票列表 — 东财 push2

```python
def market_stock_list(market: str = "us_nasdaq", sort_field: str = "f3",
                       sort_desc: bool = True, page: int = 1,
                       page_size: int = 20) -> dict:
    """
    东财 push2 全市场股票列表 — 涨跌幅/成交量/成交额排名
    market: "us_nasdaq" (m:105), "us_nyse" (m:106), "hk" (m:116)
    sort_field: 排序字段
      f3=涨跌幅, f5=成交量, f6=成交额, f2=最新价, f7=振幅, f15=最高, f16=最低
    sort_desc: True=降序(默认), False=升序
    page/page_size: 分页（默认第1页，每页20条）
    返回: {"total": 5925, "stocks": [{code, name, price, change_pct, volume, ...}, ...]}
    
    典型用途:
    - 今日涨幅 TOP 20: market_stock_list("us_nasdaq", "f3", True)
    - 今日跌幅 TOP 20: market_stock_list("us_nasdaq", "f3", False)
    - 成交量 TOP 20: market_stock_list("hk", "f5", True)
    - 遍历全市场: 循环 page=1..N, 每页100条做筛选
    """
    market_map = {"us_nasdaq": "m:105", "us_nyse": "m:106", "us_etf": "m:107", "hk": "m:116"}
    fs = market_map.get(market, market)
    
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        "fs": fs,
        "fields": "f2,f3,f4,f5,f6,f7,f12,f14,f15,f16,f17,f18",
        "pn": page,
        "pz": page_size,
        "fid": sort_field,
        "po": 1 if sort_desc else 0,
    }
    r = requests.get(url, timeout=15)
    d = r.json()
    data = d.get("data", {})
    
    total = data.get("total", 0)
    diff = data.get("diff", [])
    
    stocks = []
    for item in diff:
        stocks.append({
            "code": item.get("f12"),         # 股票代码
            "name": item.get("f14"),         # 中文名
            "price": item.get("f2"),         # 最新价(原始值, 需÷10^小数位)
            "change_pct": round(item["f3"] / 100, 2) if item.get("f3") is not None else None,  # 涨跌幅(%)
            "change_amount": item.get("f4"), # 涨跌额(原始值)
            "volume": item.get("f5"),        # 成交量(股)
            "amount": item.get("f6"),        # 成交额
            "amplitude": round(item["f7"] / 100, 2) if item.get("f7") is not None else None,  # 振幅(%)
            "high": item.get("f15"),         # 最高(原始值)
            "low": item.get("f16"),          # 最低(原始值)
            "open": item.get("f17"),         # 开盘(原始值)
            "prev_close": item.get("f18"),   # 昨收(原始值)
        })
    
    return {"total": total, "stocks": stocks}
```

---

## 数据源优先级

| 场景 | 第一优先 | 备选 | 说明 |
|------|---------|------|------|
| 美股行情 | 新浪 `gb_XXXX` | 腾讯 / 东财 push2 | 新浪有中文名+EPS+PE |
| 港股行情 | 腾讯 `r_hkXXXXX` | 新浪 / 东财 push2 | 腾讯字段最全(78个) |
| 美股K线 | 新浪（本skill，回溯至1984年） | `get_historical_prices` 工具 | 多周期/港股K线用工具 |
| 财报三表(中文) | 东财 datacenter | — | 中文科目名，按行展开 |
| 关键指标(中文) | 东财 GMAININDICATOR | — | ROE/ROA/EPS/毛利率/资产负债率 (美49/港75字段) |
| 资金流 | 东财 push2his | — | 日级主力/大单/中单/小单；**⚠️ 非中国大陆网络环境下连接被拒绝，需代理** |
| 搜索 | 东财 search | `search_symbols` 工具 | 东财有 secid 映射 |
| 全市场列表 | 东财 push2 clist | — | 涨跌幅/成交量排名，美股5925+港股18000+ |

英文基本面、分析师预期、机构持仓、期权链、新闻、SEC Filing/XBRL → 见上方「官方数据源已迁移为原生工具」。

---

## 数据源汇总

| 数据源 | 协议 | 鉴权 | 覆盖 |
|--------|------|------|------|
| 东财 push2 | HTTPS | 零 | 美股+港股 实时行情+全市场列表 |
| 东财 push2his | HTTPS | 零 | 美股+港股 资金流；⚠️ **境外网络环境下被拒绝连接，需代理** |
| 东财 datacenter | HTTPS | 零 | 美股+港股 财报三表+GMAININDICATOR关键指标 |
| 东财 search API | HTTPS | 零 | 全球股票搜索+secid映射 |
| 新浪财经 | HTTP | 零 | 美股+港股 行情、美股K线 |
| 腾讯财经 | HTTPS | 零 | 美股+港股 行情 |

Yahoo Finance / SEC EDGAR → 见上方「官方数据源已迁移为原生工具」，由 `finance-mcp-server` 直接调用。