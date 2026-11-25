---
name: video-frame-analysis
description: Use when you need to inspect a local product demo, screen recording, or app walkthrough video by extracting timestamped frames, building a contact sheet, running OCR, and saving a review bundle for Codex or similar agents.
---

# video-frame-analysis

## Overview

把“本地视频 → ffprobe → 带时间戳抽帧 → contact sheet → OCR → summary.txt / ocr.json 落盘”固化成一个可复用的轻量 skill。

适合给 Codex、Claude Code、OpenCode 这类 agent 处理本地 demo 视频、录屏、竞品页面 walkthrough。

## When to Use

适用于：
- 用户丢来一个本地视频，让你判断产品做到哪一步
- 需要把视频拆成可复查的帧图、OCR 文本、摘要文件
- 需要先做轻量证据提取，再做人工判断或进一步分析
- 想避免每次手拼 ffmpeg / tesseract 命令

不适用于：
- 网络视频下载
- 批量视频队列
- 实时流分析
- GUI 或 Web 平台
- 重型视频理解模型

## Quick Start

```bash
bash scripts/video-frame-analysis.sh /path/to/demo.mp4 ./out/demo-analysis
```

默认输出：
- `ffprobe.txt`
- `frame_*.jpg`
- `contact.png`
- `ocr.txt`
- `ocr.json`
- `summary.txt`

## Installation

推荐直接安装到 Codex / Claude Code / OpenCode：

```bash
npx skills add https://github.com/mason0510/video-frame-analysis-skills -g --all
```

安装后重启 agent 会话，再按需触发本 skill。

## Input / Output

### 输入
- 本地视频路径
- 输出目录路径

### 输出
- 视频元信息
- 带时间戳帧图
- contact sheet
- OCR 文本
- OCR JSON
- 摘要文本

## Config

```bash
FRAME_INTERVAL_SECONDS=5 FRAME_WIDTH=420 OCR_LANG=eng \
  bash scripts/video-frame-analysis.sh ./demo.mp4 ./out/demo
```

| 变量 | 说明 | 默认值 |
|---|---|---|
| `FRAME_INTERVAL_SECONDS` | 抽帧时间间隔（秒） | `8` |
| `FRAME_WIDTH` | 单帧宽度 | `360` |
| `OCR_LANG` | OCR 语言候选 | `chi_sim+eng` |

## Project Files

- `scripts/video-frame-analysis.sh`：主脚本
- `tests/test_video_frame_analysis.sh`：最小闭环测试
- `references/output-format.md`：输出目录说明
- `agents/openai.yaml`：OpenAI/Codex 侧显示信息

## Common Mistakes

- 把它当成重型视频理解模型
- 抽帧过密导致 OCR 噪声暴涨
- 忽略 contact sheet，只盯 OCR 文本
- 没检查本机是否装了 `ffmpeg` / `tesseract`
