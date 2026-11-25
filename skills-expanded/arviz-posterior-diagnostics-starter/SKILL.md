# ArviZ Posterior Diagnostics Starter

Use this skill to generate a deterministic toy posterior and summarize uncertainty diagnostics with `ArviZ`.

## Run

```bash
./slurm/envs/statistics/bin/python \
  skills/statistical-and-machine-learning-foundations-for-science/arviz-posterior-diagnostics-starter/scripts/run_arviz_posterior_diagnostics.py \
  --out scratch/arviz/posterior_diagnostics.json
```

## Output

The JSON summary includes:

- per-parameter means and 90% HDIs
- `ess_bulk`, `ess_tail`, and `r_hat`
- `max_rhat` and `min_ess_bulk`

## Notes

- This is a starter for the taxonomy leaf `uncertainty-estimation`.
- The posterior is simulated deterministically for reproducible testing; it is not fitted from real data.
