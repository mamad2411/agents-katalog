---
name: tonghuashun
description: 同花顺股票数据与分析综合技能。通过 thsdk 获取 A股/港股/美股实时行情、分钟K线、盘口深度、大单流向、板块指数、资金流向、问财选股等全量市场数据。数据源优先级：thsdk → akshare → 直连API(新浪/东财) → wencai_nlp → 浏览器。
version: 1.1.0
---

# 同花顺综合股票分析技能

## 数据获取规则（最高优先级）

1. **首选**：通过本技能（thsdk 接口）获取完整的行情数据和技术指标
2. **Fallback**：thsdk 游客账户在指数类数据（`market_data_index`、指数 `klines`）上经常返回空 `QueryData错误:not data`。出现此情况时，**立即切换 akshare** 作为数据源，无需等待浏览器或用户授权。akshare 在本环境已安装
3. **深度 Fallback**：当 akshare 也全部返回 None（常见原因：`http_proxy` 环境变量阻断 East Money API），**不要报告"暂无数据"**——立即用直连 API（新浪财经 CSV 或东方财富 Push API）获取，详见 `references/sina-eastmoney-direct-api.md`
4. **兜底**：直连 API 也失败时，用 thsdk 的 `wencai_nlp` 查询指数行情（thsdk 不走 HTTP proxy）：`ths.wencai_nlp("上证指数 深证成指 创业板指 今日涨跌幅")`
5. **数据源优先级**：thsdk API → akshare → 直连 API（新浪/东财）→ wencai_nlp → 本机浏览器 → 其他（需用户授权）

\n\n## 依赖安装

\n\n## 依赖安装

## 依赖安装

```bash
pip install --upgrade thsdk
```

首次使用时自动检查安装，版本要求 >= 1.7.14。

## 连接

```python
from thsdk import THS

with THS() as ths:   # 游客模式，无需账户配置
    ...
```

## 对话引导规范

### 澄清意图（意图模糊时必问）

| 用户说 | 可能的意图 | 必问 |
|--------|-----------|------|
| "帮我看看XX股票" | 实时行情？K线？大单？ | 是 |
| "分析一下XX" | 技术面？资金面？和谁对比？ | 是 |
| "XX板块怎么样" | 整体涨跌？成分股？领涨股？ | 是 |
| "选一些好股票" | 短线？价值？哪个行业？条件？ | 是 |
| "XX的5分钟K线" | 意图明确 | 否，直接执行 |
| "今日涨停股" | 意图明确 | 否，直接执行 |

---

## 第一步：代码解析

所有中文名/缩写/短代码先用 `search_symbols` 获得完整 THSCODE：

```python
with THS() as ths:
    resp = ths.search_symbols("同花顺")
    # data → [
    #   {'THSCODE': 'USZA300033', 'Name': '同花顺',
    #    'MarketStr': 'USZA', 'Code': '300033', 'MarketDisplay': '深A'},
    # ]
```

**选码规则：**

| 情况 | 处理 |
|------|-----|
| 0条 | 告知未找到 |
| 1条 | 直接使用 |
| 多条，只有1只A股（MarketDisplay含"沪A"或"深A"） | 自动选A股 |
| 多条，多只A股 | 展示列表，等用户选择 |

**便捷封装函数（来自 stock_utils）：**

```python
from stock_utils import search_stock_candidates, get_candidate_by_index

with THS() as ths:
    result = search_stock_candidates(ths, "平安银行")
    # result['status']: 'found' / 'need_selection' / 'not_found'
    # result['ths_code']: 唯一匹配时的完整代码
    # result['display']: 格式化的展示文本
```

**市场前缀说明：**

| 前缀 | 含义 |
|------|------|
| `USHA` | 上海A股 |
| `USZA` | 深圳A股 |
| `USHI` | 上海指数 |
| `USZI` | 深圳指数 |
| `USTM` | 北交所 |
| `UHKG` | 港股 |
| `URFI` | 行业/概念板块 |
| `UFXB` | 外汇（基本汇率） |

**常用指数 THSCODE（直接使用，无需 search_symbols）：**

| 指数 | THSCODE |
|------|---------|
| 上证指数 | `USHI000001` |
| 深证成指 | `USZI399001` |
| 创业板指 | `USZI399006` |
| 科创50 | `USHI000688` |
| 沪深300 | `USHI000300` |
| 中证500 | `USHI000905` |
| 上证50 | `USHI000016` |

> 指数前缀是 `USHI`/`USZI`，需调用 `market_data_index`，不能用 `market_data_cn`

---

## A股行情（market_data_cn）

```python
with THS() as ths:
    resp = ths.market_data_cn("USZA300033", "基础数据")
    resp = ths.market_data_cn(["USZA300033", "USZA000001"], "汇总")
    df = resp.df
```

> ⚠️ **Pitfall：多股 + `"汇总"` 批量调用会报 `list index out of range`。**
> 当需要查询多只股票的"汇总"数据时，**必须逐只调用** `market_data_cn(code, "汇总")`，
> 不要传入列表。`"基础数据"` 等简单 query_key 在少量同市场股票时可能成功，
> 但为安全起见，建议所有多股场景统一改为逐只调用。

**query_key 选项：**

| query_key | 含义 |
|-----------|------|
| `"基础数据"` | 价格、涨跌幅、成交量、金额、开高低、涨速 |
| `"基础数据2"` | 精简版基础数据 |
| `"基础数据3"` | 极简（价格、昨收、成交量） |
| `"扩展1"` | 涨幅、涨跌、换手率、量比、主力净流入、委比 |
| `"扩展2"` | 涨幅、换手率、总市值、流通市值、委比 |
| `"汇总"` | 全量字段，多股对比首选 |

> 同市场限制：USHA 和 USZA 不能在同一次调用中混合

---

## K线数据

**interval 参数：** `"1m"` / `"5m"` / `"15m"` / `"30m"` / `"60m"` / `"120m"` / `"day"` / `"week"` / `"month"` / `"quarter"` / `"year"`

> 必须写 `"5m"`，不能写 `"5min"`

**count 与 start/end 二选一，不可混用：**

```python
from datetime import datetime
from zoneinfo import ZoneInfo
tz = ZoneInfo('Asia/Shanghai')

with THS() as ths:
    resp = ths.klines("USZA300033", interval="5m", count=78)
    resp = ths.klines("USZA300033", interval="day",
                      start_time=datetime(2025, 1, 1, tzinfo=tz),
                      end_time=datetime(2025, 3, 1, tzinfo=tz))
    resp = ths.klines("USHA600519", interval="day", count=250, adjust="forward")

    df = resp.df
    # 字段：时间, 收盘价, 成交量, 总金额, 开盘价, 最高价, 最低价
```

---

## 分时与盘口数据

### 日内分时（当日）

```python
with THS() as ths:
    resp = ths.intraday_data("USZA300033")
    df = resp.df
    # 字段：时间(datetime+tz), 价格, 成交量, 总金额, 领先指标
```

### 历史分时（近一年）

```python
with THS() as ths:
    resp = ths.min_snapshot("USZA300033", date="20240315")
    df = resp.df
```

### 五档盘口

```python
with THS() as ths:
    resp = ths.depth("USZA300033")
    resp = ths.depth(["USZA300033", "USHA600519"])
    df = resp.df
    # 字段：买1~5价/量, 卖1~5价/量, 代码, 昨收价
```

### 买卖深度详情

```python
with THS() as ths:
    resp = ths.order_book_bid("USZA300033")   # 买方深度
    resp = ths.order_book_ask("USZA300033")   # 卖方深度
```

### 3秒 Tick

```python
with THS() as ths:
    resp = ths.tick_level1("USZA300033")
    df = resp.df
```

### 超级盘口（含委托档位）

```python
with THS() as ths:
    resp = ths.tick_super_level1("USZA300033")                   # 实时
    resp = ths.tick_super_level1("USZA300033", date="20240315")  # 历史
    # 部分字段值为 4294967295 表示无效数据，需过滤
```

---

## 大单与竞价

### 大单流向

```python
with THS() as ths:
    resp = ths.big_order_flow("USZA300033")
    df = resp.df
    # 字段：时间, 成交方向, 成交量, 总金额, 委托买入价, 委托卖出价
```

### 集合竞价异动（9:15~9:25）

```python
with THS() as ths:
    resp_sh = ths.call_auction_anomaly("USHA")   # 沪市
    resp_sz = ths.call_auction_anomaly("USZA")   # 深市
```

### 早盘集合竞价快照

```python
with THS() as ths:
    resp = ths.call_auction("USZA300033")
```

---

## 板块与指数

### 行业/概念板块列表

```python
with THS() as ths:
    resp = ths.ths_industry()   # 同花顺行业，约90个
    resp = ths.ths_concept()    # 概念板块，约390个
    # 仅返回：代码(URFIXXXXXX), 名称
```

### 板块行情（两步走）

```python
with THS() as ths:
    resp = ths.ths_industry()
    target = next(r for r in resp.data if '半导体' in r['名称'])
    link_code = target['代码']
    resp = ths.market_data_block(link_code, "基础数据")
    # query_key 也支持 "扩展"（含板块涨速、主力净流入等）
```

### 板块成分股

```python
with THS() as ths:
    resp = ths.block_constituents("URFI883404")
```

### 指数行情

```python
with THS() as ths:
    resp = ths.market_data_index("USHI000001")
    resp = ths.market_data_index(["USHI000001", "USHI000300", "USHI000905"])
```

---

## 资金流向（get_fund_flow）

```python
from stock_utils import get_fund_flow

with THS() as ths:
    result = get_fund_flow(ths, "贵州茅台")
    # result['main_net_inflow']: 主力净流入
    # result['retail_net_inflow']: 散户净流入
```

---

## 多市场行情

### 港股

```python
with THS() as ths:
    resp = ths.stock_hk_lists()
    resp = ths.market_data_hk("UHKG00700", "基础数据")
```

### 美股

```python
with THS() as ths:
    resp = ths.stock_us_lists()
    resp = ths.nasdaq_lists()
    resp = ths.market_data_us("UNQQAAPL", "基础数据")
```

> ⚠️ **Pitfall：thsdk 游客账户查询 US 个股经常失败。**
> 游客账户下 `market_data_us` 可能返回全 `"?"`，`search_symbols` 可能返回杠杆 ETF 而非正股。
> 出现此情况时，立即切换到 akshare `stock_us_daily(ticker, adjust="qfq")` 逐只获取，
> 详见 `references/akshare-index-fallback.md` 中"美股个股日线"一节。

> ⚠️ **Pitfall：US 个股搜索返回 ETF 而非正股。**
> 搜索 "苹果" 可能返回 "每日2倍做多苹果ETF" 而非 AAPL。此时不宜用第一个结果，
> 应直接用 akshare 按 ticker 获取。新 IPO 公司（如 SPCX）thsdk 可能完全找不到，
> 需用 Yahoo Finance browser lookup 确认代码后再用 akshare。

### 外汇

```python
with THS() as ths:
    resp = ths.forex_list()
    resp = ths.market_data_forex("UFXBGBPUSD", "基础数据")
```

### 期货

```python
with THS() as ths:
    resp = ths.futures_lists()
    resp = ths.market_data_future("UCFSAU2506", "基础数据")
```

### 债券 / ETF

```python
with THS() as ths:
    resp = ths.bond_lists()
    resp = ths.fund_etf_lists()
    resp = ths.market_data_bond("USHD123456", "基础数据")
    resp = ths.market_data_fund("USHA510300", "基础数据")
```

---

## 多股票批量对比

```python
import pandas as pd
import time
from thsdk import THS

stock_names = ["贵州茅台", "五粮液", "泸州老窖"]

with THS() as ths:
    stock_codes = []
    for name in stock_names:
        resp = ths.search_symbols(name)
        a_shares = [s for s in resp.data
                    if any(m in s.get('MarketDisplay', '') for m in ['沪A', '深A'])]
        if a_shares:
            stock_codes.append({'name': name, 'code': a_shares[0]['THSCODE']})

    rows = []
    for stock in stock_codes:
        resp = ths.market_data_cn(stock['code'], "汇总")
        if resp and resp.data:
            row = resp.data[0]
            row['股票名称'] = stock['name']
            rows.append(row)
        time.sleep(0.3)   # 逐只调用，避免限流

    klines_data = {}
    for s in stock_codes:
        resp = ths.klines(s['code'], interval="day", count=30, adjust="forward")
        klines_data[s['name']] = resp.df

# 归一化走势
for name, df in klines_data.items():
    df['归一化'] = df['收盘价'] / df['收盘价'].iloc[0] * 100

# 相关性矩阵
returns = pd.DataFrame({name: df['收盘价'].pct_change() for name, df in klines_data.items()})
corr_matrix = returns.corr()
```

---

## 问财自然语言查询（wencai_nlp）

```python
with THS() as ths:
    resp = ths.wencai_nlp("连续3日主力净流入，换手率大于5%，非ST")
    df = resp.df
    # 股票代码格式为 "605366.SH"，需转换
```

**返回代码转换：**

```python
def to_ths_code(code_str: str) -> str:
    try:
        code, market = str(code_str).split('.')
        mapping = {'SH': 'USHA', 'SZ': 'USZA', 'BJ': 'USTM'}
        prefix = mapping.get(market.upper(), '')
        return f"{prefix}{code}" if prefix else None
    except Exception:
        return None
```

**常用查询示例：**

| 类型 | 示例 |
|------|------|
| 行情 | `"今日涨停，非ST"` |
| 板块 | `"今日申万行业涨跌幅排名"` |
| 财务 | `"连续3年ROE大于15%，非ST"` |
| 技术 | `"均线多头排列，MACD金叉"` |
| 信息 | `"今日龙虎榜"` |
| 成交量放大 | `"上周五成交量较前一日放大超过2倍，总市值小于100亿，上周五涨幅大于3%，非ST，非北交所"` |
| 热门板块+小盘 | `"今日板块涨幅排名"`（配合 `block_constituents` 深挖） |

> ⚠️ **Pitfall：wencai 列名编码日期不匹配 — 列名和预期完全不同**
>
> wencai 返回的 DataFrame 列名会将 NLP 查询中的日期相关性编码进列名，且**编码格式不可预测**。
> 例如查询 `"上周五成交量较前一日放大超过2倍"`，你期望的列名可能是 `成交量环比增长率[20260710]`，
> 但实际列名可能长这样：`{(}{(}成交量[20260710]{-}成交量[20260709]{)}{/}成交量[20260709]{)}`。
>
> 同样，`总市值` 可能变成 `总市值[20260709]`，而 `涨跌幅` 可能是 `涨跌幅:前复权[20260710]`。
>
> **解决方案：**
> ```python
> # 第一步：先打印所有列名确认实际名称
> resp = ths.wencai_nlp("你的查询")
> df = resp.df
> print("Columns:", df.columns.tolist())
>
> # 第二步：按位置索引取值（推荐），或按实际列名取
> VOL_RATIO_COL = df.columns[0]   # 通常是成交量环比列
> MCAP_COL = df.columns[2]        # 通常是市值列
> PRICE_COL = df.columns[5]       # 最新价
> CHANGE_COL = df.columns[6]      # 涨跌幅
> CODE_COL = df.columns[8]        # 股票代码
> NAME_COL = df.columns[10]       # 股票简称
>
> for i, row in df.iterrows():
>     d = row.to_dict()
>     code = str(d[CODE_COL])
>     name = str(d[NAME_COL])
>     vol_ratio = float(d[VOL_RATIO_COL] or 0)
> ```
>
> > ⚠️ **Pitfall：wencai 财务数据列名 GBK 编码乱码（Windows）**
> 在 Windows 终端下，wencai 返回的财务数据（如 ROE、PE、PB 等）DataFrame 列名可能出现 GBK 编码乱码，导致按列名取值全部失败。
>
> **解决方案：用股票代码匹配行，而非依赖列名。**
> wencai 返回的股票代码格式为 `"600519.SH"` / `"300033.SZ"`，可通过 `to_ths_code()` 转换后匹配对应行数据，绕过乱码列名问题。
>
> ```python
> # ❌ 错误做法：按列名取值（可能因乱码失败）
> # roe = df['净资产收益率'][0]
>
> # ✅ 正确做法：按股票代码定位行
> target_code = "600519.SH"
> for _, row in df.iterrows():
>     if target_code in str(row.values):
>         # 该行为目标股票数据，按位置取字段
>         break
> ```

---

## 实时资讯

**不要用 `news()` 作为新闻搜索的首选。** 游客账户的 `news()` 只返回 20 条无过滤快讯，不支持定向搜索，几乎查不到你想要的新闻。

**第一选择永远是 `news-search` 子 skill：**

```bash
python3 ~/.hermes/skills/tonghuashun/news-search/scripts/news_search.py "美国取消对香港国家紧急状态" --size 5
```

- 基于 iwencai 问财 API，支持中文关键词搜索
- 返回央视、新华社、财经、微信公号等一手报道，时效性优于 AP News
- 同一新闻比海外媒体早数小时到一天，且有中方官方回应等独家内容
- 已验证：有效覆盖政策新闻、财报消息、行业动态等全品类财经资讯

海外新闻后备：AP News 内搜 `apnews.com/search`（英文关键词），但时效性不如问财。

> ⚠️ 旧用法 `ths.news()` 保留仅用于获取实时快讯轮播（如突发消息页面），不做定向新闻搜索。

---

## 其他 API

### 权息资料

```python
resp = ths.corporate_action("USZA300033")
```

### IPO 数据

```python
resp = ths.ipo_today()   # 今日申购/上市
resp = ths.ipo_wait()    # 待申购
```

### 市场列表

```python
resp = ths.stock_cn_lists()    # 全部A股
resp = ths.stock_hk_lists()    # 港股
resp = ths.stock_us_lists()    # 美股
resp = ths.stock_bj_lists()    # 北交所
resp = ths.bond_lists()        # 可转债
resp = ths.fund_etf_lists()    # ETF
resp = ths.futures_lists()     # 期货主力合约
resp = ths.forex_list()        # 外汇
```

---

## 错误处理

```python
with THS() as ths:
    resp = ths.klines("USZA300033", interval="5m", count=60)
    if not resp:
        print(f"调用失败: {resp.error}")
    elif resp.df.empty:
        print("数据为空，可能是非交易时间")
    else:
        df = resp.df
```

**常见报错：**

| 错误 | 原因 | 解决 |
|------|------|------|
| `"未登录"` | 未 connect | 确保用 `with THS() as ths` |
| `"证券代码必须为10个字符"` | 格式错误 | 先过 `search_symbols` |
| `"一次性查询多支股票必须市场代码相同"` | 沪深混合 | 按市场分组查询 |
| `"无效的周期类型: 5min"` | interval 写法错 | 改为 `"5m"` |
| `"'count' 参数不能与 'start_time' 同时使用"` | 参数冲突 | 二选一 |
| `"list index out of range"` (market_data_cn) | 多股+汇总批量调用 | 改为逐只调用 `market_data_cn(code, "汇总")` |
| `"QueryData错误:not data"` (指数行情/指数K线) | 游客账户对指数类数据权限不足 | 立即走 fallback 链：① 新浪直连 `hq.sinajs.cn/list=sh000001` → ② 东财 Push API → ③ akshare（无代理时）→ ④ wencai_nlp。见 `references/sina-eastmoney-direct-api.md` |
| wencai 返回的 DataFrame 列名乱码 | Windows GBK 编码 | 用股票代码（`.SH`/`.SZ`）匹配行，不按列名取值 |
| `stock_us_spot_em()` 超时 (tqdm 走不完) | 全量 5500+ 美股下载过慢 | 改用 `stock_us_daily(symbol, adjust="qfq")` 逐只获取 |
| [`thsdk`]QueryData错误:not data (US个股) | 游客账户无 US 股票数据权限 | 切换 akshare `stock_us_daily(ticker, adjust="qfq")` |
| akshare 指数/行业函数全部返回 None | http_proxy 环境变量阻断 East Money API | 见下方「akshare 被代理阻断时的直连方案」 |

**注意事项：**
- 游客账户在部分专业数据/实时数据上可能有权限限制
- 批量拉取时建议加 `time.sleep(0.5)` 避免限流
- `THS` 为同步阻塞，在 FastAPI/asyncio 中需放入线程池
- **thsdk 不走 HTTP 代理**：不同于 akshare（走东方财富 API，受 `http_proxy`/`https_proxy` 阻断），thsdk 使用自有 TCP 协议直连同花顺行情服务器，在有代理的环境下正常工作。如果 akshare 全部报 `ProxyError`，优先切 thsdk。

### akshare 被代理阻断时的直连方案

当环境设置了 http_proxy/https_proxy 且 MacPacket/Shadowrocket 不转发 East Money 流量时，akshare 的 requests 调用全部返回 None。此时用以下直连方案代替：

**方案 A：直接请求新浪财经 API（最可靠）**

```python
import requests
url = "http://hq.sinajs.cn/list=sh000001"
headers = {"Referer": "https://finance.sina.com.cn"}
r = requests.get(url, headers=headers, timeout=10,
                 proxies={"http": None, "https": None})
# 返回 CSV 格式
```

字段顺序：名称, 开盘, 前收, 最新, 最高, 最低, ..., 日期, 时间。
代码格式：sh000001（上证）、sz399001（深成指）、sz399006（创业板）。

**方案 B：东方财富 push API**

```python
url = "https://push2.eastmoney.com/api/qt/ulist.np/get"
params = {"fltt": 2, "fields": "f2,f3,f4,f12,f14",
          "secids": "1.000001",
          "_": int(__import__("time").time() * 1000)}
r = requests.get(url, params=params, timeout=10,
                 proxies={"http": None, "https": None})
# f2=最新价, f3=涨跌幅%, f4=涨跌额
```

**方案 C：wencai_nlp 查询指数（thsdk 不走 HTTP proxy）**

```python
with THS() as ths:
    resp = ths.wencai_nlp("上证指数 深证成指 创业板指 今日涨跌幅")
```

### 市场总结文档格式检查（防止被批评）

写完含有 Markdown 表格的市场总结后，在 commit 前逐项检查：

- [ ] 表格每行开头是 | 不是 ||
- [ ] 分隔行 |--- 与表头对齐
- [ ] 表格中无多余空列（patch 后重新 read_file 确认）
- [ ] SVG 图表引用的数据与文字版一致

### Market Summary SVG 输出规范

每次大盘回顾/板块分析输出应包括：

1. **Markdown 文档** `docs/jul-NN-market-review/README.md` — 表格、分析、结论
2. **SVG 柱状图** `indices.svg` — 各指数涨跌幅对比（红跌绿涨），标注关键信号（如剪刀差）
3. **SVG 条图** `sectors.svg` — 领涨板块成分股涨幅排行，标注主力净流入

SVG 尺寸规范：
- 指数图：700×420，横排6-7个指数柱，基线用虚线，重点标注用 stroke-dasharray
- 板块图：600×420，成分股纵排队列（左标签右条图），底部补充其他板块亮点
- 颜色：上涨 #27ae60 / 下跌 #e74c3c，基线 #ccc dashed
- 字体：Helvetica Neue, 11-13px 正文

> SVG 数据与表格数据必须一致。commit 前快速对照。

### 大盘回顾/市场总结写作原则

当用户要求跨市场大盘回顾（如"上周五大盘走势"、"看下各市场"）时，**数据集齐后必须做逻辑分析**，不要只罗列数据：

1. **识别关键信号**——哪个市场/板块是涨跌幅极值（如本次A股创业板-7.15%是全球领跌）
2. **关联验证**——VIX、黄金、原油等辅助指标佐证宏观判断（如VIX+12.19%确认risk-off）
3. **子板块分化**——同一市场内部谁涨谁跌，分歧就是信号（如存储全面上涨vs半导体普跌）
4. **归因分析**——linking data to catalysts（如Big Tech财报前瞻、伊朗冲突、联储表态）
5. **结论提炼**——2-4条可执行的核心判断，格式：**加粗标题** — 一句话分析

**关键分析模式：指数剪刀差（"二八分化"）**

当获取全市场指数数据后，必算以下剪刀差：

| 对比组合 | 含义 |
|----------|------|
| 上证50 vs 中证500 | 大盘 vs 中小盘风格切换，剪刀差>3%即极端分化 |
| 上证指数 vs 创业板指 | 权重 vs 成长风格 |
| 沪深300 vs 科创50 | 传统蓝筹 vs 科技成长 |

如果剪刀差 > 2%（如上证50+3.01% vs 中证500-1.36%，差=4.37%），须以**"极致二八分化"**为市场核心叙事，分析资金从中小盘撤出涌入大盘蓝筹的逻辑。写作顺序：描述剪刀差幅度 → 给具体数据 → 归因 → 后市展望。

> 用户讨厌"数据堆砌"式的总结。**逻辑分析 > 数据罗列**。



| 用户需求 | 方法 |
|---------|------|
| 今日涨停/连板/竞价强势股 | `wencai_nlp("今日涨停，非ST")` |
| 放量异动选股（按日期） | `wencai_nlp("昨日成交量较前一日放大超过2倍，总市值小于100亿，昨日涨幅大于3%，非ST")` + 按位置取列 |
| 财务选股（ROE/PE/PB） | `wencai_nlp("连续3年ROE大于15%，非ST")` |
| 技术形态选股 | `wencai_nlp("均线多头排列，MACD金叉")` |
| 分钟K线 | `klines(code, interval="5m", count=78)` |
| 今日分时 | `intraday_data(code)` |
| 历史某日分时 | `min_snapshot(code, date="20250101")` |
| 五档盘口 | `depth(code)` |
| 买方/卖方深度详情 | `order_book_bid(code)` / `order_book_ask(code)` |
| 大单流向 | `big_order_flow(code)` |
| 竞价异动扫描 | `call_auction_anomaly("USHA")` |
| 申万行业列表 | `ths_industry()` |
| 概念板块列表 | `ths_concept()` |
| 板块行情（涨幅/市值） | `market_data_block(link_code)` |
| 板块成分股 | `block_constituents(link_code)` |
| 指数行情 | `market_data_index(ths_code)` |
| 多股票对比 | 批量 `market_data_cn` + `klines` |
| 港股行情 | `market_data_hk(code)` |
| 美股行情 | `market_data_us(code)` |
| 外汇汇率 | `market_data_forex(code)` |
| 期货行情 | `market_data_future(code)` |
| 实时资讯/快讯 | `news()` |
| 权息资料 | `corporate_action(code)` |
| 今日IPO / 待申购 | `ipo_today()` / `ipo_wait()` |
| 实时行情 | `market_data_cn(code, "汇总")` |
| 资金流向 | `get_fund_flow(ths, name)` |
| 日K线 | `get_kline_data(ths, name, interval="day", count=30)` |

---

## 资源文件

| 文件 | 用途 |
|------|------|
| `scripts/stock_utils.py` | 核心工具函数：自动安装、代码解析、数据获取封装 |
| `scripts/example.py` | 基础用法示例 |
| `references/api_reference.md` | thsdk 原始 API 完整参考文档 |
| `references/iwencai-skills.md` | 已安装的 iwencai 问财 skills 总览 |
| `references/wencai-column-quirks.md` | wencai 列名日期编码实测记录 + 安全处理模式 |
| `references/wencai-market-summary-workflow.md` | 已验证的 wencai 市场总结查词 + 字段解析（当标准API失败时） |
| `references/sina-eastmoney-direct-api.md` | akshare 被代理阻断时的新浪/东方财富直连方案 + 字段解析 |
| `references/akshare-index-fallback.md` | thsdk 游客账户指数数据失败时，用 akshare 替代方案 |
| `assets/stock_template.py` | 含可视化的股票分析完整模板 |
| `examples/01_minute_kline.py` | 分钟K线 + 均线 + 成交量异动标注 |
| `examples/02_sector_industry.py` | 行业排名 + 概念板块成分股 + 指数行情 |
| `examples/03_multi_stock_compare.py` | 多股批量对比：表格 + 归一化走势 + 相关性 |
| `examples/04_bigorder_auction.py` | 大单流向 + 竞价异动扫描 + 分时/盘口 + 资讯 |
| `examples/05_wencai_nlp.py` | 问财NLP：选股/行情/财务/技术/复杂组合 |
