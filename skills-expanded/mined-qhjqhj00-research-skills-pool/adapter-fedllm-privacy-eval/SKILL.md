---
name: adapter-fedllm-privacy-eval
description: Evaluates the privacy vulnerability of adapter-based federated large language models against gradient inversion attacks. It measures how accurately an adversary can reconstruct private training text from shared adapter gradients under varying batch sizes, model architectures, and defensive mechanisms. Use when the user wants to benchmark on CoLA, SST, Rotten Tomatoes, or asks about evaluating this task. Reports ROUGE-1.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2601.17533
  bibtex_key: chen2026reconstructing
  confidence: high
---

# adapter-fedllm-privacy-eval

> Reconstructing Training Data from Adapter-based Federated Large Language Models — Silong Chen et al. (2026) (arXiv:2601.17533, 2026)

## What this evaluates

Evaluates the privacy vulnerability of adapter-based federated large language models against gradient inversion attacks. It measures how accurately an adversary can reconstruct private training text from shared adapter gradients under varying batch sizes, model architectures, and defensive mechanisms.

## Datasets

- **CoLA** — total ?; splits: (unstated)
- **SST** — total ?; splits: (unstated)
- **Rotten Tomatoes** — total ?; splits: (unstated)

## Metrics

- `ROUGE-1` **(primary)** — range: percent
  - Unigram overlap ratio between generated and reference text. Computed as the sum of matched unigrams in the generated text divided by the total unigrams in the reference.
- `ROUGE-2` — range: percent
  - Bigram overlap ratio between generated and reference text. Computed as the sum of matched bigrams in the generated text divided by the total bigrams in the reference.

## Input / output format

**Input**: Adapter gradients (extracted from the first two Transformer layers) and the frozen backbone model architecture/weights. Gold reference is the original training text.

**Output**: Reconstructed text sequence (tokens/words) generated via constrained greedy decoding.

## Scoring recipe

```python
def compute_rouge_n(generated, reference, n=1):
    from collections import Counter
    from nltk.util import ngrams
    gen_ngrams = list(ngrams(generated.split(), n))
    ref_ngrams = list(ngrams(reference.split(), n))
    gen_counts = Counter(gen_ngrams)
    ref_counts = Counter(ref_ngrams)
    matched = sum((gen_counts & ref_counts).values())
    total_ref = sum(ref_counts.values())
    return (matched / total_ref) * 100 if total_ref > 0 else 0.0
```

## Common pitfalls

- Assuming frozen backbone gradients are sufficient for reconstruction; DAGER fails because it relies on them, while UTR exploits adapter gradients.
- Ignoring batch size scaling effects; reconstruction quality for GPT2 degrades on SST/RT at batch sizes >32 due to unidirectional attention.
- Confusing defense parameters; DP uses noise multiplier sigma while GP uses pruning rate r, with vastly different utility-privacy trade-offs.

## Evidence (verbatim from paper)

> Following prior work, we evaluate the quality of text reconstruction using ROUGE-1/2 scores (Lin, [2004]). ROUGE-1 and ROUGE-2 are widely adopted metrics for assessing the quality of text summarization or machine-generated text by comparing it to human-written reference summaries. ROUGE-N is computed as follows: ROUGE-N = Σ_i Count_i(matched n-grams) / Σ_i Count_i(n-grams in Reference_i)

## Citation

```bibtex
@misc{chen2026reconstructing,
  title={Reconstructing Training Data from Adapter-based Federated Large Language Models},
  author={Silong Chen et al. (2026)},
  year={2026},
  note={arXiv:2601.17533}
}
```

- arXiv: 2601.17533
