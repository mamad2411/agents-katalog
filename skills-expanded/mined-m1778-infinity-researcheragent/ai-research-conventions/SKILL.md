---
name: ai-research-conventions
description: AI/Machine Learning research conventions, standard evaluation suites, benchmark tracking, and model card formats.
license: MIT
---

# AI Research Conventions

Guidelines for generating AI/ML engineering specifications that software engineers and ML practitioners can directly implement.

## Required Technical Specification Sections

1. **Mathematical Formulation**: Formal definitions of the forward pass, loss objective, and regularization terms.
2. **Model Geometry**: Tensor shapes across all stages (Input $\to$ Latents $\to$ Reconstruction $\to$ Output).
3. **Training Recipe**: Token budgeting, batch size, learning rates, gradient clipping, precision (bf16/fp16/fp32).
4. **Implementation Reference**: Link to canonical open-source repositories and verified reference implementations.
5. **Steering & Downstream Intervention**: How learned representations or weights are manipulated at runtime (e.g., activation patching, feature clamping).
