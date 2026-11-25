---
name: answer-switching-rate
description: Measures the causal influence of activation-based interventions (linear directions or multidimensional cones) on an LLM's factual reasoning. It quantifies how effectively steering or ablating specific neural subspaces switches model outputs from truthful to untruthful across a set of propositional prompts. Use when the user has predictions and gold and needs to compute Answer Switching Rate (ASR).
metadata:
  skill_kind: metric
  source_arxiv: 2505.21800
  bibtex_key: yu2025directions
  confidence: high
---

# answer-switching-rate

> From Directions to Cones: Exploring Multidimensional Representations of Propositional Facts in LLMs — Yu et al. (2025) (arXiv:2505.21800, 2025)

## What this evaluates

Measures the causal influence of activation-based interventions (linear directions or multidimensional cones) on an LLM's factual reasoning. It quantifies how effectively steering or ablating specific neural subspaces switches model outputs from truthful to untruthful across a set of propositional prompts.

## Datasets

- **ALPACA** — total 200; splits: test (200)

## Metrics

- `Answer Switching Rate (ASR)` **(primary)** — range: [0, 1]
  - The proportion of prompts whose model outputs become untruthful after an activation-based intervention. Calculated as the number of switched prompts divided by the total number of prompts (baseline assumes near-perfect initial accuracy).
- `KL Divergence` — range: [0, ∞)
  - The Kullback-Leibler divergence between the original model's output distribution and the intervened model's output distribution on general instruction prompts. Lower values indicate better retention of unrelated capabilities.
- `Cosine Similarity` — range: [-1, 1]
  - The cosine similarity between the classic DIM truth vector and each orthonormal basis vector of the discovered concept cone. Values near 1 indicate strong alignment.

## Input / output format

**Input**: Text prompts containing propositional facts (for ASR) or general instructions (for ALPACA/KL), paired with model activation vectors at specific layers and token positions for intervention.

**Output**: Model-generated text completions. Evaluated as binary truthfulness switches for ASR, or as full token probability distributions for KL divergence and cosine alignment.

## Scoring recipe

```python
def compute_asr(prompts, interventions, ground_truths):
    switched = 0
    for prompt, intervention in zip(prompts, interventions):
        output = apply_intervention(prompt, intervention)
        if not is_truthful(output, ground_truths[prompt]):
            switched += 1
    return switched / len(prompts)

def compute_kl(prompts, orig_model, int_model, n=200):
    total_kl = 0
    for prompt in prompts[:n]:
        p_orig = orig_model.generate_dist(prompt)
        p_int = int_model.generate_dist(prompt)
        total_kl += kl_divergence(p_orig, p_int)
    return total_kl / n
```

## Common pitfalls

- ASR measures the *switching* to untruthfulness, not accuracy improvement; a high ASR means the intervention successfully breaks factual consistency.
- The denominator for ASR assumes the baseline model achieves near-perfect accuracy on the factual prompts; if the model is already untruthful on some inputs, the rate should be normalized against the baseline failure count rather than total prompts.
- KL divergence is computed over the full output distribution, not just the final token, and the paper uses a strict threshold of 0.1 to discard cones that cause excessive distributional shift.

## Evidence (verbatim from paper)

> Specifically, we measure the success of activation-based interventions across multiple datasets and model families by computing the ASR - the proportion of inputs which affect model outputs after an intervention. Formally, we define the Answer Switching Rate (ASR) as: ASR = (# of prompts whose output becomes untruthful after ablation) / (baseline # of prompts that the model... In practice, the baseline is almost always the same as the total number of prompts as the models nearly always achieve full accuracy when answering our simple propositions.

## Citation

```bibtex
@misc{yu2025directions,
  title={From Directions to Cones: Exploring Multidimensional Representations of Propositional Facts in LLMs},
  author={Yu et al. (2025)},
  year={2025},
  note={arXiv:2505.21800}
}
```

- arXiv: 2505.21800
