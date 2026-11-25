---
name: ai-science-genomic-llms
description: "Embed DNA with genomic foundation models (Nucleotide Transformer, HyenaDNA, Evo) via HuggingFace transformers; k-mer tokenize, probe promoter motifs. Use for DNA LLMs, genomic embeddings, or NT/HyenaDNA/Evo choice."
tool_type: python
primary_tool: transformers
---

# Genomic Foundation Models: Nucleotide Transformer, HyenaDNA, and Evo

## When to Use

- Extracting sequence embeddings from a pretrained DNA/RNA language model for a downstream classifier (promoter, splice site, enhancer)
- Deciding between k-mer, BPE, or character-level tokenization for a genomic sequence task
- Choosing which foundation model fits a task: short-window classification vs. 100kb+ long-range regulatory context vs. sequence generation
- Building a lightweight k-mer baseline before paying for a large model's inference cost
- Explaining why 6-mer tokenization loses single-nucleotide resolution needed for splice-site or variant tasks

## Version Compatibility

- `transformers` >= 4.40, `torch` >= 2.1, Python >= 3.10
- Model checkpoints (HuggingFace Hub): `InstaDeepAI/nucleotide-transformer-500m-human-ref`, `LongSafari/hyenadna-tiny-1k-seqlen-hf`, `togethercomputer/evo-1-8k-base`
- `trust_remote_code=True` is required for HyenaDNA and Evo (custom modeling code, not yet in core `transformers`)

## Prerequisites

- `pip install transformers torch numpy`
- GPU strongly recommended for NT-500M+/Evo (T4 minimum, A100 for NT-2.5B/Evo-7B); CPU is fine for the toy k-mer baselines below
- Familiarity with tokenization concepts and basic PyTorch model inference

## Tokenization Strategies

- **Character-level** (`A,C,G,T,N`): highest resolution, longest sequences
- **k-mer tokens** (e.g. k=6): compressed vocab; k=6 -> 4096 tokens, k=8 -> 65,536 — prefer k<=6 for explicit k-mer tokenization
- **BPE/subword**: data-driven units (DNABERT-2)
- **Nucleotide Transformer**: overlapping 6-mers, stride=1, 4096-vocab, ~L/6 tokens per sequence — loses single-nucleotide resolution
- **HyenaDNA**: single-nucleotide tokens processed by a Hyena (implicit convolution) operator instead of self-attention; handles up to 1M nucleotides without O(L^2) attention cost
- **Evo**: single-nucleotide, trained on prokaryotic/viral genomes (not human) — use for microbial sequence design/scoring, not mammalian regulatory biology

**Goal:** get real contextual embeddings out of a pretrained genomic LLM instead of hand-built features.
**Approach:** load the tokenizer + model from the HuggingFace Hub, mask-average the last hidden state over real (non-padding) tokens.

```python
import torch
from transformers import AutoTokenizer, AutoModelForMaskedLM


def embed_with_nucleotide_transformer(
    sequences: list[str],
    checkpoint: str = "InstaDeepAI/nucleotide-transformer-500m-human-ref",
) -> torch.Tensor:
    """Mean-pool the last hidden layer of Nucleotide Transformer over real tokens.

    Returns a (n_sequences, hidden_dim) tensor of sequence embeddings.
    """
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    model = AutoModelForMaskedLM.from_pretrained(checkpoint, trust_remote_code=True)
    model.eval()

    tokens = tokenizer(sequences, return_tensors="pt", padding=True)["input_ids"]
    attention_mask = tokens != tokenizer.pad_token_id

    with torch.no_grad():
        outputs = model(tokens, attention_mask=attention_mask, output_hidden_states=True)
    hidden = outputs["hidden_states"][-1]  # (batch, seq_len, hidden_dim)

    mask = attention_mask.unsqueeze(-1)
    mean_embeddings = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1)
    return mean_embeddings


# embeddings = embed_with_nucleotide_transformer(["ATTCCGATTCCG", "ATTTCTCTCTCTGAGATCGATCGAT"])
# embeddings.shape -> (2, 1280) for the 500M checkpoint
```

## k-mer Baseline: Tokenize, Embed, Classify

**Goal:** a zero-GPU sanity-check baseline for a promoter/motif classification task, useful before committing to a foundation model.
**Approach:** count k-mer frequencies as a fixed-length vector, then classify with nearest-centroid — no training loop, no gradients.

```python
import numpy as np
from collections import Counter

np.random.seed(7)


def kmers(seq: str, k: int = 6) -> list[str]:
    """Slide a window of size k across seq, returning all overlapping k-mers."""
    seq = seq.upper()
    return [seq[i:i + k] for i in range(len(seq) - k + 1)]


def kmer_embedding(seq: str, vocab: list[str], k: int = 3) -> np.ndarray:
    """Frequency-normalized k-mer count vector over a fixed vocab (order matters)."""
    counts = Counter(kmers(seq, k))
    vec = np.array([counts[v] for v in vocab], dtype=float)
    return vec / (vec.sum() + 1e-9)


def random_dna(n: int) -> str:
    return "".join(np.random.choice(list("ACGT"), size=n))


def inject_motif(seq: str, motif: str, pos: int) -> str:
    return seq[:pos] + motif + seq[pos + len(motif):]


alphabet = ["A", "C", "G", "T"]
vocab_3 = [a + b + c for a in alphabet for b in alphabet for c in alphabet]

# Synthetic promoter task: half the sequences get a TATA box injected at pos=20
n_samples, length, motif = 120, 80, "TATAAA"
seqs, labels = [], []
for _ in range(n_samples):
    s = random_dna(length)
    if np.random.rand() < 0.5:
        s = inject_motif(s, motif, pos=20)
        labels.append(1)
    else:
        labels.append(0)
    seqs.append(s)

X = np.stack([kmer_embedding(s, vocab_3, k=3) for s in seqs])
y = np.array(labels)
X_train, y_train = X[:90], y[:90]
X_test, y_test = X[90:], y[90:]

# Nearest-centroid: classify by distance to each class's mean embedding
c0 = X_train[y_train == 0].mean(axis=0)
c1 = X_train[y_train == 1].mean(axis=0)
d0 = ((X_test - c0) ** 2).sum(axis=1)
d1 = ((X_test - c1) ** 2).sum(axis=1)
pred = (d1 < d0).astype(int)

acc = (pred == y_test).mean()
print(f"Nearest-centroid probe accuracy: {acc:.3f}")
```

**Goal:** demonstrate why short context windows silently break long-range regulatory prediction.
**Approach:** a toy rule requiring two motifs 900+ bp apart; truncating the sequence drops one motif and flips the label.

```python
def distal_interaction_label(seq: str) -> int:
    """Toy long-range rule: motif A near the start AND motif B near the end."""
    has_a = "GATA" in seq[:120]
    has_b = "CACC" in seq[-120:]
    return int(has_a and has_b)


toy_long = random_dna(1000)
toy_long = inject_motif(toy_long, "GATA", 40)
toy_long = inject_motif(toy_long, "CACC", 920)

print("Long-range label:", distal_interaction_label(toy_long))
print("Truncated to 200 bp, the CACC motif at pos 920 is lost -> label flips to 0.")
```

## Model Selection

| Task profile | Preferred model |
|---|---|
| Short-window promoter/enhancer classification | DNABERT-2 / Nucleotide Transformer |
| Distal regulatory context (100kb+) | HyenaDNA |
| Prokaryotic sequence generation / scoring | Evo |
| Variant effect on expression tracks | Enformer / AlphaGenome |
| Splicing-focused interpretation | SpliceAI |

Start with the k-mer baseline above; escalate to a foundation model only when accuracy or context length demands it — inference on NT-2.5B/Evo-7B needs an A100.

## Pitfalls

- **6-mer tokenization loses single-base resolution**: splice-site and single-variant tasks (GT/AG dinucleotide) need character-level or short k-mer models, not Nucleotide Transformer's default 6-mers
- **Evo is prokaryotic/viral, not human**: don't apply it to mammalian regulatory-genomics tasks
- **Short windows silently drop long-range signal**: a 200bp window can't see a 100kb enhancer-promoter interaction — check the model's effective context vs. the biology before trusting a negative prediction
- **`trust_remote_code=True` required**: HyenaDNA and Evo ship custom modeling code on the Hub; review it before running in a shared/production environment
- **Coordinate systems**: BED is 0-based half-open, VCF/GFF are 1-based inclusive — mixing them causes off-by-one errors when mapping model outputs back to genome coordinates
- **Multiple testing**: apply FDR correction (Benjamini-Hochberg) when scoring thousands of candidate motifs/variants with any of these models

## See Also

- `bio-structural-biology-modern-structure-prediction` — coding-variant follow-up after a genomic-LLM hit (AlphaFold2/3)
- `esm` — protein language model equivalent for amino-acid sequences
- `bio-variant-calling-variant-annotation` — annotating variants before scoring them with a genomic LLM
- `bio-sequence-manipulation-motif-search` — classical motif search as an alternative to embedding-based probes
