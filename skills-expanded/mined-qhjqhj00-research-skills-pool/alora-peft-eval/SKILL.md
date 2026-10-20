---
name: alora-peft-eval
description: Evaluates the effectiveness of dynamic low-rank adaptation (LoRA) for fine-tuning large language models across classification, question answering, and instruction generation tasks. It measures how well rank allocation strategies preserve performance while maintaining or reducing tunable parameter counts. Use when the user wants to benchmark on SQuAD, BoolQ, COPA, ReCoRD, SST-2, RTE, QNLI, Alpaca, MT-Bench, E2E, or asks about evaluating this task. Reports accuracy, GPT-4 score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2403.16187
  bibtex_key: liu2024alora
  confidence: high
---

# alora-peft-eval

> ALoRA: Allocating Low-Rank Adaptation for Fine-tuning Large Language Models — Liu et al. (2024) (arXiv:2403.16187, 2024)

## What this evaluates

Evaluates the effectiveness of dynamic low-rank adaptation (LoRA) for fine-tuning large language models across classification, question answering, and instruction generation tasks. It measures how well rank allocation strategies preserve performance while maintaining or reducing tunable parameter counts.

## Datasets

- **SQuAD** — total ?; splits: test (-1)
- **BoolQ** — total ?; splits: test (-1)
- **COPA** — total ?; splits: test (-1)
- **ReCoRD** — total ?; splits: test (-1)
- **SST-2** — total ?; splits: test (-1)
- **RTE** — total ?; splits: test (-1)
- **QNLI** — total ?; splits: test (-1)
- **Alpaca** — total ?; splits: test (-1)
- **MT-Bench** — total ?; splits: test (-1)
- **E2E** — total ?; splits: test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Proportion of correctly predicted class labels or boolean answers out of total instances.
- `f1-em` — range: percent
  - F1 score computed over exact match (EM) between predicted and ground-truth answers, standard for QA benchmarks.
- `BLEU` — range: percent
  - N-gram precision score with brevity penalty for machine translation and text generation tasks.
- `ROUGE-L` — range: percent
  - Longest common subsequence recall/precision score for evaluating generated text similarity.
- `METEOR` — range: percent
  - Metric combining unigram precision, recall, and alignment penalties, tuned for human correlation in generation.
- `GPT-4 score` **(primary)** — range: [0, 10]
  - Average score assigned by GPT-4 acting as an automated judge on instruction-following quality, following standard MT-Bench protocol.

## Input / output format

**Input**: Text prompts or instructions formatted for the language modeling (LM) head. Classification and QA tasks use standard prompt templates; instruction tuning uses Alpaca-style prompts.

**Output**: Generated text or class labels via LM head decoding. Inference uses beam search with beam size 5.

## Scoring recipe

```python
def compute_metrics(predictions, golds, task_type):
    if task_type in ['SST-2', 'RTE', 'QNLI', 'BoolQ', 'COPA']:
        return sum(p == g for p, g in zip(predictions, golds)) / len(golds) * 100
    elif task_type in ['ReCoRD', 'SQuAD']:
        em = sum(p == g for p, g in zip(predictions, golds)) / len(golds) * 100
        f1 = compute_f1(predictions, golds) * 100
        return (f1 + em) / 2
    elif task_type == 'E2E':
        return bleu_score(predictions, golds) * 100, rouge_l(predictions, golds) * 100, meteor_score(predictions, golds) * 100
    elif task_type == 'MT-Bench':
        return gpt4_judge_score(predictions, golds)
    return 0
```

## Common pitfalls

- Exact prompt templates and dataset splits are deferred to Appendix B, so readers must verify task-specific formatting before reproducing.
- Performance is reported as the median over five random seeds, not the mean ± standard deviation, which can mask variance.
- MT-Bench evaluation relies on GPT-4 as an automated judge, which may introduce scorer bias or inconsistency compared to human evaluation.

## Evidence (verbatim from paper)

> For the E2E benchmark Novikova et al. (2017), the results are reported in Table 2. The results show that on the E2E task, our ALoRA method successfully outperforms LoRA and SoRA regarding BLEU, ROUGE-L, or METEOR scores. We run each task under five different random seeds and report the median performance on the test set of each task.

## Citation

```bibtex
@misc{liu2024alora,
  title={ALoRA: Allocating Low-Rank Adaptation for Fine-tuning Large Language Models},
  author={Liu et al. (2024)},
  year={2024},
  note={arXiv:2403.16187}
}
```

- arXiv: 2403.16187
