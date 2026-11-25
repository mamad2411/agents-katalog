---
name: remove-background
description: Remove the background from an image. Use when the user wants to remove, delete, or strip the background from a photo or image, make an image transparent, or isolate a subject from its background.
---

# Remove Background from Image

Remove the background from any image using AI, outputting a PNG with transparency.

## Primary Method: Local rembg Library

Use the locally installed `rembg` Python library. This is fast, reliable, and doesn't require network access.

### Usage

```bash
python3 -c "
from rembg import remove
from pathlib import Path

input_path = '/path/to/input.png'
output_path = '/path/to/output_no_bg.png'

with open(input_path, 'rb') as f:
    input_data = f.read()

output_data = remove(input_data)

with open(output_path, 'wb') as f:
    f.write(output_data)

print(f'Background removed. Saved to: {output_path}')
"
```

### Dependencies

The following are already installed:
- `rembg`
- `onnxruntime`
- `pillow`

The u2net model is cached at `~/.u2net/u2net.onnx` (downloads automatically on first use if missing).

### Example Workflow

User: "Remove the background from ./photo.jpg"

1. Determine output path: `./photo_no_bg.png`
2. Run the Python script with input and output paths
3. Inform user of the saved file location

## Fallback Method: Replicate API

Only use this if the local `rembg` method fails (e.g., missing dependencies).

### Using Replicate

Use the `mcp__replicate__create_predictions` tool with:

```
version: "95fcc2a26d3899cd6c2691c900465aaeff466285a65c14638cc5f36f34befaf1"
input: { "image": "<image_url_or_data_url>" }
Prefer: "wait"
```

### CRITICAL: Handling Local Files with Data URLs

**DO NOT truncate the base64 data.** The full data URL can be 100KB+ for typical images.

For small files (< 256KB), create a data URL:

```bash
# Create the COMPLETE data URL - do NOT preview or truncate it
python3 -c "
import base64
import sys

filepath = sys.argv[1]
with open(filepath, 'rb') as f:
    data = base64.b64encode(f.read()).decode()

ext = filepath.split('.')[-1].lower()
mime_types = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png', 'webp': 'image/webp'}
mime = mime_types.get(ext, 'image/png')

# Output the FULL data URL
print(f'data:{mime};base64,{data}')
" "/path/to/image.png"
```

**WARNING:** Never use `head`, `tail`, or any truncation when handling data URLs. The entire base64 string must be passed to the API.

For larger files (> 256KB), use the Replicate Files API to upload first:
1. Use `mcp__replicate__create_files` to upload the image
2. Use the returned URL in the prediction request

## Supported Input Formats

- PNG, JPG/JPEG, WebP
- Local file paths or URLs
- Any image size (larger images take longer to process)

## Output

- PNG format with RGBA mode (alpha channel for transparency)
- Save to user's specified path, or same directory with `_no_bg.png` suffix

## Error Handling

- If image file doesn't exist: inform the user
- If rembg fails: check dependencies with `pip show rembg`
- If Replicate fails: check the error message, ensure data URL is not truncated
- If format unsupported: suggest converting to PNG/JPG first
