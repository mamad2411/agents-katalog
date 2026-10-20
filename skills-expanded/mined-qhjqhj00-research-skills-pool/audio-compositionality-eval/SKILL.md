---
name: audio-compositionality-eval
description: Probes whether audio encoders preserve algebraic consistency when identical sources are added to different base scenes (A-COAT), and whether representations can be accurately reconstructed from discrete attribute-level primitives like timbre, pitch, rate, and amplitude (A-TRE). Use when the user wants to benchmark on Synthetic Audio Scenes, or asks about evaluating this task. Reports A-COAT.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.13685
  bibtex_key: chen2026evaluatingcompositional
  confidence: high
---

# audio-compositionality-eval

> Evaluating Compositional Structure in Audio Representations — Chen et al. (2026) (arXiv:2603.13685, 2026)

## What this evaluates

Probes whether audio encoders preserve algebraic consistency when identical sources are added to different base scenes (A-COAT), and whether representations can be accurately reconstructed from discrete attribute-level primitives like timbre, pitch, rate, and amplitude (A-TRE).

## Datasets

- **Synthetic Audio Scenes** — total ?; splits: test (-1); repo https://github.com/chuyangchencd/audio-compositionality

## Metrics

- `A-COAT` **(primary)** — range: [-1, 1]
  - Cosine similarity between additive transformation difference vectors: $\frac{\langle z_{B}-z_{A}, z_{D}-z_{C}\rangle}{\|z_{B}-z_{A}\|\|z_{D}-z_{C}\|}$. Measures alignment of how the encoder represents adding the same sources to different base scenes.
- `A-TRE` — range: [-1, 1]
  - Cosine similarity between the encoder's scene embedding and a prediction made from attribute-level token vectors aggregated via a Transformer: $\frac{\langle z, \hat{z}\rangle}{\|z\|\|\hat{z}\|}$. Measures reconstructibility from compositional primitives.

## Input / output format

**Input**: A-COAT: quadruple of synthetic audio scenes $(A,B,C,D)$ where $B=A\cup T$ and $D=C\cup T$. A-TRE: single synthetic audio scene $X$ with discrete attribute metadata (timbre, pitch, rate, amplitude per source).

**Output**: Embedding vector $z_X \in \mathbb{R}^D$ produced by the audio encoder for each scene.

## Scoring recipe

```python
import numpy as np
def compute_acoat(z_A, z_B, z_C, z_D):
    d1 = z_B - z_A
    d2 = z_D - z_C
    return np.dot(d1, d2) / (np.linalg.norm(d1) * np.linalg.norm(d2))
def compute_atre(z, z_hat):
    return np.dot(z, z_hat) / (np.linalg.norm(z) * np.linalg.norm(z_hat))
```

## Common pitfalls

- A-COAT requires computing cosine similarity on difference vectors, not raw scene embeddings; direct similarity will yield incorrect alignment scores.
- A-TRE involves training a lightweight composition model $g_\theta$ on a training split before evaluation; the metric measures alignment of the predicted embedding $\hat{z}$ with ground truth $z$, not the encoder's raw output alone.
- Synthetic scenes use discrete attribute classes; inconsistent discretization or source ordering across scenes can artificially inflate or deflate A-TRE reconstruction scores.

## Evidence (verbatim from paper)

> For an encoder $f$ producing embeddings $z_{X}\=f(X)$, we evaluate whether the difference vectors $z_{B}-z_{A}$ and $z_{D}-z_{C}$ align. The A-COAT score is their cosine similarity: $\mathrm{A\text{-}COAT}(A,B,C,D)\=\frac{\langle z_{B}-z_{A},\;z_{D}-z_{C}\rangle}{\|z_{B}-z_{A}\|\,\|z_{D}-z_{C}\|}.$ The score lies in $[-1,1]$, where $1$ indicates perfect alignment... The A-TRE score for a scene is the cosine similarity between the encoder and predicted embeddings: $\mathrm{A\text{-}TRE}(X)\=\frac{\langle z,\hat{z}\rangle}{\|z\|\;\|\hat{z}\|},\qquad z\=f(X).$

## Citation

```bibtex
@misc{chen2026evaluatingcompositional,
  title={Evaluating Compositional Structure in Audio Representations},
  author={Chen et al. (2026)},
  year={2026},
  note={arXiv:2603.13685}
}
```

- arXiv: 2603.13685
