---
name: plumed-metad
description: Metadynamics setup and analysis with PLUMED. Use when setting up
  well-tempered metadynamics, calculating free energy surfaces with sum_hills,
  reweighting trajectories, running block error analysis, or assessing convergence.
---

# PLUMED Metadynamics

Well-tempered metadynamics deposits Gaussian hills along chosen collective variables (CVs),
discouraging revisits and gradually recovering the free energy surface. Unlike umbrella sampling,
no windows are needed — the bias adapts on-the-fly. The key trade-off is CV quality: a poor CV
produces a heavily biased ensemble that is hard to reweight.

Assumes a GROMACS-patched PLUMED installation; see `gmx-install` skill if needed.
Start from an NPT-equilibrated system; see `gmx-prep` for those stages.

---

## Information to Collect

**Before generating any input files, ask the user:**

1. **CV type**: What describes the slow degree of freedom?
   - Torsion / dihedral? → atom indices or MOLINFO shortcut
   - RMSD from one reference state? → reference PDB file (suitable for folding, binding)
   - Two RMSDs (2D)? → two reference PDB files (two-state transitions)
   - Custom / path-based? → FUNC= expression and constituent CVs
2. **Reference structure(s)**: PDB file for MOLINFO and/or RMSD CVs
3. **Secondary CVs to monitor** (not biased, but printed to COLVAR for analysis)
4. **System temperature** T (K) — needed for `kBT`, reweighting, and BIASFACTOR choice
5. **BIASFACTOR** (γ): ratio of exploration temperature to system temperature
   - Small barriers (< 10 kBT): γ = 5–15
   - Large barriers (> 20 kBT): γ = 30–60
6. **SIGMA**: Gaussian width ≈ std-dev of CV in short unbiased run (run Stage 1 first)
   - Typical: 0.1–0.4 rad for torsions; 0.05 nm for RMSD
7. **Grid bounds** GRID_MIN/MAX: physical CV range (must enclose all relevant states)
8. **PACE**: Gaussian deposition interval in MD steps (default 500 = 1 ps at dt=0.002)
9. **Simulation length** (nsteps)
10. **PBC handling**: For RMSD or distance CVs, does the molecule cross periodic boundaries?
    (If yes, add `WHOLEMOLECULES ENTITY0=FIRST_ATOM-LAST_ATOM` before CV definitions.)

---

## Parameter Guide

| Parameter | Torsion / angle | Protein RMSD |
|-----------|----------------|--------------|
| SIGMA | σ of CV from unbiased run (≈ 0.1–0.4 rad) | 0.05 nm |
| BIASFACTOR | 8–15 | 30–60 |
| HEIGHT | 1.2 kJ/mol | 1.2 kJ/mol |
| PACE | 500 steps | 500 steps |
| GRID_BIN | 600 over [-π, π] | 200 over [0, max] nm |
| GRID_SPACING | ~ 0.05 rad | ~ 0.02 nm |

---

## Stage 1: Unbiased run + sigma estimation

Run a short unbiased simulation to observe CV fluctuations.

```bash
gmx mdrun -plumed plumed_unbiased.dat -s topol.tpr -nsteps 200000 -x traj_unbiased.xtc
```

```python
import plumed, numpy as np

colvar = plumed.read_as_pandas("colvar.dat")
cv1 = colvar["cv1"]

print(f"CV range visited: [{cv1.min():.3f}, {cv1.max():.3f}]")
print(f"Suggested SIGMA = {cv1.std():.3f}  (std-dev from unbiased run)")
print(f"Suggested GRID_MIN/MAX: [{cv1.min() - 3*cv1.std():.3f}, {cv1.max() + 3*cv1.std():.3f}]")
```

**Verify:** CV samples a finite range and is not stuck; std-dev is physically reasonable.

---

## Stage 2: Metadynamics simulation

Choose the template that matches your CV type and fill in parameters from Stage 1.

```bash
gmx mdrun -plumed plumed_metad_CVTYPE.dat -s topol.tpr -nsteps NSTEPS -x traj.xtc
```

Monitor progress:
```bash
tail -f COLVAR   # watch CV evolving; should diffuse broadly after a while
wc -l HILLS      # growing HILLS file confirms Gaussians are being deposited
```

**Verify:** CV explores significantly more space than the unbiased run; HILLS file is non-empty.

---

## Stage 3: Free energy surface from sum_hills

```bash
# Compute FES at STRIDE-step intervals for convergence assessment
plumed sum_hills --hills HILLS --stride STRIDE_FOR_FES --mintozero

# Output: fes_0.dat, fes_1.dat, ..., fes_N.dat
# Each file has columns: cv1 [cv2] fes [sigma]
```

```python
import plumed, numpy as np, matplotlib.pyplot as plt, glob

fes_files = sorted(glob.glob("fes_*.dat"),
                   key=lambda f: int(f.split("_")[1].split(".")[0]))

for fname in fes_files[-5:]:  # plot last 5 snapshots
    d = plumed.read_as_pandas(fname).dropna()
    plt.plot(d.iloc[:, 0], d.iloc[:, 1], label=fname)

plt.xlabel("CV"); plt.ylabel("F (kJ/mol)")
plt.legend(); plt.show()

# Quantify convergence: track ΔF between two basins
# Ask user to identify approximate basin boundaries from the FES plot
```

**Verify:** FES changes slowly between snapshots near the end of the simulation.

---

## Stage 4: Reweighting (unbiased projection)

Reweighting lets you project the unbiased FES onto any CV, including ones not biased.

```bash
# Run plumed driver on the production trajectory
plumed driver --plumed plumed_reweight.dat --ixtc traj.xtc
```

The reweight template (RESTART=YES, HEIGHT=0) reads the existing HILLS file and computes
`REWEIGHT_BIAS` logweights, which are used to produce unbiased histograms.

```python
import plumed, numpy as np, matplotlib.pyplot as plt

data = plumed.read_as_pandas("COLVAR_REWEIGHT")
cv1 = np.array(data["cv1"])
bias = np.array(data["metad.bias"])

kBT = TEMPERATURE * 8.314462618e-3
bmax = bias.max()
logW = (bias - bmax) / kBT
W = np.exp(logW)

# Weighted histogram → FES
bins = np.linspace(CV1_MIN, CV1_MAX, N_BINS + 1)
hist, edges = np.histogram(cv1, bins=bins, weights=W, density=True)
centers = 0.5 * (edges[:-1] + edges[1:])
fes = -kBT * np.log(hist + 1e-300)
fes -= fes.min()

plt.plot(centers, fes)
plt.xlabel("CV"); plt.ylabel("F (kJ/mol)")
plt.show()
```

**Verify:** Reweighted FES matches sum_hills FES in qualitative features.

---

## Stage 5: Block analysis (error estimation)

Divide the trajectory into blocks and compute free energy variance as a function of block size.
A plateau in the error curve indicates that blocks are statistically independent.

Prepare a weight file from `COLVAR_REWEIGHT`:
```python
import plumed, numpy as np

data = plumed.read_as_pandas("COLVAR_REWEIGHT")
kBT = TEMPERATURE * 8.314462618e-3
bias = np.array(data["metad.bias"])
logW = (bias - bias.max()) / kBT

with open("cv.weight", "w") as f:
    for cv_val, lw in zip(data["cv1"], logW):
        f.write(f"{cv_val:.6f} {lw:.6f}\n")
```

Run the block analysis script for multiple block sizes:
```bash
for bs in 1 2 5 10 20 50 100 200 500 1000; do
    python3 ${CLAUDE_SKILL_DIR}/templates/do_block_fes.py cv.weight 1 CV1_MIN CV1_MAX N_BINS KBT ${bs}
done
```

Plot results:
```python
import numpy as np, matplotlib.pyplot as plt, glob

block_sizes, errors = [], []
for bs in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]:
    try:
        d = np.loadtxt(f"fes.{bs}.dat")
        # Average error over the FES (exclude infinite/NaN values)
        err = np.nanmean(d[:, 2][np.isfinite(d[:, 2])])
        block_sizes.append(bs)
        errors.append(err)
    except Exception:
        pass

plt.semilogx(block_sizes, errors, "o-")
plt.xlabel("Block size (frames)"); plt.ylabel("Mean error (kJ/mol)")
plt.title("Block analysis — plateau indicates convergence")
plt.show()
```

**Verify:** Error plateaus before block size = total trajectory length / 2.

---

## Stage 6: Convergence assessment

Combine Stage 3 and Stage 5 diagnostics:
- Plot ΔF between basins as a function of simulation time (from sum_hills output)
- Compare the magnitude of ΔF fluctuations to the block analysis plateau error

**If FES is still drifting**: CV is insufficient for the process, or simulation is too short.
Consider adding dimensions, switching to a better CV, or using `plumed-remd`.

**If FES converged but block error is large**: Simulation sampled the right space but
autocorrelation is long. Run longer, or use replica methods.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| HILLS grows but FES does not change | Grid too coarse or too fine | Adjust GRID_SPACING; must be < SIGMA |
| Bias diverges / system explodes | HEIGHT too large or BIASFACTOR too small | Reduce HEIGHT; increase BIASFACTOR |
| RMSD diverges to large values | Molecule wraps across PBC | Add `WHOLEMOLECULES ENTITY0=ATOM_RANGE`; use TYPE=OPTIMAL |
| Reweighted FES differs strongly from sum_hills FES | RESTART=YES missing | Add `RESTART=YES` to METAD in reweight template |
| Block error never plateaus | Trajectory too short or CV poor | Run longer; check that multiple barrier crossings occurred |
| sum_hills: grid too small | CV visited outside GRID_MIN/MAX | Rerun with wider grid; PLUMED deposits outside grid but cannot reconstruct FES there |

---

## Working Examples (alanine dipeptide)

The `${CLAUDE_SKILL_DIR}/templates/examples/` directory contains working PLUMED input files from PLUMED Masterclass 21.4,
using alanine dipeptide in vacuum with backbone torsion angles as CVs.
Use these as a reference for syntax; adapt CV definitions for your own system.

- `plumed_ex1.dat` — Unbiased MD, MOLINFO + torsion CVs
- `plumed_ex2.dat` — 1D well-tempered METAD
- `plumed_ex3.dat` — Reweighting (RESTART=YES, COLVAR_REWEIGHT)
- `plumed_ex4.dat` — REWEIGHT_BIAS + HISTOGRAM + CONVERT_TO_FES + DUMPGRID

Run example (requires `data/diala/topolA.tpr` and `data/diala/dialaA.pdb`):
```bash
gmx mdrun -plumed ${CLAUDE_SKILL_DIR}/templates/examples/plumed_ex1.dat \
          -s data/diala/topolA.tpr -nsteps 200000
```

---

## Credits

This skill is inspired by and based on:

**PLUMED Masterclass 21.4 — Metadynamics**
Author: Max Bonomi (Institut Pasteur, Paris), 2021
https://github.com/plumed/masterclass-21-4

The `do_block_fes.py` script and the example files in `templates/examples/` are taken directly
from that masterclass. All credit for those files belongs to Max Bonomi.
The generic workflow, templates, and SKILL.md text are original additions built on top
of the masterclass material.

PLUMED is developed by the PLUMED consortium: https://www.plumed.org

---

## See Also

- `gmx-prep` — System preparation: EM → NVT → NPT
- `plumed-us` — Umbrella sampling (fixed windows, good when CV is well defined)
- `plumed-remd` — Replica exchange to enhance convergence or use multiple CVs simultaneously
