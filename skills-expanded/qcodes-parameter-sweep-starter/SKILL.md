# QCoDeS Parameter Sweep Starter

Use this skill to run a tiny deterministic parameter sweep with `QCoDeS`, persist the measurements to a local dataset database, and summarize the recorded sweep.

## What it does

- reads a short setpoint list from a TSV file
- records a synthetic measurement sweep into a QCoDeS SQLite database
- reports run metadata, setpoint range, response statistics, and captured points

## When to use it

- you need a verified starter for `instrument-control-and-scheduling`
- you want a local pattern for QCoDeS `Measurement` plus dataset capture before wiring in real instruments
- you need a deterministic instrumentation example without hardware dependencies

## Example

```bash
./slurm/envs/instrumentation/bin/python skills/robotics-lab-automation-and-scientific-instrumentation/qcodes-parameter-sweep-starter/scripts/run_qcodes_parameter_sweep.py \
  --setpoints skills/robotics-lab-automation-and-scientific-instrumentation/qcodes-parameter-sweep-starter/examples/toy_setpoints.tsv \
  --db-out scratch/qcodes/toy_sweep.db \
  --summary-out scratch/qcodes/toy_sweep_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/robotics-lab-automation-and-scientific-instrumentation/qcodes-parameter-sweep-starter/tests -p 'test_*.py'`
- Expected summary: `point_count == 4`, `response_mean == 1.15`, `run_id == 1`
