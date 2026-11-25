---
name: astrochart-eval
description: Evaluates multimodal large language models' ability to comprehend scientific charts and perform knowledge-intensive reasoning in astronomy. It probes visual understanding, data extraction, numerical calculation, and domain-specific inference. Use when the user wants to benchmark on AstroChart, or asks about evaluating this task. Reports Accuracy (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.19498
  bibtex_key: lu2025domaincqa
  confidence: high
---

# astrochart-eval

> DomainCQA: Crafting Knowledge-Intensive QA from Domain-Specific Charts — Lu et al. (2025) (arXiv:2503.19498, 2025)

## What this evaluates

Evaluates multimodal large language models' ability to comprehend scientific charts and perform knowledge-intensive reasoning in astronomy. It probes visual understanding, data extraction, numerical calculation, and domain-specific inference.

## Datasets

- **AstroChart** — total 1690; splits: test (1690)

## Metrics

- `Accuracy (%)` **(primary)** — range: percent
  - Percentage of correctly answered questions. Numerical answers are scored via exact match (derivation) or relative error normalized by axis range (retrieval). Open-ended answers are scored 0-1 by an LLM judge based on relevance, correctness, and completeness.

## Input / output format

**Input**: A chart image and a corresponding question (fundamental or advanced).

**Output**: A numerical value or a free-text answer.

## Scoring recipe

```python
def compute_accuracy(predictions, golds, task_types):
    correct = 0
    for pred, gold, t in zip(predictions, golds, task_types):
        if t == 'numerical':
            if 'derivation' in gold:
                correct += (pred == gold)
            else:
                rel_err = abs(pred - gold) / (gold_max - gold_min)
                correct += (rel_err <= 0.05) # threshold per paper's convention
        else:
            score = llm_judge_score(pred, gold) # 0 to 1
            correct += (score >= 0.5)
    return correct / len(predictions) * 100
```

## Common pitfalls

- Models often return full axis ranges instead of specific intervals for retrieval tasks.
- OCR errors and limited math skills cause significant drops in calculation accuracy.
- LLM judge scores may vary; human validation is recommended for reliability.

## Evidence (verbatim from paper)

> We assess the accuracy of model outputs for both numerical and open-ended questions (details in Appendix K). For numerical responses, we computed relative error normalized by the axis range for retrieval tasks, and required an exact match for derivation tasks such as counting or arithmetic. For open-ended responses, an LLM judge (DeepSeek-V3) assigned scores from 0 to 1 based on relevance, correctness, and completeness, following Liu et al. ([2023c]).

## Citation

```bibtex
@misc{lu2025domaincqa,
  title={DomainCQA: Crafting Knowledge-Intensive QA from Domain-Specific Charts},
  author={Lu et al. (2025)},
  year={2025},
  note={arXiv:2503.19498}
}
```

- arXiv: 2503.19498
