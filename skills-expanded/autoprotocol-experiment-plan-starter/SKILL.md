# Autoprotocol Experiment Plan Starter

Use this skill to generate a deterministic Autoprotocol JSON plan for a small liquid-handling experiment and inspect a concise execution summary.

## What This Skill Does

- reads a simple transfer plan from TSV
- constructs an Autoprotocol `Protocol` with source and assay plates
- emits machine-readable protocol JSON plus a compact summary of refs and operations

## When To Use It

- when you need a runnable `robotic-experiment-planning` starter
- when you want a local machine-readable lab plan before targeting a specific robot platform
- when you need deterministic protocol artifacts for repository tests

## Run

```bash
./slurm/envs/instrumentation/bin/python skills/robotics-lab-automation-and-scientific-instrumentation/autoprotocol-experiment-plan-starter/scripts/build_autoprotocol_experiment_plan.py \
  --transfers skills/robotics-lab-automation-and-scientific-instrumentation/autoprotocol-experiment-plan-starter/examples/toy_transfers.tsv \
  --protocol-json scratch/instrumentation/autoprotocol_plan.json \
  --summary-out scratch/instrumentation/autoprotocol_plan_summary.json
```

## Notes

- This skill only creates a protocol specification; it does not execute wet-lab work.
- The transfer plan is intentionally small and deterministic so the generated JSON stays stable across runs.
