---
name: daily-risk-pack
description: 每日风险包——并行运行 VaR/回撤/限额三类 Subagent，汇总红绿灯报告
inputs: []
outputs:
  - daily_risk_<date>.md
  - daily_risk_<date>.json
---

# Trust Boundary

持仓数据属于 Restricted Tier，所有 Subagent 只通过 mcp.portfolio 访问。
本 Skill 输出报告不对外发送，只在风控团队内部使用。

# 步骤 1：并行运行三类 Subagent

同时调用（不等前一个完成再启动下一个）：
- var-monitor（计算组合 VaR/ES，独立重算）
- drawdown-monitor（计算最大回撤，三色预警）
- position-limit-monitor（仓位限额逐条检查）

# 步骤 2：汇总结果

收集三个 Subagent 的 JSON 输出，判断整体风险等级：
- GREEN：全部 PASS，无 Yellow / Red Alert
- YELLOW：有 Yellow Alert，无 Red Alert
- RED：任意 Red Alert 或超限

# 步骤 3：输出每日风险报告

## 每日风险包（{日期}）

**整体状态**：[GREEN / YELLOW / RED]

| 指标 | 当前值 | 限额 | 使用率 | 状态 |
|---|---|---|---|---|
| VaR (95%, 1D) | X% | Y% | Z% | |
| ES (95%, 1D) | X% | Y% | Z% | |
| 最大回撤 (30D) | X% | Y% | - | |
| 超仓位限额数 | X 条 | 0 | - | |

# 步骤 4：审计日志

每次运行必须记录（保存 6 个月）：
```json
{
  "run_time": "",
  "overall_status": "",
  "var_pass": true,
  "drawdown_status": "",
  "limit_breaches": 0,
  "human_confirmed_by": "",
  "human_confirmed_at": ""
}
```
