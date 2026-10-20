---
skillx:
  name: exoplanet-workflows
  purpose: Orchestrate the full staged pipeline to recover one orbital period and complete the required output contract.
  scope_in:
    - end-to-end light-curve tasks requiring ordered preprocessing, transit search, cross-check, and final period output
    - situations where multiple methods exist and must stay in clear primary/secondary roles
  scope_out:
    - not for broad astrophysical interpretation or planet characterization beyond period recovery
    - not for method-shopping without convergence to a single final period
  requires:
    - access to light-curve columns (time, flux, flux_err, quality)
    - staged execution with explicit intermediate artifacts
    - writing exactly one final scalar period to /root/period.txt
  preferred_tools:
    - light-curve-preprocessing
    - transit-least-squares
    - box-least-squares
    - lomb-scargle-periodogram
  risks:
    - missing stage artifacts despite running code
    - selecting a non-transit periodicity
    - finishing analysis but forgetting final file write
  examples:
    - input: Recover the hidden transiting-planet period from a noisy TESS light curve.
      expected_behavior: run the five-stage pipeline, keep stage contracts explicit, choose one validated final period, write /root/period.txt.
---

# Bundle Objective

Recover one exoplanet orbital period (days) and complete the required deliverable:
- `/root/period.txt` contains one numeric value, rounded to 3 decimals, newline-terminated.

# Stage Graph (Preserve Order)

1. `light-curve-preprocessing` → produce cleaned/detrended light-curve artifact
2. `transit-least-squares` (primary) → produce primary transit candidate artifact
3. `box-least-squares` (secondary cross-check) → produce support/challenge artifact near candidate
4. `lomb-scargle-periodogram` (diagnostic) → produce variability/alias context artifact
5. `exoplanet-workflows` finalization → select final period, write `/root/period.txt`

Do not reorder the bundle into LS-first final selection or BLS-only replacement of TLS without strong evidence.

# Stage Contracts (Bundle-Level)

For each stage, require:
- **Input artifact exists** before running.
- **Output artifact is explicit** (named values, not vague prose).
- **Handoff note** states what next stage should consume.

Minimum artifact set expected before final write:
- preprocessed light-curve summary (point counts + detrending choice)
- TLS primary candidate (period, significance, alias check note)
- BLS cross-check outcome (support/challenge + nearest period)
- LS diagnostic outcome (dominant generic periodicity + relation to transit candidate)

# Final Selection Rule

Use TLS candidate as primary decision anchor.
Adjust only if cross-check evidence is strong and coherent:
- BLS and LS both consistently support a different period and
- the alternative better matches transit behavior than stellar variability.

If evidence is mixed, prefer the transit-shaped candidate from TLS and document why.

# Output Contract (Hard Gate)

Before declaring completion, verify all:
1. A single final period value is chosen.
2. Value is numeric in days.
3. Rounded to exactly 3 decimals.
4. `/root/period.txt` exists.
5. File contains only the scalar value plus newline.

If any check fails, task is not complete.

# Completion Discipline

Treat “analysis done” and “contract done” as separate states.
Task completion requires contract done.
