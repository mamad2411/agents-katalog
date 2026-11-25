---
name: openbabel
description: Use when converting molecular file formats, generating 3D coordinates, searching conformers, computing descriptors/fingerprints, or filtering chemical libraries with OpenBabel. Covers both pybel Python API and obabel command-line tool.
---

# OpenBabel — Chemical Format Conversion & Manipulation

OpenBabel 3.1.1. Two interfaces: **pybel** (Python API, high-level) and **obabel** (CLI, batch processing). Supports 146 formats, MMFF94/UFF/GAFF force fields.

## When to Use This Skill

- Converting between molecular formats: SMILES ↔ SDF ↔ MOL2 ↔ PDB ↔ InChI ↔ CIF ↔ XYZ ↔ 100+ others
- Generating 3D coordinates from SMILES (quick alternative to RDKit ETKDGv3)
- Conformer searching with force field scoring
- Protonation state at given pH
- Computing molecular descriptors (LogP, TPSA, MR) and fingerprints
- SMARTS substructure filtering of large libraries
- Batch library processing (split, deduplicate, filter)
- Converting formats unsupported by RDKit (CIF, VASP POSCAR, XYZ, etc.)

## Quick Start

```python
from openbabel import pybel

# Read SMILES → generate 3D → write SDF
mol = pybel.readstring('smi', 'CC(=O)Oc1ccccc1C(=O)O')   # aspirin
mol.make3D(forcefield='mmff94', steps=500)
mol.write('sdf', 'aspirin.sdf', overwrite=True)

# Read SDF → SMILES
for mol in pybel.readfile('sdf', 'library.sdf'):
    print(mol.write('can').strip())   # canonical SMILES
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| pybel Python API: read, write, 3D, descriptors, fingerprints, SMARTS | `references/pybel-python.md` |
| obabel CLI: conversion, --gen3d, --conformer, filtering, pH, split | `references/obabel-cli.md` |
| Format codes, fingerprint types, descriptors, Tanimoto | `references/formats-fingerprints.md` |

## Two Interfaces

| | pybel | obabel CLI |
|---|---|---|
| Use case | Scripted workflows, per-molecule logic | Batch conversion, library filtering |
| Import | `from openbabel import pybel` | `subprocess` or shell |
| Speed | Moderate | Fast (C++ core) |
| Flexibility | High (per-atom access) | Moderate (flags) |

## Installation

```bash
conda install -c conda-forge openbabel   # recommended (includes C++ libs)
pip install openbabel                     # Linux/macOS only

# Verify
python -c "from openbabel import pybel; print(pybel.readstring('smi','C').molwt)"
obabel --version
```

## Key Global Variables

```python
from openbabel import pybel

pybel.informats    # dict: {'sdf': 'MDL MOL format', 'smi': 'SMILES format', ...}
pybel.outformats   # dict of writable formats
pybel.fps          # list of fingerprint types: ['FP2', 'FP3', 'FP4', 'MACCS']
pybel.descs        # list of descriptor names
pybel.forcefields  # list of available force fields
```

## Relation to RDKit

| Task | Prefer |
|------|--------|
| Drug-like 3D (ETKDGv3) | RDKit |
| Non-organic / unusual atoms | OpenBabel (UFF) |
| Format not in RDKit (CIF, XYZ, etc.) | OpenBabel |
| SMARTS filtering (speed) | OpenBabel CLI |
| Fingerprints (ECFP) | RDKit |
| Fingerprints (FP2/FP3/MACCS) | OpenBabel |

## Related Skills

- `rdkit` — complementary: ETKDGv3 conformers, ECFP fingerprints, reactions
- `ase` — ASE reads XYZ/CIF; OpenBabel converts to those formats
- `scientific-skills:datamol` — fast preprocessing, also wraps RDKit
