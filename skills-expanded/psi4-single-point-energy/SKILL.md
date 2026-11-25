---
name: psi4-single-point-energy
description: Use this skill to run a deterministic Psi4 single-point Hartree-Fock energy on a tiny water molecule. Do not use it for production quantum chemistry benchmarking or large basis-set studies.
---

## Purpose
Provide a minimal, runnable Psi4 starter that computes one deterministic single-point energy for a bundled water geometry and records the result as compact JSON.

## When to use
- You need a verified local Psi4 entry point.
- You want a tiny quantum-chemistry smoke calculation before scaling to larger molecules or better methods.
- You need a deterministic summary that can be tested in CI-like local workflows.

## When not to use
- You need high-accuracy energetics, conformer searches, or production optimizations.
- You need solvent models, post-HF methods, or large basis sets.

## Inputs
- Optional output JSON path
- Optional method and basis, defaulting to `hf` and `sto-3g`

## Outputs
- JSON summary with Psi4 version, job label, molecule metadata, and single-point energy in Hartree

## Requirements
- `slurm/envs/psi4` with Psi4 installed

## Procedure
1. Run `slurm/envs/psi4/bin/python skills/computational-chemistry-and-molecular-simulation/psi4-single-point-energy/scripts/run_psi4_single_point.py --out skills/computational-chemistry-and-molecular-simulation/psi4-single-point-energy/assets/water_hf_sto3g_summary.json`.
2. Confirm the output reports `psi4_version`, `method`, `basis`, and a negative `energy_hartree`.
3. Reuse the script as a seed for larger Psi4 workflows after validating the dedicated prefix.

## Validation
- The command exits successfully under `slurm/envs/psi4/bin/python`.
- The result reports a 3-atom water molecule.
- The `hf/sto-3g` energy is reproducible for the bundled geometry.

## Failure modes and fixes
- Missing Psi4 prefix: install or reactivate `slurm/envs/psi4`.
- Import failure: confirm the script is run with `slurm/envs/psi4/bin/python`, not the base interpreter.
- Numerical drift after edits: reset the geometry, method, basis, and thread count to the bundled defaults.

## Safety and limits
- Educational starter only.
- The bundled water calculation is intentionally tiny and not suitable for scientific claims by itself.

## Provenance
- Psi4 documentation: https://psicode.org/psi4manual/master/index.html
- Psi4 installation guide: https://psicode.org/installs/v1.10.x/

## Related skills
- `openmm-system-minimization`
