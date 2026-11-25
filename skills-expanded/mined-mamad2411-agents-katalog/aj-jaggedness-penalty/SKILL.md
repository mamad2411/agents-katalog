---
name: aj_jaggedness_penalty
description: Proposes a diagnostic metric to quantify the discrepancy between macro-averaged benchmark scores and experienced reliability in deployment. It accounts for uneven task coverage by measuring the dispersion of error rates across domains, highlighting how gap-uniform evaluation can misstate actual user experience. Use when the user has predictions and gold and needs to compute CV_d(e_d).
metadata:
  skill_kind: metric
  source_arxiv: 2601.07573
  bibtex_key: gans2026model
  confidence: high
---

# aj_jaggedness_penalty

> A Model of Artificial Jagged Intelligence — Joshua S. Gans (arXiv:2601.07573, 2026)

## What this evaluates

Proposes a diagnostic metric to quantify the discrepancy between macro-averaged benchmark scores and experienced reliability in deployment. It accounts for uneven task coverage by measuring the dispersion of error rates across domains, highlighting how gap-uniform evaluation can misstate actual user experience.

## Datasets

- (no dataset; pure metric skill)

## Metrics

- `CV_d(e_d)` **(primary)** — range: other
  - Coefficient of variation of domain-level error rates, calculated as sqrt(Var(e_d))/E[e_d], where e_d = 1 - s_d. Used as a diagnostic for the inspection wedge between benchmark averages and experienced reliability.

## Input / output format

**Input**: Per-domain benchmark scores s_d(m) and domain-level error rates e_d = 1 - s_d.

**Output**: A single dispersion statistic (CV_d(e_d)) or a deployment-weighted score S^dep(m).

## Scoring recipe

```python
def compute_jaggedness_penalty(scores_per_domain):
    errors = [1 - s for s in scores_per_domain]
    mean_err = sum(errors) / len(errors)
    var_err = sum((e - mean_err)**2 for e in errors) / len(errors)
    return (var_err ** 0.5) / mean_err
```

## Common pitfalls

- Assuming macro-averaged benchmark scores reflect deployment reliability without checking domain exposure distribution.
- Treating long-tail benchmarks like BIG-bench as representative of average-case performance rather than tail-risk modules.

## Evidence (verbatim from paper)

> If only an unweighted or uniform-weight benchmark is available, one can report a dispersion statistic across domains, such as CV_d(e_d) for domain-level error rates e_d ≡ 1-s_d. In settings where domain size and domain error are positively associated (the AJI mechanism), CV_d(e_d) is informative about how far the macro-average can drift from experienced reliability.

## Citation

```bibtex
@misc{gans2026model,
  title={A Model of Artificial Jagged Intelligence},
  author={Joshua S. Gans},
  year={2026},
  note={arXiv:2601.07573}
}
```

- arXiv: 2601.07573
