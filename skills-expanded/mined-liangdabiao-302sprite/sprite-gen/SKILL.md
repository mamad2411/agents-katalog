---
name: sprite-gen
version: 1.0.0
summary: "Generate animated sprite sheets from text descriptions using Agent LLM + ImageGen + sharp/gifenc. No third-party API required."
triggers:
  - "精灵图"
  - "sprite sheet"
  - "sprite animation"
  - "游戏动画"
  - "角色动画"
  - "generate sprite"
  - "生成精灵图"
  - "像素动画"
---

# Sprite Sheet Generation Skill

Generate animated sprite sheets from text descriptions. Uses only Agent-native capabilities — no third-party API keys needed.

## Architecture

```
User Input → Agent LLM (prompt rewrite) → ImageGen (transparent sprite) → sharp (cut frames) → gifenc (animated GIF) → HTML preview
```

## Workflow

### Step 1: Receive User Input

Collect from user (use AskUserQuestion if not provided):
- **character**: Character description (e.g. "baby dragon, chibi kawaii, isometric action RPG")
- **gridSize**: Grid dimension, 2-6, default 4 (produces 4x4=16 frames)
- **actionType**: Optional — "walk", "attack", "idle", "cast", "dance" (enriches the LLM prompt)

### Step 2: Agent LLM Prompt Rewrite

**Do NOT call any external API.** Use your own LLM capability to perform the rewrite.

Use this system prompt (adapted from `buildRewriteSystemPrompt`):

```
You are an animation director and character designer for a sprite sheet pipeline.
Given a character concept, you MUST return exactly two sections, nothing else:

CHARACTER: A vivid description of the character's appearance — body type, armor, weapons, colors, silhouette, art style. Be extremely specific and visual.

CHOREOGRAPHY: A {gridWord}-beat continuous animation loop that showcases this specific character's personality and abilities. Each beat is one row of the sheet. The last beat must transition seamlessly back into the first.
For each beat, describe the body position, weight distribution, limb placement, and motion arc in one sentence.
The choreography must feel natural and unique to THIS character.

RULES:
- Never use numbers or digits anywhere.
- Never mention grids, pixels, frames, cells, or image generation.
- Write as if directing a real actor through a motion capture session.
- The {gridWord} beats must form one fluid, looping performance.
- For locomotion: strictly alternate left and right legs in each beat.
```

User message: `Design the character and choreograph a {gridWord}-beat animation loop for: {character}`

Parse the LLM response into the rewritten prompt text.

### Step 3: Build Technical Sprite Prompt

Concatenate the rewritten prompt with this technical spec (adapted from `buildSpritePrompt`):

```
STRICT TECHNICAL REQUIREMENTS FOR THIS IMAGE:

FORMAT: A single image containing a {gridWord}-by-{gridWord} grid of equally sized cells.
Every cell must be the exact same dimensions, perfectly aligned, with no gaps or overlap.

FORBIDDEN: Absolutely no text, no numbers, no letters, no digits, no labels,
no watermarks, no signatures, no UI elements anywhere in the image.

CONSISTENCY: The exact same single character must appear in every cell.
Same proportions, same art style, same level of detail, same camera angle throughout.
Isometric three-quarter view. Full body visible head to toe in every cell.
Strong clean silhouette against a plain solid flat-color background.

ANIMATION FLOW: The cells read left-to-right, top-to-bottom, like reading a page.
This is one continuous motion sequence. Each cell shows the next moment in the movement.
The transition between rows must be just as smooth as transitions within a row.
Each row contains {gridWord} phases of the motion. The last cell loops back to the first.

MOTION QUALITY: Show real weight and physics. Bodies shift weight between feet.
Arms counterbalance legs. Torsos rotate into actions. Follow-through on every movement.
For locomotion: strictly alternate left and right legs.

CHARACTER AND ANIMATION DIRECTION:
{rewrittenPrompt}
```

Grid word mapping: 2→"two", 3→"three", 4→"four", 5→"five", 6→"six"

### Step 4: ImageGen Call

Call the **ImageGen** tool (via DeferExecuteTool) with:
- `prompt`: The full technical sprite prompt from Step 3
- `size`: `"1024x1024"` — square format for grid
- `format`: `"png"` — PNG preserves transparency

**IMPORTANT**: ImageGen does NOT currently honor `background: "transparent"`. Generated images will have solid color backgrounds (often with gradients and grid lines). The `--remove-bg` flag in the processing script handles this automatically via **floodfill from border pixels** — far more robust than simple corner sampling because it handles gradient backgrounds and only removes regions connected to the border (won't accidentally delete character pixels that match the bg color).

**Fallback Strategy A (preferred)**: Single ImageGen call produces the full grid.
**Fallback Strategy B**: If grid alignment is poor, generate individual frames (N² calls) and composite with sharp.
**Fallback Strategy C**: First frame text-to-image, subsequent frames image-to-image for consistency.

### Step 5: Process Sprite Sheet

Run the processing script to cut frames, remove background, and create GIF:

```bash
{node_path} {skill_dir}/scripts/process-sprite.mjs \
  --input <path-to-generated-png> \
  --grid <gridSize> \
  --frame-size 200 \
  --remove-bg \
  --bg-tolerance 50 \
  --outdir <output-dir>
```

The script:
1. Reads the sprite sheet PNG
2. **Auto-removes background via floodfill**: Seeds from all border pixels, floodfills connected regions with similar colors (within tolerance), marks them as transparent. Handles gradients and grid lines. Only removes regions connected to the border — character pixels are preserved even if they match the bg color.
3. Uses sharp to cut the N×N grid into individual frames (also with transparent bg)
4. Cleans transparent edges (2px erosion to remove fringe)
5. Uses gifenc to encode an animated GIF with transparency (magenta sentinel for transparent pixels)
6. Generates an HTML preview page with checker pattern background, showing the GIF + individual frames

**Key flags**:
- `--remove-bg`: Auto-detect and remove solid background color (highly recommended for ImageGen output)
- `--bg-tolerance N`: Color distance threshold (5-120, default 45). Increase if background isn't fully removed
- `--frame-size N`: Output frame size in pixels (64-512, default 200)
- `--skip-frames`: Skip individual frame extraction (faster if you only need the GIF)

### Step 6: Present Results

Use `present_files` to show:
1. The HTML preview page (primary)
2. The animated GIF file
3. The sprite sheet PNG (original)

## Parameters Reference

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| character | (required) | any string | Character description |
| gridSize | 4 | 2-6 | Grid dimension (4 = 16 frames) |
| frameSize | 200 | 64-512 | Output GIF frame size in px |
| actionType | none | walk/attack/idle/cast/dance | Animation type hint |
| bgTolerance | 45 | 5-120 | Color distance threshold for bg removal |

## Dependencies

- `sharp` — image processing (must be in node_modules or workspace)
- `gifenc` — GIF encoding (must be in node_modules or workspace)
- Node.js 18+ (ESM support)

## Output Files

- `sprite-{timestamp}.png` — Original sprite sheet from ImageGen
- `sprite-{timestamp}.gif` — Animated GIF with transparency
- `sprite-{timestamp}-preview.html` — Interactive preview page
- `frames/frame-{N}.png` — Individual frame files (optional)
