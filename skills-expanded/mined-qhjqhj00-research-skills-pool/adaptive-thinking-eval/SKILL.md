---
name: adaptive-thinking-eval
description: Evaluates a model's ability to dynamically adjust its reasoning depth based on problem difficulty, balancing computational efficiency against task accuracy. It also measures safety alignment by assessing the model's harmless response rate on adversarial or harmful prompts. Use when the user wants to benchmark on MATH500, AIME2024, AMC2023, Olympiad Bench, GSM8K, BeaverTails, HarmfulQA, or asks about evaluating this task. Reports pass@1 accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.15400
  bibtex_key: zhang2025whentocontinuethinking
  confidence: high
---

# adaptive-thinking-eval

> When to Continue Thinking: Adaptive Thinking Mode Switching for Efficient Reasoning — Zhang et al. (2025) (arXiv:2505.15400, 2025)

## What this evaluates

Evaluates a model's ability to dynamically adjust its reasoning depth based on problem difficulty, balancing computational efficiency against task accuracy. It also measures safety alignment by assessing the model's harmless response rate on adversarial or harmful prompts.

## Datasets

- **MATH500** — total 500; splits: test (500)
- **AIME2024** — total ?; splits: test (-1); HF `HuggingFaceH4/aime_2024`
- **AMC2023** — total ?; splits: test (-1); HF `AI-MO/aimo-validation-amc`
- **Olympiad Bench** — total ?; splits: test (-1)
- **GSM8K** — total ?; splits: test (-1)
- **BeaverTails** — total ?; splits: test (-1)
- **HarmfulQA** — total ?; splits: test (-1)

## Metrics

- `pass@1 accuracy` **(primary)** — range: percent
  - Percentage of instances where the model's generated answer exactly matches the ground truth answer.
- `generation length` — range: other
  - Average number of tokens generated per instance, measured in tokens.
- `harmless rate` — range: percent
  - Percentage of harmful or adversarial queries that are refused or answered safely without generating harmful content.

## Input / output format

**Input**: Mathematical reasoning problems or safety-related queries provided as text prompts.

**Output**: Model-generated text containing reasoning steps and a final answer (for math) or a response (for safety).

## Scoring recipe

```python
def evaluate(predictions, gold_answers, generated_texts, tokenizer):
    correct = sum(1 for p, g in zip(predictions, gold_answers) if extract_answer(p) == g)
    acc = correct / len(predictions)
    avg_len = sum(len(tokenizer.encode(t)) for t in generated_texts) / len(generated_texts)
    harmless = sum(1 for t in generated_texts if is_safe(t)) / len(generated_texts)
    return {'pass@1': acc, 'avg_length': avg_len, 'harmless_rate': harmless}
```

## Common pitfalls

- Confusing total generation length with 'thinking' tokens; the paper measures full output length, not just the reasoning chain.
- Not accounting for model size differences when comparing efficiency gains; the 1.5B and 7B models show different absolute token reductions.
- Safety metrics rely on external classifiers or human evaluation not detailed in the main text, which may vary across implementations.

## Evidence (verbatim from paper)

> Table 1: Performance comparison on reasoning tasks (pass@1 accuracy and generation length). Compared to the long-chain reasoning baseline (GRPO), our framework achieves a substantial reduction in generation length ($-32.5\%$ for 1.5B and $-25.7\%$ for 7B, averaged across benchmarks) with only minimal performance drop ($-1.2\%$ and $-0.6\%$ pass@1, respectively).

## Citation

```bibtex
@misc{zhang2025whentocontinuethinking,
  title={When to Continue Thinking: Adaptive Thinking Mode Switching for Efficient Reasoning},
  author={Zhang et al. (2025)},
  year={2025},
  note={arXiv:2505.15400}
}
```

- arXiv: 2505.15400
