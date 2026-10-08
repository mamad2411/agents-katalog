---
name: ai-science-geneformer-scgpt
description: Tokenize scRNA-seq via Geneformer gene-rank or scGPT expression-bin encoding; annotate cell types, simulate in-silico knockouts. Use for foundation-model cell annotation, Geneformer/scGPT tokenization, or perturbation prediction.
tool_type: python
primary_tool: geneformer
---

# Geneformer and scGPT for Single-Cell Modeling

## When to Use

- Annotating cell types from an expression matrix using a pretrained single-cell foundation model instead of marker-gene scoring
- Explaining or prototyping Geneformer's rank-value tokenization or scGPT's (gene, expression-bin) tokenization
- Predicting the transcriptional effect of a gene knockout or drug/cytokine treatment in silico before running a wet-lab perturbation
- Deciding whether Geneformer or scGPT fits a project (architecture, pretraining data, perturbation support)
- Building a toy pipeline to sanity-check tokenization/embedding logic before scaling to real checkpoints (HuggingFace `ctheodoris/Geneformer`, `bowang-lab/scGPT`) or CellxGene Census

## Version Compatibility

- Python ≥ 3.10, NumPy ≥ 1.24, pandas ≥ 2.0
- Real checkpoints: `geneformer` (HuggingFace, transformers ≥ 4.30), `scgpt` (PyTorch ≥ 2.0, flash-attn optional)
- `cellxgene-census` ≥ 1.15 for pulling real-scale (30M+ cell) training/eval data

## Prerequisites

- `pip install numpy pandas` (toy workflow below); `pip install geneformer scgpt cellxgene-census transformers torch` for real checkpoints
- Familiarity with AnnData / expression-matrix basics (see `anndata`, `bio-single-cell-preprocessing` skills)
- Concept: masked language modeling (MLM) pretraining objective

## Architecture Overview

**Geneformer** (Theodoris et al., *Nature* 2023) — pretrained on ~30M human single-cell transcriptomes.
- Rank-value tokenization: rank all ~20,000 genes by expression per cell (rank 1 = highest), keep top-K (K=2048) — eliminates the dropout problem since only ordering matters, not zero-inflated counts
- Each gene maps to a learned embedding; raw count values are never seen by the model, only relative order
- Pretraining: masked LM — predict masked gene tokens from the remaining ranked genes
- Fine-tuning: cell-type classification, gene dosage sensitivity, in-silico perturbation (zero out a gene token, observe CLS embedding shift), drug response
- Why ranks over raw counts: raw counts vary with library size and batch/protocol; rank order is inherently normalized without explicit batch correction

**scGPT** (Cui et al., *Nature Methods* 2024) — pretrained on ~33M cells from CellxGene.
- Expression-binning tokenization: gene vocab ~60,000 Entrez IDs → learned embeddings; expression discretized into bins (e.g. 51); each cell = sequence of (gene_token, expression_bin_token) pairs
- Conditioned on a batch/condition token for multi-batch training
- Perturbation module: a learned perturbation embedding is injected into the sequence to predict post-perturbation expression profiles (in-silico knockouts, drug response)

| Feature | Geneformer | scGPT |
|---|---|---|
| Input representation | Gene ranks only | Gene identity + binned expression |
| Pretraining data | ~30M cells | ~33M cells |
| Context length | 2048 genes | variable |
| Perturbation modeling | Via embedding shift | Via explicit perturbation tokens |
| Output | CLS embedding, masked gene prediction | Expression profiles, perturbation responses |

## Rank-Token Embedding (Geneformer-style)

**Goal:** turn a cells × genes expression matrix into rank-based tokens and a fixed-length embedding, without ever using raw magnitudes.

**Approach:** for each cell, take the top-K expressed genes sorted by rank, then build an embedding that weights each gene by `1/(rank+1)` so higher-ranked genes contribute more.

```python
import numpy as np
import pandas as pd

genes = [f'G{i:02d}' for i in range(30)]  # toy expression matrix: 240 cells x 30 genes, 3 cell types with markers
n_cells = 240

types = np.random.choice(['Tcell', 'Bcell', 'Myeloid'], size=n_cells, p=[0.35, 0.30, 0.35])
X = np.random.gamma(shape=1.5, scale=1.0, size=(n_cells, len(genes)))

markers = {
    'Tcell': [1, 2, 3],
    'Bcell': [8, 9, 10],
    'Myeloid': [15, 16, 17],
}
for i, t in enumerate(types):
    X[i, markers[t]] += np.random.uniform(2.5, 4.0)

expr = pd.DataFrame(X, columns=genes)


def topk_rank_tokens(row: np.ndarray, k: int = 8) -> tuple:
    """Geneformer-style tokenization: return the indices of the top-k genes by
    expression, highest first. Only ordering survives -- magnitude is discarded."""
    idx = np.argsort(row)[::-1][:k]
    return tuple(idx.tolist())


def toy_cell_embedding(token_tuple: tuple, n_genes: int = 30) -> np.ndarray:
    """Build a fixed-length embedding from ranked gene tokens: earlier ranks
    (higher expression) get more weight (1/(rank+1)), then L2-normalize."""
    v = np.zeros(n_genes, dtype=float)
    for rank, g in enumerate(token_tuple):
        v[g] += 1.0 / (rank + 1)
    return v / (np.linalg.norm(v) + 1e-9)


tokens = [topk_rank_tokens(expr.iloc[i].values, k=8) for i in range(n_cells)]
E = np.vstack([toy_cell_embedding(t, n_genes=len(genes)) for t in tokens])
print('Embedding matrix:', E.shape)
```

## Cell-Type Annotation (Nearest Centroid)

**Goal:** classify cells by type using only the rank-token embeddings — analogous to fine-tuning Geneformer's CLS token for a classification head.

**Approach:** compute per-class centroids on a train split, assign each test cell to its nearest centroid in embedding space.

```python
def annotate_by_centroid(E: np.ndarray, y: np.ndarray, train_idx: np.ndarray, test_idx: np.ndarray) -> np.ndarray:
    """Nearest-centroid cell-type annotation: fit one centroid per class on
    train_idx, then assign each test_idx row to its closest centroid."""
    classes = np.unique(y[train_idx])
    centroids = {c: E[train_idx][y[train_idx] == c].mean(axis=0) for c in classes}

    def predict_one(vec):
        dists = {c: np.linalg.norm(vec - centroids[c]) for c in centroids}
        return min(dists, key=dists.get)

    return np.array([predict_one(E[i]) for i in test_idx])


y = np.array(types)
idx = np.arange(n_cells)
np.random.shuffle(idx)
train, test = idx[:180], idx[180:]

pred = annotate_by_centroid(E, y, train, test)
acc = float((pred == y[test]).mean())
print('Annotation accuracy:', round(acc, 3))
```

## In-Silico Perturbation Prototype

**Goal:** approximate scGPT's perturbation-prediction workflow (predict expression after a gene knockout or treatment) without a trained perturbation head.

**Approach:** apply hand-specified multiplicative rules per perturbation to stand in for a learned perturbation embedding — real scGPT replaces this branch with a learned token injected into the transformer.

```python
def perturb_predict(cell_vec: np.ndarray, pert: str) -> np.ndarray:
    """Toy stand-in for scGPT's perturbation module: apply a rule-based
    expression change for a named perturbation (KO_<gene> or CYTOKINE_X)."""
    out = cell_vec.copy()
    if pert == 'KO_G02':
        out[2] *= 0.2          # knockout: strong knockdown of G02
    elif pert == 'KO_G09':
        out[9] *= 0.2          # knockout: strong knockdown of G09
    elif pert == 'CYTOKINE_X':
        out[[1, 3, 15]] *= 1.3  # treatment: upregulate responsive genes
    return out


cell0 = expr.iloc[0].values
for p in ['KO_G02', 'KO_G09', 'CYTOKINE_X']:
    pred_expr = perturb_predict(cell0, p)
    print(p, 'delta_mean=', round(float((pred_expr - cell0).mean()), 4))
```

## Pitfalls

- **Rank tokenization loses magnitude**: Geneformer never sees raw or normalized counts, only top-K gene order — don't assume it can answer "how much" questions, only "which genes / how ranked"
- **scGPT expression bins**: expression is discretized (e.g. ~51 bins), not continuous — precision below bin resolution is unrecoverable
- **Perturbation code above is illustrative, not predictive**: real in-silico perturbation requires a model trained on Perturb-seq data (e.g. scGPT's perturbation module, GEARS); rule-based multipliers do not generalize to unseen perturbations
- **Batch effects**: check for batch confounding before trusting annotation or perturbation output as biological signal, even with foundation-model embeddings
- **Verify pretraining overlap**: transfer learning needs fewer labeled cells than training from scratch, but only helps if the pretraining corpus covers a similar tissue/cell type to your data
- **API drift**: verify any `Geneformer`/`scGPT` class or checkpoint name against the current HuggingFace/GitHub repo before use — these libraries change quickly and names are easy to hallucinate

## See Also

- `bio-single-cell-preprocessing` — QC, normalization, and AnnData setup before tokenization
- `bio-single-cell-cell-annotation` — marker-gene-based annotation as a non-foundation-model baseline
- `bio-single-cell-perturb-seq` — real Perturb-seq experimental design and analysis
- `cellxgene-census` — pulling real-scale (30M+ cell) training/eval data

## References

- [Geneformer paper (Nature 2023)](https://www.nature.com/articles/s41586-023-06139-9)
- [scGPT paper (Nature Methods 2024)](https://www.nature.com/articles/s41592-024-02201-0)
- [CellxGene Census documentation](https://chanzuckerberg.github.io/cellxgene-census/)
