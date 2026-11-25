---
name: rdkit
description: Use when working with RDKit for cheminformatics in Python. Covers molecular I/O, property calculation, Lipinski filters, fingerprints, similarity, 3D conformer generation, reactions, fragmentation, substructure search, MCS, stereochemistry, and tautomers.
---

# RDKit

The primary Python library for cheminformatics. Molecular manipulation, descriptors, fingerprints, 3D generation, reactions, and more.

## When to Use This Skill

- Reading/writing molecules from SMILES, SDF, MOL, PDB files
- Calculating molecular properties and drug-likeness filters (Ro5, QED)
- Computing and comparing molecular fingerprints (Morgan/ECFP, MACCS, RDKit FP)
- Generating 3D conformers (ETKDG, MMFF, UFF)
- Substructure searching and SMARTS queries
- Maximum Common Substructure (MCS) analysis
- Chemical reactions via SMARTS or RXN files
- Molecular fragmentation (BRICS, RECAP, Murcko scaffolds)
- Stereochemistry assignment and analysis
- Tautomer enumeration and molecule standardization
- Molecular visualization (2D SVG/PNG, similarity maps)

## Quick Start

```python
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, Draw, rdMolDescriptors

# Load molecule
mol = Chem.MolFromSmiles('CC(=O)Oc1ccccc1C(=O)O')  # aspirin

# Basic properties
print(Descriptors.MolWt(mol))        # 180.16
print(Descriptors.MolLogP(mol))      # 1.31
print(rdMolDescriptors.CalcNumHBD(mol))  # 1
print(rdMolDescriptors.CalcNumHBA(mol))  # 4
print(rdMolDescriptors.CalcTPSA(mol))    # 63.6

# Morgan fingerprint (ECFP4-like)
fpgen = AllChem.GetMorganGenerator(radius=2)
fp = fpgen.GetFingerprint(mol)

# 2D image
img = Draw.MolToImage(mol, size=(300, 200))
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| SMILES, SDF, MOL, PDB, SMARTS I/O, serialization | `references/io-molecules.md` |
| Descriptors, Lipinski Ro5, QED, ADME, drug filters | `references/properties-descriptors.md` |
| Morgan, MACCS, RDKit FP, atom pair, similarity, diversity | `references/fingerprints-similarity.md` |
| 3D conformers (ETKDG), MMFF/UFF optimization, 3D descriptors | `references/3d-conformers.md` |
| Reactions (SMARTS), BRICS, RECAP, Murcko, tautomers, standardization | `references/transformations.md` |
| Substructure search (SMARTS), MCS, rings, stereochemistry, pharmacophores | `references/analysis-search.md` |
| Visualization: SVG/PNG, highlighting, similarity maps, grids | `references/visualization.md` |

## Key Modules

| Module | Import | Role |
|--------|--------|------|
| `Chem` | `from rdkit import Chem` | Core molecule objects, I/O |
| `AllChem` | `from rdkit.Chem import AllChem` | 3D, fingerprints, reactions |
| `Descriptors` | `from rdkit.Chem import Descriptors` | 200+ 2D descriptors |
| `rdMolDescriptors` | `from rdkit.Chem import rdMolDescriptors` | Fast C++ descriptors |
| `DataStructs` | `from rdkit import DataStructs` | Fingerprint similarity |
| `Draw` | `from rdkit.Chem import Draw` | 2D visualization |
| `rdMolDraw2D` | `from rdkit.Chem.Draw import rdMolDraw2D` | SVG/Cairo rendering |
| `MACCSkeys` | `from rdkit.Chem import MACCSkeys` | MACCS fingerprints |
| `rdFMCS` | `from rdkit.Chem import rdFMCS` | Maximum Common Substructure |
| `BRICS` | `from rdkit.Chem import BRICS` | BRICS fragmentation |
| `Recap` | `from rdkit.Chem import Recap` | RECAP fragmentation |
| `MurckoScaffold` | `from rdkit.Chem.Scaffolds import MurckoScaffold` | Scaffold extraction |
| `rdMolStandardize` | `from rdkit.Chem.MolStandardize import rdMolStandardize` | Tautomers, cleanup |
| `rdChemReactions` | `from rdkit.Chem import rdChemReactions` | Reaction handling |

## Installation

```bash
# conda (recommended)
conda install -c conda-forge rdkit

# pip (official wheel since 2022)
pip install rdkit

# verify
python -c "from rdkit import Chem; print(Chem.MolFromSmiles('c1ccccc1'))"
```

## Related Skills

- `deepchem` — ML models on molecular datasets built on top of RDKit
- `cheminformatics` — SMILES notation, file formats, molecular representations
- `nextflow` — Pipeline execution for high-throughput molecular workflows
