---
name: amigo-eval
description: Probes long-horizon agentic planning, cross-image grounding, and uncertainty-driven question selection. Models must iteratively ask constrained Yes/No/Unsure questions to identify a hidden target from a gallery of visually similar dress images while strictly tracking constraints and avoiding prohibited attributes. Use when the user wants to benchmark on AMIGO, or asks about evaluating this task. Reports identification success.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2603.28662
  bibtex_key: wang2026amigo
  confidence: high
---

# amigo-eval

> AMIGO: Agentic Multi-Image Grounding Oracle Benchmark — Wang et al. (2026) (arXiv:2603.28662, 2026)

## What this evaluates

Probes long-horizon agentic planning, cross-image grounding, and uncertainty-driven question selection. Models must iteratively ask constrained Yes/No/Unsure questions to identify a hidden target from a gallery of visually similar dress images while strictly tracking constraints and avoiding prohibited attributes.

## Datasets

- **AMIGO** — total 4587; splits: test (4587)

## Metrics

- `identification success` **(primary)** — range: [0, 1]
  - Binary accuracy: 1 if the model's final guess matches the hidden target's 1-indexed position in the gallery, 0 otherwise.
- `protocol compliance` — range: [0, 1]
  - Fraction of turns where the model adheres to the 10 interaction rules without triggering a 'Skip' response from the oracle.
- `efficiency` — range: other
  - Mean number of turns (questions asked) per episode, measuring how quickly the model narrows the candidate set.

## Input / output format

**Input**: A batch of dress images forming a gallery and a system signal 'End of uploading'. The model receives the images and iteratively receives oracle responses (Yes/No/Unsure/Skip) to its questions.

**Output**: Per turn: exactly one question about an observable attribute. Final turn: 'My guess of your favorite dress: #<number>' where <number> is the 1-indexed gallery position.

## Scoring recipe

```python
def score_episode(predictions, gold_idx):
    final_guess = int(predictions[-1].split('#')[-1].strip())
    success = 1 if final_guess == gold_idx else 0
    skips = sum(1 for p in predictions if p.oracle == 'Skip')
    compliance = 1.0 - (skips / len(predictions))
    efficiency = len(predictions)
    return {'identification success': success, 'protocol compliance': compliance, 'efficiency': efficiency}
```

## Common pitfalls

- Asking about prohibited attributes (e.g., color, sleeve length, background) immediately triggers a 'Skip' response and breaks protocol compliance.
- Enumerating attribute values across turns (e.g., cycling through neckline types) is explicitly forbidden and penalized.
- Guessing before the feasible candidate set is narrowed to exactly one image violates the strict protocol rules.

## Evidence (verbatim from paper)

> Evaluated via identification success, efficiency, protocol compliance, and trajectory diagnostics, AMIGO enables diagnostic analysis of planning, belief maintenance, and response to ambiguity in agentic vision-language models.

## Citation

```bibtex
@misc{wang2026amigo,
  title={AMIGO: Agentic Multi-Image Grounding Oracle Benchmark},
  author={Wang et al. (2026)},
  year={2026},
  note={arXiv:2603.28662}
}
```

- arXiv: 2603.28662
