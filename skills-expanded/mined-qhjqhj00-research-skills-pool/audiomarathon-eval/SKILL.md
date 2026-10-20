---
name: audiomarathon-eval
description: Evaluates long-context audio understanding and inference efficiency across speech, sound, and music domains. It probes temporal dependency modeling, multi-hop reasoning, and memory/token-pruning scalability in Large Audio Language Models. Use when the user wants to benchmark on AudioMarathon, or asks about evaluating this task. Reports F1-score.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2510.07293
  bibtex_key: he2025audiomarathon
  confidence: high
---

# audiomarathon-eval

> AudioMarathon: A Comprehensive Benchmark for Long-Context Audio Understanding and Efficiency in Audio LLMs — He et al. (2025) (arXiv:2510.07293, 2025)

## What this evaluates

Evaluates long-context audio understanding and inference efficiency across speech, sound, and music domains. It probes temporal dependency modeling, multi-hop reasoning, and memory/token-pruning scalability in Large Audio Language Models.

## Datasets

- **AudioMarathon** — total ?; splits: test (-1); repo https://github.com/DabDans/AudioMarathon

## Metrics

- `F1-score` **(primary)** — range: percent
  - Harmonic mean of precision and recall, or exact-match accuracy for MCQs. Used for classification and multiple-choice tasks.
- `Word Accuracy Rate (WAR)` — range: percent
  - Ratio of correctly recognized words to the total number of words in the reference transcript for ASR tasks.
- `macro F1-score` — range: percent
  - Unweighted mean of recall or precision calculated independently for each class, then averaged. Used for audio event detection to balance precision and recall across imbalanced classes.
- `Latency` — range: other
  - Wall-clock time required to process a single audio instance from input to output.
- `Peak GPU Memory Usage` — range: other
  - Maximum VRAM consumed by the model during a single inference pass.

## Input / output format

**Input**: Full audio file (90–300 seconds) concatenated with an instruction-following prompt containing a question and labeled options (2, 4, or 5 options depending on the task). The order of options is randomized per instance.

**Output**: A single selected option label corresponding to the correct answer.

## Scoring recipe

```python
def compute_metrics(predictions, gold, task_type):
    if task_type == 'ASR':
        return sum(p == g for p, g in zip(predictions, gold)) / len(gold) * 100  # WAR
    elif task_type == 'audio_event_detection':
        return macro_f1_score(predictions, gold)  # macro F1
    else:  # classification / MCQ
        return sum(p == g for p, g in zip(predictions, gold)) / len(gold) * 100  # F1/Accuracy
```

## Common pitfalls

- Option order is randomized per instance to mitigate positional bias, so models cannot exploit fixed answer positions.
- ASR evaluation uses a filtered test subset of LibriSpeech-long, not the standard full dataset.
- Efficiency metrics (latency, memory) are reported alongside accuracy, requiring consistent hardware and batch-size settings for fair comparison.

## Evidence (verbatim from paper)

> For task performance, we adopt standard metrics per task: F1-score for classification and MCQs, Word Accuracy Rate (WAR) for ASR, and macro F1-score for audio event detection to balance precision and recall across classes. Inference efficiency is assessed via latency and peak GPU memory usage. We also report speedup over a vanilla model.

## Citation

```bibtex
@misc{he2025audiomarathon,
  title={AudioMarathon: A Comprehensive Benchmark for Long-Context Audio Understanding and Efficiency in Audio LLMs},
  author={He et al. (2025)},
  year={2025},
  note={arXiv:2510.07293}
}
```

- arXiv: 2510.07293
