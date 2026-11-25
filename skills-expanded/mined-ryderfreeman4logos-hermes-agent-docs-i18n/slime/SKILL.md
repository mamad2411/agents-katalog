---
name: slime
description: RL post-training for LLMs with Megatron and SGLang.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [sglang-router>=0.2.3, ray, torch>=2.0.0, transformers>=4.40.0]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Reinforcement Learning, Megatron-LM, SGLang, GRPO, Post-Training, GLM]

---

# slime：用于强化学习规模扩展的LLM训练后框架

slime是由清华大学THUDM团队开发的LLM训练后框架，为GLM-4.5、GLM-4.6及GLM-4.7等模型提供了技术支持。该框架将用于训练的Megatron-LM技术与用于高效模型部署生成的SGLang技术相连接。

## 何时使用slime

**在以下情况下可选择slime：**
- 需要结合Megatron-LM的训练功能与SGLang的推理能力
- 需要具备灵活数据缓冲区的自定义数据生成工作流
- 需要训练GLM、Qwen3、DeepSeek V3或Llama 3等模型
- 需要兼具研究级功能与生产环境支持（由Z.ai提供保障）的框架

**在以下情况下可考虑其他替代方案：**
- 需要企业级稳定性功能 → 使用**miles**
- 需要灵活更换后端技术 → 使用**verl**
- 需要PyTorch原生的抽象层功能 → 使用**torchforge**

## 核心特性

- **训练功能**：支持全并行度的Megatron-LM训练（TP、PP、DP、SP模式）
- **模型部署**：基于SGLang的高效生成技术，并配有路由器功能
- **数据缓冲区**：提供灵活的提示词管理及样本存储功能
- **支持的模型**：GLM-4.x系列、Qwen3、DeepSeek V3/R1、Llama 3

## 架构概览

```
┌─────────────────────────────────────────────────────────┐
│                    Data Buffer                          │
│ - Prompt initialization and management                  │
│ - Custom data generation and filtering                  │
│ - Rollout sample storage                                │
└─────────────┬───────────────────────────┬───────────────┘
              │                           │
┌─────────────▼───────────┐ ┌─────────────▼───────────────┐
│ Training (Megatron-LM)  │ │ Rollout (SGLang + Router)   │
│ - Actor model training  │ │ - Response generation       │
│ - Critic (optional)     │ │ - Reward/verifier output    │
│ - Weight sync to rollout│ │ - Multi-turn support        │
└─────────────────────────┘ └─────────────────────────────┘
```

## 安装指南

```bash
# Recommended: Docker
docker pull slimerl/slime:latest
docker run --rm --gpus all --ipc=host --shm-size=16g \
  -it slimerl/slime:latest /bin/bash

# Inside container
cd /root/slime && pip install -e . --no-deps
```

### 来源内容

```bash
git clone https://github.com/THUDM/slime.git
cd slime
pip install -r requirements.txt
pip install -e .
```

## 快速入门：GRPO训练

```bash
# Source model configuration
source scripts/models/qwen3-4B.sh

# Launch training
python train.py \
    --actor-num-nodes 1 \
    --actor-num-gpus-per-node 4 \
    --rollout-num-gpus 4 \
    --advantage-estimator grpo \
    --use-kl-loss --kl-loss-coef 0.001 \
    --rollout-batch-size 32 \
    --n-samples-per-prompt 8 \
    --global-batch-size 256 \
    --num-rollout 3000 \
    --prompt-data /path/to/data.jsonl \
    ${MODEL_ARGS[@]} ${CKPT_ARGS[@]}
```

## 工作流 1：标准 GRPO 训练

该工作流用于训练具有群体相对优势的推理模型。

### 前提条件清单
- [ ] 已安装 Docker 环境或 Megatron-LM + SGLang
- [ ] 模型检查点（HuggingFace 或 Megatron 格式）
- [ ] 以 JSONL 格式提供的训练数据

### 第 1 步：准备数据

```python
# data.jsonl format
{"prompt": "What is 2 + 2?", "label": "4"}
{"prompt": "Solve: 3x = 12", "label": "x = 4"}
```

或者以聊天格式输入：
```python
{
    "prompt": [
        {"role": "system", "content": "You are a math tutor."},
        {"role": "user", "content": "What is 15 + 27?"}
    ],
    "label": "42"
}
```

### 第 2 步：配置模型

选择预配置好的模型脚本：

```bash
# List available models
ls scripts/models/
# glm4-9B.sh, qwen3-4B.sh, qwen3-30B-A3B.sh, deepseek-v3.sh, llama3-8B.sh, ...

# Source your model
source scripts/models/qwen3-4B.sh
```

### 第3步：启动训练

```bash
python train.py \
    --actor-num-nodes 1 \
    --actor-num-gpus-per-node 8 \
    --rollout-num-gpus 8 \
    --advantage-estimator grpo \
    --use-kl-loss \
    --kl-loss-coef 0.001 \
    --prompt-data /path/to/train.jsonl \
    --input-key prompt \
    --label-key label \
    --apply-chat-template \
    --rollout-batch-size 32 \
    --n-samples-per-prompt 8 \
    --global-batch-size 256 \
    --num-rollout 3000 \
    --save-interval 100 \
    --eval-interval 50 \
    ${MODEL_ARGS[@]}
```

### 第4步：监控训练过程
- [ ] 查看TensorBoard日志：`tensorboard --logdir outputs/`
- [ ] 确认奖励曲线呈上升趋势
- [ ] 监控各节点的GPU使用率

---

## 工作流2：异步训练

通过并行执行推理与训练操作，利用异步模式提升处理效率。

### 适用场景
- 模型规模较大且生成时间较长
- 同步模式下GPU空闲时间较多
- 存储足够内存用于数据缓冲

### 启动异步训练

```bash
python train_async.py \
    --actor-num-nodes 1 \
    --actor-num-gpus-per-node 8 \
    --rollout-num-gpus 8 \
    --advantage-estimator grpo \
    --async-buffer-size 4 \
    --prompt-data /path/to/train.jsonl \
    ${MODEL_ARGS[@]}
```

### 异步操作专用参数

```bash
--async-buffer-size 4        # Number of rollouts to buffer
--update-weights-interval 2  # Sync weights every N rollouts
```

## 工作流 3：多轮智能体训练

此工作流适用于需要工具使用能力或多步骤推理能力的智能体训练。

### 先决条件
- [ ] 用于实现多轮逻辑的自定义生成函数
- [ ] 工具/环境接口

### 第 1 步：定义自定义生成函数

```python
# custom_generate.py
async def custom_generate(args, samples, evaluation=False):
    """Multi-turn generation with tool calling."""
    for sample in samples:
        conversation = sample.prompt

        for turn in range(args.max_turns):
            # Generate response
            response = await generate_single(conversation)

            # Check for tool call
            tool_call = extract_tool_call(response)
            if tool_call:
                tool_result = execute_tool(tool_call)
                conversation.append({"role": "assistant", "content": response})
                conversation.append({"role": "tool", "content": tool_result})
            else:
                break

        sample.response = response
        sample.reward = compute_reward(sample)

    return samples
```

### 第二步：使用自定义功能启动代理

```bash
python train.py \
    --custom-generate-function-path custom_generate.py \
    --max-turns 5 \
    --prompt-data /path/to/agent_data.jsonl \
    ${MODEL_ARGS[@]}
```

如需查看完整的多轮搜索示例，请参阅 `examples/search-r1/`。

---

## 配置参考

### 三种参数类型

Slime 支持三种类型的参数：

**1. Megatron 参数**（直接传递）：
```bash
--tensor-model-parallel-size 2
--pipeline-model-parallel-size 1
--num-layers 32
--hidden-size 4096
```

**2. SGLang 参数**（以 `--sglang-` 为前缀）：
```bash
--sglang-mem-fraction-static 0.8
--sglang-context-length 8192
--sglang-log-level INFO
```

**3. slime 参数**：
```bash
# Resource allocation
--actor-num-nodes 1
--actor-num-gpus-per-node 8
--rollout-num-gpus 8
--colocate  # Share GPUs between training/inference

# Data
--prompt-data /path/to/data.jsonl
--input-key prompt
--label-key label

# Training loop
--num-rollout 3000
--rollout-batch-size 32
--n-samples-per-prompt 8
--global-batch-size 256

# Algorithm
--advantage-estimator grpo  # or: gspo, ppo, reinforce_plus_plus
--use-kl-loss
--kl-loss-coef 0.001
```

### 核心限制条件

```
rollout_batch_size × n_samples_per_prompt = global_batch_size × num_steps_per_rollout
```

示例：32 × 8 = 256 × 1

---

## 数据缓冲系统

slime 的数据缓冲功能可实现灵活的数据管理：

### 基本数据源

```python
class RolloutDataSource:
    def get_samples(self, num_samples):
        """Fetch prompts from dataset."""
        return self.dataset.sample(num_samples)

    def add_samples(self, samples):
        """Called after generation (no-op by default)."""
        pass
```

### 缓冲数据源（离线模式）

```python
class RolloutDataSourceWithBuffer(RolloutDataSource):
    def __init__(self):
        self.buffer = []

    def add_samples(self, samples):
        """Store generated samples for reuse."""
        self.buffer.extend(samples)

    def buffer_filter(self, args, buffer, num_samples):
        """Custom selection logic (prioritized, stratified, etc.)."""
        return select_best(buffer, num_samples)
```

## 常见问题与解决方案

### 问题：SGLang 引擎崩溃

**症状**：推理引擎在训练过程中突然终止运行

**解决方案**：
```bash
# Enable fault tolerance
--use-fault-tolerance

# Increase memory allocation
--sglang-mem-fraction-static 0.85

# Reduce batch size
--rollout-batch-size 16
```

### 问题：权重同步超时

**症状**：模型部署完成后训练进程卡住

**解决方案**：
```bash
# Increase sync interval
--update-weights-interval 5

# Use colocated mode (no network transfer)
--colocate
```

### 问题：训练过程中出现内存溢出

**症状**：在反向传播阶段出现 CUDA 内存不足的情况

**解决方案**：
```bash
# Enable gradient checkpointing
--recompute-activations

# Reduce micro-batch size
--micro-batch-size 1

# Enable sequence parallelism
--sequence-parallel
```

### 问题：数据加载速度缓慢

**症状**：在数据获取过程中GPU处于空闲状态

**解决方案**：
```bash
# Increase data workers
--num-data-workers 4

# Use streaming dataset
--streaming-data
```

## 支持的模型

| 模型系列 | 配置选项 |
|----------|----------|
| GLM | GLM-4.5、GLM-4.6、GLM-4.7、GLM-Z1-9B |
| Qwen | Qwen3（4B、8B、30B-A3B）、Qwen3-MoE、Qwen2.5 |
| DeepSeek | V3、V3.1、R1 |
| Llama | Llama 3（8B、70B） |
| 其他 | Kimi K2、Moonlight-16B |

所有模型在 `scripts/models/` 目录下均配有预配置脚本。

---

## 高级主题

### 共享部署模式

通过在训练与推理之间共享 GPU 来降低内存占用：

```bash
python train.py \
    --colocate \
    --actor-num-gpus-per-node 8 \
    --sglang-mem-fraction-static 0.4 \
    ${MODEL_ARGS[@]}
```

### 自定义奖励模型

```python
# custom_rm.py
class CustomRewardModel:
    def __init__(self, model_path):
        self.model = load_model(model_path)

    def compute_reward(self, prompts, responses):
        inputs = self.tokenize(prompts, responses)
        scores = self.model(inputs)
        return scores.tolist()
```

```bash
--custom-rm-path custom_rm.py
```

### 多任务评估功能

```bash
--eval-prompt-data aime /path/to/aime.jsonl \
--eval-prompt-data gsm8k /path/to/gsm8k.jsonl \
--n-samples-per-eval-prompt 16
```

## 资源

- **文档**：https://thudm.github.io/slime/
- **GitHub 仓库**：https://github.com/THUDM/slime
- **博客文章**：https://lmsys.org/blog/2025-07-09-slime/
- **示例代码**：请查看 `examples/` 目录，其中包含14个以上可直接运行的示例。

