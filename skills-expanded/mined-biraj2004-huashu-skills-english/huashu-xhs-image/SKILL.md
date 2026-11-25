---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |
|-------|------------|---------|
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |
|-------|------------|---------|
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |
|-------|------------|---------|
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |
|-------|------------|---------|
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |
|-------|------------|---------|
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-xhs-image
description: |
  Generate high-quality images for Xiaohongshu (Little Red Book) posts. Default path is AI-generated (Gemini); HTML is only used as fallback for precise data tables. Use when the user mentions "Xiaohongshu images", "Xiaohongshu cover", "Xiaohongshu pictures", "make a Xiaohongshu image", or "post illustrations".
---

# Xiaohongshu Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

---

## Huashu's Design Aesthetic Profile

### What He Likes

- **Texture and warmth** — Organic elements such as paper folds, handwritten strokes, stamps, washi tape
- **Handwritten / calligraphic fonts** — Notebook feel; especially effective for personal sharing scenarios
- **Text filling the canvas** — Xiaohongshu is a mobile vertical screen; text must be large enough to read at a glance
- **Core element emphasis** — Key numbers / keywords as visual heroes (3× enlarged, colour-changed, decorated)
- **Clear structure** — Main title > subtitle > list; distinct hierarchy
- **Warm colour tones** — Cream, warm orange, warm gold perform well

### What He Dislikes

- **HTML screenshots** — Too flat, feels like a PowerPoint template, soulless (only use as precise data table fallback)
- **Cyber-neon / dark blue backgrounds** — #0D1117 and similar dark blues are an aesthetic no-go zone
- **Signature / watermark** — Cover images must not include "Huashu" or "@Huashu"
- **Excessive blank space** — Better to be fuller than sparse and empty

### Proven Good Styles

| Style | Performance | Best For |
|-------|------------|---------|
| Hand-drawn notebook (warm paper + calligraphy + hand-drawn icons) | ⭐⭐⭐⭐⭐ | Tutorials, tips, personal sharing |
| Dark gold poster (dark background + gold large text) | ⭐⭐⭐⭐ | Product launches, impactful titles (needs strong content) |
| Minimalist infographic (light background + large numbers + clean hierarchy) | ⭐⭐⭐⭐ | Data-driven, comparisons |

---

## Core Parameters

| Parameter | Value |
|-----------|-------|
| Standard dimensions | 1080 × 1440 px (3:4) |
| AI generation resolution | `--resolution 2K` |
| AI Prompt aspect ratio declaration | `3:4 portrait aspect ratio, 1080x1440 pixels` |
| HTML viewport (fallback) | `--viewport-size=1080,1440` |

---

## Step 1: Understand the Content

Read the user-provided content and quickly extract:

- **Theme**: What is this post about?
- **Core keywords**: Which words / numbers need to be visual heroes?
- **Mood / tone**: Suspense? Informative? Warm? Impactful?
- **Image count and type**: Single cover / carousel set / infographic?

No need to show the analysis to the user — proceed directly to Step 2.

---

## Step 2: Design Proposal ✅ Must Wait for User Selection

**This is the most critical step in the entire workflow. Never skip it.**

### Proposal Format

Present **2–3 design directions** to the user, each including:

```text
### Direction A: [Style Name]
- Visual style: [One sentence describing the visual feel, e.g., "warm cream notebook paper + brush calligraphy headline + hand-drawn icons"]
- Colour palette: [Background + primary colour + accent colour]
- Copy layout: [Which text is enlarged as the hero, which is subtitle, overall arrangement]
- Mood: [The first feeling the viewer gets]
```

### Proposal Principles

1. **Each direction must be clearly different** (style, mood, and colour must differ on at least one dimension)
2. **Mark recommendations** (explain why a particular direction is recommended based on the content)
3. **Be specific about copy** (not "title enlarged" — say "the number '28' as a 200px hero element in orange")
4. **No more than 3 directions** (too many choices makes selecting harder)

### Proposal Example

> **Direction A: Hand-drawn Notebook Style (Recommended)**
>
> - Visual style: Cream grid paper background + brush calligraphy headline + hand-drawn tech icons
> - Colour palette: Background #FDF6EC + Primary #D97706 (warm orange) + emphasis circles
> - Copy layout: "Ali C4 Building" and "A Bunch of People from Guangdong Arrived" fill the upper half as heroes; "AI Open-Source Champion" in orange as the visual anchor; bottom right "Qianwen App" stamp
> - Mood: Friendly, authentic, like a friend sharing insider news

> **Direction B: Dark Gold Reveal Style**
>
> - Visual style: Dark frosted background + gold large text + badge decoration
> - Colour palette: Background #1A1A1A + Primary #E2B714 (gold) + white as support
> - Copy layout: "Global AI Open-Source Champion" in gold fills the canvas; "Big Tech Insider" gold badge at top; white subtitle below
> - Mood: Impactful, insider feel, authoritative

**Only proceed to Step 3 after the user has made a selection.** The user might:

- Select one directly → Proceed to generation
- Ask for a mix / adjustments → Modify the direction and re-confirm
- Be unhappy with all options → Ask for preferences and re-propose

---

## Step 3: Generate Images

### Build the Prompt

Based on the user's chosen direction, build a complete prompt.

**Prompt template:**

```text
Create a [style] cover for a Xiaohongshu post. 3:4 portrait aspect ratio, 1080x1440 pixels, high quality rendering.

VISUAL STYLE: [Expand from the visual style description in the proposal]
COLOR PALETTE: [Specific colour description]
TYPOGRAPHY: text fills most of the canvas, oversized bold typography, clear visual hierarchy.

TEXT TO RENDER:
- [Main title — hero element, visually dominant]
- [Subtitle]
- [Other text elements]

The word/number "[core keyword]" is visually dominant, 3x larger than other text, with decorative emphasis.

IMPORTANT: Do NOT include any personal signature, watermark, or author name.

[1–2 sentences describing the mood / atmosphere of the image]
```

**Key prompt keywords (add as needed):**

- Large text → `text fills most of the canvas, oversized bold typography`
- Core emphasis → `the word/number "XX" is visually dominant, 3x larger than other text, with decorative emphasis`
- Handwriting → `handwritten style Chinese text / brush calligraphy lettering`
- Paper texture → `warm cream paper texture with subtle grid lines, notebook page feel`
- Clear hierarchy → `clear visual hierarchy with distinct heading, subheading, and list levels`
- No signature → `Do NOT include any personal signature, watermark, or author name`

### Two Generation Paths (Always Provide Both)

| Path | Tool | Advantages | Disadvantages | Cost |
|------|------|-----------|--------------|------|
| **AI-generated** | Gemini Pro Image | Good texture, warmth, rich visuals | Chinese characters may render incorrectly | API cost per image |
| **HTML screenshot** | Playwright | Text 100% accurate, zero cost, batch-capable | Flat, lacks texture | Free |

**Always provide both paths so the user can compare.** HTML is zero cost, so multiple colour / layout variants can be generated per direction. AI path — 1 image per direction is sufficient.

### File Organisation (Must Follow)

When generating multiple versions, all related files (PNG + HTML source) go in **the same subfolder**:

```text
[Article directory]/
├── article.md
└── [article-short-name]-xhs-images/          ← Subfolder
    ├── A-notebook-AI.png
    ├── A1-notebook-HTML-warm.png
    ├── A1-notebook-HTML-warm.html
    ├── B-newspaper-AI.png
    └── ...
```

**Naming convention**: `[Direction letter][Variant number]-[Style name]-[Path AI/HTML]-[Variant description].png`

- Direction letter: A/B/C (matching the design proposals)
- AI path — no variant number: `A-notebook-AI.png`
- HTML variants — with variant number: `A1-notebook-HTML-warm.png`, `A2-notebook-HTML-green.png`
- Folder name uses the article keyword: `[keyword]-xhs-images/`

### AI Generation Command

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/xhs-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[direction]-[style]-AI.png" \
  --resolution 2K
```

After generation, move to the images subfolder. Sets can be generated in parallel (`run_in_background=true`).

---

## Step 4: Preview Confirmation

### Browser Preview (Required)

After generation, open all images with the `open` command so the user can compare side by side:

```bash
open "[image path 1]" "[image path 2]" "[image path 3]"
```

### Inline Preview

Also display generation results inline using the Read tool.

**Basic checks:**

1. Are the Chinese characters rendered correctly?
2. Is the ratio 3:4 portrait orientation?
3. Does the style match the selected direction?
4. Does it include any signature or watermark?

### Design Review (Required)

Score each image on two dimensions (out of 10) and provide optimisation directions:

| Dimension | Criteria |
|-----------|---------|
| **Design Score** | Visual hierarchy, typography, colour harmony, texture, creativity |
| **Xiaohongshu Appeal** | Does it stand out in the feed? Is the text large enough? Information density, emotional communication, does it spark curiosity? |

**Review output format:**

- Per image: Overall score + 1-sentence core evaluation + 1 optimisation direction
- Final summary ranking table with recommendations highlighted
- The user can decide whether to adopt the optimisation suggestions

**User feedback handling:**

- Satisfied → Step 5 upload
- Text errors → Use HTML rendering as fallback for that image
- Style wrong → Adjust prompt and regenerate
- Major direction change → Return to Step 2 for a new proposal

---

## Step 5: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link.

---

## HTML Screenshot Path (For AI text rendering failures, precise data tables, or user-requested comparisons)

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=1080,1440 --wait-for-timeout=1000
```

HTML template requirements:

- Canvas: `width: 1080px; height: 1440px`
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Safe zone: 80px top/bottom, 60px left/right

---

## Quick Reference

### Chinese Text Rendering Limits (AI Path)

- Main title: ≤ 7 characters
- Subtitle: ≤ 15 characters
- Body text: ≤ 20 characters per line
- Verify every image individually

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best For |
|--------|-----------|---------|--------|---------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content |

### Golden Rules

- Title: large, bold, prominent (occupies 30–50% of canvas)
- Core numbers / keywords as visual emphasis (enlarged, coloured, decorated)
- Cover information density → sparks curiosity
- Carousel sets maintain consistent style
- Vertical 3:4, making full use of screen real estate
- No signature / watermark

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
) {
        " $cell "
      } else {
        " $cell "
      }
    }
    '|' + ($fixedCells -join '|') + '|'
  
| `wechat-image` | WeChat article images (sister skill) |
| `image-to-slides` | PPT images (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — Xiaohongshu platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
