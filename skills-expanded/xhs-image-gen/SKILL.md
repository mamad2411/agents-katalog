---
name: xhs-image-gen
description: Generate Xiaohongshu (小红书) carousel images (3:4, 1080x1440) from structured content. Creates professional slide decks with Chinese typography and proper XHS formatting. Triggers on "做小红书图", "xhs images", "generate xhs slides", "小红书配图", "carousel images", or any XHS image generation request.
inputs:
  - name: content_json
    type: json
    required: true
    description: Structured JSON with a slides array — each slide has title, body, and optional image_hint fields
outputs:
  - name: image_files
    type: list
    description: List of file paths to the generated PNG carousel images (1080x1440, 3:4 ratio)
---

# XHS Image Generator Skill

Generate professional Xiaohongshu carousel images from structured content JSON. Outputs 3:4 vertical PNGs (1080x1440) with Chinese typography, ready for upload.

---

## Setup

**Clone the skill:**
```bash
git clone https://github.com/PHY041/claude-agent-skills
cd claude-agent-skills/skills/xhs-image-gen
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

**Optional — AI cover generation (uses fal.ai):**
```bash
export FAL_API_KEY="your_fal_api_key"
```

---

## Quick Start

```bash
# Template-only (fast, free)
venv/bin/python3 generate.py content.json --output /tmp/xhs-output/

# AI cover + template content (recommended)
FAL_API_KEY="..." venv/bin/python3 generate.py content.json --ai-cover --output /tmp/xhs-output/
```

---

## Workflow

### Step 1: Understand the Topic

When user asks to create XHS content for topic X:
1. Understand the topic and target audience
2. Plan 4-6 slides (cover + 2-4 content + summary)
3. Choose appropriate template

### Step 2: Decide on Cover Style

| Mode | Flag | When to Use |
|------|------|-------------|
| **Gradient cover** (default) | _(none)_ | Clean, fast, no API cost |
| **AI cover** | `--ai-cover` | Eye-catching background via fal.ai |

AI cover uses flux/schnell to generate an atmospheric background, applies a dark gradient overlay, and renders white text on top. Content slides always use templates (no AI). Cost: ~$0.003 per cover.

### Step 3: Generate Content JSON

```json
{
  "template": "tutorial",
  "ai_cover": true,
  "slides": [
    {
      "type": "cover",
      "title": "大标题（简短有力）",
      "subtitle": "副标题（补充说明）",
      "tag": "分类标签",
      "author": "@your_handle",
      "ai_prompt": "optional: custom fal.ai prompt for background"
    },
    {
      "type": "content",
      "title": "第一个要点",
      "number": 1,
      "body": "详细说明\n用换行分段\n每段1-2句话",
      "highlight": "可选：重点提示框内容"
    },
    {
      "type": "list",
      "title": "清单/工具列表",
      "items": [
        "第一项 — 简短说明",
        "第二项 — 简短说明",
        "第三项 — 简短说明"
      ]
    },
    {
      "type": "summary",
      "title": "总结",
      "points": [
        "核心收获一",
        "核心收获二",
        "核心收获三"
      ],
      "cta": "关注我获取更多干货"
    }
  ]
}
```

### Step 4: Generate Images

```bash
cat > /tmp/xhs-content.json << 'EOF'
{... your JSON here ...}
EOF

venv/bin/python3 generate.py /tmp/xhs-content.json --output /tmp/xhs-output/
```

### Step 5: Present to User

Show the generated images for review. If approved, they're ready for manual upload to Xiaohongshu.

---

## Available Templates

| Template | Style | Best For |
|----------|-------|----------|
| `tutorial` | White bg, blue accent | How-to, tutorials, step-by-step |
| `dark` | Dark bg, soft blue accent | Tech, dev tools, coding |
| `warm` | Cream bg, amber accent | Lifestyle, personal stories |
| `nature` | Light green bg, green accent | Wellness, growth, nature |
| `coral` | Light pink bg, red accent | Alerts, hot takes, comparisons |

Select with `--template dark` or set `"template": "dark"` in JSON.

### Custom Accent Color

Override with `"accent_color": "#FF6B6B"` in the JSON root.

---

## Content Rules (CRITICAL)

### Slide Count
- **Minimum 3 slides** (cover + 1 content + summary)
- **Optimal 4-6 slides** (XHS algorithm favors multi-image carousels)
- **Maximum 9 slides** (beyond this, completion rate drops)

### Text Length Per Slide
- **Title:** 6-12 characters (Chinese) — must be scannable
- **Body:** 4-6 lines max per slide — don't cram
- **List items:** 8 max per slide
- **CTA:** Under 12 characters

### Language & Tone
- Write in Chinese (simplified)
- 朋友分享 tone — like telling a friend, not marketing
- Short sentences, line breaks between ideas
- Concrete numbers > vague claims ("省90%时间" > "节省大量时间")

### What NOT to Do
- No English-only slides (mixed OK, pure English bad for XHS)
- No walls of text (if body > 6 lines, split into 2 slides)
- No generic AI-sounding language
- No hype words: 颠覆、革命性、10倍、全网最强

---

## CLI Options

```
generate.py <content.json> [--template NAME] [--output DIR] [--ai-cover]
generate.py --list-templates
```

| Flag | Effect |
|------|--------|
| `--ai-cover` | Generate fal.ai background for cover slide |
| `--template` | Template preset (tutorial, dark, warm, nature, coral) |
| `--output` | Output directory (default: ./output) |

**AI cover also activatable via JSON:** set `"ai_cover": true` in the root object.

### Output
- Files named `slide-01-cover.png`, `slide-02-content.png`, etc.
- All 1080x1440px (3:4 vertical)
- PNG format, ready for XHS upload

---

## Example

Test with the bundled example:

```bash
venv/bin/python3 generate.py example.json --output /tmp/xhs-test/
open /tmp/xhs-test/  # Preview on macOS
```
