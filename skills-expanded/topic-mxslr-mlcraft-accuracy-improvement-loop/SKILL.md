---
name: accuracy-improvement-loop
description: "Use when an existing model's results are disappointing and the user wants higher accuracy - 'accuracy is still too low', 'improve/boost the model', 'why is it bad', 'make it better than the paper', 'combine methods to beat SOTA'. Diagnoses the real bottleneck first (error analysis, learning curves, leakage, saliency), then researches the specific gap, synthesizes a principled combination of techniques from the literature, and ranks next levers by expected impact - with honest ceilings, not magic promises."
---

# Accuracy-Improvement Loop

Do NOT throw random tricks at the model. Diagnose, research the gap, combine principled fixes, verify. This is the loop a professional runs to push toward (and recognize) the ceiling.

## Step 1 - Diagnose the bottleneck (evidence, not guesses)
- **Re-audit leakage FIRST** (`data-rigor-and-leakage`). A suspicious jump/drop is often a split problem. Fixing leakage may *lower* the number - that is success, because it was fake.
- **Learning curves**: train loss down but val loss up means overfitting; both flat or low means underfitting or a data problem; unstable means an LR, batch, or BatchNorm issue.
- **Error analysis**: inspect the confusion matrix and the actual misclassified samples. What do the errors have in common?
- **Saliency check** (Grad-CAM): is the model attending to the *signal* or to an **artifact** (background, labels, muscle/border, watermark, spurious correlation)? Fix the data/preprocessing if so.
- **Per-branch/per-model check**: in fusion/ensembles, is one component dragging the rest down?

## Step 2 - Research the specific gap
Invoke `literature-review` / `paper-researcher` targeted at the *diagnosed* problem (e.g., "small-lesion whole-image classification", "fusion gradient dilution", "class imbalance long-tail"), not the generic task. Extract techniques that address *this* failure mode.

## Step 3 - Synthesize a principled combination
Combine the best-evidenced techniques that target the bottleneck - this is how you "beat existing work": a grounded combination, not one silver bullet. Common high-impact levers (pick by diagnosis):
- **Data/signal**: higher input resolution, better ROI/region focus, artifact removal, cleaner labels, stronger domain-appropriate augmentation, more/balanced data (incl. synthesis only if justified).
- **Architecture**: stronger/more-suitable backbone for *this* dataset (not just the trendiest); attention (CBAM/self-attention); multi-scale features; multi-view/multi-input; **feature-fusion done right** - gated fusion + **deep supervision / auxiliary per-branch losses** to beat gradient dilution when a weak branch drags a fusion.
- **Training**: discriminative LR, better schedule, regularization retuned to the diagnosis, longer training, EMA/SWA, self-distillation, patch-pretraining then whole-image.
- **Inference/aggregation**: TTA, calibrated thresholds, **ensembles** (soft-voting / weighted-by-val / stacking) - output-level fusion is often the cheapest real gain.
- **Weakly-supervised localization** (e.g., GMIC-style) when lesions/objects are tiny in a large input - often both more accurate *and* gives free saliency.

## Step 4 - Rank, run, verify
- Rank candidate levers by **expected impact vs cost**; try the biggest first (usually data/resolution/leakage, then architecture).
- Change **one lever at a time** where feasible so you know what worked.
- Verify with `rigorous-evaluation`; keep only what improves **validation** honestly.

## Honesty (the professor standard)
- Every dataset has a **realistic ceiling**. State it. Do not promise to beat leaky 99% papers.
- Know when you have hit diminishing returns - and say so, instead of chasing noise.
- A defensible, reproducible gain > a fragile record that won't survive review.
