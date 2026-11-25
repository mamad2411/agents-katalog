---
name: repo-ominicontrol
description: How to use OminiControl (Yuanshi9815/OminiControl), a minimal universal control framework for FLUX diffusion transformers covering subject-driven generation, in-painting, edge/depth-guided generation and style LoRA combination. Use when a user wants to generate consistent-subject images or add spatial control to FLUX.
---

# OminiControl (`Yuanshi9815/OminiControl`)

Apache-2.0 code, from the xML Lab at the National University of Singapore. Cloned shallow at `/home/user/yuanshi9815/ominicontrol` (re-clone `git clone --depth 1 https://github.com/Yuanshi9815/OminiControl`). The saved note spelled it "ominicontrol".

## What it does
Adds control signals to FLUX with about 0.1% extra parameters. Supports subject-driven control and spatial control (Canny edge, depth, colourisation, deblurring, in-painting). OminiControl2 adds KV-cache conditioning (about 1.5x speed-up reported). OminiControl Art stylises images. Training code is included so you can train custom control tasks.

## Setup
```bash
conda create -n omini python=3.12 && conda activate omini
pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cu128   # match your CUDA
pip install -r requirements.txt
```
Examples are notebooks: `examples/subject.ipynb`, `subject_dev.ipynb` (FLUX.1-dev), `inpainting.ipynb`, `spatial.ipynb`, `combine_with_style_lora.ipynb`, `ominicontrol_art.ipynb`.

## Notes
- `generate(..., condition_scale=1.3)` strengthens the condition; `kv_cache=True` needs a LoRA trained with independent conditions.
- If loading several LoRAs, call `pipe.set_adapters([...])` explicitly.
- FLUX.1-dev weights carry a non-commercial licence; FLUX.1-schnell is Apache-2.0. Confirm before commercial use.
- Subject-driven generation of real people needs their consent.

## Related
`ai-image-design-tools`, `repo-wan21`.
