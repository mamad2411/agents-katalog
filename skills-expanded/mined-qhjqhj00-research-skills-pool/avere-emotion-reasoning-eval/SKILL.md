---
name: avere-emotion-reasoning-eval
description: This benchmark probes multimodal large language models' ability to reason about emotions from audio and video inputs while avoiding spurious cue associations and hallucinations. It specifically tests whether models can correctly align relevant audiovisual cues with emotional labels and resist over-reliance on textual priors or irrelevant modalities. Use when the user wants to benchmark on EmoReAlM, DFEW, RAVDESS, MER2023, EMER, or asks about evaluating this task. Reports average accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2602.07054
  bibtex_key: chaubey2026avere
  confidence: high
---

# avere-emotion-reasoning-eval

> AVERE: Improving Audiovisual Emotion Reasoning with Preference Optimization — Chaubey et al. (2026) (arXiv:2602.07054, 2026)

## What this evaluates

This benchmark probes multimodal large language models' ability to reason about emotions from audio and video inputs while avoiding spurious cue associations and hallucinations. It specifically tests whether models can correctly align relevant audiovisual cues with emotional labels and resist over-reliance on textual priors or irrelevant modalities.

## Datasets

- **EmoReAlM** — total 4000; splits: test (-1)
- **DFEW** — total ?; splits: test (-1)
- **RAVDESS** — total ?; splits: test (-1)
- **MER2023** — total ?; splits: test (-1)
- **EMER** — total ?; splits: test (-1)

## Metrics

- `average accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly predicted answers across all EmoReAlM tasks. Computed as the mean of per-task accuracies.
- `precision, recall, F1` — range: [0, 1]
  - Standard binary classification metrics calculated for Yes/No response tasks on EmoReAlM.
- `UAR / WAR` — range: [0, 1]
  - Unweighted and Weighted Average Recall computed across emotion classes for DFEW and RAVDESS benchmarks.
- `weighted F1` — range: [0, 1]
  - Weighted F1 score computed across emotion classes for the MER2023 benchmark.
- `GPT-based evaluation score` — range: other
  - Automated comparison of generated free-text responses against ground truth using GPT, assessing clue overlap, label overlap, spurious cue-emotion associations, and hallucinatory cues.

## Input / output format

**Input**: Multimodal prompts containing audio and video inputs paired with emotion reasoning questions (multiple-choice or Yes/No). Text subtitles are explicitly removed during zero-shot evaluation to test pure audiovisual reasoning.

**Output**: Model-generated responses: either a selected multiple-choice option or a free-text description/reasoning for EMER tasks.

## Scoring recipe

```python
def score_emorealm(predictions, golds):
    correct = sum(1 for p, g in zip(predictions, golds) if p == g)
    return correct / len(golds)

def score_yesno(predictions, golds):
    tp = sum(1 for p, g in zip(predictions, golds) if p == g == 1)
    fp = sum(1 for p, g in zip(predictions, golds) if p == 1 and g == 0)
    fn = sum(1 for p, g in zip(predictions, golds) if p == 0 and g == 1)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    return prec, rec, f1
```

## Common pitfalls

- Evaluating models with text subtitles as input, which contradicts the zero-shot audiovisual reasoning protocol and artificially inflates performance.
- Conflating spurious cue-emotion associations (linking irrelevant cues to emotions) with hallucinatory cues (fabricating non-existent cues), as the benchmark treats them as distinct failure modes requiring separate assessment.
- Relying solely on automatic metrics without conducting user evaluation for reasoning quality, as GPT-based and human checks are required to capture hallucination and inconsistency.

## Evidence (verbatim from paper)

> For EmoReAlM benchmark, we report the average accuracy per task for all the tasks. For tasks with Yes/No responses, we additionally report the precision, recall and F1 score following previous multimodal hallucination benchmarks (Sung-Bin et al., 2025; Li et al., 2023). Beyond EmoReAlM, we also evaluate on established emotion recognition datasets—DFEW (Jiang et al., 2020), RAVDESS (Livingstone & Russo, 2018), MER2023 (Lian et al., 2023a)—and the emotion reasoning dataset EMER (Lian et al., 2023b). None of these datasets is used in training to ensure zero-shot evaluation. Following prior work (Cheng et al., 2024; Han et al., 2025b), we report unweighted and weighted average recalls for DFEW and RAVDESS and weighted F1 for MER2023. For emotion reasoning, we adopt GPT-based evaluation (Cheng et al., 2024), comparing generated responses against ground truth. In addition to clue and label overlap, we assess two dimensions: (i) spurious cue-emotion associations, where irrelevant cues are linked to emotions, and (ii) hallucinatory cues, where non-existent audiovisual cues are fabricated.

## Citation

```bibtex
@misc{chaubey2026avere,
  title={AVERE: Improving Audiovisual Emotion Reasoning with Preference Optimization},
  author={Chaubey et al. (2026)},
  year={2026},
  note={arXiv:2602.07054}
}
```

- arXiv: 2602.07054
