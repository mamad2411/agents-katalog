---
name: av-odyssey-bench-eval
description: Evaluates multimodal large language models' ability to perceive, integrate, and reason over interleaved audio and visual inputs. It probes basic auditory perception (e.g., loudness, pitch, duration) and complex cross-modal tasks spanning timbre, tone, melody, spatial reasoning, temporal dynamics, hallucination detection, and intricate reasoning across 10 domains. Use when the user wants to benchmark on AV-Odyssey Bench, or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2412.02611
  bibtex_key: gong2024avodyssey
  confidence: high
---

# av-odyssey-bench-eval

> AV-Odyssey Bench: Can Your Multimodal LLMs Really Understand Audio-Visual Information? — Gong et al. (2024) (arXiv:2412.02611, 2024)

## What this evaluates

Evaluates multimodal large language models' ability to perceive, integrate, and reason over interleaved audio and visual inputs. It probes basic auditory perception (e.g., loudness, pitch, duration) and complex cross-modal tasks spanning timbre, tone, melody, spatial reasoning, temporal dynamics, hallucination detection, and intricate reasoning across 10 domains.

## Datasets

- **AV-Odyssey Bench** — total 4555; splits: test (4555)

## Metrics

- `accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly answered multiple-choice questions out of the total number of questions. Calculated as the number of matches between predicted and ground-truth options divided by the total question count.

## Input / output format

**Input**: Interleaved multimodal inputs consisting of a text question, one or more images/videos, and one or more audio clips. Questions are structured as multiple-choice with four options (A, B, C, D) that may be text, images, or audio.

**Output**: A single letter corresponding to the chosen option (A, B, C, or D).

## Scoring recipe

```python
correct = 0
for pred, gold in zip(predictions, gold_labels):
    if pred == gold:
        correct += 1
accuracy = correct / len(predictions)
```

## Common pitfalls

- Models may bypass multimodal inputs by relying on textual context or memorization from pretraining data, potentially inflating scores on questions with redundant descriptions.
- Input ordering biases, such as the sequence of audio clips or option presentation, can affect performance if not randomized or controlled during evaluation.

## Evidence (verbatim from paper)

> The results on DeafTest are shown in TableLABEL:table:api_model_basic_performace. Among the four tasks, sound counting and duration separation seem to be simpler than the other two for MLLMs, since Gemini 1.5 Pro achieves more than 80% accuracy on the two tasks. Nonetheless, all the results are far behind the expected 100%. Especially on loudness comparison and pitch comparison tasks, none of these MLLMs achieve a score over 65%.

## Citation

```bibtex
@misc{gong2024avodyssey,
  title={AV-Odyssey Bench: Can Your Multimodal LLMs Really Understand Audio-Visual Information?},
  author={Gong et al. (2024)},
  year={2024},
  note={arXiv:2412.02611}
}
```

- arXiv: 2412.02611
