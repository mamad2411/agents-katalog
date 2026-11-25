---
name: literature-review
description: "Use when starting an ML task or choosing a method, to research papers/benchmarks and find the best approach and the REALISTIC accuracy ceiling. Finds SOTA, critically appraises reported numbers, and flags claims inflated by data leakage or ROI-cropping. Triggers on 'what's the best model/method for', 'state of the art', 'research papers', 'benchmark', 'how accurate can this get'."
---

# Literature Review (research-first, skeptical)

Never pick a method from memory or hype. Ground it in evidence.

## Do this
1. Delegate breadth to the **`paper-researcher`** agent when available; otherwise run diverse `WebSearch` yourself (by task, by `dataset + "state of the art"`, by method family, by `"patient-level" / "leakage"`).
2. Read the top 2-5 sources. For each, record: **method, dataset + split, headline metric, how the split was done.**

## Appraise every number adversarially
A high number is a hypothesis to disprove, not a target:
- **Whole-input vs ROI/patch?** ROI-crop (lesion already cropped) is a *different, easier* problem than whole-image. Numbers are not comparable.
- **Split integrity?** A random per-sample split with multiple samples per subject causes leakage and inflated scores. Demand group/patient/temporal or the official split.
- **Test size & metric?** A tiny test set or thresholded accuracy is unstable. Prefer AUC / mAP / F1 with confidence intervals.
- **Comparable?** Only the official benchmark split can be compared across papers.

## Output an evidence brief
- SOTA table with columns: method, dataset/split, metric, credibility note.
- **Realistic ceiling**: best *rigorous, leakage-free, comparable* number - the honest target.
- Ranked techniques worth combining, each with evidence + caveat.
- Traps to avoid.
- Sources as markdown links.

## Red flags = distrust, don't chase
99%+ on a hard whole-image medical/vision benchmark almost always means ROI-only or leakage. Say so plainly. The professional move is knowing which numbers are fake.
