---
name: prism-bic-rank
description: Run the BIC-ranked model competition on PRISM predictions vs standard-QED parameterizations. Used by prism-computer at the end of each phase to rank candidate functional forms on equal footing with a free-parameter penalty. Implements the model-selection pattern established in v2/v3/v4 of the pipeline.
---

# BIC-Ranked Model Competition

The Bayesian Information Criterion penalizes free parameters:

```
BIC = n_obs · ln(RSS / n_obs) + k · ln(n_obs)
```

where `k` is the number of free parameters and `RSS` is the residual sum of squares. **Lower BIC is better.** A BIC gap of ~6 is conventionally considered decisive; ~10+ is strong evidence.

## Standard model slate (from v4)

Every phase's model competition should include, at minimum:

| Model | Parameters | Purpose |
|---|---|---|
| `rydberg_null` | 1 (R) | Baseline: pure 1/n² |
| `dirac_reduced` | 0 | Dirac fine-structure with reduced mass |
| `dirac_recoil` | 0 | + leading Breit recoil |
| `qed_standard` | 2 | Dirac + recoil + Bethe-log-style s-state + α⁴ fine |
| `prism_<variant>` | varies | The PRISM-derived functional form(s) under test |

The PRISM variant(s) come from the theoretician's current derivation. They must NOT include hand-tuned parameters from prior fits — that voids the "without tuning" claim.

## Workflow

1. Read predictions and measured values from `working_dir/predictions/*.csv` and `knowledge_base/literature_values.yaml`.
2. Run `scripts/bic_rank.py --models <slate> --data <csv> --out <json>`.
3. Write ranking to `working_dir/predictions/<task_id>_bic_ranking.csv` with columns: `model, params, rss, bic, delta_bic, rank, interpretation`.
4. Generate a Pareto-style plot of BIC vs parameter count at `working_dir/figures/<task_id>_bic_ranking.png`.

## Interpretation guidance

- `delta_bic < 2`: models indistinguishable on this data.
- `2 ≤ delta_bic < 6`: positive evidence for the lower-BIC model.
- `6 ≤ delta_bic < 10`: strong evidence.
- `delta_bic ≥ 10`: decisive.

## Honest reporting

From v4 experience: when a naive `rydberg_null` wins the competition, that's usually a degenerate-fit artifact (the ionization limit IS the Rydberg constant). Flag this case in the output — do not let it masquerade as a PRISM falsification.

Similarly, if `dirac_reduced` wins but the residuals are at ~10⁻³ eV (far above the ~10⁻⁶ eV QED scale), you're probably fitting recoil systematic, not QED. Surface this to the validator — the right test needs reduced-mass correction applied first.

## Output contract

The ranking CSV carries a sidecar `.meta.yaml`:

```yaml
generated_by: prism-computer
generated_at: <timestamp>
spec_task_id: <P#-T#>
models_ranked: <count>
top_model: <name>
delta_bic_to_second: <float>
interpretation: <one-line>
warnings:
  - <anything_suspicious>
```
