---
name: accentbox-eval
description: Evaluates a zero-shot text-to-speech system's ability to generate speech with high-fidelity target accents while preserving the reference speaker's voice. It probes the model's capacity to disentangle accent characteristics from speaker identity using continuous embeddings, measuring both objective acoustic similarity and subjective listener preference across inherent and cross-accent generation tasks. Use when the user wants to benchmark on Common Voice v17.0 (English), VCTK, LibriTTS-R (clean), or asks about evaluating this task. Reports Accent Cosine Similarity (AccCos).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2409.09098
  bibtex_key: zhong2024accentbox
  confidence: high
---

# accentbox-eval

> AccentBox: Towards High-Fidelity Zero-Shot Accent Generation — Zhong et al. (2024) (arXiv:2409.09098, 2024)

## What this evaluates

Evaluates a zero-shot text-to-speech system's ability to generate speech with high-fidelity target accents while preserving the reference speaker's voice. It probes the model's capacity to disentangle accent characteristics from speaker identity using continuous embeddings, measuring both objective acoustic similarity and subjective listener preference across inherent and cross-accent generation tasks.

## Datasets

- **Common Voice v17.0 (English)** — total ?; splits: seen_train (-1), seen_val (-1), seen_test (-1), unseen_val (-1), unseen_test (-1)
- **VCTK** — total ?; splits: finetune (-1), test (-1)
- **LibriTTS-R (clean)** — total ?; splits: pretrain (-1)

## Metrics

- `Accent Cosine Similarity (AccCos)` **(primary)** — range: [0, 1]
  - Cosine similarity between accent embeddings extracted from reference and generated speech using AID models. Higher values indicate better accent fidelity.
- `Speaker Cosine Similarity (SpkCos)` — range: [0, 1]
  - Cosine similarity between speaker embeddings extracted from reference and generated speech using Resemblyzer. Higher values indicate better speaker preservation.
- `Accent Similarity Preference` — range: percent
  - Percentage of listeners preferring a system's output over a baseline in ABC ranking or AB preference tests based on accent similarity.

## Input / output format

**Input**: Reference speech utterance (fixed 24th utterance per speaker) and target text (Comma Gets a Cure passage, 23 sentences).

**Output**: Synthesized 24kHz audio waveform matching the target accent and reference speaker.

## Scoring recipe

```python
def compute_acc_cos(reference_speech, generated_speech, aid_model):
    ref_emb = aid_model.encode(reference_speech)
    gen_emb = aid_model.encode(generated_speech)
    return cosine_similarity(ref_emb, gen_emb)

def compute_spk_cos(reference_speech, generated_speech):
    ref_emb = resemblyzer.encode(reference_speech)
    gen_emb = resemblyzer.encode(generated_speech)
    return cosine_similarity(ref_emb, gen_emb)
```

## Common pitfalls

- WER is explicitly avoided because ASR models are biased against accents; using it would conflate accent fidelity with recognition difficulty rather than generation quality.
- Subjective listening tests are only conducted on two accents (American and Irish) due to budget constraints, so preference results do not generalize to all accents.
- Accent embeddings are extracted using two different AID models to prevent bias toward the proposed system, which could skew similarity scores if only the proposed model's embeddings were used.

## Evidence (verbatim from paper)

> (i) Accent Cosine Similarity (AccCos): We use two AID models #4 and #6 to extract accent embeddings, and calculate cosine distances between reference and generated speech, avoiding biases towards Proposed which is conditioned on embeddings from #6. (ii) Speaker Cosine Similarity (SpkCos): We use Resemblyzer [37] to extract speaker embeddings of generated speech and compare them to reference speech (speaker) for cosine distance calculation.

## Citation

```bibtex
@misc{zhong2024accentbox,
  title={AccentBox: Towards High-Fidelity Zero-Shot Accent Generation},
  author={Zhong et al. (2024)},
  year={2024},
  note={arXiv:2409.09098}
}
```

- arXiv: 2409.09098
