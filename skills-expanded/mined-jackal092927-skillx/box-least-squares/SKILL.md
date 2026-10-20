---
skillx:
  name: box-least-squares
  purpose: Run a focused transit-style cross-check around the primary candidate to support or challenge final period selection.
  scope_in:
    - backup/validation transit search near candidate periods
    - candidate comparison when TLS confidence or alias risk is nontrivial
  scope_out:
    - not for replacing TLS as default primary method
    - not for broad unconstrained peak-hunting
  requires:
    - cleaned light curve from preprocessing
    - TLS primary candidate and candidate neighborhood
  preferred_tools:
    - astropy.timeseries.BoxLeastSquares
    - focused period window or candidate-centered checks
  risks:
    - coarse grid causing false disagreement
    - selecting a high-power alias without transit-context checks
    - spending effort on BLS while output contract remains incomplete
  examples:
    - input: Cross-check a TLS candidate near ~P days.
      expected_behavior: run BLS in focused mode, report support/challenge for that candidate, hand off a clear conclusion artifact.
---

# Stage Purpose

Provide secondary evidence for or against the primary TLS candidate without derailing pipeline completion.

# Input Contract

Required inputs:
- cleaned arrays (`time_clean`, `flux_clean`, optional `flux_err_clean`)
- TLS candidate artifact (`period_primary_days`, alias notes)

BLS stage is invalid if run without reference to the TLS candidate context.

# Output Contract

Produce a BLS cross-check artifact with:
- `bls_best_period_days` in the evaluated window
- relation to TLS candidate: `supports` / `challenges` / `inconclusive`
- period difference vs TLS candidate
- at least one quality indicator (power or depth-SNR-like statistic)
- note on grid/window choice (to interpret disagreements)

# Recommended Procedure

1. Build BLS model on cleaned light curve.
2. Search a focused window around TLS candidate first.
3. Optionally inspect nearest alternative peak if alias risk is high.
4. Classify BLS outcome as support/challenge/inconclusive.

# Stage-Local Checks

Before handoff:
- search window/gridding is recorded and not trivially coarse
- outcome classification is explicit
- candidate comparison references TLS period directly
- no switch to exploratory full-range method-shopping unless justified

# Handoff to Finalization

Pass:
- BLS best period in evaluated region
- support/challenge classification
- concise interpretation of whether BLS should change the final pick

Final stage should use this as secondary evidence, not as default override.
