---
name: TCAV_score
description: Measures the influence of human-defined emotional concepts (physiognomy, utterance polarity, voice pitch) on a multimodal emotion recognition model's decisions using Concept Activation Vectors. It quantifies how much each concept drives the model's classification decisions across different network layers. Use when the user has predictions and gold and needs to compute TCAV score.
metadata:
  skill_kind: metric
  source_arxiv: 2202.01072
  bibtex_key: asokan2022tcav
  confidence: high
---

# TCAV_score

> Interpretability for Multimodal Emotion Recognition using Concept Activation Vectors — Asokan et al. (2022) (arXiv:2202.01072, 2022)

## What this evaluates

Measures the influence of human-defined emotional concepts (physiognomy, utterance polarity, voice pitch) on a multimodal emotion recognition model's decisions using Concept Activation Vectors. It quantifies how much each concept drives the model's classification decisions across different network layers.

## Datasets

- **IEMOCAP** — total 4498; splits: train (4290), test (1208)

## Metrics

- `TCAV score` **(primary)** — range: [0, 1]
  - The average dot product between the gradient of the loss with respect to the model's activations and the Concept Activation Vector (CAV), computed over a set of test samples. Higher scores indicate stronger concept influence on the model's predictions.

## Input / output format

**Input**: Multimodal utterances (video, audio, text) with ground-truth emotion labels (0-5) and binary concept labels (+ve/-ve).

**Output**: Emotion classification predictions and TCAV scores for each concept across specified network layers.

## Scoring recipe

```python
def compute_tcav_scores(model, test_samples, concepts, layers):
    tcav_results = {}
    for concept in concepts:
        cav = train_cav(concept.positive, concept.negative, n_repeats=30)
        scores = []
        for sample in test_samples:
            for layer in layers:
                activations = forward_pass(model, sample, layer)
                grad = compute_gradient_loss_wrt_activations(model, sample, layer)
                score = dot(grad, cav)
                scores.append(score)
        tcav_results[concept.name] = mean(scores)
    return tcav_results

# Statistical validation
tcav_scores = compute_tcav_scores(model, test_set, concepts, layers)
random_tcav_scores = compute_tcav_scores(model, test_set, random_concepts, layers)
p_value = ttest_2samp(tcav_scores, random_tcav_scores)
return tcav_scores, p_value
```

## Common pitfalls

- CAV training must be repeated 30 times to account for binary classifier initialization and preprocessing variance.
- Statistical significance requires comparing proposed concept TCAV scores against 50 random CAVs using a 2-tailed t-test at α=0.05.

## Evidence (verbatim from paper)

> We evaluate the statistical significance of our concepts by training 50 random CAVs for each layer and assigning random labels. We then perform a 2-tailed t-test on the TCAV score distributions of the random concepts and the proposed concepts at a significance level α = 0.05.

## Citation

```bibtex
@misc{asokan2022tcav,
  title={Interpretability for Multimodal Emotion Recognition using Concept Activation Vectors},
  author={Asokan et al. (2022)},
  year={2022},
  note={arXiv:2202.01072}
}
```

- arXiv: 2202.01072
