---
name: mdanalysis
description: Use when analyzing molecular dynamics trajectories with MDAnalysis. Covers Universe/AtomGroup, RMSD/RMSF/alignment, contacts and hydrogen bonds, dihedral/secondary structure/PCA analysis, and protein-ligand binding analysis.
---

# MDAnalysis — MD Trajectory Analysis

MDAnalysis 2.10.0 (2025). Core pattern: `Universe` (topology + trajectory) → `AtomGroup` (selection) → `AnalysisBase.run()` → `.results`.

## When to Use This Skill

- Loading GROMACS, AMBER, NAMD, CHARMM, LAMMPS trajectories
- RMSD and RMSF calculations (protein stability, flexibility)
- Structural alignment across trajectory frames
- Hydrogen bond detection and lifetime analysis
- Protein-ligand contacts and binding site analysis
- Dihedral angles (Ramachandran plots, chi angles)
- Secondary structure (DSSP) assignment
- PCA of conformational dynamics
- Radial distribution functions (RDF), density maps
- Mean square displacement (MSD), diffusion coefficients

## Quick Start

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms, align

# Load topology + trajectory
u = mda.Universe('protein.prmtop', 'traj.dcd')
print(u)                   # <Universe with 45000 atoms>
print(len(u.trajectory))   # number of frames

# Select atoms
protein = u.select_atoms('protein')
ca      = u.select_atoms('protein and name CA')
ligand  = u.select_atoms('resname LIG')

# Iterate trajectory
for ts in u.trajectory:
    print(ts.frame, ts.time, ca.positions.mean(axis=0))
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Universe, topology formats, selections, trajectory I/O, writing | `references/universe-selections.md` |
| RMSD, RMSF, alignment, radius of gyration | `references/rmsd-rmsf-alignment.md` |
| Hydrogen bonds, native contacts, binding residues | `references/contacts-hbonds.md` |
| Dihedrals, DSSP, PCA, RDF, density, MSD | `references/structure-dynamics.md` |
| Protein-ligand interaction analysis workflow | `references/protein-ligand.md` |

## Key Modules

| Module | Import | Role |
|--------|--------|------|
| `rms` | `from MDAnalysis.analysis import rms` | RMSD, RMSF |
| `align` | `from MDAnalysis.analysis import align` | Structural alignment |
| `contacts` | `from MDAnalysis.analysis import contacts` | Native contacts |
| `hydrogenbonds` | `from MDAnalysis.analysis.hydrogenbonds.hbond_analysis import HydrogenBondAnalysis` | H-bonds |
| `dihedrals` | `from MDAnalysis.analysis.dihedrals import Ramachandran, Janin` | Dihedral angles |
| `dssp` | `from MDAnalysis.analysis.dssp import DSSP` | Secondary structure |
| `pca` | `from MDAnalysis.analysis.pca import PCA` | Conformational PCA |
| `rdf` | `from MDAnalysis.analysis.rdf import InterRDF` | Radial distribution |
| `density` | `from MDAnalysis.analysis.density import DensityAnalysis` | Density maps |
| `msd` | `from MDAnalysis.analysis.msd import EinsteinMSD` | Diffusion |
| `distances` | `from MDAnalysis.analysis.distances import dist, between` | Distances |

## Supported Formats

```
Topology:  PSF, PRMTOP (Amber), GRO (GROMACS), PDB, MOL2, TPR, CRD, XML
Trajectory: DCD, XTC, TRR, NC (Amber), LAMMPSDUMP, H5MD, TNG, XYZ, PDB
```

## Installation

```bash
pip install MDAnalysis MDAnalysisData
conda install -c conda-forge mdanalysis

# Verify
python -c "import MDAnalysis; print(MDAnalysis.__version__)"
```

## AnalysisBase Pattern (all analysis modules)

```python
analysis = SomeAnalysis(atomgroup, **params)
analysis.run(start=0, stop=None, step=1, verbose=True)
results = analysis.results      # dict-like Results object
```

## Related Skills

- `ase` — ASE MD trajectories, structure building (complementary)
- `scientific-skills:matplotlib` — plotting RMSD, RMSF curves
- `scientific-skills:seaborn` — heatmaps for contact maps
- `scientific-skills:plotly` — interactive conformational space plots
- `scientific-skills:biopython` — PDB fetching and sequence tools
