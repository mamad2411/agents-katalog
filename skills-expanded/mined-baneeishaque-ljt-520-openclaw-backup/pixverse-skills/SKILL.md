---
name: pixverse
description: "Generate high-quality AI videos using Pixverse API - text-to-video, image-to-video, and video extension"
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "bins": ["pixverse"], "env": ["PIXVERSE_API_KEY"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "npm",
              "package": ".",
              "bins": ["pixverse"],
              "label": "Build pixverse skills (npm)",
            },
          ],
      },
  }
---

# Pixverse Skills

AI video generation skills for Claude Code and OpenClaw.

## Features

- **Text-to-Video**: Generate videos from text descriptions
- **Image-to-Video**: Animate static images
- **Video Extension**: Extend existing videos seamlessly

## Installation

1. Get your API key from [Pixverse Platform](https://platform.pixverse.ai)
2. Set environment variable:
   ```bash
   export PIXVERSE_API_KEY="sk-your-api-key"
   ```
3. Link to skills directory:
   ```bash
   # For Claude Code
   ln -s $(pwd) ~/.claude/skills/pixverse

   # For OpenClaw
   ln -s $(pwd) ~/.openclaw/skills/pixverse
   ```

## Usage

### Generate Video from Text

```
Please generate a video of a cat playing piano
```

Or use the skill directly:
```
/gen_video {"prompt": "a cat playing piano", "duration": 5, "resolution": "720p"}
```

### Image to Video

```
Animate this image: /path/to/photo.jpg with a slow zoom in effect
```

### Extend Video

```
Extend this video: /path/to/clip.mp4 by 5 seconds
```

## Requirements

- Node.js 20+
- Pixverse API key
- Internet connection

## Support

- Documentation: https://docs.platform.pixverse.ai
- GitHub: https://github.com/PixVerseAI/Pixverse-Skills
