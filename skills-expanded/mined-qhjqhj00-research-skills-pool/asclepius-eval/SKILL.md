---
name: asclepius-eval
description: This benchmark evaluates the clinical reasoning, perception, and diagnostic capabilities of multi-modal large language models across 15 medical specialties. It probes tasks ranging from anatomical and attribute perception to disease identification, staging, treatment planning, and medical report generation. Use when the user wants to benchmark on Asclepius, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.11217
  bibtex_key: wang2024asclepius
  confidence: high
---

# asclepius-eval

> A Spectrum Evaluation Benchmark for Medical Multi-Modal Large Language Models — Wang et al. (2024) (arXiv:2402.11217, 2024)

## What this evaluates

This benchmark evaluates the clinical reasoning, perception, and diagnostic capabilities of multi-modal large language models across 15 medical specialties. It probes tasks ranging from anatomical and attribute perception to disease identification, staging, treatment planning, and medical report generation.

## Datasets

- **Asclepius** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Proportion of correct answers for multiple-choice and yes/no questions, calculated as the number of matches divided by the total number of instances.
- `Exact Match` — range: [0, 1]
  - Binary score indicating whether the model's generated text exactly matches the gold standard answer, used for open-ended questions.
- `ROUGE-L` — range: [0, 1]
  - Recall-oriented overlap of the longest common subsequence between the generated medical report and the gold-standard reference text.

## Input / output format

**Input**: A system prompt instructing the model to act as a professional doctor, followed by a clinical question and one or two medical images.

**Output**: A direct answer to the question without reasoning or additional information. Format depends on task type: choice/text for MC/YesNo, exact string for open-ended, or free-form text for report generation.

## Scoring recipe

```python
def score(predictions, golds, task_type):
    if task_type in ['multiple_choice', 'yes_no']:
        return sum(p == g for p, g in zip(predictions, golds)) / len(golds)
    elif task_type == 'open_ended':
        return sum(p.strip() == g.strip() for p, g in zip(predictions, golds)) / len(golds)
    elif task_type == 'report_generation':
        return rouge_l_score(predictions, golds)
```

## Common pitfalls

- Models may refuse to generate report generation outputs due to built-in safety guidelines, leading to missing scores (e.g., GPT-4V).
- Exact Match for open-ended medical questions can be overly strict, penalizing semantically correct but syntactically different clinical terminology.
- Data contamination is a major concern; models pre-trained on medical corpora may have seen the benchmark data, inflating performance.

## Evidence (verbatim from paper)

> Asclepius includes a range of question types: multiple choice, yes/no, open-ended questions, and report generation tasks. We adopt accuracy as metric for multiple-choice questions and yes/no questions. Moreover, open-ended questions demand a more subtle assessment approach; here, the Exact Match metric is utilized to measure the precision of the textual responses due to its stability and rigor. For the evaluation of report generation, the ROUGE-L scoring system is employed to determine the extent to which the models’ generated texts align with the gold-standard reports. Accuracy and Exact Match results can be utilized to calculate the accuracy score, and ROUGE-L scores are directly reported.

## Citation

```bibtex
@misc{wang2024asclepius,
  title={A Spectrum Evaluation Benchmark for Medical Multi-Modal Large Language Models},
  author={Wang et al. (2024)},
  year={2024},
  note={arXiv:2402.11217}
}
```

- arXiv: 2402.11217
