---
name: live-transcriber
description: 从48.cn直播分享页面提取m3u8流媒体地址、下载视频、语音转文字并生成内容总结。当用户提供48.cn直播链接并要求提取视频、转写文字、分析直播内容时触发。关键词：直播转写、m3u8提取、视频转文字、48直播、口袋48、语音识别、直播总结。支持HLS流媒体下载、Whisper语音识别、自动内容摘要。
allowed-tools: Read, Write, Bash
---

# Live Transcriber - 48.cn 直播视频转写工具

## Overview

从 SNH48/GNZ48 等口袋48直播分享页面，全自动完成：**m3u8提取 → 视频下载 → 语音转文字 → 内容总结**。

## When to Use

当用户：
- 提供 `h5.48.cn` 的直播分享链接，要求提取流媒体/视频
- 要求将48直播视频转为文字或生成字幕
- 要求分析/总结48直播内容
- 提及"直播转写"、"m3u8提取"、"视频转文字"等关键词

## Workflow

### Step 1: 提取 m3u8 流媒体地址

使用浏览器自动化打开直播页面，拦截网络请求获取 m3u8 地址，同时调用内部 API 获取直播详情。

**方式A：浏览器自动化（推荐）**

```bash
# 启动浏览器
agent-browser open "<LIVE_SHARE_URL>"
agent-browser wait 5000

# 从网络请求中过滤 m3u8
agent-browser network requests --filter "m3u8"

# 也可从 video 元素直接获取
agent-browser eval "document.querySelector('video') ? document.querySelector('video').src : 'no video src'"

# 关闭浏览器
agent-browser close
```

**方式B：直接调用 API（更快，需要 liveId）**

从 URL 参数中提取 `id` 字段作为 `liveId`，调用：

```bash
curl -s -X POST 'https://pocketapi.48.cn/live/api/v1/live/getLiveOne' \
  -H 'Content-Type: application/json' \
  -H 'os: android' \
  -d '{"liveId": "<LIVE_ID>"}'
```

返回的 JSON 中 `content.playStreamPath` 即为 m3u8 地址，同时可获取：
- `content.user.userName` - 成员名
- `content.title` - 直播标题
- `content.ctime` - 开始时间戳（毫秒）
- `content.msgFilePath` - 弹幕 LRC 文件
- `content.user.userAvatar` - 头像
- `content.coverPath` - 封面
- `content.onlineNum` - 在线人数

### Step 2: 下载视频

```bash
ffmpeg -i "<M3U8_URL>" -c copy -bsf:a aac_adtstoasc <OUTPUT_DIR>/live_video.mp4 -y
```

视频通常为竖屏 540x960，H.264 + AAC 格式。

### Step 3: 提取音频

```bash
ffmpeg -i <OUTPUT_DIR>/live_video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 <OUTPUT_DIR>/audio.wav -y
```

输出 16kHz 单声道 WAV，适配 Whisper 输入要求。

### Step 4: 语音转文字

**依赖安装（首次运行）：**

```bash
# 检查并安装 faster-whisper
python3.11 -c "from faster_whisper import WhisperModel" 2>/dev/null || pip3.11 install faster-whisper
```

**执行转写：**

使用 `<skill-directory>/scripts/transcribe.py`：

```bash
python3.11 <skill-directory>/scripts/transcribe.py \
  --input <OUTPUT_DIR>/audio.wav \
  --output-dir <OUTPUT_DIR> \
  --model base \
  --language zh
```

参数说明：
- `--model`: 可选 tiny/base/small/medium/large-v2，推荐 base（速度与精度平衡）
- `--language`: 语言代码，中文为 zh
- `--beam-size`: 解码宽度，默认 3
- `--vad`: 启用 VAD 过滤静音，默认开启

输出文件：
- `transcript.json` - 结构化 JSON（含时间戳）
- `transcript.txt` - 带时间戳的纯文本

### Step 5: 生成内容总结

基于转写文本，生成结构化总结报告，包含：

1. **直播基本信息表格**（成员、标题、时间、时长等）
2. **分段内容总结**（按时间段划分，每段概括核心话题）
3. **关键话题一览表**
4. **重要时间节点**（如提到的公演日期、生日等）
5. **转写说明与术语修正**

输出为 Markdown 格式，保存至用户工作目录。

### Step 6: 清理临时文件

视频和音频文件通常较大，完成转写后应提醒用户是否需要清理：

```bash
# 可选：清理大文件
rm -f <OUTPUT_DIR>/live_video.mp4 <OUTPUT_DIR>/audio.wav
```

保留最终输出：
- `snh48_live_summary.md` - 内容总结
- `snh48_transcript.txt` - 完整转写
- `snh48_live_analysis.md` - 流媒体技术分析（可选）

## Resources

### scripts/

- `transcribe.py` - 基于 faster-whisper 的语音转写脚本，支持参数化配置

### references/

- `api_reference.md` - 48.cn 口袋 API 接口参考文档

### assets/

无

## Notes

- 长视频（>60分钟）下载约需 1-2 分钟，转写约需 2-5 分钟（取决于模型大小）
- base 模型对中文口语识别有一定误差，专有名词（人名、术语）可能不准确，需人工校验
- m3u8 地址有时效性，直播回放可能随时下线，建议尽快下载
- ffmpeg 和 faster-whisper 需预先安装，首次使用会自动检测
