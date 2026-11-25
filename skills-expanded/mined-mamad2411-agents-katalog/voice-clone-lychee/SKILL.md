---
name: voice-clone-lychee
description: |
  调 lychee-openapi 的语音克隆接口 /open/voice/zeroshot/clone，上传参考音频生成克隆音色。
  触发：用户说「克隆这个声音」「用这个声音合成」「/voice-clone」「训练音色」。
---

# Voice Clone Lychee

上传一段参考音频，通过 lychee OpenAPI 生成可供后续语音合成使用的克隆音色。

## 配置

设置环境变量 `LYCHEE_API_KEY`；未设置时兼容读取 `TTS_API_KEY`。

## 用法

```bash
python scripts/clone.py --file reference.wav
python scripts/clone.py --file voice.mp3 --carry-back "project-001"
python scripts/clone.py --file sample.m4a --output clone-result.json --timeout 180
```

## 参数

| 参数 | 必填 | 说明 |
|---|---:|---|
| `--file` | 是 | 参考音频，支持 wav、mp3、m4a |
| `--carry-back` | 否 | 服务端原样透传的字符串，最多 500 字符 |
| `--timeout` | 否 | HTTP 超时秒数，默认 120 |
| `--output` | 否 | 将服务端完整 JSON 响应写入文件 |

## 参考音频限制

- 格式：wav、mp3、m4a。
- 大小：不超过 10MB。
- 时长：1–30 秒。
- 非 wav 文件会由服务端通过 ffmpeg 转换为 wav。

## 重要：后续合成使用 request_id

克隆接口响应中的 `speaker_id` 始终为 `null`。请使用成功响应的 `request_id` 作为后续 voice-infer 接口的 `speaker_id`。

成功时命令行输出：

```json
{"success": true, "request_id": "<uuid>", "carry_back": "<透传值>"}
```
