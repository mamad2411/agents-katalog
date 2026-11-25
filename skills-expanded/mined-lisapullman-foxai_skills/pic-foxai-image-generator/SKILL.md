---
name: pic-foxai-image-generator
description: Generate images using FoxAI (pic.foxai.edu.kg) - Chinese AI image generator
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["node"], "npm": ["playwright"] },
        "install":
          [
            {
              "id": "install-playwright",
              "kind": "npm",
              "pkg": "playwright",
              "label": "Install Playwright",
            }
          ],
      },
  }
---

# FoxAI Image Generator

Generate images using FoxAI (https://pic.foxai.edu.kg/)

## Usage

```bash
/node/path/to/foxai_generator.cjs "prompt" --count 1
```

## Examples

```bash
# Generate a cute cat
/node/path/to/foxai_generator.cjs "cute cat" --count 1

# Generate with custom model
/node/path/to/foxai_generator.cjs "landscape" --model "FLUX.1 [schnell]" --count 1

# Generate multiple images
/node/path/to/foxai_generator.cjs "sunset over ocean" --count 4
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `prompt` | Image description | Required |
| `--count` | Number of images | 1 |
| `--model` | Model name | FLUX.1 [schnell] |
| `--resolution` | Image size | 1024x1024 |
| `--negative` | Negative prompt | (optional) |

## Available Models

- `FLUX.1 [schnell]` - Fast, detailed
- `Stable Diffusion XL Base 1.0`
- `DreamShaper 8 LCM`
- `Stable Diffusion XL Lightning`

## Notes

- Login password: `20200108`
- Images saved to: `/root/.openclaw/workspace/foxai_*.png`
