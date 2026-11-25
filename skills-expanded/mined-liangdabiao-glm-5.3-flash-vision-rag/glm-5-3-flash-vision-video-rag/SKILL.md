---
name: glm-5.3-flash-vision-video-rag
description: 基于智谱GLM-5.3-Flash视觉大模型的视频理解与问答（video RAG）。当用户提到视频、录像、mp4、监控、游戏录像、影片、动画，并想提问、查找、定位、总结或理解其内容，或问"什么时候发生的"、"某一秒在干什么"、要时间戳定位、片段回放时，使用本skill。支持剧情理解、事件时间线、OCR字幕/HUD识别；回答带 [MM:SS] 时间戳引用，并生成可播放片段与关键帧展示给用户。无音频分析能力。（GLM 版本；DeepSeek 版为 deepseek-v4-flash-vision-video-rag）
---

# GLM-5.3-Flash Vision Video RAG

让 GLM-5.3-Flash 视觉大模型"看懂"一段视频：先按时间轴抽帧阅读、建立索引
（一次性、缓存复用），再对用户问题做 本地粗筛 → 视觉精排 → 深读回答，
回答带 `[MM:SS]` 时间戳引用，并自动切出可播放片段、关键帧和自包含 HTML 预览。

模型没有音频模态——所有理解基于画面（如实告知用户）。
与 DeepSeek 姊妹版同构；差异详见 `references/api-notes.md`。

## 环境要求

- Python：`openai`；**ffmpeg/ffprobe 必须在 PATH**
- API key：环境变量 `GLM_API_KEY` 或 `~/.glm_api_key` 首行（代码不内置密钥）

## 工作流

### 第 1 步：建索引（每份视频一次）

```bash
python scripts/ingest.py "<视频路径>"
```

宏观抽帧密度自适应：≤60s→1fps，≤10min→0.5fps，≤30min→0.25fps，更长→0.1fps
（`--fps` 覆盖）。30s 视频约 20 秒完成。参数：`--force`｜`--limit-frames N`｜`--clean`。

### 第 2 步：提问

```bash
python scripts/ask.py "<视频路径>" "问题"
```

本地粗筛 → 视觉精排 top3 段 → 深读选中段全部帧（effort=high，预算给足）→
带 `[MM:SS]` 引用的回答。**微观层自动触发**：动作类问题（瞄准/击杀/瞬间/轨迹…）
命中时对运动最强时刻抽 12fps 中心放大追加分析；`--micro 00:04-00:07` 强制窗口，
`--no-micro` 禁用。

stdout 分段：答案 / 引用时刻 / 关键帧 / 可播放片段 / 预览（均在 ./video-vision-out/）。

### 第 3 步：展示

优先把 HTML 预览或片段 mp4/关键帧 jpg 路径给用户双击打开；inline 展示只作补充。

```bash
python scripts/show.py "<视频>" --at 00:07          # 该时刻帧
python scripts/show.py "<视频>" --clip 00:05-00:12  # 可播放片段
python scripts/show.py "<视频>" --micro 00:04       # 高帧率放大序列
```

## 回答规范

- 以脚本答案为事实基础，保留 `[MM:SS]` 标记；提醒时间戳是采样估计（±2s）
- 无音频相关问题明确说明；"帧内容不足"时如实转告
- 展示必须给可打开的本地路径

## 注意事项

- 深读/微观 max_tokens 已按"模型始终思考"给足；不要调小（会空回复）
- 排错先读 `references/api-notes.md`
