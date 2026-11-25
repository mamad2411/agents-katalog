---
name: asr-lychee
description: |
  调 lychee-openapi 的语音识别接口 /open/asr，上传音频文件返回识别文本。
  触发：用户说「转录音频」「把这段音频转文字」「识别这段语音」「ASR」「/asr-lychee」。
  不要用此 skill 做实时流式识别（流式用 WebSocket；本 skill 走 HTTP multipart）。
---

# ASR Lychee

上传本地音频到 lychee OpenAPI，返回语音识别文本。

## 配置

设置环境变量 `LYCHEE_API_KEY`；为了兼容旧配置，未设置时会尝试 `TTS_API_KEY`。

## 用法

```bash
python scripts/asr.py --file /path/to/audio.wav
python scripts/asr.py --file audio.mp3 --language zh-CN --output transcript.txt
python scripts/asr.py --file audio.wav --debug --output result.json
```

## 参数

| 参数 | 必填 | 说明 |
|---|---:|---|
| `--file` | 是 | 音频文件，支持 mp3、wav、m4a |
| `--language` | 否 | 语言代码，如 `zh-CN`、`en-US` |
| `--output` | 否 | 输出文件；默认输出到 stdout |
| `--debug` | 否 | 输出完整 data JSON，而不是纯文本 |
| `--timeout` | 否 | HTTP 超时秒数，默认 60 |

## 文件限制

- 大小不超过 2GB。
- 时长必须在 10 秒至 60 分钟之间。
- 超出限制的文件会被服务端拒绝。

## 输出与错误

默认仅打印识别文本，或将文本写入 `--output` 指定的文件。使用 `--debug` 时输出完整 data JSON。

未设置 API key、文件无效、网络失败或服务端返回错误时，命令会在 stderr 输出可读错误信息。
