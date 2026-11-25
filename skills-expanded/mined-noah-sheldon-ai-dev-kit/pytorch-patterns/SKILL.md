---
name: pytorch-patterns
description: PyTorch patterns — nn.Module model definition, training loops, DataLoader optimization, GPU utilization, distributed training with DDP, torch.compile, mixed precision, gradient accumulation, checkpointing, learning rate scheduling, CUDA toolchain.
origin: AI Dev Kit
---

# PyTorch Patterns

Production-grade PyTorch patterns for model definition, training, optimization,
distributed execution, and deployment compatibility.

## When to Use

- Defining neural network architectures with `nn.Module`.
- Writing or refactoring training loops for correctness and efficiency.
- Optimizing DataLoaders for I/O-bound training pipelines.
- Enabling GPU utilization with mixed precision and gradient accumulation.
- Scaling training across multiple GPUs with DDP (Distributed Data Parallel).
- Using `torch.compile` for accelerated execution.
- Implementing checkpointing, LR scheduling, and training reproducibility.

## Core Concepts

### 1. Model Definition with nn.Module

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional


class ResidualBlock(nn.Module):
    """Residual block with batch norm and optional dropout."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.dropout = nn.Dropout2d(dropout) if dropout > 0 else nn.Identity()

        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.dropout(out)
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)
        return F.relu(out)


class MyModel(nn.Module):
    """Example model with proper initialization and forward pass."""

    def __init__(self, num_classes: int = 10, dropout: float = 0.3) -> None:
        super().__init__()
        self.num_classes = num_classes

        # Feature extractor
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            ResidualBlock(64, 128, stride=1, dropout=dropout),
            ResidualBlock(128, 256, stride=2, dropout=dropout),
            nn.AdaptiveAvgPool2d(1),
        )

        # Classifier
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(256, num_classes),
        )

        self._init_weights()

    def _init_weights(self) -> None:
        """Kaiming initialization for conv layers, Xavier for linear."""
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        return self.classifier(x)
```

### 2. Training Loops

```python
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm


class Trainer:
    """Reusable training loop with logging and checkpointing."""

    def __init__(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        optimizer: torch.optim.Optimizer,
        scheduler: Optional[torch.optim.lr_scheduler._LRScheduler] = None,
        device: torch.device = None,
        use_amp: bool = True,
        gradient_accumulation_steps: int = 1,
    ) -> None:
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.use_amp = use_amp
        self.gradient_accumulation_steps = gradient_accumulation_steps
        self.scaler = torch.amp.GradScaler("cuda", enabled=use_amp)
        self.epoch = 0
        self.best_val_loss = float("inf")

    def train_epoch(self) -> dict:
        self.model.train()
        total_loss = 0.0
        correct = 0
        total = 0

        for batch_idx, (inputs, targets) in enumerate(tqdm(self.train_loader, desc=f"Epoch {self.epoch}")):
            inputs, targets = inputs.to(self.device), targets.to(self.device)

            with torch.amp.autocast("cuda", enabled=self.use_amp):
                outputs = self.model(inputs)
                loss = F.cross_entropy(outputs, targets)
                loss = loss / self.gradient_accumulation_steps

            self.scaler.scale(loss).backward()

            if (batch_idx + 1) % self.gradient_accumulation_steps == 0:
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()

            total_loss += loss.item() * self.gradient_accumulation_steps
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        return {
            "loss": total_loss / len(self.train_loader),
            "accuracy": 100.0 * correct / total,
        }

    @torch.no_grad()
    def validate(self) -> dict:
        self.model.eval()
        total_loss = 0.0
        correct = 0
        total = 0

        for inputs, targets in self.val_loader:
            inputs, targets = inputs.to(self.device), targets.to(self.device)
            outputs = self.model(inputs)
            loss = F.cross_entropy(outputs, targets)

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        return {
            "val_loss": total_loss / len(self.val_loader),
            "val_accuracy": 100.0 * correct / total,
        }

    def fit(self, num_epochs: int, checkpoint_path: str = "best_model.pt") -> list[dict]:
        history = []
        for epoch in range(num_epochs):
            self.epoch = epoch + 1
            train_metrics = self.train_epoch()
            val_metrics = self.validate()

            if self.scheduler is not None:
                self.scheduler.step()

            metrics = {**train_metrics, **val_metrics, "epoch": self.epoch}
            history.append(metrics)

            # Checkpoint best model
            if val_metrics["val_loss"] < self.best_val_loss:
                self.best_val_loss = val_metrics["val_loss"]
                self.save_checkpoint(checkpoint_path)

            print(f"Epoch {self.epoch}: {metrics}")

        return history

    def save_checkpoint(self, path: str) -> None:
        torch.save({
            "epoch": self.epoch,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "best_val_loss": self.best_val_loss,
            "scaler_state_dict": self.scaler.state_dict(),
        }, path)

    def load_checkpoint(self, path: str) -> None:
        checkpoint = torch.load(path, weights_only=False)
        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.scaler.load_state_dict(checkpoint["scaler_state_dict"])
        self.epoch = checkpoint["epoch"]
        self.best_val_loss = checkpoint["best_val_loss"]
```

### 3. DataLoader Optimization

```python
from torch.utils.data import DataLoader, Dataset


def create_optimized_dataloader(
    dataset: Dataset,
    batch_size: int = 32,
    num_workers: int = 4,
    pin_memory: bool = True,
    persistent_workers: bool = True,
    prefetch_factor: int = 2,
) -> DataLoader:
    """Create a DataLoader optimized for GPU training."""
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,       # Faster CPU → GPU transfer
        persistent_workers=persistent_workers,  # Don't restart workers each epoch
        prefetch_factor=prefetch_factor,        # Pre-load N batches per worker
        drop_last=True,             # Consistent batch sizes
    )
```

**Custom Dataset with efficient __getitem__:**

```python
from pathlib import Path
from PIL import Image


class ImageDataset(Dataset):
    def __init__(self, image_dir: str | Path, transform=None):
        self.image_dir = Path(image_dir)
        self.image_paths = list(self.image_dir.glob("*.jpg"))
        self.transform = transform

    def __len__(self) -> int:
        return len(self.image_paths)

    def __getitem__(self, idx: int):
        img = Image.open(self.image_paths[idx]).convert("RGB")
        label = self._parse_label(self.image_paths[idx])

        if self.transform:
            img = self.transform(img)

        return img, label
```

### 4. GPU Utilization

```python
def setup_device() -> torch.device:
    """Select the best available device."""
    if torch.cuda.is_available():
        device = torch.device("cuda")
        # Print GPU info
        print(f"GPU: {torch.cuda.get_device_name(0)}")
        print(f"Memory: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f} GB")
        return device
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def check_gpu_memory():
    """Monitor GPU memory usage."""
    allocated = torch.cuda.memory_allocated() / 1e9
    reserved = torch.cuda.memory_reserved() / 1e9
    print(f"GPU Memory — Allocated: {allocated:.2f} GB, Reserved: {reserved:.2f} GB")
```

### 5. Distributed Training with DDP

```python
import os
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data.distributed import DistributedSampler


def setup_ddp(rank: int, world_size: int) -> None:
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "12355"
    dist.init_process_group("nccl", rank=rank, world_size=world_size)
    torch.cuda.set_device(rank)


def cleanup_ddp() -> None:
    dist.destroy_process_group()


def train_ddp(rank: int, world_size: int) -> None:
    setup_ddp(rank, world_size)

    model = MyModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    # DistributedSampler ensures each GPU sees a different shard
    sampler = DistributedSampler(dataset, num_replicas=world_size, rank=rank)
    loader = DataLoader(dataset, batch_size=32, sampler=sampler)

    # Training loop same as before, but with ddp_model
    for epoch in range(num_epochs):
        sampler.set_epoch(epoch)  # Shuffle differently each epoch
        for batch in loader:
            ...

    cleanup_ddp()


# Launch: torchrun --nproc_per_node=4 train_ddp.py
```

### 6. torch.compile

```python
# PyTorch 2.0+ compilation for faster execution
model = MyModel().to(device)

# Compile the model (first call has overhead, subsequent calls are fast)
model = torch.compile(model, mode="reduce-overhead")  # or "max-autotune"

# For training with AMP:
with torch.amp.autocast("cuda"):
    output = model(inputs)
```

### 7. Mixed Precision Training

```python
# Already shown in Trainer class with GradScaler + autocast
# Key points:
# 1. Use torch.amp.autocast("cuda") for forward pass
# 2. Use GradScaler for backward pass
# 3. Check for NaNs if loss diverges
# 4. Some ops (e.g., large matrix multiplications) may need fp32

# Model sections that should stay in fp32:
# - Final classification layer (small, negligible speed impact)
# - Loss computation (always fp32)
```

### 8. Gradient Accumulation

```python
# Simulate larger batch sizes when GPU memory is limited
# Effective batch size = batch_size * gradient_accumulation_steps

# In training loop:
for i, (inputs, targets) in enumerate(loader):
    with torch.amp.autocast("cuda"):
        outputs = model(inputs)
        loss = criterion(outputs, targets) / accumulation_steps

    scaler.scale(loss).backward()

    if (i + 1) % accumulation_steps == 0:
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

### 9. Model Checkpointing

```python
# Save full training state
def save_full_checkpoint(model, optimizer, scheduler, scaler, epoch, path):
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict() if scheduler else None,
        "scaler_state_dict": scaler.state_dict(),
    }, path)


# Save only model weights (for inference)
def save_model_weights(model, path):
    torch.save(model.state_dict(), path)


# Load for inference
def load_model_for_inference(model, weights_path, device):
    model.load_state_dict(torch.load(weights_path, weights_only=True))
    model.to(device)
    model.eval()
    return model
```

### 10. Learning Rate Scheduling

```python
from torch.optim.lr_scheduler import (
    CosineAnnealingLR,
    OneCycleLR,
    ReduceLROnPlateau,
    LinearLR,
    SequentialLR,
)

# Cosine annealing
scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs, eta_min=1e-6)

# One Cycle (good for fast training)
scheduler = OneCycleLR(
    optimizer,
    max_lr=1e-3,
    steps_per_epoch=len(train_loader),
    epochs=num_epochs,
)

# Warmup + Cosine
warmup = LinearLR(optimizer, start_factor=0.1, total_iters=5)
cosine = CosineAnnealingLR(optimizer, T_max=num_epochs - 5)
scheduler = SequentialLR(optimizer, schedulers=[warmup, cosine], milestones=[5])

# Reduce on plateau
scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=3)
# Call scheduler.step(val_loss) after each epoch
```

### 11. CUDA Toolchain Compatibility

```python
# Check CUDA availability and version
print(f"PyTorch CUDA: {torch.version.cuda}")
print(f"System CUDA: {torch.cuda.get_arch_list()}")

# Ensure compatibility
# PyTorch 2.x requires CUDA 11.8+ for full feature support
# torch.compile requires Triton (auto-installed with PyTorch 2.x)

# Set deterministic behavior for reproducibility
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False  # Set True for faster but non-deterministic

# Random seeds
def seed_everything(seed: int = 42) -> None:
    import random
    import numpy as np
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
```

## Anti-Patterns

- **No `.train()` / `.eval()` switching** — dropout and batch norm behave incorrectly
- **Calling `.backward()` without `optimizer.zero_grad()`** — gradients accumulate across batches
- **DataLoader on main thread** — `num_workers=0` bottlenecks GPU with CPU data loading
- **Not pinning memory** — missing `pin_memory=True` slows CPU → GPU transfers
- **Saving entire model with `torch.save(model)`** — use `state_dict()` for portability
- **Mixed precision without GradScaler** — causes gradient underflow for small values
- **Hardcoding device** — always use `device = torch.device("cuda" if ... else "cpu")`
- **No LR scheduling** — fixed learning rate is slower and converges to worse optima
- **Not setting seed for reproducibility** — results vary across runs

## Best Practices

1. **Always use `nn.Module` with type-hinted forward passes** — clear interfaces.
2. **Separate model definition from training logic** — use a Trainer class.
3. **Use `DataLoader` with `num_workers >= 2`, `pin_memory=True`, `persistent_workers=True`**.
4. **Enable mixed precision** with `autocast` + `GradScaler` for 2-3x speedup on modern GPUs.
5. **Use gradient accumulation** to simulate large batch sizes on limited GPU memory.
6. **Checkpoint everything** — model, optimizer, scaler, scheduler, and epoch.
7. **Use `torch.compile`** for production training where the compilation overhead is amortized.
8. **DDP for multi-GPU** — not DataParallel (which is deprecated and slower).
9. **Seed everything** for reproducibility — Python, NumPy, PyTorch, and CUDA.
10. **Monitor GPU memory** with `torch.cuda.memory_allocated()` to detect leaks.

## Related Skills

- `mlops-workflow` — Experiment tracking, model versioning, and deployment
- `data-pipelines` — ETL patterns for preparing training data
- `python-patterns` — General Python OOP patterns applicable to model design
- `docker-patterns` — Containerizing PyTorch training and inference services
