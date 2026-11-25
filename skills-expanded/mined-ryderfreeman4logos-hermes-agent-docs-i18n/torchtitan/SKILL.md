---
name: torchtitan
description: Pretrain LLMs at scale with PyTorch 4D parallelism.
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [torch>=2.6.0, torchtitan>=0.2.0, torchao>=0.5.0]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Model Architecture, Distributed Training, TorchTitan, FSDP2, Tensor Parallel, Pipeline Parallel, Context Parallel, Float8, Llama, Pretraining]

---

# TorchTitan——PyTorch 原生分布式大语言模型预训练框架

## 快速入门

TorchTitan 是 PyTorch 官方推出的大规模大语言模型预训练平台，支持可组合的 4D 并行计算技术（FSDP2、TP、PP、CP），在 H100 GPU 上的训练速度相比基础方案可提升 65% 以上。

**安装方式**：
```bash
# From PyPI (stable)
pip install torchtitan

# From source (latest features, requires PyTorch nightly)
git clone https://github.com/pytorch/torchtitan
cd torchtitan
pip install -r requirements.txt
```

**下载分词器**：
```bash
# Get HF token from https://huggingface.co/settings/tokens
python scripts/download_hf_assets.py --repo_id meta-llama/Llama-3.1-8B --assets tokenizer --hf_token=...
```

**在8块GPU上开始训练**：
```bash
# Configs are selected by name from the Python config registry
# (torchtitan/models/llama3/config_registry.py), not by TOML path
MODULE=llama3 CONFIG=llama3_8b ./run_train.sh
```

## 常见工作流程

### 工作流程 1：在单节点上预训练 Llama 3.1 8B 模型

复制此检查清单：

```
Single Node Pretraining:
- [ ] Step 1: Download tokenizer
- [ ] Step 2: Configure training
- [ ] Step 3: Launch training
- [ ] Step 4: Monitor and checkpoint
```

**步骤 1：下载分词器**

```bash
python scripts/download_hf_assets.py \
  --repo_id meta-llama/Llama-3.1-8B \
  --assets tokenizer \
  --hf_token=YOUR_HF_TOKEN
```

**第2步：配置训练参数**

在torchtitan当前的架构中，运行配置定义在Python的**配置注册表**中（位于`torchtitan/models/llama3/config_registry.py`），可通过`CONFIG=<名称>`（或`--config <名称>`）按名称来选择这些配置。如需自定义配置，可在注册表中添加自己的配置文件；或者直接在命令行中覆盖特定字段的值（例如`--optimizer.lr 3e-4 --training.steps 1000`）。

对于8B参数规模的模型，相应的设置如下所示（以字段形式呈现；可在注册表条目中设置这些值，或通过`--section.key value`的方式进行覆盖）：

```toml
# fields for a llama3 8B run (register in config_registry.py or pass as --overrides)
[job]
dump_folder = "./outputs"
description = "Llama 3.1 8B training"

[model]
name = "llama3"
flavor = "8B"
hf_assets_path = "./assets/hf/Llama-3.1-8B"

[optimizer]
name = "AdamW"
lr = 3e-4

[lr_scheduler]
warmup_steps = 200

[training]
local_batch_size = 2
seq_len = 8192
max_norm = 1.0
steps = 1000
dataset = "c4"

[parallelism]
data_parallel_shard_degree = -1  # Use all GPUs for FSDP

[activation_checkpoint]
mode = "selective"
selective_ac_option = "op"

[checkpoint]
enable = true
folder = "checkpoint"
interval = 500
```

**第3步：启动训练**

```bash
# 8 GPUs on single node (config selected by name from the registry)
MODULE=llama3 CONFIG=llama3_8b ./run_train.sh

# Override individual fields on the command line
MODULE=llama3 CONFIG=llama3_8b ./run_train.sh --optimizer.lr 3e-4 --training.steps 1000

# Or explicitly with torchrun (run_train.sh wraps this)
torchrun --nproc_per_node=8 \
  -m torchtitan.train \
  --module llama3 --config llama3_8b
```

**第4步：监控与检查点生成**

TensorBoard日志会被保存至 `./outputs/tb/` 目录中：
```bash
tensorboard --logdir ./outputs/tb
```

### 工作流 2：基于 SLURM 的多节点训练

```
Multi-Node Training:
- [ ] Step 1: Configure parallelism for scale
- [ ] Step 2: Set up SLURM script
- [ ] Step 3: Submit job
- [ ] Step 4: Resume from checkpoint
```

**步骤 1：配置并行度以实现规模扩展**

针对基于 256 块 GPU（32 个节点）运行的 700 亿参数模型：
```toml
[parallelism]
data_parallel_shard_degree = 32  # FSDP across 32 ranks
tensor_parallel_degree = 8        # TP within node
pipeline_parallel_degree = 1      # No PP for 70B
context_parallel_degree = 1       # Increase for long sequences
```

**步骤 2：配置 SLURM 脚本**

```bash
#!/bin/bash
#SBATCH --job-name=llama70b
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=8
#SBATCH --gpus-per-node=8

srun torchrun \
  --nnodes=32 \
  --nproc_per_node=8 \
  --rdzv_backend=c10d \
  --rdzv_endpoint=$MASTER_ADDR:$MASTER_PORT \
  -m torchtitan.train \
  --module llama3 --config llama3_70b
```

**步骤 3：提交任务**

```bash
sbatch multinode_trainer.slurm
```

**第4步：从检查点继续训练**

如果在配置的文件夹中存在检查点，训练将自动从中继续。

### 工作流程3：为H100显卡启用Float8训练模式

在H100 GPU上，使用Float8格式可提升30-50%的训练速度。

```
Float8 Training:
- [ ] Step 1: Install torchao
- [ ] Step 2: Configure Float8
- [ ] Step 3: Launch with compile
```

**步骤 1：安装 torchao**

```bash
USE_CPP=0 pip install git+https://github.com/pytorch/ao.git
```

**步骤 2：配置 Float8**

在当前的 torchtitan 中，Float8 是通过在配置注册表中的 `model_registry()` 调用中设置 `quantization` 参数来在配置阶段实现的（而非通过 `[quantize.linear.float8]` 这一 TOML 配置项）。需添加一个 `Float8LinearConverter.Config` 对象：

```python
# in torchtitan/models/llama3/config_registry.py (your model_registry(...) call)
from torchtitan.components.quantization import Float8LinearConverter

model_spec = model_registry(
    "8B",
    quantization=[
        Float8LinearConverter.Config(
            recipe_name="rowwise",          # or "rowwise_with_gw_hp"
            filter_fqns=["output"],          # skip layers too small to benefit
            model_compile_enabled=True,      # requires torch.compile for competitive perf
        ),
    ],
)
```

也请在运行配置中启用 `torch.compile`：
```toml
[compile]
enable = true
components = ["model", "loss"]
```

**第3步：通过编译方式启动**

```bash
# Float8 config is baked into the registered config; just select it and enable compile
MODULE=llama3 CONFIG=llama3_8b ./run_train.sh --compile.enable
```

### 工作流 4：针对 405B 模型的 4D 并行处理方案

```
4D Parallelism (FSDP + TP + PP + CP):
- [ ] Step 1: Create seed checkpoint
- [ ] Step 2: Configure 4D parallelism
- [ ] Step 3: Launch on 512 GPUs
```

**步骤 1：创建种子检查点**

这是确保在多个 PP 阶段之间实现一致初始化的必要条件：
```bash
NGPU=1 MODULE=llama3 CONFIG=llama3_405b ./run_train.sh \
  --checkpoint.enable \
  --checkpoint.create_seed_checkpoint \
  --parallelism.data_parallel_shard_degree 1 \
  --parallelism.tensor_parallel_degree 1 \
  --parallelism.pipeline_parallel_degree 1
```

**步骤 2：配置 4D 并行处理**

```toml
[parallelism]
data_parallel_shard_degree = 8   # FSDP
tensor_parallel_degree = 8       # TP within node
pipeline_parallel_degree = 8     # PP across nodes
context_parallel_degree = 1      # CP for long sequences

[training]
local_batch_size = 32
seq_len = 8192
```

**步骤 3：在 512 块 GPU 上启动**

```bash
# 64 nodes x 8 GPUs = 512 GPUs
srun torchrun --nnodes=64 --nproc_per_node=8 \
  -m torchtitan.train \
  --module llama3 --config llama3_405b
```

## 何时使用 TorchTitan 及其替代方案

**适合使用 TorchTitan 的场景：**
- 从零开始预训练大型语言模型（8B 到 405B+ 参数量）
- 需要无需第三方依赖的纯 PyTorch 解决方案
- 需要可组合的 4D 并行计算能力（FSDP2、TP、PP、CP）
- 在支持 Float8 加速的 H100 硬件上进行训练
- 希望生成的检查点能与 torchtune/HuggingFace 兼容

**可选择的其他替代方案：**
- **Megatron-LM**：专为 NVIDIA 平台设计，可实现最佳性能
- **DeepSpeed**：拥有更完善的 ZeRO 优化生态及推理支持功能
- **Axolotl/TRL**：适用于微调而非预训练任务
- **LitGPT**：用于教学目的的小规模训练场景

## 常见问题

**问题：大型模型导致内存不足**

请启用激活值检查点功能并减小批量大小：
```toml
[activation_checkpoint]
mode = "full"  # Instead of "selective"

[training]
local_batch_size = 1
```

或者可以使用梯度累积方法：
```toml
[training]
local_batch_size = 1
global_batch_size = 32  # Accumulates gradients
```

**问题：异步集合操作导致 TP 模式下内存占用过高**

设置环境变量：
```bash
export TORCH_NCCL_AVOID_RECORD_STREAMS=1
```

**问题：Float8训练并未带来更快的速度提升**

Float8的优势仅体现在大规模矩阵乘法运算中。可通过转换器中的`filter_fqns`功能来过滤掉小型层：
```python
from torchtitan.components.quantization import Float8LinearConverter

Float8LinearConverter.Config(
    # add "auto_filter_small_kn" to auto-skip layers too small to benefit
    filter_fqns=["attention.wk", "attention.wv", "output", "auto_filter_small_kn"],
    model_compile_enabled=True,
)
```

**问题：更改并行度后检查点加载失败**

请使用 DCP 的重分片功能：
```bash
# Convert sharded checkpoint to single file
python -m torch.distributed.checkpoint.format_utils \
  dcp_to_torch checkpoint/step-1000 checkpoint.pt
```

**问题：流水线并行初始化**

请先创建种子检查点（参见工作流 4 的第 1 步）。

## 支持的模型

| 模型 | 参数量 | 状态 |
|-------|--------|------|
| Llama 3.1 | 8B、70B、405B | 已投入生产使用 |
| Llama 4 | 多种规格 | 测试中 |
| DeepSeek V3 | 16B、236B、671B（混合精度版） | 测试中 |
| GPT-OSS | 20B、120B（混合精度版） | 测试中 |
| Qwen 3 | 多种规格 | 测试中 |
| Flux | 扩散模型 | 测试中 |

## 性能基准测试（H100）

| 模型 | GPU 数量 | 并行策略 | 每 GPU TPS | 优化技术 |
|-------|----------|----------|-----------|----------|
| Llama 8B | 8 | FSDP | 5,762 | 基准值 |
| Llama 8B | 8 | FSDP+编译+FP8 | 8,532 | 提升 48% |
| Llama 70B | 256 | FSDP+TP+AsyncTP | 876 | 二维并行 |
| Llama 405B | 512 | FSDP+TP+PP | 128 | 三维并行 |

## 进阶主题

**FSDP2 配置**：有关 FSDP2 与 FSDP1 的详细对比以及 ZeRO 等效配置，请参阅 [references/fsdp.md](references/fsdp.md)。

**Float8 训练**：关于张量级缩放与行级缩放的实现方法，请参阅 [references/float8.md](references/float8.md)。

**检查点保存**：有关 HuggingFace 格式转换及异步检查点保存的详细信息，请参阅 [references/checkpoint.md](references/checkpoint.md)。

**添加自定义模型**：关于 TrainSpec 协议的用法，请参阅 [references/custom-models.md](references/custom-models.md)。

## 相关资源

- GitHub 仓库：https://github.com/pytorch/torchtitan
- 论文链接：https://arxiv.org/abs/2410.06511
- ICLR 2025 发表页：https://iclr.cc/virtual/2025/poster/29620
- PyTorch 论坛讨论帖：https://discuss.pytorch.org/c/distributed/torchtitan/44

