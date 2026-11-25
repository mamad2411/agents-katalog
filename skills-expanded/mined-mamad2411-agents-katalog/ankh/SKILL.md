---
name: ankh
description: >
  Generate protein embeddings with Ankh models or complete protein sequences with Ankh3. 
  Covers ankh-base, ankh-large, ankh3-large, and ankh3-xl via HuggingFace transformers 
  (T5EncoderModel / T5ForConditionalGeneration). Use even when the user asks broadly for 
  "protein representations" or "T5 protein model" without naming Ankh explicitly.
  Do not use for Ankh fine-tuning or model selection — see model-selection
  for those tasks.
compatibility: transformers ≥4.30, torch ≥2.0. Optional: pip install ankh (thin wrapper around transformers, not mandatory).
---

# Ankh Inference

For model choice and fine-tuning strategy, see the model-selection skill.

---

## Model variants

| Model | HuggingFace ID | Notes |
|---|---|---|
| ankh-base | `ElnaggarLab/ankh-base` | ~450 M params. Lighter; fast on CPU / small GPU. No prefix tokens. |
| ankh-large | `ElnaggarLab/ankh-large` | ~1.2 B params. Best quality pre-Ankh3. No prefix tokens. |
| ankh3-large | `ElnaggarLab/ankh3-large` | MLM + seq-completion training. Requires `[NLU]` or `[S2S]` prefix. |
| ankh3-xl | `ElnaggarLab/ankh3-xl` | Highest quality. Requires `[NLU]` or `[S2S]` prefix. |

---

## When to use / When NOT to use

| Use this skill | Use model-selection instead |
|---|---|
| Ankh3 sequence completion (generate second half from first) | LoRA or full fine-tuning setup |
| Producing residue-level or sequence-level representations | Prediction heads and training loops |

---

## Package table

| Use case | Package | Install |
|---|---|---|
| All Ankh variants via HuggingFace | **transformers** (preferred) | `pip install transformers` |
| ankh-base / ankh-large convenience loaders | **ankh** | `pip install ankh` |

---

## ankh-base / ankh-large — HuggingFace (recommended)

```python
import torch
from transformers import T5Tokenizer, T5EncoderModel

device = "cuda" if torch.cuda.is_available() else "cpu"

# Must use T5Tokenizer — AutoTokenizer resolves to a different class for these checkpoints.
tokenizer = T5Tokenizer.from_pretrained("ElnaggarLab/ankh-base")
model = T5EncoderModel.from_pretrained("ElnaggarLab/ankh-base").eval().to(device)

inputs = tokenizer(
    sequences,                  # list[str]
    return_tensors="pt",
    padding=True,
    truncation=True,
    add_special_tokens=True,
)
inputs = {k: v.to(device) for k, v in inputs.items()}

with torch.no_grad():
    outputs = model(**inputs)

# Mean-pool over attended positions (attention_mask handles padding).
hidden = outputs.last_hidden_state                        # (B, L, D)
mask   = inputs["attention_mask"].unsqueeze(-1).float()   # (B, L, 1)
pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1.0)  # (B, D)
```

Replace `"ElnaggarLab/ankh-base"` with `"ElnaggarLab/ankh-large"` for the larger variant.

---

## ankh-base / ankh-large — ankh package

```python
import ankh, torch

model, tokenizer = ankh.load_base_model()   # or ankh.load_large_model()
model = model.eval().to(device)

# tokenizer returns ids; use the same mean-pool recipe above.
```

Use the `ankh` package only when you also need its downstream classification heads.
For standalone embeddings, the HuggingFace path above is preferred.

---

## Ankh3 — embeddings (NLU prefix)

Ankh3 requires a task prefix prepended to every sequence **before tokenization**.
Use `[NLU]` for embedding extraction; `[S2S]` is an alternative that can sometimes
improve embedding quality (see Hard constraints).

```python
import torch
from transformers import T5Tokenizer, T5EncoderModel

ckpt = "ElnaggarLab/ankh3-xl"   # or ElnaggarLab/ankh3-large
tokenizer = T5Tokenizer.from_pretrained(ckpt)
model = T5EncoderModel.from_pretrained(ckpt).eval().to(device)

prefixed = ["[NLU]" + seq for seq in sequences]

inputs = tokenizer(
    prefixed,
    return_tensors="pt",
    padding=True,
    truncation=True,
    add_special_tokens=True,
    is_split_into_words=False,
)
inputs = {k: v.to(device) for k, v in inputs.items()}

with torch.no_grad():
    outputs = model(**inputs)

hidden = outputs.last_hidden_state
mask   = inputs["attention_mask"].unsqueeze(-1).float()
pooled = (hidden * mask).sum(1) / mask.sum(1).clamp(min=1.0)  # (B, D)
```

---

## Ankh3 — sequence completion (S2S prefix)

Ankh3 is jointly trained on sequence completion: given the first half of a sequence,
the decoder generates the second half autoregressively.

```python
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers.generation import GenerationConfig

ckpt = "ElnaggarLab/ankh3-xl"
tokenizer = T5Tokenizer.from_pretrained(ckpt)
model = T5ForConditionalGeneration.from_pretrained(ckpt).eval().to(device)

half = len(sequence) // 2
s2s_input = "[S2S]" + sequence[:half]

encoded = tokenizer(
    s2s_input,
    return_tensors="pt",
    add_special_tokens=True,
    is_split_into_words=False,
)
encoded = {k: v.to(device) for k, v in encoded.items()}

# min_length = max_length = half + 1 accounts for the decoder start token.
gen_cfg = GenerationConfig(
    min_length=half + 1, max_length=half + 1, do_sample=False, num_beams=1
)

with torch.no_grad():
    generated = model.generate(encoded["input_ids"], gen_cfg)

completed = sequence[:half] + tokenizer.batch_decode(generated, skip_special_tokens=True)[0]
```

---

## Hard constraints

- **`T5Tokenizer` only.** Never use `AutoTokenizer` — it resolves to the wrong tokenizer class for Ankh checkpoints and silently mishandles the vocabulary.
- **Ankh3 prefix is mandatory.** Do not feed Ankh3 raw sequences. Use `[NLU]` for embeddings, `[S2S]` for sequence completion. Omitting the prefix degrades representation quality.
- **`[S2S]` prefix for embeddings.** For some downstream tasks, embedding with the `[S2S]` prefix yields better quality than `[NLU]`. Pass `prefix="[S2S]"` to the script's `embed` command if experimenting.
- **No prefix for ankh-base/ankh-large.** These models do not have `[NLU]` / `[S2S]` in their vocabulary. Adding them will cause unknown-token errors.
- **`is_split_into_words=False`.** Pass this flag to the tokenizer whenever sequences carry a prefix token.
- **License: CC-BY-NC-SA-4.0** — non-commercial use only. Flag before any production deployment.

---

## Script

`scripts/ankh_inference.py` provides importable functions and a CLI for both inference modes.

```
python scripts/ankh_inference.py embed --sequences seqs.txt --model ankh-base --output emb.npy
python scripts/ankh_inference.py embed --sequences seqs.txt --model ankh3-xl --prefix "[NLU]" --output emb.npy
python scripts/ankh_inference.py complete --sequence MKTAYIAKQRQISFVK... --model ankh3-xl
python scripts/ankh_inference.py complete --sequence MKTAYIAKQRQISFVK... --model ankh3-xl --split-at 64 --output completed.txt
python scripts/ankh_inference.py --help
```
