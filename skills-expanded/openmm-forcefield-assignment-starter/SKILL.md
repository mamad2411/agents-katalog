# OpenMM Force-Field Assignment Starter

Use this skill to assign a simple water force field to a tiny PDB topology with OpenMM and summarize the resulting system.

## What it does

- Loads a small example PDB topology.
- Applies OpenMM `tip3p.xml` with deterministic `createSystem` settings.
- Reports particle, residue, constraint, and force-class counts in JSON.

## When to use it

- You need a verified local starter for `force-field assignment`.
- You want a small, deterministic system-construction check before longer OpenMM workflows.

## Example

```bash
./slurm/envs/chem-tools/bin/python skills/computational-chemistry-and-molecular-simulation/openmm-forcefield-assignment-starter/scripts/run_openmm_forcefield_assignment.py \
  --input skills/computational-chemistry-and-molecular-simulation/openmm-forcefield-assignment-starter/examples/two_waters.pdb \
  --out scratch/openmm-forcefield/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/computational-chemistry-and-molecular-simulation/openmm-forcefield-assignment-starter/tests -p 'test_*.py'`
- Repository smoke target: `make smoke-openmm-forcefield`
