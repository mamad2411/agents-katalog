---
name: weights-and-biases
description: "W&B: log ML experiments, sweeps, model registry, dashboards."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [wandb]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [MLOps, Weights And Biases, WandB, Experiment Tracking, Hyperparameter Tuning, Model Registry, Collaboration, Real-Time Visualization, PyTorch, TensorFlow, HuggingFace]

---

# Weights & Biases：机器学习实验追踪与MLOps工具

## 何时使用该功能

当您需要以下功能时，可使用Weights & Biases（W&B）：
- 通过自动指标记录功能**追踪机器学习实验**
- 在实时仪表板中**可视化训练过程**
- **对比不同超参数及配置下的实验结果**
- 利用自动化扫描功能**优化超参数设置**
- 通过版本控制和流程追溯功能**管理模型注册表**
- 基于团队工作空间实现**机器学习项目的协作开发**
- 通过流程追溯功能**追踪数据集、模型及代码等工件**

**用户规模**：20万+机器学习从业者 | **GitHub星标数**：1.05万+ | **集成数量**：100+种

## 安装指南

```bash
# Install W&B
pip install wandb

# Login (creates API key)
wandb login

# Or set API key programmatically
export WANDB_API_KEY=your_api_key_here
```

## 快速入门

### 基本实验跟踪功能

```python
import wandb

# Initialize a run
run = wandb.init(
    project="my-project",
    config={
        "learning_rate": 0.001,
        "epochs": 10,
        "batch_size": 32,
        "architecture": "ResNet50"
    }
)

# Training loop
for epoch in range(run.config.epochs):
    # Your training code
    train_loss = train_epoch()
    val_loss = validate()

    # Log metrics
    wandb.log({
        "epoch": epoch,
        "train/loss": train_loss,
        "val/loss": val_loss,
        "train/accuracy": train_acc,
        "val/accuracy": val_acc
    })

# Finish the run
wandb.finish()
```

### 集成 PyTorch 技术

```python
import torch
import wandb

# Initialize
wandb.init(project="pytorch-demo", config={
    "lr": 0.001,
    "epochs": 10
})

# Access config
config = wandb.config

# Training loop
for epoch in range(config.epochs):
    for batch_idx, (data, target) in enumerate(train_loader):
        # Forward pass
        output = model(data)
        loss = criterion(output, target)

        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # Log every 100 batches
        if batch_idx % 100 == 0:
            wandb.log({
                "loss": loss.item(),
                "epoch": epoch,
                "batch": batch_idx
            })

# Save model
torch.save(model.state_dict(), "model.pth")
wandb.save("model.pth")  # Upload to W&B

wandb.finish()
```

## 核心概念

### 1. 项目与运行任务

**项目**：相关实验的集合
**运行任务**：训练脚本的单次执行

```python
# Create/use project
run = wandb.init(
    project="image-classification",
    name="resnet50-experiment-1",  # Optional run name
    tags=["baseline", "resnet"],    # Organize with tags
    notes="First baseline run"      # Add notes
)

# Each run has unique ID
print(f"Run ID: {run.id}")
print(f"Run URL: {run.url}")
```

### 2. 配置跟踪

自动追踪超参数：

```python
config = {
    # Model architecture
    "model": "ResNet50",
    "pretrained": True,

    # Training params
    "learning_rate": 0.001,
    "batch_size": 32,
    "epochs": 50,
    "optimizer": "Adam",

    # Data params
    "dataset": "ImageNet",
    "augmentation": "standard"
}

wandb.init(project="my-project", config=config)

# Access config during training
lr = wandb.config.learning_rate
batch_size = wandb.config.batch_size
```

### 3. 指标日志记录

```python
# Log scalars
wandb.log({"loss": 0.5, "accuracy": 0.92})

# Log multiple metrics
wandb.log({
    "train/loss": train_loss,
    "train/accuracy": train_acc,
    "val/loss": val_loss,
    "val/accuracy": val_acc,
    "learning_rate": current_lr,
    "epoch": epoch
})

# Log with custom x-axis
wandb.log({"loss": loss}, step=global_step)

# Log media (images, audio, video)
wandb.log({"examples": [wandb.Image(img) for img in images]})

# Log histograms
wandb.log({"gradients": wandb.Histogram(gradients)})

# Log tables
table = wandb.Table(columns=["id", "prediction", "ground_truth"])
wandb.log({"predictions": table})
```

### 4. 模型检查点功能

```python
import torch
import wandb

# Save model checkpoint
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}

torch.save(checkpoint, 'checkpoint.pth')

# Upload to W&B
wandb.save('checkpoint.pth')

# Or use Artifacts (recommended)
artifact = wandb.Artifact('model', type='model')
artifact.add_file('checkpoint.pth')
wandb.log_artifact(artifact)
```

## 超参数扫描

自动搜索最优的超参数设置。

### 定义扫描配置

```python
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {
        'name': 'val/accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'learning_rate': {
            'distribution': 'log_uniform',
            'min': 1e-5,
            'max': 1e-1
        },
        'batch_size': {
            'values': [16, 32, 64, 128]
        },
        'optimizer': {
            'values': ['adam', 'sgd', 'rmsprop']
        },
        'dropout': {
            'distribution': 'uniform',
            'min': 0.1,
            'max': 0.5
        }
    }
}

# Initialize sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")
```

### 定义训练函数

```python
def train():
    # Initialize run
    run = wandb.init()

    # Access sweep parameters
    lr = wandb.config.learning_rate
    batch_size = wandb.config.batch_size
    optimizer_name = wandb.config.optimizer

    # Build model with sweep config
    model = build_model(wandb.config)
    optimizer = get_optimizer(optimizer_name, lr)

    # Training loop
    for epoch in range(NUM_EPOCHS):
        train_loss = train_epoch(model, optimizer, batch_size)
        val_acc = validate(model)

        # Log metrics
        wandb.log({
            "train/loss": train_loss,
            "val/accuracy": val_acc
        })

# Run sweep
wandb.agent(sweep_id, function=train, count=50)  # Run 50 trials
```

### 扫描策略

```python
# Grid search - exhaustive
sweep_config = {
    'method': 'grid',
    'parameters': {
        'lr': {'values': [0.001, 0.01, 0.1]},
        'batch_size': {'values': [16, 32, 64]}
    }
}

# Random search
sweep_config = {
    'method': 'random',
    'parameters': {
        'lr': {'distribution': 'uniform', 'min': 0.0001, 'max': 0.1},
        'dropout': {'distribution': 'uniform', 'min': 0.1, 'max': 0.5}
    }
}

# Bayesian optimization (recommended)
sweep_config = {
    'method': 'bayes',
    'metric': {'name': 'val/loss', 'goal': 'minimize'},
    'parameters': {
        'lr': {'distribution': 'log_uniform', 'min': 1e-5, 'max': 1e-1}
    }
}
```

## 构件

通过数据血缘追踪数据集、模型及其他文件。

### 日志构件

```python
# Create artifact
artifact = wandb.Artifact(
    name='training-dataset',
    type='dataset',
    description='ImageNet training split',
    metadata={'size': '1.2M images', 'split': 'train'}
)

# Add files
artifact.add_file('data/train.csv')
artifact.add_dir('data/images/')

# Log artifact
wandb.log_artifact(artifact)
```

### 使用 Artifact

```python
# Download and use artifact
run = wandb.init(project="my-project")

# Download artifact
artifact = run.use_artifact('training-dataset:latest')
artifact_dir = artifact.download()

# Use the data
data = load_data(f"{artifact_dir}/train.csv")
```

### 模型注册表

```python
# Log model as artifact
model_artifact = wandb.Artifact(
    name='resnet50-model',
    type='model',
    metadata={'architecture': 'ResNet50', 'accuracy': 0.95}
)

model_artifact.add_file('model.pth')
wandb.log_artifact(model_artifact, aliases=['best', 'production'])

# Link to model registry
run.link_artifact(model_artifact, 'model-registry/production-models')
```

## 集成示例

### HuggingFace Transformers

```python
from transformers import Trainer, TrainingArguments
import wandb

# Initialize W&B
wandb.init(project="hf-transformers")

# Training arguments with W&B
training_args = TrainingArguments(
    output_dir="./results",
    report_to="wandb",  # Enable W&B logging
    run_name="bert-finetuning",
    logging_steps=100,
    save_steps=500
)

# Trainer automatically logs to W&B
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset
)

trainer.train()
```

### PyTorch Lightning

```python
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import WandbLogger
import wandb

# Create W&B logger
wandb_logger = WandbLogger(
    project="lightning-demo",
    log_model=True  # Log model checkpoints
)

# Use with Trainer
trainer = Trainer(
    logger=wandb_logger,
    max_epochs=10
)

trainer.fit(model, datamodule=dm)
```

### Keras/TensorFlow

```python
import wandb
from wandb.keras import WandbCallback

# Initialize
wandb.init(project="keras-demo")

# Add callback
model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=10,
    callbacks=[WandbCallback()]  # Auto-logs metrics
)
```

## 可视化与分析

### 自定义图表

```python
# Log custom visualizations
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(x, y)
wandb.log({"custom_plot": wandb.Image(fig)})

# Log confusion matrix
wandb.log({"conf_mat": wandb.plot.confusion_matrix(
    probs=None,
    y_true=ground_truth,
    preds=predictions,
    class_names=class_names
)})
```

### 报告功能

在 W&B 用户界面中创建可共享的报告：
- 结合运行记录、图表与文本
- 支持 Markdown 格式
- 可嵌入可视化图表
- 支持团队协作

## 最佳实践

### 1. 使用标签与组进行分类管理

```python
wandb.init(
    project="my-project",
    tags=["baseline", "resnet50", "imagenet"],
    group="resnet-experiments",  # Group related runs
    job_type="train"             # Type of job
)
```

### 2. 记录所有相关日志

```python
# Log system metrics
wandb.log({
    "gpu/util": gpu_utilization,
    "gpu/memory": gpu_memory_used,
    "cpu/util": cpu_utilization
})

# Log code version
wandb.log({"git_commit": git_commit_hash})

# Log data splits
wandb.log({
    "data/train_size": len(train_dataset),
    "data/val_size": len(val_dataset)
})
```

### 3. 使用描述性名称

```python
# ✅ Good: Descriptive run names
wandb.init(
    project="nlp-classification",
    name="bert-base-lr0.001-bs32-epoch10"
)

# ❌ Bad: Generic names
wandb.init(project="nlp", name="run1")
```

### 4. 保存重要工件

```python
# Save final model
artifact = wandb.Artifact('final-model', type='model')
artifact.add_file('model.pth')
wandb.log_artifact(artifact)

# Save predictions for analysis
predictions_table = wandb.Table(
    columns=["id", "input", "prediction", "ground_truth"],
    data=predictions_data
)
wandb.log({"predictions": predictions_table})
```

### 5. 在网络连接不稳定时使用离线模式

```python
import os

# Enable offline mode
os.environ["WANDB_MODE"] = "offline"

wandb.init(project="my-project")
# ... your code ...

# Sync later
# wandb sync <run_directory>
```

## 团队协作

### 共享运行任务

```python
# Runs are automatically shareable via URL
run = wandb.init(project="team-project")
print(f"Share this URL: {run.url}")
```

### 团队项目

- 在 wandb.ai 创建团队账户
- 添加团队成员
- 设置项目可见性（私有/公开）
- 使用团队级工件与模型注册表

## 定价方案

- **免费版**：无限个公开项目，100GB 存储空间
- **学术版**：面向学生及研究人员免费
- **团队版**：50美元/人/月，支持私有项目，存储空间无限
- **企业版**：定制化定价，提供本地部署选项

## 资源链接

- **文档**：https://docs.wandb.ai
- **GitHub 仓库**：https://github.com/wandb/wandb（星标数超1.05万）
- **示例代码**：https://github.com/wandb/examples
- **社区板块**：https://wandb.ai/community
- **Discord 社群**：https://wandb.me/discord

## 相关内容

- `references/sweeps.md` – 全面的超参数优化指南
- `references/artifacts.md` – 数据与模型版本控制方案
- `references/integrations.md` – 各框架专用示例


