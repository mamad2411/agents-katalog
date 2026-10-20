---
name: automotive-verification-eval
description: Evaluates software model checkers on their ability to verify safety requirements in industrial automotive C code generated from Simulink models. It probes how well tools handle floating-point arithmetic, pointer operations, and complex control logic under bounded and unbounded verification constraints. Use when the user wants to benchmark on DSR, ECC, or asks about evaluating this task. Reports SV-COMP quantile plots.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2003.11689
  bibtex_key: westhofen2020benchmarking
  confidence: high
---

# automotive-verification-eval

> Benchmarking Software Model Checkers on Automotive Code — Westhofen et al. (2020) (arXiv:2003.11689, 2020)

## What this evaluates

Evaluates software model checkers on their ability to verify safety requirements in industrial automotive C code generated from Simulink models. It probes how well tools handle floating-point arithmetic, pointer operations, and complex control logic under bounded and unbounded verification constraints.

## Datasets

- **DSR** — total 105; splits: test (105); repo https://github.com/moves-rwth/cbmc-with-kInduction
- **ECC** — total 74; splits: test (74); repo https://github.com/moves-rwth/cbmc-with-kInduction

## Metrics

- `SV-COMP quantile plots` **(primary)** — range: other
  - A scoring system adapted from SV-COMP that rewards correct definite verification results and heavily penalizes incorrect ones. Assumes BTC EmbeddedValidator results as ground truth. Wrong violation results are penalized by -16 points, and wrong proof results by -32 points.

## Input / output format

**Input**: C source code files generated from Simulink models, with safety requirements specified via a pattern-based approach.

**Output**: Per requirement: 'True' (proof), 'False' (counterexample/violation), or 'Unknown' (timeout or bounded proof only).

## Scoring recipe

```python
score = 0
for task in tasks:
    if btc_result[task] == 'definite':
        if verifier_result[task] == btc_result[task]:
            score += 1
        elif verifier_result[task] == 'False' and btc_result[task] == 'True':
            score -= 32
        elif verifier_result[task] == 'True' and btc_result[task] == 'False':
            score -= 16
return score
```

## Common pitfalls

- Using BTC EmbeddedValidator as ground truth is debatable because many of its definite results are actually bounded proofs rather than unbounded verifications.
- Floating-point precision differences (e.g., 64 vs 80 bits) can cause conflicting but technically correct results between tools, which the scoring scheme penalizes as errors.
- The SV-COMP punishment scheme heavily penalizes tools that return many results if some are wrong, making conservative verifiers appear artificially better.

## Evidence (verbatim from paper)

> In absence of the true verification results, let us assume the results of BTC EmbeddedValidator as a “ground truth”. We update the quantile plots to *now punish wrong results* (i.e., results in conflict with BTC) by *${-}16$ and ${-}32$ points for wrong violation and proof results*, respectively, as in the SV-COMP.

## Citation

```bibtex
@misc{westhofen2020benchmarking,
  title={Benchmarking Software Model Checkers on Automotive Code},
  author={Westhofen et al. (2020)},
  year={2020},
  note={arXiv:2003.11689}
}
```

- arXiv: 2003.11689
