---
name: qm-dft
description: Use when working with quantum chemistry (QM) and DFT calculations. Covers DFT functional/basis set selection, ORCA input/output, xTB semi-empirical methods (GFN2, CREST), PySCF Python-native QM, and standard workflows (geometry opt, frequencies, NMR, TD-DFT, reaction barriers, RESP charges).
---

# QM/DFT — Quantum Chemistry Calculations

Quantum mechanics-based methods compute electronic structure explicitly — enabling bond breaking/forming, spectroscopic properties, and accurate energetics beyond force fields. Python ecosystem: **ORCA** (best free QM, subprocess), **xTB/tblite** (fast semi-empirical, Python API), **PySCF** (pure Python, scriptable).

## When to Use This Skill

- Geometry optimization with QM accuracy (beyond MM force fields)
- Reaction energetics: transition states, barrier heights, IRC
- Spectroscopy: IR/Raman frequencies, NMR shifts, UV-Vis (TD-DFT)
- Partial charge calculation: RESP, ESP, NBO, Mulliken
- pKa estimation, protonation states
- Conformer search and ranking (CREST + xTB)
- Parametrization validation: compare QM vs force field energies
- Property prediction: dipole moment, polarizability, HOMO/LUMO gaps

## Method Cost Hierarchy

| Method | Cost | Accuracy | Use case |
|--------|------|----------|----------|
| GFN-FF | O(N²) | ~MM | Pre-screening, conformers |
| GFN2-xTB | O(N²·8) | Good | Conformers, pre-opt, pKa |
| r²SCAN-3c | O(N³) | Very good | Routine geometry opt |
| B3LYP-D3BJ/def2-SVP | O(N⁴) | Good | Drug-like molecules opt |
| B3LYP-D3BJ/def2-TZVP | O(N⁴) | Better | Single-point on opt geom |
| ωB97X-D/def2-TZVP | O(N⁴) | Very good | Reaction barriers, CT states |
| DLPNO-CCSD(T)/CBS | O(N⁵⁺) | Benchmark | High-accuracy energetics |

## Quick Start

```python
# xTB geometry optimization (fastest QM-level method)
import subprocess

result = subprocess.run(
    ['xtb', 'mol.xyz', '--opt', '--gfn', '2', '--alpb', 'water'],
    capture_output=True, text=True, cwd='workdir/'
)
# Output: xtbopt.xyz (optimized), xtbopt.log

# Parse final energy
for line in result.stdout.split('\n'):
    if 'TOTAL ENERGY' in line:
        energy = float(line.split()[3])  # Hartree
        print(f"E = {energy:.8f} Eh")
```

```python
# ORCA single-point DFT (via subprocess)
orca_input = """\
! B3LYP D3BJ def2-SVP TightSCF
%pal nprocs 4 end
%maxcore 2000

* xyzfile 0 1 mol.xyz
"""

with open('sp.inp', 'w') as f:
    f.write(orca_input)

result = subprocess.run(['orca', 'sp.inp'], capture_output=True, text=True)
# Parse with chem_qm.py: python chem_qm.py --parse sp.out
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| DFT functionals, basis sets, dispersion, Jacob's ladder | `references/dft-theory.md` |
| ORCA: input syntax, optimization, freq, NMR, TD-DFT, output parsing | `references/orca-practical.md` |
| xTB/GFN2: CLI, Python (tblite), CREST, solvation, pKa | `references/xtb-semiempirical.md` |
| PySCF: Python QM, HF/DFT/MP2/CCSD, NMR, ESP charges | `references/pyscf-python.md` |
| Standard recipes: opt→freq, RESP, UV-Vis, barriers, NBO | `references/common-workflows.md` |

## Key Tools

| Tool | Version | Install | Role |
|------|---------|---------|------|
| ORCA | 6.0 | orca-forum.org (free) | General QM: DFT, MP2, CCSD(T), TD-DFT |
| xTB | 6.7 | `conda install -c conda-forge xtb` | Fast semi-empirical |
| tblite | 0.3 | `pip install tblite` | xTB Python API |
| CREST | 3.0 | `conda install -c conda-forge crest` | Conformer/ensemble search |
| PySCF | 2.7 | `pip install pyscf` | Python-native QM |
| Psi4 | 1.9 | `conda install -c conda-forge psi4` | Python QM + MP2/CCSD |

## Related Skills

- `ase` — structure building, ASE-driven optimization with ORCA/xTB calculators
- `force-fields` — pre-optimize with MM before QM; GAFF2 validation
- `docking` — QM refinement of top docking poses
- scripts: `chem_qm.py` — ORCA/Gaussian input gen + output parsing (ALKYL native)
- `scientific-skills:rowan` — cloud QM (DFT, pKa, Chai-1) without local ORCA install
