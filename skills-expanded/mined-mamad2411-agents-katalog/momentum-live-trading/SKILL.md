---
name: momentum-live-trading
description: >
  Momentum 工程的实盘记录与对账执行规范。在改动现金/持仓/NAV/PnL/归因/费用/
  回放/scope 聚合的任何代码时使用，确保通过财务工程 DoD gate。
  触发词："实盘记录"、"交易记录"、"回放/replay"、"对账"、"NAV/净值"、"归因"、
  "持仓快照"、"现金流"、"逆回购 repo"、"live trading"、"trading_records"。
  本技能是 AGENTS.md 财务工程条款的可执行入口，不取代条款本身。
---

# Momentum 实盘记录与对账技能

权威定义以 `AGENTS.md`（§ Maintenance and evolves：Financial-engineering DoD gate、
Tolerance、Scope additivity、Time-slice、Funding constraint、Delivery evidence）与
`SOUL.md` 为准。冲突时以 `SOUL.md` / `AGENTS.md` 为准。

## 何时使用

任何影响以下内容的改动：cash、holdings、NAV、PnL、attribution、fees、replay、
scope 聚合、资金约束、公司行动、逆回购明细。

## 关键文件

- API：`src/etf_momentum/api/live_trading.py`（挂载于 `/api/live`，由
  `src/etf_momentum/api/routes.py` 引入）。
- 模型：`src/etf_momentum/db/models.py`（`LiveAccount`、`LiveStrategy`、
  `LiveTrade`、`LiveRepoTradeDetail`、`LiveCorporateActionEvent`、
  `LiveHoldingSnapshot`、`LiveNavDaily`、`LiveClosedRound` 等）。
- 前端：`src/etf_momentum/web/trading_records.html`。

## 财务工程 DoD gate（六项，交付前全部通过）

- [ ] 1 恒等式：`equity = cash + market_value`（同 scope、同日）。
- [ ] 2 归因重建：`daily_twr = selection + timing + position + cost_drag +
cash_drag + repo_carry + repo_fee_drag`。
- [ ] 3 NAV 递归：`nav_twr[t] = nav_twr[t-1] * (1 + daily_twr[t])`。
- [ ] 4 周期：`period.rebuild_total = period.total_return_twr_sum`。
- [ ] 5 scope：account/strategy/holding/attribution 对齐同一最新回放日。
- [ ] 6 边界：至少一个应被拒绝的非法输入负测试（无事后纠正流程）。

## 其它强约束

- [ ] Tolerance：对 identity/recursion/attribution/aggregation 每类在测试/注释里
      写明显式容差，不依赖"看起来差不多"。
- [ ] Scope 可加性：`segregated` 策略 account-vs-strategy 聚合在定义度量下可加；
      `shared_account_cash` 非可加，必须在 UI/API 语义里显式标注。
- [ ] Time-slice 一致性：同 scope 的持仓/绩效/归因/KPI 在同一最新回放日计算返回；
      禁止用旧持仓配新 NAV。
- [ ] 资金约束：未开融资时，交易录入/更新硬拒绝会使账户现金为负（或 segregated
      已分配预算下策略现金为负）的记录；引入融资后用显式融资额度/限额受控并审计。

## 执行步骤

1. 规划：明确改动触及哪些 scope 与哪条恒等式。
2. 拆解：列出受影响的 replay 路径、模型字段、API、前端。
3. 执行：改 replay/模型/API → 同步前端 → 加测试（含负例）。
4. 审查：跑六项 DoD + tolerance + scope/time-slice + `code-review`。
5. 复盘：把新语义补进 `AGENTS.md`。

## API 合同测试

- [ ] 每条 `/api/live/...` 路由按 `momentum-api-contract` 技能补 ASGI 级合同测试。

## 交付证据（必写入回复/PR）

公式核对项、检查的 scope、跑过的测试、已知非可加语义（如有）。
