---
name: astrovisbench-eval
description: Evaluates large language models' ability to act as coding assistants for astronomy-specific scientific workflows. It probes domain-specific API usage, data manipulation, and the generation of research-standard visualizations from natural language queries. Use when the user wants to benchmark on AstroVisBench, or asks about evaluating this task. Reports execution-based evaluation.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2505.20538
  bibtex_key: joseph2025astrovisbench
  confidence: medium
---

# astrovisbench-eval

> AstroVisBench: A Code Benchmark for Scientific Computing and Visualization in Astronomy — Joseph et al. (2025) (arXiv:2505.20538, 2025)

## What this evaluates

Evaluates large language models' ability to act as coding assistants for astronomy-specific scientific workflows. It probes domain-specific API usage, data manipulation, and the generation of research-standard visualizations from natural language queries.

## Datasets

- **AstroVisBench** — total ?; splits: test (-1); repo https://github.com/astro-datalab/notebooks-latest

## Metrics

- `execution-based evaluation` **(primary)** — range: [0, 1]
  - Compares key variables from executing the predicted code alongside setup code against an expected result y. Returns a boolean or score based on variable match.
- `LLM-as-a-judge` — range: [0, 1]
  - An LLM scores the quality of the generated visualization based on the predicted code and setup, validated against expert annotations.

## Input / output format

**Input**: Setup code cells (c_{1...j}) and a natural language query (q) describing the functionality of the core cells.

**Output**: A predicted code cell (ĉ) intended to perform the requested data processing or visualization task.

## Scoring recipe

```python
def score_processing(setup_code, predicted_code, expected_result):
    exec(setup_code + predicted_code)
    return compare_variables(globals(), expected_result)

def score_visualization(predicted_code, setup_code):
    prompt = f'Setup: {setup_code}\nPredicted Code: {predicted_code}\nRate visualization quality.'
    return llm_judge_score(prompt)
```

## Common pitfalls

- Queries often underspecify data file names or subjective filtering thresholds, requiring explicit clarifications to be appended during evaluation.
- Execution-based evaluation only checks key variables, not full code correctness, side effects, or proper error handling.
- LLM-as-a-judge scores for visualization quality require careful validation against human experts to mitigate model bias.

## Evidence (verbatim from paper)

> It proposes execution-based evaluation for processing tasks (comparing key variables) and a novel LLM-as-a-judge system validated against expert annotations for visualization quality, revealing significant gaps in LLMs' ability to handle domain-specific APIs, data manipulation, and research-standard visualizations.

## Citation

```bibtex
@misc{joseph2025astrovisbench,
  title={AstroVisBench: A Code Benchmark for Scientific Computing and Visualization in Astronomy},
  author={Joseph et al. (2025)},
  year={2025},
  note={arXiv:2505.20538}
}
```

- arXiv: 2505.20538
