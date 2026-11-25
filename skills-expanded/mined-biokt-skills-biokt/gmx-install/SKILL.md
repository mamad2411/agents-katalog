---
name: gmx-install
description: GROMACS source build with PLUMED, GPU (CUDA), and MPI support. Use when
  installing or reinstalling GROMACS from source, patching with PLUMED, configuring
  cmake flags for GPU/MPI, or running GROMACS benchmark tests to validate an installation.
---

# GROMACS + PLUMED Source Installation

## Arguments

Parse the user's request for these flags (all default ON except `test`):

| Argument | Default | Effect |
|---|---|---|
| `plumed` | **on** | Build PLUMED from source and patch GROMACS |
| `mpi` | **on** | Enable MPI (`gmx_mpi` binary) |
| `gpu` | **on** | Enable CUDA GPU offload |
| `test` | **off** | Download and run GROMACS benchmark systems |

**If the user requests only `test`** (no install), skip directly to [Step 6 — Benchmark Tests](#step-6--benchmark-tests-only-if-teston). Detect this when the request contains only "test", "benchmark", or "run benchmarks" with no mention of installing or building. In that case, first run `gmx --version` to confirm GROMACS is available and whether `gmx_mpi` exists, then proceed with Step 6 only.

Examples:
- "install GROMACS with PLUMED" → plumed=on, mpi=on, gpu=on, test=off
- "install without MPI" → plumed=on, mpi=off, gpu=on, test=off
- "install and test" → plumed=on, mpi=on, gpu=on, test=on
- "plain GROMACS install" → plumed=off, mpi=off, gpu=on, test=off
- "test the installation" → skip to Step 6 only
- "run GROMACS benchmarks" → skip to Step 6 only

---

## Versions (update when user specifies different versions)

| Software | Default version |
|---|---|
| GROMACS | 2024.2 |
| PLUMED | 2.9.2 |

---

## Prerequisites

Verify these are available before starting:

```bash
# Compilers
gcc --version          # need gcc >= 9
cmake --version        # need cmake >= 3.18
# MPI (if mpi=on)
mpicc --version        # OpenMPI or MPICH
# CUDA (if gpu=on)
nvcc --version         # CUDA toolkit >= 11.4
nvidia-smi             # confirm GPU is visible
# Build tools
make --version
```

For Ubuntu/Debian:
```bash
sudo apt install build-essential cmake libfftw3-dev \
    libopenmpi-dev openmpi-bin \
    python3 python3-dev zlib1g-dev
```

For conda environments:
```bash
conda install -c conda-forge cmake openmpi fftw
```

---

## Step 1 — Set Install Paths

```bash
# Adjust these to your system
GMX_VERSION=2024.2
PLUMED_VERSION=2.9.2

# Install roots — change to preferred location
INSTALL_ROOT=$HOME/opt
PLUMED_ROOT=${INSTALL_ROOT}/plumed-${PLUMED_VERSION}
GMX_ROOT=${INSTALL_ROOT}/gromacs-${GMX_VERSION}

# Source directories
BUILD_DIR=$HOME/build
mkdir -p ${BUILD_DIR}
```

---

## Step 2 — Build PLUMED (skip if plumed=off)

```bash
cd ${BUILD_DIR}

# Download
wget https://github.com/plumed/plumed2/releases/download/v${PLUMED_VERSION}/plumed-${PLUMED_VERSION}.tgz
tar xf plumed-${PLUMED_VERSION}.tgz
cd plumed-${PLUMED_VERSION}

# Configure — with MPI if mpi=on
# With MPI:
./configure --prefix=${PLUMED_ROOT} --enable-mpi CXX=mpicxx CC=mpicc
# Without MPI:
# ./configure --prefix=${PLUMED_ROOT}

make -j$(nproc)
make install

# Add to environment (also add to ~/.bashrc or module)
export PATH=${PLUMED_ROOT}/bin:$PATH
export LD_LIBRARY_PATH=${PLUMED_ROOT}/lib:$LD_LIBRARY_PATH
export PLUMED_KERNEL=${PLUMED_ROOT}/lib/libplumedKernel.so

# Verify
plumed --version
```

**Optional Python interface** (for postprocessing with plumed.read_as_pandas etc.):
```bash
cd ${BUILD_DIR}/plumed-${PLUMED_VERSION}
pip install --user .
```

---

## Step 3 — Download and Patch GROMACS

```bash
cd ${BUILD_DIR}

# Download GROMACS source
wget https://ftp.gromacs.org/gromacs/gromacs-${GMX_VERSION}.tar.gz
tar xf gromacs-${GMX_VERSION}.tar.gz
cd gromacs-${GMX_VERSION}

# Patch with PLUMED (skip if plumed=off)
plumed patch -p -e gromacs-${GMX_VERSION}
# When prompted, confirm the patch. Use --runtime for runtime-linking (recommended):
# plumed patch -p --runtime -e gromacs-${GMX_VERSION}
```

> **`--runtime` vs static patch:** `--runtime` links `libplumedKernel.so` at run time via `$PLUMED_KERNEL` — lets you update PLUMED without recompiling GROMACS. Omit `--runtime` for a statically linked build (simpler, less flexible).

---

## Step 4 — CMake Configuration

```bash
cd ${BUILD_DIR}/gromacs-${GMX_VERSION}
mkdir build && cd build
```

### Full build (GPU + MPI + PLUMED)

```bash
cmake .. \
    -DCMAKE_INSTALL_PREFIX=${GMX_ROOT} \
    -DCMAKE_BUILD_TYPE=Release \
    -DGMX_GPU=CUDA \
    -DGMX_MPI=ON \
    -DGMX_OPENMP=ON \
    -DGMX_DOUBLE=OFF \
    -DGMX_BUILD_OWN_FFTW=ON \
    -DGMX_SIMD=AUTO \
    -DGMX_PLUMED=ON \
    -DPLUMED_ROOT=${PLUMED_ROOT} \
    -DREGRESSIONTEST_DOWNLOAD=OFF \
    2>&1 | tee cmake_config.log
```

### GPU + MPI, no PLUMED (`-DGMX_PLUMED=OFF`, remove `-DPLUMED_ROOT`)

```bash
cmake .. \
    -DCMAKE_INSTALL_PREFIX=${GMX_ROOT} \
    -DCMAKE_BUILD_TYPE=Release \
    -DGMX_GPU=CUDA \
    -DGMX_MPI=ON \
    -DGMX_OPENMP=ON \
    -DGMX_DOUBLE=OFF \
    -DGMX_BUILD_OWN_FFTW=ON \
    -DGMX_SIMD=AUTO \
    2>&1 | tee cmake_config.log
```

### GPU only, no MPI, no PLUMED

```bash
cmake .. \
    -DCMAKE_INSTALL_PREFIX=${GMX_ROOT} \
    -DCMAKE_BUILD_TYPE=Release \
    -DGMX_GPU=CUDA \
    -DGMX_MPI=OFF \
    -DGMX_OPENMP=ON \
    -DGMX_DOUBLE=OFF \
    -DGMX_BUILD_OWN_FFTW=ON \
    -DGMX_SIMD=AUTO \
    2>&1 | tee cmake_config.log
```

### CPU only (no GPU)

Replace `-DGMX_GPU=CUDA` with `-DGMX_GPU=OFF`.

**Verify cmake output:**
```
-- GROMACS version: 2024.2
-- Configured with PLUMED support: yes      ← if plumed=on
-- MPI support: yes                          ← if mpi=on
-- GPU support: CUDA                         ← if gpu=on
-- SIMD level: AVX2_256 (or higher)
```

---

## Step 5 — Build and Install

```bash
make -j$(nproc) 2>&1 | tee make.log
make install

# Source the GMXRC
source ${GMX_ROOT}/bin/GMXRC

# Verify
gmx --version          # serial binary
gmx_mpi --version      # MPI binary (if mpi=on)
```

Add to `~/.bashrc` (or a module file):
```bash
export PLUMED_KERNEL=${PLUMED_ROOT}/lib/libplumedKernel.so   # if runtime patch
source ${GMX_ROOT}/bin/GMXRC
```

> **Sourcing GMXRC under `set -e`:** GMXRC uses unbound variables internally; wrap with `set +u` if your shell uses strict mode:
> ```bash
> set +u; source ${GMX_ROOT}/bin/GMXRC; set -u
> ```

---

## Step 6 — Benchmark Tests (only if test=on)

> **Standalone mode:** If invoked without a build (e.g. "test the installation"), start here. First confirm GROMACS is available:
> ```bash
> gmx --version          # note the version
> gmx_mpi --version 2>/dev/null && echo "MPI binary available" || echo "No gmx_mpi"
> ```
> Use `gmx_mpi mdrun` in the commands below if the MPI binary is present, otherwise use `gmx mdrun`.

GROMACS ships with benchmark TPR files you can download to validate performance.

### Download benchmark systems

```bash
BENCH_DIR=${BUILD_DIR}/gmx-benchmarks
mkdir -p ${BENCH_DIR} && cd ${BENCH_DIR}

# Water benchmark (small, quick)
wget https://ftp.gromacs.org/pub/benchmarks/water_GMX50_bare.tar.gz
tar xf water_GMX50_bare.tar.gz

# ADH benchmark (medium, ~95k atoms)
wget https://ftp.gromacs.org/pub/benchmarks/ADH_bench_systems.tar.gz
tar xf ADH_bench_systems.tar.gz
```

### Run water benchmark (quick validation, ~30 s)

```bash
cd ${BENCH_DIR}/water-cut1.0_GMX50_bare/1536

# GPU + MPI (adjust -ntmpi to number of GPUs)
gmx_mpi mdrun -s topol.tpr -deffnm bench_water \
    -ntmpi 1 -ntomp 8 -pme gpu -bonded gpu -nb gpu -v -nsteps 5000

# GPU only, no MPI
gmx mdrun -s topol.tpr -deffnm bench_water \
    -ntmpi 1 -ntomp 8 -pme gpu -bonded gpu -nb gpu -v -nsteps 5000
```

### Run ADH benchmark (more realistic, ~2 min)

```bash
cd ${BENCH_DIR}/ADH_bench_systems/adh_cubic

gmx_mpi mdrun -s topol.tpr -deffnm bench_adh \
    -ntmpi 1 -ntomp 8 -pme gpu -bonded gpu -nb gpu -v -nsteps 10000
```

### Interpret results

```
Performance:    XXX  ns/day   (higher is better)
               YYY   hours/ns
```

Expected ballpark for a single modern GPU (A100/V100):
- Water 1536: > 500 ns/day
- ADH cubic: > 200 ns/day

If performance is poor, check:
```bash
# Was GPU offload actually used?
grep -E "GPU|CUDA" bench_water.log | head -20

# Check device assignment
gmx mdrun -s topol.tpr -ntmpi 1 -ntomp 8 -gpu_id 0 -v -nsteps 100
```

### Validate PLUMED patch (if plumed=on)

```bash
# Create a minimal plumed.dat
echo "PRINT STRIDE=100 ARG=* FILE=COLVAR" > plumed_test.dat

gmx_mpi mdrun -s topol.tpr -deffnm bench_plumed \
    -plumed plumed_test.dat -ntmpi 1 -ntomp 4 -v -nsteps 1000

# Confirm PLUMED output was written
ls -lh COLVAR
head COLVAR
```

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `plumed patch` fails: version mismatch | PLUMED doesn't know this GMX version | Check `plumed patch -l` for supported versions; use closest available |
| `cmake` can't find CUDA | CUDA not in PATH | `export PATH=/usr/local/cuda/bin:$PATH; export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH` |
| `gmx_mpi` not found after install | MPI disabled or PATH not set | Confirm `-DGMX_MPI=ON`; source GMXRC |
| `libplumedKernel.so: cannot open` | `PLUMED_KERNEL` not exported | `export PLUMED_KERNEL=${PLUMED_ROOT}/lib/libplumedKernel.so` |
| Poor GPU performance | PME still on CPU | Add `-pme gpu -bonded gpu -nb gpu` to mdrun |
| `SIMD: no such instruction` | Wrong SIMD flag | Use `-DGMX_SIMD=AUTO` or set to `SSE4.1` for older CPUs |
| `make: out of memory` with `-j$(nproc)` | Too many parallel jobs | Use `-j4` or `-j8` instead |
| GMXRC `unbound variable` error under `set -e` | GMXRC uses `$VARIABLE:-` syntax | Wrap: `set +u; source GMXRC; set -u` |
| `gmx_mpi` (even `--version`) or any MPI program hangs at 0 CPU; stray `orted --singleton-died-pipe` daemons | hwloc's GL plugin waits on a hung local X server (`strace` shows `poll` on `/tmp/.X11-unix/X*`); not a GROMACS/MPI build problem, so a rebuild won't help | `export HWLOC_COMPONENTS=-gl` (unsetting `DISPLAY` is not enough); kill the daemons with `kill -9` |
| `-bonded gpu` error in water benchmark | Pure water has no bonded terms | Drop `-bonded gpu` for water boxes |
| `-update gpu` error with `-plumed` | PLUMED requires CPU update | Drop `-update gpu` when PLUMED is active |
