---
skillx:
  name: lomb-scargle-periodogram
  purpose: Provide diagnostic periodicity context (especially stellar variability and aliases) to reduce wrong-period selection risk.
  scope_in:
    - exploratory periodicity checks on cleaned light curves
    - alias/variability context for transit candidate adjudication
  scope_out:
    - not for replacing transit-focused selection as default final path
    - not for returning strongest generic period without transit relevance check
  requires:
    - cleaned light curve from preprocessing
    - TLS candidate context for comparison
  preferred_tools:
    - lightkurve Lomb-Scargle periodogram
    - targeted comparison against transit candidate and harmonics
  risks:
    - confusing stellar rotation with planet period
    - overtrusting max-power generic peak
    - producing diagnostics that do not feed final decision
  examples:
    - input: Diagnose whether dominant variability could be masking or aliasing a transit candidate.
      expected_behavior: report dominant LS periods and explain their relation to the TLS candidate, then hand off a compact diagnostic artifact.
---

# Stage Purpose

Use LS as a diagnostic lens to contextualize periodic structure, not as an automatic final selector.

# Input Contract

Required inputs:
- cleaned arrays from preprocessing
- TLS primary candidate period for explicit comparison

# Output Contract

Produce an LS diagnostic artifact containing:
- `ls_top_period_days` (and optionally a small ranked set)
- relation to TLS candidate: `consistent` / `harmonic-related` / `inconsistent`
- note on likely variability origin (transit-compatible vs broad stellar variability)
- whether LS evidence should alter final period choice

# Recommended Procedure

1. Compute LS periodogram over an appropriate range.
2. Record top period(s) and inspect harmonic relationships.
3. Compare LS peaks to TLS candidate and alias possibilities.
4. Return concise recommendation for finalization stage.

# Stage-Local Checks

Before handoff:
- periodogram view/range is explicit enough to interpret results
- TLS comparison is explicit (not implied)
- diagnostic conclusion is decision-useful (not just a plot)

# Handoff to Finalization

Pass:
- dominant LS period context
- compatibility judgement relative to TLS candidate
- recommendation: keep TLS candidate or re-open candidate review

If evidence is ambiguous, mark as inconclusive rather than forcing a replacement.
