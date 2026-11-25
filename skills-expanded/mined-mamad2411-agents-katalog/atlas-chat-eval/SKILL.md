---
name: atlas-chat-eval
description: Evaluates large language models on Moroccan Arabic (Darija) across multiple-choice reasoning, instruction following, translation, summarization, and sentiment analysis. It probes dialect-specific linguistic features, script variability (Arabic vs. Arabizi), and real-world instruction-following capabilities in a low-resource setting. Use when the user wants to benchmark on DarijaMMLU, DarijaHellaSwag, Belebele_Ary, DarijaBench, DarijaAlpacaEval, or asks about evaluating this task. Reports Accuracy.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2409.17912
  bibtex_key: shang2024atlaschat
  confidence: high
---

# atlas-chat-eval

> Atlas-Chat: Adapting Large Language Models for Low-Resource Moroccan Arabic Dialect — Shang et al. (2024) (arXiv:2409.17912, 2024)

## What this evaluates

Evaluates large language models on Moroccan Arabic (Darija) across multiple-choice reasoning, instruction following, translation, summarization, and sentiment analysis. It probes dialect-specific linguistic features, script variability (Arabic vs. Arabizi), and real-world instruction-following capabilities in a low-resource setting.

## Datasets

- **DarijaMMLU** — total ?; splits: test (-1)
- **DarijaHellaSwag** — total ?; splits: test (-1)
- **Belebele_Ary** — total ?; splits: test (-1)
- **DarijaBench** — total ?; splits: test (-1)
- **DarijaAlpacaEval** — total ?; splits: test (-1)

## Metrics

- `Accuracy` **(primary)** — range: [0, 1]
  - Percentage of correctly predicted options in multiple-choice and discriminative sentiment classification tasks.
- `BLEU` — range: [0, 1]
  - Standard n-gram based translation metric comparing generated text to reference.
- `ROUGE-1/L` — range: [0, 1]
  - Recall-oriented overlap metric for summarization based on unigrams or longest common subsequence.
- `chrF` — range: [0, 1]
  - Character n-gram F-score metric providing finer-grained evaluation than word-level BLEU.
- `BERTScore` — range: [0, 1]
  - Semantic similarity metric using contextual embeddings (DarijaBERT for summarization, multilingual BERT for translation).
- `Win-rate` — range: [0, 1]
  - Percentage of instances where the LLM-as-a-Judge prefers the generated summary over the reference.

## Input / output format

**Input**: Multiple-choice questions, source-target text pairs for translation, source text for summarization, and text for sentiment classification. Evaluated in zero-shot and few-shot settings.

**Output**: Model-generated answers (options for MC), translated text, summarized text, or sentiment labels. For LLM-as-a-Judge evaluations, models use default sampling-based decoding.

## Scoring recipe

```python
def compute_metrics(predictions, gold, metric_type):
    if metric_type == 'accuracy':
        return sum(p == g for p, g in zip(predictions, gold)) / len(gold)
    elif metric_type == 'win_rate':
        # LLM-as-a-Judge (Jais-13B-Chat) selects preferred output
        return sum(judge_prefers(pred, ref) for pred, ref in zip(predictions, gold)) / len(gold)
    elif metric_type in ['bleu', 'rouge', 'chrf', 'bertscore']:
        return compute_standard_metric(predictions, gold, metric_type)
    return 0.0
```

## Common pitfalls

- n-gram metrics (BLEU/ROUGE) are overly rigid for Darija due to lack of standardization (diacritics, agglutinations, Arabizi vs Arabic script), often penalizing semantically correct outputs.
- LLM-as-a-Judge evaluations require specific setup: using Jais-13B-Chat as the judge model and default sampling-based decoding, not greedy decoding.
- Few-shot performance gains vary significantly by model size (pronounced for 9B/27B, not observed for 2B).

## Evidence (verbatim from paper)

> We employed Accuracy to evaluate models on multiple-choice benchmarks, including DarijaMMLU, DarijaHellaSwag, Belebele_Ary, and the discriminative sentiment analysis task within DarijaBench. For translation and summarization tasks, we adopted the conventional BLEU *(Papineni et al., [2002])* and ROUGE-1/L *(Lin, [2004])*, respectively. However, since these metrics are based on $n$-grams, they are not well-suited for assessing Darija. For example, the same word in Darija can be written in multiple ways ("How are you?" \= "\<كيدير>" \= "\<كيداير>" \= "\<كي داير>") due to the lack of standardization (e.g., diacritics, agglutinations, borrowings), making them overly rigid in cases where slight variations still convey the same meaning. To gain a more fine-grained insight, we also included chrF *(Popović, [2015])*, operating at the level of character $n$-grams. In addition, to capture higher-level semantic similarity, we also used BERTScore *(Zhang et al., [2019])*, with DarijaBERT as the reference model for summarization, and multilingual BERT383838[https://hf.co/google-bert/bert-base-multilingual-cased](https://hf.co/google-bert/bert-base-multilingual-cased "") for translation.

## Citation

```bibtex
@misc{shang2024atlaschat,
  title={Atlas-Chat: Adapting Large Language Models for Low-Resource Moroccan Arabic Dialect},
  author={Shang et al. (2024)},
  year={2024},
  note={arXiv:2409.17912}
}
```

- arXiv: 2409.17912
