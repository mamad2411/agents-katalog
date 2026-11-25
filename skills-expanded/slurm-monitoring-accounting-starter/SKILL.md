# Slurm Monitoring and Accounting Starter

Use this skill to submit a tiny probe job, capture live `squeue` snapshots while it waits or runs, and then summarize final `sacct` accounting.

## What it does

- Renders and submits a short Slurm batch job.
- Polls `squeue` to record live queue states.
- Resolves final job accounting through `sacct`.
- Optionally captures `seff` output when the command is available on the cluster.

## When to use it

- You need a verified starter for Slurm monitoring and post-run accounting.
- You want a reusable pattern for debugging queue state transitions and final resource summaries.

## Example

```bash
python3 skills/hpc/slurm-monitoring-accounting-starter/scripts/run_slurm_monitoring_accounting.py \
  --partition cpu \
  --job-name monitor-accounting \
  --sleep 2 \
  --out scratch/slurm-monitoring/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/hpc/slurm-monitoring-accounting-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase26_frontier_completion_skills -v`
