---
name: pytorch-training-loop
description: Writes a correct PyTorch training loop with seeding, mixed precision, clipping and resumable checkpoints. Use it to start or fix a training script.
---

# PyTorch training loop

Get the loop right on tiny data before spending hours on big data.

## Steps

1. Seed everything from one function: `random`, `numpy`, `torch.manual_seed`, and `torch.cuda.manual_seed_all`. For a worker-based `DataLoader`, pass a `worker_init_fn` and a seeded `generator`.
2. Pick the device once and move the model and each batch with `.to(device, non_blocking=True)`. Use `pin_memory=True` on CUDA.
3. Per step, in this order: `optimizer.zero_grad(set_to_none=True)`, forward, loss, backward, gradient clipping with `clip_grad_norm_`, `optimizer.step()`, then `scheduler.step()` at the interval the scheduler expects.
4. Mixed precision: wrap the forward and loss in `torch.autocast`, use `GradScaler` for float16 (not needed for bfloat16), and unscale before clipping.
5. Call `model.train()` before training and `model.eval()` with `torch.no_grad()` for validation. Switch back afterwards.
6. Checkpoint model, optimizer, scheduler, scaler, epoch and RNG state to a temp file, then rename it over the last one, so a crash never leaves a half-written file. Keep the best by validation metric.
7. Log training loss, validation metric, learning rate and gradient norm every N steps.
8. Sanity check first: overfit 8 samples to near zero loss. If it cannot, fix the loop before touching hyperparameters.

## Rules

- Never call `.item()` on every step in a hot loop; accumulate tensors and sync periodically.
- Never evaluate on the training split.

## Report

The files written, the overfit test result, and how to resume from a checkpoint.
