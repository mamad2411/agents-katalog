---
name: pytorch-lightning
description: Clean training loops with built-in distributed support.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [lightning, torch, transformers]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [PyTorch Lightning, Training Framework, Distributed Training, DDP, FSDP, DeepSpeed, High-Level API, Callbacks, Best Practices, Scalable]

---

# PyTorch Lightning——高级训练框架

## 快速入门

PyTorch Lightning 对 PyTorch 代码进行了结构化整理，在保留高度灵活性的同时减少了冗余代码。

**安装方式**：
```bash
pip install lightning
```

**将 PyTorch 转换为 Lightning**（3个步骤）：

```python
import lightning as L
import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset

# Step 1: Define LightningModule (organize your PyTorch code)
class LitModel(L.LightningModule):
    def __init__(self, hidden_size=128):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(28 * 28, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 10)
        )

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = nn.functional.cross_entropy(y_hat, y)
        self.log('train_loss', loss)  # Auto-logged to TensorBoard
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)

# Step 2: Create data
train_loader = DataLoader(train_dataset, batch_size=32)

# Step 3: Train with Trainer (handles everything else!)
trainer = L.Trainer(max_epochs=10, accelerator='gpu', devices=2)
model = LitModel()
trainer.fit(model, train_loader)
```

**就是这样！** Trainer可处理以下功能：
- GPU/TPU/CPU切换
- 分布式训练（DDP、FSDP、DeepSpeed）
- 混合精度训练（FP16、BF16）
- 梯度累积
- 检查点保存
- 日志记录
- 进度条显示

## 常见工作流程

### 工作流程1：从PyTorch转换为Lightning

**原始PyTorch代码**：
```python
model = MyModel()
optimizer = torch.optim.Adam(model.parameters())
model.to('cuda')

for epoch in range(max_epochs):
    for batch in train_loader:
        batch = batch.to('cuda')
        optimizer.zero_grad()
        loss = model(batch)
        loss.backward()
        optimizer.step()
```

**闪电版**：
```python
class LitModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = MyModel()

    def training_step(self, batch, batch_idx):
        loss = self.model(batch)  # No .to('cuda') needed!
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters())

# Train
trainer = L.Trainer(max_epochs=10, accelerator='gpu')
trainer.fit(LitModel(), train_loader)
```

**优势**：代码行数从40多行缩减至15行，无需进行设备管理，可实现自动分布式处理。 

### 工作流程2：验证与测试

```python
class LitModel(L.LightningModule):
    def __init__(self):
        super().__init__()
        self.model = MyModel()

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        loss = nn.functional.cross_entropy(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        val_loss = nn.functional.cross_entropy(y_hat, y)
        acc = (y_hat.argmax(dim=1) == y).float().mean()
        self.log('val_loss', val_loss)
        self.log('val_acc', acc)

    def test_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self.model(x)
        test_loss = nn.functional.cross_entropy(y_hat, y)
        self.log('test_loss', test_loss)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)

# Train with validation
trainer = L.Trainer(max_epochs=10)
trainer.fit(model, train_loader, val_loader)

# Test
trainer.test(model, test_loader)
```

**自动功能**：
- 默认情况下，每个训练周期都会执行验证
- 将指标记录到 TensorBoard 中
- 根据验证损失自动保存最佳模型检查点

```python
# Same code as single GPU!
model = LitModel()

# 8 GPUs with DDP (automatic!)
trainer = L.Trainer(
    accelerator='gpu',
    devices=8,
    strategy='ddp'  # Or 'fsdp', 'deepspeed'
)

trainer.fit(model, train_loader)
```

**启动**：
```bash
# Single command, Lightning handles the rest
python train.py
```

**无需任何修改**：
- 自动数据分发
- 梯度同步
- 多节点支持（只需设置 `num_nodes=2` 即可）

### 工作流 4：用于监控的回调功能

```python
from lightning.pytorch.callbacks import ModelCheckpoint, EarlyStopping, LearningRateMonitor

# Create callbacks
checkpoint = ModelCheckpoint(
    monitor='val_loss',
    mode='min',
    save_top_k=3,
    filename='model-{epoch:02d}-{val_loss:.2f}'
)

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    mode='min'
)

lr_monitor = LearningRateMonitor(logging_interval='epoch')

# Add to Trainer
trainer = L.Trainer(
    max_epochs=100,
    callbacks=[checkpoint, early_stop, lr_monitor]
)

trainer.fit(model, train_loader, val_loader)
```

**结果**：
- 自动保存表现最佳的3个模型
- 若5个训练周期内无改进则提前终止
- 将学习率信息记录到TensorBoard中

### 工作流程5：学习率调度

```python
class LitModel(L.LightningModule):
    # ... (training_step, etc.)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)

        # Cosine annealing
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=100,
            eta_min=1e-5
        )

        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'interval': 'epoch',  # Update per epoch
                'frequency': 1
            }
        }

# Learning rate auto-logged!
trainer = L.Trainer(max_epochs=100)
trainer.fit(model, train_loader)
```

## 何时使用 PyTorch Lightning 及其替代方案

**适合使用 PyTorch Lightning 的情况包括**：
- 希望代码结构清晰、井然有序
- 需要可用于生产环境的训练循环
- 在单 GPU、多 GPU 或 TPU 环境间切换
- 需要内置的回调函数和日志记录功能
- 团队协作（标准化的代码结构）

**主要优势**：
- **结构清晰**：将研究代码与工程实现分离
- **操作便捷**：仅需一行代码即可启用 DDP、FSDP 和 DeepSpeed
- **回调功能**：支持模块化的训练扩展
- **可复现性强**：减少样板代码，从而降低错误概率
- **经过验证**：每月下载量超 100 万次，实战检验可靠

**适合选择替代方案的情况**：
- **Accelerate**：对现有代码改动最小，灵活性更高
- **Ray Train**：支持多节点调度及超参数调优
- **原生 PyTorch**：提供最大程度的控制权，适用于学习研究
- **Keras**：属于 TensorFlow 生态系统

## 常见问题

**问题：损失值不下降**

请检查数据与模型设置：
```python
# Add to training_step
def training_step(self, batch, batch_idx):
    if batch_idx == 0:
        print(f"Batch shape: {batch[0].shape}")
        print(f"Labels: {batch[1]}")
    loss = ...
    return loss
```

**问题：内存不足**

请减小批量大小或采用梯度累积技术：
```python
trainer = L.Trainer(
    accumulate_grad_batches=4,  # Effective batch = batch_size × 4
    precision='bf16'  # Or 'fp16', reduces memory 50%
)
```

**问题：未运行验证流程**

请确保传入了 val_loader 参数：
```python
# WRONG
trainer.fit(model, train_loader)

# CORRECT
trainer.fit(model, train_loader, val_loader)
```

**问题：DDP意外启动了多个进程**

Lightning会自动检测GPU。如需手动指定设备，请进行如下设置：
```python
# Test on CPU first
trainer = L.Trainer(accelerator='cpu', devices=1)

# Then GPU
trainer = L.Trainer(accelerator='gpu', devices=1)
```

## 高级主题

**回调机制**：有关 EarlyStopping、ModelCheckpoint、自定义回调函数以及回调钩子的详细信息，请参阅 [references/callbacks.md](references/callbacks.md)。

**分布式训练策略**：关于 DDP、FSDP、DeepSpeed ZeRO 集成以及多节点部署的说明，请查看 [references/distributed.md](references/distributed.md)。

**超参数调优**：若需了解如何与 Optuna、Ray Tune 以及 WandB 的调参功能进行集成，可参考 [references/hyperparameter-tuning.md](references/hyperparameter-tuning.md)。

## 硬件要求

- **CPU**：可用（适合调试）
- **单块 GPU**：可用
- **多块 GPU**：支持 DDP（默认）、FSDP 或 DeepSpeed
- **多节点环境**：支持 DDP、FSDP、DeepSpeed
- **TPU**：支持（需 8 核）
- **Apple MPS**：支持

**精度选项**：
- FP32（默认）
- FP16（适用于 V100 及更早型号的 GPU）
- BF16（推荐用于 A100/H100）
- FP8（仅适用于 H100）

## 相关资源

- 文档：https://lightning.ai/docs/pytorch/stable/
- GitHub 仓库：https://github.com/Lightning-AI/pytorch-lightning ⭐ 29,000+ 次点赞
- 当前版本：2.5.5 及以上
- 示例代码：https://github.com/Lightning-AI/pytorch-lightning/tree/master/examples
- Discord 社群：https://discord.gg/lightning-ai
- 应用案例：Kaggle 冠军团队、研究实验室及生产环境团队均在使用该框架


