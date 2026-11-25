---
name: thumbnail-generator
description: Generate YouTube thumbnails by face-swapping onto existing templates, then modify colors, text, and styling. Use when creating thumbnails, recreating thumbnails from other creators, or designing YouTube thumbnails.
allowed-tools: Read, Grep, Glob, Bash
---

# Thumbnail Generator — Face Swap + Style Variations

## Goal
Take inspiration thumbnails from creators you like, generate new thumbnails in the same style but with your face, then apply stochastic modifications (background colors, text changes, styling tweaks). Produces 3 variations by default, each intentionally different.

## Inputs
- **Source thumbnails**: YouTube URLs, direct image URLs, or local image paths
- **Face reference**: `face.png` in `.tmp/thumbnails/face/` — this is the only reference photo. Always use `--refs 1`
- **Modifications** (optional): Additional instructions like "replace the logo with X" or "change background to dark blue"

## Process

### Step 1: Download & Inspect Source Thumbnail
Download the source thumbnail and **visually inspect it yourself** using the Read tool before generating anything.

```bash
# From YouTube URL — use --source with the direct image URL (faster, avoids video ID parsing)
python3 execution/recreate_thumbnails.py --source "https://i.ytimg.com/vi/VIDEO_ID/maxresdefault.jpg" --no-match --refs 1 --variations 1

# From local file
python3 execution/recreate_thumbnails.py --source "path/to/thumbnail.jpg" --no-match --refs 1 --variations 1
```

### Step 2: Visual Analysis (ALWAYS DO THIS)
After inspecting the source thumbnail, identify 3-4 minor visual elements that can be subtly varied without changing the thumbnail's overall look. Examples:
- Background color/tint (white → warm cream, cool gray, light blue)
- Arrow or accent color (red → orange, gold, deeper red)
- Text shadow weight or outline thickness
- Logo color shift (subtle hue change)
- Lighting warmth (cool vs warm white)

Keep variations **minor** — the thumbnail should still look like the same thumbnail at a glance. The goal is subtle differentiation, not a redesign.

### Step 3: Generate 3 Variations with Micro-Tweaks
Run **3 separate generations in parallel** (1 variation each), each with a different micro-tweak from your analysis passed via `--prompt`. This ensures each output is meaningfully different rather than relying on stochastic model variance alone.

```bash
# Variation 1: tweak element A
python3 execution/recreate_thumbnails.py --source "URL" --no-match --refs 1 --variations 1 \
  --prompt "Make the background wall a very subtle warm cream instead of pure white"

# Variation 2: tweak element B
python3 execution/recreate_thumbnails.py --source "URL" --no-match --refs 1 --variations 1 \
  --prompt "Change the red arrow to a gold/yellow arrow"

# Variation 3: tweak element C
python3 execution/recreate_thumbnails.py --source "URL" --no-match --refs 1 --variations 1 \
  --prompt "Add a subtle cool blue tint to the lighting"
```

Always append the user's own instructions (if any) to each prompt alongside the micro-tweak.

### Step 4: Edit Pass (Optional)
Pick your favorite, then refine:
```bash
python3 execution/recreate_thumbnails.py --edit ".tmp/thumbnails/20260228/115127_1.png" \
  --prompt "Change background to teal. Replace 'AI GOLD RUSH' with 'AGENT SKILLS'. Make text bigger."
```

Edit passes support:
- Background color changes
- Text replacement and resizing
- Logo swaps
- Graph/chart modifications
- Any visual tweak you can describe

## Key Behaviors
- **Face + body adaptation**: The script adapts skin tone, hair, build, and neck to match Nick — not just a face paste
- **Forced 1280x720 output**: All outputs are resized to exact YouTube thumbnail dimensions
- **Single reference photo**: Always use `--refs 1`. The reference is `face.png` (clean headshot). Using noisy references (thumbnails with text overlays, etc.) degrades quality
- **Always use `--no-match`**: Face direction matching requires specially named files (`nick_yawL30_pitchU10.jpg`). We don't have those, so always skip with `--no-match`

## File Locations
| Path | Purpose |
|------|---------|
| `.tmp/thumbnails/face/face.png` | The single face reference photo (clean headshot) |
| `.tmp/thumbnails/YYYYMMDD/` | Generated thumbnails organized by date |
| `execution/recreate_thumbnails.py` | Main script |

## Environment
Requires in `.env`:
```
NANO_BANANA_API_KEY=your_gemini_api_key
```

## Cost
- ~$0.14-0.24 per generation/edit
- 3 parallel variations = ~$0.50 total
- Edit passes are one image at a time = ~$0.14-0.24

## Tips
- 1 clean reference photo beats 2 where one is noisy
- Run all 3 variations in parallel (separate Bash calls) for speed
- Keep micro-tweak prompts simple and direct
- Reference exact text strings when changing copy

## First-Run Setup

Before executing, check if the workspace has a `.gitignore` file. If it doesn't, assume the user is new to this skill. In that case:

1. Ask the user if this is their first time running this skill
2. If yes, walk them through how it works and what they need to configure/set up (API keys, env vars, dependencies, etc.)
3. Let them know that Nick wishes them the best!
