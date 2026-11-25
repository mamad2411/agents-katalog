---
name: tpl-ai-ml-fine-tuning-huggingface
description: Template do pack (ai-ml/04-fine-tuning-huggingface.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/04-fine-tuning-huggingface.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Fine-Tuning with HuggingFace + PEFT (LoRA) + Weights & Biases

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/04-fine-tuning-huggingface.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Language:** Python 3.12
- **Training:** HuggingFace Transformers 4.40+ + PEFT 0.10+ (LoRA/QLoRA)
- **Framework:** PyTorch 2.2+ (CUDA 12.1)
- **Tracking:** Weights & Biases (wandb)
- **Data:** HuggingFace Datasets
- **Quantization:** bitsandbytes (4-bit QLoRA), ONNX + optimum
- **Base Models:** Llama 3 8B / Mistral 7B / Gemma 2B

---

## PROJECT STRUCTURE
```
finetune/
├── config/
│   ├── training_config.yaml    # Hyperparameters
│   └── lora_config.yaml        # LoRA settings per model
├── data/
│   ├── prepare.py              # Dataset preparation + validation
│   ├── format.py               # Prompt formatting per task
│   └── quality_check.py        # Dataset quality filters
├── train.py                    # Training entry point
├── evaluate.py                 # Post-training evaluation
├── inference.py                # Optimized inference
└── export.py                   # ONNX / TensorRT export
```

---

## ARCHITECTURE RULES
1. **Fine-tune vs prompt engineer first** — default to prompt engineering; fine-tune only when prompt fails or cost/latency demands it.
2. **QLoRA for GPU memory** — use 4-bit quantization + LoRA; full fine-tune only with 80GB+ VRAM.
3. **Data quality > data quantity** — 1000 high-quality examples > 100k noisy ones. Filter aggressively.
4. **Evaluation set never leaks into training** — strict 80/10/10 split; no contamination.
5. **Track every experiment in W&B** — run name = `{model}_{task}_{date}_{run_id}`; log config, metrics, artifacts.
6. **Checkpoint every N steps** — save best checkpoint by eval loss, not last checkpoint.
7. **Gradient checkpointing always on** — saves 40-60% VRAM with minimal speed penalty.
8. **Inference uses merged weights or ONNX** — don't load PEFT adapter in production; merge or export.

---

## WHEN TO FINE-TUNE DECISION TABLE
```
Approach         │ When to Use                         │ Cost  │ Latency
─────────────────┼─────────────────────────────────────┼───────┼─────────
Zero-shot        │ General tasks, GPT-5.4 level model   │ Low   │ Medium
Few-shot         │ Consistent output format needed      │ Low   │ Medium
Prompt tuning    │ Want to avoid fine-tune complexity   │ Low   │ Medium
LoRA fine-tune   │ Domain-specific knowledge, style     │ Med   │ Low
QLoRA fine-tune  │ Same but GPU-poor (<= 24GB VRAM)    │ Med   │ Low
Full fine-tune   │ Major behavior change, huge dataset  │ High  │ Low

Fine-tune IS worth it when:
  ✅ Same prompt used 1M+ times/month (API cost exceeds training cost)
  ✅ Output format must be extremely consistent (JSON, SQL)
  ✅ Domain knowledge not in base model (proprietary, recent events)
  ✅ Latency < 100ms needed (self-hosted + ONNX)

Fine-tune is NOT worth it when:
  ❌ You haven't tried 5+ prompt variations first
  ❌ Dataset < 500 examples
  ❌ Task changes frequently (format, instructions)
```

---

## LORA CONFIG SELECTION

```python
# config/lora_config.yaml
# LoRA targets vary by architecture — use these as starting points

# Llama 3 / Mistral (attention + MLP)
lora_config_llama:
  r: 16                     # Rank: 8=conservative, 16=balanced, 64=aggressive
  lora_alpha: 32            # Alpha = 2x rank is a good default
  target_modules:
    - q_proj
    - k_proj
    - v_proj
    - o_proj
    - gate_proj
    - up_proj
    - down_proj
  lora_dropout: 0.05
  bias: none
  task_type: CAUSAL_LM

# Rules for rank selection:
#   r=8:  Minimal task adaptation (style, format)
#   r=16: Standard (classification, structured output)
#   r=32: Complex task learning (domain knowledge injection)
#   r=64: Approaching full fine-tune behavior
```

---

## TRAINING SCRIPT

```python
# train.py
import torch
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    TrainingArguments, BitsAndBytesConfig,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset
import wandb

def train():
    wandb.init(
        project="my-llm-finetune",
        name=f"llama3-8b-lora-r16-{wandb.util.generate_id()}",
        config={
            "model": "meta-llama/Meta-Llama-3-8B",
            "task": "instruction-following",
            "r": 16,
            "epochs": 3,
        }
    )

    # QLoRA: 4-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Meta-Llama-3-8B",
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation="flash_attention_2",  # 2x faster attention
    )
    model = prepare_model_for_kbit_training(model)

    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # LoRA config
    lora_config = LoraConfig(
        r=16,
        lora_alpha=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                         "gate_proj", "up_proj", "down_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()   # Should be ~1-5% of total params

    # Dataset
    dataset = load_dataset("path/to/my_dataset", split="train")
    eval_dataset = load_dataset("path/to/my_dataset", split="validation")

    training_args = TrainingArguments(
        output_dir="./checkpoints",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,      # Effective batch = 16
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        fp16=False,
        bf16=True,                          # Better than fp16 on A100/H100
        gradient_checkpointing=True,
        optim="paged_adamw_32bit",          # Reduced memory optimizer
        evaluation_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        save_total_limit=3,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        logging_steps=10,
        report_to="wandb",
        group_by_length=True,               # Reduces padding waste
        dataloader_num_workers=4,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        dataset_text_field="text",          # Column with formatted prompt
        max_seq_length=2048,
        packing=True,                       # Packs short sequences together
    )

    trainer.train()
    trainer.save_model("./final-adapter")   # Saves only LoRA weights
    wandb.finish()

if __name__ == "__main__":
    train()
```

---

## DATASET PREPARATION

```python
# data/prepare.py
from datasets import Dataset
import json

SYSTEM_PROMPT = "You are a helpful assistant specialized in Python code review."

def format_instruction(example: dict) -> str:
    """Format as Llama 3 chat template."""
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{SYSTEM_PROMPT}<|eot_id|><|start_header_id|>user<|end_header_id|>
{example['instruction']}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
{example['output']}<|eot_id|>"""

def quality_filters(example: dict) -> bool:
    """Filter low-quality examples."""
    instruction = example.get("instruction", "")
    output = example.get("output", "")

    # Minimum length checks
    if len(instruction.split()) < 5 or len(output.split()) < 10:
        return False

    # No truncated outputs
    if output.endswith("...") or output.endswith("etc."):
        return False

    # Max length (avoid sequences > 2048 tokens)
    if len(instruction) + len(output) > 6000:
        return False

    return True

def prepare_dataset(raw_data: list[dict]) -> Dataset:
    dataset = Dataset.from_list(raw_data)

    # Apply quality filters
    before = len(dataset)
    dataset = dataset.filter(quality_filters)
    print(f"Filtered: {before - len(dataset)} examples removed ({len(dataset)} remaining)")

    # Format and add text column
    dataset = dataset.map(
        lambda x: {"text": format_instruction(x)},
        remove_columns=dataset.column_names,
    )

    return dataset.train_test_split(test_size=0.1, seed=42)
```

---

## MERGE AND EXPORT

```python
# export.py — merge LoRA weights into base model for production
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def merge_and_export(base_model_id: str, adapter_path: str, output_dir: str):
    print("Loading base model...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)

    print("Loading LoRA adapter and merging...")
    model = PeftModel.from_pretrained(model, adapter_path)
    model = model.merge_and_unload()    # Merges LoRA weights, removes adapter overhead

    print("Saving merged model...")
    model.save_pretrained(output_dir, safe_serialization=True)
    tokenizer.save_pretrained(output_dir)

    print(f"Merged model saved to {output_dir}")

# Export to ONNX for fast inference
def export_to_onnx(model_dir: str, onnx_dir: str):
    from optimum.onnxruntime import ORTModelForCausalLM
    model = ORTModelForCausalLM.from_pretrained(model_dir, export=True)
    model.save_pretrained(onnx_dir)
```

---

## EVALUATION METRICS
```
Task Type    │ Primary Metric       │ Secondary
─────────────┼──────────────────────┼──────────────────
Classification│ F1 / Accuracy        │ Confusion matrix
Summarization │ ROUGE-L             │ BERTScore
Code gen      │ Pass@k (execution)   │ CodeBLEU
Extraction    │ Exact Match / F1     │ Character F1
Instruction   │ LLM-as-Judge (0-10)  │ Human eval %
```

---

## QUANTIZATION FOR INFERENCE

```python
# Load quantized model for fast inference (4-bit, no training)
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_4bit = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    "./merged-model",
    quantization_config=bnb_4bit,
    device_map="auto",
)

# Benchmark: Llama 3 8B in 4-bit ≈ 5GB VRAM, ~30 tokens/sec on RTX 3090
```
