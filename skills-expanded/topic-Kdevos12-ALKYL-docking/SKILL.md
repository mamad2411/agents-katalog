---
name: docking
description: Use when performing protein-ligand docking, virtual screening, or structure-based drug design. Covers receptor preparation (protonation, pocket definition), AutoDock Vina/Gnina docking engines, high-throughput virtual screening pipelines, pose analysis with interaction fingerprints, and ensemble docking for protein flexibility.
---

# Docking — Protein-Ligand Docking & Virtual Screening

AutoDock Vina 1.2 · Gnina · pdbfixer · ProLIF · fpocket. For structure-based drug design: binding mode prediction, virtual screening, and lead optimization by docking.

## When to Use This Skill

- Predicting how a small molecule binds to a protein (binding mode / pose)
- Virtual screening: ranking a library of compounds by predicted binding affinity
- Validating a pharmacophore hypothesis in 3D structural context
- Ensemble docking to account for protein flexibility
- Re-scoring docking poses with physics-based (MM-GB/SA) or CNN-based scoring
- Fragment-based screening (→ see `fbdd` skill for growing/linking)

## Decision Tree — Docking vs. Other Methods

```
Input: protein structure 3D?
  NO  → ligand-based methods (pharmacophore, QSAR, similarity search)
  YES → docking

Compound set size?
  > 10 000   → VS pipeline (references/virtual-screening.md)
  10–10 000  → standard docking batch (references/vina-gnina.md)
  < 10       → manual docking + careful pose analysis

Goal: binding mode accuracy vs. ranking accuracy?
  Binding mode → high exhaustiveness, Gnina CNN rescoring
  Ranking      → standard Vina + clustering + MM-GB/SA rescore

Protein structure source?
  X-ray / CryoEM  → direct prep (references/protein-prep.md)
  Homology model  → validate first (→ homology-modeling skill)
  AlphaFold       → check pLDDT > 80 in pocket region before docking
```

## Quick Start

```python
import subprocess
from pathlib import Path

# 1. Prepare receptor (pdbfixer + obabel → PDBQT)
# See references/protein-prep.md for full workflow

# 2. Prepare ligand
import subprocess
subprocess.run([
    "obabel", "ligand.sdf", "-O", "ligand.pdbqt",
    "--gen3d", "-h"
], check=True)

# 3. Run Vina
result = subprocess.run([
    "vina",
    "--receptor", "receptor.pdbqt",
    "--ligand",   "ligand.pdbqt",
    "--center_x", "10.5",
    "--center_y", "-2.3",
    "--center_z", "14.1",
    "--size_x",   "20",
    "--size_y",   "20",
    "--size_z",   "20",
    "--exhaustiveness", "16",
    "--num_modes", "9",
    "--out", "docked.pdbqt"
], capture_output=True, text=True, check=True)

# 4. Parse best score
for line in result.stdout.splitlines():
    if line.strip().startswith("1 "):
        print("Best score:", line.split()[1], "kcal/mol")
        break
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Clean PDB, add H, assign protonation, define docking box | `references/protein-prep.md` |
| AutoDock Vina / Gnina docking, parameters, scoring | `references/vina-gnina.md` |
| High-throughput VS pipeline, metrics (BEDROC, EF), filtering | `references/virtual-screening.md` |
| Extract interactions (H-bonds, hydrophobic, π), ProLIF, clustering | `references/pose-analysis.md` |
| Ensemble docking, protein flexibility, MD snapshots | `references/ensemble-docking.md` |

## Key Tools

| Tool | Install | Role |
|------|---------|------|
| `vina` | `conda install -c conda-forge autodock-vina` | Docking engine (empirical scoring) |
| `gnina` | prebuilt binary or Docker | CNN scoring function |
| `pdbfixer` | `conda install -c conda-forge pdbfixer` | PDB cleaning, H addition, missing residues |
| `openbabel` | `conda install -c conda-forge openbabel` | Format conversion → PDBQT |
| `prolif` | `pip install prolif` | Protein-Ligand Interaction Fingerprints |
| `fpocket` | `conda install -c conda-forge fpocket` | Pocket detection / box definition |
| `propka` | `pip install propka` | pKa prediction for protonation |
| `meeko` | `pip install meeko` | Ligand PDBQT prep (better than obabel for Vina) |

## Scoring Function Reference

| Method | Score type | Precision | Speed | Use case |
|--------|-----------|-----------|-------|----------|
| Vina empirical | ΔG (kcal/mol) | ★★★ | ★★★★★ | VS, binding mode |
| Gnina CNN | unitless affinity | ★★★★ | ★★★★ | Rescoring, pose selection |
| MM-GB/SA | ΔG (kcal/mol) | ★★★★ | ★★ | Lead opt rescoring |
| FEP/TI | ΔΔG (kcal/mol) | ★★★★★ | ★ | Precise relative ranking |

## Installation

```bash
# Vina + OpenBabel (required)
conda install -c conda-forge autodock-vina openbabel

# pdbfixer + propka (receptor prep)
conda install -c conda-forge pdbfixer
pip install propka

# ProLIF (pose analysis)
pip install prolif

# meeko (better ligand PDBQT prep)
pip install meeko

# fpocket (pocket detection)
conda install -c conda-forge fpocket

# Gnina (CNN rescoring) — prebuilt binary
wget https://github.com/gnina/gnina/releases/latest/download/gnina
chmod +x gnina && mv gnina ~/.local/bin/

# Verify Vina
vina --version   # AutoDock Vina 1.2.x
```

## Related Skills

- `force-fields` → MM-GB/SA rescoring after docking
- `mdanalysis` → generate conformational ensemble for ensemble docking
- `homology-modeling` → build receptor when no crystal structure available
- `pharmacophore` → pharmacophore-constrained docking, pose validation
- `free-energy` → FEP/TI for accurate ΔΔG after docking hit identification
- `py3Dmol` → 3D visualization of poses inline
- Scripts: `chem_filter.py --lipinski` → pre-filter library before VS
- Scripts: `chem_3d.py` → generate 3D conformers for ligand prep
