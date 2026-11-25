---
name: veed-ugc
description: Generate UGC-style promotional videos with AI lip-sync. Takes an image (person with product from Morpheus/Ad-Ready) and a brief, generates a script, and creates a video of the person speaking. Uses ElevenLabs for voice synthesis.
---

# Veed-UGC

Generate UGC (User Generated Content) style promotional videos with AI lip-sync using ComfyDeploy's Veed-UGC workflow.

## Overview

Veed-UGC transforms static images into dynamic promotional videos:
1. Takes a photo of a person with a product (from Morpheus or Ad-Ready)
2. Receives a brief describing the tone and content
3. Internally generates a script from the brief
4. Creates a lip-synced video of the person speaking the script

Perfect for creating authentic-feeling promotional content at scale.

## API Details

**Endpoint:** `https://api.comfydeploy.com/api/run/deployment/queue`
**Deployment ID:** `627c8fb5-1285-4074-a17c-ae54f8a5b5c6`

## Required Inputs

| Input | Description | Example |
|-------|-------------|---------|
| `image` | URL of person+product image | Output from Morpheus/Ad-Ready |
| `brief` | Tone and content direction | "Tono: Argentino informal, promocionando el speaker Sonos como el mejor regalo para papá" |
| `voice_id` | ElevenLabs voice ID | Default: `PBi4M0xL4G7oVYxKgqww` |

## Brief Guidelines

The brief should include:
- **Tone**: The speaking style (informal, profesional, entusiasta, etc.)
- **Language/Accent**: Regional flavor (Argentino, Mexicano, Español neutro, etc.)
- **Content direction**: What should the person talk about
- **Call to action**: What action to promote (optional)

### Example Briefs

**Casual Argentine promotion:**
```
Tono: Argentino informal, como hablando con un amigo.
Promocionar el speaker Sonos Move como el regalo perfecto para el día del padre.
Mencionar la portabilidad y el sonido premium.
```

**Professional product review:**
```
Tono: Profesional pero cercano, español neutro.
Review del producto destacando calidad de construcción y diseño.
Enfocarse en por qué vale la inversión.
```

**Enthusiastic unboxing style:**
```
Tono: Entusiasta, como influencer de tech.
Reacción al recibir el producto, destacar el packaging y primeras impresiones.
Incluir call to action para seguir el canal.
```

## Voice IDs (ElevenLabs)

| Voice | ID | Description |
|-------|-----|-------------|
| Default | `PBi4M0xL4G7oVYxKgqww` | Main voice |

*More voices coming soon*

## Usage

```bash
uv run ~/.clawdbot/skills/veed-ugc/scripts/generate.py \
  --image "https://example.com/person-with-product.png" \
  --brief "Tono: Argentino informal, promocionando el producto" \
  --output "ugc-video.mp4"
```

### With local image file:
```bash
uv run ~/.clawdbot/skills/veed-ugc/scripts/generate.py \
  --image "./morpheus-output.png" \
  --brief "Tono: Entusiasta, review del producto" \
  --voice-id "PBi4M0xL4G7oVYxKgqww" \
  --output "promo-video.mp4"
```

## Workflow Integration

### Typical Pipeline

1. **Generate image with Morpheus/Ad-Ready**
   ```bash
   uv run morpheus... --output product-shot.png
   ```

2. **Create UGC video from the image**
   ```bash
   uv run veed-ugc... --image product-shot.png --brief "..." --output promo.mp4
   ```

### Batch Production

For campaign production, generate multiple variations:
- Different briefs (different angles/messages)
- Different voice IDs (different personas)
- Different source images (different models/settings)

## Output

The workflow outputs an MP4 video file with:
- The original image animated with lip-sync
- AI-generated voiceover based on the brief
- Natural head movements and expressions

## Notes

- Image should clearly show a person's face (frontal or 3/4 view works best)
- Brief is transformed into a script internally - keep it directional, not literal
- Video length depends on the generated script
- Processing time: ~2-5 minutes depending on script length
