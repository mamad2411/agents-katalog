---
name: llama-cpp
description: llama.cpp local GGUF inference + HF Hub model discovery.
version: 2.1.2
author: Orchestra Research
license: MIT
dependencies: [llama-cpp-python>=0.2.0]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [llama.cpp, GGUF, Quantization, Hugging Face Hub, CPU Inference, Apple Silicon, Edge Deployment, AMD GPUs, Intel GPUs, NVIDIA, URL-first]
---

# llama.cpp + GGUF

此技能适用于在本地进行GGUF模型推理、量化格式选择，以及查找适用于llama.cpp的Hugging Face仓库。

## 适用场景

- 在CPU、Apple Silicon芯片、CUDA、ROCm或Intel GPU上运行本地模型
- 为特定的Hugging Face仓库寻找合适的GGUF格式模型
- 根据Hub中的信息构建`llama-server`或`llama-cli`命令
- 在Hub中搜索已支持llama.cpp的模型
- 查看某个仓库中可用的`.gguf`文件及其大小
- 根据用户的RAM或VRAM容量选择Q4/Q5/Q6/IQ等量化版本

## 模型查找流程

在请求使用`hf`、Python脚本或自定义代码之前，优先尝试通过URL进行查找。

1. 在Hub上搜索候选仓库：
   - 基础链接：`https://huggingface.co/models?apps=llama.cpp&sort=trending`
   - 若需查找特定模型系列，可添加`search=<术语>`参数
   - 若用户对模型大小有要求，可添加`num_parameters=min:0,max:24B`之类的筛选条件
2. 使用llama.cpp的本地应用视图打开该仓库：
   - 链接格式：`https://huggingface.co/<仓库名>?local-app=llama.cpp`
3. 当本地应用视图内容可见时，将其视为权威信息来源：
   - 复制准确的`llama-server`或`llama-cli`命令
   - 按照Hugging Face显示的格式直接采用推荐的量化设置
4. 将带有`?local-app=llama.cpp`参数的页面内容作为文本或HTML进行读取，并提取“硬件兼容性”部分的信息：
   - 相较于通用表格，优先参考其中明确的量化标签和大小数值
   - 保留仓库特有的量化标识，如`UD-Q4_K_M`或`IQ4_NL_XL`
   - 若页面源代码中未显示该部分内容，请说明情况，并转而使用树形API及通用量化指南
5. 通过树形API确认实际存在的文件：
   - 链接格式：`https://huggingface.co/api/models/<仓库名>/tree/main?recursive=true`
   - 仅保留`type`为`file`且`path`以`.gguf`结尾的条目
   - 以`path`和`size`字段作为文件名和字节大小的权威依据
   - 将量化后的模型文件与`mmproj-*.gguf`格式的投影文件以及`BF16/`格式的分片文件区分开
   - 仅将`https://huggingface.co/<仓库名>/tree/main`作为人工查询的备用选项
6. 若本地应用视图的内容无法以文本形式显示，则根据仓库信息及选定的量化格式重新构造命令：
   - 简化版量化选择方式：`llama-server -hf <仓库名>:<量化格式>`
   - 基于具体文件的备用方式：`llama-server --hf-repo <仓库名> --hf-file <文件名.gguf>`
7. 仅当某个仓库未提供GGUF格式文件时，才建议将其从Transformers模型权重转换而来。

## 快速入门

### 安装llama.cpp

```bash
# macOS / Linux (simplest)
brew install llama.cpp
```

```bash
winget install llama.cpp
```

```bash
git clone https://github.com/ggml-org/llama.cpp
cd llama.cpp
cmake -B build
cmake --build build --config Release
```

### 直接在 Hugging Face Hub 上运行

```bash
llama-cli -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

```bash
llama-server -hf bartowski/Llama-3.2-3B-Instruct-GGUF:Q8_0
```

### 从 Hub 运行完整的 GGUF 文件

当树形 API 显示自定义文件名，或缺失完整的 HF 片段时，请使用此方法。

```bash
llama-server \
    --hf-repo microsoft/Phi-3-mini-4k-instruct-gguf \
    --hf-file Phi-3-mini-4k-instruct-q4.gguf \
    -c 4096
```

### 兼容 OpenAI 的服务器检测

```bash
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Write a limerick about Python exceptions"}
    ]
  }'
```

## Python绑定（llama-cpp-python）

使用命令 `pip install llama-cpp-python` 进行安装（若使用CUDA，则需执行：`CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python --force-reinstall --no-cache-dir`；若使用Metal，则为：`CMAKE_ARGS="-DGGML_METAL=on" ...`）。

### 基本生成功能

```python
from llama_cpp import Llama

llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,
    n_gpu_layers=35,     # 0 for CPU, 99 to offload everything
    n_threads=8,
)

out = llm("What is machine learning?", max_tokens=256, temperature=0.7)
print(out["choices"][0]["text"])
```

### 聊天与流式处理

```python
llm = Llama(
    model_path="./model-q4_k_m.gguf",
    n_ctx=4096,
    n_gpu_layers=35,
    chat_format="llama-3",   # or "chatml", "mistral", etc.
)

resp = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"},
    ],
    max_tokens=256,
)
print(resp["choices"][0]["message"]["content"])

# Streaming
for chunk in llm("Explain quantum computing:", max_tokens=256, stream=True):
    print(chunk["choices"][0]["text"], end="", flush=True)
```

### 嵌入模型

```python
llm = Llama(model_path="./model-q4_k_m.gguf", embedding=True, n_gpu_layers=35)
vec = llm.embed("This is a test sentence.")
print(f"Embedding dimension: {len(vec)}")
```

您也可以直接从 Hub 加载 GGUF 模型：

```python
llm = Llama.from_pretrained(
    repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
    filename="*Q4_K_M.gguf",
    n_gpu_layers=35,
)
```

## 选择量化版本

首先参考Hub页面上的信息，其次再依据通用规则进行判断。

- 建议优先选择HF针对用户硬件配置标注为兼容的量化版本。
- 用于常规聊天时，可从`Q4_K_M`开始选择。
- 进行代码编写或技术工作时，若内存允许，建议选择`Q5_K_M`或`Q6_K`。
- 在内存资源极为紧张的情况下，仅当用户明确将模型适配性置于质量之上时，才考虑使用`Q3_K_M`、`IQ`系列或`Q2`系列量化版本。
- 对于多模态模型仓库，需单独提及`mmproj-*.gguf`文件——这些投影器文件并非主模型文件。
- 不要对仓库原有的标签进行标准化处理。若页面显示为`UD-Q4_K_M`，则直接报告该标签即可。

## 从仓库中提取可用的GGUF文件

当用户询问有哪些GGUF文件时，需返回以下信息：

- 文件名
- 文件大小
- 量化标签
- 该文件是主模型还是辅助投影器文件

除非用户特别要求，否则忽略以下内容：

- README文件
- BF16格式的分片文件
- imatrix二进制数据或校准相关文件

此步骤可使用tree API来完成：

- `https://huggingface.co/api/models/<repo>/tree/main?recursive=true`

以`unsloth/Qwen3.6-35B-A3B-GGUF`这样的仓库为例，local-app页面会显示诸如`UD-Q4_K_M`、`UD-Q5_K_M`、`UD-Q6_K`和`Q8_0`之类的量化版本标识，而tree API则会提供包含字节大小的精确文件路径，如`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`和`Qwen3.6-35B-A3B-Q8_0.gguf`。可通过tree API将量化标签转换为具体的文件名。

## 搜索模式

可直接使用以下URL格式：

```text
https://huggingface.co/models?apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&sort=trending
https://huggingface.co/models?search=<term>&apps=llama.cpp&num_parameters=min:0,max:24B&sort=trending
https://huggingface.co/<repo>?local-app=llama.cpp
https://huggingface.co/api/models/<repo>/tree/main?recursive=true
https://huggingface.co/<repo>/tree/main
```

## 输出格式

在回应探索请求时，建议采用结构化且简洁的格式，例如：

```text
Repo: <repo>
Recommended quant from HF: <label> (<size>)
llama-server: <command>
Other GGUFs:
- <filename> - <size>
- <filename> - <size>
Source URLs:
- <local-app URL>
- <tree API URL>
```

## 参考资料

- **[hub-discovery.md](references/hub-discovery.md)** — 仅涉及 URL 的 Hugging Face 工作流、搜索模式、GGUF 文件提取以及命令重构相关内容
- **[advanced-usage.md](references/advanced-use.md)** — 推测解码、批量推理、受语法约束的生成、LoRA 技术、多 GPU 使用、自定义构建方式以及基准测试脚本
- **[quantization.md](references/quantization.md)** — 量化质量与性能之间的权衡、何时选择 Q4/Q5/Q6/IQ 等量化级别、模型大小调整方法以及 imatrix 技术
- **[server.md](references/server.md)** — 直接从 Hugging Face Hub 启动服务器、OpenAI API 接口、Docker 部署方案、NGINX 负载均衡配置以及监控方法
- **[optimization.md](references/optimization.md)** — CPU 线程优化、BLAS 库应用、GPU 卸载优化策略、批量推理参数调优以及相关基准测试
- **[troubleshooting.md](references/troubleshooting.md)** — 安装、转换、量化及推理过程中出现的服务器问题处理方法，以及 Apple Silicon 平台下的调试技巧

## 资源链接

- **GitHub 仓库**：https://github.com/ggml-org/llama.cpp
- **Hugging Face GGUF + llama.cpp 文档**：https://huggingface.co/docs/hub/gguf-llamacpp
- **Hugging Face 本地应用文档**：https://huggingface.co/docs/hub/main/local-apps
- **Hugging Face 本地智能体文档**：https://huggingface.co/docs/hub/agents-local
- **本地应用示例页面**：https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF?local-app=llama.cpp
- **树形 API 示例**：https://huggingface.co/api/models/unsloth/Qwen3.6-35B-A3B-GGUF/tree/main?recursive=true
- **llama.cpp 搜索示例**：https://huggingface.co/models?num_parameters=min:0,max:24B&apps=llama.cpp&sort=trending
- **许可证**：MIT
