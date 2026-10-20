---
name: "nlp-pipelines"
description: "Building NLP systems end to end — text preprocessing, fine-tuning transformer models, named entity recognition (NER), text classification, sentimen..."
---

# NLP Pipelines

## When to activate
Building NLP systems end to end — text preprocessing, fine-tuning transformer models, named entity recognition (NER), text classification, sentiment analysis, multilingual models, or serving NLP inference. Use this when the task involves Hugging Face Transformers, tokenization design, BIO tagging, or deploying NLP models to production.

## When NOT to use
Pure retrieval-augmented generation or embedding search (those are covered in AI engineering skills). Image/audio classification that happens to output text. Prompt engineering for LLM chat applications. Simple regex-based text processing that does not require a learned model.

## Instructions

### Text Preprocessing

Normalize before tokenizing to reduce vocabulary fragmentation:

```python
import unicodedata
import re

def normalize_text(text: str) -> str:
    # NFC normalization handles accented chars, lookalike unicode
    text = unicodedata.normalize("NFC", text)
    # Collapse whitespace variants
    text = re.sub(r"\s+", " ", text).strip()
    # Remove control characters (keep newlines for document structure)
    text = "".join(c for c in text if unicodedata.category(c)[0] != "C" or c == "\n")
    return text
```

BPE and WordPiece tokenizers (used by RoBERTa and BERT respectively) handle subwords automatically — do not manually stem or lemmatize before passing text to a transformer tokenizer. Stemming breaks subword alignment.

### Fine-Tuning with Hugging Face Trainer API

For classification, use `AutoModelForSequenceClassification` with the correct `num_labels`:

```python
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
from datasets import load_dataset
import evaluate
import numpy as np

MODEL_ID = "xlm-roberta-base"
NUM_LABELS = 3  # positive, neutral, negative

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_ID, num_labels=NUM_LABELS
)

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, max_length=512)

dataset = load_dataset("csv", data_files={"train": "train.csv", "validation": "val.csv"})
tokenized = dataset.map(tokenize, batched=True)

f1_metric = evaluate.load("f1")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    return f1_metric.compute(predictions=preds, references=labels, average="macro")

args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    lr_scheduler_type="cosine",
    warmup_ratio=0.06,
    gradient_accumulation_steps=2,   # effective batch = 32
    fp16=True,
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="f1",
    report_to="mlflow",
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["validation"],
    tokenizer=tokenizer,
    data_collator=DataCollatorWithPadding(tokenizer),
    compute_metrics=compute_metrics,
)
trainer.train()
```

**Learning rate schedule**: use cosine with warmup (`warmup_ratio=0.06`). Linear warmup prevents the early loss spikes from large initial gradient norms on the freshly initialized classification head.

**Gradient accumulation**: when GPU memory limits batch size, accumulate gradients across N steps to simulate a larger effective batch. Larger effective batch generally stabilizes fine-tuning.

### NER with BIO Tagging

BIO (Beginning / Inside / Outside) is the standard tagging scheme. Each token gets one label:

```
Token:  "Apple   Inc.    announced   a    new   iPhone"
Label:  B-ORG   I-ORG   O           O    O     B-PROD
```

Use `AutoModelForTokenClassification` and align labels to subword tokens (only label the first subword of each word):

```python
from transformers import AutoModelForTokenClassification

label2id = {"O": 0, "B-ORG": 1, "I-ORG": 2, "B-PER": 3, "I-PER": 4, "B-LOC": 5, "I-LOC": 6}

def align_labels(examples):
    tokenized = tokenizer(examples["tokens"], truncation=True,
                          is_split_into_words=True, max_length=512)
    labels_out = []
    for i, label_seq in enumerate(examples["ner_tags"]):
        word_ids = tokenized.word_ids(batch_index=i)
        prev_word_id = None
        label_ids = []
        for word_id in word_ids:
            if word_id is None:
                label_ids.append(-100)  # special tokens ignored in loss
            elif word_id != prev_word_id:
                label_ids.append(label_seq[word_id])
            else:
                label_ids.append(-100)  # subword continuation — ignore
            prev_word_id = word_id
        labels_out.append(label_ids)
    tokenized["labels"] = labels_out
    return tokenized
```

Use `seqeval` for NER evaluation — it computes span-level F1, not token-level:

```python
seqeval = evaluate.load("seqeval")

def compute_ner_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=-1)
    true_labels = [[id2label[l] for l in label_row if l != -100]
                   for label_row in labels]
    true_preds = [[id2label[p] for p, l in zip(pred_row, label_row) if l != -100]
                  for pred_row, label_row in zip(preds, labels)]
    return seqeval.compute(predictions=true_preds, references=true_labels)
```

### Evaluation: Macro vs Micro F1

Use **macro-F1** for imbalanced datasets (most NLP classification tasks). Macro averages F1 per class equally regardless of support, so rare classes are not drowned out by the majority class. Micro-F1 is dominated by the largest class and is misleading when class distribution is skewed.

```python
# Macro — equal weight per class
f1_macro = f1_score(y_true, y_pred, average="macro")

# Micro — global TP/FP/FN, dominated by frequent classes
f1_micro = f1_score(y_true, y_pred, average="micro")
```

Report both in model cards; gate CI on macro-F1.

### Multilingual: XLM-R vs mBERT

Prefer XLM-R (`xlm-roberta-base` or `xlm-roberta-large`) over mBERT for most multilingual tasks. XLM-R was trained on more data (100 languages, Common Crawl), uses SentencePiece BPE (better low-resource tokenization), and consistently outperforms mBERT on XNLI, NER, and QA benchmarks. Use mBERT only if you have an existing checkpoint or strict size constraints.

Zero-shot cross-lingual transfer: fine-tune on English only, evaluate on target languages. Works reasonably well for classification and NER with XLM-R, often exceeding 80% of supervised performance on closely related languages.

### ONNX Export and INT8 Quantization

```python
from optimum.exporters.onnx import main_export

# Export with Optimum (handles dynamic axes, pooling, classification head)
main_export(
    model_name_or_path="./checkpoints/best",
    output="./onnx",
    task="text-classification",
    opset=17,
)

# INT8 quantization — halves model size, ~2x faster on CPU
from optimum.onnxruntime import ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig

quantizer = ORTQuantizer.from_pretrained("./onnx")
qconfig = AutoQuantizationConfig.avx512_vnni(is_static=False, per_channel=False)
quantizer.quantize(save_dir="./onnx_int8", quantization_config=qconfig)
```

### FastAPI Serving with Async Batching

Load tokenizer and ONNX session at startup; use a queue to batch concurrent requests:

```python
from fastapi import FastAPI
from contextlib import asynccontextmanager
import onnxruntime as ort
from transformers import AutoTokenizer
import asyncio, numpy as np

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
    app.state.session = ort.InferenceSession(
        "onnx_int8/model.onnx",
        providers=["CPUExecutionProvider"],
    )
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/classify")
async def classify(texts: list[str]):
    enc = app.state.tokenizer(
        texts,
        return_tensors="np",
        padding=True,
        truncation=True,
        max_length=512,
    )
    logits = app.state.session.run(
        ["logits"],
        {"input_ids": enc["input_ids"], "attention_mask": enc["attention_mask"]},
    )[0]
    preds = np.argmax(logits, axis=-1).tolist()
    return {"predictions": preds}
```

## Example

Fine-tune XLM-R for 3-class multilingual sentiment classification (positive / neutral / negative):

1. Normalize and tokenize with `xlm-roberta-base` tokenizer, truncate to 512 tokens.
2. Train with Trainer API using cosine LR schedule, `warmup_ratio=0.06`, `gradient_accumulation_steps=2`, `fp16=True`, 4 epochs.
3. Evaluate on validation set — report macro-F1 (target ≥ 0.82) and per-class F1. Gate CI on macro-F1.
4. Export to ONNX with Optimum, apply INT8 dynamic quantization.
5. Benchmark: assert p99 latency < 150ms on a batch of 32 sentences.
6. Serve behind FastAPI with tokenizer and ORT session loaded once at startup.

Zero-shot cross-lingual: after fine-tuning on English data only, evaluate on French and German test sets to confirm transfer (XLM-R typically retains 85%+ of English F1 on closely related European languages).

---
