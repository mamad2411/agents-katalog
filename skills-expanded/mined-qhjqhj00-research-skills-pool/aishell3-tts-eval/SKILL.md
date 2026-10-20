---
name: aishell3-tts-eval
description: Evaluates the ability of a multi-speaker TTS system to synthesize high-fidelity Mandarin speech that preserves speaker identity across both seen and unseen speakers. It probes zero-shot voice cloning capability and generalization to novel speakers using objective speaker verification metrics. Use when the user wants to benchmark on AISHELL-3, or asks about evaluating this task. Reports SV-EER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2010.11567
  bibtex_key: shi2020aishell3
  confidence: high
---

# aishell3-tts-eval

> AISHELL-3: A Multi-speaker Mandarin TTS Corpus and the Baselines — Yao Shi et al. (2020) (arXiv:2010.11567, 2020)

## What this evaluates

Evaluates the ability of a multi-speaker TTS system to synthesize high-fidelity Mandarin speech that preserves speaker identity across both seen and unseen speakers. It probes zero-shot voice cloning capability and generalization to novel speakers using objective speaker verification metrics.

## Datasets

- **AISHELL-3** — total ?; splits: train (64773), validation (-1), test (-1)

## Metrics

- `Cosine Similarity` — range: [0, 1]
  - Measures the cosine of the angle between speaker embedding vectors extracted from synthesized speech and ground truth/reference audio. Higher values indicate greater speaker identity similarity.
- `SV-EER` **(primary)** — range: percent
  - Speaker Verification Equal-Error-Rate calculated by drawing 10,000 pairs of audio samples per trial. It represents the operating point where the false acceptance rate equals the false rejection rate in a speaker verification task.

## Input / output format

**Input**: Textual content (Mandarin characters/pinyin) and a reference audio clip or mean speaker embedding to condition the synthesis.

**Output**: Synthesized audio waveforms for each prompt.

## Scoring recipe

```python
def evaluate_synthesis(synthesized_audio, reference_audio, audio_pool):
    emb_syn = extract_speaker_embedding(synthesized_audio)
    emb_ref = extract_speaker_embedding(reference_audio)
    cosine_sim = cosine_similarity(emb_syn, emb_ref)
    scores = []
    for _ in range(10000):
        pair = random_sample_pair(audio_pool)
        scores.append(cosine_similarity(extract_speaker_embedding(pair[0]), extract_speaker_embedding(pair[1])))
    eer = compute_equal_error_rate(scores)
    return cosine_sim, eer
```

## Common pitfalls

- Text-dependent and text-independent conditions must be evaluated separately, as they use different reference embeddings (ground truth audio vs. mean speaker embedding).
- Synthesized samples with mis-aligned attention maps must be filtered out using inter-step attention cosine similarity before embedding extraction to avoid skewing results.
- Inference randomness from dropout layers requires generating multiple versions (3 per sample) and selecting the best or averaging, as noted in the protocol.

## Evidence (verbatim from paper)

> In both trials, we synthesize 20 text-dependent and 20 text-independent utterances for every speaker, where text-dependent means the ground-truth audio with the same textual content is used to extract the speaker embedding, while text-independent is using the speakers’ respective mean embedding vectors as the reference. ... Cosine Similarity. We use cosine function to measure speaker embedding vector similarity, which is a common method used in speaker verification systems. ... SV-EER. We also make use of the concept of Speaker Verification (SV) Equal-Error-Rate (EER) as an objective evaluation index. ... To evaluate the system using the EER measure, we draw 10,000 pairs of samples from a pool of audio samples per trial.

## Citation

```bibtex
@misc{shi2020aishell3,
  title={AISHELL-3: A Multi-speaker Mandarin TTS Corpus and the Baselines},
  author={Yao Shi et al. (2020)},
  year={2020},
  note={arXiv:2010.11567}
}
```

- arXiv: 2010.11567
