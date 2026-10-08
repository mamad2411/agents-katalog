---
name: ai-science-esm2-embeddings
description: Generate ESM2 protein embeddings (fair-esm/transformers) and predict structure with ESMFold. Use when embedding sequences, scoring mutations zero-shot, annotating protein function, or doing fast MSA-free structure prediction.
tool_type: python
primary_tool: fair-esm
---

# ESM2 Embeddings and ESMFold

## When to Use

- Need a fixed-length vector representation of a protein sequence for downstream ML (classification, clustering, similarity search)
- Scoring point mutations / variants zero-shot without labeled training data
- Predicting a 3D structure quickly (no MSA) for screening before a slower AlphaFold2 run
- Annotating protein function or detecting homology when a sequence has no close characterized relatives
- Extracting per-residue features for binding-site, disorder, or secondary-structure prediction

## Version Compatibility

- `fair-esm` 2.0.0 (import name `esm`), PyTorch ≥2.0, Python ≥3.9
- Alternative: HuggingFace `transformers` ≥4.30 (`EsmModel`/`EsmForMaskedLM`, checkpoints `facebook/esm2_t33_650M_UR50D`, etc.) — same weights, no `fair-esm` dependency
- ESMFold requires an additional `pip install "fair-esm[esmfold]"` plus `openfold`; GPU with ≥16GB VRAM recommended for the 650M+ models

## Prerequisites

- `pip install fair-esm torch` (or `pip install transformers torch`)
- GPU strongly recommended for anything above ESM2-150M; CPU is fine for embedding extraction on short sequences with the 8M/35M models
- Familiarity with protein FASTA format and basic PyTorch tensor ops

## ESM2 Architecture

ESM2 (Lin et al., 2023, *Science*) is a transformer protein language model trained with masked-language-modeling (~15% masking) on UniRef50/90 (~65M unique training sequences).

| Model | Layers | Embedding dim | Params |
|---|---|---|---|
| ESM2-8M | 6 | 320 | 8M |
| ESM2-35M | 12 | 480 | 35M |
| ESM2-150M | 30 | 640 | 150M |
| ESM2-650M | 33 | 1280 | 650M |
| ESM2-3B | 36 | 2560 | 3B |
| ESM2-15B | 48 | 5120 | 15B |

ESM2-650M is the sweet spot for most tasks (single GPU, strong signal). Tokenization is one token per amino acid (33-token vocabulary: 20 standard AAs + B/U/Z/O + `<cls>`/`<eos>`/`<pad>`/`<mask>`/`<unk>`) — no k-mer/subword splitting, so a 500-residue protein is 502 tokens.

Despite no structural supervision, ESM2 representations predict secondary structure (~80% linear-probe accuracy), contact maps (from attention), enzymatic function (same EC number clusters together), and evolutionary distance (correlates with embedding cosine similarity).

## Extracting Embeddings

**Goal:** get a per-residue or mean-pooled vector for one or more protein sequences.
**Approach:** load ESM2 via `fair-esm`, batch-encode sequences, run a forward pass with `repr_layers` set to the layer(s) you want, then pool over the residue axis (excluding `<cls>`/`<eos>`).

```python
# pip install fair-esm torch
import esm
import torch


def embed_sequences(sequences: dict[str, str], layer: int = 33, device: str = "cpu"):
    """Return {name: (per_residue_emb, mean_emb)} using ESM2-650M.

    per_residue_emb: (seq_len, 1280) tensor, one row per amino acid.
    mean_emb: (1280,) tensor, mean-pooled over residues (excludes <cls>/<eos>).
    """
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    model = model.eval().to(device)
    batch_converter = alphabet.get_batch_converter()

    data = list(sequences.items())
    _, _, batch_tokens = batch_converter(data)
    batch_tokens = batch_tokens.to(device)

    with torch.no_grad():
        out = model(batch_tokens, repr_layers=[layer], return_contacts=False)
    reps = out["representations"][layer]

    results = {}
    for i, (name, seq) in enumerate(data):
        per_residue = reps[i, 1 : len(seq) + 1]  # drop <cls> (pos 0) and <eos>
        results[name] = (per_residue.cpu(), per_residue.mean(0).cpu())
    return results


if __name__ == "__main__":
    seqs = {
        "protein1": "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQ",
        "protein2": "ACDEFGHIKLMNPQRSTVWY",
    }
    embeddings = embed_sequences(seqs)
    for name, (per_res, mean_vec) in embeddings.items():
        assert per_res.shape == (len(seqs[name]), 1280)
        assert mean_vec.shape == (1280,)
        print(name, "per-residue:", tuple(per_res.shape), "mean:", tuple(mean_vec.shape))
```

Use mean pooling for sequence-level tasks (classification, clustering); use per-residue vectors for residue-level tasks (variant scoring, binding-site prediction). Extract from the last layer (33 for ESM2-650M) for most tasks; intermediate layers can help structural probes.

## ESMFold Structure Prediction

**Goal:** predict a 3D structure from sequence alone, without an MSA search.
**Approach:** load the ESMFold wrapper (ESM2-3B + folding trunk), run `infer_pdb`, then read the pLDDT confidence out of the B-factor column.

```python
# pip install "fair-esm[esmfold]" torch openfold
import esm
import torch


def predict_structure(sequence: str, out_path: str = "predicted.pdb") -> str:
    """Predict structure with ESMFold and write a PDB file. Returns the PDB text."""
    model = esm.pretrained.esmfold_v1().eval()
    if torch.cuda.is_available():
        model = model.cuda()
    with torch.no_grad():
        pdb_str = model.infer_pdb(sequence)
    with open(out_path, "w") as f:
        f.write(pdb_str)
    return pdb_str


def confidence_bucket(mean_plddt: float) -> str:
    """Bucket a mean pLDDT score (0-100) using the standard AlphaFold2/ESMFold thresholds."""
    if mean_plddt >= 90:
        return "very_high"
    if mean_plddt >= 70:
        return "usable"
    if mean_plddt >= 50:
        return "low"
    return "very_low"


if __name__ == "__main__":
    for v, expected in [(96, "very_high"), (82, "usable"), (63, "low"), (41, "very_low")]:
        assert confidence_bucket(v) == expected
    print("confidence_bucket checks passed")
```

ESMFold is ~10-60x faster than AlphaFold2 (no MSA) with comparable accuracy on easy targets, but degrades on proteins with many homologs where MSA-derived co-evolution signal matters. Use ESMFold for rapid screening, AF2 for final structural analysis. No-GPU option: POST the sequence to `https://api.esmatlas.com/foldSequence/v1/pdb/` and save the response text as a PDB.

## Amino Acid Composition Baseline

Always benchmark ESM2 against this trivial baseline first — if ESM2 doesn't beat it, the task may be composition-dependent rather than context-dependent, and you don't need a language model.

```python
import numpy as np

np.random.seed(9)
AA = list("ACDEFGHIKLMNPQRSTVWY")
AA_INDEX = {a: i for i, a in enumerate(AA)}


def toy_embed(seq: str) -> np.ndarray:
    """20-aa composition frequency + normalized length as a 21-dim baseline embedding."""
    vec = np.zeros(21, dtype=float)
    for a in seq:
        if a in AA_INDEX:
            vec[AA_INDEX[a]] += 1
    if len(seq) > 0:
        vec[:20] /= len(seq)
    vec[20] = min(len(seq) / 500.0, 1.0)
    return vec


def random_protein(n: int) -> str:
    return "".join(np.random.choice(AA, size=n))


def inject_motif(seq: str, motif: str, pos: int) -> str:
    return seq[:pos] + motif + seq[pos + len(motif):]


if __name__ == "__main__":
    N, motif = 200, "HGH"
    seqs, y = [], []
    for _ in range(N):
        s = random_protein(80)
        if np.random.rand() < 0.5:
            s = inject_motif(s, motif, 25)
            y.append(1)
        else:
            y.append(0)
        seqs.append(s)

    X = np.vstack([toy_embed(s) for s in seqs])
    y = np.array(y)
    train, test = np.arange(150), np.arange(150, N)
    c0 = X[train][y[train] == 0].mean(axis=0)
    c1 = X[train][y[train] == 1].mean(axis=0)
    pred = (((X[test] - c1) ** 2).sum(axis=1) < ((X[test] - c0) ** 2).sum(axis=1)).astype(int)
    acc = float((pred == y[test]).mean())
    assert 0.0 <= acc <= 1.0
    print("Composition-probe accuracy:", acc)
```

## Pitfalls

- **Off-by-one on `<cls>`/`<eos>`**: per-residue slicing must use `[1 : len(seq)+1]` — forgetting to drop `<cls>` shifts every residue index by one
- **Layer index depends on model size**: `repr_layers=[33]` is correct only for ESM2-650M (33 layers); use the model's own layer count (e.g. `[12]` for ESM2-35M), not a hardcoded 33
- **Sequence length limits**: attention is O(n²) in sequence length; very long proteins (>1000 aa) need chunking or a smaller model to fit GPU memory
- **ESMFold accuracy drop on homolog-rich families**: skipping the MSA loses co-evolution signal AF2 exploits — cross-check low-confidence ESMFold regions with AF2 before trusting them
- **`fair-esm` is largely unmaintained**: for new projects prefer HuggingFace `transformers` (`EsmModel.from_pretrained("facebook/esm2_t33_650M_UR50D")`) for the same weights with active support

## See Also

- `esm` — broader ESM model family usage (ESM-1v, ESM-IF1) beyond embeddings/ESMFold
- `bio-structural-biology-alphafold-predictions` — AlphaFold2 structure prediction for final/high-accuracy analysis
- `bio-structural-biology-modern-structure-prediction` — comparing modern structure predictors including ESMFold
- `alphafold-database` — fetching precomputed AlphaFold structures instead of predicting from scratch
