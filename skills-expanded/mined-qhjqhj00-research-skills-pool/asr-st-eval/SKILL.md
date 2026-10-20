---
name: asr-st-eval
description: Evaluates multilingual automatic speech recognition and speech translation capabilities across diverse language pairs and domains. It also probes cross-lingual semantic alignment through speech-to-speech retrieval and integration with large language models. Use when the user wants to benchmark on Aishell, LibriSpeech, CoVoSTv2, Fleurs, CommonVoice, MLS, VoxPopuli, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2511.14410
  bibtex_key: liu2025tta
  confidence: high
---

# asr-st-eval

> TTA: Transcribe, Translate and Alignment for Cross-lingual Speech Representation — Liu et al. (2025) (arXiv:2511.14410, 2025)

## What this evaluates

Evaluates multilingual automatic speech recognition and speech translation capabilities across diverse language pairs and domains. It also probes cross-lingual semantic alignment through speech-to-speech retrieval and integration with large language models.

## Datasets

- **Aishell** — total ?; splits: test (-1)
- **LibriSpeech** — total ?; splits: test-clean (-1)
- **CoVoSTv2** — total ?; splits: test (-1)
- **Fleurs** — total ?; splits: dev+test (-1)
- **CommonVoice** — total ?; splits: test (-1)
- **MLS** — total ?; splits: test (-1)
- **VoxPopuli** — total ?; splits: test (-1)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate: the minimum number of word edits (insertions, deletions, substitutions) required to change the predicted transcript into the reference transcript, normalized by the number of words in the reference.
- `BLEU` — range: percent
  - Bilingual Evaluation Understudy: geometric mean of modified n-gram precisions (typically up to 4-grams) with a brevity penalty to discourage overly short translations.
- `Retrieval Accuracy` — range: percent
  - Percentage of query utterances correctly matched to their semantically aligned counterpart in another language based on cosine similarity of extracted speech embeddings.

## Input / output format

**Input**: Raw speech audio files. For ASR-LLM probing, speech inputs paired with text-based prompts like 'Please repeat the following content:'.

**Output**: Transcribed text, translated text, or language ID labels. For retrieval, cosine similarity scores between query and candidate embeddings.

## Scoring recipe

```python
def compute_metrics(predictions, references):
    wer = 100 * (edit_distance(predictions, references) / len(references))
    bleu = compute_bleu(predictions, references) * 100
    return {'WER': wer, 'BLEU': bleu}

def compute_retrieval_accuracy(embeddings, labels):
    sim_matrix = cosine_similarity(embeddings)
    correct = sum(np.argmax(sim_matrix[i]) == labels[i] for i in range(len(labels)))
    return 100 * correct / len(labels)
```

## Common pitfalls

- Zero-shot generalization on Fleurs is notably weaker than on in-distribution benchmarks like Aishell or LibriSpeech.
- Joint ASR-ST training does not inherently improve ASR WER unless it introduces new ST data sources beyond the ASR corpus.

## Evidence (verbatim from paper)

> A comprehensive evaluation of ASR and ST performance across multiple benchmarks is presented in Table [1]. The ZT-based models are directly compared against the Whisper series in terms of model scale, recognition WER, and translation BLEU score.

## Citation

```bibtex
@misc{liu2025tta,
  title={TTA: Transcribe, Translate and Alignment for Cross-lingual Speech Representation},
  author={Liu et al. (2025)},
  year={2025},
  note={arXiv:2511.14410}
}
```

- arXiv: 2511.14410
