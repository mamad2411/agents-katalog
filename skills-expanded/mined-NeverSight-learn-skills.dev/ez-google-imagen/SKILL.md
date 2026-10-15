---
name: ez-google-imagen
description: Generate/edit images with Google Gemini and Imagen models. Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image and --model.
---

# ez-google-imagen

Generate new images or edit existing ones using Google's Gemini and Imagen models.

Currently supports:
- **Vertex AI ADC** (Application Default Credentials) - default
- **Gemini API key** - fallback

## Models

| Model | Type | Editing | Notes |
|-------|------|---------|-------|
| `gemini-3-pro-image-preview` | Gemini | Yes | Default. High quality generation and editing. |
| `imagen-4.0-generate-001` | Imagen 4 | No | Best image quality. Generation only. |

Use `--model` to select. Default: `gemini-3-pro-image-preview`.

### Model Aliases

Short names you can use instead of full model IDs:

| Alias | Resolves to |
|-------|-------------|
| `nano-banana` | `gemini-3-pro-image-preview` |
| `gemini` | `gemini-3-pro-image-preview` |
| `imagen` | `imagen-4.0-generate-001` |
| `imagen4` | `imagen-4.0-generate-001` |

Example: `--model nano-banana` is equivalent to `--model gemini-3-pro-image-preview`.

Imagen models use `generate_images` API (generation only). Gemini models use `generate_content` API (generation + editing).

## Usage

Script path (do NOT cd to skill directory first):

```
SCRIPT=~/.openclaw/skills/ez-google-imagen/scripts/generate_image.py
```

**Generate (Gemini, default):**
```bash
uv run $SCRIPT --prompt "your image description" --filename "output-name.png"
```

**Generate (Imagen 4):**
```bash
uv run $SCRIPT --prompt "your image description" --filename "output-name.png" --model imagen-4.0-generate-001
```

**Generate (API key fallback):**
```bash
uv run $SCRIPT --prompt "your image description" --filename "output-name.png" --api-key KEY
```

**Edit existing image (Gemini only):**
```bash
uv run $SCRIPT --prompt "editing instructions" --filename "output-name.png" --input-image "path/to/input.png"
```

**Important:** Always run from the user's current working directory so images are saved where the user is working, not in the skill directory.

## Default Workflow (draft → iterate → final)

Goal: fast iteration without burning time on 4K until the prompt is correct.

- Draft (1K): quick feedback loop
  - `uv run $SCRIPT --prompt "<draft prompt>" --filename "yyyy-mm-dd-hh-mm-ss-draft.png" --resolution 1K`
- Iterate: adjust prompt in small diffs; keep filename new per run
  - If editing: keep the same `--input-image` for every iteration until you're happy.
- Final (4K): only when prompt is locked
  - `uv run $SCRIPT --prompt "<final prompt>" --filename "yyyy-mm-dd-hh-mm-ss-final.png" --resolution 4K`

## Resolution Options

The Gemini image API supports three resolutions (uppercase K required):

- **1K** (default) - ~1024px resolution
- **2K** - ~2048px resolution
- **4K** - ~4096px resolution

Map user requests to API parameters:
- No mention of resolution → `1K`
- "low resolution", "1080", "1080p", "1K" → `1K`
- "2K", "2048", "normal", "medium resolution" → `2K`
- "high resolution", "high-res", "hi-res", "4K", "ultra" → `4K`

## Authentication

The script supports two authentication methods:

### 1. Vertex AI ADC (Default)
Uses Application Default Credentials - no configuration needed if ADC is set up.
- Default project: read from `GOOGLE_CLOUD_PROJECT` env var, or auto-detected from ADC
- Default location: `global`
- Override with `--project` and `--location` flags if needed

### 2. API Key (Fallback)
If you need to use a Gemini API key instead:
1. `--api-key` argument (use if user provided key in chat)
2. `GEMINI_API_KEY` environment variable

The script tries Vertex AI ADC first (if no API key provided), then falls back to API key auth.

## Preflight + Common Failures (fast fixes)

- Preflight:
  - `command -v uv` (must exist)
  - Vertex AI ADC configured (default) OR `GEMINI_API_KEY` set / `--api-key` passed
  - If editing: `test -f "path/to/input.png"`

- Common failures:
  - `Error: Failed to initialize Vertex AI with ADC` → run `gcloud auth application-default login` or provide API key
  - `Error loading input image:` → wrong path / unreadable file; verify `--input-image` points to a real image
  - "quota/permission/403" style API errors → wrong credentials, no access, or quota exceeded

## Filename Generation

Generate filenames with the pattern: `yyyy-mm-dd-hh-mm-ss-name.png`

**Format:** `{timestamp}-{descriptive-name}.png`
- Timestamp: Current date/time in format `yyyy-mm-dd-hh-mm-ss` (24-hour format)
- Name: Descriptive lowercase text with hyphens
- Keep the descriptive part concise (1-5 words typically)
- Use context from user's prompt or conversation
- If unclear, use random identifier (e.g., `x9k2`, `a7b3`)

Examples:
- Prompt "A serene Japanese garden" → `2025-11-23-14-23-05-japanese-garden.png`
- Prompt "sunset over mountains" → `2025-11-23-15-30-12-sunset-mountains.png`
- Prompt "create an image of a robot" → `2025-11-23-16-45-33-robot.png`
- Unclear context → `2025-11-23-17-12-48-x9k2.png`

## Image Editing

When the user wants to modify an existing image:
1. Check if they provide an image path or reference an image in the current directory
2. Use `--input-image` parameter with the path to the image
3. The prompt should contain editing instructions (e.g., "make the sky more dramatic", "remove the person", "change to cartoon style")
4. Common editing tasks: add/remove elements, change style, adjust colors, blur background, etc.

## Prompt Handling

**For generation:** Pass user's image description as-is to `--prompt`. Only rework if clearly insufficient.

**For editing:** Pass editing instructions in `--prompt` (e.g., "add a rainbow in the sky", "make it look like a watercolor painting")

Preserve user's creative intent in both cases.

## Prompt Templates (high hit-rate)

Use templates when the user is vague or when edits must be precise.

- Generation template:
  - "Create an image of: <subject>. Style: <style>. Composition: <camera/shot>. Lighting: <lighting>. Background: <background>. Color palette: <palette>. Avoid: <list>."

- Editing template (preserve everything else):
  - "Change ONLY: <single change>. Keep identical: subject, composition/crop, pose, lighting, color palette, background, text, and overall style. Do not add new objects. If text exists, keep it unchanged."

## Output

- Saves PNG to current directory (or specified path if filename includes directory)
- Script outputs the full path to the generated image
- **Do not read the image back** - just inform the user of the saved path

## Examples

**Generate with Gemini (default):**
```bash
uv run $SCRIPT --prompt "A serene Japanese garden with cherry blossoms" --filename "2025-11-23-14-23-05-japanese-garden.png" --resolution 4K
```

**Generate with Imagen 4:**
```bash
uv run $SCRIPT --prompt "A serene Japanese garden" --filename "2025-11-23-14-23-05-japanese-garden.png" --model imagen-4.0-generate-001
```

**Edit existing image (Gemini only):**
```bash
uv run $SCRIPT --prompt "make the sky more dramatic with storm clouds" --filename "2025-11-23-14-25-30-dramatic-sky.png" --input-image "original-photo.jpg" --resolution 2K
```

**Using API key (fallback):**
```bash
uv run $SCRIPT --prompt "A mountain landscape" --filename "mountain.png" --api-key "your-api-key-here"
```
