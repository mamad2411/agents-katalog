---
name: huggingface-patterns
description: "When to activate: HuggingFace, Transformers, PEFT, LoRA, QLoRA, fine-tuning, Trainer API, datasets library, tokenizers, inference, model hub"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: ml-ai
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# HuggingFace Transformers Patterns

## Inference Pipeline

```python
from transformers import pipeline

# Zero-shot classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
result = classifier(
    "This product broke after one week",
    candidate_labels=["positive", "negative", "neutral"],
)

# Text generation
generator = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.2",
                     device_map="auto", torch_dtype="auto")
output = generator("Explain attention mechanisms:", max_new_tokens=200, do_sample=True, temperature=0.7)

# NER
ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
entities = ner("Apple Inc. was founded by Steve Jobs in Cupertino.")
```

## Fine-tuning with Trainer API

```python
from transformers import (
    AutoModelForSequenceClassification, AutoTokenizer,
    TrainingArguments, Trainer
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, f1_score

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

dataset = load_dataset("imdb")

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, max_length=512, padding="max_length")

tokenized = dataset.map(tokenize, batched=True)
tokenized = tokenized.rename_column("label", "labels")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return {"accuracy": accuracy_score(labels, preds), "f1": f1_score(labels, preds)}

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    warmup_ratio=0.1,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    fp16=True,
    report_to="mlflow",
)

trainer = Trainer(
    model=model, args=training_args,
    train_dataset=tokenized["train"], eval_dataset=tokenized["test"],
    compute_metrics=compute_metrics,
)
trainer.train()
```

## LoRA Fine-tuning with PEFT

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

# QLoRA — quantized + LoRA (fits 7B on single GPU)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    quantization_config=bnb_config,
    device_map="auto",
)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,               # LoRA rank
    lora_alpha=32,      # Scaling factor
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 20,971,520 || all params: 3,773,952,000 || trainable%: 0.56%

# Merge and export after training
merged_model = model.merge_and_unload()
merged_model.save_pretrained("fine-tuned-mistral")
```

## Datasets Library

```python
from datasets import Dataset, DatasetDict, load_dataset
import pandas as pd

# From pandas
df = pd.read_csv("training_data.csv")
dataset = Dataset.from_pandas(df)

# Map transformation
def format_prompt(example):
    return {
        "text": f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"
    }

dataset = dataset.map(format_prompt, remove_columns=["instruction", "response"])

# Train/test split
splits = dataset.train_test_split(test_size=0.1, seed=42)
dataset_dict = DatasetDict({"train": splits["train"], "test": splits["test"]})

# Push to Hub
dataset_dict.push_to_hub("myorg/my-dataset", private=True)

# Stream large datasets
stream_dataset = load_dataset("wikipedia", "20220301.en", streaming=True)
for sample in stream_dataset["train"].take(10):
    print(sample["text"][:100])
```

## Tokenizer Patterns

```python
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

# Chat template formatting
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is RAG?"},
]
formatted = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Token count
tokens = tokenizer(long_text, return_tensors="pt")
print(f"Token count: {tokens.input_ids.shape[1]}")

# Batch tokenization with padding
batch = tokenizer(
    texts, padding=True, truncation=True,
    max_length=512, return_tensors="pt"
)
```
