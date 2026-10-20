---
name: amega-clinical-reasoning-eval
description: Evaluates the clinical reasoning capabilities and on-device runtime efficiency of various LLMs using the AMEGA benchmark. It measures response accuracy via an LLM-as-a-judge scoring system and tracks inference throughput and thermal throttling effects across different mobile hardware configurations. Use when the user wants to benchmark on AMEGA, or asks about evaluating this task. Reports AMEGA score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2502.08954
  bibtex_key: nissen2025medicineontheedge
  confidence: medium
---

# amega-clinical-reasoning-eval

> Medicine on the Edge: Comparative Performance Analysis of On-Device LLMs for Clinical Reasoning — Nissen et al. (2025) (arXiv:2502.08954, 2025)

## What this evaluates

Evaluates the clinical reasoning capabilities and on-device runtime efficiency of various LLMs using the AMEGA benchmark. It measures response accuracy via an LLM-as-a-judge scoring system and tracks inference throughput and thermal throttling effects across different mobile hardware configurations.

## Datasets

- **AMEGA** — total ?; splits: test (-1); repo https://github.com/StanfordBDHG/HealthBench

## Metrics

- `AMEGA score` **(primary)** — range: other
  - Mean score assigned by GPT-4o to model-generated responses on clinical cases and questions, averaged across all compatible device runs.
- `output tokens per second` — range: tokens/sec
  - Inference throughput calculated as the number of generated output tokens divided by total inference time, reported as minimum and maximum values across tested devices.

## Input / output format

**Input**: Clinical reasoning cases and questions from the AMEGA dataset, processed by on-device LLMs for text generation.

**Output**: Generated text responses from the LLMs, which are subsequently fed into GPT-4o for automated evaluation.

## Scoring recipe

```python
responses = run_models_on_devices(amega_dataset)
judge_scores = []
for resp in responses:
    score = gpt4o_judge(resp)
    judge_scores.append(score)
omega_score = mean(judge_scores)
throughput = count_tokens(resp) / inference_time
```

## Common pitfalls

- Memory constraints on older iOS devices often prevent larger models from running, leading to missing data or forced exclusions (e.g., MedFound 8B).
- Thermal throttling significantly degrades throughput (up to 55% drop in 'serious' state), which must be accounted for when comparing runtime performance.
- iOS enforces a strict 2.25 GB memory limit that terminates applications exceeding it, regardless of theoretical model footprint.

## Evidence (verbatim from paper)

> Table 3 presents the mean AMEGA scores for each model, categorized by type and size. The mean score was computed across all model runs on compatible devices.

## Citation

```bibtex
@misc{nissen2025medicineontheedge,
  title={Medicine on the Edge: Comparative Performance Analysis of On-Device LLMs for Clinical Reasoning},
  author={Nissen et al. (2025)},
  year={2025},
  note={arXiv:2502.08954}
}
```

- arXiv: 2502.08954
