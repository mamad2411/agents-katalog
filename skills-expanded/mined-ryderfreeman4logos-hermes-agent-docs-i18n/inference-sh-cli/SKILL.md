---
name: inference-sh-cli
description: Run 150+ AI apps (image, video, LLM) via inference.sh CLI.
version: 1.0.0
author: okaris
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [AI, image-generation, video, LLM, search, inference, FLUX, Veo, Claude]
    related_skills: []
---

# inference.sh 命令行工具

通过简单的命令行界面即可在云端运行150多种AI应用，且无需GPU。

所有命令均通过**终端工具**来执行`infsh`指令。

## 适用场景

- 用户请求生成图像（FLUX、Reve、Seedream、Grok、Gemini图像）
- 用户请求生成视频（Veo、Wan、Seedance、OmniHuman）
- 用户咨询有关inference.sh或infsh的问题
- 用户希望运行AI应用而无需管理各个提供商的API
- 用户需要基于AI的搜索功能（Tavily、Exa）
- 用户需要生成头像或口型同步内容

## 先决条件

必须已安装并完成身份验证`infsh`命令行工具。可通过以下方式进行检查：

```bash
infsh me
```

如果尚未安装：

```bash
curl -fsSL https://cli.inference.sh | sh
infsh login
```

有关完整的设置详情，请参阅 `references/authentication.md` 文件。

## 工作流程

### 1. 始终先进行搜索

切勿凭猜测确定应用名称——务必通过搜索来找到正确的应用 ID：

```bash
infsh app list --search flux
infsh app list --search video
infsh app list --search image
```

### 2. 运行应用

请使用搜索结果中显示的准确应用编号。为获得机器可读取的输出格式，务必使用 `--json` 参数：

```bash
infsh app run <app-id> --input '{"prompt": "your prompt here"}' --json
```

### 3. 解析输出结果

JSON格式的输出中包含生成的媒体文件的URL。可通过`MEDIA:<url>`的格式将这些URL展示给用户，以实现内联显示。

## 常用命令

### 图像生成

```bash
# Search for image apps
infsh app list --search image

# FLUX Dev with LoRA
infsh app run falai/flux-dev-lora --input '{"prompt": "sunset over mountains", "num_images": 1}' --json

# Gemini image generation
infsh app run google/gemini-2-5-flash-image --input '{"prompt": "futuristic city", "num_images": 1}' --json

# Seedream (ByteDance)
infsh app run bytedance/seedream-5-lite --input '{"prompt": "nature scene"}' --json

# Grok Imagine (xAI)
infsh app run xai/grok-imagine-image --input '{"prompt": "abstract art"}' --json
```

### 视频生成

```bash
# Search for video apps
infsh app list --search video

# Veo 3.1 (Google)
infsh app run google/veo-3-1-fast --input '{"prompt": "drone shot of coastline"}' --json

# Seedance (ByteDance)
infsh app run bytedance/seedance-1-5-pro --input '{"prompt": "dancing figure", "resolution": "1080p"}' --json

# Wan 2.5
infsh app run falai/wan-2-5 --input '{"prompt": "person walking through city"}' --json
```

### 本地文件上传

当您提供文件路径时，CLI会自动上传对应的本地文件：

```bash
# Upscale a local image
infsh app run falai/topaz-image-upscaler --input '{"image": "/path/to/photo.jpg", "upscale_factor": 2}' --json

# Image-to-video from local file
infsh app run falai/wan-2-5-i2v --input '{"image": "/path/to/image.png", "prompt": "make it move"}' --json

# Avatar with audio
infsh app run bytedance/omnihuman-1-5 --input '{"audio": "/path/to/audio.mp3", "image": "/path/to/face.jpg"}' --json
```

### 搜索与调研

```bash
infsh app list --search search
infsh app run tavily/tavily-search --input '{"query": "latest AI news"}' --json
infsh app run exa/exa-search --input '{"query": "machine learning papers"}' --json
```

### 其他类别

```bash
# 3D generation
infsh app list --search 3d

# Audio / TTS
infsh app list --search tts

# Twitter/X automation
infsh app list --search twitter
```

## 常见问题

1. **切勿随意猜测应用 ID** —— 请务必先运行 `infsh app list --search <term>`。应用 ID 随时会发生变化，且新应用也会不断添加。
2. **始终使用 `--json` 参数** —— 原始输出格式较难解析。使用 `--json` 参数可获取包含 URL 的结构化输出。
3. **检查认证状态** —— 若命令因认证错误而失败，请运行 `infsh login`，或确认 `INFSH_API_KEY` 已正确设置。
4. **长时间运行的应用** —— 视频生成过程可能需要 30 到 120 秒。终端工具的超时时间应足够长，但仍建议告知用户该过程可能需要一些时间。
5. **输入格式** —— `--input` 参数要求输入 JSON 字符串，请确保正确转义引号。

## 参考文档

- `references/authentication.md` —— 认证设置、登录及 API 密钥相关内容
- `references/app-discovery.md` —— 应用目录的搜索与浏览方法
- `references/running-apps.md` —— 应用运行方式、输入格式及输出处理方法
- `references/cli-reference.md` —— 完整的 CLI 命令参考手册
