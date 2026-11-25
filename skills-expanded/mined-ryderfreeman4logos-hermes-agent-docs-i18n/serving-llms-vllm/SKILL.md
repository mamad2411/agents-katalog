---
name: serving-llms-vllm
description: "vLLM: high-throughput LLM serving, OpenAI API, quantization."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [vllm, torch, transformers]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [vLLM, Inference Serving, PagedAttention, Continuous Batching, High Throughput, Production, OpenAI API, Quantization, Tensor Parallelism]

---

# vLLM —— 高性能大语言模型服务框架

## 适用场景

适用于部署生产级大语言模型 API、优化推理延迟与吞吐量，以及为 GPU 内存有限的场景提供模型服务。该框架支持 OpenAI 兼容的接口、量化技术（GPTQ/AWQ/FP8）以及张量并行处理。

## 快速入门

通过 PagedAttention（基于分块的关键字值缓存机制）和连续批处理（混合预填充请求与解码请求），vLLM 的吞吐量相比传统 Transformer 框架可提升 24 倍。

**安装方式**：
```bash
pip install vllm
```

**基础离线推理**：
```python
from vllm import LLM, SamplingParams

llm = LLM(model="meta-llama/Llama-3-8B-Instruct")
sampling = SamplingParams(temperature=0.7, max_tokens=256)

outputs = llm.generate(["Explain quantum computing"], sampling)
print(outputs[0].outputs[0].text)
```

**兼容 OpenAI 的服务器**：
```bash
vllm serve meta-llama/Llama-3-8B-Instruct

# Query with OpenAI SDK
python -c "
from openai import OpenAI
client = OpenAI(base_url='http://localhost:8000/v1', api_key='EMPTY')
print(client.chat.completions.create(
    model='meta-llama/Llama-3-8B-Instruct',
    messages=[{'role': 'user', 'content': 'Hello!'}]
).choices[0].message.content)
"
```

## 常见工作流程

### 工作流程 1：生产环境 API 部署

复制此清单并跟踪进度：

```
Deployment Progress:
- [ ] Step 1: Configure server settings
- [ ] Step 2: Test with limited traffic
- [ ] Step 3: Enable monitoring
- [ ] Step 4: Deploy to production
- [ ] Step 5: Verify performance metrics
```

**步骤 1：配置服务器设置**

根据模型规模选择相应的配置方案：

```bash
# For 7B-13B models on single GPU
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --max-model-len 8192 \
  --port 8000

# For 30B-70B models with tensor parallelism
vllm serve meta-llama/Llama-2-70b-hf \
  --tensor-parallel-size 4 \
  --gpu-memory-utilization 0.9 \
  --quantization awq \
  --port 8000

# For production with caching and metrics
vllm serve meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching \
  --enable-metrics \
  --metrics-port 9090 \
  --port 8000 \
  --host 0.0.0.0
```

**步骤 2：在有限流量下进行测试**

在生产环境部署之前，先运行负载测试：

```bash
# Install load testing tool
pip install locust

# Create test_load.py with sample requests
# Run: locust -f test_load.py --host http://localhost:8000
```

请确保首次生成令牌的时间（TTFT）小于 500 毫秒，且吞吐量大于 100 个请求/秒。

**步骤 3：启用监控功能**

vLLM 会在 9090 端口上暴露 Prometheus 指标：

```bash
curl http://localhost:9090/metrics | grep vllm
```

需要监控的关键指标：
- `vllm:time_to_first_token_seconds` —— 延迟时间
- `vllm:num_requests_running` —— 正在处理的请求数量
- `vllm:gpu_cache_usage_perc` —— KV缓存使用率

**第4步：部署到生产环境**

建议使用Docker以确保部署的一致性：

```bash
# Run vLLM in Docker
docker run --gpus all -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3-8B-Instruct \
  --gpu-memory-utilization 0.9 \
  --enable-prefix-caching
```

**第5步：验证性能指标**

确认部署结果是否达到预期目标：
- TTFT < 500毫秒（针对短文本提示）
- 吞吐量 > 预设请求/秒阈值
- GPU利用率 > 80%
- 日志中无内存不足错误

### 工作流2：离线批量推理

用于在无需服务器开销的情况下处理大型数据集。

复制此检查清单：

```
Batch Processing:
- [ ] Step 1: Prepare input data
- [ ] Step 2: Configure LLM engine
- [ ] Step 3: Run batch inference
- [ ] Step 4: Process results
```

**步骤 1：准备输入数据**

```python
# Load prompts from file
prompts = []
with open("prompts.txt") as f:
    prompts = [line.strip() for line in f]

print(f"Loaded {len(prompts)} prompts")
```

**步骤 2：配置大语言模型引擎**

```python
from vllm import LLM, SamplingParams

llm = LLM(
    model="meta-llama/Llama-3-8B-Instruct",
    tensor_parallel_size=2,  # Use 2 GPUs
    gpu_memory_utilization=0.9,
    max_model_len=4096
)

sampling = SamplingParams(
    temperature=0.7,
    top_p=0.95,
    max_tokens=512,
    stop=["</s>", "\n\n"]
)
```

**步骤 3：执行批量推理**

为提升效率，vLLM 会自动对请求进行批量处理：

```python
# Process all prompts in one call
outputs = llm.generate(prompts, sampling)

# vLLM handles batching internally
# No need to manually chunk prompts
```

**第4步：处理结果**

```python
# Extract generated text
results = []
for output in outputs:
    prompt = output.prompt
    generated = output.outputs[0].text
    results.append({
        "prompt": prompt,
        "generated": generated,
        "tokens": len(output.outputs[0].token_ids)
    })

# Save to file
import json
with open("results.jsonl", "w") as f:
    for result in results:
        f.write(json.dumps(result) + "\n")

print(f"Processed {len(results)} prompts")
```

### 工作流 3：量化模型服务

在有限的 GPU 内存中部署大型模型。

```
Quantization Setup:
- [ ] Step 1: Choose quantization method
- [ ] Step 2: Find or create quantized model
- [ ] Step 3: Launch with quantization flag
- [ ] Step 4: Verify accuracy
```

**步骤 1：选择量化方法**

- **AWQ**：最适合 70B 模型，精度损失最小  
- **GPTQ**：支持多种模型类型，压缩效果优异  
- **FP8**：在 H100 GPU 上运行速度最快  

**步骤 2：查找或创建量化后的模型**

可使用 HuggingFace 提供的预量化模型：

```bash
# Search for AWQ models
# Example: TheBloke/Llama-2-70B-AWQ
```

**步骤 3：使用量化标志启动**

```bash
# Using pre-quantized model
vllm serve TheBloke/Llama-2-70B-AWQ \
  --quantization awq \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.95

# Results: 70B model in ~40GB VRAM
```

**第4步：验证准确性**

检查输出结果是否符合预期质量标准：

```python
# Compare quantized vs non-quantized responses
# Verify task-specific performance unchanged
```

## 何时使用 vLLM 及其替代方案

**适合使用 vLLM 的场景：**
- 部署生产级 LLM API（每秒请求量超过 100 次）
- 提供兼容 OpenAI 的接口
- GPU 内存有限但需要运行大型模型
- 多用户应用（聊天机器人、智能助手）
- 需要低延迟与高吞吐量的处理能力

**建议选择替代方案的情况：**
- **llama.cpp**：适用于 CPU/边缘设备推理，单用户使用
- **HuggingFace transformers**：适合研究、原型开发以及一次性文本生成任务
- **TensorRT-LLM**：仅支持 NVIDIA 硬件，需追求极致性能时使用
- **Text-Generation-Inference**：已集成在 HuggingFace 生态系统中

## 常见问题

**问题：加载模型时内存不足**

降低内存占用：
```bash
vllm serve MODEL \
  --gpu-memory-utilization 0.7 \
  --max-model-len 4096
```

或者使用量化功能：
```bash
vllm serve MODEL --quantization awq
```

**问题：首个令牌生成速度过慢（TTFT超过1秒）**

为重复发送的提示语启用前缀缓存功能：
```bash
vllm serve MODEL --enable-prefix-caching
```

对于较长的提示词，请启用分块预填充功能：
```bash
vllm serve MODEL --enable-chunked-prefill
```

**问题：模型未找到错误**

如需使用自定义模型，请使用 `--trust-remote-code` 参数：
```bash
vllm serve MODEL --trust-remote-code
```

**问题：吞吐量过低（<50 次请求/秒）**

增加并发序列数：
```bash
vllm serve MODEL --max-num-seqs 512
```

使用 `nvidia-smi` 工具检查 GPU 的利用率——该数值应大于 80%。

**问题：推理速度低于预期**

请确认张量并行化已使用 2 的幂次方数量的 GPU：
```bash
vllm serve MODEL --tensor-parallel-size 4  # Not 3
```

启用推测解码以提升生成速度：
```bash
vllm serve MODEL --speculative-model DRAFT_MODEL
```

## 高级主题

**服务器部署方案**：有关 Docker、Kubernetes 及负载均衡配置的详细信息，请参阅 [references/server-deployment.md](references/server-deployment.md)。

**性能优化**：关于 PagedAttention 调优、连续批处理机制及基准测试结果的详情，可查看 [references/optimization.md](references/optimization.md)。

**量化指南**：涉及 AWQ/GPTQ/FP8 的配置方法、模型准备流程以及精度对比等内容，请参考 [references/quantization.md](references/quantization.md)。

**故障排除**：详细的错误信息、调试步骤及性能诊断方法，请查阅 [references/troubleshooting.md](references/troubleshooting.md)。

## 硬件要求

- **小型模型（7B-13B）**：1 块 A10（24GB）或 A100（40GB）显卡
- **中型模型（30B-40B）**：2 块支持张量并行的 A100（40GB）显卡
- **大型模型（70B+）**：4 块 A100（40GB）显卡或 2 块 A100（80GB）显卡，建议使用 AWQ/GPTQ 技术

支持的硬件平台：NVIDIA（主要支持）、AMD ROCm、Intel GPU 以及 TPU。

## 相关资源

- 官方文档：https://docs.vllm.ai
- GitHub 仓库：https://github.com/vllm-project/vllm
- 相关论文：《基于 PagedAttention 的大型语言模型高效内存管理方法》（SOSP 2023）
- 社区论坛：https://discuss.vllm.ai



