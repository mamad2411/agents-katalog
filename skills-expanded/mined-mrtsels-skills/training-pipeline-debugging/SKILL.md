---
name: training-pipeline-debugging
description: "Use when ML training converges (loss decreases) but evaluation metrics are worse than a trivial baseline (NoOp). Diagnoses and fixes target-format mismatches between model outputs and loss function targets."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [debugging, training, pytorch, gnn, machine-learning]
    related_skills: [systematic-debugging]
---

# Training Pipeline Debugging: Target-Format Mismatch

## Overview

The most common silent bug in GNN/ML training pipelines: **model output format does not match target format**. The loss decreases (because MSE between two tensors of different magnitudes still produces a gradient), but evaluation metrics are meaningless.

## When to Use

- Training loss converges to a reasonable value but evaluation metrics are WORSE than a NoOp baseline (leave input unchanged).
- Position error is 10-100x larger than the uncorrected input's error.
- The model's "improvement" over baseline is *negative* across all configs.
- You changed the model output format but forgot to update the target computation.

## Detection

### Quick Check: Print Shapes + Values

```python
# In the training loop, after one forward pass:
print(f"prediction['coord'] shape: {predictions['coord'].shape}")
print(f"prediction['coord'][0]:  {predictions['coord'][0]}")
print(f"targets['coord'] shape:   {targets['coord'].shape}")
print(f"targets['coord'][0]:      {targets['coord'][0]}")
```

If values are in completely different ranges (e.g. `[-0.02, 0.01, 0.03, -0.01]` vs `[0.59, 0.20, 0.65, 0.25]`), you have a format mismatch.

### The Three-Question Test

1. **What format does the model output?** (xyxy? xywh? cxcywh? delta?)
2. **What format is the target?** (raw GT boxes? delta? normalized?)
3. **Are they the same?** If not, that's your bug.

## Common Patterns

| Model output | Correct target | Wrong target (what NOT to do) |
|---|---|---|
| `Δcx, Δcy, Δw, Δh` (deltas) | `gt_xywh - vlm_xywh` | `raw_gt_xyxy` |
| `x1, y1, x2, y2` (absolute xyxy) | `raw_gt_xyxy` | `gt_xywh` or deltas |
| `cx, cy, w, h` (absolute cxcywh) | `gt_xywh` | `gt_xyxy` |
| Classification logits | integer class indices | bbox coordinates |

## NaN Loss Causes

### 1. LayerNorm on empty tensor

`nn.LayerNorm(hidden_dim)` on a tensor of shape `[0, hidden_dim]`:
- LayerNorm computes `mean` and `std` over the last dim
- With 0 elements, `0/0 = NaN`
- NaN propagates through the entire network

**Fix:**
```python
x = self.norm(x) if x.numel() > 0 else x
```

### 2. BCE on empty tensor

`F.binary_cross_entropy(pred, target)` where both have shape `[0, 1]`:
- Some PyTorch versions return NaN on empty BCE
- Other versions return 0.0 — behavior is version-dependent

**Fix:**
```python
if prediction.numel() == 0 or target.numel() == 0:
    return torch.tensor(0.0, device=prediction.device)
return F.binary_cross_entropy(prediction, target)
```

### 3. Circular imports causing silent hangs

**Pattern (bipartite-gnn-gui case):**
```
data/__init__.py          → from .graph_dataset import GraphDataset
graph_dataset.py           → from graph.builder import BipartiteGraphBuilder
graph/builder.py           → from .schema import ConstraintNode
graph/schema.py            → from data.vlm_output import VLMOutputElement
data/__init__.py (again!)  → ← CYCLE!
```

The import hangs silently — no error, no output, 100% CPU.

**Fix:** Make the offending import lazy:
```python
# In data/__init__.py — remove the eager import
# from .graph_dataset import GraphDataset, collate_graph_samples  # DON'T

# Add a lazy accessor
def _get_graph_dataset():
    from .graph_dataset import GraphDataset, collate_graph_samples
    return GraphDataset, collate_graph_samples
```

**Detection:** Run a simple import test from scratch:
```bash
time python -c "from bipartite_gnn_gui.model.model import BipartiteGNNCorrector"
```
If it hangs for >30s, you have a circular import.

### 4. VLM-GT element count mismatch

Real VLM predictions detect a DIFFERENT number of elements than ground truth. The pipeline assumes both have the same `N`, causing:
```
RuntimeError: The size of tensor a (2) must match the size of tensor b (23)
```

**Fix:** Use Hungarian matching to align VLM predictions with GT:
1. Match VLM → GT using IoU-based Hungarian matching (threshold ~0.3)
2. Build combined element list: matched VLM elements (in GT index order) + unmatched GT (FN) + unmatched VLM (FP)
3. Per-element targets:
   - `coord`: delta for matched, zero-delta for FN/FP
   - `existence`: 1 for matched+FN, 0 for FP
   - `gt_boxes`: GT boxes for GT-indexed positions, zeros for FP

The existing `match_predictions_to_ground_truth()` in `ground_truth.py` provides the Hungarian matching.

## The Fix

In the dataset's `__getitem__` or `build_graph` function:

```python
# BAD: model outputs Δcx,Δcy,Δw,Δh but targets are raw xyxy GT boxes
targets["coord"] = gt_boxes  # WRONG

# GOOD: convert both to same space, compute delta
def _to_cxcywh(boxes):
    x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w, h = x2 - x1, y2 - y1
    return torch.stack([cx, cy, w, h], dim=-1)

gt_xywh = _to_cxcywh(gt_boxes)
vlm_xywh = _to_cxcywh(vlm_boxes)
targets["coord"] = gt_xywh - vlm_xywh  # CORRECT: model predicts deltas
# Keep raw GT for evaluation
targets["gt_boxes"] = gt_boxes
```

## Verification

After fixing, re-run training and compare:

| Metric | Before (wrong) | After (correct) |
|---|---|---|
| Best val_loss | 0.050 | **0.016** (3x lower) |
| Recall | 9.4% | **38%** (4x higher) |
| Size error | 0.328 | **0.117** (2.8x lower) |

Also verify **all training data is actually used**:

```python
# In the training log, check: "Split: 79 train / 20 val"
# 79 = int(99 * 0.8) = 79  ✅   20 = 99 - 79  ✅

# Verify the DataLoader yields all training samples:
num_steps = 0
for _ in train_loader:
    num_steps += 1
print(f"Steps per epoch: {num_steps}")  # Should equal len(train_dataset)
```

Common gotchas:
- `batch_size=None` → each loader item = one sample. Steps = number of training samples.
- `batch_size=N` with collation that doesn't stack HeteroData → steps ≈ samples / N.
- Early stopping can cut training short. Check patience vs actual epoch count.
- Tiny validation sets (e.g. 1-2 samples after 80/20 split) produce noisy val metrics — increase sample count.

If recall improves and loss drops significantly, the fix worked.

## Common Pitfalls

1. **Only fixing one of two locations.** The bug often appears in BOTH the `GraphDataset.__getitem__` AND a standalone `build_graph()` function in experiment scripts.
2. **Forgetting the evaluation path.** The evaluate function may also use `targets["coord"]` as GT reference — add a `targets["gt_boxes"]` key for the raw GT boxes used in evaluation.
3. **The loss still decreases before the fix.** A format mismatch doesn't prevent convergence — it just trains the model to match meaningless targets. Always check against a baseline.

<script id="target-format-verifier">
# Paste into training loop after one forward pass
import torch

def verify_targets_match_outputs(predictions: dict, targets: dict, tolerance: float = 10.0):
    """Check if prediction and target tensors are in the same numeric range."""
    for key in predictions:
        if key not in targets:
            print(f"  ⚠️  prediction has '{key}' but target does not")
            continue
        p, t = predictions[key], targets[key]
        if p.shape != t.shape:
            print(f"  ❌ SHAPE MISMATCH '{key}': pred {p.shape} vs target {t.shape}")
            continue
        p_range = (p.min().item(), p.max().item(), p.mean().item())
        t_range = (t.min().item(), t.max().item(), t.mean().item())
        print(f"  '{key}' pred=[{p_range[0]:.4f},{p_range[1]:.4f}] μ={p_range[2]:.4f}")
        print(f"         tgt=[{t_range[0]:.4f},{t_range[1]:.4f}] μ={t_range[2]:.4f}")
        # Flag if ranges are completely different orders of magnitude
        p_mag = max(abs(p_range[0]), abs(p_range[1]))
        t_mag = max(abs(t_range[0]), abs(t_range[1]))
        if p_mag > 0 and t_mag > 0 and (p_mag / t_mag > tolerance or t_mag / p_mag > tolerance):
            print(f"  ⚠️  RANGE MISMATCH (> {tolerance}x difference)")
</script>

## Related

- `systematic-debugging` skill — general 4-phase root cause debugging
- `AGENTS.md` in project root — project-specific conventions
