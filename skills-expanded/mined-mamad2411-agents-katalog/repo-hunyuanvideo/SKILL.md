---
name: repo-hunyuanvideo
description: How to run HunyuanVideo (Tencent-Hunyuan/HunyuanVideo), Tencent's open-source text-to-video model, and the licence restriction that excludes the EU, UK and South Korea. Use when a user asks about self-hosting HunyuanVideo, its GPU needs, or whether they may legally use it.
---

# HunyuanVideo (`Tencent-Hunyuan/HunyuanVideo`)

Cloned shallow for review at `/home/user/tencent-hunyuan/hunyuanvideo` (re-clone with `git clone --depth 1 https://github.com/Tencent-Hunyuan/HunyuanVideo`). Weights are downloaded separately (`ckpts/README.md`).

## Licence warning - read first
The repo uses the **Tencent Hunyuan Community License**, which states it **does not apply in the European Union, United Kingdom and South Korea**; the licensed Territory is worldwide excluding those. A user located in Greece or any EU state has no licence grant under this text. Say this before helping with setup, recommend `repo-wan21` or `repo-cogvideo` (Apache-2.0 code) as alternatives, and suggest legal review if the user still wants to proceed. The README also lists newer variants (HunyuanVideo-1.5, -I2V, -Avatar, HunyuanCustom) in separate repos with their own licences - check each.

## Requirements (from README)
- NVIDIA GPU with CUDA. Minimum 60 GB for 720x1280x129 frames, 45 GB for 544x960x129; 80 GB recommended.
- Python 3.10.9, PyTorch 2.6 (CUDA 11.8 or 12.4), flash-attention v2.6.3, optional xDiT for multi-GPU.
- FP8 weights and the community "GP" low-VRAM fork exist; verify their licences too.

## Setup and run
```bash
conda create -n HunyuanVideo python==3.10.9 && conda activate HunyuanVideo
python -m pip install -r requirements.txt
python3 sample_video.py --prompt "..." --video-size 720 1280 --video-length 129 --save-path ./results
# or: python gradio_server.py
```
Confirm exact flags in `sample_video.py --help` before running; the README sections change.

## Related
`ai-video-generators`, `repo-wan21`, `repo-cogvideo`.
