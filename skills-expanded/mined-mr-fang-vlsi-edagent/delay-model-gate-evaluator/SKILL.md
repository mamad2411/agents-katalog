---
name: delay-model-gate-evaluator
description: "Execute delay-model validation gates against HPWL baselines. Use when evaluating model consistency, running Gate-0 contract checks, building Gate-1 bucketed scorecards, performing wirelength-aware correlation checks, or deciding readiness for active optimization."
---

# Delay Model Gate Evaluator

Run these checks before promoting model changes into placement/CTS optimization.

## Placeholder conventions

- `<merged_or_unified_tsv>`: Path to a merged or unified TSV file, for example `data/merged_asap7_delay_v2.tsv` or `data/unified_timing_run03.tsv`.
- `<tag>`: Descriptive run identifier such as `run03_lr1e-3` or `v2_bspdn_baseline`. Use one naming scheme consistently across gates.

## Gate-0: Contract and sign consistency

```bash
ROOT=/mnt/research/Hu_Jiang/Students/Fang_Donghao/TAMU-ASAP07-BSPDN-BPR-V0.00
cd "$ROOT"

python3 scripts/debug/check_delay_model_contract.py \
  --input-tsv <merged_or_unified_tsv> \
  --delta-sign back_minus_front \
  --min-sign-acc 0.60 \
  --out-prefix slurm_logs/04_delay_modeling/<tag>.contract
```

Use `--strict` for CI-style hard fail.

**If Gate-0 fails:** Check the contract output first. If sign accuracy is below the threshold, inspect the worst-performing net groups for data quality issues such as missing features, outlier wirelengths, or inconsistent labels. Re-train or filter the input TSV before proceeding.

## Gate-1: Bucketed scorecard

```bash
python3 scripts/debug/bucketed_delay_model_scorecard.py \
  --input-tsv <merged_or_unified_tsv> \
  --delta-sign back_minus_front \
  --out-prefix slurm_logs/04_delay_modeling/<tag>.bucketed
```

## Promotion criteria
1. Gate-0 sign contract passes (sign accuracy >= 0.60; use >= 0.75 for production-critical flows).
2. Key buckets (long + high fanout) show correlation equal to or better than the HPWL baseline.
3. Scorecard results are archived with clear run tag and data source.

**If promotion criteria are not met:** Do not proceed to active optimization. Iterate on the delay model instead by reviewing feature engineering, checking training-data coverage for underperforming buckets, and re-running both gates after the update.

Load `references/metric_contract.md` before interpreting results.
