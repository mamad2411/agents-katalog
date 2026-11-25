---
name: "training-patterns"
description: "Training loop patterns with code: a PyTorch Lightning LightningModule, the Hugging Face Trainer with custom metrics, LR finder and warmup schedules, gradient monitoring and clipping, and checkpoint resume. Use when writing or debugging model training."
---

# Training Patterns

Expert patterns for PyTorch Lightning modules, HuggingFace Trainer, LR scheduling, gradient monitoring, checkpoint resume, and early stopping.

## Pattern 1: PyTorch Lightning LightningModule

Complete LightningModule structure with validation, logging, and optimizer config.

```python
import torch
import torch.nn as nn
import pytorch_lightning as pl
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torchmetrics import AUROC, F1Score

class ChurnClassifier(pl.LightningModule):
    def __init__(self, input_dim: int, hidden_dim: int = 256,
                 lr: float = 1e-3, weight_decay: float = 1e-4,
                 pos_weight: float = 3.0):
        super().__init__()
        self.save_hyperparameters()  # logs all __init__ args to checkpoint

        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.GELU(),
            nn.Linear(hidden_dim // 2, 1),
        )
        self.criterion = nn.BCEWithLogitsLoss(
            pos_weight=torch.tensor([pos_weight])
        )
        self.val_auroc = AUROC(task="binary")
        self.val_f1 = F1Score(task="binary", threshold=0.5)

    def forward(self, x):
        return self.net(x).squeeze(-1)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y.float())
        self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y.float())
        proba = torch.sigmoid(logits)
        self.val_auroc.update(proba, y)
        self.val_f1.update(proba, y)
        self.log("val_loss", loss, prog_bar=True)

    def on_validation_epoch_end(self):
        self.log("val_auroc", self.val_auroc.compute(), prog_bar=True)
        self.log("val_f1", self.val_f1.compute())
        self.val_auroc.reset()
        self.val_f1.reset()

    def configure_optimizers(self):
        optimizer = AdamW(self.parameters(),
                          lr=self.hparams.lr,
                          weight_decay=self.hparams.weight_decay)
        scheduler = CosineAnnealingLR(optimizer, T_max=self.trainer.max_epochs)
        return {
            "optimizer": optimizer,
            "lr_scheduler": {"scheduler": scheduler, "interval": "epoch"},
        }

# Trainer with callbacks
from pytorch_lightning.callbacks import (
    ModelCheckpoint, EarlyStopping, LearningRateMonitor
)

trainer = pl.Trainer(
    max_epochs=100,
    gradient_clip_val=1.0,
    precision="bf16-mixed",
    callbacks=[
        ModelCheckpoint(monitor="val_auroc", mode="max", save_top_k=3,
                        save_last=True, dirpath="checkpoints/",
                        filename="churn-{epoch:02d}-{val_auroc:.4f}"),
        EarlyStopping(monitor="val_auroc", mode="max", patience=10,
                      min_delta=1e-4),
        LearningRateMonitor(logging_interval="step"),
    ],
    logger=pl.loggers.WandbLogger(project="churn-model"),
)
trainer.fit(model, datamodule=dm)
```

## Pattern 2: HuggingFace Trainer with Custom Metrics

Production Trainer setup with warmup schedule and early stopping.

```python
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    EarlyStoppingCallback,
    DataCollatorWithPadding,
)
from sklearn.metrics import roc_auc_score, f1_score
import numpy as np

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
data_collator = DataCollatorWithPadding(tokenizer, pad_to_multiple_of=8)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    proba = torch.softmax(torch.tensor(logits), dim=-1)[:, 1].numpy()
    preds = (proba > 0.5).astype(int)
    return {
        "roc_auc": roc_auc_score(labels, proba),
        "f1": f1_score(labels, preds),
    }

args = TrainingArguments(
    output_dir="outputs/bert-classifier",
    num_train_epochs=10,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=64,
    gradient_accumulation_steps=2,          # effective batch = 64
    learning_rate=2e-5,
    warmup_ratio=0.06,                       # 6% of steps for warmup
    lr_scheduler_type="cosine",
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="roc_auc",
    greater_is_better=True,
    bf16=True,
    dataloader_num_workers=4,
    report_to=["wandb"],
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    data_collator=data_collator,
    compute_metrics=compute_metrics,
    callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
)

# Resume from checkpoint if exists
trainer.train(resume_from_checkpoint=last_checkpoint)
```

## Pattern 3: LR Finder and Warmup Schedule

Find optimal learning rate before committing to a full training run.

```python
import pytorch_lightning as pl
from pytorch_lightning.tuner import Tuner

# LR finder
trainer = pl.Trainer(max_epochs=1)
model = ChurnClassifier(input_dim=50)
tuner = Tuner(trainer)

lr_finder = tuner.lr_find(model, datamodule=dm,
                           min_lr=1e-6, max_lr=1e-1,
                           num_training=200)

suggested_lr = lr_finder.suggestion()
print(f"Suggested LR: {suggested_lr:.2e}")

# Plot loss vs LR
fig = lr_finder.plot(suggest=True)
fig.savefig("lr_finder.png")

# Apply suggested LR
model.hparams.lr = suggested_lr

# Manual cosine warmup schedule (HuggingFace)
from transformers import get_cosine_schedule_with_warmup

total_steps = len(train_dataloader) * num_epochs
warmup_steps = int(0.06 * total_steps)

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=warmup_steps,
    num_training_steps=total_steps,
)
```

## Pattern 4: Gradient Monitoring and Clipping

Track gradient norms per step to catch instability early.

```python
import torch
import wandb

def compute_grad_norm(model: torch.nn.Module, norm_type: float = 2.0) -> float:
    """Compute total gradient norm across all parameters."""
    total_norm = 0.0
    for p in model.parameters():
        if p.grad is not None:
            param_norm = p.grad.data.norm(norm_type)
            total_norm += param_norm.item() ** norm_type
    return total_norm ** (1.0 / norm_type)

# In training loop
for step, batch in enumerate(train_loader):
    optimizer.zero_grad()
    loss = model(batch)
    loss.backward()

    # Compute norm BEFORE clipping (for monitoring)
    grad_norm_before = compute_grad_norm(model)

    # Clip gradients
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

    grad_norm_after = compute_grad_norm(model)

    optimizer.step()
    scheduler.step()

    if step % 50 == 0:
        wandb.log({
            "train/loss": loss.item(),
            "train/grad_norm_before_clip": grad_norm_before,
            "train/grad_norm_after_clip": grad_norm_after,
            "train/lr": scheduler.get_last_lr()[0],
            "step": step,
        })

    # Sanity check: abort if NaN
    if torch.isnan(loss):
        raise RuntimeError(f"NaN loss at step {step}. Aborting.")
```

## Pattern 5: Checkpoint Resume

Reliable checkpoint save and resume from interruption.

```python
import os
import torch

def save_checkpoint(model, optimizer, scheduler, epoch, best_metric,
                    path: str):
    """Atomic checkpoint write: temp file → rename."""
    tmp_path = path + ".tmp"
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
        "best_metric": best_metric,
    }, tmp_path)
    os.rename(tmp_path, path)  # atomic on POSIX systems
    print(f"Checkpoint saved: {path} (epoch={epoch}, metric={best_metric:.4f})")

def load_checkpoint(path: str, model, optimizer, scheduler):
    """Load checkpoint and return epoch + best metric."""
    checkpoint = torch.load(path, map_location="cpu")
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
    return checkpoint["epoch"], checkpoint["best_metric"]

# Usage
checkpoint_path = "checkpoints/model_best.pt"
start_epoch = 0
best_metric = 0.0

if os.path.exists(checkpoint_path):
    start_epoch, best_metric = load_checkpoint(
        checkpoint_path, model, optimizer, scheduler
    )
    print(f"Resuming from epoch {start_epoch}, best AUC={best_metric:.4f}")

for epoch in range(start_epoch, max_epochs):
    train_one_epoch(model, train_loader, optimizer, scheduler)
    val_metric = evaluate(model, val_loader)

    if val_metric > best_metric:
        best_metric = val_metric
        save_checkpoint(model, optimizer, scheduler, epoch,
                        best_metric, checkpoint_path)
```

## Anti-Patterns

### Anti-Pattern 1: No Single-Batch Overfit Test
Before starting a long training run, verify the model can overfit a single batch (loss → 0). If it cannot, there is a bug in the loss function, model architecture, or data pipeline. This test takes 30 seconds and prevents wasting GPU-hours.

### Anti-Pattern 2: Saving Checkpoints Without Optimizer State
A checkpoint without optimizer state cannot be resumed — the learning rate schedule and adaptive momentum (Adam m1/m2) are lost. Always save optimizer and scheduler state alongside model weights.

### Anti-Pattern 3: Monitoring Only Training Loss
Training loss decreasing while validation loss increases = overfitting. Training loss plateauing = LR too low or gradient vanishing. Always monitor both curves and gradient norms — the combination tells the real story.

### Anti-Pattern 4: Fixed LR Without Schedule
Transformers trained with constant LR are 5-10% worse than with cosine warmup schedule. The warmup phase prevents early gradient explosions; the decay phase allows fine-grained convergence. Always use a schedule.
