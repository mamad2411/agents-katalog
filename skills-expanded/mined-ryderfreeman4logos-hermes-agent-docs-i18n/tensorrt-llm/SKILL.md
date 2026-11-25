---
name: tensorrt-llm
description: High-throughput LLM inference on NVIDIA GPUs.
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [tensorrt-llm, torch]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Inference Serving, TensorRT-LLM, NVIDIA, Inference Optimization, High Throughput, Low Latency, Production, FP8, INT4, In-Flight Batching, Multi-GPU]

---

# TensorRT-LLM

NVIDIA推出的开源库，旨在利用NVIDIA GPU的高性能优化大语言模型推理效率。

## 何时使用TensorRT-LLM

**以下情况建议使用TensorRT-LLM：**
- 在NVIDIA GPU（A100、H100、GB200）上部署模型
- 需要极高的处理速度（Llama 3模型可达24,000+ tokens/秒）
- 实时应用对低延迟有严格要求
- 处理量化后的模型（FP8、INT4、FP4格式）
- 需要在多台GPU或节点之间扩展部署

**以下情况建议改用vLLM：**
- 需要更简单的设置流程以及以Python为优先的API接口
- 希望使用PagedAttention机制且无需经过TensorRT编译
- 在AMD GPU或非NVIDIA硬件上运行模型

**以下情况建议改用llama.cpp：**
- 在CPU或Apple Silicon平台上部署模型
- 需要在没有NVIDIA GPU的情况下进行边缘端部署
- 希望使用更简单的GGUF量化格式

## 快速入门

### 安装

```bash
# Docker (recommended) — images are on NGC (nvcr.io), not Docker Hub.
# Replace x.y.z with the desired version (e.g. 1.2.1). Browse tags on NGC:
# https://catalog.ngc.nvidia.com/orgs/nvidia/teams/tensorrt-llm/containers/release/tags
docker pull nvcr.io/nvidia/tensorrt-llm/release:x.y.z

# pip install (current stable GA)
pip install tensorrt_llm

# Requires CUDA 13.2.1, TensorRT 10.x, Python 3.10-3.12
```

### 基本推理

```python
from tensorrt_llm import LLM, SamplingParams

# Initialize model
llm = LLM(model="meta-llama/Meta-Llama-3-8B")

# Configure sampling
sampling_params = SamplingParams(
    max_tokens=100,
    temperature=0.7,
    top_p=0.9
)

# Generate
prompts = ["Explain quantum computing"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(output.text)
```

### 使用 trtllm-serve 进行服务部署

```bash
# Start server (automatic model download and compilation)
trtllm-serve meta-llama/Meta-Llama-3-8B \
    --tp_size 4 \              # Tensor parallelism (4 GPUs)
    --max_batch_size 256 \
    --max_num_tokens 4096

# Client request
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Meta-Llama-3-8B",
    "messages": [{"role": "user", "content": "Hello!"}],
    "temperature": 0.7,
    "max_tokens": 100
  }'
```

## 核心特性

### 性能优化
- **传输中批量处理**：在生成过程中实现动态批量化
- **分页KV缓存**：高效的内存管理机制
- **Flash Attention**：优化的注意力计算内核
- **量化技术**：支持FP8、INT4、FP4格式，提升推理速度2-4倍
- **CUDA图优化**：降低内核启动开销

### 并行处理能力
- **张量并行（TP）**：将模型分布在多块GPU上运行
- **流水线并行（PP）**：按层分配计算任务
- **专家并行**：专为混合专家模型设计
- **多节点部署**：突破单机限制实现扩展

### 高级功能
- **推测解码**：借助草稿模型加快生成速度
- **LoRA服务**：高效的多适配器部署方案
- **分离式服务**：将预填充与生成过程分开处理

## 常见应用模式

### 量化模型（FP8格式）

```python
from tensorrt_llm import LLM

# Load FP8 quantized model (2× faster, 50% memory)
llm = LLM(
    model="meta-llama/Meta-Llama-3-70B",
    dtype="fp8",
    max_num_tokens=8192
)

# Inference same as before
outputs = llm.generate(["Summarize this article..."])
```

### 多 GPU 部署

```python
# Tensor parallelism across 8 GPUs
llm = LLM(
    model="meta-llama/Meta-Llama-3-405B",
    tensor_parallel_size=8,
    dtype="fp8"
)
```

### 批量推理

```python
# Process 100 prompts efficiently
prompts = [f"Question {i}: ..." for i in range(100)]

outputs = llm.generate(
    prompts,
    sampling_params=SamplingParams(max_tokens=200)
)

# Automatic in-flight batching for maximum throughput
```

## 性能基准测试

**Meta Llama 3-8B**（H100 GPU）：
- 处理速度：24,000 个标记/秒
- 延迟：每个标记约 10 毫秒
- 相较于 PyTorch：**速度快 100 倍**

**Llama 3-70B**（8× A100 80GB）：
- FP8 量化模式：速度为 FP16 的 2 倍
- 使用 FP8 后内存占用减少 50%

## 支持的模型

- **LLaMA 系列**：Llama 2、Llama 3、CodeLlama
- **GPT 系列**：GPT-2、GPT-J、GPT-NeoX
- **Qwen 系列**：Qwen、Qwen2、QwQ
- **DeepSeek 系列**：DeepSeek-V2、DeepSeek-V3
- **Mixtral 系列**：Mixtral-8x7B、Mixtral-8x22B
- **视觉模型**：LLaVA、Phi-3-vision
- HuggingFace 上的 **100 多种模型**

## 参考资料

- **[优化指南](references/optimization.md)** – 量化处理、批量处理、KV 缓存优化
- **[多 GPU 部署指南](references/multi-gpu.md)** – 张量/流水线并行处理、多节点部署
- **[服务部署指南](references/serving.md)** – 生产环境部署、监控及自动扩缩容

## 相关资源

- **文档**：https://nvidia.github.io/TensorRT-LLM/
- **GitHub 仓库**：https://github.com/NVIDIA/TensorRT-LLM
- **模型列表**：https://huggingface.co/models?library=tensorrt_llm


