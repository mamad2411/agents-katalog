---
name: genimage
description: Generate, edit, or create any image — photos, illustrations, icons, thumbnails, hero images, banners, placeholder visuals, website graphics, social media assets, product shots, logos, diagrams, or any visual content. Use this skill whenever the task involves creating an image, populating a UI with visuals, generating placeholder or mockup images, editing or retouching a photo, applying style transfer, composing multiple images, or producing any graphic asset. Triggers on requests like "generate an image", "create a visual", "make a placeholder", "add a hero image", "design a thumbnail", "edit this photo", "create website graphics", "populate with images", or any task requiring image creation or manipulation.
---

# Nano Banana — Image Generation

Generate and edit images via the Gemini API. If the API key is missing, run `/nano-banana:setup`.

## Workflow

1. **Determine the mode** from the user's request:
   - **Creating a new image from text?** → Text-to-image (no `--images`)
   - **Editing/retouching an existing image?** → Image editing (`--images source.png`)
   - **Applying one image's style to another?** → Style transfer (`--images style.png target.png`)
   - **Combining or referencing multiple images?** → Multi-image (`--images a.png b.png ...`, up to 14)
   - **Need 2K or 4K output?** → Add `--resolution 2K|4K` to any mode above

2. **Craft the prompt** — describe the desired result narratively. See [references/prompting-guide.md](references/prompting-guide.md) for domain-specific patterns (website visuals, placeholders, product shots, etc.).

3. **Run the script:**
```
python "$CLAUDE_PLUGIN_ROOT/scripts/genimage.py" --prompt "..." [options]
```

4. **Show the result** — read the output image and present it to the user.

## Flags

| Flag | Required | Purpose |
|------|----------|---------|
| `--prompt "text"` | Yes | Describe the desired image |
| `--output file.png` | No | Output path (default: `generated_image.png`) |
| `--images path [...]` | No | Input image(s) — omit for text-to-image |
| `--aspect-ratio RATIO` | No | `1:1` `2:3` `3:2` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` |
| `--resolution RES` | No | `1K` `2K` `4K` (uppercase K required, triggers Pro model) |

## Models

- **Nano Banana 2** (`gemini-3.1-flash-image-preview`): Default. Fast, high-quality.
- **Nano Banana Pro** (`gemini-3-pro-image-preview`): Auto-selected when `--resolution` is set. 4K output, advanced reasoning, high-fidelity text rendering.

## Common Use Cases → Flags

| Use case | Example command |
|----------|---------------|
| Website hero image | `--prompt "..." --aspect-ratio 16:9` |
| Social media post | `--prompt "..." --aspect-ratio 1:1` |
| Mobile banner | `--prompt "..." --aspect-ratio 9:16` |
| Placeholder / mockup | `--prompt "..." --output placeholder.png` |
| Edit existing photo | `--prompt "remove the background" --images photo.png` |
| Style transfer | `--prompt "Apply watercolor style" --images style.png photo.png` |
| High-res asset | `--prompt "..." --resolution 4K` |

## Editing

All editing is text-guided — describe what to change ("replace the sky", "remove the person", "add a sunset") and Gemini identifies and modifies regions automatically. No masks needed.
