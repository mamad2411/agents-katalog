---
name: finance-quant-backtesting-team
description: 从A股/期货历史数据获取到量化策略编写、多因子选股模型、回测引擎执行，再到生成包含胜率、收益率、夏普比率、最大回撤等核心指标的专业回测报告的完整量化交易工作流。支持经典策略（双均线、网格交易、突破策略）、事件驱动策略和因子分析。
---

# 量化回测

Use this skill as the routing entry point for the 量化回测 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$joinquant`
- `$stock-strategy-backtester`
- `$quant-backtest-strategy`
- `$quant-strategy`
- `$quant`
- `$openclaw-backtester`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
