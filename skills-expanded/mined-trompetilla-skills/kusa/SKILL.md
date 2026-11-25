---
name: kusa
description: Generate images using the Kusa.pics API.
---
# Kusa.pics Image Generator

Generate images using the Kusa.pics API.

## Configuration
- API Key: Set `KUSA_API_KEY` environment variable.

## Usage
```bash
export KUSA_API_KEY="your_api_key_here"
node skills/kusa-image/index.js "Your prompt here" [--style <id>] [--width <w>] [--height <h>]
```

## Options
- `--style`: Style ID (Default: 6)
- `--width`: Width (Default: 960)
- `--height`: Height (Default: 1680)
