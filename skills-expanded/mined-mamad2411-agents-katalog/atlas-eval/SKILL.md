---
name: atlas-eval
description: This benchmark probes frontier scientific reasoning across multiple disciplines (e.g., physics, chemistry, biology, computer science, mathematics) using original, multi-step problems. It evaluates a model's ability to generate complex, open-ended, LaTeX-formatted answers and assesses both solution accuracy and inference stability across multiple sampling runs. Use when the user wants to benchmark on ATLAS, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.14366
  bibtex_key: liu2025atlas
  confidence: high
---

# atlas-eval

> ATLAS: A High-Difficulty, Multidisciplinary Benchmark for Frontier Scientific Reasoning — Liu et al. (2025) (arXiv:2511.14366, 2025)

## What this evaluates

This benchmark probes frontier scientific reasoning across multiple disciplines (e.g., physics, chemistry, biology, computer science, mathematics) using original, multi-step problems. It evaluates a model's ability to generate complex, open-ended, LaTeX-formatted answers and assesses both solution accuracy and inference stability across multiple sampling runs.

## Datasets

- **ATLAS** — total 800; splits: val (-1), test (-1); repo https://github.com/open-compass/ATLAS

## Metrics

- `Accuracy` **(primary)** — range: percent
  - Average accuracy across multiple inferences. Calculated as the total number of correctly judged predictions divided by the total number of generated predictions (typically 4 per question), multiplied by 100.
- `mG-Pass@k` — range: percent
  - A stability metric adapted from G-Pass@k. It measures the proportion of questions where at least one of the first k predictions is judged correct by the LLM-as-Judge. Commonly reported at k=2 and k=4.

## Input / output format

**Input**: A complex, multi-step scientific question requiring open-ended, LaTeX-formatted answers, often containing multiple sub-questions.

**Output**: Step-by-step reasoning followed by a final answer strictly formatted in JSON.

## Scoring recipe

```python
predictions = generate_answers(question, n=4)
parsed_answers = parse_json(predictions)
judgments = []
for ans in parsed_answers:
    judge_output = judge_llm(question, ans, ground_truth)
    judgments.append(parse_json(judge_output)['correct'])
accuracy = sum(judgments) / (len(judgments) * num_questions) * 100
mG_Pass_k = sum(1 for q in range(num_questions) if any(judgments[q][:k])) / num_questions * 100
```

## Common pitfalls

- Output truncation or invalid JSON formatting can cause answer extraction failures, artificially lowering reported accuracy if not filtered.
- LLM-as-Judge scores are highly sensitive to the specific judge model used; switching judges (e.g., Qwen3 vs GPT-OSS-120B) can shift accuracy scores by 3-5%.
- Numerical tolerance thresholds must be explicitly defined in judge prompts, as strict exact-match evaluation incorrectly penalizes valid scientific approximations.

## Evidence (verbatim from paper)

> Referencing typical reasoning tasks such as code and mathematics, we report the average accuracy across multiple inferences and G-Pass@$k$ to assess the stability of LLMs’ performance.

## Citation

```bibtex
@misc{liu2025atlas,
  title={ATLAS: A High-Difficulty, Multidisciplinary Benchmark for Frontier Scientific Reasoning},
  author={Liu et al. (2025)},
  year={2025},
  note={arXiv:2511.14366}
}
```

- arXiv: 2511.14366
