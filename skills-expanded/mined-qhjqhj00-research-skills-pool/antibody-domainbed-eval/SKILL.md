---
name: antibody-domainbed-eval
description: Evaluates out-of-distribution generalization of protein language models and sequence CNNs for therapeutic antibody design across different antigen targets and generative models. It probes robustness to covariate shifts, label shifts, and assay biases in molecular sequence data. Use when the user wants to benchmark on Antibody DomainBed, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2407.21028
  bibtex_key: tagasovska2024antibodydomainbed
  confidence: high
---

# antibody-domainbed-eval

> Antibody DomainBed: Out-of-Distribution Generalization in Therapeutic Protein Design — Tagasovska et al. (2024) (arXiv:2407.21028, 2024)

## What this evaluates

Evaluates out-of-distribution generalization of protein language models and sequence CNNs for therapeutic antibody design across different antigen targets and generative models. It probes robustness to covariate shifts, label shifts, and assay biases in molecular sequence data.

## Datasets

- **Antibody DomainBed** — total ?; splits: train (-1), val (-1), test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly predicted binding labels across test environments. Computed as the mean of correct predictions divided by total predictions, multiplied by 100.

## Input / output format

**Input**: Amino acid sequences for antibody heavy chain, light chain, and antigen, often concatenated with a 25-residue poly-glycine linker and adjusted positional embeddings.

**Output**: Binary classification label indicating binding affinity (positive/negative).

## Scoring recipe

```python
def compute_accuracy(predictions, gold):
    correct = sum(1 for p, g in zip(predictions, gold) if p == g)
    return (correct / len(gold)) * 100
```

## Common pitfalls

- Models trained on one antigen target (e.g., HIV) often fail to generalize to another (e.g., HER2) due to significant covariate and label shifts.
- Batch effects and assay biases can create spurious correlations that inflate in-distribution performance but hurt out-of-distribution generalization.

## Evidence (verbatim from paper)

> There is an advantage of the SeqCNN framework achieving higher accuracy on environment 4, however, those number are still around 50% and hence we can not consider them useful since we could not use such model in practice.

## Citation

```bibtex
@misc{tagasovska2024antibodydomainbed,
  title={Antibody DomainBed: Out-of-Distribution Generalization in Therapeutic Protein Design},
  author={Tagasovska et al. (2024)},
  year={2024},
  note={arXiv:2407.21028}
}
```

- arXiv: 2407.21028
