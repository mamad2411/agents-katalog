---
name: daily-pnl-reviewer
description: End-of-day review skill for Indian intraday traders — analyses today's trades, computes win rate / expectancy / max DD, flags behavioural patterns (revenge trading, oversizing, time-of-day skew), and writes a journal entry. Trigger after market close, when reviewing trade logs, or when user says "review my day".
---

# Daily P&L Reviewer

The trade is only half the work. The review is where edge gets built.

## When to use

- After 15:30 IST when market is closed.
- User uploads / points to today's trade log (JSON / CSV / SQLite).
- User asks "how did I do today" or "review my trades".

## Inputs expected

A list of trades with at minimum:
- entry_time, exit_time
- instrument, side, qty
- entry_price, exit_price
- pnl (₹)
- rationale / setup tag (optional but valuable)

## Metrics to compute

### Performance
- Net P&L (after estimated STT + brokerage + GST)
- Win rate = wins / total
- Avg win, avg loss, **expectancy** = (win_rate × avg_win) − (loss_rate × avg_loss)
- Profit factor = total wins ₹ / total losses ₹

### Risk
- Max intraday drawdown
- Largest single loss as % of starting capital
- Did daily loss cap trigger?

### Behavioural flags (these matter more than P&L)

| Flag | How to detect |
|---|---|
| **Revenge trading** | New entry within 5 min of a losing exit, larger size than baseline |
| **Oversizing** | Position size > 2× median for the day |
| **Late-day chasing** | New entries after 14:45 IST that aren't part of a closing-bell setup |
| **Setup drift** | Trades without a tagged setup, or "vibe" entries |
| **Holding losers** | Avg time-in-loss > 1.5× avg time-in-win |

## Output: the journal entry

Write to `~/projects/zerodha-signal-app/journal/YYYY-MM-DD.md` (or user-specified path):

```markdown
# 2026-06-06 — Trading Journal

## Numbers
- Net P&L: ₹+2,340 (2.3% on ₹1L)
- Trades: 6 (4W / 2L), win rate 67%
- Expectancy: ₹+390 / trade
- Max DD: ₹-1,100 at 11:42 IST

## What worked
- 09:30 ORB on BankNifty — clean, on-plan, sized right.

## What didn't
- 13:15 CE buy on Nifty — entered without OI confirmation, exited for -₹600.

## Behavioural flags
- ⚠ Revenge entry at 13:25 (within 5 min of loss). Recovered, but pattern noted.

## Tomorrow's focus
- Don't enter inside 12:30–13:30 chop unless setup is A+.
```

## Tone

Honest, blunt, no pep talk. Treat the user as an adult building a process.
