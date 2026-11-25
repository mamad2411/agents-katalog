---
name: position-sizer
description: Use this skill to calculate a risk-based position size (how many shares to buy) from an account size, risk tolerance, entry price, and stop distance. Trigger on "how many shares should I buy", "position size", "risk per trade", "ATR-based stop", "Kelly criterion", "risk 1% of account". If the user hasn't given a stop-loss level or risk percentage, ask for those before calculating — sizing without a defined risk per trade isn't really position sizing.
---

# Position Sizer

## Overview

"How many shares should I buy?" only has a defensible answer once you know how much you're willing to lose if the stop is hit. This skill does the arithmetic — fixed-fractional risk sizing, ATR-based stop distance, and Kelly criterion — on numbers the user supplies. It does not fetch prices or recommend a trade.

**Not financial advice.** This calculates how many shares fit a chosen risk budget; it does not evaluate whether the trade itself is a good idea.

## When to use

- คำนวณจำนวนหุ้นที่ควรซื้อ ตามความเสี่ยงที่รับได้ต่อไม้
- Sizing a position given account equity, entry price, and a stop-loss level
- Converting ATR (Average True Range) into a volatility-scaled stop and matching position size
- Estimating a Kelly-criterion fraction from historical win-rate/win-loss stats (as an upper bound, not a recommendation — see Known limitations)

## When NOT to use

- No stop-loss level or risk percentage has been specified — ask for these first; sizing "how many shares fit my account" without a risk budget is really just "how much can I afford," a different question
- The user wants a signal on whether to take the trade at all — this skill only sizes a trade already decided on

## Core knowledge

**Fixed-fractional sizing**: risk a fixed percentage of account equity per trade.

```
dollar_risk_per_share = |entry_price - stop_price|
total_risk_amount = account_equity × risk_pct
shares = floor(total_risk_amount / dollar_risk_per_share)
```

Shares are always rounded **down** so actual dollar risk never exceeds the budget. Common `risk_pct` defaults discussed in trading literature range roughly 0.5%-2% per trade — this skill doesn't assert a "correct" number; ask the user or use their stated tolerance.

**ATR-based stop**: instead of a fixed percentage stop, scale the stop distance to the security's own recent volatility: `stop_price = entry_price - (ATR × multiplier)`, commonly multiplier 1.5-3×. Then size with the same fixed-fractional formula using this derived stop distance.

**Kelly criterion**: `f = win_rate - (1 - win_rate) / b`, where `b = avg_win / avg_loss`. This gives the theoretically optimal fraction of capital to risk **given accurate win-rate/win-loss inputs** — in practice those inputs are estimated from limited history and are often wrong, so full Kelly is aggressive and prone to large drawdowns from estimation error. Traders commonly use a fraction of it ("half Kelly" or less). This skill returns the raw fraction and does not apply that discount — treat it as an upper bound to discuss, not a size to use directly.

## Common mistakes

1. Sizing a position without a defined stop — there's no "risk per share" to base the calculation on.
2. Rounding shares up instead of down — rounding up means actual dollar risk can exceed the stated budget.
3. Using full Kelly fraction directly as a position size without acknowledging estimation-error risk.
4. Treating ATR multiplier or risk percentage as fixed universal constants — both are user/strategy-specific choices this skill takes as parameters, not defaults to assert.
5. Confusing `dollar_risk_per_share` (entry-to-stop distance) with `position_value` (entry price × shares) — a small risk-per-share doesn't mean a small total position value; report both.

## Code

`size.py` — pure Decimal arithmetic, no dependencies:

- `fixed_fractional_size(account_equity, risk_pct, entry_price, stop_price)` → `SizeResult(shares, dollar_risk_per_share, total_risk_amount, actual_risk_amount, position_value)`
- `atr_based_stop(entry_price, atr, multiplier=2.0)` → stop price
- `atr_based_size(account_equity, risk_pct, entry_price, atr, multiplier=2.0)` → `SizeResult`, derives the stop from ATR first
- `kelly_fraction(win_rate, avg_win, avg_loss)` → raw Kelly fraction (see caveat above)

Run `python3 size.py` for the self-test.

## Known limitations

- Does not model fractional shares, lot-size minimums, or broker-specific constraints — output is whole shares only.
- Does not account for commissions/slippage in the risk calculation.
- Kelly fraction is highly sensitive to input estimation error — never present the raw output as a recommended size without flagging that.
