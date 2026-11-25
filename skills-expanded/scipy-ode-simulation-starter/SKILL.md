# SciPy ODE Simulation Starter

Use this skill to integrate a deterministic predator-prey ordinary differential equation with `scipy.integrate.solve_ivp` and return a compact trajectory summary.

## What it does

- Solves a Lotka-Volterra system with fixed parameters and deterministic initial conditions.
- Reports peak times, peak populations, and the final state from the simulated trajectory.
- Produces a small JSON summary that is stable enough for repository smoke tests.

## When to use it

- You need a runnable starter for `ODE / SDE simulation workflows`.
- You want a minimal verified example of `solve_ivp` before building larger simulation workflows.

## Example

```bash
slurm/envs/scientific-python/bin/python skills/scientific-computing-and-numerical-methods/scipy-ode-simulation-starter/scripts/run_scipy_ode_simulation.py \
  --out scratch/scipy-ode/lotka_volterra_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/scientific-computing-and-numerical-methods/scipy-ode-simulation-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase30_empty_domain_seed_skills -v`
