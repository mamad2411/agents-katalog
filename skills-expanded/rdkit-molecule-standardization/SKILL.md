---
name: rdkit-molecule-standardization
description: Use this skill to standardize one small-molecule SMILES string with RDKit MolStandardize. It is for local cleanup, salt stripping, uncharging, and tautomer canonicalization, not docking or batch-library processing.
---

## Purpose
Turn a single SMILES string into a deterministic standardization summary using `RDKit` `MolStandardize`.

## When to use
- You need a local starter for the taxonomy leaf `molecule-standardization`.
- You want to strip salts or counterions before downstream featurization.
- You want a compact JSON summary with fragment-parent, uncharged, and canonical-tautomer SMILES.

## When not to use
- You need conformers, docking, or quantum chemistry.
- You need bulk normalization across large compound libraries.

## Inputs
- One SMILES string passed by `--smiles` or a single-line file passed by `--smiles-file`
- Optional molecule name
- Optional JSON output path

## Outputs
- JSON summary with cleaned, fragment-parent, uncharged, and canonical-tautomer SMILES
- Charge before and after standardization
- Formula and heavy-atom count for the standardized molecule

## Requirements
- `slurm/envs/chem-tools` with `RDKit` and `MolStandardize`

## Procedure
1. Run `slurm/envs/chem-tools/bin/python skills/drug-discovery-and-cheminformatics/rdkit-molecule-standardization/scripts/standardize_rdkit_molecule.py --smiles-file skills/drug-discovery-and-cheminformatics/rdkit-molecule-standardization/examples/sodium_acetate.smiles --name sodium-acetate`.
2. Inspect `fragment_parent_smiles` to confirm salt stripping.
3. Inspect `uncharged_smiles` and `canonical_tautomer_smiles` before reusing the molecule downstream.

## Validation
- The script exits successfully with the `chem-tools` prefix.
- The sodium acetate example standardizes to `CC(=O)O`.
- The runtime output matches `assets/sodium_acetate_standardized.json`.

## Failure modes and fixes
- Invalid SMILES: verify the input string or the first non-empty line in the SMILES file.
- Missing RDKit environment: run the script with `slurm/envs/chem-tools/bin/python`.

## Safety and limits
- This is a molecule-cleanup helper only.
- It does not imply medicinal-chemistry, ADMET, or synthesis interpretation.

## Provenance
- RDKit documentation: https://www.rdkit.org/docs/
- RDKit MolStandardize API: https://www.rdkit.org/docs/source/rdkit.Chem.MolStandardize.rdMolStandardize.html

## Related skills
- `rdkit-molecular-descriptors`
- `chembl-molecule-search`
