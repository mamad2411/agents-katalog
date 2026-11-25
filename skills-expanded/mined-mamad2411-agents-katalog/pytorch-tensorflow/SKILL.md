---
name: "pytorch-tensorflow"
description: "PyTorch and TensorFlow model training, data loaders, GPU setup, checkpointing, inference optimization"
---

# PyTorch / TensorFlow Skill

## When to activate
- Writing neural network training loops in PyTorch
- Building and training Keras/TensorFlow models
- Implementing custom loss functions or model architectures
- Setting up GPU training with device management
- Writing data loaders and preprocessing pipelines for model training
- Implementing model evaluation, checkpointing, and early stopping
- Debugging NaN losses, exploding gradients, or training instability
- Porting models between PyTorch and TensorFlow

## When NOT to use
- scikit-learn tasks (classification, regression, clustering on tabular data) — not deep learning
- Pandas/Polars data manipulation before the modeling step
- Hugging Face fine-tuning with trainer API (different workflow)
- Inference-only deployments without training code

## Instructions

### PyTorch training loop — standard structure
```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

def train(model, train_loader, val_loader, epochs, lr, device):
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-2)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()

    best_val_loss = float('inf')

    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0.0
        for batch in train_loader:
            inputs, targets = batch
            inputs, targets = inputs.to(device), targets.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()

            # Gradient clipping — always for stability
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

            optimizer.step()
            train_loss += loss.item()

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch in val_loader:
                inputs, targets = batch
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                val_loss += criterion(outputs, targets).item()

        scheduler.step()

        # Checkpoint best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), 'best_model.pt')

        print(f"Epoch {epoch+1}/{epochs} | Train: {train_loss/len(train_loader):.4f} | Val: {val_loss/len(val_loader):.4f}")
```

### Device management
```python
# Always explicit device selection
device = torch.device('cuda' if torch.cuda.is_available() else
                       'mps' if torch.backends.mps.is_available() else
                       'cpu')
model = model.to(device)
```
Never hardcode `'cuda'` — always check availability.

### Custom model structure
```python
class MyModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, dropout=0.3):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LayerNorm(hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.network(x)
```
Prefer `nn.Sequential` for simple feedforward; use `forward()` override for complex branching.

### Debugging training instability
1. **NaN loss** → check for log(0) in loss, exploding inputs, or division by zero in preprocessing
2. **Exploding gradients** → add `clip_grad_norm_` (already in template above)
3. **Vanishing gradients** → check activation functions (avoid sigmoid/tanh in deep networks), use residual connections
4. **Loss not decreasing** → reduce LR 10x, check data loader shuffling, verify labels are correct
5. **GPU OOM** → reduce batch size, use gradient checkpointing, use mixed precision

### Mixed precision training (PyTorch)
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for batch in train_loader:
    optimizer.zero_grad()
    with autocast():
        outputs = model(inputs)
        loss = criterion(outputs, targets)
    scaler.scale(loss).backward()
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    scaler.step(optimizer)
    scaler.update()
```

### TensorFlow/Keras — standard structure
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.AdamW(learning_rate=1e-3, weight_decay=1e-2),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks = [
    tf.keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint('best_model.keras', save_best_only=True),
    tf.keras.callbacks.ReduceLROnPlateau(patience=3, factor=0.5)
]

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=100,
    callbacks=callbacks
)
```

## Example

**User:** Build a PyTorch text classifier for sentiment analysis (binary) with embedding, LSTM, and dropout.

**Expected output:**
- `SentimentLSTM(nn.Module)` — embedding layer, LSTM, dropout, linear head
- `forward()` — handles packed sequences or padded input
- Training loop with gradient clipping, validation per epoch, best model checkpoint
- `device` auto-detected (CUDA/MPS/CPU)
- Train/val split via `DataLoader` with shuffling on train only

---
