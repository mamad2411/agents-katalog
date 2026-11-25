---
name: tolerance-stackup
description: Runs 1-D tolerance stack-ups (worst-case, RSS, Monte Carlo) on a dimension chain, ranks contributors, and estimates reject rate against a gap spec. Use when the user asks about tolerance stack-up, gap/interference analysis, clearance between parts, or how to allocate tolerances.
---

# Tolerance Stack-up

## Workflow

1. **Define the gap.** Name the gap being studied and its spec (LSL / USL). Draw the loop in text:
   `Housing face → bore bottom (+) → bearing (−) → spacer (−) → gear hub (−) → gap`.
2. **Build the chain CSV** (`scripts/example_chain.csv` shows the format). Rules:
   - Go around the loop in one direction; dimensions pointing the "positive" way are `+1`, the rest `-1`.
   - Enter unequal tolerances as `plus`/`minus` (both positive numbers). The script handles mean shift.
   - `dist`: `normal` for controlled processes (set `cpk`), `uniform` for unknown processes or purchased parts with no data.
   - Convert GD&T to ± equivalents first: position Ø0.2 → ±0.1 radial; flatness/parallelism add as their own rows.
3. **Run:**
   ```bash
   python scripts/stackup.py chain.csv --lsl 0.10 --usl 0.60 --out stack
   ```
4. **Interpret**
   - Worst-case OK → done; tolerances can be loosened.
   - Worst-case fails but RSS / MC passes → acceptable for high volume if the processes really are in control; state the predicted ppm.
   - MC reject > 2700 ppm (beyond ±3σ) → redesign: tighten the top 1–2 contributors only, or add an adjustment (shim, slotted hole).
5. **Recommend tolerance reallocation**: tighten the contributors with the largest `pct_rss` first; loosen the ones under 5%.

## Output format
- Loop diagram (text) and the chain table
- Results table: Nominal | Worst-case min/max | RSS min/max | MC ±3σ | Reject ppm
- Contributor chart (`stack_contrib.png`) and histogram (`stack_hist.png`)
- 2–3 concrete recommendations

## Limits
1-D linear stacks only. For 2-D/3-D stacks (angular errors, chains with rotation), linearize with sensitivity coefficients: enter `direction` as the partial derivative ∂gap/∂xᵢ instead of ±1, and say so in the report.
