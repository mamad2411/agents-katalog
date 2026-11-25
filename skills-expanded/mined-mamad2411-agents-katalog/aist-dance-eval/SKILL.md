---
name: aist-dance-eval
description: Evaluates the quality, diversity, and music-motion synchronization of generated 3D dance sequences. It probes a model's ability to synthesize physically plausible, choreographically diverse, and rhythm-aligned human motion from audio input. Use when the user wants to benchmark on AIST++, or asks about evaluating this task. Reports FID_k.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2203.13055
  bibtex_key: li2022bailando
  confidence: high
---

# aist-dance-eval

> Bailando: 3D Dance Generation by Actor-Critic GPT with Choreographic Memory — Li et al. (2022) (arXiv:2203.13055, 2022)

## What this evaluates

Evaluates the quality, diversity, and music-motion synchronization of generated 3D dance sequences. It probes a model's ability to synthesize physically plausible, choreographically diverse, and rhythm-aligned human motion from audio input.

## Datasets

- **AIST++** — total 992; splits: train (952), test (40)

## Metrics

- `FID_k` **(primary)** — range: [0, ∞) (lower is better)
  - Fréchet Inception Distance computed on kinetic features (velocities and energies) extracted using the official AIST++ evaluation toolbox. Lower values indicate higher motion quality.
- `FID_g` — range: [0, ∞) (lower is better)
  - Fréchet Inception Distance computed on geometric features (3D joint positions relative to templates) extracted using the official AIST++ evaluation toolbox. Lower values indicate better choreographic structure.
- `Div_k` — range: [0, ∞) (higher is better)
  - Average pairwise kinetic feature distance among generated motion sequences, measuring choreographic variety. Higher values indicate greater diversity.
- `Div_g` — range: [0, ∞) (higher is better)
  - Average pairwise geometric feature distance among generated motion sequences, measuring choreographic variety. Higher values indicate greater diversity.
- `Beat Align Score` — range: [0, 1] (higher is better)
  - Beat Align Score: 1/|B^m| * sum_{t^m in B^m} exp(-min_{t^d in B^d} ||t^d - t^m||^2 / (2*sigma^2)), where B^d and B^m are dance and music beat times, and sigma=3. Higher values indicate better rhythm synchronization.
- `User Study` — range: percent
  - Winning rate in pairwise human preference tests where participants choose which of two dance videos (model vs. baseline/ground truth) dances better to the music.

## Input / output format

**Input**: Target music audio features (438-dim MFCC, delta, CQT, tempogram, onset strength) and a pair of starting pose codes (randomly sampled or manually specified).

**Output**: Autoregressively generated sequence of discrete pose codes representing 3D dance movements, matching the duration of the input music.

## Scoring recipe

```python
def compute_metrics(generated_dances, reference_dances, music_beats, dance_beats):
    gen_feats = extract_features(generated_dances) # kinetic or geometric
    ref_feats = extract_features(reference_dances) # AIST++ train+test
    fid = frechet_distance(gen_feats, ref_feats)
    div = average_pairwise_distance(gen_feats)
    bas = 0.0
    for t_m in music_beats:
        min_dist = min(abs(t_d - t_m) for t_d in dance_beats)
        bas += math.exp(-min_dist**2 / (2 * 3**2))
    bas /= len(music_beats)
    return fid, div, bas
```

## Common pitfalls

- FID is calculated against the full AIST++ dataset (train + test), not just the test split.
- Beat Align Score uses a fixed Gaussian width sigma=3; changing this significantly alters the score.
- Diversity is computed as average feature distance, but high diversity can sometimes correlate with jittery/unrealistic motions, which FID penalizes.

## Evidence (verbatim from paper)

> For quantitative evaluations, we measure the generated dance from three perspectives: the quality of generated dances, the diversity of motions and the alignment between the rhythms of music and generated movements. In concrete, for the dance quality, we calculate the Fréchet Inception Distances (FID) [13] between the generated dance and all motion sequences (including training and test data) of the AIST++ dataset on kinetic features [33] (denoted as  $k$ ) and geometric features [32] (denoted as  $g$ ), which are both extracted using the toolbox of [12]. As to the diversity, we compute the average feature distance of generated movements following [30]. Regarding to the alignment between music and generated motions, we calculate the average temporal distance between each music beat and its closest dance beat as the Beat Align Score:

## Citation

```bibtex
@misc{li2022bailando,
  title={Bailando: 3D Dance Generation by Actor-Critic GPT with Choreographic Memory},
  author={Li et al. (2022)},
  year={2022},
  note={arXiv:2203.13055}
}
```

- arXiv: 2203.13055
