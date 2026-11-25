---
name: rdkit-molecular-descriptors
description: Use this skill to compute compact cheminformatics descriptors from one SMILES string with RDKit. Do not use it for docking, quantum chemistry, or large library screening.
---

## Purpose
Turn a SMILES string into a compact descriptor summary suitable for quick triage, featurization, and metadata enrichment.

## When to use
- You need a local RDKit-backed molecular summary from a SMILES string.
- You want canonical SMILES, formula, weight, and simple physicochemical descriptors.

## When not to use
- You need conformer generation, docking, or reaction modeling.
- You need batch-scale descriptor computation for millions of compounds.

## Inputs
- One SMILES string
- Optional molecule name
- Optional JSON output path

## Outputs
- JSON summary with canonical SMILES, formula, exact mass, logP, TPSA, HBA/HBD, rotatable bonds, ring count, and heavy-atom count

## Requirements
- `slurm/envs/chem-tools` with RDKit available

## Procedure
1. Run `slurm/envs/chem-tools/bin/python skills/drug-discovery-and-cheminformatics/rdkit-molecular-descriptors/scripts/compute_rdkit_descriptors.py --smiles "CC(=O)OC1=CC=CC=C1C(=O)O" --name aspirin`.
2. Inspect `canonical_smiles`, `formula`, `molecular_weight`, and `tpsa`.
3. Reuse the JSON payload for downstream filtering or reporting.

## Validation
- The command exits successfully.
- `canonical_smiles` is non-empty for a known valid molecule.
- Descriptor fields are numeric where expected.

## Failure modes and fixes
- Invalid SMILES: verify the input string and quoting.
- Missing RDKit environment: run the script with `slurm/envs/chem-tools/bin/python`.

## Safety and limits
- Descriptor calculation only.
- No medicinal-chemistry or safety interpretation is implied.

## Provenance
- RDKit docs: https://www.rdkit.org/docs/index.html
- RDKit repository: https://github.com/rdkit/rdkit

## Related skills
- `chembl-molecule-search`

