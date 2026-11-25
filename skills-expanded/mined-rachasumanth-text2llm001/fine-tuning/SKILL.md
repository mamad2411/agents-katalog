---
name: fine-tuning
description: Fine-tune pretrained models with LoRA, QLoRA, or full fine-tuning using HF Trainer and TRL for instruction, chat, and preference alignment.
---

# Fine-Tuning (LoRA / QLoRA / Full)

Use this skill when the user wants to **adapt an existing pretrained model** rather than train from scratch.
Covers instruction tuning, chat fine-tuning, DPO/RLHF alignment, and domain adaptation.

## Supported Methods

- **LoRA** — low-rank adapter injection, minimal VRAM, fast iteration.
- **QLoRA** — quantized base model (4-bit NF4) + LoRA for ultra-low memory.
- **Full fine-tuning** — all parameters updated, requires more compute but maximum control.

Default to QLoRA unless user specifies otherwise or VRAM budget permits full fine-tuning.

## Dataset Formats

Accept and convert between common formats:

- **Alpaca** (`instruction`, `input`, `output`)
- **ShareGPT** (multi-turn `conversations` array)
- **OpenAI chat** (`messages` with `role`/`content`)
- **Preference pairs** (chosen/rejected for DPO)

Validate dataset schema before training. Report malformed rows and auto-skip with warning.

## Training Stack

### HF Trainer + PEFT

- Use `transformers.Trainer` or `trl.SFTTrainer` for supervised fine-tuning.
- Use `trl.DPOTrainer` for preference alignment.
- Configure LoRA via `peft.LoraConfig` with sensible defaults:
  - rank: 16–64
  - alpha: 16–64
  - target modules: auto-detect or explicit (`q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`)
  - dropout: 0.05

### Training Defaults

- gradient accumulation to simulate larger effective batch
- cosine LR schedule with warmup
- bf16/fp16 mixed precision
- gradient checkpointing enabled for QLoRA
- max sequence length configurable (default: 2048)

## Adapter Management

- Save adapters separately from base model.
- Support adapter merging back into base weights for inference.
- Validate merged model produces correct outputs before publishing.
- Track adapter lineage: base model, dataset, training config, metrics.

## Evaluation During Training

- Run eval on held-out split every N steps.
- Log train loss, eval loss, and learning rate.
- Early stopping on eval loss plateau (configurable patience).

## Deliverables

1. `finetune_config.yaml` (method, hyperparameters, dataset)
2. `adapter_config.json` (LoRA rank, target modules, alpha)
3. Adapter weights (or merged model if requested)
4. `finetune_report.md` (metrics, training curves, recommendations)

## Python Dependencies

- `transformers`
- `peft`
- `trl`
- `bitsandbytes`
- `datasets`
- `accelerate`
