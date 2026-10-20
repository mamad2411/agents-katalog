---
name: autoformalization-compile-eval
description: Probes a model's ability to translate informal natural language mathematical statements into syntactically and semantically valid formal code for theorem provers (Isabelle or Lean4). It measures how well the model captures formal syntax, type-checking rules, and prover-specific conventions without requiring proof generation. Use when the user wants to benchmark on miniF2F, ProofNet, or asks about evaluating this task. Reports Compilation rates (%).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2311.03755
  bibtex_key: jiang2023multilingual
  confidence: high
---

# autoformalization-compile-eval

> Multilingual Mathematical Autoformalization — Jiang et al. (2023) (arXiv:2311.03755, 2023)

## What this evaluates

Probes a model's ability to translate informal natural language mathematical statements into syntactically and semantically valid formal code for theorem provers (Isabelle or Lean4). It measures how well the model captures formal syntax, type-checking rules, and prover-specific conventions without requiring proof generation.

## Datasets

- **miniF2F** — total ?; splits: test (-1)
- **ProofNet** — total ?; splits: test (-1)

## Metrics

- `Compilation rates (%)` **(primary)** — range: percent
  - Percentage of generated formal statements that successfully compile in the target theorem prover (Isabelle or Lean4). Calculated as (number of successfully compiled statements / total test instances) * 100.

## Input / output format

**Input**: Informal natural language mathematical statement.

**Output**: Formal statement in Isabelle or Lean4.

## Scoring recipe

```python
def compute_compilation_rate(predictions, prover):
    compiled_count = 0
    for pred in predictions:
        if prover.compile(pred):  # e.g., lean4.compile or isabelle.compile
            compiled_count += 1
    return (compiled_count / len(predictions)) * 100
```

## Common pitfalls

- Compilation success does not guarantee mathematical correctness or that the formal statement accurately reflects the original informal intent.
- Results are highly sensitive to the specific version and configuration of the theorem prover environment used for evaluation.
- Cross-prover generalization (e.g., training on Isabelle but testing on Lean4) often yields lower rates due to syntax and type system differences, requiring careful regime matching.

## Evidence (verbatim from paper)

> on two downstream benchmarks: miniF2F (Zheng et al., 2022) and ProofNet (Azerbayev et al., 2023), consisting of high-school mathematical competition and undergraduate-level mathematical exercise problems respectively.

Table 3: Compilation rates (%) on miniF2F and ProofNet.

## Citation

```bibtex
@misc{jiang2023multilingual,
  title={Multilingual Mathematical Autoformalization},
  author={Jiang et al. (2023)},
  year={2023},
  note={arXiv:2311.03755}
}
```

- arXiv: 2311.03755
