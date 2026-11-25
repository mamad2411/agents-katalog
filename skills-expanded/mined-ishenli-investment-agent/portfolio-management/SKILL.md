---
name: portfolio-management
description: >
  查询与分析用户的投资组合：交易账户、可用资金、当前持仓、行业分布、历史收益与组合快照。
  当用户询问"我的账户余额"、"资金情况"、"现在有哪些持仓"、"仓位分布"、"持仓收益"、
  "账户资产"、"组合表现"，或要求基于真实持仓进行分析时，**务必使用此技能**。
version: "1.0.0"
category: portfolio
author: investment-agent
---

# 投资组合查询与分析

用户问及"自己的"资产、账户、持仓、资金时，必须查询真实数据，禁止凭空编造或沿用上一次对话的记忆。

## 账户与资金

- 余额：调用 `accountBalanceTool`（可直接读取账户资金字段；传 `before_transaction_id` 可计算到某笔交易之前的余额）。
- 账户列表 / 市场与币种：`dbQueryTool` 查表 `accounts`（列：account_name, market, currency, userId）。
- 已删除账户会自动过滤，无需担心脏数据。

## 持仓

用 `dbQueryTool` 查表 `asset_positions`（列：account_id, symbol, quantity, average_price_cents, sector, currency；`sector` 取值 stock/etf/fund/crypto）：

```json
{"table": "asset_positions", "orderBy": "quantity", "orderDirection": "DESC", "limit": 50}
```

- 聚焦某个账户时加条件：`{"table": "asset_positions", "whereColumn": "account_id", "whereValue": 1}`。
- 平均成本以"分"为单位（average_price_cents），金额计算时除以 100。市值全部以分计价，换算时注意。
- 类型分布：按 `sector` 字段在回答中分组统计，不要逐行罗列全部记录。

## 快照与收益

- 组合快照：`dbQueryTool` 查表 `portfolio_snapshots`（列：account_id, snapshot_date, total_value_cents, cash_balance_cents, positions 为 JSON 持仓明细），适合做净值曲线、期间对比。
- 收益指标：表 `revenue_metrics`。
- 交易流水：见 `transaction-management` 技能（不要用 dbQuery 逐笔查交易再做账户级汇总，优先用工具）。

## 组合分析要求

1. 先拿全量持仓与账户，再下结论；给出文字结论 + 分组数据。
2. 集中度分析：单一标的或单一 sector 占比超过默认阈值（如 40%）时必须提示。
3. 涉及市值/收益计算时，用 `stockGetPriceTool` 取最新价格配合持仓数量计算，并注明计算口径与价格时点。
4. 无法获取价格时明确说明，不要估算后冒充实测值。

## 限制

- 本技能只做查询与分析。重开账户、修改账户等管理操作不在 Agent 能力范围内，提示用户去应用对应页面完成。
