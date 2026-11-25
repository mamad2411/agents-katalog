---
name: read-image
description: >
  Read and analyze images using a vision-capable model. Supports custom focus: user can specify
  what to focus on (layout, code, errors, data, etc.) via prompt parameter. Use when the user
  asks to read, describe, analyze, or transcribe content from an image file (PNG, JPG, GIF, WebP,
  BMP, TIFF). Trigger keywords: read image, describe image, analyze image, what's in this image,
  look at this, 读图, 看图, 分析图片, 描述图片, 截图, 图片内容, 关注排版, 重点看.
---

# Read Image — Vision Model Bridge

Your current model does not support image input. Use this skill to analyze images by calling
a vision-capable model (mimo-v2.5) via the Anthropic API.

## When to Use

- User asks you to read, describe, or analyze an image file
- User shares a screenshot or photo path
- User asks about visual content (diagrams, charts, UI screenshots, code screenshots)
- Any task requiring image understanding

## How to Use

### Step 1: Locate the image

Find the image file path. It may be:
- Provided directly by the user
- Referenced in the conversation
- A screenshot in a temp directory
- Referenced in code or config

If the path is unclear, ask the user.

### Step 2: Call the vision model

Run this command in Bash:

```bash
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "<IMAGE_PATH>" "<YOUR_PROMPT>"
```

**Parameters:**
- `<IMAGE_PATH>` — Absolute path to the image file
- `<YOUR_PROMPT>` — **可选**。告诉视觉模型你更关注什么。省略则使用默认的全面描述。

**自定义关注点示例：**
```bash
# 关注排版布局
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "xxx.png" "重点分析这张图的排版布局，包括对齐方式、间距、层次结构。"

# 关注代码内容
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "xxx.png" "完整转录图中的所有代码，保持原始格式。"

# 关注错误信息
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "xxx.png" "提取图中所有错误信息和堆栈跟踪。"

# 关注图表数据
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "xxx.png" "提取图表中的所有数据点、坐标轴标签和图例。"
```

### Step 3: Use the result

The script outputs the vision model's analysis as plain text. Use it to:
- Answer the user's question about the image
- Transcribe code or text from screenshots
- Describe diagrams and visual content
- Debug UI issues from screenshots

## Example Usage

```bash
# Read a screenshot
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "/tmp/screenshot.png" "What error message is shown?"

# Analyze a diagram
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "/path/to/diagram.jpg" "Describe the architecture shown in this diagram."

# Transcribe code from image
VISION_MODEL="mimo-v2.5" bash ~/.claude/skills/read-image/read-image.sh "/path/to/code.png" "Transcribe all the code in this image exactly as written."
```

## Supported Formats

JPG, JPEG, PNG, GIF, WebP, BMP, TIFF

## Troubleshooting

- **"File not found"** — Check the path. Use absolute paths.
- **"Unsupported image format"** — Convert to PNG or JPG first.
- **API error** — Check `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_BASE_URL` are set.
- **Timeout** — Large images may take longer. The script has a 120s timeout.
- **Empty response** — The image may be too large. Try resizing to under 5MB.

## Notes

- The vision model is `mimo-v2.5` (set via `VISION_MODEL` env var)
- Your main model (`mimo-v2.5-pro`) remains unchanged for all other tasks
- Max response length: 4096 tokens
- The script uses your existing Anthropic API credentials from settings
