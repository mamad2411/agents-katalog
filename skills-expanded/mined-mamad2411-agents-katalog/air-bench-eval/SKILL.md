---
name: air-bench-eval
description: Evaluates Large Audio-Language Models on foundational audio comprehension across speech, natural sounds, and music, as well as open-ended instruction-following via generative responses. It probes the model's ability to understand mixed audio, follow complex prompts, and produce accurate, contextually relevant text. Use when the user wants to benchmark on AIR-Bench, or asks about evaluating this task. Reports GPT-4 alignment strategy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.07729
  bibtex_key: yang2024airbench
  confidence: high
---

# air-bench-eval

> AIR-Bench: Benchmarking Large Audio-Language Models via Generative Comprehension — Yang et al. (2024) (arXiv:2402.07729, 2024)

## What this evaluates

Evaluates Large Audio-Language Models on foundational audio comprehension across speech, natural sounds, and music, as well as open-ended instruction-following via generative responses. It probes the model's ability to understand mixed audio, follow complex prompts, and produce accurate, contextually relevant text.

## Datasets

- **AIR-Bench** — total 21000; splits: test (-1)

## Metrics

- `GPT-4 alignment strategy` **(primary)** — range: percent
  - Percentage of model hypotheses correctly aligned with the golden choice by GPT-4 after format normalization, used to overcome output format variations across models.
- `Exact matching strategy` — range: percent
  - Direct string or token match between the model's generated choice and the golden choice, without format normalization.
- `Average GPT-4 score` — range: [1, 10]
  - Mean score (1-10 scale) assigned by GPT-4 to model-generated responses against reference answers derived from audio meta-information, averaged over swapped hypothesis/reference positions to mitigate bias.

## Input / output format

**Input**: Audio clip (speech, natural sound, or music) paired with a text instruction or question.

**Output**: Text response: for the foundation benchmark, a single-choice answer (letter or word); for the chat benchmark, an open-ended generative response.

## Scoring recipe

```python
def score_foundation(hypothesis, golden_choice):
    prompt = f'Match hypothesis to golden choice. Hypothesis: {hypothesis}, Golden: {golden_choice}'
    return 1 if call_gpt4(prompt) == golden_choice else 0

def score_chat(hypothesis, audio_meta):
    reference = generate_reference(audio_meta)
    prompt = f'Score response 1-10 vs reference. Response: {hypothesis}, Reference: {reference}'
    return call_gpt4(prompt)

# Apply positional swap and average for chat
score = (score_chat(hyp, ref) + score_chat(ref, hyp)) / 2
```

## Common pitfalls

- Exact matching fails due to varied output formats (e.g., 'B', 'B.', 'B)') across models, requiring GPT-4 alignment for fair comparison.
- Positional bias in GPT-4 scoring occurs when the hypothesis is placed before the reference; the protocol requires averaging scores from swapped positions to mitigate this.
- Human evaluation for chat tasks uses pairwise preference rather than direct numerical scoring, which differs from the automated GPT-4 scoring method.

## Evidence (verbatim from paper)

> For the foundation benchmark, we also conduct a comparison between the use of an exact matching strategy with our proposed GPT-4 alignment strategy. As an example, we try to match ‘B’, ‘B.’, ‘B)’, etc. with LALMs’ hypothesis for the exact matching. The results are shown in Table 4. We can find that BLSP and SALMONN have a high success rate in directly generating the choice, showcasing their strong ability to follow single-choice instruction. However, we find that it is challenging to precisely extract the predicted choice from the hypotheses of other models due to significant variations in the output formats of different LALMs. However, with the assistance of GPT-4 as the evaluator, the success rate for all models can be improved to 100%.

## Citation

```bibtex
@misc{yang2024airbench,
  title={AIR-Bench: Benchmarking Large Audio-Language Models via Generative Comprehension},
  author={Yang et al. (2024)},
  year={2024},
  note={arXiv:2402.07729}
}
```

- arXiv: 2402.07729
