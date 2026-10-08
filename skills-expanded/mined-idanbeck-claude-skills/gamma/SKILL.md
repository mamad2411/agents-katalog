---
name: gamma-skill
description: Generate presentations, documents, webpages, and social content using Gamma AI. Supports card dimensions, headers/footers, sharing, multiple image sources, and PDF/PPTX export.
allowed-tools: Bash, Read
---

# Gamma Skill - Presentation Generation (v2.0)

Generate presentations, documents, webpages, and social content using Gamma's API v1.0.

## First-Time Setup (~2 minutes)

### 1. Get API Access

Gamma API requires a **Pro, Ultra, Teams, or Business** account.

1. Go to [Gamma Settings](https://gamma.app/settings)
2. Navigate to **Members** tab
3. Click **API key** tab
4. Click **Create key**
5. Copy the key (format: `sk-gamma-xxxxxxxx`)

### 2. Save API Key

```bash
echo '{"api_key": "sk-gamma-YOUR-KEY-HERE"}' > ~/.claude/skills/gamma-skill/config.json
```

## Commands

### Generate Presentation/Document

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate "Your content here" [options]
```

**From file:**
```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate --file notes.md --wait
```

**Core Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--format` / `-f` | presentation, document, webpage, social | presentation |
| `--text-mode` / `-m` | generate, condense, preserve | generate |
| `--theme` / `-t` | Theme ID | (Gamma default) |
| `--auto-theme` / `-T` | Auto-detect preferred theme (zerg, etc.) | false |
| `--num-cards` / `-n` | Number of slides (1-60 Pro, 1-75 Ultra) | (auto) |
| `--instructions` / `-i` | Additional specs (max 2000 chars) | |
| `--export-as` / `-e` | pdf or pptx | |
| `--folder` | Folder ID to save to | |
| `--card-split` | auto or inputTextBreaks | auto |
| `--wait` / `-w` | Wait for completion | false |
| `--timeout` | Max wait seconds | 300 |

**Text Options:**

| Flag | Description | Values |
|------|-------------|--------|
| `--tone` | Content tone | any text (professional, casual, etc.) |
| `--audience` | Target audience | any text |
| `--language` | Output language | ISO code (en, he, es, fr, etc.) |
| `--text-amount` | Text density per card | brief, medium, detailed, extensive |

**Image Options:**

| Flag | Description | Values |
|------|-------------|--------|
| `--image-source` | Where images come from | aiGenerated, pictographic, pexels, giphy, webAllImages, webFreeToUse, webFreeToUseCommercially, placeholder, noImages |
| `--image-model` | AI image model | (default: gemini-2.5-flash-image) |
| `--image-style` | Visual style description | any text (max 500 chars) |
| `--no-images` | Disable all images | |

**Card Options:**

| Flag | Description | Values |
|------|-------------|--------|
| `--dimensions` / `-d` | Card dimensions | presentation: fluid/16x9/4x3; document: fluid/pageless/letter/a4; social: 1x1/4x5/9x16 |
| `--header-footer` | Header/footer items | position:type[:value] (repeatable) |
| `--hf-hide-first` | Hide header/footer on first card | |
| `--hf-hide-last` | Hide header/footer on last card | |

Header/footer positions: topLeft, topRight, topCenter, bottomLeft, bottomRight, bottomCenter
Header/footer types: text, image, cardNumber

**Sharing Options:**

| Flag | Description | Values |
|------|-------------|--------|
| `--share` | Email addresses to share with | space-separated emails |
| `--share-access` | Access for shared users | view, comment, edit, fullAccess |
| `--workspace-access` | Workspace member access | noAccess, view, comment, edit, fullAccess |
| `--external-access` | External user access | noAccess, view, comment, edit |

### Create from Template

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py from-template GAMMA_ID "Your content" [options]
```

Get template ID from the Gamma URL (e.g., `gamma.app/docs/GAMMA_ID`).

Supports: `--theme`, `--folder`, `--export-as`, `--image-model`, `--image-style`, all sharing options, `--wait`.

### Check Generation Status

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py status GENERATION_ID
```

### Get Export URLs

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py export GENERATION_ID
```

Returns PDF/PPTX download URLs (temporary, re-run if expired).

### List Themes

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py themes [--limit N] [--search QUERY]
```

### List Folders

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py folders
```

## Examples

### Pitch Deck with Branding

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  "Zerg AI: AI-powered kernel generation.
   Problem: Custom hardware drivers are expensive.
   Solution: AI generates optimized kernels automatically.
   Market: $50B embedded systems market.
   Traction: 3 enterprise pilots." \
  --format presentation \
  --dimensions 16x9 \
  --num-cards 10 \
  --tone professional \
  --audience investors \
  --header-footer "bottomRight:text:Zerg AI" "topLeft:image:https://zergai.com/logo.png" \
  --hf-hide-first \
  --auto-theme \
  --export-as pdf \
  --wait
```

### From Obsidian Notes

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  --file ~/vault/Writing/pitch-notes.md \
  --format presentation \
  --instructions "Focus on the problem and solution. Use data visualizations." \
  --export-as pptx \
  --wait
```

### Social Media Cards

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  "5 ways AI is transforming embedded systems" \
  --format social \
  --dimensions 4x5 \
  --text-amount brief \
  --image-source pexels \
  --wait
```

### Stock Photos Instead of AI Images

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  "Company all-hands Q1 review" \
  --format presentation \
  --image-source pexels \
  --tone casual \
  --audience "engineering team" \
  --wait
```

### Share with Team

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  "Sprint retrospective - Q1 Week 11" \
  --format document \
  --share alice@company.com bob@company.com \
  --share-access edit \
  --workspace-access view \
  --wait
```

### A4 Document

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  --file ~/vault/Epoch/report.md \
  --format document \
  --dimensions a4 \
  --text-mode preserve \
  --export-as pdf \
  --wait
```

### Remix a Template

```bash
python3 ~/.claude/skills/gamma-skill/gamma_skill.py from-template g_abc123def456 \
  "Update with our Q1 2026 metrics: ARR $2M, 15 enterprise customers, NPS 72" \
  --export-as pdf \
  --share investor@firm.com \
  --share-access view \
  --wait
```

## Text Modes

| Mode | Description |
|------|-------------|
| `generate` | AI expands your notes into full content |
| `condense` | AI summarizes your content |
| `preserve` | Keep your text mostly as-is, just format it |

## Image Sources

| Source | Description |
|--------|-------------|
| `aiGenerated` | AI-generated images (default, uses credits) |
| `pictographic` | Icon/illustration style |
| `pexels` | Stock photos from Pexels |
| `giphy` | GIFs from Giphy |
| `webAllImages` | Web image search |
| `webFreeToUse` | Free-to-use web images |
| `webFreeToUseCommercially` | Commercially licensed web images |
| `placeholder` | Placeholder images |
| `noImages` | No images at all |

## Custom Images (via Google Drive)

The Gamma API doesn't have a dedicated image upload endpoint. To use your own images (AI-generated, diagrams, screenshots):

1. **Generate or obtain your image** (e.g., via nano-banana-pro skill)
2. **Upload to Google Drive** using the google-docs-skill:
   ```bash
   python3 ~/.claude/skills/google-docs-skill/docs_skill.py upload-image /path/to/image.png
   ```
3. **Use the `directUrl`** (lh3.googleusercontent.com format) in your inputText:
   ```
   Use this image: https://lh3.googleusercontent.com/d/FILE_ID
   ```
4. **Set `--image-source noImages`** so Gamma uses only your provided URLs

**Important:** Only `lh3.googleusercontent.com/d/{id}` URLs work. The `drive.google.com/uc?export=view` format does a 303 redirect that Gamma cannot follow.

### Full Pipeline Example

```bash
# 1. Generate image
python3 ~/.claude/skills/nano-banana-pro/generate_image.py "circuit board closeup" --output /tmp/imgs

# 2. Upload to Drive (returns lh3 direct URL)
python3 ~/.claude/skills/google-docs-skill/docs_skill.py upload-image /tmp/imgs/image.png

# 3. Embed URL in content and generate deck
python3 ~/.claude/skills/gamma-skill/gamma_skill.py generate \
  "Title slide. Use this image: https://lh3.googleusercontent.com/d/FILE_ID ..." \
  --image-source noImages --wait
```

## Credit System

Gamma uses credits for generation:

- **Slides:** 3-4 credits each
- **AI Images:** 2-120 credits depending on model
- **Pro:** ~400 credits/month
- **Ultra:** ~1000 credits/month

Use `--image-source pexels` or `--no-images` to conserve credits.

## Requirements

- Python 3.9+
- No external dependencies (uses stdlib only)
- Gamma Pro/Ultra/Teams/Business account

## Security Notes

- API key stored in `~/.claude/skills/gamma-skill/config.json` (gitignored)
- Key can be revoked in Gamma Settings > Members > API key
- No OAuth - simple API key authentication
