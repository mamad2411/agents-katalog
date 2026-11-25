---
name: repo-cogvideo
description: How to use CogVideo / CogVideoX (zai-org, formerly THUDM), open-source text-to-video, image-to-video and video-continuation models that run on modest GPUs via Diffusers, with LoRA fine-tuning. Use when a user wants low-VRAM self-hosted video generation or fine-tuning.
---

# CogVideo / CogVideoX (`zai-org/CogVideo`)

Code licence Apache-2.0; **model weights have their own licence** (`MODEL_LICENSE`; CogVideoX-2B is Apache-2.0 per the README, check the others). Cloned shallow at `/home/user/zai-org/cogvideo` (re-clone `git clone --depth 1 https://github.com/zai-org/CogVideo`).

## Models and memory (README figures, Diffusers path)
- CogVideoX-2B: FP16 about 4 GB minimum, INT8 (torchao) about 3.6 GB; runs on old GPUs such as a GTX 1080 Ti.
- CogVideoX-5B and 5B-I2V: BF16 from about 5-10 GB with offloading; CogVideoX1.5-5B supports 10-second clips.
- SAT (SwissArmyTransformer) path needs far more memory (about 18-76 GB). Prefer Diffusers.

## Run
```bash
pip install -r requirements.txt
python inference/cli_demo.py --prompt "..." --model_path THUDM/CogVideoX-5b --generate_type t2v
# quantised: inference/cli_demo_quantization.py ; prompt rewriting: inference/convert_demo.py
```
Verify option names with `--help`; model ids moved from THUDM to zai-org on Hugging Face in places.

## Fine-tuning
`finetune/README.md` documents LoRA and full fine-tuning; the README states CogVideoX-5B LoRA fits on a single RTX 4090 via `cogvideox-factory`. Before fine-tuning use the `finetune` and `eval-harness` skills: define the eval set first.

## Related
`ai-video-generators`, `repo-wan21`, `repo-hunyuanvideo`.
