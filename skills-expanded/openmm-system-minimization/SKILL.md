---
name: openmm-system-minimization
description: Use this skill to run a deterministic OpenMM energy minimization on a tiny toy system. Do not use it for production molecular dynamics or force-field validation.
---

## Purpose
Provide a minimal, runnable OpenMM starter that creates a small bonded system, minimizes its energy, and reports before/after energies and coordinates.

## When to use
- You need a verified local OpenMM entry point.
- You want a tiny deterministic minimization example before scaling to larger simulations.

## When not to use
- You need biomolecular force-field preparation or explicit-solvent production runs.
- You need ensemble sampling or long-timescale trajectories.

## Inputs
- Optional JSON summary path

## Outputs
- JSON summary with OpenMM version, platform, initial/final potential energy, and final coordinates

## Requirements
- `slurm/envs/chem-tools` with OpenMM available

## Procedure
1. Run `slurm/envs/chem-tools/bin/python skills/computational-chemistry-and-molecular-simulation/openmm-system-minimization/scripts/run_openmm_minimization.py`.
2. Compare `initial_potential_energy_kj_mol` and `final_potential_energy_kj_mol`.
3. Reuse the script as a seed for more realistic system-building workflows.

## Validation
- The command exits successfully.
- Final potential energy is lower than the initial potential energy.
- Final coordinates are emitted for all particles.

## Failure modes and fixes
- Missing OpenMM environment: run the script with `slurm/envs/chem-tools/bin/python`.
- Numerical issues: reset the toy system to the bundled defaults.

## Safety and limits
- Educational starter only.
- This is not a physically meaningful production system.

## Provenance
- OpenMM user guide: https://docs.openmm.org/latest/userguide/

## Related skills
- `rdkit-molecular-descriptors`

