---
name: rdkit-scaffold-analysis-starter
description: Use this skill to compute Murcko scaffold summaries for a small local molecule set with RDKit. Prefer it for deterministic scaffold grouping and smoke-scale cheminformatics checks.
---

## Purpose
Analyze a small local TSV of SMILES strings with RDKit Murcko scaffolds and emit a compact JSON summary that can feed later smoke integration or scaffold triage workflows.

## When to use
- You need a local scaffold grouping summary for a small curated molecule set.
- You want canonical SMILES, Murcko scaffolds, generic scaffolds, and group counts from one deterministic run.

## When not to use
- You need large library clustering, matched molecular pair analysis, or SAR interpretation.
- You need remote compound lookup or medicinal-chemistry recommendations.

## Inputs
- A TSV file with columns `name` and `smiles`
- Optional JSON output path

## Outputs
- JSON with per-molecule canonical SMILES, Murcko scaffold, generic scaffold, scaffold groups, generic scaffold groups, and summary counts

## Requirements
- `slurm/envs/chem-tools/bin/python`
- RDKit available in that environment

## Procedure
1. Inspect `examples/molecules.tsv`.
2. Run `slurm/envs/chem-tools/bin/python skills/drug-discovery-and-cheminformatics/rdkit-scaffold-analysis-starter/scripts/run_rdkit_scaffold_analysis.py --input skills/drug-discovery-and-cheminformatics/rdkit-scaffold-analysis-starter/examples/molecules.tsv`.
3. Review `molecules`, `scaffold_groups`, and `summary`.

## Validation
- The bundled example returns at least one scaffold group with count `>= 2`.
- Invalid SMILES input returns a non-zero exit code with a clear error message.

## Failure modes and fixes
- Invalid SMILES: fix the offending row in the input TSV.
- Missing RDKit environment: rerun with `slurm/envs/chem-tools/bin/python`.
- Missing `name` or `smiles` columns: use a header row with exactly those field names.

## Safety and limits
- Local scaffold computation only.
- No medicinal-chemistry conclusions are implied by the grouping.

## Provenance
- RDKit docs: https://www.rdkit.org/docs/index.html
- RDKit Murcko scaffold API: https://www.rdkit.org/docs/source/rdkit.Chem.Scaffolds.MurckoScaffold.html
- RDKit repository: https://github.com/rdkit/rdkit

## Related skills
- `rdkit-molecular-descriptors`
- `rdkit-molecule-standardization`
