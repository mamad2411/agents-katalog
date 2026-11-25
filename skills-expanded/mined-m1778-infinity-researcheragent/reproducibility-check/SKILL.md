---
name: reproducibility-check
description: Reproducibility and sanity verification protocols for algorithmic claims, data pipelines, and mathematical formulations.
license: MIT
---

# Reproducibility Verification Protocol

Use this skill when auditing a paper's reproducibility or writing a technical implementation spec.

## Checklist

1. **Architecture & Equations**:
   - Are layer dimensions ($d_{\text{model}}$, $d_{\text{sae}}$, expansion factor) explicitly specified?
   - Are activation functions (ReLU, TopK, Gated, JumpreLU) formulated mathematically?
   - Are weight initialization schemes (e.g., normalized columns of decoder, orthogonal init) documented?

2. **Training Dynamics**:
   - Optimizer (Adam, AdamW) and hyperparameters ($\beta_1$, $\beta_2$, $\epsilon$, weight decay).
   - Learning rate schedule (warmup steps, decay schedule, peak LR).
   - Sparsity penalty coefficients ($\lambda$) or target sparsity ($k$).
   - Batch size in tokens and total training token volume.

3. **Evaluation Protocol**:
   - Reconstruction fidelity metrics: Fraction of variance explained (FVU), Cross-Entropy loss recovery.
   - Sparsity metrics: $L_0$ norm (active features per token).
   - Interpretability metrics: Auto-interpretability score, downstream steering efficacy.
