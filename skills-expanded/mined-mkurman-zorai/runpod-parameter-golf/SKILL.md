---
name: runpod-parameter-golf
description: "Run Parameter Golf competition submissions on RunPod GPU Pods. Covers required operator inputs, RunPod pod specs, FineWeb SP1024 data caching, record-folder hygiene, torchrun launch commands, monitoring, artifact-size checks, and result collection."
tags: [runpod, parameter-golf, gpu-training, fineweb, competition, torchrun, h100]
---

# RunPod Parameter Golf

Use this skill when launching or preparing a Parameter Golf submission on RunPod, especially when the operator expects the agent to provision a Pod or run a competition-style training job.

## Non-Negotiables

- A valid competition-style run happens in a Parameter Golf checkout from inside one record folder.
- The submission must be self-contained: no local package imports, unrelated training code, local-only checkpoints, or hidden dependencies.
- Use stock FineWeb SP1024 cached shards unless the submission intentionally changes tokenizer/data and proves BPB accounting.
- The 16MB cap is decimal: `16,000,000` bytes.
- Do not claim completion before the log contains `final_int8_zlib_roundtrip_exact` and the artifact-size line.

## What To Ask The Operator For

Before you can run it yourself, request:

```text
RunPod API key or SSH command:
Budget ceiling:
Run mode: smoke / final / smoke-then-final
GPU: 1xH100 smoke? 8xH100 final?
Cloud/storage: Secure Cloud? volume GB or networkVolumeId?
File transfer: Git clone / rsync/SCP / runpodctl?
Source folder or repo URL/branch:
Cleanup policy: stop or terminate after artifacts are safe?
```

If API access is provided, use least privilege that can create/list/start/stop/delete Pods and optionally create/list network volumes. Treat keys as secrets; never write them into logs, commits, or durable memory.

## Recommended RunPod Pod Specs

### Final 8xH100 run

```json
{
  "cloudType": "SECURE",
  "computeType": "GPU",
  "gpuTypeIds": ["NVIDIA H100 80GB HBM3"],
  "gpuCount": 8,
  "imageName": "runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04",
  "containerDiskInGb": 50,
  "volumeInGb": 200,
  "volumeMountPath": "/workspace",
  "ports": ["22/tcp", "8888/http"],
  "supportPublicIp": true,
  "interruptible": false
}
```

### Smoke run

Use the same image and ports with `gpuCount=1`. If the FineWeb cache must be downloaded on the smoke pod, keep `volumeInGb=200`; otherwise 100GB is acceptable.

## Setup Commands On The Pod

```bash
cd /workspace
if [ ! -d parameter-golf ]; then
  git clone https://github.com/openai/parameter-golf.git
fi
cd /workspace/parameter-golf
python3 -m pip install --upgrade pip
pip install numpy sentencepiece huggingface-hub datasets tqdm
```

Download data:

```bash
# Smoke cache
python3 data/cached_challenge_fineweb.py --variant sp1024 --train-shards 1

# Final cache
python3 data/cached_challenge_fineweb.py --variant sp1024
```

Expected paths:

```text
/workspace/parameter-golf/data/datasets/fineweb10B_sp1024/
/workspace/parameter-golf/data/tokenizers/fineweb_1024_bpe.model
```

## Submission Placement

The run folder must look like this:

```text
/workspace/parameter-golf/records/<track>/<date_or_name>/
  README.md
  submission.json
  train_gpt.py
```

For a prepared non-record ConvGPT-style folder:

```bash
mkdir -p /workspace/parameter-golf/records/track_non_record_16mb
# Copy or clone the folder here, then:
cd /workspace/parameter-golf/records/track_non_record_16mb/<submission-folder>
```

## Launch Commands

### Final 8xH100

```bash
RUN_ID=convgpt_hybridconv_sp1024_8h100 \
DATA_PATH=/workspace/parameter-golf/data/datasets/fineweb10B_sp1024 \
TOKENIZER_PATH=/workspace/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
VOCAB_SIZE=1024 \
MODEL_DIM=256 \
NUM_LAYERS=8 \
MLP_MULT=2 \
GRID_SIZE=32 \
MAX_WALLCLOCK_SECONDS=600 \
TRAIN_LOG_EVERY=50 \
VAL_LOSS_EVERY=1000 \
torchrun --standalone --nproc_per_node=8 train_gpt.py 2>&1 | tee runpod_console.log
```

### 1xH100 smoke

```bash
RUN_ID=convgpt_hybridconv_sp1024_smoke \
DATA_PATH=/workspace/parameter-golf/data/datasets/fineweb10B_sp1024 \
TOKENIZER_PATH=/workspace/parameter-golf/data/tokenizers/fineweb_1024_bpe.model \
VOCAB_SIZE=1024 \
MODEL_DIM=256 \
NUM_LAYERS=8 \
MLP_MULT=2 \
GRID_SIZE=32 \
ITERATIONS=5 \
MAX_WALLCLOCK_SECONDS=0 \
TRAIN_BATCH_TOKENS=65536 \
VAL_BATCH_SIZE=65536 \
TRAIN_LOG_EVERY=1 \
VAL_LOSS_EVERY=0 \
torchrun --standalone --nproc_per_node=1 train_gpt.py 2>&1 | tee smoke_console.log
```

## Monitoring Checklist

Watch for:

- dependency import failures (`sentencepiece`, `torch`, `numpy`)
- missing data paths
- `CUDA out of memory`
- `final_model.int8.ptz` creation
- `Total submission size int8+zlib: ...`
- `final_int8_zlib_roundtrip_exact val_loss:... val_bpb:...`

After success:

```bash
cp logs/${RUN_ID}.txt train.log
python3 - <<'PY'
from pathlib import Path
log = Path('train.log').read_text(errors='ignore')
for key in ['Total submission size int8+zlib', 'final_int8_zlib_roundtrip_exact']:
    print('\n'.join(line for line in log.splitlines() if key in line)[-2000:])
PY
```

Update `submission.json` with exact `val_bpb`, `val_loss`, artifact size, command, GPU count, and run status.

## File Transfer Notes

RunPod docs distinguish:

- basic proxied SSH: quick shell access, no SCP/SFTP
- full SSH with public IP and exposed `22/tcp`: supports SCP/SFTP/rsync
- `runpodctl send/receive`: easy for small-to-medium transfers
- `rsync`: best for large or repeated transfers

For agents, prefer full SSH or Git clone so the workflow is reproducible and resumable.

## Cleanup

Before stopping/terminating:

1. Confirm `train.log`, `submission.json`, `README.md`, and `train_gpt.py` are present.
2. Copy out `train.log` and `final_model.int8.ptz` if the Pod volume is not persistent.
3. Stop the Pod to release GPU if preserving `/workspace` data.
4. Terminate only after artifacts are safely copied or stored on a network volume.
