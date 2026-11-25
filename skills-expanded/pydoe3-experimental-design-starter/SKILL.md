# pyDOE3 Experimental Design Starter

Use this skill to generate a tiny full-factorial design from bounded factor definitions and summarize the resulting experiment table.

## What This Skill Does

- reads a small JSON factor specification
- generates a `2^k` full-factorial design with `pyDOE3`
- maps coded levels to real factor bounds
- reports factor names and generated rows for downstream experiment planning

## Run

```bash
./slurm/envs/statistics/bin/python skills/statistical-and-machine-learning-foundations-for-science/pydoe3-experimental-design-starter/scripts/run_pydoe3_experimental_design.py --input skills/statistical-and-machine-learning-foundations-for-science/pydoe3-experimental-design-starter/examples/toy_factors.json --out scratch/statistics/experimental_design_summary.json
```
