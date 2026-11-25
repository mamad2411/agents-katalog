---
name: allvb-eval
description: Evaluates multimodal large language models' ability to comprehend hour-long videos across nine distinct tasks, including classification, recognition, localization, captioning, emotion recognition, and needle-in-a-haystack retrieval. It specifically probes temporal reasoning, detail extraction, and long-context retention over extended video durations. Use when the user wants to benchmark on ALLVB, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.07298
  bibtex_key: tan2025allvb
  confidence: high
---

# allvb-eval

> ALLVB: All-in-One Long Video Understanding Benchmark — Tan et al. (2025) (arXiv:2503.07298, 2025)

## What this evaluates

Evaluates multimodal large language models' ability to comprehend hour-long videos across nine distinct tasks, including classification, recognition, localization, captioning, emotion recognition, and needle-in-a-haystack retrieval. It specifically probes temporal reasoning, detail extraction, and long-context retention over extended video durations.

## Datasets

- **ALLVB** — total 1376; splits: test (1376)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Percentage of correctly answered multiple-choice questions. Calculated as (number of correct predictions / total number of questions) * 100.

## Input / output format

**Input**: Video frames or clips corresponding to the entire movie, a specific sub-plot, or a Needle-in-a-Haystack segment, accompanied by subtitles and a multiple-choice question with 5 options.

**Output**: A single uppercase letter (A, B, C, D, or E) indicating the selected option.

## Scoring recipe

```python
def compute_accuracy(predictions, gold_labels):
    correct = sum(1 for p, g in zip(predictions, gold_labels) if p == g)
    return (correct / len(gold_labels)) * 100
```

## Common pitfalls

- Questions are generated from movie scripts using GPT-4o, so script-video mismatches (e.g., visual details like object colors or actions) may cause answer discrepancies if models rely solely on visual input without script context.
- The Needle-in-a-Haystack task divides videos into 10 segments and samples 11 frames per segment, requiring frame-level retrieval rather than just temporal context understanding, which can confuse models trained only on video-level inputs.

## Evidence (verbatim from paper)

> All Q&As are presented as multiple-choice questions, with each question offering 5 options, one correct answer, and 4 distractors. This format allows for easy calculation of accuracy during testing and eliminates the subjective judgment issues associated with open-ended answers.

## Citation

```bibtex
@misc{tan2025allvb,
  title={ALLVB: All-in-One Long Video Understanding Benchmark},
  author={Tan et al. (2025)},
  year={2025},
  note={arXiv:2503.07298}
}
```

- arXiv: 2503.07298
