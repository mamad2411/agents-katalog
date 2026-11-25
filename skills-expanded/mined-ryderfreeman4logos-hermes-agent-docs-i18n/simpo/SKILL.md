---
name: simpo
description: Reference-free preference alignment, simpler than DPO.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [torch, transformers, datasets, trl, accelerate]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Post-Training, SimPO, Preference Optimization, Alignment, DPO Alternative, Reference-Free, LLM Alignment, Efficient Training]

---

# SimPO – 简易偏好优化算法

## 快速入门

SimPO是一种无需参考模型的偏好优化方法，即便没有参考模型也能实现优于DPO的优化效果。

**安装方式**：
```bash
# Create environment
conda create -n simpo python=3.10 && conda activate simpo

# Install PyTorch 2.2.2
# Visit: https://pytorch.org/get-started/locally/

# Install alignment-handbook
git clone https://github.com/huggingface/alignment-handbook.git
cd alignment-handbook
python -m pip install .

# Install Flash Attention 2
python -m pip install flash-attn --no-build-isolation
```

**训练**（Mistral 7B）：
```bash
ACCELERATE_LOG_LEVEL=info accelerate launch \
  --config_file accelerate_configs/deepspeed_zero3.yaml \
  scripts/run_simpo.py \
  training_configs/mistral-7b-base-simpo.yaml
```

## 常见工作流程

### 工作流程 1：基于基础模型（Mistral 7B）进行训练

**配置文件**（`mistral-7b-base-simpo.yaml`）：
```yaml
# Model
model_name_or_path: mistralai/Mistral-7B-v0.1
torch_dtype: bfloat16

# Dataset
dataset_mixer:
  HuggingFaceH4/ultrafeedback_binarized: 1.0
dataset_splits:
  - train_prefs
  - test_prefs

# SimPO hyperparameters
beta: 2.0                  # Reward scaling (2.0-10.0)
gamma_beta_ratio: 0.5       # Target margin (0-1)
loss_type: sigmoid          # sigmoid or hinge
sft_weight: 0.0             # Optional SFT regularization

# Training
learning_rate: 5e-7         # Critical: 3e-7 to 1e-6
num_train_epochs: 1
per_device_train_batch_size: 1
gradient_accumulation_steps: 8

# Output
output_dir: ./outputs/mistral-7b-simpo
```

**启动培训**：
```bash
accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \
  scripts/run_simpo.py training_configs/mistral-7b-base-simpo.yaml
```

### 工作流 2：微调指令模型（Llama 3 8B）

**配置文件**（`llama3-8b-instruct-simpo.yaml`）：
```yaml
model_name_or_path: meta-llama/Meta-Llama-3-8B-Instruct

dataset_mixer:
  argilla/ultrafeedback-binarized-preferences-cleaned: 1.0

beta: 2.5
gamma_beta_ratio: 0.5
learning_rate: 5e-7
sft_weight: 0.1             # Add SFT loss to preserve capabilities

num_train_epochs: 1
per_device_train_batch_size: 2
gradient_accumulation_steps: 4
output_dir: ./outputs/llama3-8b-simpo
```

**启动**：
```bash
accelerate launch --config_file accelerate_configs/deepspeed_zero3.yaml \
  scripts/run_simpo.py training_configs/llama3-8b-instruct-simpo.yaml
```

### 工作流 3：需大量推理的任务（较低学习率）

**适用于数学/代码任务**：
```yaml
model_name_or_path: deepseek-ai/deepseek-math-7b-base

dataset_mixer:
  argilla/distilabel-math-preference-dpo: 1.0

beta: 5.0                   # Higher for stronger signal
gamma_beta_ratio: 0.7       # Larger margin
learning_rate: 3e-7         # Lower LR for reasoning
sft_weight: 0.0

num_train_epochs: 1
per_device_train_batch_size: 1
gradient_accumulation_steps: 16
```

## 何时使用 SimPO 及其替代方案

**适合使用 SimPO 的情况**：
- 希望采用比 DPO 更简单的训练方式（无需参考模型）
- 已有偏好数据（选定/拒绝的配对）
- 需要比 DPO 更好的性能
- 计算资源有限
- 单节点训练即可满足需求

**算法选择对比**：
- **SimPO**：最简单，性能最佳，无需参考模型
- **DPO**：需要参考模型作为基准，策略更为保守
- **PPO**：控制能力最强，但需要奖励模型，设置较为复杂
- **GRPO**：内存效率高的强化学习算法，无需评价函数

**应选择替代方案的情况**：
- **OpenRLHF**：支持多节点分布式训练，可采用 PPO/GRPO 算法
- **TRL**：需要在同一框架中整合多种方法
- **DPO**：作为成熟的基准进行对比测试

## 常见问题

**问题：损失值发散**

降低学习率：
```yaml
learning_rate: 3e-7  # Reduce from 5e-7
```

降低测试版本强度：
```yaml
beta: 1.0  # Reduce from 2.0
```

**问题：模型遗忘自身能力**

添加SFT正则化机制：
```yaml
sft_weight: 0.1  # Add SFT loss component
```

**问题：偏好设置分离度不足**

提高β值与边际值：
```yaml
beta: 5.0            # Increase from 2.0
gamma_beta_ratio: 0.8  # Increase from 0.5
```

**问题：训练过程中出现内存不足**  
降低批次大小：
```yaml
per_device_train_batch_size: 1
gradient_accumulation_steps: 16  # Maintain effective batch
```

启用梯度检查点功能：
```yaml
gradient_checkpointing: true
```

## 高级主题

**损失函数**：有关 Sigmoid 损失与 Hinge 损失的对比、数学公式以及各自适用场景的信息，请参阅 [references/loss-functions.md](references/loss-functions.md)。

**超参数调优**：关于 beta、gamma 参数及学习率的选择指南，以及针对不同模型规模的推荐方案，请查看 [references/hyperparameters.md](references/hyperparameters.md)。

**数据集准备**：有关偏好数据格式、数据质量筛选以及自定义数据集创建的方法，请参考 [references/datasets.md](references/datasets.md)。

## 硬件要求

- **GPU**：建议使用 NVIDIA A100/H100
- **显存需求**：
  - 7B 模型：1 块 A100 40GB 显存（搭配 DeepSpeed ZeRO-3）
  - 8B 模型：2 块 A100 40GB 显存
  - 70B 模型：8 块 A100 80GB 显存
- **单节点部署**：使用 DeepSpeed ZeRO-3 即可满足需求
- **混合精度计算**：建议采用 BF16 格式

**内存优化方案**：
- DeepSpeed ZeRO-3（默认配置）
- 梯度检查点技术
- Flash Attention 2

## 相关资源

- 论文：https://arxiv.org/abs/2405.14734（2024 年 NeurIPS 大会发表）
- GitHub 仓库：https://github.com/princeton-nlp/SimPO
- 模型地址：https://huggingface.co/princeton-nlp
- 对齐手册：https://github.com/huggingface/alignment-handbook



