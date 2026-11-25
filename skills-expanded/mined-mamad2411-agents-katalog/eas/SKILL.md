---
name: EAS
description: This evaluation validates the Emotional Attitude Score (EAS) metric by measuring its consistency with human judgment on word-level sentiment polarity. It probes whether the metric's pseudo-log-likelihood-based scores reliably capture positive or negative emotional attitudes toward ambiguous attitude words in gender-inclusive contexts. Use when the user has predictions and gold and needs to compute EAS.
metadata:
  skill_kind: metric
  source_arxiv: 2407.16266
  bibtex_key: chen2024beyond
  confidence: high
---

# EAS

> Beyond Binary Gender: Evaluating Gender-Inclusive Machine Translation with Ambiguous Attitude Words — Chen et al. (2024) (arXiv:2407.16266, 2024)

## What this evaluates

This evaluation validates the Emotional Attitude Score (EAS) metric by measuring its consistency with human judgment on word-level sentiment polarity. It probes whether the metric's pseudo-log-likelihood-based scores reliably capture positive or negative emotional attitudes toward ambiguous attitude words in gender-inclusive contexts.

## Datasets

- **AmbGIMT** — total ?; splits: eval (100); repo https://github.com/pppa2019/ambGIMT

## Metrics

- `EAS` **(primary)** — range: continuous
  - Emotional Attitude Score computed via pseudo-log-likelihood (PLL) from instruction-following LLMs. Scores are compared pairwise; the difference s1 - s2 determines the predicted label.

## Input / output format

**Input**: Pairs of ambiguous attitude words (w1, w2) with their corresponding EAS scores (s1, s2).

**Output**: Predicted label y in {-1, 0, 1}, where y=-1 if s1 - s2 <= -1, y=0 if -1 < s1 - s2 < 1, and y=1 if s1 - s2 >= 1.

## Scoring recipe

```python
diff = s1 - s2
if diff <= -1:
    y_pred = -1
elif diff >= 1:
    y_pred = 1
else:
    y_pred = 0

# Human label y_gold is majority vote of 3 annotators:
# 1 if w1 more positive, -1 if w1 more negative, 0 if close

kappa = cohen_kappa_score(y_gold, y_pred)
```

## Common pitfalls

- The threshold boundaries (-1 and 1) for mapping continuous EAS differences to discrete labels are arbitrary and may not generalize across different LLM backbones.
- Human labels are derived from a small pool of 3 undergraduate volunteers, which may not represent broader demographic or linguistic perspectives on gender-inclusive translation.
- The evaluation only checks pairwise consistency, not absolute score calibration or direct translation quality.

## Evidence (verbatim from paper)

> To ensure the proposed evaluation metric, EAS, can truly reflect how positive the emotional attitude towards the words is, we conduct a human evaluation to explore the consistency of the score and human judgment. We randomly sample 100 word pairs from the collected words, assuming a word pair is $(w_{1},w_{2})$, and the correspondent EAS is $(s_{1},s_{2})$. ... We use the Kappa metric to evaluate the consistency; the values higher than 0.8 mean a high consistency, and the results are 0.87, 0.81, and 0.83 for MiniCPM-2B, Gemma-7B-it, and Mistral-7B, respectively.

## Citation

```bibtex
@misc{chen2024beyond,
  title={Beyond Binary Gender: Evaluating Gender-Inclusive Machine Translation with Ambiguous Attitude Words},
  author={Chen et al. (2024)},
  year={2024},
  note={arXiv:2407.16266}
}
```

- arXiv: 2407.16266
