---
name: transaction-management
description: >
  查询与记录用户的交易：入金、出金、买入、卖出，以及交易历史、按日期范围查询、交易摘要。
  当用户说"记一笔买入"、"帮我记录今天卖了 XX"、"查一下最近的交易"、"这个月的交易流水"、
  "买卖记录"、"入金了多少"，或要求基于交易记录做统计时，**务必使用此技能**。
version: "1.0.0"
category: portfolio
author: investment-agent
---

# 交易记录管理

## 记录新交易：addTransactionTool

用户委托记交易（"记一笔"、"帮我记录"）时调用 `addTransactionTool`。参数规则：

| 参数 | 必填条件 | 说明 |
|------|----------|------|
| `account_id` | 必填 | 账户 ID（字符串）。不确定时先用 `dbQueryTool` 查 `accounts` 确认，**禁止猜 ID** |
| `type` | 必填 | `deposit` 入金 / `withdrawal` 出金 / `buy` 买入 / `sell` 卖出 |
| `amount` | deposit / withdrawal 必填 | 金额（数值，不带货币单位符号） |
| `symbol` | buy / sell 必填 | 标的代码，如 `AAPL`、`600519`、`0700.HK` |
| `quantity` | buy / sell 必填 | 数量 |
| `price` | buy / sell 必填 | 单价 |
| `sector` | 可选 | `stock` / `etf` / `fund` / `crypto`，默认 `stock` |
| `market` | 可选 | `US` / `CN` / `HK` |
| `description` | 可选 | 交易描述 |
| `trade_time` | 可选 | ISO 格式；用户没说时间就不要编造，留空用默认 |

流程：确认账户 → 确认关键字段取值 → 执行 → 向用户复述记录内容。**写入操作必须复述确认的数据再返回**，字段不清楚就问，不要代填。

## 查询

- 最近交易：`transactionHistoryTool`（`limit` 默认 50，`offset` 翻页）。
- 日期范围：`transactionHistoryByDateTool`，参数 `start_date` / `end_date`（YYYY-MM-DD）。相对日期（"这个月"、"上周"）必须先换算成具体日期。
- 交易摘要（Markdown 汇总）：`transactionSummaryTool`。
- 资金余额变化：配合 `accountBalanceTool`。

## 统计口径

- 盈亏、平均成本等派生指标由交易记录计算时，注明计算窗口（时间范围、账户、标的）。
- buy/sell 金额 = quantity × price；如果两笔字段可疑（数量或价格异常），指出并把原始数据贴出来，不要静默纠正。

## 限制

- 修改、删除已有交易记录没有对应工具；发现错误记录时明确告知用户到应用界面处理。
