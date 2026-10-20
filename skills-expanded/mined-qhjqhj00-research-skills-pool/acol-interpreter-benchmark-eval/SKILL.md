---
name: acol-interpreter-benchmark-eval
description: Evaluates the execution speed and dispatching efficiency of different interpreter implementations (AST vs. bytecode variants) for a simple imperative language (ACOL) in Prolog. Use when the user wants to benchmark on ACOL Interpreter Benchmarks, or asks about evaluating this task. Reports geometric_mean_runtime.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2008.12543
  bibtex_key: korner2020bytecode
  confidence: high
---

# acol-interpreter-benchmark-eval

> On the Performance of Bytecode Interpreters in Prolog — Korner et al. (2020) (arXiv:2008.12543, 2020)

## What this evaluates

Evaluates the execution speed and dispatching efficiency of different interpreter implementations (AST vs. bytecode variants) for a simple imperative language (ACOL) in Prolog.

## Datasets

- **ACOL Interpreter Benchmarks** — total 6; splits: test (6); repo https://github.com/pkoerner/prolog-interpreters

## Metrics

- `geometric_mean_runtime` **(primary)** — range: other
  - Geometric mean of 10 execution runs per interpreter per benchmark. Also reported as normalized runtime relative to the baseline AST interpreter.

## Input / output format

**Input**: ACOL programs (while-loops, if-statements, assignments, comparisons, additions/subtractions) with pre-initialized environment variables.

**Output**: Execution time in seconds (mean ± 0.95 confidence interval over 10 runs).

## Scoring recipe

```python
runtimes = []
for _ in range(10):
    t = run_program_in_interpreter(program, interpreter)
    runtimes.append(t)
mean_runtime = geometric_mean(runtimes)
normalized_runtime = mean_runtime / baseline_ast_mean_runtime
return mean_runtime, normalized_runtime
```

## Common pitfalls

- Compilation time is explicitly excluded; only interpreter dispatch/runtime is measured.
- Geometric mean is used for aggregation instead of arithmetic mean, as specified by the authors.
- Small handwritten programs may benefit from AST caching, skewing results compared to larger generated programs.

## Evidence (verbatim from paper)

> Each program was executed with every interpreter ten times. The runtime consists only of the time spent in the interpreter. Compilation time is excluded, as it is not implemented efficiently and, ultimately, not relevant. The mean value is determined by the geometric mean as proposed by [5].

## Citation

```bibtex
@misc{korner2020bytecode,
  title={On the Performance of Bytecode Interpreters in Prolog},
  author={Korner et al. (2020)},
  year={2020},
  note={arXiv:2008.12543}
}
```

- arXiv: 2008.12543
