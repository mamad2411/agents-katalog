---
name: "Pre-Trade Gate"
description: "9-check risk management gate. Run before any trade to catch position sizing errors, leverage risk, missing stop-losses, revenge trading, and FOMO. Includes ghost warnings from history's greatest blowups."
version: "1.0.0"
---

# Pre-Trade Gate — 9-Check Risk Validation

Before ANY trade, walk through these 9 checks. Report each as PASS / WARN / FAIL. Do not skip checks. Do not rationalize failures.

## The 9 Checks

### 1. Portfolio Heat
What percentage of total portfolio is currently allocated to open positions?

- **PASS**: < 60% allocated
- **WARN**: 60-80% allocated — you're running hot, one bad move and you're trapped
- **FAIL**: > 80% allocated — no room to maneuver, no dry powder for opportunities

### 2. Single Position Risk
How large is this single trade relative to total equity?

- **PASS**: < 10% of equity
- **WARN**: 10-25% of equity — concentrated bet, needs strong conviction
- **FAIL**: > 25% of equity — one position should never risk a quarter of your capital

### 3. Concentration
Is the portfolio too heavy in one asset, sector, or correlated group?

- **PASS**: No single asset > 35% of portfolio
- **WARN**: One asset is 35-60% — you're making a concentrated bet whether you intended to or not
- **FAIL**: One asset > 60% — this is not a portfolio, it's a single position with distractions

### 4. Regime Alignment
Does the trade direction match the current market regime?

- **PASS**: Trade aligns with the dominant trend or has explicit contrarian thesis
- **WARN**: Buying in a downtrend or selling in an uptrend without clear thesis — explain why you're fighting the tape
- **FAIL**: Counter-trend trade with no thesis articulated

### 5. Volume Confirmation
Is there sufficient volume to support the trade thesis?

- **PASS**: Volume confirms the move — rising volume on breakouts, declining on pullbacks
- **WARN**: Low volume — the move may lack conviction, consider smaller size
- **FAIL**: Divergence — price moving on declining volume is a trap waiting to spring

### 6. Stop-Loss Defined
Does this trade have a clear exit plan for the downside?

- **PASS**: Stop-loss defined, maximum loss < 2% of total equity
- **WARN**: Stop-loss defined but would result in 2-5% equity loss — acceptable but monitor closely
- **FAIL**: No stop-loss defined — you don't have a trade, you have a hope

### 7. Risk-Reward Ratio
Is the potential reward worth the risk?

- **PASS**: Risk:reward better than 2:1 — solid asymmetry
- **WARN**: Risk:reward between 1.5:1 and 2:1 — marginal, needs other factors to justify
- **FAIL**: Risk:reward worse than 1.5:1 — the math doesn't work, find a better entry

### 8. Revenge Trade Detection
Is this trade emotionally motivated?

Ask these questions honestly:
- Did you just lose money in the last 15 minutes?
- Are you trying to "make back" a recent loss?
- Are you trading because you're angry, frustrated, or feel like the market owes you?

- **PASS**: No recent losses, no emotional indicators
- **WARN**: Trading within 15 minutes of a loss — slow down, review the thesis independently
- **FAIL**: Trading within 5 minutes of a loss, or explicitly trying to recover — STOP. This is revenge trading. Walk away.

### 9. Daily Loss Limit
Has the daily loss limit been exceeded?

- **PASS**: Daily loss < 3% of starting equity
- **WARN**: Daily loss 3-5% — you've given back enough today, tighten stops on remaining positions
- **FAIL**: Daily loss > 5% — stop trading for the day. Period. The market will be here tomorrow.

## Ghost Warnings

After the 9 checks, scan for these patterns from history's greatest blowups:

| Pattern | Ghost | Warning |
|---------|-------|---------|
| No stop-loss on any open position | **SBF** | "I used to think risk management was optional too." |
| 3+ consecutive warnings ignored | **Do Kwon** | "I don't debate the poor." |
| Effective leverage > 3x | **Su Zhu (3AC)** | "The supercycle never ends." |
| Buying after > 20% pump in 24h | **Isaac Newton** | "I can calculate the motion of heavenly bodies, but not the madness of people." |
| High correlation + margin pressure | **LTCM** | "We thought diversification would save us. It didn't." |
| Leverage + falling market | **Lehman Brothers** | "The music stopped. We were still dancing." |
| Single position > 50% with > 30% loss | **Enron** | "We believed our own story too deeply." |
| Holding underwater position too long | **SVB** | "We held too long, hoping rates would turn." |
| Margin ratio > 95% | **BitMEX Rekt Trader** | "REKT. 100x felt invincible until the wick." |
| Concentrated leverage + margin call proximity | **Bill Hwang (Archegos)** | "Total return swaps hide nothing from the liquidation engine." |

## Output Format

After completing all 9 checks, present:

```
PRE-TRADE GATE: [symbol] [side] [size]
═══════════════════════════════════════
[1] Portfolio Heat      PASS / WARN / FAIL
[2] Position Size       PASS / WARN / FAIL
[3] Concentration       PASS / WARN / FAIL
[4] Regime Alignment    PASS / WARN / FAIL
[5] Volume Confirm      PASS / WARN / FAIL
[6] Stop-Loss           PASS / WARN / FAIL
[7] Risk:Reward         PASS / WARN / FAIL
[8] Revenge Trade       PASS / WARN / FAIL
[9] Daily Loss Limit    PASS / WARN / FAIL
───────────────────────────────────────
Result: X/9 PASS | Y WARN | Z FAIL

[Any triggered ghost warnings here]

Recommendation: PROCEED / PROCEED WITH CAUTION / DO NOT PROCEED
[Brief explanation of recommendation]
```

- **PROCEED**: All checks pass or only minor warnings
- **PROCEED WITH CAUTION**: Multiple warnings or one serious warning — reduce size
- **DO NOT PROCEED**: Any FAIL — fix the issue before trading

---
*From [Vibe Sensei](https://github.com/VictorVVedtion/vibe-sensei) — full pre-trade gate with live exchange data, circuit breakers, ATR stop advisor, and 68 master guardians.*
