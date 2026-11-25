---
name: download-model
description: "Download a model from ModelScope to the shared models directory (/mnt/share_data/weichenhan.wch/models). Use when: user asks to download a model, fetch a model, pull a model from ModelScope, or prepare a model for training/inference. Handles Qwen, LLaMA, and any ModelScope-hosted model."
argument-hint: "ModelScope model ID, e.g. Qwen/Qwen2.5-7B-Instruct"
---

# Download Model from ModelScope

## When to Use
- User asks to download / fetch / pull a specific model
- User wants to prepare a model for RL training or inference
- User references a ModelScope model ID (e.g. `Qwen/Qwen2.5-7B-Instruct`)

## Environment
- **Models directory**: `$MODELS_DIR` or `/mnt/share_data/weichenhan.wch/models`
- **Python venv**: `/root/wch/exp_RL/.venv/bin/python`
- **Dependency**: `modelscope` (pre-installed in venv)

## Procedure

1. **Identify the model ID** from the user's request (e.g. `Qwen/Qwen2.5-7B-Instruct`).

2. **Check disk space** before downloading large models:
   ```bash
   df -h /mnt/share_data/
   ```

3. **Run the download script** in the background (models are large):
   ```bash
   /root/wch/exp_RL/.venv/bin/python /root/wch/exp_RL/.github/skills/download-model/scripts/download_model.py <model_id>
   ```
   - The script saves to `/mnt/share_data/weichenhan.wch/models/<org>--<model_name>/`
   - If the model already exists locally, the script skips the download.
   - Use `--revision <branch>` to specify a branch (default: `master`).

4. **Verify** the download completed:
   ```bash
   ls -lh /mnt/share_data/weichenhan.wch/models/<org>--<model_name>/
   ```

5. **Report the local path** to the user so they can use it in training configs.

## Model Path Convention

Models are stored as `<org>--<model_name>` under `$MODELS_DIR`:
```
/mnt/share_data/weichenhan.wch/models/
├── Qwen--Qwen2.5-1.5B-Instruct/
├── Qwen--Qwen2.5-7B-Instruct/
└── Qwen--Qwen2.5-Coder-7B-Instruct/
```

To reference in training scripts, use:
```python
import os
model_path = os.path.join(os.environ["MODELS_DIR"], "Qwen--Qwen2.5-7B-Instruct")
```

## Common Models for This Project

| Model ID | Size | Used In |
|----------|------|---------|
| `Qwen/Qwen2.5-1.5B-Instruct` | ~3 GB | Exp 1 (GRPO math) |
| `Qwen/Qwen2.5-7B-Instruct` | ~15 GB | Exp 2 (DAPO), Exp 4 (Agentic) |
| `Qwen/Qwen2.5-Coder-7B-Instruct` | ~15 GB | Exp 3 (Code RL) |
| `Qwen/Qwen2.5-14B-Instruct` | ~28 GB | Exp 4 (Agentic + LoRA) |
