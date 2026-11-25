---
name: stock-sdk-mcp
description: 股票行情数据服务 - 支持 A股/港股/美股实时行情、K线、技术指标、板块数据。当用户查询股票、基金、行情、技术分析、板块数据、市场概览、股票筛选、持仓监控时使用此技能。
---

# Stock SDK MCP

股票行情数据服务，基于 [stock-sdk-mcp](https://github.com/chengzuopeng/stock-sdk-mcp) 构建。支持 A股/港股/美股/基金的实时行情、K线数据、技术指标计算、板块数据查询。

## 支持的市场

| 市场 | 说明 |
|------|------|
| A股 | 沪深北交易所、科创板、创业板 |
| 港股 | 香港交易所 |
| 美股 | 纳斯达克、纽交所 |
| 基金 | 公募基金 |

## 命令格式

所有工具通过 mcp2cli 调用：

```bash
# 列出所有工具
uvx mcp2cli --mcp-stdio "npx -y stock-sdk-mcp" --list

# 查看工具帮助
uvx mcp2cli --mcp-stdio "npx -y stock-sdk-mcp" <tool-name> --help
```

---

## 核心工具速查

### 最常用工具

| 工具 | 用途 | 示例 |
|------|------|------|
| `get-quotes-by-query` | 按名称/代码/拼音查询行情（推荐） | `--queries '["茅台", "腾讯"]'` |
| `get-kline-with-indicators` | 获取K线+技术指标 | `--symbol "600519" --indicators '{"macd":true}'` |
| `get-concept-list` | 概念板块列表 | 无参数 |
| `get-industry-list` | 行业板块列表 | 无参数 |

### 代码格式

| 市场 | 格式 | 示例 |
|------|------|------|
| A股 | `sh600519` 或 `600519` | 茅台 |
| 港股 | `00700` | 腾讯 |
| 美股 | `AAPL` | 苹果 |

---

## 高级技能（按需加载）

根据用户场景，参考以下技能文档：

| 场景 | 技能文档 | 说明 |
|------|----------|------|
| 技术分析 | [stock-analyst.md](./stock-analyst.md) | K线形态、MACD/RSI/KDJ分析 |
| 股票筛选 | [stock-screener.md](./stock-screener.md) | 按条件筛选全市场股票 |
| 市场概览 | [market-overview.md](./market-overview.md) | 大盘走势、热点板块 |
| 持仓监控 | [realtime-monitor.md](./realtime-monitor.md) | 自选股跟踪、盈亏计算 |

---

## 工具分类索引

### 一、实时行情
- `get-quotes-by-query` - 通用查询（最推荐）
- `get-a-share-quotes` - A股行情
- `get-hk-quotes` - 港股行情
- `get-us-quotes` - 美股行情
- `get-fund-quotes` - 基金净值

### 二、批量行情（数据量大，谨慎使用）
- `get-all-a-share-quotes` - 全A股（5000+只）
- `get-all-hk-quotes` - 全港股（2000+只）
- `get-all-us-quotes` - 全美股（8000+只）

### 三、K线数据
- `get-kline-with-indicators` - 带技术指标的K线（核心）
- `get-history-kline` - A股历史K线
- `get-hk-history-kline` - 港股历史K线
- `get-us-history-kline` - 美股历史K线
- `get-minute-kline` - 分钟K线
- `get-today-timeline` - 当日分时

### 四、板块数据
- `get-industry-list/spot/constituents/kline` - 行业板块
- `get-concept-list/spot/constituents/kline` - 概念板块

### 五、扩展功能
- `get-fund-flow` - 资金流向
- `get-panel-large-order` - 盘口大单
- `get-trading-calendar` - 交易日历
- `get-dividend-detail` - 分红详情

---

## 注意事项

1. **批量查询**：`get-all-*` 系列数据量大，谨慎使用
2. **市场识别**：`get-quotes-by-query` 自动识别市场，最推荐
3. **技术指标**：`get-kline-with-indicators` 一次性获取K线和指标，效率最高
