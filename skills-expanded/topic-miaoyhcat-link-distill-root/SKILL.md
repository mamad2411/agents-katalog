---
name: link-distill
description: >
  AI视频分析工具：扔链接，自动转录、总结、提取结构化知识。
  支持1200+平台（B站、抖音、YouTube、小红书…）。
  任何AI Agent都能用（Claude Code、Codex、ZCode、OpenClaw、Cursor）。
  关键词：视频转文字、内容蒸馏、知识提取、AI Agent技能。
---

# link-distill — 和 AI 一起从视频中学

用户给你视频链接时，你做三件事：**跑 link-distill → 读结果 → 跟用户聊**

## 0. 首次使用：装依赖

```bash
cd <link-distill目录>
pip install yt-dlp openai-whisper torch funasr
# 确保 ffmpeg 已安装（winget install ffmpeg）
```

## 1. 跑 link-distill

```bash
python link-distill.py "<用户给的链接>"
```

会自动：
- 下载音频 → FunASR/Whisper 转文字
- （可选 --vision）场景检测 + 视觉分析
- DeepSeek AI 结构化蒸馏

输出保存到 `last_analysis.json`，同时打印到终端。

## 2. 读结果

输出结构：
- 📌 核心主题 — 一句话概括
- 📝 校正全文 — 纠错后的文本
- 🧠 思维模型/框架 — 可迁移的思考结构
- 📏 原则/规则 — 可以直接用的判断标准
- 📖 案例 — 实际操作经验
- ⚠️ 边界/注意 — 容易翻车的地方
- 💡 可执行步骤 — 能照着做的

## 3. 跟用户聊

不要只丢文本。主动分析、提问、联系已有知识。

好的交流方式：
- 先给一个一句话概括
- 再问用户想深入了解哪个点
- 或者直接提出你的观察和疑问

## 可选参数

| 参数 | 用途 | 需要 |
|:-----|:-----|:------|
| `--vision` | 分析画面内容 | `ollama pull llava:7b` |
| `--note` | 抖音图文模式 | `pip install playwright` |
| `--json` | JSON 格式输出 | 无 |

## 原理

```
链接 → yt-dlp（1200+站）→ 音频 → FunASR/Whisper → DeepSeek AI → 结构化分析 → 你俩聊
```
