---
name: trading
description: Route and manage trading/investing workflow skills — market breadth and uptrend participation scoring, exposure/posture synthesis, risk-based position sizing, drawdown circuit breaker, periodic portfolio review, dividend/value screening, and trade journaling. Use when the user asks for market-regime checks, position sizing, risk gates, portfolio review, or trade journaling/stats.
---

# Trading Skills

Use this skill to find the right trading/investing skill in `skills/trading/`.

## Purpose

`skills/trading/` is a workflow toolkit for a **time-constrained individual investor** — long-term/dividend/ETF core holdings, plus disciplined swing trading as a satellite strategy, plus general market-awareness. It structures market review, risk management, and trade journaling. **It is not a signal service and does not place trades.** Every skill in this category treats the human as the decision-maker; the skills compute numbers and structure checklists, they don't recommend trades.

Pattern inspired by [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) (MIT) — see `NOTICE.md` for attribution. That source repo has 71 skills; this starter set (9 skills) covers the three areas actually in use here (long-term/dividend investing, disciplined swing trading, general market awareness) rather than replicating the full catalog. Expand it the same way `thai/` was expanded — pick one gap at a time, verify it, register it.

## Skills in this category

| Skill | Purpose | Area |
|---|---|---|
| [market-breadth-analyzer](market-breadth-analyzer/SKILL.md) | % of a universe trading above a moving average, from a CSV | Market regime |
| [uptrend-analyzer](uptrend-analyzer/SKILL.md) | % of a universe in an established "stage 2" uptrend structure | Market regime |
| [exposure-coach](exposure-coach/SKILL.md) | Combines breadth + uptrend + drawdown state into one exposure-ceiling read | Market regime |
| [position-sizer](position-sizer/SKILL.md) | Risk-based share sizing (fixed-fractional, ATR-based, Kelly) | Swing / risk |
| [drawdown-circuit-breaker](drawdown-circuit-breaker/SKILL.md) | Mechanical size-reduction/halt rule after account drawdown | Swing / risk |
| [portfolio-manager](portfolio-manager/SKILL.md) | Periodic core-portfolio review checklist (concentration, rebalance, dividends) | Core portfolio |
| [dividend-value-screener](dividend-value-screener/SKILL.md) | Value/dividend-quality screening checklist, yield-trap detection | Core portfolio |
| [trader-memory-core](trader-memory-core/SKILL.md) | Trade journal schema + win rate / R-multiple / expectancy stats | Trade memory |
| [backtest-expert](backtest-expert/SKILL.md) | Simulate a long-only rule (or MA-crossover) against historical prices — win rate, drawdown, profit factor | Strategy validation |

**Suggested chain for a daily/weekly market check**: market-breadth-analyzer + uptrend-analyzer → exposure-coach → (if opening new risk) position-sizer, gated by drawdown-circuit-breaker → close the loop with trader-memory-core after the trade closes. **Before trusting a rule enough to trade it at all**, run it through backtest-expert first.

## Rules

- **Every skill in this category must carry a "not financial advice" disclaimer.** Treat it as load-bearing — do not remove it during later edits.
- No skill in this category executes trades, connects to a broker, or claims to predict future returns. If a request implies an automated signal/execution service, say so explicitly and decline that framing rather than building toward it.
- Illustrative thresholds (risk %, drawdown triggers, exposure bands) are starting heuristics, not validated rules — every skill that uses one says so and tells the user to tune it against their own history.
- Code-bearing skills operate on data the user supplies (CSV, account numbers, journal entries) — none of them fetch live market data. If live data integration is ever added, it needs its own explicit skill/tool with its own API-key and rate-limit handling, not folded silently into these.

## Known limitations

- This is a starter set (9 of the source repo's 71 skills), chosen for long-term/dividend investing, disciplined swing trading, and general market awareness. Screener skills that need live technical/fundamental data (breakout screeners, earnings calendars, full CANSLIM/VCP screening) are still out of scope — the source repo's `docs/en/skills/` catalog is the reference if/when those get added.
- Market-structure heuristics (uptrend definition, breadth interpretation bands, exposure thresholds) reflect common, widely-cited conventions, not a single "correct" methodology — different traders/strategies define these differently.
