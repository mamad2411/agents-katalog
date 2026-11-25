---
name: deepseek-v4-flash-vision-video-rag
description: 基于DeepSeek视觉大模型（deepseek-v4-flash-vision-exp）的视频理解与问答（video RAG）。当用户提到视频、录像、mp4、监控、游戏录像、影片、动画，并想提问、查找、定位、总结或理解其内容，或问"什么时候发生的""某一秒在干什么"、要时间戳定位、片段回放时，使用本skill。支持剧情理解、事件时间线、OCR字幕/HUD识别；回答带 [MM:SS] 时间戳引用，并生成可播放片段与关键帧展示给用户。无音频分析能力。
---

# DeepSeek V4-Flash Vision Video RAG

让视觉大模型"看懂"一段视频：先把视频按时间轴抽帧阅读、建立索引（一次性、缓存
复用），再对用户问题做 本地粗筛 → 视觉精排 → 深读回答，回答带 `[MM:SS]` 时间戳
引用，并自动切出可播放片段、关键帧和自包含 HTML 预览。

模型没有音频模态——所有理解基于画面；音频轨会被忽略（如实告知用户）。

## 环境要求

- Python 依赖：`openai`（本机已装）
- **ffmpeg / ffprobe 必须在 PATH**（本机已装；缺了先安装）
- API key：从环境变量 `DEEPSEEK_API_KEY` 或本机 `~/.deepseek_api_key` 文件（首行）读取，
  代码中不内置任何密钥；缺失时报错并给出设置指引
- 脚本在 `scripts/` 下，Windows 直接 `python scripts/xxx.py`

## 工作流

### 第 1 步：建立索引（每份视频一次，之后走缓存）

```bash
python scripts/ingest.py "<视频路径>"
```

- ffprobe 元数据 → 宏观抽帧（≤60s→1fps，≤10min→0.5fps，≤30min→0.25fps，更长→0.1fps，
  `--fps` 可覆盖）→ Files API 上传 → 25 帧/批视觉卡片 → 段聚合（30s/段）→ 本地场景切换检测
- 30s 视频约 30 秒完成；重复运行直接命中缓存
- 常用参数：`--force` 重建｜`--limit-frames N` 先试前 N 帧｜`--clean` 清缓存
- 输出打印帧卡片数/段数/场景切换/运动统计，可据此向用户简报视频概况

### 第 2 步：回答用户问题

```bash
python scripts/ask.py "<视频路径>" "用户的问题"
```

- 本地粗筛（TF-IDF，零费用）→ 视觉精排选 top3 段（1 次调用，关推理）→ 深读选中段
  全部帧（1 次调用，开推理，max_tokens=32768）→ 带 `[MM:SS]` 引用的回答
- **微观层自动触发**：问题含动作类词（瞄准/击杀/瞬间/轨迹…）且深读有引用时，
  对运动最强的引用时刻抽 12fps 中心放大帧追加一次分析（+1 次调用）；
  `--micro 00:04-00:07` 强制指定窗口，`--no-micro` 禁用

stdout 分段：`=== 答案 ===`、`=== 引用时刻 ===`、`=== 关键帧 ===`、
`=== 可播放片段 ===`（均为 `./video-vision-out/` 下文件）、`=== 预览 ===`。

### 第 3 步：向用户展示（必须做）

终端里用户未必能看到 inline 图片/视频，必须给出可自行打开的路径，按优先级：

1. **HTML 预览（首选）**：`./video-vision-out/<视频名>_<问题>.html` —— 自包含单文件，
   答案 + 引用时刻的**可播放片段**（base64 内嵌 `<video>`）+ 关键帧，双击浏览器打开。
   Windows 下可代用户执行 `start "<路径>"`
2. **单独的片段 mp4 / 关键帧 jpg 路径**：用户只要某个时刻时逐个给出
3. 支持 inline 的环境可再 Read 图片作补充，但不得只依赖它

用户想直接看某个时刻/片段：

```bash
python scripts/show.py "<视频路径>" --at 00:07          # 该时刻帧
python scripts/show.py "<视频路径>" --clip 00:05-00:12  # 可播放片段
python scripts/show.py "<视频路径>" --micro 00:04       # 12fps 中心放大帧序列
```

## 回答规范

- 以脚本产出的答案为事实基础，保留 `[MM:SS]` 时间戳引用标记
- 时刻引用是 1fps 采样的估计值（误差 ±2s），涉及精确时机时提醒用户以片段回放为准
- 答案说"帧内容不足"时如实转告，不要编造；音频相关请求明确说明无音频能力
- 展示时必须给 HTML 预览或媒体文件路径，不能只靠 inline 展示

## 注意事项

- 首次 ingest 慢是正常的；之后每次提问 2~3 次调用
- 深读/微观用 max_tokens=32768（开推理时 reasoning 计入预算，小了会得到空回复）
- 视频抽帧与采样依据实测最佳实践（GIF 不可用、两级采样、detail=low 禁用等），
  详见 `references/video-sampling.md`；索引结构见 `references/index-schema.md`
- 改 `scripts/ds_client.py` 前先读 `references/video-sampling.md` 的踩坑清单
