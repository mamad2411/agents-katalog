# /anima-mlx-convert — Download from HF, Convert to MLX, Push Back

Use this skill when: you need to convert a trained ANIMA module's model to Apple MLX format for on-device inference on Apple Silicon. Runs on Mac (NOT server).

## What This Skill Does

1. Opens the HF repo for the module
2. Downloads safetensors/ONNX/pth to Mac
3. Detects model type (LLM vs vision/robotics)
4. Converts to MLX format (with optional quantization)
5. Validates the MLX model loads and runs
6. Pushes MLX version back to HF (same repo or `-mlx` variant)

---

## Prerequisites

```bash
# Install once (uv-managed)
uv pip install mlx mlx-lm torch2mlx[all] safetensors huggingface-hub
```

Verify:
```bash
python -c "import mlx.core as mx; print(f'MLX {mx.__version__} on {mx.default_device()}')"
```

---

## Step 1: Identify the Module and HF Repo

```bash
# Module name from current directory or argument
MODULE_NAME=${1:-$(basename $(pwd))}
HF_REPO="ilessio-aiflowlab/${MODULE_NAME}"

echo "Module: $MODULE_NAME"
echo "HF Repo: https://huggingface.co/$HF_REPO"

# Check what's on HF
huggingface-cli repo info $HF_REPO 2>/dev/null || echo "Repo doesn't exist yet"
```

---

## Step 2: Download Model from HF

```bash
# Create local workspace
MLX_WORK=~/mlx-convert/$MODULE_NAME
mkdir -p $MLX_WORK/{original,mlx_output}

# Download safetensors (preferred) or pth
huggingface-cli download $HF_REPO \
  --include "*.safetensors" "*.pth" "*.json" "*.toml" "config.*" "tokenizer.*" \
  --local-dir $MLX_WORK/original

# Check what we got
echo "=== Downloaded files ==="
find $MLX_WORK/original -type f | head -20
du -sh $MLX_WORK/original
```

If no safetensors exists but pth does, convert first:
```python
import torch
from safetensors.torch import save_file

state = torch.load("model.pth", map_location="cpu")
if "model" in state:
    state = state["model"]
elif "state_dict" in state:
    state = state["state_dict"]
save_file(state, "model.safetensors")
```

---

## Step 3: Detect Model Type

Read the model config to determine conversion strategy:

```python
import json, os

config_path = os.path.join(work_dir, "original", "config.json")
if os.path.exists(config_path):
    config = json.load(open(config_path))
    arch = config.get("architectures", ["unknown"])[0]
    model_type = config.get("model_type", "unknown")
    print(f"Architecture: {arch}")
    print(f"Model type: {model_type}")
```

**Decision tree:**
- If `model_type` in `[llama, qwen, mistral, phi, gemma]` → use `mlx-lm`
- If architecture has `ForCausalLM`, `ForSequenceClassification` → use `mlx-lm`
- If custom vision/robotics model (ResNet, ViT, custom) → use `torch2mlx`
- If unknown → try `torch2mlx` (handles more architectures)

---

## Step 4A: Convert with mlx-lm (Language Models)

```bash
# Basic conversion
mlx_lm.convert \
  --hf-path $MLX_WORK/original \
  --mlx-path $MLX_WORK/mlx_output

# With 4-bit quantization (recommended for edge)
mlx_lm.convert \
  --hf-path $MLX_WORK/original \
  --mlx-path $MLX_WORK/mlx_output \
  -q --q-bits 4 --q-group-size 64

# With 8-bit quantization (higher quality)
mlx_lm.convert \
  --hf-path $MLX_WORK/original \
  --mlx-path $MLX_WORK/mlx_output \
  -q --q-bits 8
```

---

## Step 4B: Convert with torch2mlx (Vision/Robotics Models)

```bash
# Weights-only conversion
python -m torch2mlx $MLX_WORK/original/model.safetensors $MLX_WORK/mlx_output/
```

Or manual conversion for custom architectures:

```python
import torch
import mlx.core as mx
import numpy as np
from safetensors.torch import load_file
from safetensors.numpy import save_file as save_np

# Load PyTorch weights
pt_weights = load_file("original/model.safetensors")

mlx_weights = {}
for name, tensor in pt_weights.items():
    arr = tensor.numpy()

    # Conv2d: PyTorch [O,I,H,W] → MLX [O,H,W,I]
    if len(arr.shape) == 4:
        arr = np.transpose(arr, (0, 2, 3, 1))
        print(f"  [CONV] {name}: transposed to {arr.shape}")

    # Conv1d: PyTorch [O,I,L] → MLX [O,L,I]
    elif len(arr.shape) == 3 and 'conv' in name.lower():
        arr = np.transpose(arr, (0, 2, 1))
        print(f"  [CONV1D] {name}: transposed to {arr.shape}")

    # BatchNorm running stats: keep as-is
    # Linear: keep as-is (no transpose needed)

    mlx_weights[name] = arr

# Save as safetensors with MLX metadata
save_np(mlx_weights, "mlx_output/model.safetensors", metadata={"format": "mlx"})
print(f"Saved {len(mlx_weights)} tensors to mlx_output/model.safetensors")
```

---

## Step 5: Create MLX Config

```python
import json

# Read original config
orig_config = json.load(open("original/config.json")) if os.path.exists("original/config.json") else {}

# Create MLX config
mlx_config = {
    **orig_config,
    "model_type": orig_config.get("model_type", "custom"),
    "framework": "mlx",
    "converted_from": "pytorch",
    "quantization": None,  # or {"bits": 4, "group_size": 64}
}

with open("mlx_output/config.json", "w") as f:
    json.dump(mlx_config, f, indent=2)
```

---

## Step 6: Validate MLX Model

```python
import mlx.core as mx

# Load and verify
weights = mx.load("mlx_output/model.safetensors")
print(f"Loaded {len(weights)} tensors")

# Check shapes and dtypes
total_params = 0
for name, arr in weights.items():
    total_params += arr.size
    if total_params < 10:  # Print first few
        print(f"  {name}: {arr.shape} ({arr.dtype})")

print(f"Total parameters: {total_params:,}")
print(f"Model size: {sum(v.nbytes for v in weights.values()) / 1e6:.1f} MB")

# Quick inference test (if model class available)
# model = MyMLXModel(config)
# model.load_weights("mlx_output/model.safetensors")
# dummy = mx.random.normal((1, 3, 224, 224))
# out = model(dummy)
# print(f"Output shape: {out.shape}")
```

---

## Step 7: Create Model Card

```python
readme = f"""---
library_name: mlx
tags:
  - mlx
  - anima
  - robotics
  - apple-silicon
  - {MODULE_NAME}
license: apache-2.0
base_model: ilessio-aiflowlab/{MODULE_NAME}
---

# {MODULE_NAME} — MLX Format

Apple MLX conversion of [{MODULE_NAME}](https://huggingface.co/ilessio-aiflowlab/{MODULE_NAME}).

## Usage

```python
import mlx.core as mx

weights = mx.load("model.safetensors")
# Load into your MLX model class
```

## Conversion Details

- **Source**: ilessio-aiflowlab/{MODULE_NAME}
- **Format**: safetensors (MLX layout)
- **Quantization**: {{quantization_info}}
- **Converted with**: torch2mlx / mlx-lm

## Part of ANIMA Suite

[AIFLOW LABS](https://robotflowlabs.com) — Robotics perception stack.
"""

with open("mlx_output/README.md", "w") as f:
    f.write(readme)
```

---

## Step 8: Push to HuggingFace

```bash
# Option A: Push to same repo under mlx/ subfolder
huggingface-cli upload $HF_REPO $MLX_WORK/mlx_output mlx/ --repo-type model

# Option B: Push to separate -mlx repo (recommended)
MLX_REPO="${HF_REPO}-mlx"
huggingface-cli repo create $(basename $MLX_REPO) --organization ilessio-aiflowlab 2>/dev/null
huggingface-cli upload $MLX_REPO $MLX_WORK/mlx_output . --repo-type model

echo "✅ Pushed to https://huggingface.co/$MLX_REPO"
```

---

## Quick One-Liner (for LLMs)

```bash
# Convert + quantize + push in one command
mlx_lm.convert \
  --hf-path ilessio-aiflowlab/$MODULE_NAME \
  --mlx-path ~/mlx-convert/$MODULE_NAME/mlx_output \
  -q --q-bits 4 \
  --upload-repo ilessio-aiflowlab/${MODULE_NAME}-mlx-4bit
```

---

## Batch Convert All ANIMA Modules

```bash
#!/usr/bin/env bash
# Convert all modules that have safetensors on HF

MODULES=(
  project_loci
  project_monad
  project_petra
  project_prism
  project_morpheus
  project_atomos
  project_grid
  project_elysium
)

for mod in "${MODULES[@]}"; do
  echo "=== Converting $mod ==="
  mkdir -p ~/mlx-convert/$mod/{original,mlx_output}

  # Download
  huggingface-cli download ilessio-aiflowlab/$mod \
    --include "*.safetensors" "*.json" \
    --local-dir ~/mlx-convert/$mod/original

  # Convert (try mlx-lm first, fallback to torch2mlx)
  mlx_lm.convert \
    --hf-path ~/mlx-convert/$mod/original \
    --mlx-path ~/mlx-convert/$mod/mlx_output 2>/dev/null \
  || python -m torch2mlx \
    ~/mlx-convert/$mod/original/model.safetensors \
    ~/mlx-convert/$mod/mlx_output/

  # Push
  huggingface-cli upload ilessio-aiflowlab/${mod}-mlx \
    ~/mlx-convert/$mod/mlx_output . --repo-type model

  echo "✅ $mod done"
done
```

---

## Quantization Guide

| Bits | Size Reduction | Quality | Use Case |
|------|---------------|---------|----------|
| 4-bit | ~75% smaller | Good for inference | Edge deployment, mobile |
| 8-bit | ~50% smaller | Near-original quality | Mac inference, demos |
| fp16 | ~50% smaller | Lossless | Default MLX format |
| Mixed (3/6) | ~60% smaller | Balanced | Best quality/size tradeoff |

```bash
# Mixed quantization (recommended)
mlx_lm.convert --hf-path $MODEL --mlx-path $OUT \
  -q --quant-predicate mixed_3_6
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `No module named 'mlx'` | Only works on Apple Silicon Mac, not Linux server |
| Conv weights wrong | Check OIHW→OHWI transpose applied |
| Model too large for Mac | Use 4-bit quantization |
| `torch2mlx` fails | Fall back to manual conversion (Step 4B manual) |
| HF push fails | Check `huggingface-cli login` with write token |
