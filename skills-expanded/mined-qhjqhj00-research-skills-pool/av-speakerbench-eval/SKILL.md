---
name: av-speakerbench-eval
description: This benchmark probes fine-grained audiovisual reasoning in multimodal large language models, specifically requiring them to jointly determine who is speaking, what is being said, and when events occur within real-world video clips. It evaluates cross-modal fusion, temporal grounding, and speaker-centric perception through multiple-choice questions validated by human experts. Use when the user wants to benchmark on AV-SpeakerBench, or asks about evaluating this task. Reports MCQ accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2512.02231
  bibtex_key: nguyen2025seehearandunderstand
  confidence: high
---

# av-speakerbench-eval

> See, Hear, and Understand: Benchmarking Audiovisual Human Speech Understanding in Multimodal Large Language Models — Nguyen et al. (2025) (arXiv:2512.02231, 2025)

## What this evaluates

This benchmark probes fine-grained audiovisual reasoning in multimodal large language models, specifically requiring them to jointly determine who is speaking, what is being said, and when events occur within real-world video clips. It evaluates cross-modal fusion, temporal grounding, and speaker-centric perception through multiple-choice questions validated by human experts.

## Datasets

- **AV-SpeakerBench** — total ?; splits: test (-1)

## Metrics

- `MCQ accuracy` **(primary)** — range: percent
  - Percentage of correctly answered multiple-choice questions out of the total number of questions.

## Input / output format

**Input**: Audio-video clips paired with multiple-choice questions requiring speaker identification, speech content recognition, temporal grounding, or audio attribute estimation.

**Output**: A single selected option from the provided multiple-choice answers.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Models may exploit visual-only cues like mouth movements or gestures to answer questions without actually using the audio modality.
- Temporal grounding and overlapping speech perception are frequent failure points, leading to misaligned reasoning even when content is correctly perceived.
- Frame sampling policies vary significantly across models (e.g., 1 fps vs. fixed 8 frames), which can drastically affect temporal resolution and performance comparability.

## Evidence (verbatim from paper)

> The full evaluation results are presented in Table 2; all results are reported in MCQ accuracy. Here, we summarize the main takeaways. Existing models remain far from human performance. Human evaluation reaches an overall accuracy of 93.74%, confirming that the questions are clear and naturally solvable through audiovisual reasoning.

## Citation

```bibtex
@misc{nguyen2025seehearandunderstand,
  title={See, Hear, and Understand: Benchmarking Audiovisual Human Speech Understanding in Multimodal Large Language Models},
  author={Nguyen et al. (2025)},
  year={2025},
  note={arXiv:2512.02231}
}
```

- arXiv: 2512.02231
