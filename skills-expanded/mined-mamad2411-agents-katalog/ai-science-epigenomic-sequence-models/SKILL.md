---
name: ai-science-epigenomic-sequence-models
description: "Choose Borzoi (RNA-seq coverage, 32bp) vs Epiformer (sequence+PhyloP, chromatin accessibility) vs AlphaGenome for epigenomic prediction. Use when picking a model for RNA-seq, ATAC/DNase, or variant-effect scoring."
tool_type: python
primary_tool: NumPy
---

# Epigenomic Sequence Models: Borzoi and Epiformer

## When to Use

- Choosing between sequence-to-function model families for a specific epigenomic assay (RNA-seq coverage, ATAC-seq/DNase accessibility, variant effect prediction).
- A user asks "which model predicts chromatin accessibility from DNA sequence" or "Borzoi vs Enformer vs Epiformer" or "do I need a conservation track for this prediction."
- Debugging poor model performance caused by evaluating on the wrong output modality (e.g., using an expression model to score accessibility).
- Deciding whether a single unified model (AlphaGenome) or task-specific models are the right tradeoff for a variant-effect pipeline.
- Building a toy/benchmark predictor to sanity-check modality-specific correlations before committing to a heavyweight model download.

## Version Compatibility

- Borzoi: Calico's `borzoi-pytorch` / original Baskerville (TensorFlow) implementations, 2023 release.
- Epiformer: sequence + PhyloP conservation accessibility model, 2024 (Science-linked); requires a precomputed conservation bigWig/track per region.
- AlphaGenome: DeepMind/Google, 2025 unified multi-modal model (expression, splicing, chromatin, 3D contacts).
- Enformer: predecessor to Borzoi, 128 bp bin resolution — kept here only as a contrast point (see `ai-science-enformer-regulatory`).
- NumPy ≥1.24, Python ≥3.10 for the toy benchmark code below (no GPU or model weights required).

## Prerequisites

- `pip install numpy` for the synthetic benchmark in this skill.
- For the real models: `pip install borzoi-pytorch` (or Baskerville/TensorFlow for the original Borzoi), plus PhyloP conservation tracks (e.g., from UCSC/Ensembl) for Epiformer.
- Familiarity with `ai-science-enformer-regulatory` (bin-averaged ChIP/CAGE/DNase prediction) helps frame why Borzoi's 32 bp resolution matters.

## Key Distinctions

- **Borzoi**: sequence-only input → RNA-seq coverage at 32 bp resolution. Captures splicing, UTR usage, isoform signals.
- **Epiformer**: sequence + conservation track input → chromatin accessibility. Requires precomputed PhyloP scores for the region; cannot run sequence-only.
- **AlphaGenome** (2025): unified model for expression, splicing, chromatin, 3D contacts — avoids model-selection but is heavier compute.
- **Enformer** (predecessor): 128 bp bin averages of ChIP/CAGE/DNase — coarser resolution than Borzoi, different modality entirely.

| Goal | Preferred model |
|---|---|
| RNA-seq coverage from sequence | Borzoi |
| ATAC/chromatin accessibility | Epiformer |
| Broad multi-modal variant effects | AlphaGenome |
| Splicing triage | SpliceAI |

**Goal:** Decide which model family to trust for a given epigenomic assay, and confirm the decision with a quick modality-specific correlation check rather than assuming a proxy modality works.

**Approach:** Build toy scoring functions that mimic each model's known input dependencies (Borzoi: promoter/enhancer motifs only; Epiformer: open-chromatin motifs + conservation), generate a synthetic benchmark with noisy "observed" targets, then measure correlation per modality — including a deliberate cross-task mismatch to show why proxying is unsafe.

```python
import numpy as np

np.random.seed(19)


def random_dna(n: int) -> str:
    """Generate a random DNA sequence of length n over {A,C,G,T}."""
    return "".join(np.random.choice(list("ACGT"), size=n))


def motif_count(seq: str, motif: str) -> int:
    """Count (overlapping) occurrences of motif in seq."""
    return sum(1 for i in range(len(seq) - len(motif) + 1) if seq[i:i + len(motif)] == motif)


def toy_borzoi_expression(seq: str) -> float:
    """Borzoi-like expression score: sequence only, driven by promoter/enhancer motifs."""
    score = 0.2 + 0.35 * motif_count(seq, "TATAAA") + 0.08 * motif_count(seq, "GATA")
    return float(np.clip(score, 0.0, 3.0))


def toy_epiformer_accessibility(seq: str, conservation: float) -> float:
    """Epiformer-like accessibility score: sequence + conservation track (e.g. PhyloP)."""
    score = 0.15 + 0.12 * motif_count(seq, "ATAC") + 0.55 * conservation
    return float(np.clip(score, 0.0, 2.5))


def corr(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson correlation between two 1D arrays."""
    return float(np.corrcoef(a, b)[0, 1])


def modality_benchmark(n: int = 120):
    """Build a synthetic benchmark and report per-modality correlation, plus the
    failure mode of using the wrong modality as a proxy.
    """
    seqs = [random_dna(500) for _ in range(n)]
    cons = np.random.uniform(0.1, 0.95, size=n)

    true_expr = np.array([toy_borzoi_expression(s) for s in seqs]) + np.random.normal(0, 0.08, size=n)
    true_acc = np.array(
        [toy_epiformer_accessibility(s, c) for s, c in zip(seqs, cons)]
    ) + np.random.normal(0, 0.06, size=n)

    pred_expr = np.array([toy_borzoi_expression(s) for s in seqs])
    pred_acc = np.array([toy_epiformer_accessibility(s, c) for s, c in zip(seqs, cons)])

    expr_corr = corr(pred_expr, true_expr)
    acc_corr = corr(pred_acc, true_acc)

    # Cross-task mismatch: using an expression score to predict accessibility.
    bad_acc_proxy = (pred_expr - pred_expr.min()) / (pred_expr.max() - pred_expr.min() + 1e-9)
    mismatch_corr = corr(bad_acc_proxy, true_acc)

    return {"expression_corr": expr_corr, "accessibility_corr": acc_corr, "wrong_modality_corr": mismatch_corr}


if __name__ == "__main__":
    results = modality_benchmark()
    assert results["expression_corr"] > 0.8, "Borzoi-like model should track its own modality well"
    assert results["accessibility_corr"] > 0.8, "Epiformer-like model should track its own modality well"
    assert abs(results["wrong_modality_corr"]) < abs(results["expression_corr"]), (
        "Cross-modality proxy should correlate much worse than the matched model"
    )
    print(results)
```

## Pitfalls

- Enformer predicts 128 bp bin averages of ChIP/CAGE/DNase. Borzoi predicts RNA-seq at 32 bp — a different modality and resolution, not interchangeable.
- Epiformer cannot run without a precomputed conservation track (e.g., PhyloP) for the genome region — sequence-only input will fail or silently degrade accuracy.
- Conservation helps accessibility prediction because evolutionarily conserved non-coding regions are enriched for functional regulatory elements — dropping it removes a strong prior, not just an extra feature.
- Always benchmark a model on the output modality you actually need; using an expression-style score as a proxy for accessibility (or vice versa) looks plausible but correlates poorly (see `wrong_modality_corr` above).
- AlphaGenome's unified output avoids model-selection but costs more compute — don't reach for it by default when a lighter task-specific model (Borzoi/Epiformer/SpliceAI) already covers the assay.

## See Also

- `ai-science-enformer-regulatory` — the 128 bp bin-averaged predecessor to Borzoi.
- `ai-science-splicing-models` — SpliceAI/AlphaGenome for splicing-specific triage.
- `ai-science-variant-to-structure-models` — downstream structural consequences of variants.
- `bio-atac-seq-atac-peak-calling` — calling real ATAC-seq accessibility peaks from data (vs. predicting them).

## Sources

- [Borzoi](https://github.com/calico/borzoi)
- [Epiformer](https://github.com/yal054/epiformer)
