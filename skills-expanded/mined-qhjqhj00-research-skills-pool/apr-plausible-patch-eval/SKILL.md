---
name: apr-plausible-patch-eval
description: Evaluates the ability of code language models to automatically generate correct patches for real-world Java bugs. It probes whether pre-trained or fine-tuned models can produce syntactically valid and semantically correct code that passes developer-written test suites and survives manual verification. Use when the user wants to benchmark on Defects4J v1.2, Defects4J v2.0, QuixBugs, HumanEval-Java, or asks about evaluating this task. Reports plausible_patch.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2302.05020
  bibtex_key: jiang2023impact
  confidence: high
---

# apr-plausible-patch-eval

> Impact of Code Language Models on Automated Program Repair — Jiang et al. (2023) (arXiv:2302.05020, 2023)

## What this evaluates

Evaluates the ability of code language models to automatically generate correct patches for real-world Java bugs. It probes whether pre-trained or fine-tuned models can produce syntactically valid and semantically correct code that passes developer-written test suites and survives manual verification.

## Datasets

- **Defects4J v1.2** — total 130; splits: test (130)
- **Defects4J v2.0** — total 108; splits: test (108)
- **QuixBugs** — total 40; splits: test (40)
- **HumanEval-Java** — total 164; splits: test (164)

## Metrics

- `plausible_patch` **(primary)** — range: percent
  - Percentage of bugs where at least one of the 10 generated candidate patches passes all developer-written test cases and is manually verified as semantically correct.

## Input / output format

**Input**: Buggy Java function with buggy lines either masked by a placeholder (e.g., <mask>) or provided as comments, plus surrounding context.

**Output**: Patched code (either the whole patched function or just the patched lines plus the remainder of the function).

## Scoring recipe

```python
plausible_count = 0
for bug in bugs:
    patches = generate_patches(model, bug, k=10)
    for patch in patches:
        if run_test_cases(patch) == PASS:
            if manual_verify(patch):
                plausible_count += 1
                break
return plausible_count / len(bugs)
```

## Common pitfalls

- Data leakage: Pre-trained CLMs may have encountered Defects4J/QuixBugs during pre-training, artificially inflating performance.
- Prompt sensitivity: Model performance varies significantly depending on whether buggy lines are masked or provided as comments.
- Test suite limitations: Passing developer-written tests only indicates syntactic/compilability correctness, not semantic correctness, requiring manual verification.

## Evidence (verbatim from paper)

> For all experiments, we let each tool (CLMs, fine-tuned CLMs, or DL-based APR techniques) generate ten candidate patches for each bug and run the developer-written test cases on the patched program. The first patched program that passes all the test cases is considered a plausible patch. And we finally manually check the correctness of plausible patches

## Citation

```bibtex
@misc{jiang2023impact,
  title={Impact of Code Language Models on Automated Program Repair},
  author={Jiang et al. (2023)},
  year={2023},
  note={arXiv:2302.05020}
}
```

- arXiv: 2302.05020
