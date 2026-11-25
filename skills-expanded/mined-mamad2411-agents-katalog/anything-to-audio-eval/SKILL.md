---
name: anything-to-audio-eval
description: Evaluates a unified diffusion transformer model's ability to generate high-fidelity audio and music conditioned on diverse modalities (text, video, image, audio). It measures acoustic similarity, generation quality/diversity, and cross-modal semantic alignment across multiple standard audio generation benchmarks. Use when the user wants to benchmark on AudioCaps, VGGSound, AVVP, MusicCaps, V2M-bench, or asks about evaluating this task. Reports FAD.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2503.10522
  bibtex_key: tian2025audiox
  confidence: high
---

# anything-to-audio-eval

> AudioX: Diffusion Transformer for Anything-to-Audio Generation — Tian et al. (2025) (arXiv:2503.10522, 2025)

## What this evaluates

Evaluates a unified diffusion transformer model's ability to generate high-fidelity audio and music conditioned on diverse modalities (text, video, image, audio). It measures acoustic similarity, generation quality/diversity, and cross-modal semantic alignment across multiple standard audio generation benchmarks.

## Datasets

- **AudioCaps** — total ?; splits: test (-1)
- **VGGSound** — total ?; splits: test (-1)
- **AVVP** — total ?; splits: test (-1)
- **MusicCaps** — total ?; splits: test (-1)
- **V2M-bench** — total ?; splits: test (-1)

## Metrics

- `FAD` **(primary)** — range: other
  - Frechet Audio Distance computed using VGGish embeddings to assess audio quality and similarity. Lower values indicate better fidelity.
- `IS` — range: other
  - Inception Score evaluating both the quality and diversity of the generated audio samples. Higher values indicate better generation.
- `KL` — range: other
  - Kullback-Leibler Divergence measuring acoustic similarity between generated and reference audio distributions. Lower is better.
- `FD` — range: other
  - Frechet Distance computed using PANNs embeddings to assess audio quality and similarity. Lower is better.
- `PC` — range: other
  - Production Complexity score for audio aesthetics assessment. Higher is better.
- `PQ` — range: other
  - Production Quality score for audio aesthetics assessment. Higher is better.
- `Align.` — range: [0, 1]
  - Semantic alignment score calculated via cosine similarity. Uses CLAP embeddings for text inputs and Imagebind AV embeddings for video inputs.
- `OVL` — range: [1, 100]
  - Overall quality score from subjective user study, rated on a 1-100 scale.
- `REL` — range: [1, 100]
  - Relevance to input score from subjective user study, rated on a 1-100 scale.

## Input / output format

**Input**: Multi-modal conditioning inputs: text prompts, video frames (sampled at 5 fps), image frames, or audio clips. Inputs are provided as conditions during inference to guide the 10-second audio/music generation.

**Output**: 10-second audio or music waveform generated via a diffusion process with 250 inference steps and classifier-free guidance (scale 7.0).

## Scoring recipe

```python
def compute_metrics(predictions, gold, inputs):
    gen_feats = extract_vggish_features(predictions)
    ref_feats = extract_vggish_features(gold)
    fad = frechet_distance(gen_feats, ref_feats)
    is_score = inception_score(predictions)
    kl = kl_divergence(gen_feats, ref_feats)
    if inputs.modality == 'text':
        align = cosine_similarity(inputs.text, extract_clap_features(predictions))
    else:
        align = cosine_similarity(inputs.video, extract_imagebind_features(predictions))
    return {'FAD': fad, 'IS': is_score, 'KL': kl, 'Align.': align}
```

## Common pitfalls

- Align metric switches between CLAP score (text input) and Imagebind AV score (video input), so cross-task comparisons require noting the different embedding models.
- FAD and IS are highly sensitive to the number of generated samples and audio preprocessing (e.g., sampling rate, normalization); results may vary if not matched to the paper's exact pipeline.
- User study (OVL/REL) uses only 10 professional raters on 25 samples per task, limiting statistical power for subjective claims.

## Evidence (verbatim from paper)

> To quantitatively evaluate our model, we use several metrics: Kullback-Leibler Divergence (KL) for acoustic similarity, Inception Score (IS) for evaluating both the quality and diversity of the generated audio, Frechet Distance (FD) using PANNs [33] and Frechet Audio Distance (FAD) [26] using VGGish [24] for assessing audio quality and similarity, Production Complexity (PC) and Production Quality (PQ) [60] for audio aesthetics assessment, and Alignment (Align.) for evaluating semantic alignment between input and generated audio. For Align., we use CLAP [64] score when the input is text and Imagebind AV score (IB) [20] when the input is video, both calculated using cosine similarity.

## Citation

```bibtex
@misc{tian2025audiox,
  title={AudioX: Diffusion Transformer for Anything-to-Audio Generation},
  author={Tian et al. (2025)},
  year={2025},
  note={arXiv:2503.10522}
}
```

- arXiv: 2503.10522
