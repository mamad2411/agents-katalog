---
name: virtual-screening
description: |
  Molecular docking and virtual screening for drug discovery. Use for screening
  compound libraries against protein targets, predicting binding affinities, and
  identifying lead candidates.

  Keywords: docking, virtual screening, molecular docking, binding affinity, lead identification
category: Computational Chemistry
tags: [docking, screening, molecular-modeling, drug-design]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - rdkit
  - openbabel
  - docking-engine
---

# Virtual Screening Skill

Molecular docking and virtual screening capabilities for lead identification.

## Quick Start

```
/virtual-screening EGFR --library compounds.sdf --top 10
/dock "target.pdb" --ligands "ligands.smi" --engine vina
/screen-kinases --scaffold quinazoline --threshold -7.0
```

## Capabilities

### 1. Molecular Docking

Predict binding poses and affinities for compound-target pairs.

**Supported docking engines**:
- AutoDock Vina - Fast, widely used
- SMINA - Vina derivative with custom scoring
- DiffDock - Deep learning-based
- GNINA - Graph neural network scoring

### 2. Virtual Screening

Screen large compound libraries against targets.

**Library sources**:
- ChEMBL (bioactive compounds)
- PubChem (diverse compounds)
- ZINC (commercially available)
- Enamine (make-on-demand)

### 3. Binding Affinity Prediction

Estimate binding energies using scoring functions.

### 4. Pose Analysis

Analyze binding modes and key interactions.

## Docking Workflow

```
1. Target Preparation
   ├── Retrieve PDB structure
   ├── Remove water/ligands
   ├── Add hydrogens
   └── Define binding site

2. Ligand Preparation
   ├── Generate 3D conformations
   ├── Minimize energy
   └── Generate protonation states

3. Docking
   ├── Set grid box
   ├── Run docking engine
   └── Generate poses

4. Analysis
   ├── Score poses
   ├── Analyze interactions
   └── Rank compounds
```

## Output Structure

### Docking Results

```markdown
# Virtual Screening Results: EGFR Kinase

## Summary
| Metric | Value |
|--------|-------|
| Compounds screened | 10,000 |
| Successful dockings | 9,847 |
| Top hits (≤ -8 kcal/mol) | 47 |
| Processing time | 2.5 hours |

## Top 10 Compounds

| Rank | Compound ID | Affinity (kcal/mol) | LE | LLE | Interactions |
|------|-------------|---------------------|-----|-----|--------------|
| 1 | CHEMBL210 | -10.2 | 0.42 | 6.8 | H-bond: Met793, hinge |
| 2 | CHEMBL456 | -9.8 | 0.38 | 6.5 | H-bond: Met793, Lys745 |
| 3 | ZINC12345 | -9.5 | 0.35 | 6.2 | π-π: Phe723 |

## Binding Mode Analysis (Top Hit)

### Compound: CHEMBL210
**Affinity**: -10.2 kcal/mol
**LE**: 0.42
**LLE**: 6.8

**Key Interactions**:
- H-bond with Met793 (hinge region)
- H-bond with Thr854
- π-π stacking with Phe723
- Hydrophobic pocket: Le718, Val726

## Pharmacophore Features

1. **Hinge binder**: N-heterocycle H-bond donor/acceptor
2. **Gatekeeper interaction**: Small hydrophobic group
3. **Solvent front**: Polar substituent
4. **Back pocket**: Extended hydrophobic moiety

## Recommendations

1. **Synthesis priority**: Top 5 compounds
2. **SAR exploration**: Around quinazoline core
3. **Experimental validation**: SPR, ITC binding assays
```

## Scoring Metrics

| Metric | Formula | Good Range |
|--------|---------|------------|
| Binding affinity | Docking score | ≤ -7 kcal/mol |
| Ligand Efficiency (LE) | Score / Heavy atoms | ≥ 0.3 |
| LLE (LipE) | Score - LogP | ≥ 6 |
| Size | Heavy atom count | 20-40 |

## Running Scripts

```bash
# Virtual screening with Vina
python scripts/virtual_screening.py \
  --target EGFR \
  --library data/compounds.sdf \
  --top 50 \
  --output results.json

# Docking with custom settings
python scripts/docking.py \
  --pdb 1m17.pdb \
  --center_x 10.5 \
  --center_y 20.3 \
  --center_z 15.8 \
  --size_x 20 \
  --size_y 20 \
  --size_z 20

# Rescoring with GNINA
python scripts/rescore.py \
  --poses docked_poses.sdf \
  --model gnina \
  --output rescored.json
```

## Requirements

```bash
# Core dependencies
pip install rdkit meeko

# Docking engines
# AutoDock Vina: http://vina.scripps.edu/
# SMINA: https://github.com/ccsb-scripps/AutoDock-Vina
# GNINA: https://github.com/gnina/gnina

# Optional
pip install prody pymol-open-source
```

## Reference

- See [reference/docking-guide.md](reference/docking-guide.md) for detailed docking protocols
- See [reference/scoring-functions.md](reference/scoring-functions.md) for scoring function details
- See [reference/structure-prep.md](reference/structure-prep.md) for protein preparation

## Best Practices

1. **Prepare structures carefully**: Clean PDB, remove duplicates
2. **Validate docking protocol**: Re-dock co-crystal ligand
3. **Consider multiple poses**: Top 3-5 poses per compound
4. **Use consensus scoring**: Combine multiple scoring functions
5. **Check binding modes**: Visual inspection of top poses
6. **Account for flexibility**: Consider induced fit if needed

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Incorrect binding site | Validate with known inhibitor |
| Poor ligand preparation | Generate multiple conformations |
| Single scoring function | Use consensus scoring |
| Ignoring protein flexibility | Use ensemble docking |
| Overinterpreting scores | Remember scoring is approximate |

## Limitations

- **Scoring accuracy**: ±2 kcal/mol typical error
- **Protein flexibility**: Limited in standard docking
- **Solvent effects**: Often implicit/explicit simplified
- **Binding kinetics**: Not predicted (affinity only)
- **Synthetic accessibility**: Not assessed
