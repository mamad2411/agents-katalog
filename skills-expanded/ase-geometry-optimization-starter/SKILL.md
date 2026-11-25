# ASE Geometry Optimization Starter

Use this skill to optimize a tiny argon dimer with ASE and summarize the final geometry.

## What This Skill Does

- reads a small JSON specification for an `Ar2` starting geometry
- attaches a deterministic Lennard-Jones calculator
- runs ASE `BFGS` optimization
- reports initial and final distances plus energy improvement

## Run

```bash
./slurm/envs/chem-tools/bin/python skills/computational-chemistry-and-molecular-simulation/ase-geometry-optimization-starter/scripts/run_ase_geometry_optimization.py --input skills/computational-chemistry-and-molecular-simulation/ase-geometry-optimization-starter/examples/toy_argon_dimer.json --out scratch/chemistry/ase_geometry_optimization_summary.json
```
