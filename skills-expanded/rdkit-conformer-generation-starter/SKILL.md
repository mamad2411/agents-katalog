# RDKit Conformer Generation Starter

Use this skill to generate a small deterministic conformer ensemble with RDKit ETKDG and summarize the lowest-energy structures.

## What it does

- Reads a small TSV of molecules with `name` and `smiles`.
- Generates multiple 3D conformers per molecule with a fixed random seed.
- Optimizes them with UFF and reports the ranked conformer energies.
- Writes compact JSON suitable for smoke tests or later structure-aware workflows.

## When to use it

- You need a verified local starter for `small-molecule conformer generation`.
- You want a deterministic 3D-geometry precursor before docking, force-field setup, or descriptor work.

## Example

```bash
./slurm/envs/chem-tools/bin/python skills/computational-chemistry-and-molecular-simulation/rdkit-conformer-generation-starter/scripts/run_rdkit_conformer_generation.py \
  --input skills/computational-chemistry-and-molecular-simulation/rdkit-conformer-generation-starter/examples/molecules.tsv \
  --num-confs 4 \
  --out scratch/rdkit-conformers/summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/computational-chemistry-and-molecular-simulation/rdkit-conformer-generation-starter/tests -p 'test_*.py'`
- Repository smoke target: `make smoke-rdkit-conformers`
