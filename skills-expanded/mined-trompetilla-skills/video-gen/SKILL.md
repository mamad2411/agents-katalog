---
name: video-gen
description: Generate videos using Tencent Cloud VOD AIGC models (Kling, Vidu, Hailuo, etc.). Updated with full API support.
---

# Video Generation Skill (VOD AIGC)

This skill generates high-quality AI videos using Tencent Cloud VOD AIGC API.
It supports **Text-to-Video (T2V)** and **Image-to-Video (I2V)** across multiple models.

## Supported Models
- **Kling** (1.6, 2.0, 2.1, 2.5, 2.6, o1)
- **Hailuo** (02, 2.3)
- **Vidu** (q2, q2-turbo, q2-pro)
- **Jimeng** (3.0pro)
- **Seedance** (1.0-pro, 1.5-pro, etc.)
- **GV** (3.1)
- **OS** (2.0)

## Usage

```bash
node skills/video-gen/index.js "<Prompt>" [options]
```

### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--model <name>` | Model name (Kling, Hailuo, Vidu, etc.) | Kling |
| `--model-version <ver>` | Model version (e.g. 2.1, 2.5) | 2.5 |
| `--image <url>` | Reference image URL for I2V | None |
| `--last-frame <url>` | Last frame image URL (Kling 2.1, Vidu, GV) | None |
| `--resolution <res>` | 720P, 1080P, 2K, 4K | 1080P |
| `--ratio <ratio>` | 16:9, 9:16, 1:1 | 16:9 |
| `--enhance` | Enable prompt enhancement | Disabled |
| `--chat-id <id>` | Feishu chat ID for progress cards | None |

### Examples

**1. Basic Text-to-Video (Kling 2.5)**
```bash
node skills/video-gen/index.js "A cyberpunk city in rain" --model Kling --model-version 2.5 --chat-id "oc_..."
```

**2. Image-to-Video (Hailuo 2.3)**
```bash
node skills/video-gen/index.js "Make the cat jump" --model Hailuo --model-version 2.3 --image "https://example.com/cat.jpg"
```

**3. Start & End Frame (Kling 2.1)**
```bash
node skills/video-gen/index.js "Morph from day to night" --model Kling --model-version 2.1 --image "https://.../day.jpg" --last-frame "https://.../night.jpg"
```

## Credentials
Requires `.env` variables:
- `VITE_VOD_SECRET_ID`
- `VITE_VOD_SECRET_KEY`
- `VITE_VOD_SUB_APP_ID`
