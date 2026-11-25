---
name: apiz
description: API 网关服务，提供数百种 AI 模型的访问（包括图像生成、视频生成、音频处理、对话等）。使用 apiz CLI 进行模型查询、文档查看和生成任务提交。当用户需要生成图片/视频/音频、查询 AI 模型、语音合成、语音克隆、音乐生成、视频解析、字幕制作、或使用 apiz AI 网关时触发。
---

# Apiz CLI 完全参考

## 全局参数

所有命令共享以下全局 flags：

| Flag | 环境变量 | 说明 |
|------|---------|------|
| `--api-key` | `APIZ_API_KEY` | Bearer token (sk-...) |
| `--base-url` | `APIZ_BASE_URL` | 后端地址（默认 https://api.apiz.ai） |
| `--timeout` | `APIZ_TIMEOUT` | 请求超时（如 30s, 2m） |
| `--max-retries` | | 重试次数（默认 2） |
| `--profile` | | 配置文件名 |
| `--config` | | 配置文件路径覆盖 |
| `--json` | | JSON 输出 |
| `--yaml` | | YAML 输出 |
| `--table` | | 表格输出 |

## 所有命令速查

| 命令 | 功能 | 是否需要 API Key |
|------|------|:---:|
| `apiz auth login --api-key <key>` | 登录 | 否（写入配置） |
| `apiz account balance` | 查余额 | 是 |
| `apiz account checkin` | 每日签到（随机 50-150 积分） | 是 |
| `apiz models list --category <cat>` | 列出模型（image/video/audio） | 否 |
| `apiz models info <id> --lang zh` | 模型元数据 + 参数 schema | 否 |
| `apiz models docs <id> --lang zh` | 模型文档教程 | 否 |
| `apiz generate <prompt> --model <id>` | 提交生成任务 | 是 |
| `apiz tasks get <task-id>` | 查询任务状态 | 是 |
| `apiz tasks wait <task-id>` | 等待任务完成 | 是 |
| `apiz voices list` | 列出可用音色 | 是 |
| `apiz speak <text> --voice <id>` | 语音合成（TTS） | 是 |
| `apiz align <text> --audio <url>` | 强制对齐（字幕打轴） | 是 |
| `apiz parse <share-url>` | 视频链接解析（去水印） | 否 |
| `apiz transfer <url> --type <type>` | URL 镜像到 apiz CDN | 否 |
| `apiz upload <file>` | 上传本地文件到 CDN | 是 |

## generate 生成命令详解

```bash
apiz generate "<prompt>" [flags]
```

### 全部参数

| 参数 | 类型 | 说明 | 适用场景 |
|------|------|------|---------|
| `--model` | string | **必填**。模型 ID | 全部 |
| `--wait` | bool | 阻塞等待任务完成 | 全部 |
| `--wait-timeout` | duration | 等待超时（默认 10m） | 全部 |
| `--interval` | duration | 轮询间隔（默认 5s，配合 --wait） | 全部 |
| `--json` | bool | JSON 输出 | 全部 |
| `--aspect-ratio` | string | 画面比例（16:9, 9:16, 1:1, 4:3, 3:2） | 图片/视频 |
| `--image-size` | string | 图片尺寸（square_hd, landscape_16_9, portrait_4_3） | 图片 |
| `--image-url` | string | 输入图片/音频/视频 URL | 图生图/图生视频/音频识别 |
| `--duration` | string | 视频时长（秒） | 视频 |
| `--params` | string | 额外 JSON 参数，合并到请求中 | 全部 |

> `--image-url` 用于多种输入场景：图生图、图生视频、声音克隆（输入音频样本）、语音识别（输入音频文件）。`--params` 可传入任意额外的模型参数，会与标准参数合并。

### 输出格式

成功时返回：
```json
{
  "task_id": "xxx",
  "status": "completed",
  "model": "openai/gpt-image-2",
  "result": {
    "images": [{
      "url": "https://cdn-hk.51sux.com/...",
      "content_type": "image/png",
      "width": 1122,
      "height": 1402
    }]
  },
  "price": 64,
  "created_at": "2026-07-30 19:28:30",
  "completed_at": "2026-07-30 19:29:15"
}
```

视频结果中 `result` 可能包含 `video` 字段替代 `images`。失败时 `status` 为 `"failed"` 且携带 `error` 字段。

## 完整命令参考

### 1. 安装与登录

```bash
# 安装 CLI
curl -fsSL https://apiz.ai/cli | sh

# 写入 API Key 到配置文件
apiz auth login --api-key "sk-xxx"

# 配置文件位置：~/.config/apiz/config.toml
```

API Key 优先级：`--api-key` 参数 > `APIZ_API_KEY` 环境变量 > `XSKILL_API_KEY` 环境变量 > 配置文件

### 2. 模型查询

```bash
# 按分类列出可用模型
apiz models list --category image --json
apiz models list --category video --json
apiz models list --category audio --json

# 查看模型详情（含参数 schema）
apiz models info image4.0 --lang zh --json

# 查看模型使用教程
apiz models docs image4.0 --lang zh
```

模型列表字段含义：
- `id` — 模型 ID（用于 generate 的 `--model`）
- `name` — 中文名称
- `category` — 分类（image/video/audio）
- `capability` — 能力描述
- `stats.success_rate` — 历史成功率
- `stats.pending_tasks` — 排队任务数
- `stats.processing_tasks` — 处理中任务数
- `isHot` — 热门模型标记
- `pricing` — 价格信息

`models info` 还会返回：
- `description` — 模型详细描述
- `params_schema` — 模型支持的参数 schema
- `channel` — 执行通道

### 3. 图片生成

```bash
# 基础文生图
apiz generate "一只可爱的猫" --model image4.0 --wait --json

# 指定画面比例
apiz generate "山峰日落，4K 画质" --model openai/gpt-image-2 --aspect-ratio "16:9" --wait --json

# 图片编辑（提供输入图片 + 修改描述）
apiz generate "把背景换成沙滩，保留人物" --model openai/gpt-image-2/edit --image-url "https://..." --wait --json

# ChatGPT Images 2.0 高质量生成（成功率 ~97%）
apiz generate "赛博朋克风格的城市夜景" --model openai/gpt-image-2 --wait --json

# Nano Banana Pro（Google 高级版）
apiz generate "水墨风格的山水画" --model fal-ai/nano-banana-pro --wait --json
```

### 4. 视频生成

```bash
# 文生视频
apiz generate "一只金毛在沙滩上奔跑" --model st-ai/super-seed2-lite --wait --json
apiz generate "日落时分的城市延时摄影" --model fal-ai/kling-video/v3/pro/text-to-video --wait --json

# 图生视频
apiz generate "让这张图片的场景动起来，微风吹过" --model fal-ai/kling-video/v3/pro/image-to-video --image-url "https://..." --wait --json

# 多图参考视频
apiz generate "参考这些图片的风格和构图生成视频" --model apiz/veo3.1/reference-to-video --wait --json

# 动作迁移（参考视频的动作应用到目标）
apiz generate "按参考视频的动作生成" --model fal-ai/kling-video/v3/standard/motion-control --image-url "https://..." --wait --json

# Kling O3 Pro 图生视频（成功率 100%）
apiz generate "让照片变成生动的短视频" --model fal-ai/kling-video/o3/pro/image-to-video --image-url "https://..." --wait --json

# Sora 2 文生视频（OpenAI）
apiz generate "科幻风格的太空站内部" --model apiz/sora-2/text-to-video --wait --json

# Veo 3.1 文生视频（Google 快速版）
apiz generate "野生动物纪录片风格的画面" --model apiz/veo3.1/fast/text-to-video --wait --json
```

### 5. 视频处理

```bash
# 解析视频分享链接 -> 获取无水印下载地址 (免费)
apiz parse "https://www.douyin.com/video/xxx"

# 返回: platform, title, video_url, cover_url, duration

# URL 镜像到 apiz CDN (免费)
apiz transfer "https://example.com/video.mp4" --type image

# 返回: original_url, cdn_url, type, size_bytes

# 火山 VOD 精细化字幕擦除
apiz generate "" --model volcengine/vod/subtitle-erase --image-url "<视频url>" --wait --json
```

### 6. 语音合成 (TTS)

```bash
# 列出可用音色
apiz voices list --json

# 语音合成（默认音色）
apiz speak "你好，欢迎使用AI语音合成服务" --json

# 指定音色
apiz speak "今天天气真不错" --voice "<voice-id>" --json

# 指定语速 + 模型
apiz speak "这是一条测试语音" --voice "<voice-id>" --speed 1.2 --model "speech-2.8-hd" --json

# 保存到本地文件
apiz speak "保存这段语音到文件" --output-file "output.mp3"

# TTS 模型选项：
# speech-2.8-hd     - 高清语音（默认）
# speech-2.8-turbo  - 快速语音
# speech-2.6-hd     - 高清语音 v2.6
# speech-2.6-turbo  - 快速语音 v2.6

# 语音设计（创建自定义音色）- 通过 SDK 支持
# SDK: client.voices.design({ prompt: "年轻女性，温柔语气" })

# 声音克隆（基于音频样本）
# CLI: 使用 apiz generate --model minimax/voice-clone --image-url "<样本音频url>"
```

### 7. 强制对齐 / 字幕打轴

```bash
# 说话字幕对齐
apiz align "如果您没有其他需要举报的话..." \
  --audio "https://example.com/talk.mp3" \
  --mode speech --json

# 唱歌字幕对齐
apiz align "曾经真的以为人生就这样了" \
  --audio "https://example.com/song.mp3" \
  --mode singing --json

# 保存结果到文件
apiz align "文本内容" \
  --audio "https://example.com/audio.mp3" \
  --mode speech \
  --output-file "result.json"

# 对齐参数
# --mode        : speech (默认) | singing
# --punct-mode  : 0 (=> 1), 1, 2, 3
# --interval    : 轮询间隔（默认 2s）
# --wait-timeout: 超时（默认 5m）

# 返回结构
# {
#   "duration": 120.5,
#   "utterances": [{
#     "text": "句子文本",
#     "start_time": 1000,
#     "end_time": 3000,
#     "words": [{
#       "text": "词",
#       "start_time": 1000,
#       "end_time": 1200
#     }]
#   }]
# }
```

### 8. 音频识别与音乐生成

```bash
# 语音识别（录音文件转文字）
apiz generate "" --model volcengine/speech-to-text/bigmodel-v2 --image-url "<音频文件url>" --wait --json

# 音乐生成
apiz generate "一首轻快的钢琴曲，温暖治愈风格" --model minimax/music-gen --wait --json
apiz generate "电子舞曲，节奏感强，适合运动" --model minimax/music-gen --wait --json
```

### 9. 文件上传

```bash
# 上传本地文件到 apiz CDN
apiz upload "./image.png"
apiz upload "./audio.mp3" --folder "my-uploads" --remark "demo"

# 上传参数
# --folder       : 存储文件夹（默认 cli-uploads）
# --content-type : MIME 类型（自动检测）
# --remark       : 备注
# --uploader     : 上传者标签

# 返回：public_url, file_key, file_name, file_size, content_type
```

### 10. 任务管理

```bash
# 查询任务状态
apiz tasks get "task-id-xxx"

# 等待任务完成
apiz tasks wait "task-id-xxx" --interval 3s --wait-timeout 5m

# 任务状态：
# pending    - 排队中
# processing - 处理中
# completed  - 已完成
# failed     - 失败（含 error 信息）

# TaskResponse 完整结构：
# {
#   "task_id": "xxx",
#   "status": "pending|processing|completed|failed",
#   "channel": "api",
#   "model": "model-id",
#   "progress": 0.5,
#   "result": { ... },
#   "queue_info": { ... },
#   "error": "错误信息",
#   "price": 64,
#   "created_at": "2026-07-30 19:28:30",
#   "completed_at": "2026-07-30 19:29:15"
# }
```

### 11. 账户管理

```bash
# 查余额
apiz account balance

# 每日签到（随机 50-150 积分，每天一次，幂等）
apiz account checkin
```

## 模型参考

### 图片生成模型（6 个）

| 模型 ID | 名称 | 成功率 | 说明 |
|---------|------|:------:|------|
| `image4.0` | Image 4.0 | — | 通用图片生成 |
| `openai/gpt-image-2` | ChatGPT Images 2.0 | ~97% | OpenAI 高质量文生图 |
| `openai/gpt-image-2/edit` | ChatGPT Images 2.0 Edit | ~93% | 图片编辑，需 `--image-url` |
| `fal-ai/nano-banana-2` | Nano Banana 2 | 100% | Google 文生图 v2 |
| `fal-ai/nano-banana-pro` | Nano Banana Pro | ~94% | Google 高级文生图 |
| `kapon/gemini-3-pro-image-preview` | Gemini 3 Pro Image Preview | ~52% | Gemini 3 Pro 预览版 |

### 视频生成模型（24 个）

**Kling 系列（快手可灵，fal.ai）**

| 模型 ID | 成功率 |
|---------|:------:|
| `fal-ai/kling-video/o3/pro/image-to-video` | 100% |
| `fal-ai/kling-video/v3/standard/text-to-video` | 100% |
| `fal-ai/kling-video/v3/pro/text-to-video` | 100% |
| `fal-ai/kling-video/v2.6/standard/motion-control` | 100% |
| `fal-ai/kling-video/o3/pro/reference-to-video` | ~97% |
| `fal-ai/kling-video/o3/standard/reference-to-video` | ~94% |
| `fal-ai/kling-video/v3/standard/image-to-video` | ~94% |
| `fal-ai/kling-video/v3/pro/image-to-video` | ~92% |
| `fal-ai/kling-video/v3/pro/motion-control` | ~82% |
| `fal-ai/kling-video/o3/standard/image-to-video` | ~75% |
| `fal-ai/kling-video/v3/standard/motion-control` | ~69% |

**Seedance / Super Seed 系列（火山引擎）**

| 模型 ID | 成功率 | 备注 |
|---------|:------:|------|
| `st-ai/super-seed2-lite` | ~52% | 🔥热门，轻量版 |
| `st-ai/super-seed2` | — | 🔥热门，全能模型 |
| `ark/seedance-2.0` | ~19% | 🔥热门 |

**Grok Imagine Video 系列（xAI）**

| 模型 ID | 成功率 |
|---------|:------:|
| `xai/grok-imagine-video-1.5/text-to-video` | 100% |
| `xai/grok-imagine-video-1.5/reference-to-video` | 100% |
| `xai/grok-imagine-video-1.5/image-to-video` | ~57% |

**Sora 2 系列（OpenAI，APIZ 代理）**

| 模型 ID | 能力 |
|---------|------|
| `apiz/sora-2/text-to-video` | 文生视频 |
| `apiz/sora-2/image-to-video` | 图生视频 |

**Veo 3.1 系列（Google，APIZ 代理）**

| 模型 ID | 成功率 |
|---------|:------:|
| `apiz/veo3.1/image-to-video` | ~70% |
| `apiz/veo3.1/text-to-video` | — |
| `apiz/veo3.1/reference-to-video` | — |
| `apiz/veo3.1/fast/text-to-video` | — 快速版 |

**其他**

| 模型 ID | 能力 |
|---------|------|
| `volcengine/vod/subtitle-erase` | 火山 VOD 精细化字幕擦除 |

### 音频模型（7 个）

| 模型 ID | 名称 | 能力 |
|---------|------|------|
| `minimax/t2a` | 海螺语音合成 | 文字转语音，100% |
| `minimax/voice-design` | 海螺语音设计 | 自定义音色（SDK） |
| `minimax/voice-clone` | 海螺声音克隆 | 基于样本克隆，100% |
| `minimax/music-gen` | 海螺音乐生成 | AI 作曲 |
| `volcengine/speech-to-text/bigmodel-v2` | 火山录音文件识别 | 语音转文字 |
| `volcengine/captioning/ata-speech` | 火山字幕打轴(说话) | 说话字幕 |
| `volcengine/captioning/ata-singing` | 火山字幕打轴(唱歌) | 唱歌字幕 |

## API 兼容模式

apiz 提供 OpenAI 兼容的 `/v1/chat/completions` 接口：

```python
from openai import OpenAI
client = OpenAI(
    base_url="https://api.apiz.ai/v1",
    api_key="sk-xxx"
)
# 可调用数百种对话模型
response = client.chat.completions.create(
    model="openai/gpt-5.6",
    messages=[{"role": "user", "content": "hello"}]
)
```

可用对话模型通过 `GET https://api.apiz.ai/v1/models` 查询，包含 GPT、Claude、Gemini、Qwen、DeepSeek 等数百种。

## SDK 方式

apiz 提供官方 SDK：TypeScript (`npm install apiz-sdk`)、Python (`pip install apiz`)。

```python
from apiz import Apiz
client = Apiz(api_key="sk-xxx")

# 生成（参数通过 params 字典传入）
result = client.generate(
    model="image4.0",
    params={"prompt": "a cat", "aspect_ratio": "16:9"},
)

# 语音合成（返回 audio_url / duration）
result = client.speak("你好", voice_id="xxx")

# 强制对齐（返回字级时间戳）
result = client.align(
    audio_url="https://...",
    audio_text="歌词文本",
    mode="singing",
)

# 查看余额
balance = client.account.balance()
```

完整 SDK 方法映射见 [references/sdk-api-reference.md](references/sdk-api-reference.md)。

## MCP Server

apiz 提供 MCP Server 可在 Cursor / Claude Desktop 中使用：

```json
{
  "mcpServers": {
    "apiz": {
      "command": "npx",
      "args": ["-y", "apiz-mcp"],
      "env": { "APIZ_API_KEY": "sk-..." }
    }
  }
}
```

提供 9 个工具：`generate`, `get_result`, `search_models`, `guide`, `account`, `speak`, `align`, `parse_video`, `transfer_url`。完整说明见 [references/mcp-server.md](references/mcp-server.md)。
