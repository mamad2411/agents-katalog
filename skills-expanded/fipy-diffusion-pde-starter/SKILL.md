# FiPy Diffusion PDE Starter

Use this skill to solve a tiny 1D diffusion problem with `FiPy` and summarize the evolution of the profile.

## What it does

- Builds a small 1D mesh with an initially occupied left boundary slab.
- Solves a transient diffusion equation for a few deterministic time steps.
- Reports mass conservation, center-cell value, and the leading edge of the diffused profile in JSON.

## When to use it

- You need a runnable starter for `PDE discretization and solvers`.
- You want a verified local PDE example before moving to heavier finite-element toolchains.

## Example

```bash
slurm/envs/numerics/bin/python skills/scientific-computing-and-numerical-methods/fipy-diffusion-pde-starter/scripts/run_fipy_diffusion_pde.py \
  --out scratch/numerics/fipy_diffusion_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/scientific-computing-and-numerical-methods/fipy-diffusion-pde-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase31_frontier_leaf_conversion_skills -v`
