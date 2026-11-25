---
name: pharmacophore
description: Use when working with pharmacophore modeling for drug discovery. Covers feature types (HBD/HBA/AR/HYD/POS/NEG), RDKit 2D/3D pharmacophore fingerprints and matching (Pharm2D, Pharm3D, ChemicalFeatures), structure-based pharmacophore from protein-ligand complexes, ligand-based pharmacophore from active sets, and pharmacophore-based virtual screening workflows.
---

# Pharmacophore Modeling

A pharmacophore defines the minimum set of 3D chemical features — their types, spatial arrangement, and tolerance spheres — required for biological activity. Used for scaffold hopping, virtual screening, and SAR hypothesis generation.

## When to Use This Skill

- Derive pharmacophore from a co-crystal structure (structure-based)
- Extract common features from a set of active ligands (ligand-based)
- Screen a compound library for pharmacophore matches (VS)
- Compute pharmacophore fingerprints for similarity searching
- Identify scaffold-hopping opportunities (2D-diverse but 3D-similar)
- Validate binding mode hypotheses against active/inactive SAR data

## Feature Types

| Feature | Code | SMARTS definition (simplified) |
|---------|------|--------------------------------|
| H-bond donor | HBD | `[N!H0,O!H0,n!H0]` |
| H-bond acceptor | HBA | `[N,O,F,n,o,s]` (lone pairs) |
| Aromatic | AR | any aromatic ring |
| Hydrophobic | HYD | `[c,s,C,S,Br,I,Cl]` non-polar |
| Positive ionizable | POS | `[NH2,NH3+,guanidine,amidine]` |
| Negative ionizable | NEG | `[COOH,SO3H,PO4H,COO-]` |
| Exclusion volume | XV | regions sterically forbidden |

## Quick Start

```python
from rdkit import Chem
from rdkit.Chem import AllChem, MolStandardize
from rdkit.Chem.Pharm3D import Pharmacophore, EmbedLib
from rdkit.Chem import rdMolChemicalFeatures

# Load feature factory (FDEF file bundled with RDKit)
import os
from rdkit import RDConfig
fdefName = os.path.join(RDConfig.RDDataDir, 'BaseFeatures.fdef')
factory = rdMolChemicalFeatures.BuildFeatureFactory(fdefName)

# Get features from a molecule
mol = Chem.MolFromSmiles('c1ccc(cc1)C(=O)O')  # benzoic acid
feats = factory.GetFeaturesForMol(mol)
for feat in feats:
    print(f"{feat.GetFamily():12s} {feat.GetType():20s} atoms={list(feat.GetAtomIds())}")
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Feature types, SMARTS, exclusion volumes, RDKit FDEF format | `references/features-theory.md` |
| Pharm2D fingerprints (Gobbi), Pharm3D matching, feature factory | `references/rdkit-pharmacophore.md` |
| Derive pharmacophore from protein-ligand co-crystal / interactions | `references/structure-based.md` |
| Common-feature pharmacophore from a set of active ligands | `references/ligand-based.md` |
| Pharmacophore VS workflow: conformer gen, hit scoring, enrichment | `references/vs-workflow.md` |

## Software

| Tool | Install | Role |
|------|---------|------|
| RDKit | `conda install -c conda-forge rdkit` | 2D/3D pharmacophore (built-in) |
| ProLIF | `pip install prolif` | interaction fingerprints (→ features) |
| PLIP | `pip install plip` | protein-ligand interaction profiler |
| shape-it | `conda install -c conda-forge shape-it` | shape + pharmacophore overlay |
| Pharmit | web: pharmit.csb.pitt.edu | pharmacophore search (free web) |

## Related Skills

- `rdkit` — conformer generation, substructure, 2D fingerprints
- `docking` — binding poses used to derive structure-based pharmacophore
- `mdanalysis` — dynamic pharmacophore from MD trajectories
- `daylight-theory` — SMARTS syntax for custom feature FDEF files
