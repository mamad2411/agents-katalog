---
name: trl-fine-tuning
description: "TRL: SFT, DPO, GRPO, RLOO reward modeling for LLM RLHF."
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [trl, transformers, datasets, peft, accelerate, torch]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Post-Training, TRL, Reinforcement Learning, Fine-Tuning, SFT, DPO, GRPO, RLOO, RLHF, Preference Alignment, HuggingFace]

---

# TRL – Transformer强化学习

## 快速入门

TRL提供了训练后的优化方法，用于使语言模型更符合人类的偏好。

**安装方式**：
```bash
pip install trl transformers datasets peft accelerate
```

**监督微调**（指令微调）：
```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,  # Prompt-completion pairs
)
trainer.train()
```

**DPO**（与用户偏好保持一致）：
```python
from trl import DPOTrainer, DPOConfig

config = DPOConfig(output_dir="model-dpo", beta=0.1)
trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=preference_dataset,  # chosen/rejected pairs
    processing_class=tokenizer
)
trainer.train()
```

## 常见工作流程

### 工作流程 1：完整的 RLHF 流水线（SFT → 奖励模型 → RLOO）

从基础模型到符合人类偏好的模型的完整流程。

> **注意（TRL 1.x 版本）：** PPO 已从 TRL 中**移除**——`PPOTrainer`、`PPOConfig` 以及 `python -m trl.scripts.ppo` 均不再存在。目前 TRL 仍提供在线 RL 训练器：
> **RLOO**（`RLOOTrainer` / `trl rloo`）是最接近奖励模型驱动型 RLHF 流水线的直接替代方案，而**GRPO**（`GRPOTrainer` / `trl grpo`，见工作流程 3）则是更节省内存的替代选项。下述步骤将使用 RLOO。

复制此清单：

```
RLHF Training:
- [ ] Step 1: Supervised fine-tuning (SFT)
- [ ] Step 2: Train reward model
- [ ] Step 3: RLOO reinforcement learning
- [ ] Step 4: Evaluate aligned model
```

**步骤 1：监督式微调**

使用指令遵循数据对基础模型进行训练：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# Load model
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")

# Load instruction dataset
dataset = load_dataset("trl-lib/Capybara", split="train")

# Configure training
training_args = SFTConfig(
    output_dir="Qwen2.5-0.5B-SFT",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=2e-5,
    logging_steps=10,
    save_strategy="epoch"
)

# Train
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    processing_class=tokenizer
)
trainer.train()
trainer.save_model()
```

**步骤 2：训练奖励模型**

训练模型以预测人类的偏好：

```python
from transformers import AutoModelForSequenceClassification
from trl import RewardTrainer, RewardConfig

# Load SFT model as base
model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen2.5-0.5B-SFT",
    num_labels=1  # Single reward score
)
tokenizer = AutoTokenizer.from_pretrained("Qwen2.5-0.5B-SFT")

# Load preference data (chosen/rejected pairs)
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")

# Configure training
training_args = RewardConfig(
    output_dir="Qwen2.5-0.5B-Reward",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    learning_rate=1e-5
)

# Train reward model
trainer = RewardTrainer(
    model=model,
    args=training_args,
    processing_class=tokenizer,
    train_dataset=dataset
)
trainer.train()
trainer.save_model()
```

**第3步：RLOO强化学习**

利用奖励模型对策略进行优化。在TRL 1.x版本中已移除PPO算法；此时应使用RLOO命令行工具（`trl rloo`），并通过`--reward_model_name_or_path`参数传入已训练好的奖励模型。

```bash
trl rloo \
    --model_name_or_path Qwen2.5-0.5B-SFT \
    --reward_model_name_or_path Qwen2.5-0.5B-Reward \
    --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \
    --output_dir Qwen2.5-0.5B-RLOO \
    --learning_rate 3e-6 \
    --per_device_train_batch_size 64 \
    --num_generations 4
```

对应的 Python 实现（`RLOOTrainer` / `RLOOConfig`）：
```python
from trl import RLOOTrainer, RLOOConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

reward_model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen2.5-0.5B-Reward", num_labels=1
)

config = RLOOConfig(
    output_dir="Qwen2.5-0.5B-RLOO",
    per_device_train_batch_size=64,
    learning_rate=3e-6,
    num_generations=4,
)

trainer = RLOOTrainer(
    model="Qwen2.5-0.5B-SFT",
    reward_funcs=reward_model,   # a reward model (or a callable reward function)
    args=config,
    train_dataset=dataset,       # prompt-only dataset
    processing_class=tokenizer,
)
trainer.train()
```

**第4步：进行评估**

```python
from transformers import pipeline

# Load aligned model
generator = pipeline("text-generation", model="Qwen2.5-0.5B-RLOO")

# Test
prompt = "Explain quantum computing to a 10-year-old"
output = generator(prompt, max_length=200)[0]["generated_text"]
print(output)
```

### 工作流 2：基于 DPO 的简单偏好对齐

无需奖励模型即可实现模型与偏好的对齐。

复制此检查清单：

```
DPO Training:
- [ ] Step 1: Prepare preference dataset
- [ ] Step 2: Configure DPO
- [ ] Step 3: Train with DPOTrainer
- [ ] Step 4: Evaluate alignment
```

**步骤 1：准备偏好设置数据集**

数据集格式：
```json
{
  "prompt": "What is the capital of France?",
  "chosen": "The capital of France is Paris.",
  "rejected": "I don't know."
}
```

加载数据集：
```python
from datasets import load_dataset

dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
# Or load your own
# dataset = load_dataset("json", data_files="preferences.json")
```

**步骤 2：配置 DPO**

```python
from trl import DPOConfig

config = DPOConfig(
    output_dir="Qwen2.5-0.5B-DPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=5e-7,
    beta=0.1,  # KL penalty strength
    max_prompt_length=512,
    max_length=1024,
    logging_steps=10
)
```

**第3步：使用DPOTrainer进行训练**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    processing_class=tokenizer
)

trainer.train()
trainer.save_model()
```

**命令行界面替代方案**：
```bash
trl dpo \
    --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
    --dataset_name argilla/Capybara-Preferences \
    --output_dir Qwen2.5-0.5B-DPO \
    --per_device_train_batch_size 4 \
    --learning_rate 5e-7 \
    --beta 0.1
```

### 工作流 3：基于 GRPO 的低内存在线强化学习

以极低的内存占用进行强化学习训练。

如需了解关于 GRPO 的深入指导——包括奖励函数设计、关键的训练要点（损失行为、模式崩溃问题及参数调优方法），以及高级的多阶段训练策略，请参阅 **[references/grpo-training.md](references/grpo-training.md)**。可用于实际生产的训练脚本则位于 **[templates/basic_grpo_training.py](templates/basic_grpo_training.py)** 中。

复制此检查清单：

```
GRPO Training:
- [ ] Step 1: Define reward function
- [ ] Step 2: Configure GRPO
- [ ] Step 3: Train with GRPOTrainer
```

**步骤 1：定义奖励函数**

```python
def reward_function(completions, **kwargs):
    """
    Compute rewards for completions.

    Args:
        completions: List of generated texts

    Returns:
        List of reward scores (floats)
    """
    rewards = []
    for completion in completions:
        # Example: reward based on length and unique words
        score = len(completion.split())  # Favor longer responses
        score += len(set(completion.lower().split()))  # Reward unique words
        rewards.append(score)
    return rewards
```

或者可以使用奖励模型：
```python
from transformers import pipeline

reward_model = pipeline("text-classification", model="reward-model-path")

def reward_from_model(completions, prompts, **kwargs):
    # Combine prompt + completion
    full_texts = [p + c for p, c in zip(prompts, completions)]
    # Get reward scores
    results = reward_model(full_texts)
    return [r["score"] for r in results]
```

**步骤 2：配置 GRPO**

```python
from trl import GRPOConfig

config = GRPOConfig(
    output_dir="Qwen2-GRPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=1e-5,
    num_generations=4,  # Generate 4 completions per prompt
    max_new_tokens=128
)
```

**步骤 3：使用 GRPOTrainer 进行训练**

```python
from datasets import load_dataset
from trl import GRPOTrainer

# Load prompt-only dataset
dataset = load_dataset("trl-lib/tldr", split="train")

trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_function,  # Your reward function
    args=config,
    train_dataset=dataset
)

trainer.train()
```

**命令行界面**：
```bash
trl grpo \
    --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
    --dataset_name trl-lib/tldr \
    --output_dir Qwen2-GRPO \
    --num_generations 4
```

## 何时使用 TRL 及其替代方案

**适合使用 TRL 的情况：**
- 需要使模型符合人类偏好
- 拥有偏好数据（选择/拒绝对）
- 希望使用强化学习方法（RLOO、GRPO）
- 需要训练奖励模型
- 执行完整的 RLHF 流水线

**方法选择指南：**
- **SFT**：拥有提示词与回复对，仅需基础指令遵循能力
- **DPO**：拥有偏好数据，希望实现简单对齐（无需奖励模型）
- **RLOO**：已拥有奖励模型，希望进行在线强化学习（基于奖励模型的 RLHF 方案；在 TRL 1.x 版本中已移除 PPO）
- **GRPO**：内存资源受限，但希望使用带有奖励函数的在线强化学习
- **奖励模型**：正在构建 RLHF 流水线，需要对生成内容进行评分

**建议改用替代方案的情况：**
- **HuggingFace Trainer**：无需强化学习的基础微调工具
- **Axolotl**：基于 YAML 的训练配置工具
- **LitGPT**：用于教学目的的轻量级微调工具
- **Unsloth**：高效的 LoRA 微调工具

## 常见问题

**问题：DPO 训练时出现内存不足**

解决方案：减小批量大小和序列长度。
```python
config = DPOConfig(
    per_device_train_batch_size=1,  # Reduce from 4
    max_length=512,  # Reduce from 1024
    gradient_accumulation_steps=8  # Maintain effective batch
)
```

或者使用梯度检查点技术：
```python
model.gradient_checkpointing_enable()
```

**问题：对齐质量不佳**

调整 beta 参数：
```python
# Higher beta = more conservative (stays closer to reference)
config = DPOConfig(beta=0.5)  # Default 0.1

# Lower beta = more aggressive alignment
config = DPOConfig(beta=0.01)
```

**问题：奖励模型无法学习**

请检查损失类型与学习率：
```python
config = RewardConfig(
    learning_rate=1e-5,  # Try different LR
    num_train_epochs=3  # Train longer
)
```

请确保偏好设置数据集中有明确的胜出选项：
```python
# Verify dataset
print(dataset[0])
# Should have clear chosen > rejected
```

**问题：在线强化学习（RLOO/GRPO）训练不稳定**

请调整KL/β正则化参数，使其更接近参考策略的值：
```python
from trl import RLOOConfig

config = RLOOConfig(
    beta=0.05,          # KL coefficient toward the reference model (increase for stability)
    num_generations=4,  # more samples per prompt = lower-variance advantage estimates
)
```

## 高级主题

**SFT训练指南**：有关数据集格式、对话模板、打包策略以及多GPU训练的相关内容，请参阅[references/sft-training.md](references/sft-training.md)。

**DPO变体**：IPO、cDPO、RPO以及其他DPO损失函数的相关信息，以及推荐的超参数设置，可查看[references/dpo-variants.md](references/dpo-variants.md)。

**奖励建模**：关于结果奖励与过程奖励、Bradley-Terry损失函数以及奖励模型评估的方法，详见[references/reward-modeling.md](references/reward-modeling.md)。

**在线强化学习方法**：PPO、GRPO、RLOO和OnlineDPO的详细配置信息，请参考[references/online-rl.md](references/online-rl.md)。

**GRPO深度解析**：想要了解专家级GRPO训练技巧——包括奖励函数设计理念、训练中的常见问题分析（如损失值上升的原因、模式崩溃检测）、超参数调优、多阶段训练方法以及故障排查技巧，请参阅[references/grpo-training.md](references/grpo-training.md)。可直接使用的生产级模板位于[templates/basic_grpo_training.py](templates/basic_grpo_training.py)中。

## 硬件要求

- **GPU**：NVIDIA显卡（需支持CUDA）
- **显存**：取决于模型类型与训练方法
  - SFT 7B模型：16GB（使用LoRA技术时）
  - DPO 7B模型：24GB（用于存储参考模型）
  - RLOO 7B模型：40GB（需存储策略模型与奖励模型）
  - GRPO 7B模型：24GB（内存效率更高）
- **多GPU支持**：可通过`accelerate`库实现
- **混合精度训练**：推荐使用BF16格式（适用于A100/H100显卡）

**内存优化方案**：
- 所有方法均采用 LoRA/QLoRA 技术  
- 启用梯度检查点机制  
- 通过梯度累积降低批量大小  

## 资源链接  

- 文档：https://huggingface.co/docs/trl/  
- GitHub 仓库：https://github.com/huggingface/trl  
- 相关论文：  
  - 《利用人类反馈训练能够遵循指令的语言模型》（InstructGPT，2022年）  
  - 《直接偏好优化：你的语言模型其实是一个奖励模型》（DPO，2023年）  
  - 《群体相对策略优化》（GRPO，2024年）  
- 示例代码：https://github.com/huggingface/trl/tree/main/examples/scripts



