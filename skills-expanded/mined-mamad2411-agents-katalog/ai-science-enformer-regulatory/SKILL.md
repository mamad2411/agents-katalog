---
name: ai-science-enformer-regulatory
description: "Predict CAGE/DNase/ATAC/ChIP-seq tracks from raw DNA with Enformer/Borzoi, run in-silico mutagenesis (ISM), and score noncoding variant effects. Use when predicting enhancer/promoter activity from sequence, running ISM, scoring a noncoding SNP, or prioritizing GWAS/eQTL variants."
tool_type: python
primary_tool: enformer-pytorch
---

# Enformer: Regulatory Activity from DNA

## When to Use

- Predicting CAGE/DNase/ATAC/ChIP-seq signal tracks directly from a raw DNA sequence (no alignment needed)
- Running in-silico mutagenesis (ISM) to find which bases in a promoter/enhancer drive a predicted track
- Scoring a noncoding SNP/indel for predicted effect on gene expression or chromatin accessibility
- Prioritizing GWAS/eQTL candidate variants by combining sequence-based effect size with population and functional evidence
- Needing RNA-seq/splicing-aware predictions over a larger (524 kb) window — use Borzoi instead of Enformer

## Version Compatibility

- `enformer-pytorch` >= 0.8 (PyTorch >= 2.0) — community PyTorch port of DeepMind's Enformer
- Original TensorFlow weights via `tensorflow>=2.11` + `tensorflow-hub` (`https://tfhub.dev/deepmind/enformer/1`)
- `kipoiseq` >= 0.7 for one-hot encoding / FASTA windowing utilities
- Borzoi: `borzoi-pytorch` (community port) or `calico/borzoi` (native, requires `baskerville`)

## Prerequisites

- `pip install enformer-pytorch torch kipoiseq numpy` (GPU strongly recommended: full forward pass is ~2 GB+ activations per sequence)
- A reference genome FASTA (hg38 or mm10) to pull 196,608 bp windows from
- Familiarity with one-hot DNA encoding and BED-style genomic coordinates (see `bio-genome-intervals-bed-file-basics`)

## Key Facts

- **Input**: one-hot DNA, 196,608 bp x 4, centered on the region of interest
- **Output**: 896 bins x 128 bp (~114,688 bp predicted region) across 5,313 tracks (human) / 1,643 tracks (mouse) — CAGE, DNase, ATAC, ChIP-seq across 100+ cell types
- **Architecture**: stem conv -> 6 dilated conv blocks (progressive downsampling to 128 bp/bin) -> 11 transformer layers (8 heads, relative positional encodings) -> pointwise conv + softplus
- **Training**: Poisson log-likelihood loss against real -seq coverage, joint human (hg38) + mouse (mm10) heads
- **Borzoi** extends this to 524,288 bp input, 32 bp resolution, and adds RNA-seq coverage (captures splicing effects that Enformer's CAGE tracks miss)

## Loading the Real Model and Running Inference

**Goal:** get raw track predictions for a 196,608 bp genomic window using the pretrained Enformer weights.
**Approach:** load the HuggingFace-hosted checkpoint via `enformer-pytorch`, one-hot encode a FASTA window with `kipoiseq`, and run a forward pass in eval mode.

```python
import torch
from enformer_pytorch import Enformer, str_to_one_hot

def load_enformer(device: str = "cuda") -> Enformer:
    """Load the pretrained Enformer checkpoint from the HF Hub."""
    model = Enformer.from_pretrained("EleutherAI/enformer-official-rough")
    return model.to(device).eval()

def predict_tracks(model: Enformer, seq: str, device: str = "cuda"):
    """Run Enformer on a single 196,608 bp sequence.

    Returns dict with 'human' -> (896, 5313) and 'mouse' -> (896, 1643) tensors.
    seq must be exactly model.seq_length long (pad with 'N' if shorter).
    """
    one_hot = str_to_one_hot(seq).unsqueeze(0).to(device)  # (1, L, 4)
    with torch.no_grad():
        out = model(one_hot, head="both" if hasattr(model, "heads") else None)
    return out
```

## In-Silico Mutagenesis (ISM)

Mutate one position at a time to the other 3 bases, re-run the model, and take the delta from baseline. This is the ground-truth way to attribute a track's signal to individual bases; it costs `3 * L` forward passes so restrict `pos` to a small window (e.g. a candidate motif), not the whole 196 kb input.

```python
import numpy as np

def mutate_base(seq: str, pos: int, alt: str) -> str:
    """Return seq with a single base substituted at pos."""
    return seq[:pos] + alt + seq[pos + 1:]

def ism_scores(seq: str, pos: int, model_fn):
    """Compute per-allele ISM deltas at one position.

    model_fn(seq) -> np.ndarray of track scores (already sliced to the track(s)
    of interest, e.g. output['human'][:, bin_idx, track_idx].mean()).
    Returns (ref_base, baseline_score, {alt_base: delta}).
    """
    baseline = model_fn(seq)
    ref = seq[pos]
    effects = {}
    for alt in "ACGT":
        if alt == ref:
            continue
        effects[alt] = model_fn(mutate_base(seq, pos, alt)) - baseline
    return ref, baseline, effects
```

## Variant Scoring and Prioritization

Rank candidate variants by absolute predicted effect on the track(s) relevant to the phenotype (e.g. CAGE in the tissue of interest for eQTL follow-up). Combine the sequence-based score with orthogonal evidence — population allele frequency (gnomAD), GWAS/eQTL colocalization, and chromatin context — before calling a variant causal; a large ISM delta alone is not sufficient evidence.

```python
def score_variant(seq: str, pos: int, alt: str, model_fn) -> float:
    """Predicted-track delta (mut - ref) for a single substitution at pos."""
    base = model_fn(seq)
    mut = model_fn(mutate_base(seq, pos, alt))
    return float(mut - base)

def rank_variants(seq: str, candidates: list, model_fn) -> list:
    """candidates: list of (pos, alt) tuples. Returns sorted by |delta| desc,
    each as (pos, ref_base, alt_base, delta)."""
    scored = []
    for pos, alt in candidates:
        if alt == seq[pos]:
            continue
        d = score_variant(seq, pos, alt, model_fn)
        scored.append((pos, seq[pos], alt, d))
    return sorted(scored, key=lambda x: abs(x[3]), reverse=True)


def _toy_track_model(seq: str) -> float:
    """Cheap stand-in for model_fn during development/testing — counts a
    TATA-box motif as a toy 'promoter activity' proxy so ISM/ranking logic
    can be unit-tested without loading the real 250M-parameter model."""
    return 0.4 + 0.25 * sum(1 for i in range(len(seq) - 5) if seq[i:i + 6] == "TATAAA")


if __name__ == "__main__":
    test_seq = "A" * 120 + "TATAAA" + "A" * 120
    ref, baseline, effects = ism_scores(test_seq, 122, _toy_track_model)
    assert ref == "T"
    assert all(d <= 0 for d in effects.values()), "disrupting TATAAA should not raise the toy score"

    candidates = [(p, alt) for p in (118, 120, 122, 124, 126) for alt in "ACGT"]
    ranked = rank_variants(test_seq, candidates, _toy_track_model)
    assert ranked[0][0] in (120, 121, 122, 123, 124, 125), "top hit should fall inside the motif"
    print("self-check passed:", ranked[:3])
```

## Pitfalls

- **196 kb context, ~115 kb predicted**: the outer flanks give the model context but are never scored — center your variant/motif of interest, don't put it near the edges
- **ISM vs gradient attribution**: ISM is exact but costs `O(3L)` model calls; DeepLIFT/Integrated Gradients are cheaper but require access to model internals and can be noisier for saturated (softplus) outputs
- **Track units are not linear "activity"**: outputs are Poisson-rate predictions (post-softplus) in log-ish space per 128 bp bin — compare deltas on the same track/bin, don't compare raw magnitudes across tracks
- **Reference genome build**: Enformer/Borzoi were trained on hg38/mm10 — pulling sequence from hg19 coordinates without a liftover will silently give wrong predictions
- **The 11 transformer layers are what differentiate Enformer** from conv-only baselines like Basenji2 — they are what let the model integrate signal across the full 100+ kb receptive field
- **GPU memory**: a single 196,608 bp forward pass holds large intermediate activations; batch size 1 on a 16 GB GPU is often the practical ceiling without mixed precision

## See Also

- `ai-science-genomic-llms` — sequence-only foundation models (DNA language models) as an alternative to track-supervised models like Enformer
- `ai-science-splicing-models` — for splicing-specific effect prediction (SpliceAI etc.), complementary to Borzoi's RNA-seq head
- `ai-science-variant-to-structure-models` — downstream structural consequence prediction once a variant is prioritized
- `bio-genome-intervals-bed-file-basics` — coordinate handling for defining the input window

## Sources

- [Avsec et al. 2021, Enformer (Nature Methods)](https://www.nature.com/articles/s41592-021-01252-x)
- [DeepMind Enformer](https://github.com/google-deepmind/deepmind-research/tree/master/enformer)
- [enformer-pytorch](https://github.com/lucidrains/enformer-pytorch)
- [Borzoi](https://github.com/calico/borzoi)
