---
name: ai-science-llm-finetuning
description: Fine-tune LLMs (Mistral/Llama/Qwen) with LoRA/QLoRA via HuggingFace PEFT, bitsandbytes NF4, and trl SFTTrainer. Use when doing LoRA/QLoRA fine-tuning, PEFT, instruction tuning, or SFTTrainer on limited GPU memory.
tool_type: python
primary_tool: peft
---

# LLM Fine-tuning (LoRA / QLoRA)

## When to Use

- Adapting a base or instruct LLM (Mistral, Llama, Qwen) to a domain task — e.g. biomedical Q&A, clinical note summarization, literature mining — without full fine-tuning.
- GPU memory is limited (single T4/A10/consumer GPU) and full fine-tuning of a 7B+ model is infeasible.
- Need to build/format an instruction dataset (chat templates) and run `trl`'s `SFTTrainer`.
- Deciding LoRA rank, target modules, or quantization precision (NF4 vs INT8 vs bf16).
- Debugging silent garbage output from a fine-tuned model (usually a chat-template mismatch).

## Version Compatibility

- `transformers` ≥ 4.40, `peft` ≥ 0.10, `trl` ≥ 0.9, `bitsandbytes` ≥ 0.43, `accelerate` ≥ 0.30, Python ≥ 3.10, CUDA GPU required for training (T4 sufficient for 7B in 4-bit).
- `trl`'s `SFTTrainer`/`SFTConfig` API has churned across versions — `dataset_text_field`, `max_seq_length`, and `packing` moved from `SFTTrainer.__init__` into a separate `SFTConfig` object in `trl` ≥ 0.9. Check `trl.__version__` and pass those args via `SFTConfig` on recent versions instead of directly to `SFTTrainer`.

## Prerequisites

- `pip install transformers peft trl bitsandbytes accelerate datasets`
- Familiarity with PyTorch and transformer architecture (attention projections `q_proj`/`k_proj`/`v_proj`/`o_proj`).
- A HuggingFace Hub token if the base model is gated (e.g. Llama).

## LoRA: Parameter Math

Full fine-tuning updates every entry of `W` (d×k). LoRA instead learns two small matrices and computes the update as their product:

$$\Delta W = B \cdot A, \quad B \in \mathbb{R}^{d \times r}, \; A \in \mathbb{R}^{r \times k}$$

At inference: `W_eff = W_pretrained + (alpha/r) * B @ A`. Trainable parameters scale with `r*(d+k)` instead of `d*k`.

| Model | Full FT params | LoRA r=16 | Reduction |
|---|---|---|---|
| 7B (Mistral/Llama) | 7,000,000,000 | ~6,800,000 | ~1000x |
| 13B | 13,000,000,000 | ~12,600,000 | ~1000x |

**Modules to target:** minimum `q_proj`, `v_proj`; recommended + `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`.

**Goal:** estimate trainable-parameter count for a given LoRA rank before committing GPU hours.
**Approach:** sum `2 * rank * model_dim` (A + B matrices) per targeted projection, times number of layers.

```python
def lora_param_count(model_dim, n_layers, rank, target_modules):
    """Estimate LoRA trainable parameter count for a transformer.

    model_dim: hidden size (e.g. 4096 for a 7B model)
    n_layers: number of transformer layers
    rank: LoRA rank r
    target_modules: list of projection names LoRA is applied to
    """
    params_per_layer = 2 * rank * model_dim * len(target_modules)  # A + B per module
    return params_per_layer * n_layers

total_params = 7_000_000_000  # Mistral-7B architecture: model_dim=4096, n_layers=32
for rank in (8, 16, 32, 64):
    lora_p = lora_param_count(4096, 32, rank, ["q_proj", "v_proj", "k_proj", "o_proj"])
    print(f"r={rank:3d}: {lora_p:>12,} trainable params ({lora_p / total_params * 100:.3f}% of 7B)")
```

## Quantization: 4-bit NF4 (QLoRA)

NF4 (NormalFloat 4-bit) quantizes the frozen base model weights; LoRA adapter weights stay in bfloat16 — these are separate concerns, and only the adapters receive gradient updates.

| Format | Bits | 7B model memory | Quality |
|---|---|---|---|
| float32 | 32 | 28 GB | Reference |
| bfloat16 | 16 | 14 GB | ~same |
| INT8 | 8 | 7 GB | Small loss |
| NF4 | 4 | 3.5 GB | Small loss |

**Goal:** load a 7B model in 4-bit and attach trainable LoRA adapters (QLoRA).
**Approach:** `BitsAndBytesConfig` for the frozen base, `LoraConfig` + `get_peft_model` for the trainable adapters.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, TaskType
import torch

MODEL_NAME = "mistralai/Mistral-7B-v0.1"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",              # NormalFloat 4-bit
    bnb_4bit_compute_dtype=torch.bfloat16,  # compute (forward/backward) in bf16
    bnb_4bit_use_double_quant=True,         # extra memory savings
)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME, quantization_config=bnb_config, device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token  # required: most base models have no pad token

lora_cfg = LoraConfig(
    r=16, lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05, bias="none", task_type=TaskType.CAUSAL_LM,
)
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()
```

## Chat Templates

Instruction-tuned models expect a specific prompt format; the wrong one causes silent garbage, not an error.

```python
def format_mistral(system, user, assistant=None):
    """Mistral/Llama-2-Instruct [INST] template."""
    prompt = f"[INST] <<SYS>>\n{system}\n<</SYS>>\n\n{user} [/INST]"
    if assistant:
        prompt += f" {assistant}</s>"
    return prompt

def format_alpaca(instruction, input_text="", output=""):
    """Alpaca instruction/input/response template."""
    prompt = f"### Instruction:\n{instruction}\n"
    if input_text:
        prompt += f"\n### Input:\n{input_text}\n"
    return prompt + f"\n### Response:\n{output}"

def format_chatml(system, user, assistant=None):
    """ChatML (OpenAI-compatible) template used by Qwen, many fine-tunes."""
    prompt = f"<|im_start|>system\n{system}<|im_end|>\n"
    prompt += f"<|im_start|>user\n{user}<|im_end|>\n<|im_start|>assistant\n"
    if assistant:
        prompt += f"{assistant}<|im_end|>"
    return prompt
```

## Dataset Preparation and SFTTrainer Workflow

**Goal:** turn (instruction, response) pairs into a `datasets.Dataset` with a formatted `text` field, then fine-tune with `trl.SFTTrainer`.
**Approach:** format each record with the model's chat template, wrap in `Dataset.from_list`, configure LoRA + `SFTConfig`, train.

```python
from transformers import TrainingArguments  # pip install trl peft bitsandbytes transformers accelerate datasets
from trl import SFTTrainer, SFTConfig  # SFTConfig required on trl >= 0.9
from datasets import Dataset

def build_sft_dataset(qa_pairs, formatter):
    """Format (instruction, response) dicts into a text-field Dataset.

    qa_pairs: list of {"instruction": str, "response": str}
    formatter: e.g. format_alpaca
    """
    records = [
        {**qa, "text": formatter(qa["instruction"], output=qa["response"])}
        for qa in qa_pairs
    ]
    return Dataset.from_list(records)

bio_qa = [
    {"instruction": "What is the purpose of PCR duplicate marking in NGS pipelines?",
     "response": "It prevents double-counting the same DNA fragment in variant calling and "
                 "expression quantification, which would inflate confidence in erroneous calls."},
]
dataset = build_sft_dataset(bio_qa, format_alpaca)

sft_config = SFTConfig(
    output_dir="./results", num_train_epochs=2,
    per_device_train_batch_size=2, gradient_accumulation_steps=4,
    learning_rate=2e-4, logging_steps=10, gradient_checkpointing=True,
    dataset_text_field="text", max_seq_length=2048, packing=False,
)
trainer = SFTTrainer(model=model, args=sft_config, train_dataset=dataset, tokenizer=tokenizer)
trainer.train()
trainer.model.save_pretrained("./bio_assistant")
```

## Dataset Quality Rules

| Rule | Detail |
|---|---|
| Quality > quantity | 500 curated examples > 10k noisy ones |
| Diversity | Cover all task types the model should handle |
| Format consistency | One chat template throughout |
| No contamination | Hold out the test set before generating training data |

## Pitfalls

- **LoRA rank vs quality**: higher rank (r=64) trains more parameters but is not always better — r=16 is the strong default; benefit depends on dataset size and task diversity.
- **Quantization != adapter precision**: NF4 quantizes the frozen base model weights; LoRA adapter weights stay in bfloat16. Separate concerns — don't confuse them.
- **Chat template mismatch**: loading a model with the wrong chat template causes silent garbage outputs, not errors. Always verify the template against the model card.
- **Overfitting on small datasets**: <500 examples -> 1-2 epochs. Watch eval loss; if it rises while train loss falls, stop early.
- **Missing pad token**: most base models (Mistral, Llama) have no pad token. Set `tokenizer.pad_token = tokenizer.eos_token`.
- **`trl` API drift**: `dataset_text_field`/`max_seq_length`/`packing` live on `SFTConfig`, not `SFTTrainer`, in newer `trl` releases — check `trl.__version__` before copying old tutorial code.

## See Also

- `ai-science-llm-training-systems` — experiment tracking, ablation design, and run registries for these fine-tuning jobs.
- `ai-science-genomic-llms` — genomic (DNA-sequence) foundation models rather than natural-language LLMs.
- `transformers` — general HuggingFace `transformers` usage beyond fine-tuning.
- `huggingface-lora-space-builder` — packaging a fine-tuned LoRA adapter as a hosted demo.
