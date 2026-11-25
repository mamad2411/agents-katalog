---
name: option-chain-analyzer
description: Analyses NSE option chain data for Nifty/BankNifty/stock options — computes IV, OI build-up, max pain, PCR, and key support/resistance from strike-wise OI. Trigger when user asks about option chain, max pain, PCR, OI buildup, strike analysis, IV, or wants to read NSE/Sensibull-style data.
---

# Option Chain Analyzer

Turns a raw NSE option chain JSON into actionable structure.

## When to use

- User pastes / fetches option chain data and asks for a read.
- User wants to identify max pain, PCR, or notable OI build-up.
- Pre-market or intraday: "where is BankNifty likely to pin?"

## Inputs

Either:
- A JSON dump from NSE's option chain endpoint (`https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY`), or
- Strike-wise call/put OI + premium tabular data.

## Computations

### Max pain
Strike at which total OI value (writers' loss) is minimised. Often acts as a magnet near expiry.

```
max_pain_strike = argmin over K of: sum_i max(K - K_i, 0) * call_OI_i + max(K_i - K, 0) * put_OI_i
```

### PCR (Put-Call Ratio)
```
PCR_OI = total_put_OI / total_call_OI
```
- > 1.3 → oversold / bullish reversal zone (contrarian read)
- < 0.7 → overbought / bearish reversal zone
- 0.8–1.2 → neutral

### Support / Resistance from OI
- **Strongest resistance** = strike with highest call OI above spot.
- **Strongest support** = strike with highest put OI below spot.

### OI build-up classification
| Price | OI | Reading |
|---|---|---|
| ↑ | ↑ | Long build-up |
| ↑ | ↓ | Short covering |
| ↓ | ↑ | Short build-up |
| ↓ | ↓ | Long unwinding |

### IV skew
Compare ATM call IV vs ATM put IV. Put IV > call IV → fear premium. Useful for direction bias before events.

## Output format

Return a structured summary:

```
Spot: 24,150
Max pain: 24,200 (likely pin near expiry)
PCR (OI): 1.18 → mildly bullish
Resistance: 24,300 CE (highest call OI)
Support: 24,000 PE (highest put OI)
Notable build-up:
  - 24,500 CE: short build-up (+3.2L OI, premium ↓)
  - 23,900 PE: long build-up (+2.1L OI, premium ↑)
```

## Caveats

- NSE data has ~3 min lag; max pain is a tendency, not a guarantee.
- On expiry day, max pain pull strengthens after 1 PM IST.
- Always check FII/DII data alongside — OI alone misses positioning context.
