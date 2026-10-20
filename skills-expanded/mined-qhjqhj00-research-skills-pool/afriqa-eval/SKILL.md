---
name: afriqa-eval
description: Evaluates cross-lingual open-retrieval question answering systems across 10 African languages. It probes the pipeline's ability to translate low-resource queries, retrieve relevant passages, and accurately extract or generate answers. Use when the user wants to benchmark on AFRIQA, or asks about evaluating this task. Reports BLEU.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2305.06897
  bibtex_key: ogundepo2023afriqa
  confidence: high
---

# afriqa-eval

> AfriQA: Cross-lingual Open-Retrieval Question Answering for African Languages — Ogundepo et al. (2023) (arXiv:2305.06897, 2023)

## What this evaluates

Evaluates cross-lingual open-retrieval question answering systems across 10 African languages. It probes the pipeline's ability to translate low-resource queries, retrieve relevant passages, and accurately extract or generate answers.

## Datasets

- **AFRIQA** — total ?; splits: test (-1); repo https://github.com/masakhane-io/afriqa

## Metrics

- `BLEU` **(primary)** — range: [0, 100]
  - Standard corpus-level BLEU score measuring n-gram precision between machine-translated queries and human-translated reference queries, scaled to 0-100.

## Input / output format

**Input**: Question in an African language; gold or retrieved passages; target language for translation.

**Output**: Translated query; extracted answer span or generated answer text.

## Scoring recipe

```python
def score_bleu(predictions, references):
    # predictions: list of machine-translated queries
    # references: list of human-translated reference queries
    return nltk.translate.bleu_score.corpus_bleu(references, predictions) * 100
```

## Common pitfalls

- Google Translate lacks support for Bemba, Fon, and Wolof, creating uneven baseline coverage.
- API-based translations like Google Translate change over time, threatening long-term reproducibility.
- Cross-lingual retrieval baselines skip translation, making performance gains hard to attribute solely to the retriever.

## Evidence (verbatim from paper)

> Table 4 shows the BLEU score of the different translation systems on the test set of AFRIQA, evaluated against the human-translated queries.

## Citation

```bibtex
@misc{ogundepo2023afriqa,
  title={AfriQA: Cross-lingual Open-Retrieval Question Answering for African Languages},
  author={Ogundepo et al. (2023)},
  year={2023},
  note={arXiv:2305.06897}
}
```

- arXiv: 2305.06897
