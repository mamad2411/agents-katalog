# Pymatgen Crystal Structure Parsing Starter

Use this skill to parse one crystal structure file with `pymatgen` and return a deterministic structural summary with lattice, composition, density, and symmetry metadata.

## What it does

- Loads a structure file such as CIF with `pymatgen.core.Structure`.
- Summarizes formula, reduced formula, lattice parameters, volume, density, and species counts.
- Uses `SpacegroupAnalyzer` to report a space-group symbol, number, and crystal system when symmetry analysis succeeds.

## When to use it

- You need a runnable starter for the `crystal structure parsing` leaf.
- You want a lightweight structure summary before feature engineering or property modeling.

## Example

```bash
slurm/envs/materials/bin/python skills/materials-science-and-engineering/pymatgen-crystal-structure-parsing-starter/scripts/run_pymatgen_structure_summary.py \
  --input skills/materials-science-and-engineering/pymatgen-crystal-structure-parsing-starter/examples/cscl.cif \
  --out scratch/materials/cscl_structure_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/materials-science-and-engineering/pymatgen-crystal-structure-parsing-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase28_network_materials_cheminformatics_skills -v`
