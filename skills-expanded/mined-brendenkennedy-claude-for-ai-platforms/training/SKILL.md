---
name: training
description: >
  The train / fine-tune loop conventions — every run reproducible, resumable, tracked. Carries: one
  config-driven entry point (`config-hydra`), seed-everything + cuDNN determinism, checkpoint best
  AND last with epoch/model/optimizer/scheduler/config/git-SHA (so runs resume), metrics streamed to
  the tracker, AMP mixed precision, gradient accumulation, LR scheduling, early stopping, and
  explicit `.to(device)` / dataloader `num_workers` + `pin_memory`. Load before writing or changing
  a training loop, wiring checkpointing/resume, adding a scheduler or early stopping, or debugging a
  run that won't reproduce. Triggers: train, training loop, fine-tune, train.py, epoch, checkpoint,
  ckpt, resume, seed, determinism, cudnn, reproducible run, AMP, autocast, GradScaler, gradient
  accumulation, LR schedule, warmup, early stopping, num_workers, pin_memory, best model, RNG state.
---

# training — the train / fine-tune loop conventions

> On-demand: load this before writing or editing a training loop, wiring checkpoint/resume, or chasing a
> run that won't reproduce. It carries the loop's required shape; the hyperparameters themselves live in
> the config (`config-hydra`), the splits in `datasets`, and the metric logging in `tracking-mlflow`.

## When this applies
Writing `train.py` or a trainer, adding/changing checkpointing or resume, wiring a scheduler, AMP, grad
accumulation, or early stopping, tuning the dataloader, or debugging "why did the same config give a
different result". For the deeper build (architectures, losses), delegate to the `ml-engineer` agent.

## Entry point — driven by the config, not argv
One entry point, all knobs from the composed config so a run is fully described by its config tree. See
`config-hydra` for composition/sweeps — never read `os.environ` or hardcode hyperparameters mid-loop
(the **config-over-constants** always-on convention).

```python
@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig) -> None:
    seed_everything(cfg.seed)                 # <PLACEHOLDER: seed> — record it (see below)
    device = torch.device(cfg.device if torch.cuda.is_available() else "cpu")
    # build model / optimizer / scheduler / loaders from cfg, then train(...)
```

## Seeding & determinism (do this first, every run)
A run that isn't seeded isn't reproducible — this backs the **reproducibility is non-negotiable**
always-on convention.

```python
def seed_everything(seed: int) -> None:
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False    # benchmark=True picks fast nondeterministic kernels
```
- Seed **before** building the model, optimizer, and dataloaders (init and shuffle order depend on it).
- Give each `DataLoader` a `generator=torch.Generator().manual_seed(seed)` and a `worker_init_fn` so
  workers are seeded too.
- **Record the resolved seed** into the tracker and the checkpoint. Any deliberate nondeterminism (e.g.
  `cudnn.benchmark=True` for throughput) is a documented choice, not an accident.

## Checkpointing — save **best** and **last**
Save a checkpoint that is a self-contained resume point, not just weights. Keep two: `last.pt` every
epoch (crash recovery) and `best.pt` on the monitored metric improving.

```python
ckpt = {
    "epoch": epoch,
    "model": model.state_dict(),
    "optimizer": optimizer.state_dict(),
    "scheduler": scheduler.state_dict(),
    "scaler": scaler.state_dict(),          # if using AMP
    "config": OmegaConf.to_container(cfg, resolve=True),
    "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
    "rng": {"torch": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state_all(),
            "numpy": np.random.get_state(), "python": random.getstate()},
    "metric": best_metric,
}
torch.save(ckpt, out_dir / "last.pt")
if improved:
    torch.save(ckpt, out_dir / "best.pt")
```
Log the checkpoint as a tracker artifact (`tracking-mlflow`); pair it with DVC (`data-dvc`) if models
are versioned there.

## Resume — restore state, not just weights
```python
# weights_only=False is REQUIRED here — see the warning below. Never point this at an untrusted file.
ckpt = torch.load(path, map_location=device, weights_only=False)
model.load_state_dict(ckpt["model"]); optimizer.load_state_dict(ckpt["optimizer"])
scheduler.load_state_dict(ckpt["scheduler"]); scaler.load_state_dict(ckpt["scaler"])
torch.set_rng_state(ckpt["rng"]["torch"]); torch.cuda.set_rng_state_all(ckpt["rng"]["cuda"])
np.random.set_state(ckpt["rng"]["numpy"]); random.setstate(ckpt["rng"]["python"])
start_epoch = ckpt["epoch"] + 1
```
A true resume continues the same trajectory — restore optimizer/scheduler/scaler/RNG, not just `model`.

> **`torch.load` defaults to `weights_only=True` since torch 2.6 — and the checkpoint above is not
> weights-only.** Precisely: `weights_only=True` accepts tensors and simple builtins, and rejects arbitrary
> pickled objects. The RNG block above stores `np.random.get_state()` (a numpy tuple), so a bare
> `torch.load(path, map_location=device)` raises `UnpicklingError: Weights only load failed` on a checkpoint
> this very skill told you to write. A checkpoint of *only* tensors + plain dicts/lists/strings loads fine
> under the default — so don't cargo-cult `weights_only=False` everywhere; use it when the checkpoint really
> does carry non-tensor state (RNG, config objects), which the resume dict above does. Never pass it for a
> checkpoint you downloaded — unpickling an untrusted file executes arbitrary code. This bites on resume,
> exactly when you can least afford it.

## The loop — AMP, grad accumulation, scheduler, device
```python
# torch.cuda.amp.GradScaler is DEPRECATED (FutureWarning on torch ≥2.4) — use the torch.amp form:
scaler = torch.amp.GradScaler(device.type, enabled=cfg.amp)
for step, (x, y) in enumerate(loader):
    x, y = x.to(device, non_blocking=True), y.to(device, non_blocking=True)   # explicit device move
    with torch.autocast(device_type=device.type, enabled=cfg.amp):            # device.type, NOT "cuda" —
                                                                              # hardcoding breaks CPU runs
        loss = criterion(model(x), y) / cfg.grad_accum_steps                  # scale for accumulation
    scaler.scale(loss).backward()
    if (step + 1) % cfg.grad_accum_steps == 0:                                # effective batch = bs * accum
        scaler.step(optimizer); scaler.update(); optimizer.zero_grad(set_to_none=True)
scheduler.step()                              # per-epoch here; per-step schedulers step inside the loop
```
- **AMP:** `autocast` + `GradScaler`; checkpoint the scaler (above) so resume matches.
- **Grad accumulation:** simulate a larger batch when it won't fit — divide loss by `grad_accum_steps`
  and step every N; effective batch is `batch_size * grad_accum_steps`.
- **LR schedule:** step **per-epoch** or **per-step** to match the scheduler's contract; include warmup
  where the recipe calls for it. Log the LR each step to the tracker.
- **Device:** move model and every batch explicitly with `.to(device)`; never assume CUDA — fall back to
  CPU when `torch.cuda.is_available()` is False (matches `env-uv`'s GPU sanity check).

## Anomaly detection — the loop above may not apply
One-class / industrial AD (see `datasets` for the layout) trains on **normal samples only**, and its
methods split into two shapes that this skill's loop treats very differently:
- **Gradient-trained** (autoencoder, student–teacher, normalizing-flow) — the loop above holds, but the
  "loss" is reconstruction/distillation error on normal data, and there is **no label `y`**. Early stopping
  on a *val loss over normal parts* is weak (it says nothing about defect separability) — prefer stopping
  on **val image-level AUROC** using a small held-out defect set (see `evaluation`).
- **Fit, not trained** (PaDiM, PatchCore, and most memory-bank/embedding methods) — there is **no backward
  pass at all**. You run a frozen pretrained backbone over the normal set and store features. Epochs, AMP,
  schedulers, and `optimizer.step()` are all meaningless here; forcing them into a training loop just to
  satisfy the skeleton produces confusing dead code. The "checkpoint" is the fitted memory bank / Gaussian
  stats — still save it with the config + git SHA, so it's just as reproducible.

If you're on a fit-not-trained method, say so explicitly in the run and skip the loop rather than faking a
one-epoch pass. Reproducibility still applies: seed the sampling/coreset step.

## Early stopping
Monitor the **validation** metric (never train loss), stop after `patience` epochs without improvement,
and keep `best.pt` as the return artifact. The val metric comes from the held-out split — see
`evaluation` for the metric and `datasets` for the split.

## Dataloader
`num_workers` > 0 to overlap data prep with compute (start near CPU-core count), `pin_memory=True` with a
CUDA device to speed host→device copies, `persistent_workers=True` for many short epochs. Keep the
seeded `generator`/`worker_init_fn` from the determinism section.

## Gotcha
A checkpoint without its **config + code version + RNG state** is not reproducible — you can load the
weights but not re-derive how they got there. Save all three (shown above) on every checkpoint, and
**never touch the eval/test split during training** — no early-stopping on it, no tuning against it, no
peeking (the **never leak the eval set** always-on convention; splits are owned by `datasets` and
`data-governance`). Determinism first: seed everything and record the seed.
