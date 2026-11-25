---
name: prottrans
description: >
  Generate protein embeddings with ProtBert or ProtT5-XL-UniRef50 (ProtTrans family).
  Covers Rostlab/prot_bert (BERT encoder) and Rostlab/prot_t5_xl_uniref50 (T5 encoder)
  via HuggingFace transformers. Use even when the user asks broadly for "protein
  representations" or "Rostlab model" without naming ProtTrans explicitly.
  Do not use for ProtTrans fine-tuning or model selection — see model-selection for those tasks.
compatibility: transformers ≥4.30, torch ≥2.0, sentencepiece, protobuf (required for T5 tokenizer)
---

# ProtTrans Inference

For model choice and fine-tuning strategy, see the model-selection skill.

---

## Model variants

| Model | HuggingFace ID | Architecture | d_model |
|---|---|---|---|
| ProtBert | `Rostlab/prot_bert` | BERT encoder | 1024 |
| ProtT5-XL-UniRef50 | `Rostlab/prot_t5_xl_uniref50` | T5 encoder | 1024 |
| ProtT5-XL-half (enc-only, fp16) | `Rostlab/prot_t5_xl_half_uniref50-enc` | T5 encoder | 1024 |

---

## When to use / When NOT to use

| Use this skill | Use model-selection instead |
|---|---|
| Embedding sequences with ProtBert or ProtT5 | Choosing between ProtBert, ProtT5, ESM, Ankh |
| Producing per-residue or per-protein representations | LoRA or full fine-tuning setup |
| ProtBert masked-residue prediction (`fill-mask`) | Prediction heads and training loops |

---

## Critical preprocessing — applies to both models

Both models expect sequences where **each amino acid is a separate space-delimited token**.
This must be done before tokenization. Skipping it causes multi-character tokens and incorrect
embeddings with no error.

```python
import re

def preprocess_sequences(sequences: list[str]) -> list[str]:
    """Replace rare/ambiguous AAs with X, then space-separate each residue."""
    return [" ".join(list(re.sub(r"[UZOB]", "X", seq.upper()))) for seq in sequences]

# Example: "PRTEINO" → "P R T E I N O"
# Example: "SEQWENCE" → "S E Q W E N C E"
```

---

## ProtBert — HuggingFace (recommended)

```python
import re, torch
from transformers import BertTokenizer, BertModel

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
model = BertModel.from_pretrained("Rostlab/prot_bert").eval().to(device)

sequences_proc = preprocess_sequences(sequences)  # space-separate first

inputs = tokenizer(
    sequences_proc,
    return_tensors="pt",
    padding=True,
    truncation=True,
    add_special_tokens=True,
)
inputs = {k: v.to(device) for k, v in inputs.items()}

with torch.no_grad():
    output = model(**inputs)

# Tokenized form: [CLS] A E T … [SEP] <padding>
# Exclude [CLS] (index 0) and [SEP] (last attended, index slen-1) when mean-pooling.
hidden   = output.last_hidden_state          # (B, L_padded, 1024)
seqlens  = inputs["attention_mask"].sum(1)   # (B,) — [CLS] + residues + [SEP]
pooled = torch.stack([
    hidden[i, 1 : int(seqlens[i]) - 1].mean(0)  # residues only
    for i in range(hidden.size(0))
])  # (B, 1024)
```

### ProtBert — fill-mask (MLM)

```python
from transformers import BertForMaskedLM, BertTokenizer, pipeline

tokenizer = BertTokenizer.from_pretrained("Rostlab/prot_bert", do_lower_case=False)
model = BertForMaskedLM.from_pretrained("Rostlab/prot_bert")
unmasker = pipeline("fill-mask", model=model, tokenizer=tokenizer)

# Input must already be space-separated with [MASK] at the target position.
result = unmasker("D L I P T S S K L V V [MASK] D T S L Q V K K A F F A L V T")
```

---

## ProtT5-XL-UniRef50 — HuggingFace (recommended)

```python
import re, torch
from transformers import T5Tokenizer, T5EncoderModel

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = T5Tokenizer.from_pretrained("Rostlab/prot_t5_xl_uniref50", do_lower_case=False)
model = T5EncoderModel.from_pretrained("Rostlab/prot_t5_xl_uniref50").eval().to(device)

# CPU: half-precision checkpoint loads as fp16 by default — cast to float32.
if device == "cpu":
    model.to(torch.float32)

sequences_proc = preprocess_sequences(sequences)  # space-separate first

ids = tokenizer.batch_encode_plus(sequences_proc, add_special_tokens=True, padding="longest")
input_ids      = torch.tensor(ids["input_ids"]).to(device)
attention_mask = torch.tensor(ids["attention_mask"]).to(device)

with torch.no_grad():
    embedding_repr = model(input_ids=input_ids, attention_mask=attention_mask)

# Tokenized form: A E T … [EOS] <padding>  (no [CLS])
# Exclude EOS (last attended, index slen-1) when mean-pooling.
hidden  = embedding_repr.last_hidden_state   # (B, L_padded, 1024)
seqlens = attention_mask.sum(1)              # (B,) — residues + EOS
pooled = torch.stack([
    hidden[i, : int(seqlens[i]) - 1].mean(0)  # residues only
    for i in range(hidden.size(0))
])  # (B, 1024)
```

To use the faster encoder-only half-precision checkpoint, replace the checkpoint ID with
`"Rostlab/prot_t5_xl_half_uniref50-enc"`. The float32 CPU cast above remains necessary.

---

## Hard constraints

- **Space-separate before tokenizing.** `" ".join(list(re.sub(r"[UZOB]", "X", seq.upper())))`. Both models tokenize on whitespace; skipping this produces wrong per-residue alignments silently.
- **Uppercase only.** Always pass `do_lower_case=False` to the tokenizer and uppercase sequences upstream.
- **U, Z, O, B → X.** These rare/ambiguous amino acids are not in the vocabulary. Replace before tokenization; otherwise they become `[UNK]` embeddings without error.
- **ProtBert: exclude [CLS] and [SEP].** Positions 0 and `seqlen-1` of `last_hidden_state` are special tokens, not residue embeddings.
- **ProtT5: exclude EOS.** Position `seqlen-1` of `last_hidden_state` is the EOS token, not a residue.
- **`sentencepiece` and `protobuf` required for ProtT5 tokenizer.** `pip install sentencepiece protobuf`.
- **Half-precision on CPU.** `prot_t5_xl_half_uniref50-enc` loads in fp16. Always cast to float32 when running on CPU: `model.to(torch.float32)`.

---

## Script

`scripts/prottrans_inference.py` provides importable functions and a CLI.

```
python scripts/prottrans_inference.py embed --sequences seqs.txt --model prot-bert --output emb.npy
python scripts/prottrans_inference.py embed --sequences seqs.txt --model prot-t5-xl --output emb.npy
python scripts/prottrans_inference.py embed --sequence MKTAYIAK --model prot-t5-xl-half --output emb.npy
python scripts/prottrans_inference.py --help
```
