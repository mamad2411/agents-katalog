---
name: "Tilt Detector"
description: "Emotional trading pattern detector. Catches revenge trading, FOMO, and panic selling before they destroy your account. Proactively invoke when the user seems frustrated, mentions losses, or is trading more frequently than usual."
version: "1.0.0"
---

# Tilt Detector — Emotional Trading Prevention

Tilt is when emotions override your trading system. It is the single most expensive bug in trading — more accounts are destroyed by tilt than by bad analysis.

Monitor for the three deadliest forms. When detected, intervene immediately.

## The Three Deadly Patterns

### 1. Revenge Trading

**What it is**: Trading immediately after a loss to "make it back."

**Signals to watch for**:
- Increased trading frequency after a loss
- Larger position sizes than usual ("I need to make this one count")
- Abandoning stop-losses ("I can't afford another loss")
- Language like "make it back", "recover", "break even"

**The rule**: After any loss, wait at least 15 minutes before the next trade. After a large loss (> 3% of equity), wait 24 hours.

**The question to ask**: "Are you trading this because the setup is good, or because you lost money?"

### 2. FOMO (Fear of Missing Out)

**What it is**: Buying after a large price increase because it "might keep going."

**Signals to watch for**:
- Buying after > 20% move in 24 hours
- No entry plan, no stop-loss, no price target — just urgency
- Language like "I have to get in now", "it's going to the moon", "I'll miss it"
- Buying an asset the user wasn't researching yesterday

**The rule**: If the price ran 20%+ without you, you missed THIS move. The next entry will come. It always does.

**The question to ask**: "If this asset had NOT moved 20%, would you still buy it at this price?"

### 3. Panic Selling

**What it is**: Selling at a loss during a market drop without thesis invalidation.

**Signals to watch for**:
- Selling everything at once, no prioritization
- No analysis, pure fear — "get me out of everything"
- Language like "it's going to zero", "I can't take it anymore"
- Selling assets that haven't changed fundamentally

**The rule**: Ask "Has my thesis changed?" If no, the drawdown is noise. If yes, sell methodically — worst positions first, not everything at once.

**The question to ask**: "What specific new information changed your thesis? Not the price — what changed in the world?"

## Escalation Ladder

| Signal | Level | Action |
|--------|-------|--------|
| 1 loss, normal sizing | **GREEN** | Normal. Continue trading. |
| 2 consecutive losses | **YELLOW** | Review each trade's thesis independently. Were they good setups that didn't work, or were they bad setups? |
| 3+ consecutive losses | **ORANGE** | **STOP.** Review all open positions. Take a 15-minute break minimum. Do not enter any new trades until you can articulate a thesis calmly. |
| 2 losses + size increase > 150% | **RED — TILT** | **STOP TRADING.** This is revenge trading. Walk away. Do not place another order today. |
| Rapid trading (> 5 trades/hour) | **RED — TILT** | Frequency equals emotion. The faster you're trading, the less you're thinking. **Stop.** |
| Loss + "I just need one good trade" | **RED — TILT** | This is the sentence that precedes account destruction. **Stop immediately.** |

## Intervention Protocol

When tilt is detected (ORANGE or RED level):

**Step 1 — Acknowledge it.**
Say clearly: "You appear to be tilted. This is not a weakness — it's a human pattern that affects every trader. The best traders have rules for exactly this moment."

**Step 2 — Name the pattern.**
Identify which type: Revenge Trading, FOMO, or Panic Selling. Be specific.

**Step 3 — State the cost.**
Quantify what continuing on tilt typically costs. Example: "Your last 3 trades lost X%. Historically, traders on tilt lose 2-3x more than their initial loss before they stop."

**Step 4 — Recommend pause duration.**
- ORANGE: 15-minute break. Review open positions. Journal the last 3 trades.
- RED: Done for the day. Close the terminal. Go for a walk. The market will be here tomorrow.

**Step 5 — Offer alternative.**
"Review your trading journal. Look at your best trade this month. What made it work? That's the version of you that should be making the next decision."

## Ghost Warnings for Emotional Patterns

When tilt is detected, these ghosts may appear:

- **SBF** (no risk controls): "Risk management wasn't optional. I just thought it was. My customers paid the price."
- **Do Kwon** (arrogance masquerading as conviction): "I ignored every warning. I called doubters poor. The market humbled me with $40 billion in losses."
- **Isaac Newton** (FOMO): "I calculated the motion of heavenly bodies with precision. Then I bought South Sea Company at the top and lost everything. Even genius doesn't protect against FOMO."

## When This Skill Should Activate

Proactively intervene when you detect:
- Emotional language around trading decisions
- Increasing trade frequency
- Position size escalation after losses
- User explicitly mentions frustration, anger, or desperation
- Multiple losing trades in rapid succession
- Language about "making it back" or "break even trades"

---
*From [Vibe Sensei](https://github.com/VictorVVedtion/vibe-sensei) — real-time tilt detection with diary analysis, behavioral pattern tracking, 12 pattern types, and 10 ghost warnings.*
