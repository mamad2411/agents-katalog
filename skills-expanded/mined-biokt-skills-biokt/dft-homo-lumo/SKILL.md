---
name: dft-homo-lumo
description: DFT geometry optimisation and HOMO/LUMO frontier orbital analysis for
  small molecules. Use when calculating HOMO/LUMO energies or molecular orbitals,
  optimising a molecule with DFT, generating cube files for orbital visualisation,
  running PySCF calculations from a SMILES string or molecule name, or comparing
  frontier orbitals between charged and neutral species.
---

# DFT HOMO/LUMO Analysis with PySCF

## Workflow Overview

```
SMILES / name → RDKit (3D XYZ) → PySCF DFT optimisation → SCF → HOMO/LUMO energies + cube files → py3Dmol visualisation
```

---

## Environment Setup

Use the `qc` conda environment:

```bash
conda activate qc
python -c "import pyscf, geometric, py3Dmol; print('ok')"
```

If the environment does not exist, create it:

```bash
conda create -n qc python=3.11 -c conda-forge pyscf geometric rdkit py3dmol jupyterlab matplotlib numpy scipy -y
conda activate qc
pip install pyscf-dispersion   # wB97X-D3 support; falls back gracefully if unavailable
```

---

## Directory Layout

```
MOLECULE/
├── smiles.txt
├── dft/
│   ├── inputs/
│   │   ├── gen_structures.py
│   │   └── MOLECULE.xyz          # generated 3D geometry
│   ├── scripts/
│   │   └── dft_opt_mo.py         # main PySCF workflow
│   ├── runs/
│   │   └── MOLECULE/
│   │       ├── opt.log           # optimisation log
│   │       ├── opt_geom.xyz      # optimised geometry (Angstrom)
│   │       ├── scf.chk           # PySCF checkpoint (MO coefficients)
│   │       ├── homo.cube         # HOMO volumetric data
│   │       ├── lumo.cube         # LUMO volumetric data
│   │       └── density.cube      # electron density
│   └── notebooks/
│       └── homo_lumo_analysis.ipynb
```

Create directories:

```bash
mkdir -p MOLECULE/dft/{inputs,scripts,runs/MOLECULE,notebooks}
```

---

## Step 1 — SMILES → 3D XYZ (RDKit)

```python
from rdkit import Chem
from rdkit.Chem import AllChem

def smiles_to_xyz(smiles, name, charge, out_path):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    AllChem.EmbedMolecule(mol, params)
    AllChem.MMFFOptimizeMolecule(mol)

    conf = mol.GetConformer()
    atoms = [mol.GetAtomWithIdx(i).GetSymbol() for i in range(mol.GetNumAtoms())]
    coords = conf.GetPositions()

    with open(out_path, "w") as f:
        f.write(f"{len(atoms)}\n{name}  charge={charge}\n")
        for sym, pos in zip(atoms, coords):
            f.write(f"{sym:<4s} {pos[0]:14.8f} {pos[1]:14.8f} {pos[2]:14.8f}\n")
```

Key notes:
- Always add explicit hydrogens with `Chem.AddHs` before embedding
- ETKDGv3 + MMFF pre-optimisation gives a clean starting geometry
- For charged molecules, encode the charge in the SMILES (e.g. `[NH4+]`, `[O-]`)
- If you have an existing mol2 or SDF file, read it with `Chem.MolFromMol2File` / `Chem.MolFromMolFile` instead

---

## Step 2 — DFT Geometry Optimisation (PySCF + geomeTRIC)

```python
from pyscf import gto, dft
from pyscf.geomopt import geometric_solver

mol = gto.Mole()
mol.atom   = open("MOLECULE.xyz").readlines()[2:]   # skip header
mol.atom   = "; ".join(l.strip() for l in mol.atom if l.strip())
mol.charge = CHARGE    # integer, e.g. 0, 1, -1
mol.spin   = SPIN      # 2S; 0 for closed-shell (even electrons, singlet)
mol.basis  = "def2-TZVP"
mol.verbose = 4
mol.output  = "opt.log"
mol.build()

mf = dft.RKS(mol)      # RKS for closed-shell; UKS for open-shell
mf.xc          = "CAM-B3LYP"   # or "wB97X-D3" if pyscf-dispersion installed
mf.grids.level = 4
mf.chkfile     = "scf.chk"

mol_opt = geometric_solver.optimize(mf, maxsteps=300,
                                    convergence_energy=1e-6,
                                    convergence_grms=3e-4)
```

**Charge/spin rules:**
| Molecule type | charge | spin |
|---|---|---|
| Neutral, even electrons, singlet | 0 | 0 |
| Cation (+1), even total electrons | 1 | 0 |
| Anion (−1), even total electrons | −1 | 0 |
| Radical (odd electrons) | 0 or ±1 | 1 |

To check: `mol.nelectron` must be even for `spin=0` (RKS). Odd → use `UKS` with `spin=1`.

**Functional choice:**
| Functional | PySCF keyword | Notes |
|---|---|---|
| CAM-B3LYP | `"CAM-B3LYP"` | Default; no extension needed; good for frontier MOs |
| wB97X-D3 | `"wB97X-D3"` | Best overall; requires `pip install pyscf-dispersion` |
| B3LYP | `"B3LYP"` | Standard hybrid; less accurate for CT systems |
| PBE0 | `"PBE0"` | Good general-purpose hybrid |

**Basis set choice:**
| Basis | Notes |
|---|---|
| `def2-TZVP` | Default; triple-zeta, good accuracy/cost balance |
| `def2-QZVP` | Higher accuracy single-point after opt at TZVP |
| `6-311+G(d,p)` | Pople basis; alternative for comparison |

---

## Step 3 — Final SCF and MO Extraction

```python
import numpy as np
from pyscf import dft
from pyscf.tools import cubegen

HARTREE_TO_EV = 27.2114

# Run final SCF on optimised geometry
mf_final = dft.RKS(mol_opt)
mf_final.xc          = "CAM-B3LYP"
mf_final.grids.level = 4
mf_final.chkfile     = "scf.chk"
mf_final.kernel()

# HOMO/LUMO indices
homo_idx = int(np.where(mf_final.mo_occ > 0)[0][-1])
lumo_idx = homo_idx + 1

homo_ev = mf_final.mo_energy[homo_idx] * HARTREE_TO_EV
lumo_ev = mf_final.mo_energy[lumo_idx] * HARTREE_TO_EV
gap_ev  = lumo_ev - homo_ev

print(f"HOMO: {homo_ev:.4f} eV")
print(f"LUMO: {lumo_ev:.4f} eV")
print(f"Gap:  {gap_ev:.4f} eV")

# Cube files (nx=80 ≈ 0.1 Å resolution; use 120 for publication quality)
cubegen.orbital(mol_opt, "homo.cube", mf_final.mo_coeff[:, homo_idx], nx=80, ny=80, nz=80)
cubegen.orbital(mol_opt, "lumo.cube", mf_final.mo_coeff[:, lumo_idx], nx=80, ny=80, nz=80)
cubegen.density(mol_opt, "density.cube", mf_final.make_rdm1(),          nx=80, ny=80, nz=80)
```

**Verify:**
```bash
# Cube files should be ~5 MB each at nx=80
ls -lh runs/MOLECULE/*.cube

# Check optimisation converged
grep "Converged" runs/MOLECULE/opt.log
```

---

## Step 4 — Visualisation in Jupyter (py3Dmol)

```python
import py3Dmol
from pathlib import Path

def view_orbital(xyz_path, cube_path, isovalue=0.05, width=500, height=400):
    xyz_str  = Path(xyz_path).read_text()
    cube_str = Path(cube_path).read_text()
    view = py3Dmol.view(width=width, height=height)
    view.addModel(xyz_str, "xyz")
    view.setStyle({"stick": {"radius": 0.15}, "sphere": {"radius": 0.25}})
    view.addVolumetricData(cube_str, "cube", {"isoval":  isovalue, "color": "blue", "opacity": 0.7})
    view.addVolumetricData(cube_str, "cube", {"isoval": -isovalue, "color": "red",  "opacity": 0.7})
    view.zoomTo()
    return view

view_orbital("runs/MOLECULE/opt_geom.xyz", "runs/MOLECULE/homo.cube").show()
view_orbital("runs/MOLECULE/opt_geom.xyz", "runs/MOLECULE/lumo.cube").show()
```

Standard isovalue: **0.05** for display; decrease to 0.02 to show more of the orbital extent.

---

## Reference Results: Guanidinium / Guanidine

A worked example is in:
`~/Research/Projects/Simulation/Claude/parameterize/dft/`

| Molecule | Charge | HOMO (eV) | LUMO (eV) | Gap (eV) |
|---|---|---|---|---|
| Guanidinium | +1 | −15.08 | −3.51 | 11.57 |
| Guanidine | 0 | −8.15 | +1.47 | 9.63 |

Method: CAM-B3LYP/def2-TZVP. Scripts: `dft/scripts/dft_opt_mo.py`. Notebook: `dft/notebooks/homo_lumo_analysis.ipynb`.

---

## Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `import pyscf` fails | Wrong conda env | `conda activate qc` |
| `ETKDGv3 embedding failed` | Bad SMILES or strained ring | Check SMILES with `Chem.MolFromSmiles`; try 2D→3D in Avogadro |
| `mol.nelectron` is odd with `spin=0` | Mismatch | Recount electrons; use `UKS` with `spin=1` for radicals |
| `SCF not converged` | Difficult electronic structure | Try `mf.max_cycle = 200`; or `mf.init_guess = "atom"` |
| `geometric: optimization failed` | Bad starting geometry or forces | Tighten MMFF pre-opt; reduce step size with `trust=0.1` |
| `cubegen` cube file is empty | SCF not run before cubegen | Always call `mf_final.kernel()` before `cubegen.orbital` |
| `wB97X-D3` not found | pyscf-dispersion missing | `pip install pyscf-dispersion`; or fall back to `CAM-B3LYP` |

---

## Key Parameter Choices

| Parameter | Default | When to change |
|---|---|---|
| Functional | CAM-B3LYP | Use wB97X-D3 for better dispersion; B3LYP for comparison with literature |
| Basis | def2-TZVP | Use def2-QZVP for high-accuracy single-point after opt |
| Grid level | 4 | Increase to 5 for high-accuracy integration (meta-GGAs, small gaps) |
| Cube grid | 80³ | Increase to 120³ for publication-quality images |
| `RKS` vs `UKS` | RKS (closed-shell) | Use UKS for radicals, triplets, or molecules with odd electrons |

---

## Integration with AMBER Parameterisation

After DFT optimisation, the `opt_geom.xyz` can be used as a higher-quality starting geometry for the AMBER parameterisation workflow instead of the Open Babel geometry:

```bash
obabel runs/MOLECULE/opt_geom.xyz -o mol2 -O mol2/MOLECULE.mol2
# Then continue with antechamber → parmchk2 → tleap as in the amber-parameterize skill
```

The DFT Mulliken or RESP charges can also replace AM1-BCC charges for higher accuracy.
See the `amber-parameterize` skill for the downstream GROMACS conversion.
