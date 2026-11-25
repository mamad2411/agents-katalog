---
name: aya-eval
description: Evaluates the open-ended generation capabilities of multilingual LLMs, including brainstorming, planning, and unstructured long-form responses across diverse languages, scripts, and resource levels. Use when the user wants to benchmark on AYA-HUMAN-ANNOTATED, DOLLY-MACHINE-TRANSLATED, DOLLY-HUMAN-EDITED, or asks about evaluating this task. Reports fluency and quality.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2402.06619
  bibtex_key: singh2024aya
  confidence: high
---

# aya-eval

> Aya Dataset: An Open-Access Collection for Multilingual Instruction Tuning — Singh et al. (2024) (arXiv:2402.06619, 2024)

## What this evaluates

Evaluates the open-ended generation capabilities of multilingual LLMs, including brainstorming, planning, and unstructured long-form responses across diverse languages, scripts, and resource levels.

## Datasets

- **AYA-HUMAN-ANNOTATED** — total 1750; splits: test (1750)
- **DOLLY-MACHINE-TRANSLATED** — total 200; splits: test (200)
- **DOLLY-HUMAN-EDITED** — total 200; splits: test (200)

## Metrics

- `fluency and quality` **(primary)** — range: qualitative
  - Qualitative assessment of model-generated responses for fluency, correctness, and relevance in open-ended tasks. No explicit numerical formula is provided; evaluation relies on human annotators or LLM judges to score response quality across target languages.

## Input / output format

**Input**: Multilingual instruction prompts (original human-curated or machine-translated/post-edited) specifying open-ended tasks such as brainstorming, planning, or unstructured long-form responses.

**Output**: Unstructured, long-form text generations in the target language corresponding to the prompt.

## Scoring recipe

```python
def evaluate(predictions, prompts, languages):
    scores = []
    for prompt, gen, lang in zip(prompts, predictions, languages):
        # Assess fluency and quality via human annotators or LLM judge
        score = judge_quality(gen, prompt, lang)
        scores.append(score)
    # Aggregate scores per language and overall
    return aggregate(scores)
# Note: No closed-form formula; relies on qualitative judgment of open-ended generations.
```

## Common pitfalls

- Machine-translated prompts may contain translation artifacts that render them nonsensical, skewing quality assessments.
- Cultural or geographic references in prompts can invalidate evaluations for non-English speakers if not carefully filtered.
- Limited language coverage in human-annotated sets (7 languages) versus machine-translated sets (101+ languages) creates a trade-off between evaluation quality and linguistic coverage.

## Evidence (verbatim from paper)

> The intention behind this selection was to gather a test set that allows us to evaluate the fluency and quality of responses in various languages while avoiding model assessment on prompts tied to specific cultural or geographic references that might have language-dependent validity.

## Citation

```bibtex
@misc{singh2024aya,
  title={Aya Dataset: An Open-Access Collection for Multilingual Instruction Tuning},
  author={Singh et al. (2024)},
  year={2024},
  note={arXiv:2402.06619}
}
```

- arXiv: 2402.06619
