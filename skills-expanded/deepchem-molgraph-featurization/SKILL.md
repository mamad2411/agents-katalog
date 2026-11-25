---
name: deepchem-molgraph-featurization
description: Use this skill to featurize SMILES strings into DeepChem molecular graph objects. Prefer it for local graph-based preprocessing before molecular machine-learning experiments.
---

## Purpose
Create deterministic DeepChem molecular graph features from a small SMILES table using the repo-managed `chemtools` prefix.

## When to use
- You need a lightweight DeepChem starter without training a model.
- You want to inspect graph sizes and node-feature dimensions before modeling.

## When not to use
- You need trained DeepChem models requiring TensorFlow or PyTorch.
- You need dataset download or benchmark automation.

## Inputs
- A TSV file with `molecule_id` and `smiles` columns.

## Outputs
- A JSON summary with graph dimensions for each molecule.

## Requirements
- `slurm/envs/chemtools`
- DeepChem and RDKit in that prefix

## Procedure
1. Run `slurm/envs/chemtools/bin/python skills/computational-chemistry-and-molecular-simulation/deepchem-molgraph-featurization/scripts/featurize_molecules.py --input skills/computational-chemistry-and-molecular-simulation/deepchem-molgraph-featurization/examples/molecules.tsv --out scratch/deepchem/featurization.json`.
2. Inspect node counts, edge counts, and feature dimensions.
3. Use the feature summary as a preflight step before larger molecular ML runs.

## Validation
- The script exits successfully.
- Each molecule yields graph metadata.
- Node and edge counts are positive for valid molecules.

## Failure modes and fixes
- Missing optional ML backends: this skill only requires the featurizer path, not `torch` or `tensorflow`.
- Invalid SMILES: correct the input row before featurization.

## Provenance
- DeepChem documentation: https://deepchem.readthedocs.io/en/latest/

## Related skills
- `rdkit-molecular-descriptors`
