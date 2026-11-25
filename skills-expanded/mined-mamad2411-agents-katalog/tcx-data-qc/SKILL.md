---
name: tcx-data-qc
description: "Check dates, units, currency, market anchors, formulas, and stale-data gaps before numbers drive investment reasoning."
---

# Numeric Data QC

Use this procedure when numeric data, valuation inputs, market anchors,
portfolio exposure, or risk limits affect readiness.

Required output shape:

- source date and retrieval date
- period alignment
- units and currency
- share count and per-share consistency when relevant
- source versus derived versus assumption labels
- current price or market anchor with as-of posture when relevant
- formula sanity checks
- field-level gaps and the claims or actions they limit

Quality floor:

- Do not mix periods, units, currencies, or share bases silently.
- Label derived calculations and assumptions.
- Do not fabricate prices, metrics, formulas, or retrieval timestamps.
- Judge freshness against the requested as-of and the source's expected
  observation or publication cadence; an unavailable future period is not
  stale data.
- Preserve valid fields and downgrade only the conclusions or actions that
  depend on missing, stale, conflicting, or ambiguous inputs.

Put the data-quality result near the top of the artifact so synthesis can see
whether numeric claims are decision-ready.
