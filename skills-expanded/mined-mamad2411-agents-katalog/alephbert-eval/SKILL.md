---
name: alephbert-eval
description: Evaluates pre-trained Hebrew language models on core NLP tasks including morphological analysis, named entity recognition, and sentiment analysis. It measures how well the models handle Hebrew-specific linguistic features and resource-scarce language challenges compared to existing baselines. Use when the user wants to benchmark on SPMRL Hebrew Section, UD treebanks Hebrew Section, Ben-Mordecai and Elhadad corpus, NEMO corpus, Amram et al. (2018) corpus (cleaned), or asks about evaluating this task. Reports accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2104.04052
  bibtex_key: seker2021alephbert
  confidence: medium
---

# alephbert-eval

> AlephBERT:A Hebrew Large Pre-Trained Language Model to Start-off your Hebrew NLP Application With — Seker et al. (2021) (arXiv:2104.04052, 2021)

## What this evaluates

Evaluates pre-trained Hebrew language models on core NLP tasks including morphological analysis, named entity recognition, and sentiment analysis. It measures how well the models handle Hebrew-specific linguistic features and resource-scarce language challenges compared to existing baselines.

## Datasets

- **SPMRL Hebrew Section** — total ?; splits: train (-1), test (-1)
- **UD treebanks Hebrew Section** — total ?; splits: train (-1), test (-1)
- **Ben-Mordecai and Elhadad corpus** — total ?; splits: train (-1), test (-1)
- **NEMO corpus** — total ?; splits: train (-1), test (-1)
- **Amram et al. (2018) corpus (cleaned)** — total ?; splits: train (-1), test (-1)

## Metrics

- `accuracy` **(primary)** — range: percent
  - Not explicitly specified in the provided text; standard evaluation metrics for each task (e.g., token-level accuracy for POS/morphological tagging, F1 for NER and sentiment analysis) are implied.

## Input / output format

**Input**: Modern Hebrew text sequences, provided as raw sentences or tokenized/morpheme-segmented inputs depending on the specific task (e.g., tokenized text for POS/morphological tagging, raw sentences for NER and sentiment analysis).

**Output**: Task-specific predictions: word boundaries and POS/morphological tags for segmentation/tagging tasks, entity labels for NER, and sentiment labels for sentiment analysis.

## Scoring recipe

```python
For each task, compute standard token-level or sequence-level metrics:
- POS/Tagging: accuracy = (correct_tags / total_tokens) * 100
- NER: F1 = 2 * (precision * recall) / (precision + recall) over entity spans
- Sentiment: accuracy = (correct_labels / total_samples) * 100
Aggregate results per task and report mean performance across all benchmarks.
```

## Common pitfalls

- Data leakage in the original Amram et al. (2018) sentiment corpus required a cleaned split to avoid inflated test performance.
- Hebrew's rich morphology and lack of spaces between words require careful tokenization and morphological segmentation before evaluation.
- Comparisons are made against older baselines (mBERT, HeBERT) which may not reflect current state-of-the-art performance.

## Evidence (verbatim from paper)

> We evaluated the two AlephBERT variants (small and base) on the different tasks, in order to empirically gauge the effect of model size and data size on the quality of the language model. In addition, we compared the performance of our models to existing Hebrew BERT-based instantiations (mBERT (Devlin et al., 2019) and HeBERT (Chriqui and Yahav, 2021)). We evaluated the PLMs on all key tasks of the Hebrew NLP pipeline. Benchmarks We evaluate our BERT-based models on various Hebrew NLP tasks using the following benchmarks: Word Segmentation, Part-of-Speech Tagging, Full Morphological Tagging: The Hebrew Section of the SPMRL Task (Seddah et al., 2013) The Hebrew Section of the UD^6 treebanks collection (Sadde et al., 2018) Named Entity Recognition: Token-based NER evaluation based on the corpus of Ben-Mordecai and Elhadad (Ben Mordecai and Elhadad, 2005) Token-based and Morpheme-based NER evaluation based on the Named Entities and MOrphology (henceforth NEMO) corpus (Bareket and Tsarfaty, 2020) Sentiment Analysis: Sentiment Analysis evaluation based on the corpus of Amram et al. (2018). Since the aforementioned corpus is reported to be leaking (shared material between test and train)

## Citation

```bibtex
@misc{seker2021alephbert,
  title={AlephBERT:A Hebrew Large Pre-Trained Language Model to Start-off your Hebrew NLP Application With},
  author={Seker et al. (2021)},
  year={2021},
  note={arXiv:2104.04052}
}
```

- arXiv: 2104.04052
