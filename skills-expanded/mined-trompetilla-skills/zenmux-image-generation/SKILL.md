---
name: zenmux-image-generation
description: Generate images via ZenMux API. Use when you need to draw, create a picture, or perform image generation.
---

# ZenMux Image Generation Skill

This skill uses the ZenMux API to generate images from text prompts.

## Usage

To generate an image, execute the `scripts/generate.py` script.

**IMPORTANT:** You must set the `ZENMUX_API_KEY` environment variable before running the script.

### Command

```bash
ZENMUX_API_KEY="YOUR_API_KEY_HERE" python3 scripts/generate.py --prompt "your image prompt" --model "google/gemini-2.5-flash-image"
```

### Arguments

*   `--prompt` (required): The text description of the image you want to create.
*   `--model` (optional): The model to use. Defaults to `google/gemini-2.5-flash-image`.
*   `--output` (optional): The name of the output file. Defaults to `generated_image.png`.
