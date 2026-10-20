---
name: adversarial-text-attack-eval
description: Evaluates the robustness of BERT-based text classifiers against word-level adversarial attacks by measuring how well perturbed inputs maintain semantic meaning and syntactic structure while successfully flipping model predictions. It compares three attack methods across three standard classification benchmarks to determine the optimal balance between attack success, semantic preservation, and computational efficiency. Use when the user wants to benchmark on IMDB, AG News, SST2, or asks about evaluating this task. Reports Attack Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2404.05159
  bibtex_key: dey2024semanticstealth
  confidence: low
---

# adversarial-text-attack-eval

> Semantic Stealth: Adversarial Text Attacks on NLP Using Several Methods — Dey et al. (2024) (arXiv:2404.05159, 2024)

## What this evaluates

Evaluates the robustness of BERT-based text classifiers against word-level adversarial attacks by measuring how well perturbed inputs maintain semantic meaning and syntactic structure while successfully flipping model predictions. It compares three attack methods across three standard classification benchmarks to determine the optimal balance between attack success, semantic preservation, and computational efficiency.

## Datasets

- **IMDB** — total ?; splits: train (-1), test (-1)
- **AG News** — total ?; splits: train (-1), test (-1)
- **SST2** — total ?; splits: train (-1), test (-1)

## Metrics

- `Attack Accuracy` **(primary)** — range: percent
  - Percentage of adversarially perturbed inputs that are misclassified by the target BERT-based classifier compared to the original clean inputs.
- `Perturbation Minimization` — range: other
  - Average number or percentage of words replaced or modified per input to achieve the attack goal.
- `Runtime` — range: other
  - Wall-clock time required to generate adversarial examples for a given dataset split.
- `Syntactic Coherence` — range: other
  - Qualitative or automated score measuring whether the perturbed text maintains grammatical correctness and human readability.

## Input / output format

**Input**: Clean text samples from IMDB, AG News, and SST2 datasets fed into pre-trained BERT-based text classifiers.

**Output**: Adversarially perturbed text samples, original and perturbed classification predictions, and computed evaluation scores for each attack method.

## Scoring recipe

```python
def evaluate_attack(clean_texts, perturbed_texts, model, gold_labels):
    correct_original = sum(1 for t, g in zip(clean_texts, gold_labels) if model.predict(t) == g)
    correct_perturbed = sum(1 for t, g in zip(perturbed_texts, gold_labels) if model.predict(t) != g)
    attack_accuracy = (correct_perturbed / len(clean_texts)) * 100
    perturbation_count = [count_word_changes(c, p) for c, p in zip(clean_texts, perturbed_texts)]
    runtime = time_taken_to_generate(perturbed_texts)
    return attack_accuracy, perturbation_count, runtime
```

## Common pitfalls

- Confusing semantic preservation with syntactic coherence; a perturbed sentence can be grammatically correct but semantically altered.
- Failing to normalize perturbation counts by input length, which biases results toward shorter documents.
- Assuming all three attack methods use identical perturbation budgets or stopping criteria without verifying implementation details.

## Evidence (verbatim from paper)

> This study evaluates three word-level adversarial attack methods—BERT-on-BERT, PWWS, and Fraud Bargain's Attack (FBA)—on BERT-based text classifiers using IMDB, AG News, and SST2 datasets. PWWS outperforms the others in generating semantically similar, high-accuracy adversarial examples with minimal perturbation, lower runtime, and better syntactic coherence, demonstrating superior effectiveness in maintaining human readability while misclassifying inputs.

## Citation

```bibtex
@misc{dey2024semanticstealth,
  title={Semantic Stealth: Adversarial Text Attacks on NLP Using Several Methods},
  author={Dey et al. (2024)},
  year={2024},
  note={arXiv:2404.05159}
}
```

- arXiv: 2404.05159
