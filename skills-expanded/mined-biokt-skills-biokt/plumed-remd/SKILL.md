---
name: plumed-remd
description: Multiple replica simulations with PLUMED. Use when setting up umbrella
  sampling with replica exchange, bias-exchange metadynamics, or parallel-tempering
  metadynamics, and for demuxing trajectories and WHAM analysis.
---

# PLUMED Multiple Replica Simulations

Replica exchange methods run several copies of the system simultaneously and allow them to
exchange configurations (or Hamiltonians) at regular intervals. This reduces dependence on
initial conditions and can overcome barriers that single replicas cannot cross on the
available timescale.

Requires MPI-enabled GROMACS (`gmx_mpi`); see `gmx-install` skill if needed.
MacOS OpenMPI workaround: `export OMPI_MCA_btl=self,tcp` before mpiexec.

---

## Method Selection Guide

| Use case | Method | PLUMED key feature | GROMACS key |
|----------|--------|--------------------|-------------|
| Many US windows; improve convergence | US-REMD | `RESTRAINT` + `@replicas:` | `-multidir -replex` |
| Uncertain which CV biases best | Bias-exchange METAD | `METAD @replicas:` + `RANDOM_EXCHANGES` | `-replex` |
| Large barrier; no good CV | Parallel-tempering + METAD | `METAD` per temperature | `-multidir -replex` |
| Run same simulation from different starts | Independent replicas | separate plumed.dat per run | no `-replex` |

---

## Information to Collect

**Before generating any input files, ask the user:**

1. **Method type**: US-REMD, bias-exchange METAD, PT-METAD, or independent replicas?
2. **CV and reaction coordinate** (as in `plumed-us` or `plumed-metad` — same questions apply)
3. **Number of replicas** (US-REMD: typically 8–32; bias-exchange: 2–6; PT-METAD: 4–8)
4. **Exchange frequency**: `-replex N` in GROMACS steps (default 200; exchange attempt every 200 steps)
5. **Starting structures**: single structure or multiple (one per replica) for initial-condition checks
6. **MPI launcher**: `mpiexec` or `mpirun`? Number of CPUs/GPUs available?
7. **For PT-METAD**: temperature range (T_min, T_max); temperature ladder: geometric spacing `np.geomspace(T_min, T_max, N)`
8. **For bias-exchange METAD**: which CV goes to which replica? Should one replica be unbiased (HEIGHT=0)?
9. **PBC handling**: same as `plumed-us` / `plumed-metad`

---

## Stage 1: Prepare directory structure

```bash
N=N_REPLICAS

# Create one directory per replica
for i in $(seq 0 $((N-1))); do mkdir -p rep_${i}; done

# Link or copy the TPR file into each directory
# For US-REMD: same TPR for all replicas (or different starting structures)
for i in $(seq 0 $((N-1))); do
    ln -sf $(pwd)/topol.tpr rep_${i}/topol.tpr
done

# For PT-METAD: one TPR per temperature (generate separately with grompp)
```

---

## Stage 2: Generate PLUMED input

### US-REMD
Use `plumed_us_remd.dat` with `@replicas:` listing all window centers.

```python
import numpy as np

at = np.linspace(CV_MIN, CV_MAX, N_REPLICAS, endpoint=IS_PERIODIC_FALSE)
at_str = ",".join(f"{v:.6f}" for v in at)
print(f"AT=@replicas:{at_str}")
```

Paste the output into `plumed_us_remd.dat` → `AT=@replicas:...`.

### Bias-exchange METAD
Use `plumed_bem.dat`. Define all CVs; assign one per replica via `@replicas:`.
Set `HEIGHT=@replicas:H0,H1,...` with `0.0` for any unbiased replica.

### PT-METAD
```python
import numpy as np

T = np.geomspace(T_MIN, T_MAX, N_REPLICAS)   # geometric temperature ladder
for i, temp in enumerate(T):
    H = 1.2 * (temp / T[0])   # scale HEIGHT with temperature
    print(f"Replica {i}: T={temp:.1f} K, HEIGHT={H:.3f} kJ/mol")
```

Write one `plumed_{i}.dat` per temperature using the `plumed_pt_metad.dat` template.

---

## Stage 3: Run with MPI

### US-REMD or PT-METAD (shared or per-replica plumed.dat)
```bash
mpiexec -np N_REPLICAS gmx_mpi mdrun \
    -multidir rep_0 rep_1 rep_2 ... \
    -plumed ../plumed_us_remd.dat \
    -nsteps NSTEPS \
    -replex 200
```

### Bias-exchange METAD (random pairs, all replicas see same plumed.dat)
```bash
mpiexec -np N_REPLICAS gmx_mpi mdrun \
    -multidir rep_0 rep_1 rep_2 ... \
    -plumed ../plumed_bem.dat \
    -nsteps NSTEPS \
    -replex 200
```

**Verify:**
```bash
# Colvar files should exist in each directory
ls rep_*/COLVAR
# Exchange log
grep "Replica" rep_0/md.log | tail -20
```

---

## Stage 4: WHAM analysis (without exchange / before demuxing)

```python
import numpy as np, plumed
import sys; sys.path.insert(0, "${CLAUDE_SKILL_DIR}/templates/")
import wham

kBT = TEMPERATURE * 8.314462618e-3  # kJ/mol

# Read colvar files from all replicas
col = [plumed.read_as_pandas(f"rep_{i}/colvar_multi.{i}.dat")
       for i in range(N_REPLICAS)]

# Build bias matrix
n_frames = min(len(c["bb.bias"]) for c in col)
bias = np.zeros((n_frames, N_REPLICAS))
for i in range(N_REPLICAS):
    bias[:, i] = col[i]["bb.bias"][-n_frames:]

w = wham.wham(bias, T=kBT)

# Compute population ratio of interest
cv1 = np.array(col[0]["cv1"])[-n_frames:]
in_state_B = np.logical_and(cv1 > STATE_B_MIN, cv1 < STATE_B_MAX)
in_state_A = cv1 < STATE_A_MAX

pop_ratio = (np.average(in_state_B, weights=np.exp(w["logW"])) /
             np.average(in_state_A, weights=np.exp(w["logW"])))
print(f"Population B / Population A = {pop_ratio:.4f}")
```

---

## Stage 5: Demuxing (trajectories with exchange)

After a run with `-replex`, each directory contains a replica trajectory (fixed Hamiltonian),
not a continuous physical trajectory. Demuxing reconnects frames into continuous paths.

```bash
# demux.pl is provided with GROMACS (in share/tools/ or Scripts/)
demux.pl rep_0/md.log

# This produces:
#   replica_temp.xvg   — which temperature each replica visited vs time
#   replica_index.xvg  — which replica index each frame came from

# Demultiplex all trajectories into continuous paths
gmx_mpi trjcat -demux replica_index.xvg -f rep_0/traj.xtc rep_1/traj.xtc ... -o demux.xtc
```

**Verify:** In `replica_temp.xvg`, replicas should diffuse across the replica index space.
If any replica stays stuck, exchange rate is too low (increase `-replex` frequency or reduce spacing).

---

## Stage 6: WHAM with trajectory weights (demuxed)

After demuxing, each replica may have spent unequal time at each window. Account for this
with the `traj_weight` parameter in WHAM.

```python
import numpy as np, plumed
import sys; sys.path.insert(0, "${CLAUDE_SKILL_DIR}/templates/")
import wham

kBT = TEMPERATURE * 8.314462618e-3

# Read demuxed colvar files
col = [plumed.read_as_pandas(f"colvar_process.{i}.dat") for i in range(N_REPLICAS)]

n_frames = min(len(c["bb.bias"]) for c in col)
bias = np.zeros((n_frames, N_REPLICAS))
for i in range(N_REPLICAS):
    bias[:, i] = col[i]["bb.bias"][-n_frames:]

# traj_weight: fraction of time each replica spent at each window
# Simplest estimate: count frames with bias closest to each window's minimum
traj_weight = np.ones(N_REPLICAS)  # uniform as starting point; refine if needed

w = wham.wham(bias, T=kBT, traj_weight=traj_weight)

# Bootstrap by resampling demuxed trajectories as blocks (one block per replica path)
NB = N_REPLICAS
N_BOOT = 200
pop_boot = []
for _ in range(N_BOOT):
    c = np.random.choice(NB, NB)
    bb_b = bias[np.concatenate([np.arange(c_i * (n_frames // NB),
                                           (c_i + 1) * (n_frames // NB))
                                for c_i in c])]
    w_b = wham.wham(bb_b, T=kBT, traj_weight=traj_weight)
    # ... compute statistic of interest
print(f"Bootstrap std-dev: {np.std(pop_boot):.4f}")
```

---

## Stage 7: PT-METAD reweighting (parallel-tempering with metadynamics)

At the target temperature T₀, both the temperature factor and the METAD bias must be removed.

```python
# For the replica at T0, reweight using REWEIGHT_BIAS (see plumed-metad Stage 4)
# Run plumed driver on the T=T0 replica trajectory:
#   plumed driver --plumed plumed_reweight.dat --ixtc rep_0/traj.xtc

# The METAD bias must be the same one that replica 0 used during the run (RESTART=YES)
# without additional bias from replica exchange at other temperatures.
```

**Important:** For PT-METAD, if the bias is deposited at all temperatures, each replica's HILLS
file must be used independently for reweighting at that temperature. Do NOT mix HILLS files.

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| No exchange attempts observed | `-replex` not passed or too infrequent | Add `-replex 200`; check md.log for "Replica exchange" lines |
| Exchange rate 0% | Window spacing too large or temperature gap too wide | Reduce spacing or temperature range |
| `mpiexec: cannot connect to PMI` | OpenMPI transport issue on MacOS | `export OMPI_MCA_btl=self,tcp` |
| `gmx_mpi` not found | GROMACS compiled without MPI | Rebuild with MPI; see `gmx-install` |
| Demux produces identical trajectories | Run done without `-replex` | Re-run with `-replex N` |
| PT-METAD gives wrong populations | Missing reweighting of metad bias | Apply `REWEIGHT_BIAS` at T₀; do not rely on temperature reweighting alone |
| `@replicas:` list length mismatch | List has wrong number of entries | Count must equal number of MPI ranks (`-np N`) |

---

## Working Examples (alanine dipeptide)

The `${CLAUDE_SKILL_DIR}/templates/examples/` directory contains working PLUMED input files from PLUMED Masterclass 21.5,
using alanine dipeptide in vacuum. Use these as reference for syntax; adapt for your system.

- `plumed_ex1.dat` — US-REMD: 32-window RESTRAINT with `@replicas:` syntax
- `plumed_ex2.dat` — Bias-exchange METAD: 3 replicas, `RANDOM_EXCHANGES`
- `plumed_ex3.dat` — PT-METAD: single-replica template with METAD on a secondary CV

Run example (requires `topolA.tpr`, `reference.pdb`; 32 MPI ranks):
```bash
mkdir -p $(seq -f "rep_%g" 0 31)
mpiexec -np 32 gmx_mpi mdrun \
    -multidir $(seq -f "rep_%g" 0 31) \
    -plumed ${CLAUDE_SKILL_DIR}/templates/examples/plumed_ex1.dat \
    -nsteps 200000 -replex 200
```

---

## Credits

This skill is inspired by and based on:

**PLUMED Masterclass 21.5 — Multiple Replicas**
Author: Giovanni Bussi (SISSA, Trieste), 2021
https://github.com/plumed/masterclass-21-5

The `wham.py` script (originally from Masterclass 21.3, same author) and the example files
in `templates/examples/` are taken directly from that masterclass. All credit for those files
belongs to Giovanni Bussi.

This skill also draws on material from:

**PLUMED Masterclass 21.3 — Umbrella Sampling**
Author: Giovanni Bussi (SISSA, Trieste), 2021
https://github.com/plumed/masterclass-21-3

The generic workflow, templates, and SKILL.md text are original additions built on top
of the masterclass material.

PLUMED is developed by the PLUMED consortium: https://www.plumed.org

---

## See Also

- `gmx-prep` — System preparation: EM → NVT → NPT; also covers H-REMD mdp setup
- `plumed-us` — Single-replica umbrella sampling (no MPI needed)
- `plumed-metad` — Single-replica metadynamics (no MPI needed)
