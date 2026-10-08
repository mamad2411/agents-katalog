---
name: mmpa
description: Use when performing Matched Molecular Pair Analysis (MMPA) for SAR extraction, property cliff identification, bioisostere discovery, or analogue generation. Covers MMP theory and fragmentation schemes, mmpdb 4 CLI workflow (fragment/index/loadprops/transform), RDKit programmatic MMP generation, statistical SAR delta analysis, and applying transforms to generate focused libraries.
---

# Matched Molecular Pair Analysis (MMPA)

MMPA identifies pairs of molecules (A, B) that differ by a single structural transformation (R₁ → R₂) at one site while sharing an identical molecular context. Aggregating ΔProperty across hundreds of such pairs extracts robust, context-free SAR rules.

## When to Use This Skill

- Extract SAR rules from a compound dataset (e.g., which H→F swap improves metabolic stability?)
- Identify activity cliffs (large ΔActivity for small structural change)
- Find bioisosteric replacements supported by experimental data
- Predict property changes for a proposed structural modification
- Generate analogue libraries from a lead compound using proven transforms
- Prioritize which substituent to try next based on MMPA-derived rules

## Core Concept

```
Molecule A:  [Context]-[R₁]   →   transform: R₁ → R₂
Molecule B:  [Context]-[R₂]

ΔProperty = P(B) - P(A)

SAR rule: "R₁ → R₂ causes ΔlogP = +0.45 ± 0.12 (N=18 pairs)"
```

**Fragmentation** (single-cut):
- Variable part: the part that changes between A and B
- Context: the shared skeleton (everything outside the cut bond)
- Represented via SMIRKS: `[R₁:1]>>[R₂:1]` at attachment point

**Double-cut**: both variable parts and a central linker can vary — rarer, more specific.

## Quick Start — mmpdb 4

```bash
pip install mmpdb
# or: conda install -c conda-forge mmpdb

# Full pipeline: SMILES file → SAR rules
mmpdb fragment compounds.smi -o fragments.h5
mmpdb index fragments.h5 -o mmpdb.db

# Load experimental properties (CSV with: smiles, id, prop1, prop2)
mmpdb loadprops mmpdb.db properties.csv

# Query: what transforms improve LogD?
mmpdb transform --smiles "c1ccc(cc1)C(=O)O" mmpdb.db \
    --property LogD \
    --min-pairs 3 \
    -o transform_results.csv

# Analyze SAR rules for a property
mmpdb analyze mmpdb.db --property pIC50 -o sar_rules.csv
```

## Quick Start — Programmatic (RDKit + mmpdb Python API)

```python
import mmpdblib
from mmpdblib import do_fragment, do_index

# Fragment a SMILES list programmatically
from mmpdblib.analysis_algorithms import find_mmps

smiles_dict = {
    "mol_A": "c1ccc(CC)cc1",   # ethylbenzene
    "mol_B": "c1ccc(CF)cc1",   # fluoromethylbenzene
    "mol_C": "c1ccc(CCl)cc1",  # chloromethylbenzene
}

# Find matched molecular pairs
pairs = find_mmps(list(smiles_dict.values()), list(smiles_dict.keys()))
# pairs: list of (id1, id2, transform_SMIRKS, context_SMILES)
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| MMP definition, fragmentation theory, SMIRKS transforms, property cliffs, statistical framework | `references/mmpa-theory.md` |
| mmpdb 4 CLI: fragment → index → loadprops → transform → analyze, full SAR workflow | `references/mmpdb-workflow.md` |
| RDKit programmatic MMP generation: bond cutting, attachment points, pair enumeration | `references/rdkit-fragmentation.md` |
| SAR delta statistics, activity cliff detection, bioisostere tables, visualization | `references/sar-analysis.md` |
| Applying transforms to query molecule, analogue library generation, integration with design tools | `references/transform-application.md` |

## Software Stack

| Package | Install | Role |
|---------|---------|------|
| `mmpdb` | `pip install mmpdb` | Core MMPA engine (AZ, Apache 2.0) |
| `rdkit` | conda/pip | Fragmentation, SMILES parsing, visualization |
| `pandas` | `pip install pandas` | SAR table analysis |
| `seaborn` / `matplotlib` | pip | Activity cliff heatmaps, ΔP distributions |
| `mols2grid` | `pip install mols2grid` | Interactive molecule grid visualization |

## Key Concepts

| Term | Definition |
|------|-----------|
| MMP | Two molecules differing by exactly one transformation at one site |
| Transform | SMIRKS notation: `[*:1]>>[*:1]` where `[*:1]` = attachment point |
| Variable part | The fragment that differs between the two molecules |
| Context | Shared molecular scaffold (everything outside the cut bond) |
| ΔProperty | P(B) − P(A) for any measured property |
| SAR rule | A transform + aggregated ΔP statistics across N≥3 pairs |
| Activity cliff | Large |ΔActivity| (> 1 log unit) for structurally similar molecules |

## Key Pitfalls

- **mmpdb 2 vs mmpdb 4**: many tutorials use old API (`mmpdb.make_index`); v4 uses CLI subcommands (`mmpdb fragment/index/loadprops`)
- **Single-cut only**: mmpdb default cuts one bond; avoid multi-cut for first pass (combinatorial explosion)
- **Variable part size limit**: default max_heavies=10 for variable part; increase with `--max-variable-heavies 13` for larger changes
- **N < 3 pairs → unreliable rule**: always filter output to `num_pairs >= 3`
- **Chirality**: mmpdb ignores chirality by default; use `--stereo` flag if needed
- **Property units**: ΔlogP and ΔpIC50 are in log units; ΔCl (clearance) in mL/min/kg — always report units

## Related Skills

- `rdkit` — SMILES I/O, substructure matching, property calculation (QED, LogP)
- `generative-design` — MMPA-guided focused library generation (apply transforms at scale)
- `pharmacophore` — combine MMPA bioisostere rules with pharmacophore constraints
- `docking` — score MMPA-generated analogues via Vina/Gnina
- `scientific-skills:chembl-database` — ChEMBL as MMPA input dataset for literature SAR mining
