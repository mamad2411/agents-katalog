---
name: algonauts-2019-eval
description: This benchmark evaluates a model's ability to predict human visual brain activity during object recognition. It compares model representations against fMRI and MEG neural recordings using representational similarity analysis (RSA) across spatial (EVC vs IT) and temporal (early vs late processing) dimensions. Use when the user wants to benchmark on Algonauts 2019 Challenge, or asks about evaluating this task. Reports noise-normalized variance explained.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1905.05675
  bibtex_key: cichy2019algonauts
  confidence: high
---

# algonauts-2019-eval

> The Algonauts Project: A Platform for Communication between the Sciences of Biological and Artificial Intelligence — Cichy et al. (2019) (arXiv:1905.05675, 2019)

## What this evaluates

This benchmark evaluates a model's ability to predict human visual brain activity during object recognition. It compares model representations against fMRI and MEG neural recordings using representational similarity analysis (RSA) across spatial (EVC vs IT) and temporal (early vs late processing) dimensions.

## Datasets

- **Algonauts 2019 Challenge** — total ?; splits: train (-1), test (78)

## Metrics

- `noise-normalized variance explained` **(primary)** — range: [0, 100] percent
  - Compute Representational Dissimilarity Matrices (RDMs) for both model activations and brain responses. Calculate the Spearman rank correlation between the model and brain RDMs, square it to obtain R^2, and divide by the noise ceiling (the average correlation of individual subject RDMs with the subject-averaged RDM) to normalize the score.

## Input / output format

**Input**: Sets of images (silhouettes or natural backgrounds) presented to the model to extract activation patterns.

**Output**: Representational Dissimilarity Matrices (RDMs) computed from the model's activations for the given image sets.

## Scoring recipe

```python
def score(model_rdm, brain_rdm, subject_rdms):
    rho = spearman_correlation(model_rdm, brain_rdm)
    r2 = rho ** 2
    mean_brain_rdm = np.mean(subject_rdms, axis=0)
    noise_ceiling = np.mean([spearman_correlation(sub_rdm, mean_brain_rdm) for sub_rdm in subject_rdms])
    score = (r2 / noise_ceiling) * 100
    return score
```

## Common pitfalls

- Using the held-out test brain data to train or tune the model, which is explicitly forbidden by the challenge rules.
- Failing to normalize the R^2 score by the noise ceiling, resulting in scores that cannot be fairly compared across regions or modalities with different signal-to-noise ratios.
- Confusing the spatial track (fMRI: EVC vs IT) with the temporal track (MEG: early vs late processing), which require different neural datasets and RDMs.

## Evidence (verbatim from paper)

> Comparing human brains and models is challenging because of the numerous differences between them... here we make use of a technique called representational similarity analysis (RSA)... We relate RDMs in a second step by calculating their similarity (Spearman R). Finally, we square the result to R^2 to indicate the amount of variance explained... The noise ceiling is computed by the assumption that the subject-averaged RDM is the best estimate of the ideal model RDM... We use the noise ceiling to normalize R^2 values to noise-normalized variance explained. Thus, any model can explain from 0 to 100% of the explainable variance.

## Citation

```bibtex
@misc{cichy2019algonauts,
  title={The Algonauts Project: A Platform for Communication between the Sciences of Biological and Artificial Intelligence},
  author={Cichy et al. (2019)},
  year={2019},
  note={arXiv:1905.05675}
}
```

- arXiv: 1905.05675
