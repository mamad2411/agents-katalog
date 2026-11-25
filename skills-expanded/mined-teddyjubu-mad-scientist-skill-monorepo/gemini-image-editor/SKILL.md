---

name: gemini-image-editor
description: Edit, enhance, remove objects, change backgrounds, and transform images using Google AI Studio Gemini Nano Banana Pro (Imagen 3). Use when you need to edit existing images, remove backgrounds, swap objects, change lighting, add/remove elements, or apply artistic transformations.
triggers:
  - edit this image
  - remove background
  - change the background
  - remove object from image
  - enhance this photo
  - fix this image
  - add to this image
  - transform this image
  - imagen
  - nano banana
version: 1.0.0
author: Charles Blair
created: 2026-03-12

---
Professional image editing powered by Google AI Studio Gemini Nano Banana Pro (Imagen 3).

## What This Skill Does

This skill Edit, enhance, remove objects, change backgrounds, and transform images using Google AI Studio Gemini Nano Banana Pro (Imagen 3). Use when you need to edit existing images, remove backgrounds, swap objects, change lighting, add/remove elements, or apply artistic transformations.

## What It Does

- **Edit images** with natural language prompts
- **Remove backgrounds** or replace them
- **Remove/add objects** from photos
- **Enhance quality** — lighting, colors, sharpness
- **Transform style** — artistic filters, mood changes
- **Batch processing** — edit multiple images at once

## Setup (One-Time)

API key is already configured in `.secrets/google-studio.env`.

```bash
# Verify key is loaded
source /data/.openclaw/workspace/skills/gemini-image-editor/.secrets/google-studio.env
echo $GOOGLE_API_KEY
```

## How to Use

### Via Node.js Script (Recommended)

```javascript
const { GoogleGenerativeAI } = require('@google/generative-ai');
const fs = require('fs');

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY);

async function editImage(imagePath, prompt) {
  const model = genAI.getGenerativeModel({ model: 'gemini-3-flash-preview' });
  
  const imageData = fs.readFileSync(imagePath);
  const base64Image = imageData.toString('base64');
  
  const result = await model.generateContent([
    {
      inlineData: {
        mimeType: 'image/jpeg', // or image/png
        data: base64Image
      }
    },
    prompt
  ]);
  
  // Extract and save edited image
  const response = await result.response;
  const imageBase64 = response.text(); // Returns base64 image
  
  // Save output
  const buffer = Buffer.from(imageBase64, 'base64');
  fs.writeFileSync('output.jpg', buffer);
  
  console.log('Image saved to output.jpg');
}

// Example usage
editImage('/path/to/image.jpg', 'Remove the background and replace with a modern office');
```

### Via Python Script

```python
import google.generativeai as genai
import os
import base64

genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

def edit_image(image_path, prompt):
    model = genai.GenerativeModel('gemini-3-flash-preview')
    
    # Load image
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Generate edit
    response = model.generate_content([
        {
            'mime_type': 'image/jpeg',
            'data': base64.b64encode(image_data).decode()
        },
        prompt
    ])
    
    # Save output
    output_data = base64.b64decode(response.text)
    with open('output.jpg', 'wb') as f:
        f.write(output_data)
    
    print('Image saved to output.jpg')

# Example usage
edit_image('/path/to/image.jpg', 'Remove the person in the background')
```

### Via cURL (Quick Testing)

```bash
#!/bin/bash
source /data/.openclaw/workspace/skills/gemini-image-editor/.secrets/google-studio.env

IMAGE_PATH="$1"
PROMPT="$2"
OUTPUT="${3:-output.jpg}"

# Convert image to base64
IMAGE_BASE64=$(base64 -w 0 "$IMAGE_PATH")

# API request
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key=$GOOGLE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"contents\": [{
      \"parts\": [
        {
          \"inline_data\": {
            \"mime_type\": \"image/jpeg\",
            \"data\": \"$IMAGE_BASE64\"
          }
        },
        {
          \"text\": \"$PROMPT\"
        }
      ]
    }]
  }" | jq -r '.candidates[0].content.parts[0].inline_data.data' | base64 -d > "$OUTPUT"

echo "Saved to $OUTPUT"
```

**Usage:**
```bash
./edit-image.sh input.jpg "Remove background" output.jpg
```

## Common Use Cases

### 1. Remove Background

```bash
./edit-image.sh headshot.jpg "Remove background completely, make it transparent" headshot-nobg.png
```

### 2. Replace Background

```bash
./edit-image.sh photo.jpg "Remove background and replace with a professional office setting" photo-office.jpg
```

### 3. Remove Objects

```bash
./edit-image.sh vacation.jpg "Remove the person in the red shirt on the left" vacation-clean.jpg
```

### 4. Add Elements

```bash
./edit-image.sh room.jpg "Add a potted plant in the corner and a painting on the wall" room-decorated.jpg
```

### 5. Enhance Quality

```bash
./edit-image.sh old-photo.jpg "Enhance quality, improve lighting, sharpen details, fix colors" old-photo-enhanced.jpg
```

### 6. Change Style

```bash
./edit-image.sh portrait.jpg "Convert to black and white with dramatic lighting" portrait-bw.jpg
```

### 7. Fix Lighting

```bash
./edit-image.sh dark-photo.jpg "Brighten the image, improve lighting, enhance colors" dark-photo-fixed.jpg
```

### 8. Product Photos

```bash
./edit-image.sh product.jpg "Remove all background clutter, center the product on a clean white background" product-clean.jpg
```

## Advanced Prompt Techniques

### Be Specific
❌ "Make it better"  
✅ "Remove background, center subject, brighten lighting by 20%, and add subtle shadow"

### Combine Edits
```bash
"Remove the background, replace with a sunset beach scene, enhance colors to be more vibrant, and add a subtle vignette effect"
```

### Reference Styles
```bash
"Edit this photo to look like a professional LinkedIn headshot: clean background, professional lighting, natural colors"
```

### Iterative Editing
```bash
# First pass
./edit-image.sh input.jpg "Remove background" step1.jpg

# Second pass
./edit-image.sh step1.jpg "Add office background with bookshelf" step2.jpg

# Final pass
./edit-image.sh step2.jpg "Enhance lighting and colors" final.jpg
```

## Batch Processing Script

```bash
#!/bin/bash
# batch-edit.sh

source /data/.openclaw/workspace/skills/gemini-image-editor/.secrets/google-studio.env

PROMPT="$1"
shift
IMAGES=("$@")

for IMG in "${IMAGES[@]}"; do
    FILENAME=$(basename "$IMG")
    OUTPUT="edited-$FILENAME"
    
    echo "Processing $IMG → $OUTPUT"
    ./edit-image.sh "$IMG" "$PROMPT" "$OUTPUT"
done

echo "Batch processing complete!"
```

**Usage:**
```bash
./batch-edit.sh "Remove background" *.jpg
```

## Best Practices

1. **Start with high-quality input** — better input = better output
2. **Use specific prompts** — describe exactly what you want changed
3. **Test prompts first** — try on one image before batch processing
4. **Save originals** — always keep the original file
5. **Iterate if needed** — run multiple passes for complex edits
6. **Check output format** — specify PNG for transparency, JPG for photos

## Supported Input Formats

- JPEG/JPG
- PNG
- WebP
- GIF (static)

## Supported Output Formats

- JPEG (default for photos)
- PNG (for transparency)
- WebP (for smaller file sizes)

## Limitations

- Max input size: 20MB per image
- Max resolution: 4096x4096 pixels
- Processing time: 5-30 seconds per image
- Rate limit: 60 requests per minute

## Troubleshooting

### API Key Not Found
```bash
source /data/.openclaw/workspace/skills/gemini-image-editor/.secrets/google-studio.env
echo $GOOGLE_API_KEY
```

### Image Too Large
```bash
# Resize before processing
convert input.jpg -resize 2048x2048\> resized.jpg
./edit-image.sh resized.jpg "Your prompt"
```

### Poor Results
- **Make prompt more specific**
- **Try different wording**
- **Run multiple passes** (edit → refine → polish)
- **Check input quality** (blur/noise = poor output)

## Integration with Other Skills

- **Combine with `yt-thumbnail-creator`:** Generate → edit → polish
- **Combine with `heygen-avatar-video`:** Edit avatar backgrounds
- **Combine with `openai-image-gen`:** Generate → refine with edits
- **Combine with marketing workflows:** Product photos → edited → GHL campaigns

## When to Use This Skill

✅ **Use Gemini Image Editor when:**
- Editing existing images
- Removing/replacing backgrounds
- Removing unwanted objects
- Enhancing photo quality
- Changing lighting/colors
- Adding elements to images
- Professional photo cleanup

❌ **Don't use when:**
- Generating new images from scratch (use `nano-banana-pro` or `openai-image-gen`)
- Simple crops/resizes (use ImageMagick/`convert`)
- Batch format conversion (use `ffmpeg` or `convert`)

## Quick Reference

```bash
# Setup
source /data/.openclaw/workspace/skills/gemini-image-editor/.secrets/google-studio.env

# Edit single image
./edit-image.sh input.jpg "Remove background" output.jpg

# Batch edit
./batch-edit.sh "Remove background" *.jpg

# Check API key
echo $GOOGLE_API_KEY
```

## Helper Scripts Location

All helper scripts should be saved in:
```
/data/.openclaw/workspace/skills/gemini-image-editor/scripts/
```

Create this directory structure:
```
gemini-image-editor/
├── SKILL.md
├── .secrets/
│   └── google-studio.env
└── scripts/
    ├── edit-image.sh
    ├── batch-edit.sh
    ├── edit-image.js
    └── edit-image.py
```

---

**Status:** ✅ Configured  
**API Key:** Stored in `.secrets/google-studio.env`  
**Model:** `gemini-3-flash-preview` (Imagen 3)  
**Capabilities:** Edit, enhance, remove/add objects, background replacement
