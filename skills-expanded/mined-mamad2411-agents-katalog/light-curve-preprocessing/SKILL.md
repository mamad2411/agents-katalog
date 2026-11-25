---
skillx:
  name: light-curve-preprocessing
  purpose: Produce a transit-preserving cleaned light curve artifact for downstream period search.
  scope_in:
    - quality filtering
    - outlier handling
    - conservative detrending/flattening before transit detection
  scope_out:
    - not for final period selection
    - not for aggressive smoothing that erases shallow transits
    - not for skipping flux_err or quality semantics checks
  requires:
    - time, flux, flux_err, and quality columns
    - explicit quality-flag convention check
  preferred_tools:
    - lightkurve quality filtering
    - sigma-based outlier removal
    - conservative flattening/detrending
  risks:
    - inverting quality logic (keeping bad points)
    - over-detrending transit signal away
    - producing a cleaned curve without documenting what changed
  examples:
    - input: Prepare a noisy TESS light curve with stellar variability for transit search.
      expected_behavior: filter correctly, remove outliers conservatively, flatten trends while preserving transit-like dips, pass a clear artifact to TLS.
---

# Stage Purpose

Convert raw light curve into a transit-search-ready artifact without destroying transit information.

# Input Contract

Expected input fields:
- `time`
- `flux`
- `flux_err`
- `quality`

Must verify and record quality-flag semantics before filtering (e.g., whether `0` means good).

# Output Contract

Produce a preprocessing artifact that includes at minimum:
- cleaned arrays: `time_clean`, `flux_clean`, `flux_err_clean`
- point counts: raw count, post-quality count, final count
- preprocessing parameters used:
  - outlier sigma
  - detrending/flattening method
  - flatten window (or equivalent)
- one-line risk note: why transit signal should remain preserved

Do not hand off only a plot or narrative; hand off actual cleaned arrays/values.

# Recommended Procedure

1. Apply quality filtering using verified flag semantics.
2. Remove outliers conservatively (start with moderate sigma).
3. Detrend/flatten with a window longer than expected transit duration.
4. Optionally perform a light second-pass outlier check if detrending introduces edge artifacts.
5. Confirm `flux_err` remains aligned with cleaned points.

# Stage-Local Checks

Before handoff:
- cleaned arrays are non-empty and same length
- no NaN/inf in handed-off arrays
- not an excessive data drop from raw to final (flag if severe)
- detrending choice is recorded (method + key parameters)

# Handoff to Next Stage (TLS)

Pass:
- cleaned arrays (`time_clean`, `flux_clean`, `flux_err_clean`)
- preprocessing parameter summary
- warning notes about any residual variability or aggressive filtering risk

TLS should be able to run immediately from this handoff without guessing preprocessing history.
