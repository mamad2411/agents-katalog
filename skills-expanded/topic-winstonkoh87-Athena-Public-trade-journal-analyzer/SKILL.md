---
name: trade-journal-analyzer
description: "Unified post-trade analytics: journal pattern extraction + drawdown classification. Absorbs: drawdown-classifier."
argument-hint: "analyze journal | patterns | edge audit | classify drawdown | is this noise or real"
allowed-tools:
  - Read
  - Bash
auto-invoke: true
model: default
context_trigger: "analyze trades, journal patterns, win rate, edge audit, losing streak, drawdown, is my system broken, trade review"
---

# Trade Journal Analyzer (Expanded)

> **Absorbs**: `drawdown-classifier`

Reads historical trade entries, extracts actionable statistical patterns, AND classifies drawdowns. Converts a "diary" into a "data warehouse."

## Triggers

"analyze my trades", "journal patterns", "what's my actual WR", "edge audit", "losing streak", "drawdown", "is my system broken", "should I stop trading", "3 losses in a row"

## Core Analytics

1. **Ingest**: Read entries from `.context/trading_journal/`.
2. **Parse**: Extract setup type, instrument, direction, entry, SL, TP, result, notes.
3. **Analyze**:
   - **Win Rate by Setup Type**: Which setups are actually profitable?
   - **Win Rate by Instrument**: Where is the edge strongest?
   - **Win Rate by Time of Day**: Asian vs London vs NY session performance.
   - **Average R:R Achieved**: Planned RR vs actual RR (execution gap).
   - **Drawdown Sequences**: Longest losing streaks, recovery time.
   - **Edge Decay**: Is WR trending up or down over last 20 trades?
4. **Flag**:
   - Setups with WR < breakeven threshold → flag for review or removal.
   - Instruments with consistent negative EV → stop trading them.
   - Emotional notes correlation → do emotional trades have lower WR?

## Drawdown Classification

Not all drawdowns are equal. The wrong response is more dangerous than the drawdown itself.

### Class 1: Noise (Random Variance)

- Losing streak within expected statistical bounds for the system's WR.
- **Test**: At 60% WR, a 5-loss streak has P = 0.4^5 = 1.02%. Over 200 trades, ~2 expected.
- **Response**: **Do nothing.** Continue executing. Do NOT adjust.

### Class 2: Structural (Setup Flaw)

- Losses concentrated in a specific setup, instrument, or time period.
- **Test**: Is the WR decline isolated to one setup type?
- **Response**: **Quarantine the specific setup.** Continue trading others.

### Class 3: Thesis-Breaker (Edge Invalidation)

- Systematic WR decline across ALL setups.
- **Test**: Is the WR decline persistent (>30 trades)? Has market microstructure changed?
- **Response**: **Full stop.** Trigger `circuit-breaker`. Paper trade. Re-validate edge.

## Output Format

```markdown
## Trade Journal Analysis (Last N Trades)

### Win Rate by Setup
| Setup | Trades | Wins | WR | Avg RR | EV/Trade |
|-------|--------|------|----|--------|----------|

### Win Rate Trend (Rolling 20)
[Trending UP / DOWN / FLAT] — current WR: XX%

### Drawdown Classification
Observed: X losses in last Y trades
P(this streak | WR=Z%): XX.X%
Classification: [NOISE / STRUCTURAL / THESIS-BREAKER]
Prescribed Action: [Continue / Quarantine setup X / Full stop]

### Edge Health
Verdict: [HEALTHY / DECAYING / CRITICAL]
```

## Integration

- Feeds into `zenith-execution` for forward simulation (Monte Carlo)
- Validates Kelly assumptions (is the stated WR real?)
- Triggers `circuit-breaker` if edge decay is CRITICAL
