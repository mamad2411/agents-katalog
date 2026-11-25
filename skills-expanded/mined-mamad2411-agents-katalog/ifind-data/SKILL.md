---
name: ifind-data
description: 基于同花顺 iFind API 的金融数据查询技能。用于获取 A 股、港股、美股的股票行情、基金净值、指数数据、财务报表等。触发场景：(1) 查询股票实时行情或历史价格，(2) 获取基金净值和业绩数据，(3) 查询指数成分股和估值，(4) 使用自然语言选股（问财），(5) 获取财务数据和估值指标。支持本地 SDK 和 HTTP API 两种调用方式。
---

# iFind Data

基于同花顺 iFind API 的金融数据查询技能，提供股票、基金、指数等金融数据的查询功能。

## 快速开始

### 环境配置

1. 复制 `assets/env.example` 为 `.env`，填入认证信息：
   ```
   IFIND_USERNAME=your_username
   IFIND_PASSWORD=your_password
   ```

2. 安装依赖：
   ```bash
   pip install requests pandas numpy python-dotenv loguru
   ```

3. （可选）安装本地 SDK：从 https://quantapi.10jqka.com.cn 下载 iFinDPy

### 基本用法

```python
from scripts.ifind_client import IFindClient

# 创建客户端并登录
client = IFindClient()
client.login()

# 获取股票收盘价
data = client.get_basic_data('000001.SZ', 'ths_close_price_stock', '2024-01-15,100')

# 获取实时行情
data = client.get_realtime_quotes(['000001.SZ', '600000.SH'])

# 问财自然语言查询
data = client.wencai_query('市值大于1000亿的股票', 'stock')
```

## 数据查询工作流

1. 确定查询类型：
   - **单日数据？** → 使用 `get_basic_data()`
   - **历史序列？** → 使用 `get_date_serial()`
   - **实时行情？** → 使用 `get_realtime_quotes()`
   - **自然语言选股？** → 使用 `wencai_query()`

2. 构建查询参数：
   - 证券代码格式：`000001.SZ`（深交所）、`600000.SH`（上交所）
   - 日期格式：`YYYY-MM-DD` 或 `YYYYMMDD`

3. 执行查询并处理返回的 DataFrame

## 核心功能

### 股票数据查询

```python
# 获取收盘价
client.get_basic_data('000001.SZ', 'ths_close_price_stock', '2024-01-15,100')

# 获取历史价格
client.get_date_serial('000001.SZ', 'ths_close_price_stock', 'Fill:Blank', '2024-01-01', '2024-01-15')

# 获取估值数据
client.get_basic_data('000001.SZ', 'ths_pe_stock,ths_pb_stock', '2024-01-15')
```

### 实时行情

```python
# 获取最新价
client.get_realtime_quotes('000001.SZ', 'latest,changeRatio,volume')

# 获取 Level2 盘口
client.get_realtime_quotes('000001.SZ', 'latest,bid1,bid2,bid3,bid4,bid5,ask1,ask2,ask3,ask4,ask5')
```

### 问财查询

```python
# 条件选股
client.wencai_query('市盈率小于20且ROE大于15%的股票', 'stock')

# 获取涨停股
client.wencai_query('今日涨停的股票', 'stock')

# 获取主力资金流向
client.wencai_query('主力资金流入的股票', 'stock')
```

### 指数和基金

```python
# 获取指数成分股
client.get_data_pool('p03291', 'date=20240115;blockname=001005261', 'p03291_f001:Y,p03291_f002:Y')

# 获取基金净值
client.get_basic_data('000001.OF', 'ths_unit_nav_fund', '2024-01-15')
```

## 常用指标速查

| 简称 | 指标代码 | 说明 |
|------|----------|------|
| 收盘价 | `ths_close_price_stock` | 日收盘价 |
| 市盈率 | `ths_pe_stock` | PE |
| 市净率 | `ths_pb_stock` | PB |
| 总市值 | `ths_market_value_stock` | 市值 |
| ROE | `ths_roe_stock` | 净资产收益率 |

更多指标参见 [references/indicators.md](references/indicators.md)

## 板块代码

| 简称 | 代码 |
|------|------|
| 全部A股 | `001005010` |
| 沪深300 | `001005261` |
| 中证500 | `001005262` |
| 上证50 | `001005260` |

更多板块代码参见 [references/block_codes.md](references/block_codes.md)

## 资源

- **scripts/ifind_client.py** - iFind API 客户端，提供所有数据查询方法
- **scripts/http_client.py** - HTTP API 客户端，无需安装本地 SDK
- **references/indicators.md** - 完整指标代码参考
- **references/block_codes.md** - 板块代码参考
- **references/api_examples.md** - API 调用示例
- **assets/env.example** - 环境变量配置模板
