---
name: ase
description: Use when working with ASE (Atomic Simulation Environment) for atomistic simulations. Covers structure building, geometry optimization, molecular dynamics, NEB/transition states, vibrational analysis, and calculator interfaces (ORCA, xTB, GPAW, LAMMPS).
---

# ASE — Atomic Simulation Environment

ASE 3.24.0 (December 2024). Central object: `Atoms`. Calculators are decoupled — swap between EMT, xTB, ORCA, GPAW without changing workflow.

## When to Use This Skill

- Building and manipulating atomic structures (molecules, surfaces, bulk, slabs)
- Geometry optimization (DFT, semi-empirical, force fields)
- Molecular dynamics: NVE, NVT (Langevin, Berendsen), NPT
- Transition state search: NEB, climbing image, AutoNEB
- Vibrational analysis, IR spectra, zero-point energy, thermochemistry
- Interfacing with ORCA, GPAW, xTB, VASP, LAMMPS, Quantum ESPRESSO
- Reading/writing structure files: CIF, XYZ, TRAJ, SDF, PDB, VASP POSCAR

## Quick Start

```python
from ase import Atoms
from ase.build import molecule
from ase.calculators.emt import EMT
from ase.optimize import BFGS

# Build water molecule
atoms = molecule('H2O')
atoms.calc = EMT()  # fast toy calculator

# Geometry optimization
opt = BFGS(atoms, trajectory='h2o.traj', logfile='opt.log')
opt.run(fmax=0.05)  # eV/Å convergence criterion

print(atoms.get_potential_energy())  # eV
print(atoms.get_forces())            # eV/Å
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Atoms object, cell, PBC, building molecules/surfaces/bulk | `references/atoms-structures.md` |
| Calculators: EMT, ORCA, xTB, GPAW, LAMMPS, config | `references/calculators.md` |
| Geometry optimization, constraints, filters, unit cells | `references/optimization.md` |
| Molecular dynamics: NVE/NVT/NPT, thermostats, trajectories | `references/molecular-dynamics.md` |
| NEB, climbing image, IDPP, AutoNEB, barrier extraction | `references/neb-transitions.md` |
| Vibrations, phonons, IR, ZPE, thermochemistry | `references/vibrations-analysis.md` |

## Key Modules

| Module | Import | Role |
|--------|--------|------|
| `Atoms` | `from ase import Atoms` | Core structure object |
| `units` | `from ase import units` | Unit conversions (eV, Å, fs…) |
| `io` | `from ase import io` | Read/write all formats |
| `build` | `from ase.build import …` | molecule, bulk, surface, slab |
| `optimize` | `from ase.optimize import BFGS, FIRE, LBFGS` | Geometry optimizers |
| `md` | `from ase.md.verlet import VelocityVerlet` | Molecular dynamics |
| `mep` | `from ase.mep import NEB, DyNEB` | Minimum energy paths |
| `vibrations` | `from ase.vibrations import Vibrations` | Normal modes |
| `phonons` | `from ase.phonons import Phonons` | Phonon dispersion |
| `constraints` | `from ase.constraints import FixAtoms, FixBondLength` | Constraints |
| `filters` | `from ase.filters import ExpCellFilter, FrechetCellFilter` | Cell optimization |
| `db` | `from ase.db import connect` | ASE database |

## Installation

```bash
pip install ase          # latest (3.24.0+)
conda install -c conda-forge ase

# Verify
python -c "import ase; print(ase.__version__)"
```

## Unit Conversions

```python
from ase import units

units.eV           # 1.0 (internal unit)
units.Hartree      # 27.2114 eV
units.kcal / units.mol  # 0.04336 eV
units.fs           # femtosecond in ASE time units
units.bar          # pressure
units.Bohr         # 0.529177 Å
```

## Related Skills

- `ase` + `scientific-skills:rowan` — cloud QM (DFT, pKa) for heavy calculations
- `ase` + `scientific-skills:pymatgen` — materials/crystallography workflows
- scripts: `chem_qm.py` — ORCA/Gaussian input gen + output parsing
- `scientific-skills:biopython` — PDB structure loading for biomolecular systems
