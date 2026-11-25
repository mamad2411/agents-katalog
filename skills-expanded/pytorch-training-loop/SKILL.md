---
name: pytorch-training-loop
description: Use when writing or reviewing a PyTorch training loop. Covers correct train/eval modes, gradient handling, mixed precision, checkpointing, reproducibility, and device management.
---

# PyTorch Training Loop

## Overview

A correct PyTorch loop has a precise sequence of operations. Getting the order or the modes wrong produces silent bugs (no gradients, dropout active at eval, leaked compute graphs). This skill encodes the canonical, production-ready loop.

## When to use

- Writing a training loop from scratch.
- Debugging a model that won't learn or OOMs.
- Reviewing PyTorch training code.

## Canonical loop

```python
import torch
from torch.amp import autocast, GradScaler

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
scaler = GradScaler(enabled=(device == "cuda"))
best_val = float("inf")

for epoch in range(num_epochs):
    # ---- TRAIN ----
    model.train()
    for x, y in train_loader:
        x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)
        optimizer.zero_grad(set_to_none=True)
        with autocast(device_type=device, enabled=(device == "cuda")):
            out = model(x)
            loss = criterion(out, y)
        scaler.scale(loss).backward()
        scaler.unscale_(optimizer)
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        scaler.step(optimizer)
        scaler.update()

    # ---- VALIDATE ----
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for x, y in val_loader:
            x, y = x.to(device), y.to(device)
            val_loss += criterion(model(x), y).item() * x.size(0)
    val_loss /= len(val_loader.dataset)

    # ---- CHECKPOINT BEST ----
    if val_loss < best_val:
        best_val = val_loss
        torch.save({"model": model.state_dict(),
                    "optimizer": optimizer.state_dict(),
                    "epoch": epoch}, "best.pt")
```

## Non-negotiable rules

1. `model.train()` before training, `model.eval()` before validation/inference (toggles dropout & batchnorm).
2. `optimizer.zero_grad()` **every step** — gradients accumulate otherwise.
3. Wrap validation/inference in `torch.no_grad()` (or `inference_mode()`) to save memory.
4. Detach when logging: `loss.item()`, not `loss` — keeping tensors leaks the graph and OOMs.
5. Clip gradients for RNNs/transformers to prevent explosions.

## Reproducibility header

```python
import torch, numpy as np, random
def seed_everything(seed=42):
    random.seed(seed); np.random.seed(seed)
    torch.manual_seed(seed); torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

## Pitfalls

- **Forgetting `zero_grad`** → gradients pile up, training diverges.
- **`eval()` never called** → dropout/batchnorm corrupt validation metrics.
- **Accumulating `total_loss += loss`** (tensor, not `.item()`) → memory explosion.
- **DataLoader with `num_workers=0`** on large data → CPU-bound; raise workers + `pin_memory=True`.
- **LR too high** → NaN loss; see the `ml-debugging` skill.

## Hand-off

A checkpointed model + seed config that experiment-tracking logs and model-serving loads for inference.
