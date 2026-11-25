---
name: "llm-tuning-patterns"
description: "LLM fine-tuning patterns with code: QLoRA with SFTTrainer, LoRA configuration choices, instruction dataset preparation, DPO preference training, adapter merging and export, and lm-evaluation-harness runs. Use when fine-tuning or aligning an LLM."
---

# LLM Tuning Patterns

Expert patterns for LoRA, QLoRA, instruction dataset preparation, DPO, and evaluation.

## Pattern 1: QLoRA Fine-Tuning with SFTTrainer

Complete QLoRA setup for instruction fine-tuning a 7B model on 24 GB VRAM.

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset
import torch

# 1. Load model in 4-bit
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True,
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"  # required for SFT with causal LM

# 2. Prepare model for k-bit training (enables gradient checkpointing for 4-bit)
model = prepare_model_for_kbit_training(model)

# 3. Configure LoRA
lora_config = LoraConfig(
    r=16,                           # rank
    lora_alpha=32,                  # scaling: effective_lr ∝ alpha/r
    target_modules=[                # all linear layers for maximum adaptation
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Trainable params: ~42M (0.6% of 7B)

# 4. Dataset in instruction format
dataset = load_dataset("json", data_files="train_instructions.jsonl")["train"]

def format_instruction(example):
    return f"""### Instruction:
{example['instruction']}

### Input:
{example.get('input', '')}

### Response:
{example['output']}{tokenizer.eos_token}"""

# 5. SFTTrainer handles tokenization, packing, and LoRA
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./qlora-llama2-7b",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # effective batch = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    bf16=True,
    logging_steps=10,
    save_steps=100,
    save_total_limit=3,
    gradient_checkpointing=True,    # trade compute for memory
    optim="paged_adamw_32bit",      # paged optimizer states for memory savings
)

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=dataset,
    formatting_func=format_instruction,
    max_seq_length=2048,
    packing=True,   # pack multiple short examples into one sequence for efficiency
)

trainer.train()
trainer.save_model()  # saves adapter weights only
```

## Pattern 2: LoRA Configuration Choices

Select rank and target modules based on task requirements.

```python
from peft import LoraConfig

# Minimal: only attention, very few params (good for few-shot style tuning)
minimal_lora = LoraConfig(
    r=4,
    lora_alpha=8,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

# Standard: attention + up/down projections
standard_lora = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "up_proj", "down_proj"],
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

# Full: all linear layers — maximum adaptation capacity
full_lora = LoraConfig(
    r=64,
    lora_alpha=128,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.1,
    task_type="CAUSAL_LM",
)

# Guidelines:
# r=4-8: style transfer, few-shot behavior injection
# r=16: standard task fine-tuning (classification, summarization)
# r=32-64: domain adaptation, significant behavioral change
# Increase rank if training loss plateaus early and val metrics don't improve
```

## Pattern 3: Dataset Preparation for Instruction Tuning

Format data correctly and mask user/system tokens.

```python
from datasets import Dataset
import json

def prepare_instruction_dataset(raw_data: list) -> Dataset:
    """
    Convert raw data to ChatML format with correct label masking.
    Labels for user/system turns = -100 (ignored in cross-entropy loss).
    """
    formatted = []
    for item in raw_data:
        # ChatML format
        conversation = (
            f"<|im_start|>system\n{item.get('system', 'You are a helpful assistant.')}<|im_end|>\n"
            f"<|im_start|>user\n{item['user']}<|im_end|>\n"
            f"<|im_start|>assistant\n{item['assistant']}<|im_end|>"
        )
        formatted.append({"text": conversation})
    return Dataset.from_list(formatted)

def tokenize_with_masking(examples, tokenizer, max_length=2048):
    """Tokenize and create label mask: -100 for user/system, token_id for assistant."""
    result = {"input_ids": [], "attention_mask": [], "labels": []}

    for text in examples["text"]:
        tokens = tokenizer(text, max_length=max_length, truncation=True, padding=False)
        input_ids = tokens["input_ids"]

        # Find assistant response start
        assistant_token = tokenizer.encode("<|im_start|>assistant\n", add_special_tokens=False)
        labels = [-100] * len(input_ids)

        # Find where assistant response starts
        for i in range(len(input_ids) - len(assistant_token)):
            if input_ids[i:i+len(assistant_token)] == assistant_token:
                # Unmask from assistant content onwards
                start = i + len(assistant_token)
                for j in range(start, len(input_ids)):
                    labels[j] = input_ids[j]
                break

        result["input_ids"].append(input_ids)
        result["attention_mask"].append(tokens["attention_mask"])
        result["labels"].append(labels)

    return result

# Validate dataset quality
def validate_dataset(dataset, tokenizer, n_samples: int = 5):
    print(f"Dataset size: {len(dataset)}")
    token_lengths = [len(tokenizer.encode(x['text'])) for x in dataset.select(range(100))]
    print(f"Token length (100 samples): mean={sum(token_lengths)/len(token_lengths):.0f}, max={max(token_lengths)}")

    # Check label masking
    for i in range(n_samples):
        ex = dataset[i]
        unmasked = sum(1 for l in ex.get('labels', []) if l != -100)
        total = len(ex.get('input_ids', []))
        print(f"Sample {i}: {unmasked}/{total} tokens unmasked ({unmasked/total*100:.1f}% trained on)")
```

## Pattern 4: DPO Training for Preference Alignment

Direct Preference Optimization — simpler than PPO, no reward model required.

```python
from trl import DPOTrainer, DPOConfig
from datasets import Dataset

# DPO dataset format
preference_data = [
    {
        "prompt": "Explain quantum entanglement",
        "chosen": "Quantum entanglement is a phenomenon where two particles become correlated...",
        "rejected": "It's when particles are connected or something, like magic"
    },
    # ... more preference pairs
]

dpo_dataset = Dataset.from_list(preference_data)

# DPO config
dpo_config = DPOConfig(
    beta=0.1,              # KL penalty coefficient. Higher = stay closer to reference
    max_length=1024,
    max_prompt_length=512,
    output_dir="./dpo-model",
    num_train_epochs=1,    # DPO typically needs only 1 epoch
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=5e-7,    # much lower than SFT
    bf16=True,
    logging_steps=10,
)

# DPOTrainer automatically uses the SFT model as the reference model
trainer = DPOTrainer(
    model=sft_model,               # fine-tuned SFT model as starting point
    ref_model=None,                # None = copy of model used as reference
    args=dpo_config,
    train_dataset=dpo_dataset,
    tokenizer=tokenizer,
)

trainer.train()

# DPO loss components (for monitoring):
# rewards/chosen: log probability of chosen under policy vs reference (should be positive)
# rewards/rejected: should be negative
# rewards/margins: chosen - rejected (maximize this)
```

## Pattern 5: Adapter Merging and Export

Merge LoRA weights into base model for deployment without adapter overhead.

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load base model in FP16 (not quantized — quantization prevents merging)
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    torch_dtype=torch.float16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

# Load LoRA adapter
model = PeftModel.from_pretrained(base_model, "./qlora-llama2-7b")

# Merge and unload: folds A×B into base weights
merged_model = model.merge_and_unload()

# Save merged model (full model weights, adapter-free inference)
merged_model.save_pretrained("./merged-llama2-7b-ft", safe_serialization=True)
tokenizer.save_pretrained("./merged-llama2-7b-ft")

# Verify
from transformers import pipeline
pipe = pipeline("text-generation", model="./merged-llama2-7b-ft", torch_dtype=torch.float16)
output = pipe("### Instruction:\nSummarize this text.\n\n### Response:\n", max_new_tokens=200)
print(output[0]["generated_text"])
```

## Pattern 6: Evaluation with lm-evaluation-harness

Run standardized benchmarks on fine-tuned models.

```bash
# Install EleutherAI eval harness
pip install lm-eval

# Evaluate on MMLU and HellaSwag
lm_eval --model hf \
  --model_args pretrained=./merged-llama2-7b-ft,dtype=float16 \
  --tasks mmlu,hellaswag,arc_easy,arc_challenge,truthfulqa_mc1 \
  --device cuda \
  --batch_size 8 \
  --output_path ./eval_results.json

# Custom evaluation loop
python - << 'EOF'
import json
from transformers import pipeline

pipe = pipeline("text-generation", model="./merged-llama2-7b-ft",
                torch_dtype="auto", device_map="auto")

def evaluate_custom(test_cases: list) -> dict:
    correct = 0
    for case in test_cases:
        output = pipe(
            case["prompt"],
            max_new_tokens=100,
            temperature=0.0,
            do_sample=False,
        )[0]["generated_text"]
        # Extract and compare answer
        if case["expected"].lower() in output.lower():
            correct += 1
    return {"accuracy": correct / len(test_cases), "n": len(test_cases)}
EOF
```

## Anti-Patterns

### Anti-Pattern 1: Training on User Turns
Forgetting to mask user/system tokens with -100 trains the model to predict user messages, wasting compute and degrading instruction following. Always verify that only assistant tokens have valid labels.

### Anti-Pattern 2: Too High LoRA Rank for Small Datasets
High rank (r=64) with < 1000 examples overfits quickly. Match rank to dataset size: small dataset → small rank. Monitor train vs eval loss for divergence.

### Anti-Pattern 3: No EOS Token in Training Data
Without EOS tokens, the model doesn't learn where responses end and generates indefinitely in production. Every training example must end with the tokenizer's EOS token.

### Anti-Pattern 4: DPO on Low-Quality Preference Pairs
DPO is only as good as the quality of (chosen, rejected) pairs. Preference pairs where both responses are bad, or where the distinction is subtle grammar rather than correctness, produce poorly aligned models. Curate preference data carefully.

### Anti-Pattern 5: Merging Quantized Adapters
You cannot merge LoRA adapters trained on a 4-bit quantized model into that quantized base. Merging requires the base model in FP16/BF16. Load base in full precision, then merge. Training can use quantization; deployment merge cannot.
