---
name: 3dmem-bench-eval
description: Evaluates an embodied 3D agent's ability to manage long-term spatial-temporal memory and execute complex, multi-room tasks. It probes the model's capacity for in-domain generalization, in-the-wild robustness, and long-horizon reasoning across navigation, question answering, and scene captioning. Use when the user wants to benchmark on 3DMem-Bench, or asks about evaluating this task. Reports success rate (SR).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.22657
  bibtex_key: hu20253dllmmem
  confidence: high
---

# 3dmem-bench-eval

> 3DLLM-Mem: Long-Term Spatial-Temporal Memory for Embodied 3D Large Language Model — Wenbo Hu et al. (2025) (arXiv:2505.22657, 2025)

## What this evaluates

Evaluates an embodied 3D agent's ability to manage long-term spatial-temporal memory and execute complex, multi-room tasks. It probes the model's capacity for in-domain generalization, in-the-wild robustness, and long-horizon reasoning across navigation, question answering, and scene captioning.

## Datasets

- **3DMem-Bench** — total 26000; splits: train (-1), test (-1)

## Metrics

- `success rate (SR)` **(primary)** — range: percent
  - Percentage of tasks where the agent successfully completes the specified objective. Calculated as (number of successful executions / total number of tasks) * 100.
- `sub-success rate (Sub-SR)` — range: percent
  - Percentage of tasks where the agent successfully completes a sub-goal or intermediate step within a multi-step task.
- `accuracy` — range: percent
  - Proportion of correctly answered open-ended EQA questions, evaluated using an LLM-as-judge protocol with Gemini.
- `BLEU-1 / BLEU-4 / METEOR` — range: [0, 100]
  - Standard n-gram overlap and METEOR scores between generated captions and ground-truth references.

## Input / output format

**Input**: Task instructions, current working memory state, and fused spatial-temporal features from dense 3D episodic memory, formatted as token sequences up to an 8192-token context window.

**Output**: Action execution trajectories for embodied tasks, or natural language responses for EQA and captioning tasks.

## Scoring recipe

```python
def compute_sr(predictions, golds):
    correct = sum(1 for p, g in zip(predictions, golds) if p == g)
    return (correct / len(golds)) * 100

def compute_eqa_accuracy(predictions, golds):
    # LLM-as-judge with Gemini evaluates open-ended answers
    scores = [judge_score(p, g) for p, g in zip(predictions, golds)]
    return (sum(scores) / len(scores)) * 100

def compute_captioning_metrics(predictions, golds):
    return compute_bleu_meteor(predictions, golds)
```

## Common pitfalls

- Confusing 'in-domain' vs 'in-the-wild' test splits, as baseline performance drops sharply in the latter due to distribution shift.
- Assuming 'Everything in Context' is a practical baseline; the 8192-token limit makes it infeasible for long-horizon, multi-room scenarios.
- LLM-as-judge evaluation for EQA relies on specific Gemini prompts, which may introduce bias or variance compared to exact-match metrics.

## Evidence (verbatim from paper)

> As shown in Table[2(a)], 3DLLM-Mem significantly outperforms all existing approaches on both in-domain and in-the-wild embodied tasks. Notably, while the performance of other methods drops sharply in the in-the-wild setting, our method demonstrates strong generalization capabilities with a average success rate of 32.1%.

## Citation

```bibtex
@misc{hu20253dllmmem,
  title={3DLLM-Mem: Long-Term Spatial-Temporal Memory for Embodied 3D Large Language Model},
  author={Wenbo Hu et al. (2025)},
  year={2025},
  note={arXiv:2505.22657}
}
```

- arXiv: 2505.22657
