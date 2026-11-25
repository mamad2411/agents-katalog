---
name: armor-pruning-eval
description: Evaluates the effectiveness of semi-structured 2:4 pruning methods on large language models by measuring downstream task accuracy and language modeling perplexity. It specifically tests whether adaptive matrix factorization can preserve model capabilities better than direct weight removal while maintaining inference efficiency. Use when the user wants to benchmark on MMLU, GSM8K, BBH, GPQA, ARC-C, WinoGrande, HellaSwag, Wikitext2, C4, or asks about evaluating this task. Reports Task Accuracy (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.05528
  bibtex_key: liu2025armor
  confidence: high
---

# armor-pruning-eval

> ARMOR: High-Performance Semi-Structured Pruning via Adaptive Matrix Factorization — Liu et al. (2025) (arXiv:2510.05528, 2025)

## What this evaluates

Evaluates the effectiveness of semi-structured 2:4 pruning methods on large language models by measuring downstream task accuracy and language modeling perplexity. It specifically tests whether adaptive matrix factorization can preserve model capabilities better than direct weight removal while maintaining inference efficiency.

## Datasets

- **MMLU** — total ?; splits: test (-1)
- **GSM8K** — total ?; splits: test (-1)
- **BBH** — total ?; splits: test (-1)
- **GPQA** — total ?; splits: test (-1)
- **ARC-C** — total ?; splits: test (-1)
- **WinoGrande** — total ?; splits: test (-1)
- **HellaSwag** — total ?; splits: test (-1)
- **Wikitext2** — total ?; splits: test (-1)
- **C4** — total ?; splits: validation (-1)

## Metrics

- `Task Accuracy (%)` **(primary)** — range: percent
  - Percentage of correctly answered multiple-choice or open-ended questions across seven downstream benchmarks.
- `Perplexity` — range: other
  - Exponential of the average negative log-likelihood of the ground-truth tokens in the language modeling dataset.

## Input / output format

**Input**: Pruned model weights (2:4 semi-structured sparsity with block-diagonal wrappers) and input prompts/text for each benchmark instance.

**Output**: Predicted tokens or selected options for each benchmark instance.

## Scoring recipe

```python
def compute_metrics(predictions, gold, log_probs=None):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    accuracy = (correct / len(gold)) * 100
    perplexity = None
    if log_probs is not None:
        import math
        avg_nll = -sum(log_probs) / len(log_probs)
        perplexity = math.exp(avg_nll)
    return {'Task Accuracy (%)': accuracy, 'Perplexity': perplexity}
```

## Common pitfalls

- The paper notes that ARMOR pruned models have a small relative overhead (2–5%) due to block diagonal matrices, which should not be confused with standard 2:4 sparsity memory savings.
- Perplexity evaluations use different context lengths depending on the model family (4096 for Llama-2, 8192 for Llama-3), which must be matched when reproducing results.
- Evaluations are strictly on base models (pre-training only), excluding instruction-tuned or MoE variants, so results do not generalize to post-trained architectures.

## Evidence (verbatim from paper)

> To comprehensively assess performance degradation, we employed a two-pronged evaluation strategy. First, to measure practical performance on downstream tasks, we evaluated the pruned Qwen models on a suite of seven industry-standard benchmarks using the LM Eval Harness (Gao et al., [2024]). These benchmarks cover a range of capabilities, including commonsense and complex reasoning, mathematical problem-solving, and world knowledge. A detailed description of each benchmark is available in Appendix (F). Second, to ensure comparability with the broader model compression literature, which often relies on perplexity metrics, we conducted an additional set of experiments. For this, we pruned models from the Llama-2 (7B, 13B, and 70B) (Touvron et al., [2023]) and Llama-3 (8B and 70B) (Dubey et al., [2024]) families. We then evaluated their perplexity on the test split of Wikitext2 (Merity et al., [2016]) and a subset of the C4 validation split (Dodge et al., [2021]), following standard evaluation protocols in the field.

## Citation

```bibtex
@misc{liu2025armor,
  title={ARMOR: High-Performance Semi-Structured Pruning via Adaptive Matrix Factorization},
  author={Liu et al. (2025)},
  year={2025},
  note={arXiv:2510.05528}
}
```

- arXiv: 2510.05528
