---
name: asvspoof2019-eval
description: Evaluates the robustness of speaker verification systems and anti-spoofing countermeasures against synthesized, voice-converted, and replayed speech attacks. It measures how effectively systems can distinguish genuine speech from spoofed audio and quantifies the real-world impact of spoofing on authentication reliability. Use when the user wants to benchmark on ASVspoof 2019, or asks about evaluating this task. Reports EER, min-tDCF.
metadata:
  skill_kind: dataset_eval
  source_arxiv: 1911.01601
  bibtex_key: wang2019asvspoof2019
  confidence: high
---

# asvspoof2019-eval

> ASVspoof 2019: A large-scale public database of synthesized, converted and replayed speech — Wang et al. (2019) (arXiv:1911.01601, 2019)

## What this evaluates

Evaluates the robustness of speaker verification systems and anti-spoofing countermeasures against synthesized, voice-converted, and replayed speech attacks. It measures how effectively systems can distinguish genuine speech from spoofed audio and quantifies the real-world impact of spoofing on authentication reliability.

## Datasets

- **ASVspoof 2019** — total ?; splits: development (-1), evaluation (-1)

## Metrics

- `EER` **(primary)** — range: percent
  - Equal Error Rate: the operating point where the False Acceptance Rate (FAR) equals the False Rejection Rate (FRR).
- `min-tDCF` **(primary)** — range: [0, 1]
  - Minimum tandem Detection Cost Function: the minimum value of the t-DCF over all possible decision thresholds. It combines the errors of both the ASV and CM systems into a single metric to quantify the real-world impact of spoofing on ASV reliability.

## Input / output format

**Input**: Raw audio recordings of speech (bona fide target, bona fide non-target/imposter, and spoofed via TTS, VC, or replay).

**Output**: A continuous spoofing score or decision label (bona fide vs. spoof) per utterance, used to compute FAR, FRR, and t-DCF.

## Scoring recipe

```python
# 1. Compute EER for standalone ASV or CM
thresholds = np.linspace(min_score, max_score, 1000)
for t in thresholds:
    far = mean(spoof_scores > t)
    frr = mean(genuine_scores < t)
    if abs(far - frr) < 1e-4:
        eer = far
        break

# 2. Compute min-tDCF for integrated ASV+CM
# t-DCF combines ASV and CM errors with predefined costs and priors
t_dcf_values = []
for t in thresholds:
    # Calculate FAR, FRR for ASV and CM at threshold t
    # Apply cost weights: C1*P_target*FAR + C2*P_spoof*FRR_spoof + ...
    t_dcf = compute_tandem_cost(asv_scores, cm_scores, labels, t)
    t_dcf_values.append(t_dcf)
min_t_dcf = min(t_dcf_values)
```

## Common pitfalls

- Confusing standalone CM EER with integrated ASV+CM min-tDCF; the latter accounts for cascading errors and is the primary metric for real-world impact.
- Evaluating only on development set attacks; the evaluation set contains unseen attack algorithms, making generalization to novel spoofing methods the true test.
- Ignoring the distinction between Logical Access (LA) and Physical Access (PA) scenarios, which have different replay configurations and acoustic environments.

## Evidence (verbatim from paper)

> This section describes the results obtained with the ASVspoof 2019 ASV and CM baselines. The results are presented separately for the LA and PA datasets. The metrics are the equal error rate (EER) and new ASV-centric tandem detection cost function (t-DCF) [12] which combines the errors of both ASV and CM systems into a single metric.

## Citation

```bibtex
@misc{wang2019asvspoof2019,
  title={ASVspoof 2019: A large-scale public database of synthesized, converted and replayed speech},
  author={Wang et al. (2019)},
  year={2019},
  note={arXiv:1911.01601}
}
```

- arXiv: 1911.01601
