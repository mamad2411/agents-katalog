---
name: authfix-oidc-repair-eval
description: Evaluates an automated program repair system's ability to fix real-world security and logic bugs in OpenID Connect implementations. It measures both the rate of successfully generating correct patches and the semantic quality of those patches compared to human-written developer fixes. Use when the user wants to benchmark on OpenID Connect Bug Dataset, or asks about evaluating this task. Reports fix_accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.02773
  bibtex_key: rahat2025authfix
  confidence: high
---

# authfix-oidc-repair-eval

> Automated Repair of OpenID Connect Programs (Extended Version) — Tamjid Al Rahat et al. (2025) (arXiv:2510.02773, 2025)

## What this evaluates

Evaluates an automated program repair system's ability to fix real-world security and logic bugs in OpenID Connect implementations. It measures both the rate of successfully generating correct patches and the semantic quality of those patches compared to human-written developer fixes.

## Datasets

- **OpenID Connect Bug Dataset** — total 23; splits: test (23); repo https://github.com/tamjidrahat/authfix

## Metrics

- `fix_accuracy` **(primary)** — range: [0, 1]
  - Number of correctly fixed bugs divided by the total number of bugs in the dataset. Correctness is determined by manual verification against the OpenID specification and corresponding Petri-net model.
- `semantic_equivalence_rate` — range: [0, 1]
  - Number of generated patches that are semantically equivalent to the original developer-written patch, divided by the number of patches compared. Equivalence is assessed via manual inspection.

## Input / output format

**Input**: Buggy OpenID Connect program code, English specification of the required authentication flow/security property, and a corresponding Petri-net model (PNML format) representing the specification.

**Output**: Fixed program code (patch) that satisfies the provided specification and Petri-net model.

## Scoring recipe

```python
def score(dataset, predictions):
  correct_count = 0
  equiv_count = 0
  compared_count = 0
  for instance in dataset:
    pred_patch = predictions[instance.id]
    # 1. Check correctness against spec/Petri-net
    if verify_correctness(pred_patch, instance.spec, instance.petri_net):
      correct_count += 1
    # 2. Check semantic equivalence to dev patch if available
    if instance.dev_patch is not None:
      compared_count += 1
      if is_semantically_equivalent(pred_patch, instance.dev_patch):
        equiv_count += 1
  fix_accuracy = correct_count / len(dataset)
  semantic_equivalence_rate = equiv_count / compared_count if compared_count > 0 else 0
  return fix_accuracy, semantic_equivalence_rate
```

## Common pitfalls

- Correctness and semantic equivalence are determined via manual inspection rather than automated test suites, introducing subjectivity and limiting reproducibility.
- Petri-net models are manually constructed per authentication flow, making the evaluation setup highly labor-intensive and potentially biased toward flows with well-documented specifications.
- The dataset excludes closed-source implementations and some publicly reported CVEs, so results may not generalize to all real-world OpenID deployments.

## Evidence (verbatim from paper)

> To evaluate the effectiveness of AuthFix in repairing OpenID bugs, we use it to repair 23 benchmarks in our dataset and manually check the repaired bugs to validate their correctness with respect to the corresponding specification. As shown in [Table II], it generated correct fixes for 17 out of 23 bugs. ... Upon our manual investigation, we found that 10 out of the 15 generated patches are semantically equivalent to the patches written by human developers.

## Citation

```bibtex
@misc{rahat2025authfix,
  title={Automated Repair of OpenID Connect Programs (Extended Version)},
  author={Tamjid Al Rahat et al. (2025)},
  year={2025},
  note={arXiv:2510.02773}
}
```

- arXiv: 2510.02773
