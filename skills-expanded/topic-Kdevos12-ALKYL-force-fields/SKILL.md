---
name: force-fields
description: Use when working with molecular mechanics force fields for MD simulations. Covers force field theory (AMBER/CHARMM/OPLS/SMIRNOFF), OpenMM simulation setup, OpenFF/SMIRNOFF parameterization of small molecules, GAFF2/antechamber, partial charge methods (AM1-BCC, RESP), energy decomposition, and water models.
---

# Force Fields — Molecular Mechanics for MD Simulations

Classical force fields define the potential energy of a molecular system as a sum of bonded and non-bonded terms. The parameters (k, r0, θ0, ε, σ, q) define how molecules move and interact. Python-first stack: **OpenMM** (engine) + **OpenFF toolkit** (SMIRNOFF small molecule parameterization).

## When to Use This Skill

- Setting up MD simulations with AMBER, CHARMM, or OpenFF force fields
- Parameterizing drug-like small molecules (GAFF2, SMIRNOFF Sage)
- Running energy minimization and MD with OpenMM
- Assigning partial charges (AM1-BCC, RESP)
- Understanding energy terms: bonds, angles, torsions, vdW, electrostatics
- Choosing water model (TIP3P, OPC, TIP4P-Ew)
- Analyzing energy decomposition by force group

## Quick Start

```python
# Protein-ligand simulation with OpenMM + OpenFF (SMIRNOFF Sage)
from openff.toolkit import Molecule, ForceField
from openff.toolkit.utils.exceptions import ParameterLookupError
from openmmforcefields.generators import SystemGenerator
import openmm.app as app
import openmm as mm
import openmm.unit as unit

# 1. Load protein topology
pdb = app.PDBFile('protein.pdb')

# 2. Parameterize ligand with OpenFF Sage
ligand = Molecule.from_smiles('c1ccc(cc1)CN')
ligand.generate_conformers(n_conformers=1)

# 3. Build system
system_generator = SystemGenerator(
    forcefields=['amber/ff14SB.xml', 'amber/tip3p_standard.xml'],
    small_molecule_forcefield='openff-2.2.0',
    molecules=[ligand],
    forcefield_kwargs={'nonbondedMethod': app.PME, 'constraints': app.HBonds},
)
system = system_generator.create_system(pdb.topology, molecules=[ligand])

# 4. Run with Langevin integrator
integrator = mm.LangevinMiddleIntegrator(
    300 * unit.kelvin, 1.0 / unit.picosecond, 2.0 * unit.femtoseconds
)
simulation = app.Simulation(pdb.topology, system, integrator)
simulation.context.setPositions(pdb.positions)
simulation.minimizeEnergy(maxIterations=500)
simulation.reporters.append(app.DCDReporter('traj.dcd', 1000))
simulation.step(50000)  # 100 ps
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| Force field theory: energy terms, AMBER/CHARMM/OPLS/GROMOS families | `references/ff-fundamentals.md` |
| OpenMM: System, Simulation, integrators, reporters, NPT, restart | `references/openmm-basics.md` |
| OpenFF SMIRNOFF toolkit: Molecule, parameterization, Sage 2.2 | `references/openff-smirnoff.md` |
| GAFF2/antechamber, acpype, CGenFF, AM1-BCC, RESP charges | `references/parameterization.md` |
| Energy decomposition, PME, cutoffs, water models, troubleshooting | `references/energy-analysis.md` |

## Force Field Families at a Glance

| Family | Protein FF | Small Molecule FF | Engine |
|--------|-----------|-------------------|--------|
| AMBER | ff14SB, ff19SB | GAFF2 | OpenMM, AMBER |
| CHARMM | CHARMM36m | CGenFF | OpenMM, NAMD, GROMACS |
| OPLS | OPLS-AA/M | OPLS3e | GROMACS, Schrödinger |
| OpenFF | — | Sage 2.2, Parsley | OpenMM |
| GROMOS | 54A7 | GROMOS-compat | GROMACS (united-atom) |

## Installation

```bash
# OpenMM (engine)
conda install -c conda-forge openmm

# OpenFF toolkit + Sage FF
pip install openff-toolkit
pip install openmmforcefields  # bridges OpenFF → OpenMM + GAFF2

# AMBER Tools (antechamber / tleap)
conda install -c conda-forge ambertools

# acpype (antechamber wrapper → GROMACS/AMBER topology)
conda install -c conda-forge acpype

# ParmEd (topology manipulation)
pip install parmed

# Verify
python -c "import openmm; print(openmm.__version__)"
python -c "from openff.toolkit import Molecule; print('OpenFF OK')"
```

## Related Skills

- `ase` — geometry optimization with QM calculators (ORCA, xTB, GPAW)
- `mdanalysis` — trajectory analysis after MD runs
- `docking` — pre-docking protein prep; post-MD ensemble docking
- `scientific-skills:pymatgen` — periodic materials, materials force fields (ReaxFF)
- scripts: `chem_3d.py` — RDKit 3D conformer generation (pre-MD structure)
