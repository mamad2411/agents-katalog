---
name: obliteratus
description: "OBLITERATUS: abliterate LLM refusals (diff-in-means)."
version: 2.0.0
author: Hermes Agent
license: MIT
dependencies: [obliteratus, torch, transformers, bitsandbytes, accelerate, safetensors]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Abliteration, Uncensoring, Refusal-Removal, LLM, Weight-Projection, SVD, Mechanistic-Interpretability, HuggingFace, Model-Surgery]
    related_skills: [serving-llms-vllm, llama-cpp, huggingface-tokenizers]
---

# OBLITERATUS 技能

## 功能概览

包含 9 种 CLI 命令、28 个分析模块、5 个计算层级下的 116 个模型预设，同时还支持竞赛评估功能以及基于遥测数据的推荐机制。

无需重新训练或微调，即可消除开源大型语言模型中的拒绝行为（安全约束）。该技能运用多种机制可解释性技术——包括差分均值法、SVD、白化 SVD、LEACE 概念消除法、SAE 分解法、贝叶斯核投影法等——精准识别模型权重中的拒绝逻辑并将其剔除，同时保留模型的推理能力。

**许可证警告：** OBLITERATUS 采用 AGPL-3.0 许可协议。严禁将其作为 Python 库导入，必须通过 CLI（`obliteratus` 命令）或子进程方式调用，这样才能保持 Hermes Agent 所遵循的 MIT 许可协议的纯净性。

## 视频教程

演示 Hermes Agent 如何使用 OBLITERATUS 消除 Gemma 模型的安全约束：
https://www.youtube.com/watch?v=8fG9BrNTeHs（“OBLITERATUS：一个能够消除 Gemma 4 安全约束的 AI 智能体”）

适合希望在亲自操作之前先直观了解整个端到端工作流程的用户。

## 适用场景

当用户出现以下情况时可使用此技能：
- 希望“解除审查”或“消除”某个大型语言模型的限制
- 询问如何去除模型中的拒绝机制或安全约束
- 想要创建 Llama、Qwen、Mistral 等模型的无限制版本
- 提及“去除拒绝行为”、“消除限制”、“权重投影”等相关术语
- 希望分析模型的拒绝机制运作方式
- 提到 OBLITERATUS、abliterator 或拒绝逻辑相关内容

## 第 1 步：安装

首先检查该技能是否已安装：
```bash
obliteratus --version 2>/dev/null && echo "INSTALLED" || echo "NOT INSTALLED"
```

如果尚未安装，请从 GitHub 克隆并安装：
```bash
git clone https://github.com/elder-plinius/OBLITERATUS.git
cd OBLITERATUS
pip install -e .
# For Gradio web UI support:
# pip install -e ".[spaces]"
```

**重要提示：** 安装前请务必与用户确认。该安装过程会引入约5-10GB的依赖项（如PyTorch、Transformers、bitsandbytes等）。 

## 第2步：检查硬件配置

在开始之前，先确认系统中可用的是哪款GPU：
```bash
python3 -c "
import torch
if torch.cuda.is_available():
    gpu = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
    print(f'GPU: {gpu}')
    print(f'VRAM: {vram:.1f} GB')
    if vram < 4: print('TIER: tiny (models under 1B)')
    elif vram < 8: print('TIER: small (models 1-4B)')
    elif vram < 16: print('TIER: medium (models 4-9B with 4bit quant)')
    elif vram < 32: print('TIER: large (models 8-32B with 4bit quant)')
    else: print('TIER: frontier (models 32B+)')
else:
    print('NO GPU - only tiny models (under 1B) on CPU')
"
```

### VRAM需求（采用4位量化后）

| VRAM容量 | 最大模型参数量 | 典型模型示例                          |
|:---------|:----------------|:--------------------------------------|
| 仅CPU    | 约10亿参数      | GPT-2、TinyLlama、SmolLM              |
| 4-8 GB   | 约40亿参数      | Qwen2.5-1.5B、Phi-3.5 mini、Llama 3.2 3B |
| 8-16 GB  | 约90亿参数      | Llama 3.1 8B、Mistral 7B、Gemma 2 9B   |
| 24 GB    | 约320亿参数     | Qwen3-32B、Llama 3.1 70B（高压缩版）、Command-R |
| 48 GB+   | 约720亿参数以上 | Qwen2.5-72B、DeepSeek-R1              |
| 多GPU配置 | 2000亿参数以上  | Llama 3.1 405B、DeepSeek-V3（6850亿参数MoE架构） |

## 第3步：浏览可用模型并获取推荐

```bash
# Browse models by compute tier
obliteratus models --tier medium

# Get architecture info for a specific model
obliteratus info <model_name>

# Get telemetry-driven recommendation for best method & params
obliteratus recommend <model_name>
obliteratus recommend <model_name> --insights  # global cross-architecture rankings
```

## 第4步：选择方法

### 方法选择指南
**默认值/大多数场景的推荐方案为 `advanced`。** 该模式采用带范数保持投影的多方向SVD技术，且经过充分测试。

| 使用场景                         | 推荐方法 | 原因说明                                 |
|:----------------------------------|:-------------------|:------------------------------------------|
| 默认设置/大多数模型             | `advanced`         | 采用多方向SVD技术，具备范数保持功能，性能稳定 |
| 快速测试/原型开发               | `basic`            | 操作快速简单，足以满足评估需求           |
| 高密度模型（Llama、Mistral）      | `advanced`         | 支持多方向处理及范数保持功能           |
| MoE模型（DeepSeek、Mixtral）     | `nuclear`          | 能够精细控制专家节点，有效应对MoE模型的复杂性 |
| 推理模型（R1 distills）         | `surgical`         | 具备思维链感知能力，可保留推理过程       |
| 模型持续拒绝响应                 | `aggressive`       | 结合白化SVD技术、头部微调及越狱策略       |
| 希望实现可逆修改                 | 使用引导向量（详见分析部分）         |
| 对质量要求极高且时间不受限       | `optimized`        | 通过贝叶斯搜索寻找最优参数组合           |
| 实验性自动检测                   | `informed`         | 自动识别对齐类型——属于实验性方案，性能未必始终优于`advanced` |

### 9种CLI方法
- **basic** — 通过差分均值法确定单一拒绝方向。速度较快（8B模型约需5-10分钟）。  
- **advanced**（默认值，推荐使用）—— 多个SVD方向、保范投影以及两次优化迭代。速度中等（约需10-20分钟）。  
- **aggressive** — 使用白化SVD技术结合越狱对比学习与注意力头调整机制。虽能提高处理效率，但存在更大的逻辑连贯性受损风险。  
- **spectral_cascade** — 基于DCT的频域分解方法。属于研究性质的创新方案。  
- **informed** — 在删除过程中实时进行分析以自动配置参数。属于实验性方法，其速度较“advanced”模式更慢，且结果更具不确定性。  
- **surgical** — 结合SAE特征、神经元掩蔽技术、注意力头调整以及专家级细粒度控制。处理速度极慢（约需1-2小时），最适合用于推理型模型。  
- **optimized** — 通过贝叶斯超参数搜索（Optuna TPE）优化参数。虽然运行时间最长，但能找到最优配置。  
- **inverted** — 反转拒绝方向，使模型转为主动配合状态。  
- **nuclear** — 针对顽固的MoE模型采用的强力组合策略，支持专家级细粒度控制。  

### 方向提取方法（--direction-method标志）  
- **diff_means**（默认值）—— 通过比较被拒绝与被接受时的激活值差异来实现方向判定，稳定性较高。  
- **svd** — 基于多方向SVD进行提取，更适用于复杂的对齐任务。  
- **leace** — LEACE算法（基于封闭形式估计的线性删除方法），可实现最优的线性删除效果。  

### 4种仅支持Python API的方法  
（无法通过CLI调用——需通过Python导入实现，而这违反了AGPL许可证的规定。仅当用户明确希望在自己的AGPL项目中将OBLITERATUS作为库使用时才可告知其相关信息。）
- failspy、gabliteration、heretic、rdo

## 第5步：运行 Abliteration

### 标准用法
```bash
# Default method (advanced) — recommended for most models
obliteratus obliterate <model_name> --method advanced --output-dir ./abliterated-models

# With 4-bit quantization (saves VRAM)
obliteratus obliterate <model_name> --method advanced --quantization 4bit --output-dir ./abliterated-models

# Large models (70B+) — conservative defaults
obliteratus obliterate <model_name> --method advanced --quantization 4bit --large-model --output-dir ./abliterated-models
```

### 微调参数
```bash
obliteratus obliterate <model_name> \
  --method advanced \
  --direction-method diff_means \
  --n-directions 4 \
  --refinement-passes 2 \
  --regularization 0.1 \
  --quantization 4bit \
  --output-dir ./abliterated-models \
  --contribute  # opt-in telemetry for community research
```

### 主要参数
| 参数 | 描述 | 默认值 |
|:-----|:------------|:--------|
| `--method` | 模型压缩方法 | advanced |
| `--direction-method` | 方向提取方式 | diff_means |
| `--n-directions` | 拒绝方向数量（1-32） | 取决于所选方法 |
| `--refinement-passes` | 迭代优化次数（1-5） | 2 |
| `--regularization` | 正则化强度（0.0-1.0） | 0.1 |
| `--quantization` | 模型精度：4位或8位 | none（全精度） |
| `--large-model` | 120B以上模型使用的保守默认设置 | false |
| `--output-dir` | 压缩后模型的保存路径 | ./obliterated_model |
| `--contribute` | 是否分享匿名化后的结果以供研究使用 | false |
| `--verify-sample-size` | 用于验证拒绝功能的测试提示数量 | 20 |
| `--dtype` | 模型数据类型（float16、bfloat16） | auto |

### 其他执行模式
```bash
# Interactive guided mode (hardware → model → preset)
obliteratus interactive

# Web UI (Gradio)
obliteratus ui --port 7860

# Run a full ablation study from YAML config
obliteratus run config.yaml --preset quick

# Tournament: pit all methods against each other
obliteratus tourney <model_name>
```

## 第6步：验证结果

完成消隐处理后，需检查各项输出指标：

| 指标 | 合格值 | 警告值 |
|:-------|:-----------|:--------|
| 拒绝率 | < 5%（理想值为约0%） | > 10%表示拒绝现象依然存在 |
| 困难度变化幅度 | 增加量 < 10% | > 15%表明文本连贯性受损 |
| KL散度 | < 0.1 | > 0.5说明分布发生了显著偏移 |
| 文本连贯性 | 高/通过定性检查 | 响应质量下降，出现重复内容 |

### 若拒绝率依然较高（> 10%）
1. 尝试使用`aggressive`方法
2. 增加`--n-directions`的数值（例如设置为8或16）
3. 添加`--refinement-passes 3`参数
4. 将`diff_means`替换为`--direction-method svd`进行尝试

### 若文本连贯性受损（困难度增加量 > 15%）
1. 减少`--n-directions`的数值（可尝试设置为2）
2. 增加`--regularization`的数值（可尝试设置为0.3）
3. 将`--refinement-passes`的数值降至1
4. 尝试使用更为温和的`basic`方法

## 第7步：使用消隐后的模型

最终生成的输出为标准的HuggingFace模型目录结构。

```bash
# Test locally with transformers
python3 -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained('./abliterated-models/<model>')
tokenizer = AutoTokenizer.from_pretrained('./abliterated-models/<model>')
inputs = tokenizer('How do I pick a lock?', return_tensors='pt')
outputs = model.generate(**inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
"

# Upload to HuggingFace Hub
huggingface-cli upload <username>/<model-name>-abliterated ./abliterated-models/<model>

# Serve with vLLM
vllm serve ./abliterated-models/<model>
```

## CLI 命令参考

| 命令 | 描述 |
|:--------|:------------|
| `obliteratus obliterate` | 主要的消融分析命令 |
| `obliteratus info <model>` | 输出模型架构详情 |
| `obliteratus models --tier <tier>` | 按计算层级浏览精选模型 |
| `obliteratus recommend <model>` | 基于遥测数据的方法/参数推荐功能 |
| `obliteratus interactive` | 引导式设置向导 |
| `obliteratus tourney <model>` | 比赛模式：所有方法相互对比 |
| `obliteratus run <config.yaml>` | 根据 YAML 文件执行消融研究 |
| `obliteratus strategies` | 列出所有已注册的消融策略 |
| `obliteratus report <results.json>` | 重新生成可视化报告 |
| `obliteratus ui` | 启动 Gradio 网页界面 |
| `obliteratus aggregate` | 汇总社区遥测数据 |

## 分析模块

OBLITERATUS 提供 28 个用于机制可解释性的分析模块。
完整参考信息请参见 `skill_view(name="obliteratus", file_path="references/analysis-modules.md")`。

### 快速分析命令
```bash
# Run specific analysis modules
obliteratus run analysis-config.yaml --preset quick

# Key modules to run first:
# - alignment_imprint: Fingerprint DPO/RLHF/CAI/SFT alignment method
# - concept_geometry: Single direction vs polyhedral cone
# - logit_lens: Which layer decides to refuse
# - anti_ouroboros: Self-repair risk score
# - causal_tracing: Causally necessary components
```

### 指向向量（可逆的替代方案）
无需永久修改权重，可采用推理时的指向控制方式：
```python
# Python API only — for user's own projects
from obliteratus.analysis.steering_vectors import SteeringVectorFactory, SteeringHookManager
```

## 消融策略

除了基于方向的消融方法外，OBLITERATUS 还提供了结构化消融策略：
- **嵌入层消融** — 针对嵌入层组件进行消融
- **前馈网络消融** — 移除前馈网络中的特定模块
- **注意力头剪枝** — 对注意力头进行剪枝处理
- **整层移除** — 直接删除整个层

查看所有可用策略：`obliteratus strategies`

## 评估功能

OBLITERATUS 内置了多种评估工具：
- 拒绝率基准测试
- 混乱度对比（消融前后）
- 集成 LM Eval Harness 以支持学术界常用的基准测试
- 直接与同类模型进行性能对比
- 基线性能跟踪

## 平台支持

- **CUDA** — 完全支持（NVIDIA GPU）
- **Apple Silicon (MLX)** — 通过 MLX 后端实现支持
- **CPU** — 支持参数量极小的模型（< 10亿参数）

## YAML 配置模板

可通过 `skill_view` 加载配置模板，以实现可重复的实验运行：
- `templates/abliteration-config.yaml` — 标准单模型配置模板
- `templates/analysis-study.yaml` — 消融前的分析研究配置模板
- `templates/batch-abliteration.yaml` — 多模型批量处理配置模板

## 远程监控功能

OBLITERATUS 可选择将匿名化的实验运行数据贡献至全球研究数据集。可通过 `--contribute` 参数启用该功能。系统不会收集任何个人数据，仅记录模型名称、方法及相关指标。

## 常见问题

1. **请勿将 `informed` 作为默认选项** — 该模式仍处于实验阶段，且运行速度较慢。如需获得稳定可靠的实验结果，请使用 `advanced` 模式。
2. **参数量低于10亿的模型对“消融法”的反应较差**——这类模型的拒绝行为较为肤浅且零散，难以准确提取拒绝原因。因此只能获得部分结果（仍有20-40%的拒绝率）。而30亿参数及以上的模型则能给出更清晰的拒绝理由，表现也更好（使用`advanced`模式时通常可降至0%的拒绝率）。

3. **`aggressive`模式可能会适得其反**——在小型模型上，该模式不仅会破坏文本连贯性，反而还会提高拒绝率。仅当在30亿参数及以上的模型上使用`advanced`模式后仍存在10%以上的拒绝率时，才建议启用此模式。

4. **务必监控困惑度指标**——若其数值超过15%，说明模型已受损，此时应降低攻击性参数的强度。

5. **混合专家模型需要特殊处理**——对于Mixtral、DeepSeek-MoE等这类模型，应使用`nuclear`方法进行处理。

6. **量化后的模型无法再次量化**——需先对全精度模型应用消融法，再对处理后的结果进行量化。

7. **显存占用估算仅为近似值**——虽然4位量化有助于降低显存需求，但在推理过程中峰值显存占用仍可能突然上升。

8. **推理型模型对参数极为敏感**——为保留思维链逻辑，对R1版本模型应使用`surgical`模式。

9. **可参考`obliteratus recommend`的建议**——实时监测数据往往能提供优于默认值的参数设置。

10. **遵循AGPL许可证规定**——严禁在基于MIT或Apache许可的项目中直接`import obliteratus`模块，仅可通过命令行调用。

11. **超大模型（700亿参数及以上）**——为确保保守的默认设置，始终需使用`--large-model`标志。

12. **频谱认证常显示“红色”状态**——即便实际拒绝率为0%，频谱检测也常常会标记为“不完整”。因此不应仅依赖频谱认证结果，而应直接查看真实的拒绝率。
## 辅助技能

- **vllm** — 以高吞吐量提供经过压缩处理的模型
- **gguf** — 将压缩后的模型转换为适用于 llama.cpp 的 GGUF 格式
- **huggingface-tokenizers** — 支持模型分词器的使用
