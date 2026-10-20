---
name: audio-to-image-eval
description: Evaluates an audio-to-image generative model's ability to synthesize semantically aligned images from audio prompts. It measures cross-modal alignment, perceptual image quality, and distributional similarity against ground-truth visuals. Use when the user wants to benchmark on Greatest Hits, Landscapes, Into The Wild (ITW), VEGAS, VGGSound, or asks about evaluating this task. Reports Fréchet Inception Distance (FID).
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2501.05413
  bibtex_key: petermann2025seeingsound
  confidence: high
---

# audio-to-image-eval

> Seeing Sound: Assembling Sounds from Visuals for Audio-to-Image Generation — Petermann et al. (2025) (arXiv:2501.05413, 2025)

## What this evaluates

Evaluates an audio-to-image generative model's ability to synthesize semantically aligned images from audio prompts. It measures cross-modal alignment, perceptual image quality, and distributional similarity against ground-truth visuals.

## Datasets

- **Greatest Hits** — total ?; splits: test (-1)
- **Landscapes** — total ?; splits: test (-1)
- **Into The Wild (ITW)** — total ?; splits: test (-1)
- **VEGAS** — total ?; splits: test (-1)
- **VGGSound** — total 1000; splits: test (1000)

## Metrics

- `Audio-Image Similarity (AIS)` — range: [0, 1]
  - Cosine similarity between latent embeddings of the audio prompt and generated image, computed using Wav2CLIP.
- `Image-Image Similarity (IIS)` — range: [0, 1]
  - Cosine similarity between latent embeddings of the ground-truth and generated images, computed using the CLIP visual tower.
- `Fréchet Inception Distance (FID)` **(primary)** — range: [0, ∞)
  - Fréchet distance between the multivariate Gaussian distributions of features extracted from generated and ground-truth images. Lower values indicate better perceptual quality and diversity.

## Input / output format

**Input**: 5-second audio excerpt (processed via AST embeddings) conditioning a diffusion model.

**Output**: 512×512 RGB image.

## Scoring recipe

```python
def evaluate(predictions, gold):
    gen_images = predictions['images']
    gt_images = gold['images']
    audio_clips = gold['audio']
    
    # AIS: cosine similarity via Wav2CLIP
    audio_emb = wav2clip.encode(audio_clips)
    gen_emb = wav2clip.encode(gen_images)
    ais = cosine_similarity(audio_emb, gen_emb).mean()
    
    # IIS: cosine similarity via CLIP visual tower
    gt_emb = clip_vision.encode(gt_images)
    iis = cosine_similarity(gt_emb, gen_emb).mean()
    
    # FID: distribution distance (computed over full dataset)
    fid = frechet_inception_distance(gen_images, gt_images)
    
    return {'AIS': ais, 'IIS': iis, 'FID': fid}
```

## Common pitfalls

- In-sample vs out-of-sample confusion: Models evaluated on datasets they were trained on show inflated metrics due to memorization; the paper highlights out-of-sample results as the fair comparison.
- Metric directionality: FID is lower-is-better, whereas AIS and IIS are higher-is-better. Misinterpreting the sign leads to incorrect model ranking.
- Audio standardization: All audio prompts are standardized to exactly 5 seconds and processed through AST embeddings before conditioning; raw audio lengths vary in source datasets.

## Evidence (verbatim from paper)

> Following recent literature, we evaluate different audio-to-image generative models using the following metrics. Audio-Image Similarity (AIS) aims at evaluating the alignment between a generated image and its audio counterpart, namely by computing cosine similarity between latent embeddings associated with the two modality instances. In accordance with [1, 43], we also employ Wav2CLIP [40] for this purpose. Image-Image Similarity (IIS) is the image analog to what AIS is for audio and measures the semantic similarity between generated and ground-truth images. We utilize the visual tower of CLIP [15] to obtain latent representations from images when implementing IIS. Finally, we adopt Fréchet Inception Distance (FID) [16] to quantify the distance between distribution of the generated and ground-truth images.

## Citation

```bibtex
@misc{petermann2025seeingsound,
  title={Seeing Sound: Assembling Sounds from Visuals for Audio-to-Image Generation},
  author={Petermann et al. (2025)},
  year={2025},
  note={arXiv:2501.05413}
}
```

- arXiv: 2501.05413
