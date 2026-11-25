# /anima-push-hf-datasets — Push Datasets to HuggingFace

**Purpose:** Package and push datasets to HuggingFace under `ilessio-aiflowlab` org. Creates proper dataset cards, splits, and metadata for public or private release.

**HF Organization:** `ilessio-aiflowlab`
**Naming Pattern:** `ilessio-aiflowlab/{dataset_name}` (e.g. `ilessio-aiflowlab/vivid-thermal-slam`)

---

## STEP 1: IDENTIFY — What dataset to push?

Check the current module directory for datasets:
```bash
MODULE_NAME=$(basename $(pwd) | sed 's/project_//')
echo "Module: ${MODULE_NAME}"

# Find datasets
find /mnt/forge-data/datasets -maxdepth 2 -type d | head -20
ls /mnt/forge-data/datasets/ | grep -i "${MODULE_NAME}"
```

Ask the user:
- Dataset name (human-readable)
- Public or private?
- License (default: CC-BY-4.0 for public datasets, proprietary for private)
- Source attribution (paper, authors, institution)

---

## STEP 2: ORGANIZE — Structure the dataset

Create a staging directory:
```bash
DATASET_NAME="<dataset-slug>"  # e.g. vivid-thermal-slam
STAGING="/mnt/artifacts-datai/hf_datasets/${DATASET_NAME}"
mkdir -p ${STAGING}/{train,val,test,metadata}
```

Standard structure:
```
{dataset_name}/
├── README.md              # Dataset card (REQUIRED)
├── train/                 # Training split
├── val/                   # Validation split (if exists)
├── test/                  # Test split (if exists)
├── metadata/              # Sensor specs, calibration, configs
│   ├── sensors.json       # Camera/LiDAR/IMU specs
│   ├── calibration/       # Intrinsics, extrinsics
│   └── splits.json        # Train/val/test indices
├── LICENSE                # License file
└── .gitattributes         # LFS tracking for large files
```

For rosbag datasets:
```
{dataset_name}/
├── README.md
├── bags/                  # Raw rosbags
│   ├── sequence_001.bag
│   └── sequence_002.bag
├── extracted/             # Extracted frames (optional)
│   ├── thermal/
│   ├── depth/
│   └── rgb/
├── metadata/
└── LICENSE
```

---

## STEP 3: GENERATE README — Dataset card

Generate a HuggingFace dataset card:

```markdown
---
license: cc-by-4.0
task_categories:
  - depth-estimation
  - image-segmentation
  - robotics
tags:
  - thermal
  - slam
  - robotics
  - anima
  - robot-flow-labs
  - {module_name}
pretty_name: "{Human Readable Dataset Name}"
size_categories:
  - 1K<n<10K
---

# {Dataset Name}

Part of the [ANIMA Perception Suite](https://robotflowlabs.com) by **Robot Flow Labs** / AIFLOW LABS LIMITED.

## Overview
{Brief description of what this dataset contains and why it matters}

## Source
- **Paper**: {paper title} ({arxiv_id})
- **Authors**: {author list}
- **Original source**: {URL}
- **License**: {license}

## Sensors
| Sensor | Model | Resolution | FPS | Notes |
|--------|-------|-----------|-----|-------|
| {sensor} | {model} | {resolution} | {fps} | {notes} |

## Dataset Statistics
| Split | Samples | Size |
|-------|---------|------|
| Train | {n} | {size} |
| Val | {n} | {size} |
| Test | {n} | {size} |
| **Total** | **{n}** | **{size}** |

## Usage
```python
from huggingface_hub import snapshot_download
snapshot_download("ilessio-aiflowlab/{dataset_name}", local_dir="./data")
```

## Citation
```bibtex
@article{...}
```

## License
{license} — Robot Flow Labs / AIFLOW LABS LIMITED
```

---

## STEP 4: CONFIGURE LFS — Track large files

```bash
cd ${STAGING}
cat > .gitattributes << 'EOF'
*.bag filter=lfs diff=lfs merge=lfs -text
*.rosbag filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.safetensors filter=lfs diff=lfs merge=lfs -text
*.onnx filter=lfs diff=lfs merge=lfs -text
*.trt filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.npy filter=lfs diff=lfs merge=lfs -text
*.npz filter=lfs diff=lfs merge=lfs -text
*.h5 filter=lfs diff=lfs merge=lfs -text
*.hdf5 filter=lfs diff=lfs merge=lfs -text
*.zip filter=lfs diff=lfs merge=lfs -text
*.tar filter=lfs diff=lfs merge=lfs -text
*.tar.gz filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
EOF
```

---

## STEP 5: PUSH — Upload to HuggingFace

```bash
DATASET_NAME="<dataset-slug>"
HF_REPO="ilessio-aiflowlab/${DATASET_NAME}"
STAGING="/mnt/artifacts-datai/hf_datasets/${DATASET_NAME}"
VISIBILITY="--public"  # or --private

# Create dataset repo
huggingface-cli repo create ${HF_REPO} --type dataset ${VISIBILITY} 2>/dev/null || true

# Upload with nohup (survives disconnects)
nohup bash -c "
  huggingface-cli upload ${HF_REPO} ${STAGING} --repo-type dataset
  echo '[DONE] Pushed to https://huggingface.co/datasets/${HF_REPO}'
" > /mnt/artifacts-datai/logs/hf_dataset_push_${DATASET_NAME}.log 2>&1 &
disown
echo "Pushing in background. Monitor: tail -f /mnt/artifacts-datai/logs/hf_dataset_push_${DATASET_NAME}.log"
```

---

## STEP 6: VERIFY

```bash
DATASET_NAME="<dataset-slug>"
HF_REPO="ilessio-aiflowlab/${DATASET_NAME}"
huggingface-cli download ${HF_REPO} --repo-type dataset --dry-run 2>&1
```

Print final report:
```
=== DATASET PUSH COMPLETE ===
Repo: https://huggingface.co/datasets/ilessio-aiflowlab/{dataset_name}
Visibility: public/private
Files: X
Size: Y GB
License: Z
```

---

## ARGUMENTS

- No args: Interactive — ask what dataset to push
- `--dataset PATH`: Path to dataset directory
- `--name NAME`: HF dataset name
- `--public`: Make dataset public (default for datasets)
- `--private`: Make dataset private
- `--dry-run`: Show what would be pushed without pushing

---

## DO NOT

- DO NOT push without README.md — every dataset needs a card
- DO NOT push without checking license of source data
- DO NOT push proprietary/gated datasets as public
- DO NOT push .venv, __pycache__, or build artifacts
- DO NOT push without .gitattributes for LFS
- DO NOT forget to attribute original authors
- DO NOT run upload without nohup + disown
