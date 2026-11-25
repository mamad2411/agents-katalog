---
name: apptek-callcenter-asr-eval
description: This benchmark evaluates automatic speech recognition (ASR) systems on their ability to transcribe long-form, spontaneous call-center dialogues across 14 English accents. It specifically probes robustness to non-standard accents, conversational speech patterns, and sensitivity to audio segmentation strategies. Use when the user wants to benchmark on AppTek Call-Center Dialogues, or asks about evaluating this task. Reports WER.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 2604.27543
  bibtex_key: beck2026apptekcallcenter
  confidence: high
---

# apptek-callcenter-asr-eval

> AppTek Call-Center Dialogues: A Multi-Accent Long-Form Benchmark for English ASR — Beck et al. (2026) (arXiv:2604.27543, 2026)

## What this evaluates

This benchmark evaluates automatic speech recognition (ASR) systems on their ability to transcribe long-form, spontaneous call-center dialogues across 14 English accents. It specifically probes robustness to non-standard accents, conversational speech patterns, and sensitivity to audio segmentation strategies.

## Datasets

- **AppTek Call-Center Dialogues** — total ?; splits: test (-1)

## Metrics

- `WER` **(primary)** — range: percent
  - Word Error Rate calculated as (S+D+I)/N, where S=substitutions, D=deletions, I=insertions, N=reference words. Scoring follows the Hugging Face OpenASR leaderboard protocol with case normalization, punctuation removal, number normalization, and an additional dataset-specific normalization step.

## Input / output format

**Input**: Audio recordings of agent-customer call-center dialogues, segmented into short utterances using one of five strategies: manual boundaries, proprietary segmenter, Silero VAD, or fixed 30s/60s windows.

**Output**: Raw transcribed text corresponding to the input audio segment.

## Scoring recipe

```python
def compute_wer(predictions, references):
    # Apply dataset-specific normalization first
    pred = normalize_dataset(predictions)
    ref = normalize_dataset(references)
    # Apply OpenASR leaderboard normalizations
    pred = normalize_case(pred)
    ref = normalize_case(ref)
    pred = remove_punctuation(pred)
    ref = remove_punctuation(ref)
    pred = normalize_numbers(pred)
    ref = normalize_numbers(ref)
    # Calculate WER per session and average
    wer_scores = [calculate_wer(p, r) for p, r in zip(pred, ref)]
    return sum(wer_scores) / len(wer_scores) * 100
```

## Common pitfalls

- Segmentation strategy drastically changes WER; models perform best with manual boundaries but fail with fixed 60s chunks.
- Failing to apply the paper's dataset-specific normalization causes inconsistent scoring across models with different output formats.
- Assuming lower average WER implies better accent robustness; the paper shows accent gap and average performance do not correlate.

## Evidence (verbatim from paper)

> Recognition performance was measured using word error rate (WER). Although recognition was done on segmented audio, scoring was aggregated per-session to reflect full conversational interactions. Scoring follows the Hugging Face OpenASR leaderboard protocol, including case normalization, punctuation removal, and number normalization. To ensure consistent scoring across models with differing output formats, a dataset-specific normalization was additionally applied prior to evaluation, which reduced WER by approximately 0.8-1.1% absolute consistently across all models and test sets.

## Citation

```bibtex
@misc{beck2026apptekcallcenter,
  title={AppTek Call-Center Dialogues: A Multi-Accent Long-Form Benchmark for English ASR},
  author={Beck et al. (2026)},
  year={2026},
  note={arXiv:2604.27543}
}
```

- arXiv: 2604.27543
