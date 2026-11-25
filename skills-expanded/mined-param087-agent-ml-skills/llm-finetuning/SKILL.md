---
name: llm-finetuning
description: Use when fine-tuning a large language model. Covers choosing full vs LoRA/QLoRA, dataset formatting, the transformers/PEFT/TRL stack, key hyperparameters, and evaluating fine-tunes without overfitting.
---

# LLM Fine-Tuning

## Overview

Fine-tuning adapts a base LLM to a task or style. For almost all practitioners the right default is **parameter-efficient fine-tuning (LoRA/QLoRA)** — it trains <1% of weights, fits on a single GPU, and avoids catastrophic forgetting. Reach for full fine-tuning only with strong justification and budget.

## When to use

- A base/instruct model is close but needs domain style, format, or behavior.
- You have a few hundred to tens of thousands of quality examples.

## First decide: do you even need to fine-tune?

Try **prompting + few-shot + RAG** first (see the `rag-pipeline` skill). Fine-tune when you need consistent format/style, lower latency/cost than long prompts, or to internalize a large example set.

## Method selection

| Method | Trains | VRAM | Use when |
|--------|--------|------|----------|
| Full FT | 100% | Very high | Large data + budget, max quality |
| **LoRA** | ~0.1-1% | Moderate | Default for most tasks |
| **QLoRA** | ~0.1-1% | Low (4-bit) | Single consumer GPU |

## Dataset formatting (chat / instruction)

Use the model's chat template; quality > quantity. A few thousand clean, diverse examples beat a noisy 100k dump.

```python
def to_chat(example):
    return {"messages": [
        {"role": "system", "content": "You are a helpful support agent."},
        {"role": "user", "content": example["question"]},
        {"role": "assistant", "content": example["answer"]},
    ]}
```

## QLoRA with TRL

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig
import torch

bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(BASE, quantization_config=bnb, device_map="auto")

peft_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, bias="none",
                      task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])

trainer = SFTTrainer(
    model=model, train_dataset=train_ds, eval_dataset=eval_ds, peft_config=peft_cfg,
    args=SFTConfig(per_device_train_batch_size=2, gradient_accumulation_steps=8,
                   learning_rate=2e-4, num_train_epochs=2, warmup_ratio=0.03,
                   lr_scheduler_type="cosine", bf16=True, logging_steps=10,
                   eval_strategy="steps", eval_steps=100, output_dir="out"),
)
trainer.train()
```

## Key hyperparameters

- **LR:** 1e-4 to 3e-4 for LoRA (higher than full FT).
- **Epochs:** 1-3 — more overfits and degrades general ability.
- **LoRA rank `r`:** 8-32 typical; raise for harder tasks.
- **Effective batch:** use gradient accumulation to reach 16-32.

## Evaluating a fine-tune

- Hold out a real test set; track eval loss for overfitting.
- Judge on **task metrics** (exact match, rubric/LLM-judge), not just loss.
- Check for **regression** on general benchmarks — fine-tuning can break unrelated abilities.

## Pitfalls

- Too many epochs / LR too high → overfit, repetitive or degenerate outputs.
- Wrong chat template → the model learns malformed formatting.
- Tiny/dirty dataset → memorization, not generalization.
- Skipping a base-model baseline → you can't prove the fine-tune helped.

## Hand-off

Merged or adapter weights + eval report, logged via experiment-tracking and deployed via model-serving.
