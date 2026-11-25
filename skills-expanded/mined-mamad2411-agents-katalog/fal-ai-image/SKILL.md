---
name: fal-ai-image
description: "Generate/edit images via fal.ai. Supports Google Nano Banana Pro and OpenAI GPT Image 2 selected from config/.env. Supports reference images and strong text rendering. ALWAYS read SKILL.md before first use."
---

# fal-ai-image

Generate images via fal.ai. The skill now supports two fal-hosted models:

- **Google Nano Banana Pro** (`fal-ai/nano-banana-pro`) — default, backward-compatible
- **OpenAI GPT Image 2** (`openai/gpt-image-2`) — enabled from `config/.env`

Synonyms the agent should treat as equivalent:

- `gpt` = `openai` = GPT Image 2
- `nano banana` = `google` = `gemini` = Nano Banana Pro

Best for: infographics, text rendering, banners, photo edits, reference-based compositions.

## STOP — Read Before Acting

- **DO NOT** use Pillow, ImageMagick, or post-processing for text/logo overlay unless the user explicitly asked for that workflow
- **DO NOT** use Generate mode when the user provided reference images — use **Edit mode**
- **DO NOT** assume GPT is active — check `config/README.md` logic; if no selector is configured, the skill stays on Nano Banana
- **DO NOT** guess provider-specific params — Nano Banana and GPT Image 2 use different schemas
- **DO** pass `--model ...` when the user explicitly asks for a specific model/provider or asks to compare providers
- **DO NOT** skip uploading local files — run `upload.sh` first to get URLs for `edit.sh`

## Quick Start Decision

```text
Reference images provided?  -> Edit mode   (upload.sh -> edit.sh)
Text-only generation?       -> Generate mode (generate.sh)

Model comes from config/.env:
  no selector set           -> Nano Banana Pro
  FAL_IMAGE_PROVIDER=openai -> GPT Image 2
  FAL_IMAGE_MODEL=...       -> exact override
```

## Config

Requires `FAL_KEY` in `config/.env` or the environment.

Model selection:

1. `--model` — one-off override for the current command
2. `FAL_IMAGE_MODEL` — exact override in config
3. `FAL_IMAGE_PROVIDER` — `google` or `openai`
4. nothing set — default to Nano Banana Pro

Use `--model` whenever the user explicitly says things like:

- "сделай через GPT"
- "используй OpenAI"
- "сделай через Google / Gemini / Nano Banana"
- "какие тут есть провайдеры?"

Answer that the skill supports two choices and map the command like this:

- `--model gpt` for OpenAI GPT Image 2
- `--model gemini` or `--model nano-banana` for Nano Banana

OpenAI quality default:

- `FAL_IMAGE_OPENAI_QUALITY=medium` unless overridden with `--quality`
- this skill intentionally uses `medium` as the default for GPT to avoid expensive exploratory runs

Full setup and troubleshooting: [config/README.md](config/README.md).

Read references only when needed:

- [references/MODELS.md](references/MODELS.md) — selector precedence, aliases, cost heuristics
- [references/EDITING.md](references/EDITING.md) — generate vs edit, `mask_url`, inpainting behavior

## Model Notes

### Nano Banana Pro

Strengths:

- lower-friction default for existing installs
- strong text rendering, including Cyrillic
- good at infographics, banners, and mixed text/image layouts
- supports `--web-search` in generate mode

Main params:

- `--aspect-ratio`
- `--resolution`
- `--web-search` (generate only)

### OpenAI GPT Image 2

Strengths:

- stronger prompt adherence and fine-grained edits
- better photorealism and product-style renders
- native `quality` control
- uses the same `FAL_KEY` through fal, no separate OpenAI key
- current fal pricing is size/quality-dependent; a rough high-quality mental model is about `$0.18` per image, but check the live model page before quoting an exact number

Main params:

- `--image-size`
- `--quality`

Compatibility layer:

- if `--image-size` is omitted, the scripts derive a valid OpenAI `image_size` from `--aspect-ratio` + `--resolution`
- this lets old prompts continue working after the provider switch in config

## Workflow

### Generate mode

1. Decide model from config
2. Clarify missing params only if needed:
   - Nano Banana: aspect ratio, resolution
   - GPT Image 2: image size and quality
3. Propose save path based on project structure
4. Run `generate.sh`
5. Parse result JSON, report URL and local files if downloaded

### Edit mode

1. Get reference images:
   - URL already available -> use directly
   - local file -> `upload.sh`
2. Decide model from config
3. Clarify edit intent
4. Run `edit.sh`
5. Parse result JSON, report URL and local files if downloaded

## Scripts

### generate.sh

Nano Banana example:

```bash
sh scripts/generate.sh \
  --model "gemini" \
  --prompt "infographic about coffee brewing" \
  --aspect-ratio "9:16" \
  --resolution "1K" \
  --output-dir "./images" \
  --filename "coffee_infographic"
```

GPT Image 2 example:

```bash
sh scripts/generate.sh \
  --model "gpt" \
  --prompt "realistic product hero shot with sharp packaging text" \
  --image-size "landscape_4_3" \
  --quality "medium" \
  --output-dir "./images" \
  --filename "product_hero"
```

Compatibility example for GPT:

```bash
sh scripts/generate.sh \
  --model "openai" \
  --prompt "editorial portrait, window light, magazine cover layout" \
  --aspect-ratio "4:3" \
  --resolution "2K"
```

| Param | Required | Default | Notes |
|-------|----------|---------|-------|
| `--prompt` | yes | - | text prompt |
| `--model` | no | config / Nano Banana fallback | `nano-banana`, `google`, `gemini`, `gpt`, `openai`, or exact endpoint |
| `--aspect-ratio` | no | `1:1` | Nano native; for GPT used only when `--image-size` is omitted |
| `--resolution` | no | `1K` | Nano native; for GPT used only when `--image-size` is omitted |
| `--image-size` | no | derived from ratio/resolution | GPT only; preset (`landscape_4_3`) or `WIDTHxHEIGHT` |
| `--quality` | no | `medium` via config | GPT only; `low`, `medium`, `high` |
| `--num-images` | no | 1 | 1-4 |
| `--output-format` | no | `png` | `jpeg`, `png`, `webp` |
| `--output-dir` | no | - | local path |
| `--filename` | no | `generated` | base filename |
| `--web-search` | no | false | Nano only; ignored for GPT |

### edit.sh

Nano Banana example:

```bash
sh scripts/edit.sh \
  --model "gemini" \
  --prompt "combine these into a collage" \
  --image-urls "https://example.com/img1.png,https://example.com/img2.png" \
  --aspect-ratio "16:9" \
  --output-dir "./images" \
  --filename "collage"
```

GPT Image 2 example:

```bash
sh scripts/edit.sh \
  --model "gpt" \
  --prompt "make this product shot look like a premium studio campaign" \
  --image-urls "https://example.com/source.png" \
  --mask-url "https://example.com/mask.png" \
  --image-size "auto" \
  --quality "medium" \
  --output-dir "./images" \
  --filename "studio_edit"
```

| Param | Required | Default | Notes |
|-------|----------|---------|-------|
| `--prompt` | yes | - | edit instruction |
| `--image-urls` | yes | - | comma-separated URLs |
| `--model` | no | config / Nano Banana fallback | `nano-banana`, `google`, `gemini`, `gpt`, `openai`, or exact endpoint |
| `--mask-url` | no | - | GPT edit only; optional mask for targeted edits |
| `--aspect-ratio` | no | `auto` | Nano native; for GPT used only when `--image-size` is omitted |
| `--resolution` | no | `1K` | Nano native; for GPT used only when `--image-size` is omitted |
| `--image-size` | no | derived from ratio/resolution / `auto` | GPT only |
| `--quality` | no | `medium` via config | GPT only |
| `--num-images` | no | 1 | 1-4 |
| `--output-format` | no | `png` | `jpeg`, `png`, `webp` |
| `--output-dir` | no | - | local path |
| `--filename` | no | `edited` | base filename |

### upload.sh

```bash
# Get hosted URL for local file
URL=$(sh scripts/upload.sh --file /path/to/image.png)

# Get base64 data URI for manual API work
URI=$(sh scripts/upload.sh --file /path/to/image.png --base64)
```

## Cost Guidance

- **Nano Banana Pro** is the cheaper and safer default for quick iterations
- **GPT Image 2** cost depends heavily on `quality` and `image_size`
- this skill defaults GPT to `medium` quality to reduce surprise spend

For current pricing, check fal's model pages in [config/README.md](config/README.md).

## Notes

- result URLs expire in roughly one hour — download locally if you need persistence
- uploaded files on fal storage are temporary
- `edit.sh` now polls the same `/edit` queue endpoints documented by fal
