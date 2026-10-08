---
name: slurm-submit
description: 'SLURM job submission for SLU-Libra cluster. Use when submitting heavy compute jobs (>1GB data, >5 min runtime, >100K obs regressions) on the cluster. Generates sbatch wrappers for CPU/GPU jobs with correct partition, QoS, and resource allocation.'
argument-hint: 'Script name and resource requirements (e.g., C5_1a_build_sample.py, CPU, 8G RAM, 2 hours)'
---

# SLURM Job Submission (SLU-Libra)

## When to Use
- ON_CLUSTER = True (detected via `os.environ.get("SLURM_CLUSTER_NAME")` or hostname)
- Task is compute-heavy: >1GB data, >5 min runtime, or >100K obs regressions
- About to run a Python script

**NEVER run heavy jobs directly on the cluster login node.**

## Step-by-Step

### 1. Write Python Script
Save to `scripts/` as normal.

### 2. Generate sbatch Wrapper
Create companion `.sh` in `jobs/slurm/`:

#### CPU Job (data processing, regressions)
```bash
#!/bin/bash
#SBATCH --job-name={script_name_without_ext}
#SBATCH --partition=compute
#SBATCH --qos=normal
#SBATCH --account=<PROJECT>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=jobs/slurm/logs/%x_%j.out
#SBATCH --error=jobs/slurm/logs/%x_%j.err

module purge
module load python
source .venv/bin/activate
cd "$SLURM_SUBMIT_DIR"
python scripts/{script_name}.py
```

#### GPU Job (L40S)
```bash
#!/bin/bash
#SBATCH --job-name={script_name_without_ext}
#SBATCH --partition=gpu
#SBATCH --qos=normal
#SBATCH --account=<PROJECT>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=16G
#SBATCH --gpus-per-node=L40S:1
#SBATCH --time=04:00:00
#SBATCH --output=jobs/slurm/logs/%x_%j.out
#SBATCH --error=jobs/slurm/logs/%x_%j.err

module purge
module load python cuda
source .venv/bin/activate
cd "$SLURM_SUBMIT_DIR"
python scripts/{script_name}.py
```

#### GPU Job (H100 NVL)
```bash
#!/bin/bash
#SBATCH --job-name={script_name_without_ext}
#SBATCH --partition=machinelearning
#SBATCH --qos=normal
#SBATCH --account=<PROJECT>
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32G
#SBATCH --gpus-per-node=gres/gpu:1
#SBATCH --time=04:00:00
#SBATCH --output=jobs/slurm/logs/%x_%j.out
#SBATCH --error=jobs/slurm/logs/%x_%j.err

module purge
module load python cuda
source .venv/bin/activate
cd "$SLURM_SUBMIT_DIR"
python scripts/{script_name}.py
```

### 3. Create Log Directory
```bash
mkdir -p jobs/slurm/logs
```

### 4. Submit
```bash
sbatch jobs/slurm/{wrapper_name}.sh
```

### 5. Monitor
```bash
squeue -u $USER
sacct -j <JOB_ID> --format=JobID,State,Elapsed,MaxRSS
```

## Parameter Tuning

| Workload | Partition | CPUs | Mem | Time | GPU |
|----------|-----------|------|-----|------|-----|
| DuckDB/pandas merge | compute | 4-8 | 8-32G | 02:00:00 | — |
| Large panel (>10GB) | compute | 8-16 | 32-64G | 04-08:00:00 | — |
| Regressions (OLS/FE) | compute | 4 | 8G | 01:00:00 | — |
| Bootstrap/permutation | compute | 8-16 | 16G | 04:00:00 | — |
| API extraction | compute | 2-4 | 8G | 04-12:00:00 | — |
| ML training | gpu | 6 | 16G | 04:00:00 | L40S:1 |
| Large model | machinelearning | 12 | 32G | 08:00:00 | gres/gpu:1 |

## Required sbatch Options (SLU-Libra)
Mandatory: `--nodes`, `--time`, `--qos`, `--partition`, `--account`

## File Organization
```
jobs/slurm/
  C5_1a_build_sample.sh
  logs/
    C5_1a_build_sample_864933.out
    C5_1a_build_sample_864933.err
```