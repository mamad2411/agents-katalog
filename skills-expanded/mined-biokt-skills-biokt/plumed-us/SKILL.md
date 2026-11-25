---
name: plumed-us
description: Umbrella sampling setup and analysis with PLUMED. Use when setting up
  multi-window umbrella sampling simulations, generating RESTRAINT input files,
  running WHAM analysis, or computing free energy profiles and error bars.
---

# PLUMED Umbrella Sampling

Umbrella sampling uses a series of harmonic restraint potentials (windows) to force the system
to sample different regions along a reaction coordinate. The unbiased free energy is then
recovered by combining all windows via WHAM.

Assumes a GROMACS-patched PLUMED installation; see the `gmx-install` skill if needed.
Start from an NPT-equilibrated system; see `gmx-prep` for those stages.

---

## Information to Collect

**Before generating any input files, ask the user:**

1. **Collective variable (CV)**: What reaction coordinate describes the process?
   - Torsion angle? → need atom indices or MOLINFO shortcut
   - Distance (e.g., ligand–receptor)? → need atom groups or COM groups
   - RMSD from a reference state? → need a reference PDB file
   - Custom function of other CVs? → need the FUNC= expression
2. **CV range**: What is the physically meaningful min and max? Is it periodic (angles: yes; distances: no)?
3. **Number of windows and spacing**: How many windows N? Spacing = (max−min)/N. Use `endpoint=False` for periodic CVs to avoid duplicate boundary window.
4. **Spring constant KAPPA**: How stiff should the restraint be? (default 200 kJ/mol/rad² for angles; 1000 kJ/mol/nm² for distances). Histogram overlap between adjacent windows must be verified.
5. **Reference PDB**: Is a MOLINFO structure needed (required for MOLINFO shortcuts; also for RMSD CVs)?
6. **TPR file(s)**: One starting structure or two (to check initial-condition dependence)?
7. **Simulation length per window** (nsteps) and output stride (STRIDE in PLUMED).
8. **Run mode**: Serial (one `gmx mdrun` per window) or MPI/REMD (`gmx_mpi mdrun -multidir` with `@replicas:`)?
9. **PBC**: Can the CV atom groups wrap across periodic boundaries? (If yes, need `WHOLEMOLECULES` or `NOPBC` options.)

---

## Parameter Defaults and Guidance

| CV type | KAPPA (kJ/mol/unit²) | Periodicity | BANDWIDTH |
|---------|---------------------|-------------|-----------|
| Torsion (rad) | 200 | yes, [-π, π] | 0.05 rad |
| Distance (nm) | 1000 | no, [0, ∞) | 0.01 nm |
| RMSD (nm) | 2000 | no, [0, ∞) | 0.01 nm |
| End-to-end distance (nm) | 500 | no | 0.02 nm |

Histogram overlap check: adjacent windows should overlap by ≥ 20% of their width.
If not, reduce spacing or increase KAPPA.

---

## Stage 1: Unbiased run + CV calibration

Use the `plumed_unbiased.dat` template to monitor the chosen CV without applying any bias.

```bash
gmx mdrun -plumed plumed_unbiased.dat -s topol.tpr -nsteps 200000 -x traj_unbiased.xtc
```

**Analysis:**
```python
import plumed, numpy as np, matplotlib.pyplot as plt

colvar = plumed.read_as_pandas("colvar.dat")
cv1 = colvar["cv1"]

plt.plot(colvar.time, cv1)
plt.xlabel("Time (ps)"); plt.ylabel("CV")
plt.show()

print(f"CV range visited: [{cv1.min():.3f}, {cv1.max():.3f}]")
print(f"CV std-dev (sigma estimate for METAD): {cv1.std():.3f}")
```

Use the std-dev to set SIGMA if you later run metadynamics on this CV (see `plumed-metad`).
Use the histogram to set GRID_MIN/MAX and choose window spacing.

**Verify:** `colvar.dat` exists and has data; CV time series shows the system is not stuck.

---

## Stage 2: Generate window input files

```python
import numpy as np

# Window centers — endpoint=False for periodic CVs to avoid duplicate boundary window
at = np.linspace(CV_MIN, CV_MAX, N_WINDOWS, endpoint=IS_PERIODIC_FALSE_OR_TRUE)
print(at)

# Generate one input file per window
for i, center in enumerate(at):
    with open(f"plumed_{i}.dat", "w") as f:
        f.write(f"""# vim:ft=plumed
MOLINFO STRUCTURE=REFERENCE_PDB

cv1: CV1_DEFINITION
secondary: SECONDARY_CV_DEFINITION

bb: RESTRAINT ARG=cv1 KAPPA={KAPPA} AT={center:.6f}
PRINT ARG=cv1,secondary,bb.bias FILE=colvar_{i}.dat STRIDE={STRIDE}
""")
```

Alternatively use the `plumed_us_multi.dat` template with `@replicas:` syntax and paste the
comma-separated window center list directly.

**Verify:** N files `plumed_0.dat` through `plumed_{N-1}.dat` exist with correct AT= values.

---

## Stage 3: Run windows

### Serial (one directory per window)
```bash
for i in $(seq 0 $((N_WINDOWS-1))); do
    mkdir -p window_${i}
    cd window_${i}
    gmx mdrun -plumed ../plumed_${i}.dat -s ../topol.tpr -nsteps NSTEPS \
              -x traj_${i}.xtc -deffnm window_${i}
    cd ..
done
```

### MPI/REMD (all windows simultaneously, with replica exchange)
```bash
# Create one directory per replica
for i in $(seq 0 $((N_WINDOWS-1))); do mkdir -p rep_${i}; done

# Copy or symlink the TPR file into each directory
for i in $(seq 0 $((N_WINDOWS-1))); do ln -sf ../topol.tpr rep_${i}/topol.tpr; done

# Run with replica exchange
mpiexec -np N_WINDOWS gmx_mpi mdrun \
    -multidir rep_? rep_?? \
    -plumed ../plumed_us_multi.dat \
    -nsteps NSTEPS \
    -replex 200
```

**Verify:**
```bash
ls rep_*/colvar_multi*.dat   # or colvar_0.dat ... colvar_{N-1}.dat for serial
# Check that each colvar file has data and that PRINT output covers expected time range
```

---

## Stage 4: Concatenate trajectories and compute WHAM weights

```bash
# Concatenate all window trajectories (serial mode)
gmx trjcat -cat -f window_*/traj_*.xtc -o cat.xtc

# Re-run plumed driver on the concatenated trajectory for each window
# to reproduce the bias value that window i would have felt at every frame
for i in $(seq 0 $((N_WINDOWS-1))); do
    plumed driver --plumed plumed_${i}.dat --ixtc cat.xtc --trajectory-stride STRIDE
    mv colvar_${i}.dat colvar_cat_${i}.dat
done
```

```python
import numpy as np, plumed
import sys; sys.path.insert(0, "${CLAUDE_SKILL_DIR}/templates/")
import wham

kBT = TEMPERATURE * 8.314462618e-3  # kJ/mol

# Read bias values from each window's driver output
col = [plumed.read_as_pandas(f"colvar_cat_{i}.dat") for i in range(N_WINDOWS)]
n_frames = len(col[0]["bb.bias"])
bias = np.zeros((n_frames, N_WINDOWS))
for i in range(N_WINDOWS):
    bias[:, i] = col[i]["bb.bias"][-n_frames:]

# Run binless WHAM
w = wham.wham(bias, T=kBT)

# Attach log-weights to the first colvar dataframe and write for downstream analysis
col[0]["logweights"] = w["logW"]
plumed.write_pandas(col[0], "bias_wham.dat")
print("WHAM converged in", w["nit"], "iterations, eps =", w["eps"])
```

**Verify:** `bias_wham.dat` written; logweights show expected trend (frames from over-sampled regions get negative logweights).

---

## Stage 5: Compute reweighted free energy

```python
# Read WHAM weights and project FES onto any CV
import plumed, numpy as np, matplotlib.pyplot as plt

data = plumed.read_as_pandas("bias_wham.dat")

# Option A: use PLUMED driver for the final FES computation (reads logweights as LOGWEIGHTS=)
# Option B: compute directly in Python

cv1 = np.array(data["cv1"])
logW = np.array(data["logweights"])
W = np.exp(logW - logW.max())   # normalized weights

# 1D FES via weighted histogram
bins = np.linspace(CV1_MIN, CV1_MAX, N_BINS + 1)
hist, edges = np.histogram(cv1, bins=bins, weights=W, density=True)
centers = 0.5 * (edges[:-1] + edges[1:])
fes = -kBT * np.log(hist + 1e-300)
fes -= fes.min()

plt.plot(centers, fes)
plt.xlabel("CV"); plt.ylabel("F (kJ/mol)")
plt.show()
```

---

## Stage 6: Population and error analysis (bootstrap)

```python
NB = 10       # number of blocks per trajectory
N_BOOT = 200  # bootstrap iterations

# Reshape bias array: (N_WINDOWS, NB, frames_per_block, N_WINDOWS)
frames_per_traj = n_frames // N_WINDOWS
bb = bias.reshape((N_WINDOWS, -1, N_WINDOWS))[:, -frames_per_traj:, :]
bb = bb.reshape((N_WINDOWS, NB, frames_per_traj // NB, N_WINDOWS))
cc = np.array(col[0]["cv1"]).reshape((N_WINDOWS, -1))[:, -frames_per_traj:]
cc = cc.reshape((N_WINDOWS, NB, frames_per_traj // NB))

# Full-trajectory population estimate
w0 = wham.wham(bb.reshape((-1, N_WINDOWS)), T=kBT)
tr = cc.flatten()
# Define state based on CV range — ask user for boundaries
in_state_B = np.logical_and(tr > STATE_B_MIN, tr < STATE_B_MAX)
pop = np.average(in_state_B, weights=np.exp(w0["logW"]))
print(f"Population of state B: {pop:.4f}")

# Bootstrap error
pop_boot = []
for _ in range(N_BOOT):
    c = np.random.choice(NB, NB)
    w = wham.wham(bb[:, c, :, :].reshape((-1, N_WINDOWS)), T=kBT)
    tr_b = cc[:, c, :].flatten()
    in_B = np.logical_and(tr_b > STATE_B_MIN, tr_b < STATE_B_MAX)
    pop_boot.append(np.average(in_B, weights=np.exp(w["logW"])))

print(f"Bootstrap std-dev: {np.std(pop_boot):.4f}")
```

**Note:** For periodic CVs (angles), compute circular means using `np.arctan2(np.mean(np.sin(cv)), np.mean(np.cos(cv)))` rather than arithmetic means.

---

## Stage 7: Initial-condition check

Repeat Stages 3–6 with a different starting configuration. If the reweighted FES differs from the first run by more than the bootstrap error, sampling is insufficient — either use longer windows or switch to REMD-US (`plumed-remd`).

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Adjacent window histograms don't overlap | Windows too sparse or KAPPA too small | Reduce spacing or increase KAPPA |
| WHAM does not converge (eps stays large) | Bias matrix is ill-conditioned | Check all colvar files have data; verify bias values are finite |
| Periodic CV wraps incorrectly | AT= value near periodic boundary | Use `endpoint=False` in linspace; inspect colvar plots for jumps |
| `plumed driver` misses frames | `--trajectory-stride` mismatch | Match stride to STRIDE= in plumed.dat |
| RMSD CV drifts to large values | Molecule wraps across PBC | Add `WHOLEMOLECULES ENTITY0=ATOM_RANGE` before RMSD action |
| colvar file has only a few frames | Simulation crashed early | Check GROMACS log; verify TPR is compatible with the plumed.dat CV |

---

## Working Examples (alanine dipeptide)

The `${CLAUDE_SKILL_DIR}/templates/examples/` directory contains working PLUMED input files from PLUMED Masterclass 21.3,
using alanine dipeptide in vacuum with phi torsion as the reaction coordinate.
Use these as a reference for syntax; adapt CV definitions for your own system.

- `plumed_ex1.dat` — Unbiased run, CV histograms and FES
- `plumed_ex2.dat` — CUSTOM bias + reweighting with REWEIGHT_BIAS
- `plumed_ex3.dat` — Multi-bias WHAM combination (three simulations)
- `plumed_ex4.dat` — READ + HISTOGRAM from WHAM logweights
- `plumed_ex5.dat` — 32-window RESTRAINT umbrella sampling

Run example (requires `data/topolA.tpr` and `data/reference.pdb`):
```bash
gmx mdrun -plumed ${CLAUDE_SKILL_DIR}/templates/examples/plumed_ex1.dat -s data/topolA.tpr -nsteps 200000
```

---

## Credits

This skill is inspired by and based on:

**PLUMED Masterclass 21.3 — Umbrella Sampling**
Author: Giovanni Bussi (SISSA, Trieste), 2021
https://github.com/plumed/masterclass-21-3

The `wham.py` script and the example files in `templates/examples/` are taken directly
from that masterclass. All credit for those files belongs to Giovanni Bussi.
The generic workflow, templates, and SKILL.md text are original additions built on top
of the masterclass material.

PLUMED is developed by the PLUMED consortium: https://www.plumed.org

---

## See Also

- `gmx-prep` — System preparation: EM → NVT → NPT
- `plumed-metad` — Adaptive biasing (no windows needed)
- `plumed-remd` — Replica exchange to enhance convergence across windows
