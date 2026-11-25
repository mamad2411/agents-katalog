---
name: spec-to-code-transcription
description: High-fidelity transcription protocol from research literature and architecture specifications into clean, production-grade, bug-free implementation code.
license: MIT
---

# Specification to Production Code Transcription Protocol

This skill guides the translation of mathematical formulas, research pseudocode, or architectural specifications into production-ready implementation code.

## Transcription Rules

### 1. Mathematical Equation Translation
- Always document the original equation in code comments alongside the implementation.
  ```typescript
  // Loss = (1/2) * ||x - x_hat||_2^2 + lambda * ||f(x)||_1
  const reconstructionError = 0.5 * l2NormSquared(input, reconstructed);
  const sparsityLoss = lambda * l1Norm(latentActivations);
  const totalLoss = reconstructionError + sparsityLoss;
  ```
- Ensure tensor broadcast semantics, dimension ordering (e.g., `[batch, seq_len, d_model]`), and reduction operations align exactly with the paper's specification.

### 2. Numerical Stability Safeguards
- Always protect divisions with an epsilon term:
  ```typescript
  const variance = computeVariance(activations);
  const normalized = (activations - mean) / Math.sqrt(variance + 1e-8);
  ```
- Avoid unconstrained exponential operations; use log-sum-exp or clamp inputs when operating in extreme dynamic ranges.

### 3. Hyperparameter Explicit Typing
- Never hardcode magic numbers without named constants and domain units:
  ```typescript
  const LEARNING_RATE_WARMUP_STEPS = 1000; // steps
  const ADAM_BETA1 = 0.9;
  const ADAM_BETA2 = 0.999;
  const TOP_K_ACTIVE_LATENTS = 32;         // features per token
  ```

### 4. Interface Conformance
- Export strict TypeScript types for all request and response structures.
- Ensure every public function has full return type annotations and explicit parameter checks.
