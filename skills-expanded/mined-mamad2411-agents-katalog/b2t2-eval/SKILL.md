---
name: b2t2-eval
description: Evaluates the expressiveness and type-error diagnostic quality of tabular programming type systems. It tests whether a type system can correctly type a curated set of table operations, handle example programs, and provide accurate feedback on buggy code. Use when the user wants to benchmark on Example Tables, or asks about evaluating this task. Reports expressiveness.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2111.10412
  bibtex_key: lu2021typesfortables
  confidence: high
---

# b2t2-eval

> Types for Tables: A Language Design Benchmark — Kuang-Chen Lu, Ben Greenman, Shriram Krishnamurthi (arXiv:2111.10412, 2021)

## What this evaluates

Evaluates the expressiveness and type-error diagnostic quality of tabular programming type systems. It tests whether a type system can correctly type a curated set of table operations, handle example programs, and provide accurate feedback on buggy code.

## Datasets

- **Example Tables** — total ?; splits: test (-1); repo https://github.com/brownplt/B2T2

## Metrics

- `expressiveness` **(primary)** — range: other
  - Assesses whether a type system can correctly type the curated table operations and example programs according to the benchmark's English-expressed constraints, without relying on artificial restrictions or overloading.

## Input / output format

**Input**: Table operation definitions with English type constraints, example programs using these operations, or buggy programs with known errors.

**Output**: Type-checking results (inferred types or pass/fail) for operations/programs, and type error messages or diagnostics for buggy programs.

## Scoring recipe

```python
def score_b2t2(predictions, gold):
    correct_ops = 0
    correct_errors = 0
    for case in gold:
        if case.type == 'operation':
            if predictions[case.id].matches_type(gold[case.id].expected_type):
                correct_ops += 1
        elif case.type == 'error':
            if predictions[case.id].identifies_bug(gold[case.id].bug_description):
                correct_errors += 1
    expressiveness = correct_ops / len(gold.operations)
    diagnostic_quality = correct_errors / len(gold.errors)
    return {'expressiveness': expressiveness, 'diagnostic_quality': diagnostic_quality}
```

## Common pitfalls

- Constraints are written in natural English rather than formal logic, requiring careful interpretation by type system designers.
- The benchmark intentionally minimizes overloading and avoids dynamic features like string-based expressions, so implementations relying heavily on these may not align with the design goals.

## Evidence (verbatim from paper)

> B2T2 is a benchmark for expressiveness aspects of a type system. It is not concerned with the efficiency of operations. Nor does it include broader approaches to evaluation such as cognitive dimensions [8] and conceptual design [28].

## Citation

```bibtex
@misc{lu2021typesfortables,
  title={Types for Tables: A Language Design Benchmark},
  author={Kuang-Chen Lu, Ben Greenman, Shriram Krishnamurthi},
  year={2021},
  note={arXiv:2111.10412}
}
```

- arXiv: 2111.10412
