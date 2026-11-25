# /anima-data-preflight — Mandatory Data Verification Before Training

**Purpose:** Block training until ALL required datasets are verified on disk. Prevents wasting GPU hours on mock/incomplete data.

**RULE: NO MODULE TRAINS WITHOUT PASSING DATA PREFLIGHT.**

---

## HOW IT WORKS

### Step 0: Check ANIMA module manifest + registry
```bash
MODULE_NAME=$(basename $(pwd) | sed 's/project_//')

# 1. anima_module.yaml exists in module
[ -f "anima_module.yaml" ] && echo "[✅] anima_module.yaml exists" || echo "[❌] anima_module.yaml MISSING — run /add-anima-module"

# 2. Registered in anima-infra-main registry
[ -f "/mnt/forge-data/anima-infra-main/registry/${MODULE_NAME}.yaml" ] && \
  echo "[✅] Registered in anima-infra-main/registry/" || \
  { echo "[❌] NOT in infra registry — copying now"; \
    cp anima_module.yaml "/mnt/forge-data/anima-infra-main/registry/${MODULE_NAME}.yaml"; }

# 3. Docker serving files
[ -f "Dockerfile.serve" ] && echo "[✅] Dockerfile.serve" || echo "[❌] Dockerfile.serve MISSING"
[ -f "docker-compose.serve.yml" ] && echo "[✅] docker-compose.serve.yml" || echo "[❌] docker-compose.serve.yml MISSING"
[ -f "serve.py" ] || [ -f "src/*/serve.py" ] && echo "[✅] serve.py" || echo "[❌] serve.py MISSING"
```

If any of the above are missing, fix them BEFORE proceeding to data checks.

### Step 1: Read the paper's data requirements
From the module's CLAUDE.md, ASSETS.md, PRD.md — extract:
- Every dataset the paper uses (Section "Experiments" / "Data")
- Pretrained weights / backbone models needed
- Expected sample counts per split (train/val/test)

### Step 2: Check what's on disk
For each required dataset, verify:
```bash
# 1. Path exists
ls -la "$DATASET_PATH"

# 2. Non-zero size
du -sh "$DATASET_PATH"

# 3. Sample count matches expectation
find "$DATASET_PATH" -name "*.png" -o -name "*.jpg" -o -name "*.npy" | wc -l

# 4. Can actually load a sample
python3 -c "
from PIL import Image
img = Image.open('$DATASET_PATH/first_file')
print(f'Loaded: {img.size}')
"
```

### Step 3: Check pretrained weights
```bash
# Verify weights load without error
python3 -c "
import torch
ckpt = torch.load('$WEIGHTS_PATH', map_location='cpu', weights_only=True)
print(f'Keys: {len(ckpt.keys()) if isinstance(ckpt, dict) else type(ckpt)}')
"
```

### Step 4: Generate report
```
╔══════════════════════════════════════════════════════════════╗
║  DATA PREFLIGHT — {MODULE_NAME}                              ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [✅] Dataset A — 50,000 samples at /mnt/forge-data/...      ║
║  [✅] Dataset B — 10,000 samples at /mnt/forge-data/...      ║
║  [❌] Dataset C — MISSING (paper needs 25,000 samples)       ║
║  [✅] Pretrained weights — loaded successfully               ║
║  [⚠️] Dataset D — 8,000/10,000 (80% complete)                ║
║                                                              ║
║  VERDICT: ❌ BLOCKED — Dataset C missing                      ║
║  Action: Download from https://...                           ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 5: Block or approve
- **ALL GREEN** → Print "PREFLIGHT PASSED — clear to train"
- **ANY RED** → Print "PREFLIGHT FAILED — DO NOT TRAIN" + what's missing + download instructions
- **YELLOW (>80%)** → Print "PREFLIGHT WARNING — partial data, training will work but results won't match paper"

---

## MASTER DATA REGISTRY

The master list of ALL module data requirements lives at:
```
/mnt/forge-data/datasets/DATA_REGISTRY.md
```

This file maps every module → every dataset → path on disk → status.
Updated by `/anima-data-preflight` after each run.

Check it BEFORE starting any new module.

---

## USAGE

### Before training any module:
```bash
cd /mnt/forge-data/modules/project_{module}
# Run preflight
/anima-data-preflight
```

### Check all modules at once:
```bash
/anima-data-preflight --all
```

### Check specific module:
```bash
/anima-data-preflight --module surt
```

---

## INTEGRATION WITH TRAINING

Add this to the beginning of EVERY training prompt:

```
MANDATORY: Run /anima-data-preflight before training.
If preflight FAILS → DO NOT TRAIN. Report what's missing.
If preflight WARNS → ask user before proceeding.
Only train after preflight PASSES.
```

---

## DATA LOCATIONS ON SERVER

### Primary data storage:
```
/mnt/forge-data/datasets/     — Main datasets (2.5TB disk)
/mnt/forge-data/models/       — Pretrained weights
/mnt/titan-healthcare/         — Overflow (nuScenes, kubric, healthcare, defense)
/mnt/artifacts-datai/datasets/ — Generated datasets (SOL thermal, etc.)
```

### Common datasets shared across modules:
| Dataset | Path | Size | Used by |
|---------|------|------|---------|
| COCO 2017 | /mnt/forge-data/datasets/grounding_data/coco/ | 148GB | AZOTH, LOKI, SAGA, BESTLA, ELYSIUM |
| Occ3D/nuScenes | /mnt/forge-data/datasets/occ3d_nuscenes/ | 40GB | SURT, MAGNI, FORSETI |
| nuScenes full | /mnt/titan-healthcare/nuscenes/ | 479GB | SURT, BESTLA, FORSETI |
| Replica | /mnt/forge-data/datasets/replica/ | 63GB | SIF, HEIMDALL, MIMIR |
| SensatUrban | /mnt/forge-data/datasets/sensat_urban/ | 30GB | RAN |
| VIVID++ thermal | /mnt/forge-data/datasets/vivid_plus_plus/ | 47GB | NOTT, SOL |
| SOL synthetic thermal | /mnt/artifacts-datai/datasets/sol_thermal_synthetic/ | 30GB+ | NOTT, FREYA, defense modules |
| TacQuad | /mnt/forge-data/datasets/tacquad/ | downloading | HAPTOS |
| Kubric | /mnt/titan-healthcare/kubric-train/ | 2.4TB | TYR |
| SUN RGB-D | /mnt/forge-data/datasets/sun_rgbd/ | 20GB | MIMIR |
| TUM RGB-D | /mnt/forge-data/datasets/tum/ | 6.6GB | FREYA, THOR, NOTT |

---

## DO NOT

- DO NOT train without running preflight
- DO NOT generate mock/synthetic data to "pass" preflight — that defeats the purpose
- DO NOT mark a dataset as "DONE" unless you verified sample count matches paper
- DO NOT start a multi-hour training run if ANY required dataset is missing
- DO NOT assume "file exists" means "file is correct" — check sizes and load a sample
