---
name: flash-attention
description: Speed up long-sequence transformer training and inference.
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [flash-attn, torch, transformers]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Optimization, Flash Attention, Attention Optimization, Memory Efficiency, Speed Optimization, Long Context, PyTorch, SDPA, H100, FP8, Transformers]

---

# Flash Attention——高效快速的注意力机制

## 快速入门

通过基于 I/O 特性的分块处理与重新计算技术，Flash Attention 能让 Transformer 模型中的注意力计算速度提升 2-4 倍，同时内存占用减少 10-20 倍。

**PyTorch 原生支持（最简单，需 PyTorch 2.2 及以上版本）**：
```python
import torch
import torch.nn.functional as F

q = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)  # [batch, heads, seq, dim]
k = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)
v = torch.randn(2, 8, 512, 64, device='cuda', dtype=torch.float16)

# Automatically uses Flash Attention if available
out = F.scaled_dot_product_attention(q, k, v)
```

**flash-attn 库（更多功能）**：
```bash
pip install flash-attn --no-build-isolation
```

```python
from flash_attn import flash_attn_func

# q, k, v: [batch, seqlen, nheads, headdim]
out = flash_attn_func(q, k, v, dropout_p=0.0, causal=True)
```

## 常见工作流程

### 工作流程 1：在现有 PyTorch 模型中启用该功能

复制以下检查清单：

```
Flash Attention Integration:
- [ ] Step 1: Check PyTorch version (≥2.2)
- [ ] Step 2: Enable Flash Attention backend
- [ ] Step 3: Verify speedup with profiling
- [ ] Step 4: Test accuracy matches baseline
```

**步骤 1：检查 PyTorch 版本**

```bash
python -c "import torch; print(torch.__version__)"
# Should be ≥2.2.0
```

如果版本低于2.2，请进行升级：
```bash
pip install --upgrade torch
```

**步骤 2：启用 Flash Attention 后端**

替换为标准注意力机制：
```python
# Before (standard attention)
attn_weights = torch.softmax(q @ k.transpose(-2, -1) / math.sqrt(d_k), dim=-1)
out = attn_weights @ v

# After (Flash Attention)
import torch.nn.functional as F
out = F.scaled_dot_product_attention(q, k, v, attn_mask=mask)
```

强制使用 Flash Attention 后端（`torch.backends.cuda.sdp_kernel` 已被弃用；请结合 `SDPBackend` 使用 `torch.nn.attention.sdpa_kernel`）：
```python
from torch.nn.attention import SDPBackend, sdpa_kernel

with sdpa_kernel(SDPBackend.FLASH_ATTENTION):
    out = F.scaled_dot_product_attention(q, k, v)
```

**步骤 3：通过性能分析验证加速效果**

```python
import torch.utils.benchmark as benchmark

def test_attention(use_flash):
    q, k, v = [torch.randn(2, 8, 2048, 64, device='cuda', dtype=torch.float16) for _ in range(3)]

    if use_flash:
        from torch.nn.attention import SDPBackend, sdpa_kernel
        with sdpa_kernel(SDPBackend.FLASH_ATTENTION):
            return F.scaled_dot_product_attention(q, k, v)
    else:
        attn = (q @ k.transpose(-2, -1) / 8.0).softmax(dim=-1)
        return attn @ v

# Benchmark
t_flash = benchmark.Timer(stmt='test_attention(True)', globals=globals())
t_standard = benchmark.Timer(stmt='test_attention(False)', globals=globals())

print(f"Flash: {t_flash.timeit(100).mean:.3f}s")
print(f"Standard: {t_standard.timeit(100).mean:.3f}s")
```

预期效果：对于长度超过 512 个标记的序列，处理速度可提升 2 到 4 倍。

**第 4 步：验证准确率与基准值一致**

```python
# Compare outputs
q, k, v = [torch.randn(1, 8, 512, 64, device='cuda', dtype=torch.float16) for _ in range(3)]

# Flash Attention
out_flash = F.scaled_dot_product_attention(q, k, v)

# Standard attention
attn_weights = torch.softmax(q @ k.transpose(-2, -1) / 8.0, dim=-1)
out_standard = attn_weights @ v

# Check difference
diff = (out_flash - out_standard).abs().max()
print(f"Max difference: {diff:.6f}")
# Should be <1e-3 for float16
```

### 工作流 2：使用 flash-attn 库实现高级功能

适用于多查询注意力机制、滑动窗口技术或 H100 FP8 加速场景。

复制此清单：

```
flash-attn Library Setup:
- [ ] Step 1: Install flash-attn library
- [ ] Step 2: Modify attention code
- [ ] Step 3: Enable advanced features
- [ ] Step 4: Benchmark performance
```

**步骤 1：安装 flash-attn 库**

```bash
# NVIDIA GPUs (CUDA 12.0+)
pip install flash-attn --no-build-isolation

# Verify installation
python -c "from flash_attn import flash_attn_func; print('Success')"
```

**第2步：修改注意力编码**

```python
from flash_attn import flash_attn_func

# Input: [batch_size, seq_len, num_heads, head_dim]
# Transpose from [batch, heads, seq, dim] if needed
q = q.transpose(1, 2)  # [batch, seq, heads, dim]
k = k.transpose(1, 2)
v = v.transpose(1, 2)

out = flash_attn_func(
    q, k, v,
    dropout_p=0.1,
    causal=True,  # For autoregressive models
    window_size=(-1, -1),  # No sliding window
    softmax_scale=None  # Auto-scale
)

out = out.transpose(1, 2)  # Back to [batch, heads, seq, dim]
```

**第3步：启用高级功能**

多查询注意力机制（各注意力头共享K/V向量）：
```python
from flash_attn import flash_attn_func

# q: [batch, seq, num_q_heads, dim]
# k, v: [batch, seq, num_kv_heads, dim]  # Fewer KV heads
out = flash_attn_func(q, k, v)  # Automatically handles MQA
```

滑动窗口注意力机制（局部注意力）：
```python
# Only attend to window of 256 tokens before/after
out = flash_attn_func(
    q, k, v,
    window_size=(256, 256),  # (left, right) window
    causal=True
)
```

**第4步：性能基准测试**

```python
import torch
from flash_attn import flash_attn_func
import time

q, k, v = [torch.randn(4, 4096, 32, 64, device='cuda', dtype=torch.float16) for _ in range(3)]

# Warmup
for _ in range(10):
    _ = flash_attn_func(q, k, v)

# Benchmark
torch.cuda.synchronize()
start = time.time()
for _ in range(100):
    out = flash_attn_func(q, k, v)
    torch.cuda.synchronize()
end = time.time()

print(f"Time per iteration: {(end-start)/100*1000:.2f}ms")
print(f"Memory allocated: {torch.cuda.max_memory_allocated()/1e9:.2f}GB")
```

### 工作流 3：H100 FP8 优化（FlashAttention-3）

旨在为 Hopper GPU（H100）带来最佳性能。

> **重要提示：** `pip` 包 `flash-attn`（2.8.x 版本）仅提供 **FlashAttention-2** —— 它不包含 FA3 或 FP8 针对 H100 的计算内核，同时 `flash_attn_func` 也不会自动启用 FP8 模式。FlashAttention-3 是一个独立的 **测试版**，需从仓库的 `hopper/` 目录中编译源代码生成，通过 `flash_attn_interface` 模块进行调用。FA3 支持 FP16/BF16 的前向与反向计算，以及 **仅限 FP8 的前向计算**。

```
FP8 Setup:
- [ ] Step 1: Verify Hopper (H100) GPU available
- [ ] Step 2: Build & install FlashAttention-3 from source (hopper/)
- [ ] Step 3: Use the FA3 interface (FP8 forward)
```

**步骤 1：验证 H100 GPU**

```bash
nvidia-smi --query-gpu=name --format=csv
# Should show "H100" or "H800"
```

**步骤 2：从源代码构建并安装 FlashAttention-3**

`pip install flash-attn` 命令并未包含 FA3，需从 `hopper/` 子目录中自行构建。

```bash
git clone https://github.com/Dao-AILab/flash-attention.git
cd flash-attention/hopper
python setup.py install
# (compilation is heavy and requires a CUDA toolchain + Hopper GPU)
```

**第3步：使用FA3接口（FP8前向模式）**

FA3提供了独立的模块`flash_attn_interface`（与FA2的`flash_attn`不同）。
FP8属于**仅支持前向计算**的路径，要求输入数据为`float8_e4m3fn`格式：

```python
import torch
from flash_attn_interface import flash_attn_func  # FA3 (hopper build), not `flash_attn`

# q, k, v: [batch, seqlen, nheads, headdim]
q = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)
k = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)
v = torch.randn(2, 4096, 32, 64, device='cuda', dtype=torch.float16)

# FP8 forward (inference / forward-only): cast to float8_e4m3fn
q_fp8 = q.to(torch.float8_e4m3fn)
k_fp8 = k.to(torch.float8_e4m3fn)
v_fp8 = v.to(torch.float8_e4m3fn)

out = flash_attn_func(q_fp8, k_fp8, v_fp8, causal=True)
# FP16/BF16 forward+backward is also supported by the FA3 interface.
```

## 何时使用 Flash Attention 及其替代方案

**在以下情况下应使用 Flash Attention：**
- 训练长度超过 512 个标记的 Transformer 模型
- 执行上下文长度超过 2K 个标记的推理任务
- GPU 内存不足（标准注意力机制会导致内存溢出）
- 需要在不损失精度的前提下提升 2-4 倍的速度
- 使用 PyTorch 2.2+ 版本或能够安装 flash-attn 库

**此时可考虑使用替代方案：**
- **标准注意力机制**：序列长度小于 256 个标记（其额外开销并不值得）
- **xFormers**：需要更多种类的注意力机制（而不仅仅是追求速度）
- **内存高效型注意力机制**：在 CPU 上进行推理（Flash Attention 需要 GPU）

## 常见问题

**问题：ImportError: cannot import flash_attn**

请使用不启用构建隔离模式的指令进行安装：
```bash
pip install flash-attn --no-build-isolation
```

或者先安装 CUDA 工具包：
```bash
conda install cuda -c nvidia
pip install flash-attn --no-build-isolation
```

**问题：速度低于预期（无加速效果）**

Flash Attention 的优势会随着序列长度的增加而提升：
- <512 个标记：加速效果极微（10-20%）
- 512-2K 个标记：加速 2-3 倍
- >2K 个标记：加速 3-4 倍

请确认序列长度足够。

**问题：RuntimeError：CUDA 错误**

请检查您的 GPU 是否支持 Flash Attention。
```python
import torch
print(torch.cuda.get_device_capability())
# Should be ≥(7, 5) for Turing+
```

Flash Attention 的使用要求如下：
- Ampere 系列（A100、A10）：✅ 完全支持
- Turing 系列（T4）：✅ 支持
- Volta 系列（V100）：❌ 不支持

**问题：精度下降**

请确认数据类型为 float16 或 bfloat16（而非 float32）：
```python
q = q.to(torch.float16)  # Or torch.bfloat16
```

Flash Attention 采用 float16/bfloat16 格式以实现高速运算，不支持 float32 格式。

## 高级主题

**与 HuggingFace Transformers 的集成**：如需在 BERT、GPT、Llama 模型中启用 Flash Attention，请参阅 [references/transformers-integration.md](references/transformers-integration.md) 文档。

**性能基准测试**：如需了解不同 GPU 及不同序列长度下的详细速度与内存使用情况对比，可查看 [references/benchmarks.md](references/benchmarks.md)。

## 硬件要求

- **GPU**：NVIDIA Ampere+ 系列（如 A100、A10、A30）或 AMD MI200+ 系列
- **VRAM**：与标准注意力机制要求相同（Flash Attention 不会增加内存需求）
- **CUDA**：版本 12.0 及以上（最低支持 11.8 版本）
- **PyTorch**：需为 2.2 及以上版本才能获得原生支持

**不支持的硬件**：V100（Volta）系列 GPU以及基于 CPU 的推理场景。

## 相关资源

- 论文：《FlashAttention：具有 IO 感知能力的快速且节省内存的精确注意力机制》（NeurIPS 2022）
- 论文：《FlashAttention-2：具备更好并行性与任务分区的更快注意力机制》（ICLR 2024）
- 博客文章：https://tridao.me/blog/2024/flash3/
- GitHub 仓库：https://github.com/Dao-AILab/flash-attention
- PyTorch 文档：https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html



