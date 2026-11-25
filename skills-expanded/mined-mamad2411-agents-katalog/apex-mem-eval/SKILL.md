---
name: apex-mem-eval
description: Evaluates long-term conversational memory, temporal reasoning, and factual consistency across multi-session dialogues and noisy search-augmented contexts. Probes an agent's ability to retrieve, resolve temporal conflicts, and answer complex queries over extended interaction histories. Use when the user wants to benchmark on LOCOMO, LongMemEval, SealQA-Hard, or asks about evaluating this task. Reports LOCOMO Overall Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.14362
  bibtex_key: banerjee2026apexmem
  confidence: high
---

# apex-mem-eval

> APEX-MEM: Agentic Semi-Structured Memory with Temporal Reasoning for Long-Term Conversational AI — Banerjee et al. (2026) (arXiv:2604.14362, 2026)

## What this evaluates

Evaluates long-term conversational memory, temporal reasoning, and factual consistency across multi-session dialogues and noisy search-augmented contexts. Probes an agent's ability to retrieve, resolve temporal conflicts, and answer complex queries over extended interaction histories.

## Datasets

- **LOCOMO** — total ?; splits: test (-1)
- **LongMemEval** — total ?; splits: test (-1)
- **SealQA-Hard** — total ?; splits: test (-1)

## Metrics

- `LOCOMO Overall Accuracy` **(primary)** — range: percent
  - LLM-as-a-Judge evaluates generated answers against ground truth on factual accuracy, relevance, completeness, and contextual appropriateness, aggregated into a single percentage score across single-hop, multi-hop, temporal, open-domain, and adversarial categories.
- `LongMemEval Overall Score` — range: percent
  - LLM-as-a-Judge assesses answer quality and factuality scores over extremely long inputs including multi-document collections and extended narratives.
- `SealQA-Hard Accuracy` — range: percent
  - Exact match accuracy measuring whether the generated answer correctly resolves fact-seeking questions amid conflicting or noisy web search results.

## Input / output format

**Input**: Multi-turn conversational histories spanning weeks, or collections of web-retrieved documents ordered by publication time, paired with fact-seeking questions.

**Output**: Natural language answers to the posed questions.

## Scoring recipe

```python
def score_locomo(pred, gt, question):
    prompt = f'Q: {question}\nGT: {gt}\nPred: {pred}\nScore factual accuracy, relevance, completeness, contextual appropriateness.'
    return llm_as_judge(prompt)

def score_sealqa(pred, gt):
    return 1.0 if pred.strip().lower() == gt.strip().lower() else 0.0

# Aggregate: mean of 3 trials, temperature=0, max 40 ReACT tool calls
```

## Common pitfalls

- LLM-as-a-Judge evaluation introduces model-dependent bias and variance depending on the judge's version and prompt.
- Reproducibility requires temperature=0 and averaging over 3 trials, which baselines may not match.
- Tool invocation limit of 40 ReACT steps can truncate complex reasoning chains, artificially lowering multi-hop scores.

## Evidence (verbatim from paper)

> Following Chhikara et al. (2025), we use LLM-as-a-Judge to assess factual accuracy, relevance, completeness, and contextual appropriateness of generated answers against ground truth. On the LOCOMO benchmark, APEX-MEM with GPT5 achieves 88.88% overall accuracy. On the LongMemEval, APEX-MEM with Claude 4.5 Sonnet achieves 86.2% overall score. On the SealQA-Hard benchmark, APEX-MEM with GPT5 achieves 40.15% accuracy.

## Citation

```bibtex
@misc{banerjee2026apexmem,
  title={APEX-MEM: Agentic Semi-Structured Memory with Temporal Reasoning for Long-Term Conversational AI},
  author={Banerjee et al. (2026)},
  year={2026},
  note={arXiv:2604.14362}
}
```

- arXiv: 2604.14362
