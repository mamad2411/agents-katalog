---
skillx:
  name: transit-least-squares
  purpose: Run the primary transit-focused period search and produce the main candidate artifact for final selection.
  scope_in:
    - transit-shaped periodic dimming search on cleaned light curves
    - candidate refinement and alias checks for final period decision
  scope_out:
    - not for general stellar variability interpretation
    - not for running without flux_err
    - not for final write without contract checks
  requires:
    - cleaned `time`, `flux`, `flux_err` arrays from preprocessing
    - sensible period search range
  preferred_tools:
    - transitleastsquares
    - focused refinement around best candidate
    - phase-folded and metric-based validation
  risks:
    - omitting flux_err
    - accepting weak/aliased period uncritically
    - producing candidate metrics but no handoff artifact
  examples:
    - input: Identify the orbital period in a detrended TESS light curve.
      expected_behavior: run TLS as primary search, refine near top candidate if needed, check aliases, hand off one primary candidate with evidence.
---

# Stage Purpose

Generate the bundle’s primary period candidate using transit-specific evidence.

# Input Contract

Required inputs from preprocessing stage:
- `time_clean`
- `flux_clean`
- `flux_err_clean`
- preprocessing summary notes

If `flux_err_clean` is missing, stage is not validly executable.

# Output Contract

Produce a TLS candidate artifact containing:
- `period_primary_days`
- `period_uncertainty_days` (if available)
- `SDE` and `SNR` (or equivalent strength metrics)
- candidate transit parameters (e.g., `T0`, depth, duration where available)
- alias check note for nearby half/double-period alternatives
- refinement note: whether a narrowed re-search was performed and why

# Recommended Procedure

1. Run broad TLS search over a sensible period range.
2. Identify top candidate and collect key metrics.
3. If candidate is plausible, run narrowed refinement around it for precision.
4. Compare against obvious alias alternatives (×0.5, ×2, nearby peaks).
5. Keep one primary candidate for downstream decision.

# Stage-Local Checks

Before handoff:
- TLS executed with flux uncertainties.
- Candidate period is numeric and in days.
- Strength metrics are recorded.
- Alias check was explicitly performed (even if trivial).
- Handoff contains one primary candidate, not an unranked list.

# Handoff to Next Stages (BLS + LS + Finalization)

Pass:
- primary candidate period and uncertainty
- strength metrics summary
- alias assessment summary
- rationale for why this candidate is currently preferred

Downstream stages should evaluate this candidate, not restart unconstrained search.
