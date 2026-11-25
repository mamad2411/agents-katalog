---
name: free-energy
description: Use when computing free energy differences for drug discovery. Covers FEP/TI/BAR/MBAR theory, alchemical transformations with OpenMMTools, relative binding free energy (RBFE) protocols, absolute binding free energy (ABFE), pymbar analysis, convergence diagnostics, and standard state corrections.
---

# Free Energy Calculations

Compute ΔG of binding, solvation, or mutation via alchemical transformations — coupling/decoupling atoms along a λ pathway. Gold standard for lead optimization in drug discovery: accuracy ~1 kcal/mol for congeneric series.

## When to Use This Skill

- Predict ΔΔG_bind between two ligands (RBFE / lead optimization)
- Compute absolute ΔG_bind of a ligand to a protein (ABFE)
- Calculate ΔG_solvation or ΔG_hydration for ADME
- Rank compounds from a small congeneric series (~5-50 molecules)
- Validate force field parameters against experimental affinities
- Analyze convergence of FEP simulations (MBAR, overlap matrix)

## Key Methods

| Method | Estimator | Windows | Notes |
|--------|-----------|---------|-------|
| FEP (Zwanzig) | Exponential avg | Any | High variance; avoid for large ΔG |
| TI | Numerical integration of ⟨∂H/∂λ⟩ | 10-20 | Requires smooth integrand |
| BAR | Bennett Acceptance Ratio | Adjacent pairs | Better than TI for same data |
| **MBAR** | Multistate BAR | All pairs | Best variance; recommended |
| RBFE | Relative: A→B via alchemical | 12-24 λ | Lead optimization |
| ABFE | Absolute: ligand → unbound | ~20 λ | More expensive, independent |

## Accuracy Expectations

| System | Typical error | Sim. time per edge |
|--------|--------------|-------------------|
| Congeneric RBFE (neutral) | 0.5-1.5 kcal/mol | 5-10 ns/window |
| RBFE with charge change | 1-3 kcal/mol | 10-20 ns/window |
| ABFE | 1-3 kcal/mol | 20-50 ns/window |
| Solvation ΔG | 0.3-1.0 kcal/mol | 2-5 ns/window |

## Quick Start

```python
# pymbar: MBAR from energy matrix (u_kln)
import numpy as np
from pymbar import MBAR

# u_kln[k, l, n] = u_l(x_n^k) / kBT
# k: state from which sample was drawn
# l: state at which energy is evaluated
# n: sample index

K = 12  # number of lambda windows
N_k = np.array([1000] * K)  # samples per window

# u_kln shape: (K, K, max(N_k))
mbar = MBAR(u_kln, N_k)
results = mbar.compute_free_energy_differences()

dG = results['Delta_f'][0, -1]           # ΔG (kBT units)
ddG = results['dDelta_f'][0, -1]         # uncertainty
kBT = 0.5961  # kcal/mol at 298 K

print(f"ΔG = {dG * kBT:.2f} ± {ddG * kBT:.2f} kcal/mol")
```

## Router — What to Read

| Task | Reference |
|------|-----------|
| FEP/TI/BAR/MBAR theory, thermodynamic cycles, alchemical path | `references/fep-theory.md` |
| OpenMMTools: AlchemicalFactory, ThermodynamicState, MCMC sampling | `references/openmmtools-alchemical.md` |
| RBFE protocol: edge network, protein-ligand, results | `references/rbfe-protocol.md` |
| ABFE: restraints, double-decoupling, standard state correction | `references/abfe-protocol.md` |
| pymbar, overlap matrix, convergence, uncertainty, phase space | `references/pymbar-analysis.md` |

## Software Stack

| Package | Install | Role |
|---------|---------|------|
| `pymbar` | `pip install pymbar` | MBAR/BAR/FEP estimators |
| `openmmtools` | `conda install -c conda-forge openmmtools` | Alchemical factories, MCMC |
| `perses` | `conda install -c conda-forge perses` | RBFE pipeline (OpenMM-native) |
| `openfe` | `pip install openfe` | FE campaign management (Lomap + OpenMM) |
| `alchemtest` | `pip install alchemtest` | Test datasets for FE code |
| `lomap2` | `pip install lomap2` | Ligand network RBFE planning |

## Related Skills

- `force-fields` — system parameterization; OpenFF Sage for ligands
- `docking` — starting poses for ABFE; initial ranking before FEP
- `mdanalysis` — trajectory analysis from FEP runs
- `scientific-skills:rowan` — cloud FEP without local HPC
