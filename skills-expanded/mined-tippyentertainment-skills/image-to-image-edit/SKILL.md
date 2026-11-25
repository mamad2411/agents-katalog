---
name: image-to-image-edit
description: Transform existing images using AI with text prompts. Supports style transfer, inpainting, outpainting, and guided editing.
target: https://tasking.tech
---

# Image-to-Image Edit

Transform existing images using AI diffusion models with text guidance. This skill enables powerful image editing capabilities including style transfer, content modification, inpainting, and outpainting.

## Overview

Image-to-image (img2img) generation takes an existing image as input and transforms it based on a text prompt while preserving some characteristics of the original. The `strength` parameter controls how much the image changes - low values (0.3-0.5) preserve more of the original, while high values (0.7-1.0) allow more dramatic transformations.

## Parameters

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `image_url` | string | URL or local path to the source image. Supports PNG, JPG, WEBP formats. Must be publicly accessible URL or local file path. |
| `prompt` | string | Text description of the desired transformation. Be specific about style, content, and mood. Example: "transform into oil painting style, dramatic lighting, renaissance art" |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `negative_prompt` | string | "blurry, low quality, distorted, watermark" | What to avoid in the generation. Use to exclude unwanted elements. |
| `strength` | float | 0.75 | Transformation intensity (0.0-1.0). Lower = preserve original, higher = more change. Recommended: 0.3-0.5 for subtle edits, 0.6-0.8 for style transfers, 0.9+ for near-complete rewrites. |
| `seed` | integer | random | Reproducibility seed. Same seed + same parameters = same output. Use -1 for random. |
| `steps` | integer | 25 | Inference steps (15-50). More steps = higher quality but slower. 20-30 is usually sufficient. |
| `cfg_scale` | float | 7.5 | Classifier-free guidance scale (1-20). Higher = more prompt adherence, lower = more creative freedom. |
| `width` | integer | source width | Output width in pixels. Leave empty to match source. |
| `height` | integer | source height | Output height in pixels. Leave empty to match source. |
| `sampler` | string | "dpmpp_3m_sde" | Sampling algorithm. Options: euler_a, dpmpp_3m_sde, dpmpp_2m, ddim, uni_pc, lms. DPM++ samplers recommended for quality. |
| `scheduler` | string | "karras" | Noise scheduler. Options: karras, normal, sgm_uniform, simple. Karras generally produces best results. |
| `model` | string | system default | Model checkpoint name. Examples: sdXL_v10, realisticVision_v20, dreamshaper_8. |
| `mask_url` | string | null | URL to mask image for inpainting. White areas = inpaint, black areas = preserve. PNG with alpha channel supported. |
| `inpaint` | boolean | false | Enable inpainting mode. Requires mask_url. Only modifies masked regions. |
| `outpaint` | boolean | false | Enable outpainting mode. Extends image beyond original boundaries. |
| `outpaint_direction` | string | "right" | Direction to extend: left, right, up, down, or combinations like "left,right,up". |
| `batch_size` | integer | 1 | Number of variations to generate. Each gets a different seed. |
| `backend` | string | "auto" | Which API to use: comfyui, automatic1111, stability, local. Auto-detects available backend. |

## Returns

```json
{
  "image_url": "https://storage.example.com/generated/image_12345.png",
  "seed": 123456789,
  "metadata": {
    "prompt": "oil painting style, dramatic lighting",
    "negative_prompt": "blurry, low quality",
    "strength": 0.75,
    "steps": 25,
    "cfg_scale": 7.5,
    "sampler": "dpmpp_3m_sde",
    "model": "sdXL_v10"
  },
  "processing_time": 4.2
}
```

## Usage Examples

### Basic Style Transfer

```javascript
// Transform photo into oil painting
await imageToImageEdit({
  image_url: "https://example.com/photo.jpg",
  prompt: "oil painting style, impressionist, visible brush strokes, vibrant colors",
  strength: 0.7
});
```

### Subtle Enhancement

```javascript
// Enhance photo quality while preserving content
await imageToImageEdit({
  image_url: "https://example.com/portrait.jpg",
  prompt: "professional photography, studio lighting, high detail, sharp focus",
  strength: 0.35,
  steps: 30,
  cfg_scale: 8
});
```

### Inpainting (Edit Specific Areas)

```javascript
// Replace object in image
await imageToImageEdit({
  image_url: "https://example.com/room.jpg",
  mask_url: "https://example.com/room_mask.png",
  prompt: "modern furniture, minimalist sofa, coffee table",
  inpaint: true,
  strength: 0.8
});
```

### Outpainting (Extend Image)

```javascript
// Extend image to wider aspect ratio
await imageToImageEdit({
  image_url: "https://example.com/landscape.jpg",
  prompt: "continue the landscape, mountains, sky, clouds",
  outpaint: true,
  outpaint_direction: "left,right",
  width: 1920,
  height: 1080
});
```

### Batch Variations

```javascript
// Generate multiple style variations
await imageToImageEdit({
  image_url: "https://example.com/portrait.jpg",
  prompt: "cyberpunk style, neon lights, futuristic",
  strength: 0.65,
  batch_size: 4
});
// Returns 4 images with seeds: seed, seed+1, seed+2, seed+3
```

### Reproducible Results

```javascript
// Same seed = same result
await imageToImageEdit({
  image_url: "https://example.com/photo.jpg",
  prompt: "watercolor painting style",
  strength: 0.6,
  seed: 42  // Always produces same output
});
```

## Backend Implementations

### ComfyUI Backend

ComfyUI uses a node-based workflow system. The img2img workflow:

1. **LoadImage** - Loads source image from URL or file
2. **VAEEncode** - Encodes image to latent space
3. **CLIPTextEncode** - Encodes positive/negative prompts
4. **KSampler** - Denoises latents with guidance
5. **VAEDecode** - Decodes latents back to image
6. **SaveImage** - Outputs final result

Key parameters in ComfyUI:
- `denoise` = strength (0.0-1.0)
- `sampler_name` = sampler algorithm
- `scheduler` = noise schedule

### Automatic1111 Backend

Automatic1111's img2img API accepts:

```json
{
  "init_images": ["base64_encoded_image"],
  "prompt": "transformation description",
  "negative_prompt": "what to avoid",
  "denoising_strength": 0.75,
  "steps": 25,
  "cfg_scale": 7.5,
  "seed": -1,
  "sampler_name": "DPM++ 3M SDE",
  "width": 1024,
  "height": 1024
}
```

### Stability AI API

Stability AI's image-to-image endpoint:

```json
{
  "init_image": "base64_or_url",
  "text_prompts": [
    {"text": "transformation description", "weight": 1},
    {"text": "negative prompt", "weight": -1}
  ],
  "image_strength": 0.75,
  "steps": 25,
  "cfg_scale": 7.5,
  "seed": 0
}
```

## Strength Guidelines

| Strength | Use Case | Example |
|----------|----------|---------|
| 0.2-0.4 | Subtle fixes, upscaling, detail enhancement | "sharpen details, fix lighting" |
| 0.4-0.6 | Moderate changes, style enhancement | "add dramatic lighting, enhance colors" |
| 0.6-0.8 | Style transfer, significant changes | "transform into oil painting, cyberpunk style" |
| 0.8-0.95 | Major transformation, near-complete rewrite | "completely different scene, same composition" |
| 0.95-1.0 | Almost text-to-image, minimal original | "use as rough layout guide" |

## Prompt Engineering Tips

### Be Specific About Style

❌ "make it artistic"
✅ "oil painting style, impressionist, visible brush strokes, warm color palette, dramatic lighting"

### Describe Content Changes Clearly

❌ "change the background"
✅ "replace background with sunset beach scene, golden hour lighting, ocean waves"

### Use Negative Prompts Effectively

```javascript
negative_prompt: "blurry, low quality, distorted faces, extra limbs, watermark, text, signature"
```

### Preserve Important Elements

```javascript
prompt: "style as cyberpunk art, neon lights, futuristic city background, preserve the person's face and pose"
```

## Common Use Cases

### 1. Photo to Art Style

```javascript
{
  image_url: "photo.jpg",
  prompt: "oil painting style, renaissance art, dramatic chiaroscuro lighting, museum quality",
  strength: 0.7
}
```

### 2. Background Replacement

```javascript
{
  image_url: "portrait.jpg",
  prompt: "professional studio background, gradient lighting, corporate headshot style",
  strength: 0.5,
  negative_prompt: "distracting elements, cluttered background"
}
```

### 3. Object Removal (Inpainting)

```javascript
{
  image_url: "photo.jpg",
  mask_url: "mask.png",  // White over object to remove
  prompt: "clean background, seamless fill, natural continuation",
  inpaint: true,
  strength: 0.85
}
```

### 4. Color Grading

```javascript
{
  image_url: "photo.jpg",
  prompt: "cinematic color grading, teal and orange, film look, Kodak Portra 400",
  strength: 0.3
}
```

### 5. Upscaling with Enhancement

```javascript
{
  image_url: "low_res.jpg",
  prompt: "high resolution, sharp details, 4K quality, professional photography",
  strength: 0.4,
  width: 2048,
  height: 2048
}
```

### 6. Sketch to Image

```javascript
{
  image_url: "sketch.png",
  prompt: "photorealistic rendering, detailed textures, professional photography",
  strength: 0.85
}
```

### 7. Day to Night

```javascript
{
  image_url: "daytime_photo.jpg",
  prompt: "night scene, moonlight, street lamps, stars in sky, dark blue atmosphere",
  strength: 0.65
}
```

### 8. Season Change

```javascript
{
  image_url: "summer_photo.jpg",
  prompt: "winter scene, snow covered ground, bare trees, overcast sky, cold atmosphere",
  strength: 0.7
}
```

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `image_too_large` | Image exceeds max dimensions | Resize to under 2048x2048 |
| `invalid_url` | Image URL not accessible | Use public URL or local path |
| `timeout` | Generation took too long | Reduce steps or use faster sampler |
| `out_of_memory` | GPU memory exceeded | Reduce resolution or batch size |
| `invalid_mask` | Mask format incorrect | Use PNG with white/black regions |

### Retry Strategy

```javascript
// Implement exponential backoff
async function robustImg2Img(params, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await imageToImageEdit(params);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i)));
    }
  }
}
```

## Performance Optimization

### Faster Generation

- Use `euler_a` sampler for speed (15-20 steps sufficient)
- Reduce `steps` to 15-20 for quick previews
- Lower resolution for iteration, upscale final
- Use smaller models (SD 1.5 vs SDXL)

### Higher Quality

- Use `dpmpp_3m_sde` sampler with `karras` scheduler
- Increase `steps` to 30-50 for final output
- Use SDXL or fine-tuned models
- Higher `cfg_scale` (8-12) for prompt adherence

### Memory Efficiency

- Process one image at a time
- Use tiled VAE for large images
- Enable memory-efficient attention
- Clear cache between generations

## Integration with TaskingBot

This skill integrates with TaskingBot's image generation pipeline:

```javascript
// Use with generate_image for comparison
const original = await generate_image({prompt: "landscape"});
const transformed = await imageToImageEdit({
  image_url: original.image_url,
  prompt: "oil painting style",
  strength: 0.7
});
```

## Step-by-Step Instructions

### Basic Image Editing Workflow

1. **Prepare Source Image**
   - Ensure image is accessible via public URL or local path
   - Recommended size: 512-1024px (will be resized automatically)
   - Supported formats: PNG, JPG, WEBP

2. **Craft Your Prompt**
   - Describe the desired transformation clearly
   - Include style, mood, lighting, and content changes
   - Use negative prompts to exclude unwanted elements

3. **Set Strength Appropriately**
   - 0.3-0.5: Subtle changes, enhancement
   - 0.5-0.7: Moderate style transfer
   - 0.7-0.9: Major transformation

4. **Generate and Iterate**
   - Start with default parameters
   - Adjust strength if too much/little change
   - Use same seed for reproducibility
   - Generate multiple variations with batch_size

5. **Post-Process**
   - Download result from returned URL
   - Use `enhance_image` for upscaling if needed
   - Use `edit_image` for additional refinements

### Inpainting Workflow

1. **Create Mask Image**
   - Use image editing software (Photoshop, GIMP)
   - White (#FFFFFF) = areas to change
   - Black (#000000) = areas to preserve
   - Save as PNG with same dimensions as source

2. **Configure Inpainting**
   ```javascript
   {
     image_url: "source.png",
     mask_url: "mask.png",
     prompt: "what should appear in masked areas",
     inpaint: true,
     strength: 0.8
   }
   ```

3. **Best Practices**
   - Mask slightly beyond the area you want to change
   - Use higher strength (0.8-0.95) for complete replacement
   - Describe the full scene context in prompt

### Outpainting Workflow

1. **Set Target Dimensions**
   - Original: 1024x1024
   - Target: 1920x1080 (extends left/right)

2. **Configure Outpainting**
   ```javascript
   {
     image_url: "1024x1024_image.jpg",
     prompt: "continue the scene naturally",
     outpaint: true,
     outpaint_direction: "left,right",
     width: 1920,
     height: 1080
   }
   ```

3. **Direction Options**
   - `"left"` - extend left side
   - `"right"` - extend right side
   - `"up"` - extend top
   - `"down"` - extend bottom
   - `"left,right,up"` - multiple directions

## API Reference

### Endpoint

```
POST /api/image-to-image
```

### Request Headers

```
Content-Type: application/json
Authorization: Bearer <api_key>
```

### Request Body

```json
{
  "image_url": "https://example.com/image.jpg",
  "prompt": "transformation description",
  "negative_prompt": "what to avoid",
  "strength": 0.75,
  "seed": -1,
  "steps": 25,
  "cfg_scale": 7.5,
  "width": 1024,
  "height": 1024,
  "sampler": "dpmpp_3m_sde",
  "scheduler": "karras",
  "model": "sdXL_v10",
  "mask_url": null,
  "inpaint": false,
  "outpaint": false,
  "batch_size": 1
}
```

### Response

```json
{
  "success": true,
  "image_url": "https://storage.example.com/output.png",
  "seed": 123456789,
  "metadata": {
    "prompt": "transformation description",
    "strength": 0.75,
    "steps": 25,
    "processing_time_ms": 4200
  }
}
```

## Best Practices Summary

1. **Start Conservative**: Begin with strength 0.5-0.6, adjust based on results
2. **Use Negative Prompts**: Always exclude "blurry, low quality, distorted"
3. **Match Dimensions**: Keep aspect ratio similar for best results
4. **Iterate with Seeds**: Note successful seeds for reproducibility
5. **Batch for Variations**: Use batch_size to explore options efficiently
6. **Quality vs Speed**: More steps = better quality, but slower
7. **Prompt Specificity**: Detailed prompts yield better results
8. **Test Different Samplers**: DPM++ samplers generally best for img2img

## Troubleshooting

### Image Not Changing Enough

- Increase `strength` (try 0.8-0.9)
- Make prompt more specific
- Increase `cfg_scale` (try 10-12)

### Image Changing Too Much

- Decrease `strength` (try 0.3-0.5)
- Add preservation hints to prompt
- Use lower `cfg_scale` (try 5-7)

### Artifacts or Distortions

- Increase `steps` (try 30-40)
- Try different sampler (`dpmpp_3m_sde`)
- Add "artifacts, distortion" to negative prompt

### Slow Generation

- Reduce `steps` to 15-20
- Use `euler_a` sampler
- Lower resolution
- Reduce `batch_size`

## See Also

- `generate_image` - Generate images from text prompts
- `edit_image` - Simple image editing (crop, filter, etc.)
- `enhance_image` - Upscale and improve image quality
- `generate_3d_from_image` - Convert image to 3D model

---

**Version**: 1.0.0
**Author**: TaskingBot
**Created**: 2026-03-20
**Tags**: image, generation, editing, img2img, inpainting, outpainting, style-transfer, diffusion