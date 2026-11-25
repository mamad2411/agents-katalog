---
name: abraham-eval
description: Evaluates molecular generative models by assessing their ability to recreate known ligands, predict drug-target affinity, and bind to target proteins via molecular docking. It probes the biological relevance and structural fidelity of de novo generated molecules across multiple protein targets. Use when the user wants to benchmark on ABRAHAM, or asks about evaluating this task. Reports ROOM recreation metric.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2208.09658
  bibtex_key: vinogradova2022abraham
  confidence: high
---

# abraham-eval

> A biologically-inspired multi-modal evaluation of molecular generative machine learning — Vinogradova et al. (2022) (arXiv:2208.09658, 2022)

## What this evaluates

Evaluates molecular generative models by assessing their ability to recreate known ligands, predict drug-target affinity, and bind to target proteins via molecular docking. It probes the biological relevance and structural fidelity of de novo generated molecules across multiple protein targets.

## Datasets

- **ABRAHAM** — total ?; splits: test (-1); repo https://github.com/VeaLi/MLT-LE

## Metrics

- `ROOM recreation metric` **(primary)** — range: count / percentage
  - Counts the number of generated molecules that exactly match test set ligands. Reported as average recreated ligands across 10 splits, total unique recreated molecules, and ratio of recreated to total generated molecules.
- `DTA prediction` — range: probability / pKD
  - Drug-target affinity predicted by SVM, GraphDTA, or MLT-LE models. Scores are averaged over the top 10% of generated molecules with highest classification/regression outputs.
- `Molecular docking score` — range: kcal/mol
  - Binding energy computed using Glide SP docking. Lower scores indicate higher affinity. RMSD is also calculated to measure spatial conformation similarity.

## Input / output format

**Input**: Generated molecular structures (SMILES/3D coordinates) and target protein identifiers (VDR, GABA_A, mTOR).

**Output**: Recreation counts/rates, DTA prediction scores, and docking scores/RMSD values.

## Scoring recipe

```python
def score_room(generated, test_set):
    recreated = sum(1 for mol in generated if mol in test_set)
    return recreated / len(generated)

def score_dta(predictions):
    top_10 = sorted(predictions, reverse=True)[:int(len(predictions)*0.1)]
    return sum(top_10) / len(top_10)

def score_docking(scores):
    return sum(scores) / len(scores)  # lower is better
```

## Common pitfalls

- ROOM metric only counts exact recreation, ignoring structural similarity.
- DTA predictions are averaged only over the top 10% of outputs, not the full distribution.
- Molecular docking was only performed for VDR, not for GABA_A or mTOR.

## Evidence (verbatim from paper)

> Table 1 shows the overall results of the proposed ROOM recreation metric for all three reference datasets and the following seven generative models which have been used for this study... In order to create a ranking of generative models (and molecular docking), 10% of the output molecules with highest DTA predictions (respectively absolute docking scores for VDR) were selected and their predictions averaged.

## Citation

```bibtex
@misc{vinogradova2022abraham,
  title={A biologically-inspired multi-modal evaluation of molecular generative machine learning},
  author={Vinogradova et al. (2022)},
  year={2022},
  note={arXiv:2208.09658}
}
```

- arXiv: 2208.09658
