---
name: actormind-eval
description: This benchmark evaluates a model's ability to perform speech role-playing by generating persona-consistent, emotionally grounded audio responses. It specifically probes the model's capacity for accurate voice impersonation, precise content delivery, and alignment with target emotional prosody in a conversational context. Use when the user wants to benchmark on ActorMindBench, or asks about evaluating this task. Reports RP-MOS.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.11103
  bibtex_key: chen2026actormind
  confidence: high
---

# actormind-eval

> ActorMind: Emulating Human Actor Reasoning for Speech Role-Playing — Xi Chen et al. (2026) (arXiv:2604.11103, 2026)

## What this evaluates

This benchmark evaluates a model's ability to perform speech role-playing by generating persona-consistent, emotionally grounded audio responses. It specifically probes the model's capacity for accurate voice impersonation, precise content delivery, and alignment with target emotional prosody in a conversational context.

## Datasets

- **ActorMindBench** — total ?; splits: train (-1), test (-1); repo https://github.com/OzymandiasChen/ActorMind

## Metrics

- `RP-MOS` **(primary)** — range: [1, 5]
  - Role-Playing Mean Opinion Score adapted from standard MOS. Ranges from 1 to 5. Evaluates two aspects: (1) Exact Delivery (voice resemblance and correct content; failure yields a score of 1), and (2) Emotion Expression (alignment of prosodic cues like tone, tempo, and intensity with the original ground-truth speech segment).

## Input / output format

**Input**: Role profile, contextual dialogue, emotional cues, target script/text to be spoken, and reference audio for voice cloning.

**Output**: Generated speech audio matching the target script and emotional cues.

## Scoring recipe

```python
def compute_rp_mos(generated_speech, reference_speech, target_text, voice_ref):
    # Prerequisite: Exact Delivery
    if not resembles_voice(generated_speech, voice_ref) or not matches_text(generated_speech, target_text):
        return 1
    # Emotion Expression: align prosody with ground truth
    prosody_sim = measure_prosodic_alignment(generated_speech, reference_speech)
    # Human evaluators map alignment to 1-5 scale per Appendix B.2
    return human_map_to_rpmos(prosody_sim)
```

## Common pitfalls

- RP-MOS is not a standard MOS; it explicitly adapts the scale for role-playing with a hard prerequisite for Exact Delivery.
- If Exact Delivery fails (wrong voice or incorrect words), the score is automatically 1, overriding any emotion expression quality.
- Emotion Expression relies on prosodic alignment with original speech segments as a ground-truth proxy, not just subjective listener preference.

## Evidence (verbatim from paper)

> We utilize the mean opinion score (MOS) (Chu and Peng, 2006) to measure the perceived quality of the generated speech. To adapt this metric for the role-playing setting, we introduce the RP-MOS. It ranges from 1 to 5, with 1 indicating the lowest quality and 5 the highest. In the speech role-playing context, we identify two pivotal aspects: (1) Exact Delivery and (2) Emotion Expression.

## Citation

```bibtex
@misc{chen2026actormind,
  title={ActorMind: Emulating Human Actor Reasoning for Speech Role-Playing},
  author={Xi Chen et al. (2026)},
  year={2026},
  note={arXiv:2604.11103}
}
```

- arXiv: 2604.11103
