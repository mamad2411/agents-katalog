---
name: training-optimization
description: "Use when training or fine-tuning a deep model and tuning it for best accuracy. Covers transfer learning, two-phase fine-tuning, discriminative/layer-wise LR, LR schedules + warmup, regularization tuned to over/under-fit (dropout, weight decay, label smoothing, MixUp), mixed precision, gradient checkpointing, EMA, checkpoint/resume, and fitting a GPU/time budget. Triggers on 'fine-tune', 'train the model', 'best hyperparameters', 'overfitting', 'learning rate', 'out of memory', 'training is too slow'."
---

# Training & Fine-Tuning

Best-practice recipe for transfer-learning a strong model, and how to fix over/under-fitting.

## Fine-tuning recipe (default that works)
1. **Transfer learning**: start from ImageNet/pretrained weights; train from scratch only with lots of data.
2. **Two phases**: (1) freeze backbone, train the new head; (2) unfreeze and fine-tune end-to-end at a lower LR.
3. **Discriminative / layer-wise LR**: small LR for early backbone layers, higher for the head. Biggest single fine-tuning win.
4. **Schedule**: cosine decay with a short warmup. Log the LR curve.
5. **Optimizer**: AdamW (decoupled weight decay). Gradient clipping ~1.0.
6. **Selection**: checkpoint the best epoch by the **validation** metric; early stopping.

## Diagnose then regularize (don't guess)
- **Overfitting** (train accuracy keeps rising while val loss rises or plateaus): raise weight decay, dropout, label smoothing; add MixUp; stronger-but-domain-appropriate augmentation; reduce epochs/patience; smaller/less-capacity head.
- **Underfitting** (train acc low too): reduce regularization, raise LR / capacity / resolution, train longer, check data quality.
- Match augmentation to the domain - do **not** use aggressive photometric/geometric ops that destroy the signal (e.g., harsh color/solarize on medical scans, or flips that change semantics).

## Compute & memory (fit the budget)
- **Mixed precision (AMP)** always on GPU.
- **Gradient checkpointing** to fit high resolution / big models in limited VRAM (~3× memory saving, ~30% slower).
- **Small batch + gradient accumulation** to keep an effective batch size when VRAM is tight; **freeze BatchNorm** stats at very small batch (LayerNorm backbones like ConvNeXt are safer there).
- **Preprocess once to disk** if per-epoch CPU work (decode/enhance) starves the GPU - huge speedups.
- Budget = seconds/epoch × epochs × models. Measure on a quick run first; pick resolution/epochs to fit the quota. Prefer one honest fit over a run that dies mid-way.

## Robustness
- Fixed seeds; **checkpoint per epoch + resume** so an interrupted long run continues, not restarts.
- EMA of weights and/or averaging often helps generalization - but verify it beats the plain best checkpoint on val before keeping it.
