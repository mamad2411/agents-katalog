---
name: glm-ecom-video-seedance-prompt
description: 带货视频反向拆解与 Seedance（即梦）复刻提示词生成（GLM-5.3-Flash 引擎）。当用户提供带货/电商/广告/商销/种草/千川视频，或提到即梦、Seedance、文生视频、复刻爆款、拆解视频、提示词，想分析镜头、复刻效果、生成视频提示词时，使用本skill。自动产出镜头级分镜表（景别/运镜/光影/动作时序/卖点）和符合 S-A-C-S-C 编导规范的完整提示词包（分镜头提示词+基础参数+负面词+@参考图清单），支持忠实复刻/自然流/付费流三种风格。（GLM 版本；DeepSeek 版为 ecom-video-seedance-prompt）
---

# GLM 带货视频 → Seedance Prompt

看懂一条带货视频，翻译成可复刻的 Seedance 提示词。GLM-5.3-Flash 版本，
方法论知识库与 DeepSeek 版共用（`references/seedance-knowledge.md`，
来自 `D:\PageIndex-deepseek\带货视频\` 六篇实战文档的蒸馏）。

## 环境要求

- Python：`openai`；**ffmpeg/ffprobe 必须在 PATH**
- API key：环境变量 `GLM_API_KEY` 或 `~/.glm_api_key` 首行（代码不内置密钥）

## 工作流

### 第 1 步：拆解（每份视频一次）

```bash
python scripts/analyze.py "<带货视频路径>"
```

**双通道自动选择**：
- **直传通道**（默认优先）：≤40MB 且 ≤120s 的视频整段传给 GLM，单次调用产出全部
  镜头卡+全局分析——模型看连续运动，动作时序更真实，成本约帧方式的 1/5；
  >20MB 自动先转码瘦身。镜头时间边界为模型估计值（不要求精确）
- **抽帧兜底**：超限或直传失败自动回落（ffmpeg 场景切换切分+逐镜头帧分析，
  细节颗粒度更细）；`--force-frames` 可强制走此路径

10 秒视频：直传 26 秒完成；抽帧兜底约 42 秒。参数：`--force`｜`--min-shot 0.8`｜`--clean`。

### 第 2 步：生成复刻提示词

```bash
python scripts/replicate.py "<视频路径>"                          # 忠实复刻
python scripts/replicate.py "<视频路径>" --style organic          # 自然流种草版
python scripts/replicate.py "<视频路径>" --style paid              # 付费流千川版
python scripts/replicate.py "<视频路径>" --product "品牌，卖点，色号"  # 产品信息以此为准
```

产出在 `./seedance-out/`：分镜头提示词 + 完整版 + 负面词中英 + @参考图清单 +
差异说明 + 升级建议（markdown + 自包含 HTML，每镜头提示词配原片关键帧）。

### 第 3 步：交付

1. HTML 预览路径给用户双击——逐镜头"提示词 vs 原片关键帧"对照检查
2. 完整版提示词直接可粘贴即梦；提醒按 @参考图清单备料（真人照片需打码过审）
3. 单镜头不满意用 `--shot B` 重出；换风格/产品信息重跑 generate（拆解走缓存）
4. 模型无音频能力：口播是从字幕推断的，向用户注明

## 注意事项

- 生成 effort=high 且 max_tokens=32768 已按"模型始终思考"调好，勿改小
- 编导规则改动前先读 `references/seedance-knowledge.md`
