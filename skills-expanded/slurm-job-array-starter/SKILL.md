# Slurm Job Array Starter

Use this skill to submit a tiny real Slurm job array, wait for terminal accounting, and summarize per-task outputs in compact JSON.

## What it does

- Renders and submits a minimal `sbatch --array` script on the live cluster.
- Polls queue state with `squeue` and waits for terminal task accounting with `sacct`.
- Reads each task's stdout and stderr logs and exports a per-task summary.

## When to use it

- You need a verified starter for the `job arrays` leaf.
- You want a minimal example of per-task output capture and accounting on the current Slurm cluster.
- You need deterministic JSON for tests before scaling to larger batched workloads.

## Example

```bash
python3 skills/hpc/slurm-job-array-starter/scripts/run_slurm_job_array.py \
  --partition cpu \
  --array-spec 0-1 \
  --sleep 1 \
  --out scratch/slurm-array/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/hpc/slurm-job-array-starter/tests -p 'test_*.py'`
- Expected summary: `task_count == 2` and all task states are `COMPLETED` with `ExitCode 0:0`
