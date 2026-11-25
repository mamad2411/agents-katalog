---
name: "pytorch-patterns"
description: "PyTorch patterns with code: custom Datasets with transforms, nn.Module initialization, model surgery for fine-tuning, custom autograd functions, and DataLoader throughput profiling. Use when writing or reviewing PyTorch code."
---

# PyTorch Patterns

Expert patterns for custom Dataset/DataLoader, nn.Module design, model surgery, custom autograd, and profiling.

## Pattern 1: Custom Dataset with Transforms

Production Dataset with augmentation pipeline and weighted sampling.

```python
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2

class ImageClassificationDataset(Dataset):
    def __init__(self, df: pd.DataFrame, img_dir: str,
                 transform=None, mode: str = "train"):
        self.df = df.reset_index(drop=True)
        self.img_dir = Path(img_dir)
        self.transform = transform
        self.mode = mode
        self.label_to_idx = {lbl: i for i, lbl in enumerate(sorted(df["label"].unique()))}

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int):
        row = self.df.iloc[idx]
        image = np.array(Image.open(self.img_dir / row["filename"]).convert("RGB"))
        label = self.label_to_idx[row["label"]]

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented["image"]

        return image, torch.tensor(label, dtype=torch.long)

# Transforms
train_transform = A.Compose([
    A.RandomResizedCrop(224, 224),
    A.HorizontalFlip(p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])
val_transform = A.Compose([
    A.Resize(256, 256),
    A.CenterCrop(224, 224),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])

# Weighted sampler for class imbalance
def make_weighted_sampler(dataset: Dataset) -> WeightedRandomSampler:
    labels = [dataset[i][1].item() for i in range(len(dataset))]
    class_counts = np.bincount(labels)
    class_weights = 1.0 / class_counts
    sample_weights = torch.tensor([class_weights[l] for l in labels], dtype=torch.float)
    return WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)

train_ds = ImageClassificationDataset(train_df, "data/images/", train_transform, mode="train")
sampler = make_weighted_sampler(train_ds)

train_loader = DataLoader(
    train_ds,
    batch_size=64,
    sampler=sampler,             # use sampler OR shuffle, not both
    num_workers=8,
    pin_memory=True,
    persistent_workers=True,
    prefetch_factor=2,
)
```

## Pattern 2: nn.Module with Proper Initialization

Custom module with parameter registration, buffer registration, and weight init.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class AttentionClassifier(nn.Module):
    def __init__(self, input_dim: int, num_heads: int = 8,
                 num_classes: int = 2, dropout: float = 0.1):
        super().__init__()

        # Learnable parameters (included in optimizer)
        self.projection = nn.Linear(input_dim, input_dim)
        self.attention = nn.MultiheadAttention(input_dim, num_heads,
                                               dropout=dropout, batch_first=True)
        self.norm = nn.LayerNorm(input_dim)
        self.classifier = nn.Linear(input_dim, num_classes)
        self.dropout = nn.Dropout(dropout)

        # Non-trainable buffer (saved in state_dict but not optimized)
        self.register_buffer("class_weights", torch.ones(num_classes))

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        nn.init.xavier_uniform_(self.projection.weight)
        nn.init.zeros_(self.projection.bias)
        nn.init.xavier_uniform_(self.classifier.weight)
        nn.init.zeros_(self.classifier.bias)

    def forward(self, x: torch.Tensor,
                mask: torch.Tensor = None) -> torch.Tensor:
        # x: (batch, seq_len, input_dim)
        x = self.projection(x)
        attn_out, _ = self.attention(x, x, x, key_padding_mask=mask)
        x = self.norm(x + attn_out)
        x = x.mean(dim=1)  # mean pooling
        x = self.dropout(x)
        return self.classifier(x)

    def extra_repr(self) -> str:
        return f"input_dim={self.projection.in_features}, num_classes={self.classifier.out_features}"
```

## Pattern 3: Model Surgery for Fine-Tuning

Freeze pretrained backbone, replace head, progressive unfreezing.

```python
import torchvision.models as models
import torch.nn as nn

def build_finetuned_resnet(num_classes: int,
                            freeze_backbone: bool = True) -> nn.Module:
    """Replace ResNet50 classifier head for fine-tuning."""
    model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)

    # Freeze all parameters
    if freeze_backbone:
        for param in model.parameters():
            param.requires_grad = False

    # Replace final fully connected layer (unfrozen by default)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.Linear(512, num_classes),
    )
    return model

def progressive_unfreeze(model: nn.Module, epoch: int,
                          unfreeze_schedule: dict):
    """Progressively unfreeze layers by epoch."""
    # Example schedule: {5: "layer4", 10: "layer3", 15: "layer2"}
    for unfreeze_epoch, layer_name in unfreeze_schedule.items():
        if epoch >= unfreeze_epoch:
            for name, param in model.named_parameters():
                if layer_name in name:
                    param.requires_grad = True

    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Epoch {epoch}: {trainable:,}/{total:,} params trainable ({trainable/total:.1%})")

# Usage
model = build_finetuned_resnet(num_classes=10, freeze_backbone=True)

# Optimizer: only trainable params
optimizer = torch.optim.AdamW(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-3
)
```

## Pattern 4: Custom Autograd Function

Custom backward pass for numerical stability or performance.

```python
import torch

class StableSoftmax(torch.autograd.Function):
    """Softmax with numerically stable backward for custom loss."""

    @staticmethod
    def forward(ctx, logits: torch.Tensor) -> torch.Tensor:
        # Numerically stable softmax
        shifted = logits - logits.max(dim=-1, keepdim=True).values
        exp_z = torch.exp(shifted)
        proba = exp_z / exp_z.sum(dim=-1, keepdim=True)
        ctx.save_for_backward(proba)
        return proba

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> torch.Tensor:
        (proba,) = ctx.saved_tensors
        # Jacobian-vector product for softmax
        sum_term = (grad_output * proba).sum(dim=-1, keepdim=True)
        grad_input = proba * (grad_output - sum_term)
        return grad_input

# Register as module
class StableSoftmaxLayer(torch.nn.Module):
    def forward(self, x):
        return StableSoftmax.apply(x)

# Verify gradient correctness
x = torch.randn(4, 10, requires_grad=True)
torch.autograd.gradcheck(StableSoftmax.apply, (x,), eps=1e-4, atol=1e-3)
```

## Pattern 5: DataLoader Throughput Profiling

Benchmark DataLoader to verify it is not the training bottleneck.

```python
import time
import torch
from torch.utils.data import DataLoader

def benchmark_dataloader(loader: DataLoader, n_batches: int = 50) -> dict:
    """Measure DataLoader throughput to identify data pipeline bottlenecks."""
    times = []
    total_samples = 0

    iterator = iter(loader)
    # Warmup
    for _ in range(5):
        next(iterator)

    for _ in range(n_batches):
        start = time.perf_counter()
        batch = next(iterator)
        if isinstance(batch, (list, tuple)):
            _ = batch[0].shape  # force materialization
        times.append(time.perf_counter() - start)
        total_samples += loader.batch_size

    return {
        "mean_batch_time_ms": round(1000 * sum(times) / len(times), 2),
        "throughput_samples_per_sec": round(total_samples / sum(times), 1),
        "p95_batch_time_ms": round(1000 * sorted(times)[int(0.95 * len(times))], 2),
    }

stats = benchmark_dataloader(train_loader, n_batches=100)
print(f"DataLoader throughput: {stats['throughput_samples_per_sec']:.0f} samples/s")
print(f"Mean batch time: {stats['mean_batch_time_ms']:.1f}ms")
# If this is slower than your GPU forward+backward time, increase num_workers
```

## Anti-Patterns

### Anti-Pattern 1: Calling .item() in Training Loop
`loss.item()` synchronizes CPU and GPU — it forces the GPU to finish the current operation before Python continues. Inside a training loop, this adds a sync point every step, destroying async execution. Log with `.item()` only at the end of each epoch, not every batch.

### Anti-Pattern 2: num_workers=0 for Disk I/O Datasets
Single-process data loading serializes disk reads with GPU computation. Image datasets with num_workers=0 typically achieve < 20% GPU utilization. Use `num_workers = min(8, os.cpu_count())` and measure GPU utilization with `nvidia-smi dmon`.

### Anti-Pattern 3: Creating Tensors Inside forward()
`torch.zeros(batch_size, hidden_dim)` inside `forward()` allocates on CPU and triggers H→D transfer every forward pass. Pre-allocate buffers as registered buffers or create on the correct device: `torch.zeros(..., device=x.device)`.

### Anti-Pattern 4: model.train() / model.eval() Inconsistency
`BatchNorm` and `Dropout` behave differently in train vs eval mode. Forgetting `model.eval()` before validation makes BatchNorm stats continue updating on validation data — contaminating the running statistics. Always toggle explicitly at epoch boundaries.
