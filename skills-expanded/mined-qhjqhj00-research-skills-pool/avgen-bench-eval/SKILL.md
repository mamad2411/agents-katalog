---
name: avgen-bench-eval
description: Evaluates the multi-granular capabilities of Text-to-Audio-Video (T2AV) generation models across basic uni-modal fidelity, cross-modal synchronization, and fine-grained dimensions. It probes specific capabilities including text rendering, facial consistency, musical pitch control, speech coherence, and physical plausibility to reveal systematic failure modes in current generative systems. Use when the user wants to benchmark on AVGen-Bench, or asks about evaluating this task. Reports Total.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.08540
  bibtex_key: zhou2026avgenbench
  confidence: high
---

# avgen-bench-eval

> AVGen-Bench: A Task-Driven Benchmark for Multi-Granular Evaluation of Text-to-Audio-Video Generation — Zhou et al. (2026) (arXiv:2604.08540, 2026)

## What this evaluates

Evaluates the multi-granular capabilities of Text-to-Audio-Video (T2AV) generation models across basic uni-modal fidelity, cross-modal synchronization, and fine-grained dimensions. It probes specific capabilities including text rendering, facial consistency, musical pitch control, speech coherence, and physical plausibility to reveal systematic failure modes in current generative systems.

## Datasets

- **AVGen-Bench** — total ?; splits: test (-1)

## Metrics

- `Total` **(primary)** — range: [0, 100]
  - Aggregate score: 0.2*S_basic + 0.2*S_cross + 0.6*S_fine. S_basic is mean of normalized Vis and Aud(PQ). S_cross is mean of normalized AV-Sync and Lip-Sync. S_fine is mean of Text, Face, Music, Speech, Lo-Phy*20, Hi-Phy, and Holistic.
- `Vis` — range: [0, 1]
  - Visual Quality score assessing cinematic aesthetics, lighting, and composition.
- `Aud (PQ)` — range: [0, 10]
  - Audio Production Quality score measuring acoustic clarity and studio-like fidelity.
- `AV-Sync` — range: [0, ∞) (lower is better)
  - Mean absolute temporal offset between audio and video streams.
- `Lip-Sync` — range: [0, ∞) (lower is better)
  - Frame-level error between lip movements and speech audio.
- `Text` — range: [0, 100]
  - Text Rendering Quality score evaluating explicit and incidental text legibility.
- `Face` — range: [0, 100]
  - Facial Consistency score measuring identity stability across frames.
- `Music` — range: [0, 100]
  - Pitch Accuracy score evaluating correct generation of specified musical notes/chords.
- `Speech` — range: [0, 100]
  - Speech Intelligibility & Coherence score assessing clarity and instruction adherence.
- `Lo-Phy` — range: [0, 100]
  - Low-Level Kinematic Plausibility score for natural motion and object stability.
- `Hi-Phy` — range: [0, 100]
  - High-Level Causal Reasoning score for physically accurate phenomena simulation.
- `Holistic` — range: [0, 100]
  - Holistic Semantic Alignment score for overall prompt adherence across complex constraints.

## Input / output format

**Input**: Text prompt specifying a visual scene, audio requirements, and optional constraints (e.g., exact text to render, musical notes, dialogue script).

**Output**: Synchronized audio-video clip (typically 720p resolution, ~10 seconds duration, though model-specific constraints apply).

## Scoring recipe

```python
vis_norm = vis_score * 100
aud_norm = aud_pq_score * 10
av_norm = 100 * max(0, 1 - av_sync_offset / 0.5)
lip_norm = 100 * max(0, 1 - lip_sync_error / 8)
S_basic = mean(vis_norm, aud_norm)
S_cross = mean(av_norm, lip_norm)
S_fine = mean(text, face, music, speech, lo_phy * 20, hi_phy, holistic)
total = 0.2 * S_basic + 0.2 * S_cross + 0.6 * S_fine
return total
```

## Common pitfalls

- AV-Sync and Lip-Sync use a 'lower is better' convention, while all other metrics are 'higher is better'.
- Audio Production Quality (PQ) is scaled 0-10, whereas visual/text/physical metrics are scaled 0-100; direct averaging without normalization causes incorrect Total scores.
- Physical plausibility is split into low-level kinematics and high-level causal reasoning, often requiring different specialist evaluators (e.g., VideoPhy2 for Lo-Phy).

## Evidence (verbatim from paper)

> For compact model-level comparison, we also report a Total score in Table 2: Total = 0.2S_basic + 0.2S_cross + 0.6S_fine, where S_basic = mean(Vis × 100, Aud(PQ) × 10), S_cross = mean(100·max(0,1-AV/0.5), 100·max(0,1-Lip/8)), and S_fine = mean(Text, Face, Music, Speech, Lo-Phy × 20, Hi-Phy, Holistic).

## Citation

```bibtex
@misc{zhou2026avgenbench,
  title={AVGen-Bench: A Task-Driven Benchmark for Multi-Granular Evaluation of Text-to-Audio-Video Generation},
  author={Zhou et al. (2026)},
  year={2026},
  note={arXiv:2604.08540}
}
```

- arXiv: 2604.08540
