---
name: astro-mcad-eval
description: Evaluates a classifier-based anomaly detection pipeline on simulated astronomical transient light curves. It probes the model's ability to identify rare, out-of-distribution events in real-time without prior exposure to the anomalous classes during training. Use when the user wants to benchmark on Simulated LSST-like transient light curves, or asks about evaluating this task. Reports anomaly score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2403.14742
  bibtex_key: gupta2024classifier
  confidence: medium
---

# astro-mcad-eval

> A Classifier-Based Approach to Multi-Class Anomaly Detection for Astronomical Transients — Gupta et al. (2024) (arXiv:2403.14742, 2024)

## What this evaluates

Evaluates a classifier-based anomaly detection pipeline on simulated astronomical transient light curves. It probes the model's ability to identify rare, out-of-distribution events in real-time without prior exposure to the anomalous classes during training.

## Datasets

- **Simulated LSST-like transient light curves** — total ?; splits: train (-1), test (-1); repo https://github.com/Rithwik-G/AstroMCAD

## Metrics

- `anomaly score` **(primary)** — range: other
  - A scalar value representing the likelihood of a transient being anomalous. Computed as the minimum negated isolation forest score across 12 class-specific forests: a_s = min_c (-I_c(z_s)). Higher values indicate greater deviation from known transient clusters.

## Input / output format

**Input**: A 4 x N_T matrix per transient containing scaled flux, scaled uncertainty, scaled observation time, and central passband wavelength for each timestep, concatenated with a 2-element vector of contextual features (Milky Way extinction and host galaxy spectroscopic redshift).

**Output**: A scalar anomaly score a_s computed as a_s = min_{c in {1..12}} (-I_c(z_s)), where z_s is the 9-dimensional latent representation from the penultimate layer of the trained RNN classifier, and I_c is the isolation forest trained on class c.

## Scoring recipe

```python
def compute_anomaly_score(light_curve_matrix, encoder, forests):
    z = encoder.predict(light_curve_matrix)  # 9-dim latent vector
    scores = [forest.score_samples(z) for forest in forests]  # returns negative anomaly scores
    anomaly_score = -min(scores)
    return anomaly_score

def compute_recall(predictions, threshold, true_labels):
    predicted_anomalies = predictions > threshold
    return sum(predicted_anomalies & true_labels) / sum(true_labels)
```

## Common pitfalls

- Anomalous classes are explicitly withheld during training to simulate real-world unknowns; revealing them beforehand invalidates the novelty detection setup.
- Light curves are irregularly sampled; using interpolation or imputation before encoding degrades real-time performance and distorts inter-passband relationships.
- The 9-dimensional latent space acts as a deliberate bottleneck; tuning it for classification may inject irrelevant features that confuse the isolation forests.

## Evidence (verbatim from paper)

> The goal of this work is to generate relatively large anomaly scores for anomalous transients and smaller anomaly scores for non-anomalous transients. To simulate seeing anomalous data for the first time, the five aforementioned anomalous classes are not revealed to the model until final evaluation.

## Citation

```bibtex
@misc{gupta2024classifier,
  title={A Classifier-Based Approach to Multi-Class Anomaly Detection for Astronomical Transients},
  author={Gupta et al. (2024)},
  year={2024},
  note={arXiv:2403.14742}
}
```

- arXiv: 2403.14742
