---
name: 3mdbench-eval
description: Evaluates Large Vision-Language Models in realistic telemedicine consultations by simulating multi-agent dialogues between a doctor and a temperament-based patient. It probes diagnostic accuracy from multimodal inputs (images + text) and assesses clinical competence and dialogue quality. Use when the user wants to benchmark on 3MDBench, or asks about evaluating this task. Reports F1 Score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2504.13861
  bibtex_key: sviridov20253mdbench
  confidence: high
---

# 3mdbench-eval

> 3MDBench: Medical Multimodal Multi-agent Dialogue Benchmark — Sviridov et al. (2025) (arXiv:2504.13861, 2025)

## What this evaluates

Evaluates Large Vision-Language Models in realistic telemedicine consultations by simulating multi-agent dialogues between a doctor and a temperament-based patient. It probes diagnostic accuracy from multimodal inputs (images + text) and assesses clinical competence and dialogue quality.

## Datasets

- **3MDBench** — total ?; splits: train (-1), val (-1); repo https://github.com/univanxx/3mdbench

## Metrics

- `F1 Score` **(primary)** — range: percent
  - Computed between diagnoses extracted by the LVLM and human-extracted ground truth diagnoses. Standard precision/recall F1 for diagnosis extraction.
- `Cohen's Kappa` — range: [0, 1]
  - Measures agreement between the Assessor Agent and human annotations across dialogue criteria. Averaged across criteria to determine overall agreement.

## Input / output format

**Input**: Multimodal input per instance: patient medical image(s) + text dialogue history (complaints, symptoms, follow-ups). Doctor agent may also receive rationale or external diagnostic cues (e.g., top-3 ConvNet predictions).

**Output**: Text output containing extracted diagnosis(es) and clinical recommendations. Dialogue turns are generated iteratively by the Doctor Agent (max 512 tokens, temp 0.6).

## Scoring recipe

```python
pred_diagnoses = extract_diagnoses(model_output)
gold_diagnoses = human_ground_truth
tp = len(set(pred_diagnoses) & set(gold_diagnoses))
fp = len(set(pred_diagnoses) - set(gold_diagnoses))
fn = len(set(gold_diagnoses) - set(pred_diagnoses))
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
# Statistical testing
p_value = wilcoxon_signed_rank_test(metric_values_group1, metric_values_group2)
adjusted_p = benjamini_hochberg_fdr_control(p_values, alpha=0.01)
```

## Common pitfalls

- Models often miss key symptoms or terminate questioning prematurely, unlike human clinicians who adaptively probe.
- Performance heavily depends on disease category (e.g., dermatology F1 ~47% vs throat/mucosae ~86%) and patient temperament (phlegmatic patients yield lower scores due to brevity).
- Rationale generation improves diagnostic F1 but can decrease clinical competence scores, indicating a trade-off between internal reasoning and applied communication skills.

## Evidence (verbatim from paper)

> For the diagnosis extraction task, we computed the F1 score of the diagnoses identified by the LVLM, using human-extracted diagnoses as the ground truth. To estimate the dialogue closeness, we calculated Cohen’s Kappa for each criterion from Table[2] and averaged the scores to determine overall agreement.

## Citation

```bibtex
@misc{sviridov20253mdbench,
  title={3MDBench: Medical Multimodal Multi-agent Dialogue Benchmark},
  author={Sviridov et al. (2025)},
  year={2025},
  note={arXiv:2504.13861}
}
```

- arXiv: 2504.13861
