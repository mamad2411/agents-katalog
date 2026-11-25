---
name: anim-400k-eval
description: Evaluates automated end-to-end video dubbing systems by testing their ability to generate synchronized English audio from Japanese source video, specifically probing prosody matching, timing alignment, and multi-speaker isolation capabilities. Use when the user wants to benchmark on Anim-400K, or asks about evaluating this task. Reports MUSHRA.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2401.05314
  bibtex_key: cai2024anim400k
  confidence: high
---

# anim-400k-eval

> ANIM-400K: A Large-Scale Dataset for Automated End-To-End Dubbing of Video — Cai et al. (2024) (arXiv:2401.05314, 2024)

## What this evaluates

Evaluates automated end-to-end video dubbing systems by testing their ability to generate synchronized English audio from Japanese source video, specifically probing prosody matching, timing alignment, and multi-speaker isolation capabilities.

## Datasets

- **Anim-400K** — total 437000; splits: test (-1); repo https://github.com/davidmchan/Anim400K

## Metrics

- `MUSHRA` **(primary)** — range: [0, 100]
  - MUlti Stimulus test with Hidden Reference and Anchor. Listeners rate generated audio samples on a standardized 0-100 scale against a concealed reference (gold standard dub) and anchor points (baseline auto-generated dub). Higher scores indicate better audio quality, synchronization, and naturalness.

## Input / output format

**Input**: Video clip with Japanese and English audio tracks, start/end timestamps, ASR transcripts for both languages, English subtitles for Japanese audio, speaker diarization IDs, and a separated backing audio track with a mixing ratio.

**Output**: Generated English dubbed audio track synchronized to the video, ideally matching the original timing, prosody, and speaker characteristics.

## Scoring recipe

```python
# MUSHRA Evaluation Protocol
# 1. Present test sample, hidden reference (gold dub), and anchor (baseline dub) to listeners
# 2. Listeners rate audio quality/sync on a 0-100 scale
# 3. Compute mean score across all listeners and clips
# Higher score indicates better dubbing quality
```

## Common pitfalls

- Using Mean Opinion Score (MOS) instead of MUSHRA, which the authors explicitly warn is highly dependent on user-specific factors and less reliable for dubbing evaluation.
- Ignoring multi-speaker clips, which require complex speaker isolation and reproduction that current systems struggle with.
- Failing to use the provided backing track and mixing ratio, leading to unnatural audio levels in generated dubs.

## Evidence (verbatim from paper)

> While many methods use “Mean Opinion Scoring (MOS)” scores to evaluate their approaches, these ratings are well known to be dependent on a wide range of user-dependent factors. Instead, we recommend the use of MUSHRA (MUlti Stimulus test with Hidden Reference and Anchor) to evaluate automated dubbing approaches on the Anim-400K dataset. MUSHRA involves presenting the listener with a specified quantity of test samples, a concealed variation of the reference, and one or more anchor points.

## Citation

```bibtex
@misc{cai2024anim400k,
  title={ANIM-400K: A Large-Scale Dataset for Automated End-To-End Dubbing of Video},
  author={Cai et al. (2024)},
  year={2024},
  note={arXiv:2401.05314}
}
```

- arXiv: 2401.05314
