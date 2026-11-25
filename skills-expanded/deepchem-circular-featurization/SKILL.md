---
name: deepchem-circular-featurization
description: Use this skill to compute compact DeepChem circular fingerprints from a small set of SMILES strings with the repo-managed DeepChem prefix. Do not use it for model training, docking, or large library screening.
---

## Purpose
Turn one or more SMILES strings into deterministic DeepChem `CircularFingerprint` summaries without requiring TensorFlow or PyTorch.

## When to use
- You need a lightweight DeepChem-backed fingerprinting step before downstream molecular ML work.
- You want a compact JSON payload with canonical SMILES, dense bit vectors, and active bit indices.

## When not to use
- You need graph featurizers, model training, or dataset download workflows.
- You need batch-scale featurization for very large libraries.

## Inputs
- Repeated `--smiles` arguments, or no arguments to use the bundled aspirin/caffeine example
- Optional `--size`, `--radius`, and `--out`

## Outputs
- JSON summary with `canonical_smiles`, `bit_vector`, `on_bits`, and `on_bit_count` for each molecule

## Requirements
- `slurm/envs/deepchem`
- DeepChem 2.8.0 and RDKit installed in that prefix

## Procedure
1. Run `slurm/envs/deepchem/bin/python skills/drug-discovery-and-cheminformatics/deepchem-circular-featurization/scripts/compute_circular_fingerprints.py --out skills/drug-discovery-and-cheminformatics/deepchem-circular-featurization/assets/aspirin_caffeine_fingerprints.json`.
2. Inspect `size`, `radius`, and each molecule's `canonical_smiles`, `bit_vector`, and `on_bits`.
3. Reuse the compact JSON as a deterministic preprocessing artifact for later experiments.

## Validation
- The command exits successfully under `slurm/envs/deepchem/bin/python`.
- Each molecule gets a non-empty canonical SMILES and a bit vector of the requested length.
- Repeated runs with the same inputs produce the same fingerprint payload.

## Failure modes and fixes
- Missing DeepChem runtime: run the script with `slurm/envs/deepchem/bin/python`.
- Invalid SMILES: correct the input string before featurization.
- Optional backend warnings: TensorFlow and PyTorch are not required for this fingerprint-only skill.

## Safety and limits
- Local featurization only.
- No activity prediction, medicinal-chemistry recommendation, or safety interpretation is implied.

## Provenance
- DeepChem documentation: https://deepchem.readthedocs.io/en/latest/
- RDKit documentation: https://www.rdkit.org/docs/index.html

## Related skills
- `rdkit-molecular-descriptors`
