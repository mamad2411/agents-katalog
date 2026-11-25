---
name: risk-management
description: Risk management domain knowledge for trading agents — affective state monitoring, position sizing, drawdown management, tilt detection, and behavioral guardrails. Use when checking risk before trades, managing drawdowns, detecting behavioral drift, or enforcing discipline. Triggers on "risk", "drawdown", "tilt", "position size", "lot size", "confidence", "revenge trading", "overtrading", "discipline".
---

# Risk Management

## Overview

Risk management in TradeMemory is behavioral, not just mathematical. Traditional risk management calculates position sizes and stop losses. TradeMemory adds a behavioral layer: it monitors your execution patterns, detects emotional drift, and flags when you're deviating from your own rules.

The system tracks two kinds of risk:
1. **Position risk** — How much capital is at stake on each trade
2. **Behavioral risk** — Are you making decisions rationally or emotionally

## Affective State Model

TradeMemory maintains a real-time emotional state model for the trading agent:

| Dimension | Range | What It Tracks |
|-----------|-------|----------------|
| Confidence | 0.0 - 1.0 | Self-assessed confidence, calibrated against outcomes |
| Drawdown | 0% - 100% | Current peak-to-trough equity drawdown |
| Win Streak | 0 - N | Consecutive winning trades |
| Loss Streak | 0 - N | Consecutive losing trades |
| Risk Appetite | low / normal / high | Derived from confidence + drawdown + streaks |

### How Affective State Updates
- **After a win**: Confidence += f(P&L magnitude), win streak ++, loss streak reset
- **After a loss**: Confidence -= f(P&L magnitude), loss streak ++, win streak reset
- **Drawdown crossing thresholds**: Risk appetite auto-reduces at 5%, 10%, 15% drawdown
- **Daily review**: Confidence recalibrated against actual hit rate

### Using Affective State

Check `get_agent_state` before every trading session:

```
get_agent_state() → {
  confidence: 0.42,
  drawdown: 8.3%,
  win_streak: 0,
  loss_streak: 3,
  risk_appetite: "low"
}
```

**Action rules:**
- `risk_appetite == "low"` → Reduce position size by 50% or skip marginal setups
- `loss_streak >= 3` → Stop trading for the session. Review, don't revenge trade.
- `confidence < 0.3` → Paper trade only until confidence recovers
- `drawdown > 15%` → Hard stop. No new positions until daily review.

## Behavioral Risk Indicators

### 1. Disposition Effect
**What**: Cutting winners short and holding losers too long.
**Detection**: `get_behavioral_analysis` → `disposition_ratio`
- Ratio < 1.0 = Good (holding winners longer than losers)
- Ratio > 1.5 = Problem (losers held 50% longer than winners)
- Ratio > 2.0 = Critical (classic retail trader failure mode)

### 2. Revenge Trading
**What**: Increasing position size or trade frequency after losses.
**Detection**: Compare lot sizes and trade count in the N trades after a losing streak vs baseline.
- Lot size > 1.5x baseline after loss = Revenge sizing
- Trade frequency > 2x baseline after loss = Overtrading

### 3. Overtrading
**What**: Taking more trades than the strategy generates signals for.
**Detection**: Compare actual trade count vs strategy signal count.
- If strategy generates 3 signals/week but you take 10 trades/week, you're inventing trades.

### 4. Session Drift
**What**: Trading outside designated sessions.
**Detection**: Check trade timestamps against strategy's defined trading windows.
- VolBreakout is a London session strategy. Trades at 3am UTC = session drift.

### 5. Confidence Miscalibration
**What**: Your confidence doesn't match your actual accuracy.
**Detection**: `get_behavioral_analysis` → confidence calibration curve.
- If trades rated confidence 0.8 win only 40% of the time, your confidence is miscalibrated.

## Position Sizing Rules

TradeMemory's procedural memory tracks position sizing patterns:

### Fixed Fractional
Default: Risk X% of equity per trade (typically 0.25-2%).

```
Position Size = (Equity × Risk%) / (Entry - StopLoss)
```

### Kelly Criterion
Optimal sizing based on historical edge:

```
Kelly% = WinRate - (LossRate / AvgWin÷AvgLoss)
```

- Full Kelly is too aggressive for real trading. Use Half Kelly or Quarter Kelly.
- `get_behavioral_analysis` returns Kelly criterion values per strategy.

### Lot Sizing Variance
Procedural memory tracks how consistent your sizing is:
- Low variance = Disciplined execution
- High variance = Emotional sizing (bigger when confident, smaller when scared)
- Target: coefficient of variation < 0.2

## Best Practices

### Before Every Session
1. Check `get_agent_state` — is confidence reasonable? Any active streaks?
2. Check drawdown — are you within acceptable limits?
3. Review active trading plans — don't enter trades outside your plans

### After Every Trade
1. Record the trade with `remember_trade` — include honest reflection
2. Did the trade match your strategy rules? If not, why?
3. Was position sizing consistent with your risk rules?

### After a Losing Streak (3+ consecutive losses)
1. **Stop trading.** Not permanently — just for the current session.
2. Run `/daily-review` — is there a systematic problem or just variance?
3. Check disposition ratio — are you holding losers too long?
4. Reduce position size for the next 5 trades (half the normal size)
5. Only resume full size after 2 consecutive wins at reduced size

### After a Winning Streak (5+ consecutive wins)
1. **Don't increase size.** Winning streaks end. Mean reversion is real.
2. Check if you're cherry-picking easy setups and avoiding harder (but higher EV) ones
3. Review: are the wins from your strategy or from a favorable market regime?

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| No pre-session risk check | Walk into the market emotionally unprepared | Always run `get_agent_state` first |
| Ignoring drawdown thresholds | Small drawdowns become account-threatening drawdowns | Hard stop at 15% drawdown |
| Sizing up after wins | Gives back profits faster when the streak breaks | Keep sizing constant |
| Sizing down after losses | Reduces recovery speed when edge reasserts | Keep sizing constant (unless risk appetite is "low") |
| Skipping daily reviews | Behavioral drift goes undetected for days | Daily reviews are non-negotiable |
| Paper trading with different sizing | Paper P&L doesn't reflect real execution | Same sizing rules for paper and live |
