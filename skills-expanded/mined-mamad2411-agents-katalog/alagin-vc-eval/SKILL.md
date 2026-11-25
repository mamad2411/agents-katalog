---
name: alagin-vc-eval
description: Evaluates voice conversion systems on speech quality and speaker similarity using subjective human ratings. It probes the ability of models to convert speech between speakers (specifically inter-gender) while preserving linguistic content and target speaker identity. Use when the user wants to benchmark on ALAGIN Japanese Speech Database Set B, or asks about evaluating this task. Reports Mean Opinion Score (MOS) for Speech Quality.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1804.00425
  bibtex_key: fang2018highquality
  confidence: high
---

# alagin-vc-eval

> High-quality nonparallel voice conversion based on cycle-consistent adversarial network — Fang et al. (2018) (arXiv:1804.00425, 2018)

## What this evaluates

Evaluates voice conversion systems on speech quality and speaker similarity using subjective human ratings. It probes the ability of models to convert speech between speakers (specifically inter-gender) while preserving linguistic content and target speaker identity.

## Datasets

- **ALAGIN Japanese Speech Database Set B** — total 50; splits: test (50)

## Metrics

- `Mean Opinion Score (MOS) for Speech Quality` **(primary)** — range: [1, 5]
  - Average of Likert scale ratings (1 to 5) provided by human evaluators for perceived speech quality.
- `Mean Opinion Score (MOS) for Speaker Similarity` — range: [1, 5]
  - Average of Likert scale ratings (1 to 5) provided by human evaluators for how closely the converted speech matches the target speaker's identity.

## Input / output format

**Input**: Source speech audio (or extracted 75-dim feature vectors including mel-cepstrum, F0, and aperiodicity) from a source speaker.

**Output**: Converted speech audio matching the target speaker's voice characteristics.

## Scoring recipe

```python
# For each test utterance and conversion method:
ratings_quality = [evaluator_score for evaluator_score in human_ratings_quality]
ratings_similarity = [evaluator_score for evaluator_score in human_ratings_similarity]
mos_quality = sum(ratings_quality) / len(ratings_quality)
mos_similarity = sum(ratings_similarity) / len(ratings_similarity)
# Statistical comparison across methods uses unpaired two-tail t-test with Holm-Bonferroni correction
```

## Common pitfalls

- Evaluators must listen to the full audio sample before submitting a rating; partial listens are discarded.
- The evaluation covers both male-to-female and female-to-male directions, so results should be averaged or reported separately for each gender conversion direction.
- Statistical significance is assessed using an unpaired two-tail t-test with Holm-Bonferroni compensation, not standard ANOVA or post-hoc tests.

## Evidence (verbatim from paper)

> Both metrics were evaluated on a 1-to-5 Likert mean opinion score (MOS) scale. The evaluation was carried out by means of a crowdsourced web-based interface. The evaluators were first shown a web page on which they input their gender and age. They were then each asked to rate sets of 12 utterances randomly selected from the 300 utterances. They were limited to rating a maximum of six sets so that they would not become complacent about. Although they were able to play each sample utterance as many times as they wanted, they had to completely play the audio samples and answer all the questions displayed on the web page for their evaluations to be considered in the evaluation. A total of 110 evaluators produced a total of 7200 data points, which is equivalent to 24 evaluations per utterance.

## Citation

```bibtex
@misc{fang2018highquality,
  title={High-quality nonparallel voice conversion based on cycle-consistent adversarial network},
  author={Fang et al. (2018)},
  year={2018},
  note={arXiv:1804.00425}
}
```

- arXiv: 1804.00425
