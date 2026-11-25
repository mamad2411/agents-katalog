---
name: hypothesis-and-evidence
description: Structured scientific hypothesis testing. Systematically juxtaposes supporting evidence, contrary findings, and unresolved ambiguities.
license: MIT
---

# Hypothesis and Evidence Matrix

Use this skill when evaluating a scientific assertion, architectural trade-off, or competing methodology.

## Framework

For each central thesis or design hypothesis, produce the following structure:

### 1. Statement of Hypothesis
A falsifiable claim (e.g., "TopK Sparse Autoencoders eliminate feature shrinkage and dead latents without requiring warm-up schedules").

### 2. Supporting Evidence
- Empirical results citing primary papers.
- Datasets, baseline models, and specific metrics (e.g., CE loss recovered, L0 sparsity).

### 3. Contradicting / Inconclusive Evidence
- Literature reports showing failure modes (e.g., higher inference latency, gradient vanishing, sensitivity to k).
- Negative results or contexts where alternative architectures (e.g., Gated SAEs or JumpreLU) outperform.

### 4. Verdict & Design Recommendation
- Concrete guidance for engineering implementation: when to adopt, what safeguards to add, and what hyperparameter ranges to sweep.
