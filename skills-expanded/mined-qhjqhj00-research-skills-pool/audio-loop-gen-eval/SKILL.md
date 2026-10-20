---
name: audio-loop-gen-eval
description: Evaluates the quality, diversity, and realism of generated audio drum loops. It probes a model's ability to capture spectral-temporal patterns, genre characteristics, and seamless looping properties in fixed-length music generation. Use when the user wants to benchmark on FreeSound Loop Dataset (FSLD), or asks about evaluating this task. Reports IS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2108.01576
  bibtex_key: hung2021loopbenchmark
  confidence: high
---

# audio-loop-gen-eval

> A Benchmarking Initiative for Audio-Domain Music Generation Using the Freesound Loop Dataset — Hung et al. (2021) (arXiv:2108.01576, 2021)

## What this evaluates

Evaluates the quality, diversity, and realism of generated audio drum loops. It probes a model's ability to capture spectral-temporal patterns, genre characteristics, and seamless looping properties in fixed-length music generation.

## Datasets

- **FreeSound Loop Dataset (FSLD)** — total ?; splits: train (-1); repo https://github.com/allenhung1025/LoopTest

## Metrics

- `IS` **(primary)** — range: [0, ∞) | other
  - Inception Score measuring sample quality and diversity based on a classifier's prediction entropy over generated samples. Higher values indicate better generation quality and diversity.
- `FAD` — range: [0, ∞) | other
  - Fréchet Audio Distance measuring the distribution distance between real and generated audio in a pre-trained embedding space. Lower values indicate closer distribution match.
- `JS` — range: [0, ∞) | other
  - Jensen-Shannon divergence quantifying the similarity between the probability distributions of real and generated audio features. Lower values indicate higher similarity.
- `NDB/K` — range: [0, ∞) | other
  - Neural Distance/Kernel metric evaluating distribution similarity using neural network features. Lower values indicate better alignment with real data.

## Input / output format

**Input**: Random noise vectors fed into generative models (StyleGAN, StyleGAN2, UNAGAN) to produce audio loops.

**Output**: Generated audio loops (waveforms), vocoded through MelGAN for fair comparison with real loops.

## Scoring recipe

```python
generated = [model.sample() for _ in range(2000)]
is_score = compute_inception_score(generated)
fad_score = compute_frechet_audio_distance(generated, real_dataset)
js_score = compute_js_divergence(generated, real_dataset)
ndb_score = compute_neural_distance(generated, real_dataset)
# Subjective: average ratings from 140 listeners on 4 metrics
subj_scores = {metric: mean([subject.rating(loop, metric) for subject in listeners for loop in samples]) for metric in ['Drumness', 'Loopness', 'Audio quality', 'Preference']}
```

## Common pitfalls

- IS and FAD can yield contradictory rankings (e.g., UNAGAN scores better on FAD but worse on IS).
- Subjective listening tests require vocoding both real and generated audio through the same MelGAN vocoder to control for vocoder artifacts.
- Statistical significance must be verified using Student’s t-test for objective metrics or Wilcoxon signed-rank test for subjective ratings.

## Evidence (verbatim from paper)

> Each model generates 2,000 random loops to compute the scores. We also compute these metrics on the two real datasets and add the results to Table 1, to offer an oracle reference. We see that the IS of StyleGAN2 is the closest to that of the freesound dataset, followed by UNAGAN and then StyleGAN. Student’s t-test shows that the performance edge of StyleGAN2 over either UNAGAN or StyleGAN is statistically significant (p-value<0.01). This reveals the efficacy of StyleGAN2 for generating fixed-length audio. The scores in JS and NDB further support the superiority of StyleGAN2, showing that its output is the most diverse among the three.

## Citation

```bibtex
@misc{hung2021loopbenchmark,
  title={A Benchmarking Initiative for Audio-Domain Music Generation Using the Freesound Loop Dataset},
  author={Hung et al. (2021)},
  year={2021},
  note={arXiv:2108.01576}
}
```

- arXiv: 2108.01576
