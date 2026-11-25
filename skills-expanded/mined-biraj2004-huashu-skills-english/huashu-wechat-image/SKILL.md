---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-wechat-image
description: |
  Generate high-quality images for WeChat Official Account articles. Supports cover images (2.35:1), body illustrations (16:9 / 4:3), and infographics. Provides two paths: AI-generated (visually creative) and HTML-rendered (text-precise). Use when the user mentions "official account images", "article cover", "body illustrations", or "article images".
---

# WeChat Article Image Workflow

## ⚠️ Core Principle: Propose First, Then Generate

**Never skip the design proposal and jump straight to generating.** The correct workflow:

```text
Understand content → Design proposal (2–3 directions) → User selection → Generate → Preview confirmation → Upload
```

Design aesthetic profile and proposal format are shared with the sister skill `xhs-image/SKILL.md` — applicable here too.

## Core Parameters

| Image Type | Dimensions | Ratio | Playwright Viewport | AI Prompt Aspect Ratio Declaration |
|-----------|-----------|-------|--------------------|------------------------------------|
| Top cover | 1800 x 766 px | 2.35:1 | `--viewport-size=1800,766` | `2.35:1 ultra-wide landscape, 1800x766 pixels` |
| Wide body image | 1920 x 1080 px | 16:9 | `--viewport-size=1920,1080` | `16:9 landscape, 1920x1080 pixels` |
| Square body image | 1440 x 1080 px | 4:3 | `--viewport-size=1440,1080` | `4:3 landscape, 1440x1080 pixels` |
| Infographic | 1080 x variable | variable | `--viewport-size=1080,N` | Per content |

---

## Step 0: Determine Image Requirements ✅ User Confirmation

**Present options to the user and wait for confirmation:**

| Type | Description | Number of Images | Recommended Path |
|------|-------------|-----------------|-----------------|
| **A. Cover only** | Top cover image | 1 | AI-generated |
| **B. Body images** | Chapter illustrations to aid reading comprehension | 3–8 | AI-generated (primary) |
| **C. Full set** | Cover + all body images | 4–10 | AI-generated (primary) |
| **D. Infographics only** | Data comparisons, flowcharts, checklists | 1–5 | AI-generated (precise data tables via HTML as fallback) |

**Ask the user**:

1. Cover only, body images, or a full set?
2. What is the article path / content? (to analyse content and determine image placement)
3. How many images in total?

### Image Quantity Recommendation

| Article Length | Recommended Image Count | Includes |
|---------------|------------------------|----------|
| < 1,500 words | 2–3 | Cover + 1–2 body images |
| 1,500–3,000 words | 4–6 | Cover + 1 per core section |
| 3,000–5,000 words | 6–8 | Cover + section images + infographic |
| > 5,000 words | 8–10 | No more than 10 — avoid excessive interruption |

---

## Step 1: Style Selection ✅ User Confirmation

**Based on the user's article type, recommend 3 styles to choose from.**

### Automatic Recommendation by Article Type

| Article Type | First Choice | Second Choice | Third Choice |
|-------------|-------------|--------------|-------------|
| AI tool review | Minimalist Professional | Editorial Magazine | Data Infographic |
| Technical tutorial | Minimalist Professional | Hand-drawn Whiteboard | Editorial Magazine |
| Product launch | Editorial Magazine | Bold Poster | Minimalist Professional |
| Deep analysis | Editorial Magazine | Data Infographic | Minimalist Professional |
| Personal story | Warm Snoopy illustration | Warm Narrative | Editorial Magazine |
| Industry observation | Bold Poster | Editorial Magazine | Data Infographic |

**Present 3 recommended styles to the user**, each including:

- Style name + one-line description
- Best for
- Colour tendencies

**Ask the user**: Which style do you prefer? Or do you have a reference in mind?

**Full style library**: `references/style-gallery.md`

---

## Step 2: Choose a Generation Path ✅ User Confirmation

**Recommend a path based on content characteristics; present a comparison to the user:**

| | Path A: HTML → Screenshot | Path B: AI-generated |
|---|---|---|
| **Text accuracy** | 100% (code-controlled) | Chinese characters may render incorrectly (must verify) |
| **Layout control** | Pixel-perfect | AI has creative freedom |
| **Visual creativity** | Medium (depends on design skill) | High (AI is creative) |
| **API cost** | Zero (fully local) | Consumes Gemini API per image |
| **Speed** | Fast (seconds) | Slow (10–30 seconds per image) |
| **Best for** | Text-heavy, data-heavy, checklists, infographics | Covers, atmosphere images, creative illustrations |
| **Editability** | Edit HTML and re-screenshot | Must regenerate |
| **Dark mode** | CSS directly controls colour | Declare in prompt |

### ⚠️ Huashu's Preference: AI-Generated First

> HTML screenshots feel flat — like a PowerPoint template; lacking texture and design quality. AI-generated images have rich visual detail, far superior quality to HTML.
> **Default to AI-generated; only use HTML as fallback for "complex data tables requiring word-for-word precision".**

### Path Recommendation Rules

| Image Type | Recommended Path | Reason |
|-----------|-----------------|--------|
| Top cover | **AI** | Stronger visual impact; better texture |
| Body atmosphere / scene images | **AI** | Greater creativity |
| Body infographics | **AI** | AI can produce design-quality infographics |
| Flowcharts / step diagrams | **AI** | AI adds visual hierarchy |
| Comparison charts | **AI** | Higher visual quality |
| Precise data tables (10+ cells) | **HTML** | The only scenario that needs HTML: large quantities of precise numbers |

**Default to recommending AI path — no longer asking about path each time.**

---

## Step 3: Generate Images

### Path A: HTML → Playwright Screenshot

#### 3-A-1. Create HTML

Based on the selected style and user-provided content, generate an HTML file.

**HTML template requirements:**

- Canvas size: Select based on image type (cover 1800×766, wide body 1920×1080, square body 1440×1080)
- Font: `font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif`
- Dark mode friendly: Use #F5F5F5 instead of pure white; use #1A1A2E instead of pure black
- Cover safe zone: Core information concentrated in the central square area (766×766)

**Cover poster template example (2.35:1):**

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1800px; height: 766px;
    background: #1A1A2E;
    display: flex; flex-direction: column;
    justify-content: center; align-items: center;
    padding: 60px 400px;
    font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  }
  .title {
    font-size: 96px; font-weight: 900;
    color: #FFFFFF; text-align: center;
    line-height: 1.3; letter-spacing: 4px;
  }
  .subtitle {
    font-size: 36px; font-weight: 400;
    color: #E2B714; text-align: center;
    margin-top: 30px;
  }
  .accent-line {
    width: 200px; height: 4px;
    background: #E2B714;
    margin: 30px auto;
  }
</style>
</head>
<body>
  <div class="title">Claude vs Codex</div>
  <div class="accent-line"></div>
  <div class="subtitle">A Power User's 20-Minute Real-World Comparison</div>
</body>
</html>
```

#### 3-A-2. Screenshot

```bash
npx playwright screenshot "file:///path/to/card.html" output.png \
  --viewport-size=[width],[height] --wait-for-timeout=1000
```

- Cover: `--viewport-size=1800,766`
- Wide body: `--viewport-size=1920,1080`
- Square body: `--viewport-size=1440,1080`

#### 3-A-3. ✅ Preview Confirmation

Present the screenshot result to the user using the Read tool.

**Ask the user**:

- Is the text content correct?
- Are the layout and colours satisfactory?
- Is the core information in the safe zone? (cover images specifically)
- Any adjustments needed?

**If adjustments needed**: Edit HTML → Re-screenshot → Confirm again. (HTML path iteration is very low cost)

---

### Path B: AI-Generated (Gemini Pro Image)

#### 3-B-1. Build the Prompt

**Cover Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: 2.35:1 ultra-wide landscape, 1800x766 pixels, high quality rendering.
SAFE ZONE: Center square (766x766) contains all key text and visuals.
COLOR SYSTEM: [Describe colour mood without specifying proportions]
TEXT RENDERING: Text must be large, clear, readable. Title in centre safe zone.
```

**Body Base Style Prompt:**

```text
[Base Style]:
VISUAL REFERENCE: [One sentence describing the specific style aesthetic]
CANVAS: [16:9 landscape, 1920x1080 pixels / 4:3 landscape, 1440x1080 pixels], high quality rendering.
COLOR SYSTEM: [Describe colour mood]
DARK MODE: Use medium-tone backgrounds, avoid pure white (#FFFFFF) and pure black (#000000).
```

**Per-Image Prompt:**

```text
Create a [style] [cover/illustration] for a WeChat article about [topic].

[Base Style]

DESIGN INTENT: [What emotion or action should the viewer feel/take upon seeing this]

TEXT TO RENDER:
- Title: "[Title — cover ≤10 characters; body image can be shorter or none]"
- [Other text elements]

[1–2 sentences describing the mood/atmosphere of the image, allowing AI creative freedom in composition]
```

#### 3-B-2. ✅ Prompt Confirmation

**Show the user the prompt you're about to use**, and wait for confirmation or modification. Specifically confirm:

- Is the text content to be rendered correct?
- Is the design intent accurate?
- Any other requirements?

#### 3-B-3. Generate

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run /path/to/skills/wechat-image/scripts/generate_image.py \
  --prompt "[full prompt]" \
  --filename "[timestamp]-wechat-[type]-[description].png" \
  --aspect [cover|wide|standard|square]
```

- `--aspect cover` → 2.35:1 top cover
- `--aspect wide` → 16:9 wide body image (default)
- `--aspect standard` → 4:3 square body image
- `--aspect square` → 1:1 square

Multiple images can be generated in parallel (`run_in_background=true`).

#### 3-B-4. ✅ Preview Confirmation

Present the generation results to the user using the Read tool.

**Check:**

1. Is the text accurate? (no garbled or incorrect characters)
2. Is the ratio correct? (cover 2.35:1; body 16:9 or 4:3)
3. Cover safe zone: Is the core information in the central square? (cover images)
4. Dark mode: Is pure white or pure black background avoided?
5. Is the style satisfactory?

**Ask the user**: Satisfied / Regenerate / Adjust prompt?

---

### Path C: Mixed Path (Recommended for Full Sets)

Best for full sets: **Cover uses AI-generated (eye-catching), body infographics use HTML rendering (information-precise), body atmosphere images use AI-generated**.

Execution order:

1. Generate cover using Path B → User confirmation
2. Extract consistent colour / mood from the cover
3. Body atmosphere images using Path B → User confirmation
4. Body infographics / data charts using Path A → User confirmation

---

## Step 4: Upload to Image Host

```bash
python3 /path/to/tools/upload_image.py "[image path]"
```

Returns a permanent ImgBB link. **WeChat articles must use network links** — local paths break after publishing.

---

## Quick Reference

### Cover Safe Zone

```text
┌─────────────────────────────────────┐
│          │ 766x766  │               │
│  Decor   │  Safe    │  Decor        │ 1800 x 766
│          │  Zone    │               │
└─────────────────────────────────────┘
           ↑ Moments crop zone ↑
```

### Dark Mode Adaptation

- Use #F5F5F5 (light grey) instead of pure white
- Use #1A1A2E (dark purple-grey) instead of pure black
- Body text: use #595959 or #3F3F3F, not pure black #000000
- Avoid shadow effects and white borders
- Use low-saturation colours

### Chinese Text Rendering (AI Path)

- Cover title: ≤ 10 characters
- Body image text: ≤ 20 characters per line
- Data-heavy infographic text: HTML rendering more reliable
- Verify each image individually

### Font Recommendations (HTML Path)

- Headings: `"PingFang SC"` Bold / `"Microsoft YaHei"` Bold
- Body: `"PingFang SC"` Regular

### Huashu Tech Account Colour Palette

| Scheme | Background | Primary | Accent | Best for | Dark Mode |
|--------|-----------|---------|--------|---------|----------|
| Warm Grey Professional | #F5F0EB | #D97706 | #4A90D9 | AI tools, sharing | Good |
| Minimalist Professional | #F5F5F5 | #4A90D9 | #FF6B35 | Tutorials, comparisons | Medium |
| Dark Night Gold | #1A1A2E | #E2B714 | #FFFFFF | Product launches | Good |
| Terminal Green | #1A1A1A | #00FF41 | #888888 | Programming content | Good |

### Golden Rules

- Cover core information in the central square safe zone
- Body images use mid-tone backgrounds (dark mode compatibility)
- Infographics: HTML → Screenshot first (text precision)
- Atmosphere images: AI-generated first (stronger creativity)
- Upload images to an image host for permanent links
- Illustrations within the same article maintain consistent style
- 1 image per 800–1,200 words
- At least 1 image per H2 section

### Image Placement Strategy

| Position | Necessity | Type |
|----------|-----------|------|
| Below title (cover) | Required | Cover / atmosphere image |
| After each H2 heading | Recommended | Section illustration |
| Data / comparison sections | Recommended | Infographic |
| Product / tool introductions | Optional | Screenshot / AI concept image |
| Before article closing | Optional | Closing illustration |

### Decision Flowchart

```text
User requirement → Step 0 confirm requirements
                        ↓
                 Step 1 select style (present 3 options)
                        ↓
                 Step 2 default AI-generated (HTML only for precise data tables)
                        ↓
                 Step 3 generate → preview → user confirmation
                   ├→ Satisfied → Step 4 upload
                   ├→ Text rendering error → Use HTML fallback for that image
                   └→ Not satisfied → Adjust prompt and regenerate
```

## Related Skills

| Skill | Purpose |
|-------|---------|
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

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
  
| `xhs-image` | Xiaohongshu image creation (sister skill) |
| `image-to-slides` | PPT image creation (source of style library) |

## Reference Files

- `references/style-gallery.md` — Full style library and prompt templates
- `references/design-guidelines.md` — WeChat platform design specifications

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
