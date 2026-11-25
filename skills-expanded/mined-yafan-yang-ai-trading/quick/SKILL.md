---
name: quick
description: "快照分析 — 60秒快速判断（单代理，不做多智能体辩论）"
metadata:
  argument-hint: "<股票代码，如 600519 / 0700.HK / AAPL>"
---

对 **$ARGUMENTS** 做一次快速分析（不启动多智能体辩论，追求速度）。

## 取数（真实数据，禁止编造）
```bash
$HOME/.ai-trading/.venv/bin/python $HOME/.ai-trading/tools/market_data.py $ARGUMENTS --json
$HOME/.ai-trading/.venv/bin/python $HOME/.ai-trading/tools/fundamentals.py $ARGUMENTS --json
```

## 输出（简洁，中文，一屏内）
```
## ⚡ {名称}（{代码}）快照
- 最新价 / 近期涨跌 / 技术面一句话（趋势+RSI+MACD）
- 估值一句话（PE/PB + 高估/低估）
- 财务一句话（ROE/增长/负债）

## 🎯 快速结论
倾向：偏多 / 偏空 / 中性 ｜ 关键理由（1-2 条）｜ 需关注的风险（1 条）
```

如需完整多智能体研报，改用 `/ai-trading:analyze $ARGUMENTS`。

> 仅用于研究和教育目的，不构成投资建议。投资有风险，决策需谨慎。
