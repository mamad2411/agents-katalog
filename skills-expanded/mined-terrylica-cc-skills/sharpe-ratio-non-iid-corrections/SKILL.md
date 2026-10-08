---
name: sharpe-ratio-non-iid-corrections
description: >-
  Generalized Sharpe ratio inference under non-Normal serially correlated returns.
  Implements López de Prado, Lipton & Zoonekynd (2026): PSR, MinTRL, DSR, pFDR, oFDR, SFDR
  with ρ-corrected variance (Eq 2-3). Numba JIT for production speed.
  Use when computing Sharpe significance, minimum track record, false discovery rates,
  or deflated Sharpe ratios with autocorrelation correction.
allowed-tools: Read, Grep, Glob, Bash
---

# Sharpe Ratio Non-IID Corrections

Generalized Sharpe ratio inference framework for non-Normal, serially correlated returns. Reference implementation of López de Prado, Lipton & Zoonekynd (2026).

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Quick Start

```bash
# Run all 18 validation tests (paper Exhibit 1 + numerical examples)
uv run --python 3.14 --with numpy --with scipy --with numba \
  python plugins/quant-research/skills/sharpe-ratio-non-iid-corrections/references/sharpe_numba.py
```

## Paper Metadata

| Field           | Value                                                                         |
| --------------- | ----------------------------------------------------------------------------- |
| **Title**       | How to Use the Sharpe Ratio                                                   |
| **Authors**     | Marcos López de Prado, Alexander Lipton, Vincent Zoonekynd                    |
| **Series**      | ADIA Lab Research Paper Series, No. 19                                        |
| **Date**        | March 7, 2026                                                                 |
| **SSRN**        | 5520741                                                                       |
| **Replication** | <https://github.com/zoonek/2025-sharpe-ratio>                                 |
| **Source PDF**  | [lopez-de-prado-sharpe-2026.pdf](./references/lopez-de-prado-sharpe-2026.pdf) |

## References

| Topic                                   | Reference File                                                                          |
| --------------------------------------- | --------------------------------------------------------------------------------------- |
| Full Paper Transcription (82 equations) | [how-to-use-the-sharpe-ratio-2026.md](./references/how-to-use-the-sharpe-ratio-2026.md) |
| Equation → Implementation Tracker       | [sharpe-paper-tracker.md](./references/sharpe-paper-tracker.md)                         |
| Numba JIT Implementation (850+ lines)   | [sharpe_numba.py](./references/sharpe_numba.py)                                         |
| Source PDF                              | [lopez-de-prado-sharpe-2026.pdf](./references/lopez-de-prado-sharpe-2026.pdf)           |
| Paper Figures                           | [media/](./references/media/) (8 figures from pp. 12-45)                                |

## Preflight: Experimentation Context Assessment (CRITICAL)

Before computing DSR or SFDR, Claude Code MUST assess the experimentation context to determine the correct parameters. These inputs require subjective judgment that cannot be derived from code alone.

### Decision: DSR vs SFDR

| Situation                                                                 | Use      | Why                                                      |
| ------------------------------------------------------------------------- | -------- | -------------------------------------------------------- |
| You have return series for all K strategies tested                        | **DSR**  | Can compute K_eff from eigenvalues of correlation matrix |
| Strategy is the survivor of a long, unrecoverable experimentation history | **SFDR** | K is unknowable; SFDR sets a threshold without needing K |
| Evaluating a single strategy with no selection involved                   | **PSR**  | No multiple-testing correction needed (K=1)              |

**Default for this project**: Use **SFDR**. Our strategies are survivors of hundreds of regime explorations across WFO configurations, feature sets, model architectures, and metric cutoffs. The full experimentation history is unrecoverable.

### Parameters Requiring Judgment

Before calling `sfdr_threshold()`, assess each parameter by examining the project context:

| Parameter                                                       | What to assess                                                                          | How to assess it                                                                                                                           |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **P[H₁]** (prior: fraction of genuine strategies)               | "Out of all ideas ever tried in this project, what fraction were genuinely profitable?" | Check git history, experiment logs, signal-archaeology skill, WFO result archives. Conservative default: **0.05** (1 in 20 ideas is real). |
| **SR₁** (alternative: what a real strategy's Sharpe looks like) | "When a strategy IS real, what Sharpe does it typically achieve?"                       | Look at validated production strategies, published benchmarks for the asset class. Crypto range bars: **0.3–0.5** monthly.                 |
| **q** (false discovery tolerance)                               | "What false positive rate can I tolerate?"                                              | Research: **0.05**. Production capital allocation: **0.01**. Exploratory screening: **0.10**.                                              |
| **γ₃, γ₄, ρ** (return distribution shape)                       | Skewness, Pearson kurtosis, lag-1 autocorrelation                                       | Compute directly from the return series under evaluation. These are objective — no judgment needed.                                        |
| **T** (sample length)                                           | Number of return observations                                                           | Count from data. Objective.                                                                                                                |

### Preflight Checklist

When this skill is invoked, Claude Code should:

1. **Identify the evaluation context**: Is this a single new strategy, a WFO fold comparison, or a survivor from extensive search?
2. **Determine DSR vs SFDR**: If return series for all candidates exist → DSR with K_eff. Otherwise → SFDR.
3. **Elicit P[H₁]**: Search for experimentation history (git log, experiment catalogues, the `signal-archaeology` skill). Count approximate ideas tried vs ideas that worked. If unknowable, use 0.05.
4. **Estimate SR₁**: From validated production strategies or asset-class benchmarks.
5. **Set q**: Based on the decision's consequence (research paper vs capital deployment).
6. **Compute objective parameters**: γ₃, γ₄, ρ, T directly from the return series.
7. **Report the assessment**: State all parameter choices and reasoning before computing, so the user can override.

### Example Preflight Output

```
SFDR Preflight Assessment:
  Context:    Survivor of ~300 WFO configs × 5 feature sets × 3 architectures
  Method:     SFDR (experimentation history unrecoverable)
  P[H₁]:     0.05 (conservative — ~15 genuine signals from ~300 ideas)
  SR₁:       0.4 (typical monthly Sharpe for validated crypto range bar strategies)
  q:         0.05 (research-grade threshold)
  γ₃:        -2.448 (computed from return series)
  γ₄:        10.164 (Pearson kurtosis, computed from return series)
  ρ:         0.20 (lag-1 autocorrelation, computed from return series)
  T:         24 months
  → SFDR threshold: SR_c = 0.760
  → Observed SR: 0.456
  → VERDICT: FAIL (observed SR below SFDR threshold)
```

The user may override any parameter. If they disagree with P[H₁] or SR₁, recompute with their values.

## Key Formulas

All equations use the paper's non-IID variance (Eq 2-3) with Pearson kurtosis convention (γ₄=3 for Gaussian).

| Eq    | Name        | Formula                                                            | Function                |
| ----- | ----------- | ------------------------------------------------------------------ | ----------------------- |
| 2-3   | SR Variance | V[SR̂] = (1/T)·(a − b·γ₃·SR + c·(γ₄−1)/4·SR²)                       | `sr_variance()`         |
| 9     | PSR         | Φ((SR̂ − SR₀) / σ[SR₀])                                             | `psr()`                 |
| 11    | MinTRL      | (a − b·γ₃·SR₀ + c·(γ₄−1)/4·SR₀²) · (z\_{1−α}/(SR̂−SR₀))²            | `min_trl()`             |
| 13    | Critical SR | SR₀ + σ[SR₀]·z\_{1−α}                                              | `critical_sr()`         |
| 15    | Power       | 1 − Φ((SR_c − SR₁) / σ[SR₁])                                       | `power()`               |
| 17    | β (Type II) | Φ((z\_{1−α}·√(a(ρ)) − SR₁·√T) / √(a − b·γ₃·SR₁ + c·(γ₄−1)/4·SR₁²)) | `power()` → `1 - power` |
| 21    | pFDR        | (1 + (1−β)·P[H₁]/(α·P[H₀]))⁻¹                                      | `pfdr()`                |
| 24    | oFDR        | p·P[H₀] / (p·P[H₀] + (1−Φ[z*(SR₁)])·P[H₁])                         | `ofdr()`                |
| 28    | E[max SR]   | SR₀ + √V · ((1−γ)·Φ⁻¹[1−1/K] + γ·Φ⁻¹[1−1/(Ke)])                    | `expected_max_sr()`     |
| 29-31 | DSR         | PSR with SR₀ = E[max{SR̂_k}], σ = √V[max{SR̂_k}]                     | `dsr()`                 |
| 32-33 | SFDR        | Find SR_c such that pFDR(SR_c) = q                                 | `sfdr_threshold()`      |

Where a = (1+ρ)/(1−ρ), b = (1+ρ+ρ²)/(1−ρ²), c = (1+ρ²)/(1−ρ²) are AR(1) variance coefficients (`ar1_variance_coeffs()`).

## Numerical Example (Paper Exhibit 1)

Hedge fund: T=24 months, γ₃=−2.448, γ₄=10.164 (Pearson), SR=0.036/0.079≈0.456, ρ=0.2.

| Quantity             | Equation | Value             | Notes                                           |
| -------------------- | -------- | ----------------- | ----------------------------------------------- |
| σ[SR̂] (non-Gaussian) | Eq 3     | **0.379**         | vs 0.214 Gaussian — 77% wider                   |
| PSR (SR₀=0)          | Eq 9     | **0.966**         | Still significant despite wider CI              |
| PSR (SR₀=0.1)        | Eq 9+5   | **0.900**         | Harder benchmark reduces confidence             |
| MinTRL (SR₀=0)       | Eq 11    | **19.543** months | T=24 > 19.5 → sufficient                        |
| MinTRL (SR₀=0.1)     | Eq 11    | **39.369** months | More than doubles for SR₀ closer to SR̂          |
| β (power, SR₁=0.5)   | Eq 17    | **0.411**         | vs 0.224 IID Normal — 84% higher                |
| pFDR (P[H₁]=0.1)     | Eq 21    | **0.433**         | 43.3% false discovery when true strategies rare |
| oFDR (SR₁=0.5)       | Eq 24    | **0.361**         | Even 3.4% p-value → 36% observed FDR            |
| Power (1−β)          | Eq 15    | **0.589**         | Low for 24-month track record                   |

## Implementation Architecture

6-tier dependency hierarchy (Numba JIT, Rust-ready):

```
Tier 0: norm_cdf, norm_ppf, erfinv, Brent's method
Tier 1: sr_variance (Eqs 3/58)
Tier 2: psr (Eq 9), min_trl (Eq 11), critical_sr (Eq 13)
Tier 3: power (Eq 15), moments_mk (Eqs 62-65), expected_max_sr (Eq 28), var_max_sr
Tier 4: pfdr (Eq 18-21), ofdr (Eqs 22-24), fwer (Eq 25)
Tier 5: dsr (Eqs 29-31), sfdr_threshold (Eqs 32-33)  ← APEX
```

## Related Skills

| Skill                                                                  | Relationship                                                                          |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [opendeviation-eval-metrics](../opendeviation-eval-metrics/SKILL.md)   | Consumes PSR, DSR, MinTRL for range bar evaluation; has quick-ref formulas (ρ=0 case) |
| [adaptive-wfo-epoch](../adaptive-wfo-epoch/SKILL.md)                   | Uses DSR for WFE validation across walk-forward folds                                 |
| [evolutionary-metric-ranking](../evolutionary-metric-ranking/SKILL.md) | DSR as one of the metrics in multi-objective ranking                                  |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
