# OpenMM Langevin Dynamics Starter

Use this skill to run a deterministic toy Langevin dynamics simulation in OpenMM and inspect a compact trajectory summary.

## What This Skill Does

- builds a two-particle harmonic system
- runs short Langevin dynamics on the OpenMM Reference platform
- records bond-length and potential-energy snapshots over time

## When To Use It

- when you need a runnable starter for `molecular-dynamics-setup`
- when you want a local OpenMM smoke path before scaling to larger systems
- when you need deterministic MD-like outputs in repository tests

## Run

```bash
./slurm/envs/chem-tools/bin/python skills/computational-chemistry-and-molecular-simulation/openmm-langevin-dynamics-starter/scripts/run_openmm_langevin_dynamics.py --out scratch/openmm/langevin_dynamics_summary.json
```

## Notes

- This is a tiny synthetic system, not a physically meaningful production simulation.
- The Reference platform plus a fixed velocity seed keeps the summary reproducible.
