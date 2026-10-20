---
name: avut-eval
description: Evaluates multimodal large language models on their ability to comprehend audio content within videos and align audio cues with corresponding visual information. It specifically probes whether models rely on genuine multimodal reasoning or fall back to text-based shortcuts. Use when the user wants to benchmark on AVUT, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.19951
  bibtex_key: yang2025avut
  confidence: high
---

# avut-eval

> Audio-centric Video Understanding Benchmark without Text Shortcut — Yang et al. (2025) (arXiv:2503.19951, 2025)

## What this evaluates

Evaluates multimodal large language models on their ability to comprehend audio content within videos and align audio cues with corresponding visual information. It specifically probes whether models rely on genuine multimodal reasoning or fall back to text-based shortcuts.

## Datasets

- **AVUT** — total 11609; splits: AV-Human (1734), AV-Gemini (9875); repo https://github.com/lark-png/AVUT

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Standard exact-match accuracy for multiple-choice questions: 1 if the predicted option matches the gold option, 0 otherwise.
- `success rate` — range: [0, 1]
  - Proportion of correctly sorted audio segment sequences out of total attempts for the Audio-Visual Segment Matching task.
- `WER` — range: [0, 1]
  - Word Error Rate calculated on transcriptions for the Audio-Visual Speaker Diarization task: (Substitutions + Deletions + Insertions) / Total Words in reference.

## Input / output format

**Input**: A video clip (≤2 minutes) containing synchronized audio and visual tracks, accompanied by a text prompt containing a question and four multiple-choice options (A-D) or an open-ended instruction.

**Output**: For multiple-choice tasks: a single letter corresponding to the selected option (A, B, C, or D). For open-ended tasks: a sequence of sorted audio segment identifiers or a text transcription of a visually specified speaker.

## Scoring recipe

```python
def score_instance(task_type, prediction, gold):
    if task_type in ['AIE', 'ACC', 'AEL', 'AVCM', 'AVOM', 'AVTM']:
        return 1.0 if prediction == gold else 0.0
    elif task_type == 'AVSM':
        return 1.0 if prediction == gold else 0.0
    elif task_type == 'AVDiar':
        return 1.0 - compute_wer(prediction, gold)
    return 0.0

def aggregate_scores(scores):
    return sum(scores) / len(scores)
```

## Common pitfalls

- Models may exploit visual or textual shortcuts (e.g., reading on-screen text or subtitles) instead of processing the audio, which the benchmark explicitly filters out during data curation.
- Open-ended tasks like AVSM and AVDiar require strict formatting or precise temporal alignment, making exact-match or WER scoring highly sensitive to minor transcription or ordering deviations.

## Evidence (verbatim from paper)

> “Audio Visual Segment Matching” is to sort four randomly shuffled audio segments in a video into their original order. “Audio Visual Speaker Diarization” is to transcribe the speech of a visually specified speaker with the Word Error Rate (WER) as the metric.

## Citation

```bibtex
@misc{yang2025avut,
  title={Audio-centric Video Understanding Benchmark without Text Shortcut},
  author={Yang et al. (2025)},
  year={2025},
  note={arXiv:2503.19951}
}
```

- arXiv: 2503.19951
