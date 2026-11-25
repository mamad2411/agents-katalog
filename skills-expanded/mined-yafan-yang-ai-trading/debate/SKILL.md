---
name: debate
description: "多空辩论 — 看涨 vs 看跌研究员辩论，研究经理综合出结论"
metadata:
  argument-hint: "<股票代码，如 600519>"
---

你将**独立扮演**多头研究员、空头研究员与研究经理三个角色，对 **$ARGUMENTS** 展开一轮投资辩论并给出结论。

## 第一步：准备论据（获取真实数据）
```bash
$HOME/.ai-trading/.venv/bin/python $HOME/.ai-trading/tools/market_data.py $ARGUMENTS --json
$HOME/.ai-trading/.venv/bin/python $HOME/.ai-trading/tools/fundamentals.py $ARGUMENTS --json
$HOME/.ai-trading/.venv/bin/python $HOME/.ai-trading/tools/news_fetch.py $ARGUMENTS --limit 8 --json
```
所有论点必须由真实数据支撑，禁止编造。

## 第二步：辩论（对话式，互相反驳）

### 🐂 多头研究员
建立强有力的看涨论证，强调：增长潜力、竞争优势、积极财务/技术/新闻指标；并**反驳看跌观点**。

### 🐻 空头研究员
针对多头逐条反驳，强调：风险与挑战、竞争劣势、负面指标、估值过高或过度乐观的假设。

（两方各充分陈述一轮，直接回应对方论点。）

## 第三步：🧑‍⚖️ 研究经理裁决
批判性评估双方，明确选择支持看涨、看跌或持有（仅在确有强理由时选持有），并输出：
- **明确建议**：买入 / 持有 / 卖出
- **理由**：为什么这些论点最有说服力
- **战略行动**：具体执行步骤
- **📊 目标价格区间**：必须给出具体价位（正确货币单位），不得回复“无法确定”

## 输出格式（中文）
```
## 🐂 多头论点
## 🐻 空头论点
## 🧑‍⚖️ 研究经理结论（建议 / 理由 / 目标价 / 战略行动）
```

> 本分析仅用于研究和教育目的，不构成投资建议。投资有风险，决策需谨慎。
