---
name: finetune-unsloth
description: >
  Fine-tuning LLMs with Unsloth — fast QLoRA/LoRA on a single GPU. Carries:
  `FastLanguageModel.from_pretrained(..., load_in_4bit=True)`, `get_peft_model` (r/alpha/
  target_modules incl. gate/up/down for llama-family), `use_gradient_checkpointing="unsloth"`,
  chat templates (`get_chat_template`, `train_on_responses_only`), TRL `SFTTrainer` wiring
  (max_seq_length, packing, LoRA learning rates), and export (`save_pretrained_merged`, GGUF).
  Load when fine-tuning or LoRA-adapting an LLM, choosing PEFT hyperparameters, or exporting a
  tuned model. Triggers: unsloth, fine-tune LLM, finetune, LoRA, QLoRA, PEFT, SFT, SFTTrainer,
  4-bit, bitsandbytes, chat template, train_on_responses_only, adapter, merge adapter, GGUF,
  target_modules, lora_alpha, max_seq_length, DPO, GRPO, instruction tuning.
---

# finetune-unsloth — LLM fine-tuning with Unsloth

**Pinned:** unsloth — unpinned · authored 2026-07-18 from pre-install knowledge · **run
`/skill-update finetune-unsloth` immediately after installing** (Unsloth's API moves faster than
any other tool skill's; treat every fact below as unverified until then)

> On-demand: load this before fine-tuning an LLM. This is the LLM lane's `training` — the CV loop
> conventions don't transfer, but the *disciplines* do: seed everything, track every run
> (`tracking-mlflow`/`tracking-wandb`), config over constants (`config-hydra`), and split hygiene
> (`datasets` — dedupe/decontaminate eval prompts against training data; contamination is this
> lane's leakage).

## When this applies
SFT / instruction-tuning / preference-tuning (DPO, GRPO) of an open-weights LLM with LoRA or QLoRA
via Unsloth + TRL. Full-parameter pretraining, CV training (`training`), and serving are out of
scope.

## Install — let Unsloth drive its own pin set
Unsloth pins compatible `transformers`/`trl`/`peft`/`bitsandbytes` versions; fighting it with your
own pins is the classic broken-env cause. `uv add unsloth` (plus the CUDA-matched torch per
`env-uv`) and let its resolution win; on conflict, relax your pins, not Unsloth's.

## Load + adapt (the canonical shape)
```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=cfg.model.name,          # e.g. a llama/qwen/gemma instruct checkpoint
    max_seq_length=cfg.model.max_seq_length,
    load_in_4bit=True,                  # QLoRA; False -> LoRA on 16-bit
    dtype=None,                         # auto-picks bf16/fp16 for the GPU
)
model = FastLanguageModel.get_peft_model(
    model,
    r=cfg.lora.r,                       # 8–64; capacity vs VRAM/overfit
    lora_alpha=cfg.lora.alpha,          # convention: = r (or 2r)
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],   # attn-only = weaker; include MLP
    lora_dropout=0,                     # 0 is Unsloth's fast path
    bias="none",
    use_gradient_checkpointing="unsloth",   # their long-context-friendly variant
    random_state=cfg.seed,
)
```

## Data + chat template — where silent quality loss happens
- Format with the model's own template: `get_chat_template(tokenizer, chat_template=...)` from
  `unsloth.chat_templates`, then apply to your conversation records. A mismatched template trains
  fine and degrades generation — no error anywhere.
- **Mask the loss to responses:** `train_on_responses_only(trainer, instruction_part=...,
  response_part=...)` so the model isn't trained to imitate your prompts. Verify the mask by
  decoding one batch's labels (`-100` everywhere except assistant spans) — don't trust, look.
- Dedupe train vs eval prompts, and check eval sets against known benchmark contamination before
  quoting scores.

## Train (TRL `SFTTrainer`)
LoRA defaults that work: lr `2e-4` (10× a full-FT lr), cosine or linear decay + short warmup,
`per_device_train_batch_size` small + `gradient_accumulation_steps` to reach effective batch,
1–3 epochs (more overfits an SFT set fast), `seed=cfg.seed`, bf16 on Ampere+. `packing=True`
boosts throughput on short samples but interacts with response masking — verify masks again if
you enable it. Checkpoints land in the trainer `output_dir` (adapter-only, small); log them +
the resolved config to the tracker like any run.

## Export — pick by what consumes it
- `model.save_pretrained(dir)` — adapter only (small; base model downloaded at load time).
- `model.save_pretrained_merged(dir, tokenizer, save_method="merged_16bit")` — standalone HF model.
- `model.save_pretrained_gguf(dir, tokenizer, quantization_method="q4_k_m")` — llama.cpp/Ollama.
- **The base model's license carries into every export** — release/redistribution is a
  `governance` → `model-governance` call, not a save-method choice.

## Gotchas
- **Version churn is the defining hazard.** APIs, supported models, and the pinned TRL surface
  shift between releases — hence the pin banner rule; re-run `/skill-update` on every bump.
- **VRAM math before the run:** 4-bit 7–8B ≈ 6–8 GB weights + activations (seq-length dependent);
  `max_seq_length` is the lever when OOM.
- An "it trains but outputs garbage" result is almost always the chat template or the response
  mask, not the hyperparameters — check those first.
