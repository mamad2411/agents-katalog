---
name: artseek-eval
description: Evaluates a multimodal retrieval-augmented generation pipeline for deep artwork understanding. It probes the system's ability to retrieve relevant art-historical context from a large corpus, classify artwork attributes (style, genre, artist), and generate grounded, interpretable captions/explanations from image input alone. Use when the user wants to benchmark on WikiFragments, WikiArt/ArtGraph, ArtPedia, SemArt v2.0, PaintingForm, or asks about evaluating this task. Reports NDCG@5, Top-1 Accuracy, BLEU@1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2507.21917
  bibtex_key: fanelli2025artseek
  confidence: high
---

# artseek-eval

> ArtSeek: Deep artwork understanding via multimodal in-context reasoning and late interaction retrieval — Fanelli et al. (2025) (arXiv:2507.21917, 2025)

## What this evaluates

Evaluates a multimodal retrieval-augmented generation pipeline for deep artwork understanding. It probes the system's ability to retrieve relevant art-historical context from a large corpus, classify artwork attributes (style, genre, artist), and generate grounded, interpretable captions/explanations from image input alone.

## Datasets

- **WikiFragments** — total 5651060; splits: test (10000); repo https://github.com/cilabuniba/artseek
- **WikiArt/ArtGraph** — total 116475; splits: train (-1), val (-1), test (-1)
- **ArtPedia** — total ?; splits: test (-1)
- **SemArt v2.0** — total ?; splits: test (-1)
- **PaintingForm** — total ?; splits: test (-1)

## Metrics

- `NDCG@5` **(primary)** — range: [0, 1]
  - Normalized Discounted Cumulative Gain at rank 5. Rewards early ranking of relevant results by applying a logarithmic discount to the cumulative gain of retrieved items.
- `Recall@1` — range: [0, 1]
  - Binary metric indicating whether the ground-truth fragment was successfully retrieved as the top-1 result.
- `Top-1 Accuracy` **(primary)** — range: [0, 1]
  - Percentage of instances where the highest-scoring predicted class matches the ground-truth label.
- `F1` — range: [0, 1]
  - Harmonic mean of precision and recall. Computed as weighted average for multiclass tasks and standard average for multilabel tasks.
- `BLEU@1` **(primary)** — range: [0, 1]
  - Unigram precision score measuring the overlap between generated and reference text at the word level.
- `METEOR` — range: [0, 1]
  - Metric based on unigram matching with synonymy, stemming, and paraphrase matching, penalizing fragmentation.
- `SPICE` — range: [0, 1]
  - Semantic Proposition Image Caption Evaluation score based on object-attribute-relation triples extracted from scene graphs.
- `ROUGE-L` — range: [0, 1]
  - Recall-Oriented Understudy for Gisting Evaluation measuring the longest common subsequence between generated and reference text.

## Input / output format

**Input**: Retrieval: image(s) + generated question; Classification: artwork image; Generation: artwork image + retrieved context fragments + classification attributes.

**Output**: Retrieval: ranked list of document fragments; Classification: predicted class/label probabilities; Generation: JSON object with aspect-specific sentences or full paragraph caption.

## Scoring recipe

```python
def compute_metrics(predictions, golds, task):
    if task == 'retrieval':
        ndcg = compute_ndcg_at_k(predictions, golds, k=5)
        recall = int(predictions[0] == golds[0])
        return {'NDCG@5': ndcg, 'Recall@1': recall}
    elif task == 'classification':
        top1 = accuracy(predictions, golds, k=1)
        f1 = f1_score(golds, predictions, average='weighted')
        return {'Top-1 Acc': top1, 'F1': f1}
    elif task == 'generation':
        bleu1 = bleu_score(golds, predictions, n=1)
        meteor = meteor_score(golds, predictions)
        spice = spice_score(golds, predictions)
        rouge = rouge_score(golds, predictions, 'rougeL')
        return {'BLEU@1': bleu1, 'METEOR': meteor, 'SPICE': spice, 'ROUGE-L': rouge}
```

## Common pitfalls

- Captioning metrics (BLEU, ROUGE) are limited for art explanation and may not capture semantic depth or grounding quality.
- Class imbalance in WikiArt requires restricting artist/tag evaluation to those with >100 samples for fair comparison.
- Zero-shot evaluation means models are not fine-tuned on target datasets, making direct comparison with fine-tuned baselines potentially unfair.
- SPICE computation is excluded for PaintingForm due to high computational cost from large dataset size and lengthy inputs.

## Evidence (verbatim from paper)

> We evaluate performance using Normalized Discounted Cumulative Gain (NDCG) and Recall (R). NDCG rewards the early ranking of relevant results, while Recall measures whether the original fragment (from which the query was derived) was successfully retrieved. We also report execution time (in centiseconds) to compare retrieval efficiency.

## Citation

```bibtex
@misc{fanelli2025artseek,
  title={ArtSeek: Deep artwork understanding via multimodal in-context reasoning and late interaction retrieval},
  author={Fanelli et al. (2025)},
  year={2025},
  note={arXiv:2507.21917}
}
```

- arXiv: 2507.21917
