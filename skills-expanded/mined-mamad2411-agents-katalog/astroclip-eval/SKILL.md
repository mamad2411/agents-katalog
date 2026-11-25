---
name: astroclip-eval
description: Evaluates a cross-modal foundation model's zero-shot and few-shot regression capabilities on galaxy physical properties (redshift, stellar mass, metallicity, age, sSFR) and its cross-modal similarity search performance, using fixed embeddings without task-specific fine-tuning. Use when the user wants to benchmark on PROVABGS, or asks about evaluating this task. Reports R^2.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2310.03024
  bibtex_key: parker2023astroclip
  confidence: high
---

# astroclip-eval

> AstroCLIP: A Cross-Modal Foundation Model for Galaxies — Parker et al. (2023) (arXiv:2310.03024, 2023)

## What this evaluates

Evaluates a cross-modal foundation model's zero-shot and few-shot regression capabilities on galaxy physical properties (redshift, stellar mass, metallicity, age, sSFR) and its cross-modal similarity search performance, using fixed embeddings without task-specific fine-tuning.

## Datasets

- **PROVABGS** — total ?; splits: test (-1)

## Metrics

- `R^2` **(primary)** — range: other
  - Coefficient of determination: 1 - (SS_res / SS_tot), where SS_res is the sum of squared residuals and SS_tot is the total sum of squares. Measures the proportion of variance in the target variable explained by the model.
- `cosine similarity` — range: [-1, 1]
  - Normalized scalar product between two vectors: dot(z_q, z_db) / (||z_q||_2 * ||z_db||_2). Used for ranking nearest neighbors in retrieval tasks.

## Input / output format

**Input**: Galaxy images (x^im) and/or spectra (x^sp) fed into AstroCLIP encoders to produce 512-dimensional embeddings.

**Output**: Normalized embeddings (z_bar) for retrieval, or regression predictions (redshift, M_*, Z_MW, t_age, sSFR) generated via k-NN or a single-hidden-layer MLP (width=32) on the embeddings.

## Scoring recipe

```python
def r2_score(y_true, y_pred):
    ss_res = sum((y - y_hat)**2 for y, y_hat in zip(y_true, y_pred))
    ss_tot = sum((y - mean(y_true))**2 for y in y_true)
    return 1 - (ss_res / ss_tot)

def cosine_similarity(z_q, z_db):
    return np.dot(z_q, z_db) / (np.linalg.norm(z_q) * np.linalg.norm(z_db))
```

## Common pitfalls

- Assuming the model requires task-specific fine-tuning; evaluation is strictly zero-shot or few-shot on frozen embeddings.
- Confusing photometric redshift (predicted from images) with spectroscopic redshift (nearly perfect in spectra); the paper explicitly contrasts these modalities.
- Interpreting R^2 values as bounded to [0,1]; negative values are mathematically possible if the model performs worse than the mean baseline.

## Evidence (verbatim from paper)

> We report our results in Table 2. Again, AstroCLIP demonstrates an ability to capture in its galaxy embeddings core physical properties of the input galaxy despite undergoing no task-specific training or fine-tuning. ... Table 2. Galaxy property estimation R^2 performance. We present AstroCLIP's zero- and few-shot performance in regressing stellar mass (M_*), metallicity (Z_MW), age (t_age), and specific-star formation rate (sSFR) from galaxy images and spectra.

## Citation

```bibtex
@misc{parker2023astroclip,
  title={AstroCLIP: A Cross-Modal Foundation Model for Galaxies},
  author={Parker et al. (2023)},
  year={2023},
  note={arXiv:2310.03024}
}
```

- arXiv: 2310.03024
