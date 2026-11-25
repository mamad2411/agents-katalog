---
name: hero-image-pipeline
description: "Generates publication-ready hero images for Substack articles and LinkedIn posts. Fully automated: reads the article, generates a Gemini AI scene (no text), crops to exact dimensions, composites bold Oswald text overlay via HTML+Playwright, and validates contrast with UX Knowledge. Use this skill whenever creating hero images, article covers, social media images, newsletter headers, or any branded visual content for publishing. Also use when the user mentions needing images for an article, wanting to generate a hero, or preparing visuals for Substack or LinkedIn."
trigger: QHERO
claude_tools: Read, Write, Bash, Glob, mcp__ux-knowledge__check_contrast, mcp__plugin_playwright_playwright__browser_navigate, mcp__plugin_playwright_playwright__browser_take_screenshot, mcp__plugin_playwright_playwright__browser_resize, mcp__plugin_media-pipeline_media-pipeline__create_asset
---

# QHERO — Hero Image Pipeline

Generate publication-ready hero images for Substack and LinkedIn in under 60 seconds. Two-layer approach: AI-generated scene (Gemini, no text) + deterministic Oswald headline overlay (HTML+Playwright), UX-validated.

**This is the default hero pipeline.** When the user says "QHERO", they expect the full Gemini scene + Oswald overlay pipeline — not the typography-only card from QVISUAL's `generate-hero-image.py`. QVISUAL produces simple gradient cards with text; QHERO produces illustrated scenes with composited headlines. Always use QHERO unless the user explicitly asks for a simpler text-only card.

## Why Two Layers

Gemini generates great illustrated scenes but has inconsistent text rendering — font weight, placement, and sizing vary across generations. By generating the scene without any text and overlaying the headline ourselves via HTML, we get:

- Consistent Oswald typography across every hero image
- Editor control over which words are orange vs white
- Exact font sizes with proper hierarchy (1.5-1.67x ratio)
- Pixel-perfect positioning every time
- The ability to change the headline without regenerating the scene

## Pipeline

**Prerequisite:** The headline should be finalized before starting QHERO. Run QHEADLINE first (or confirm the headline with the user) so the overlay text is locked before scene generation begins. Changing the headline after scene generation wastes a Gemini API call.

```
0. HEADLINE → Finalize via QHEADLINE swarm or user confirmation
1. ANALYZE → Read article, extract subtitle, pick scene style + headline split
2. GENERATE → Gemini API creates illustrated scene (NO TEXT in image)
3. CROP → Pillow resizes to exact 1200x630
4. OVERLAY → HTML template adds Oswald headline → Playwright screenshots
5. VALIDATE → UX Knowledge checks contrast ratios
6. OUTPUT → Final PNG
```

## Scene Styles

Two proven styles based on engagement data from past Substack and LinkedIn posts:

### Style 1: Cartoon Panels
Multi-panel cartoon illustration telling a narrative story with **cartoon humans and AI robots** as characters. The scenes tell the story visually in 1-3 panels with imagery and minimal or no words. The humans look like real people (cartoon style, not stick figures) and the robots are friendly/expressive with distinct personalities.

**When to use:** Tutorials, how-tos, step-by-step articles, "X happened then Y" narratives, any article with a clear before/during/after arc.

**Reference images:**
- `content/visuals/reference/comic-strip-robot-protest.jpeg` — 3 panels: robot submits PR → human maintainer rejects → robot protests at podium. Mix of cartoon humans and robots. Warm earth tones, clear panel borders.
- `content/visuals/reference/split-panel-homework-bike.jpg` — 2 panels: kid doing homework (before) → adults mountain biking with translucent AI hologram (after). Cartoon humans with AI element.

**Gemini prompt pattern:**
```
Comic-strip style illustration with [1-3] horizontal panels telling a visual
story, NO TEXT OR CAPTIONS anywhere in the image. Leave the top 20% as empty
dark gradient space for text overlay later.

Panel 1: [cartoon human and/or robot character doing X]
Panel 2: [conflict, change, or contrast]
Panel 3: [resolution — characters together, outcome visible]

Characters: Mix of cartoon humans (realistic proportions, expressive faces) and
friendly AI robots. Warm earth tones with pops of orange, green, and blue.
High detail, crisp lines. The panels should tell the story visually with
minimal or no words. NO TEXT OR CAPTIONS anywhere. 1200x630 pixels.
```

### Style 2: Semi-Realistic Human + Ephemeral AI
A real-looking person in a normal human situation (relaxing, working, riding a bike) with a translucent/holographic AI figure or floating UI elements doing work for them. The human is calm; the AI is active.

**When to use:** Product launches, tool announcements, "AI does X for you" articles, lifestyle-meets-tech.

**Reference images:**
- `content/visuals/reference/photorealistic-openclaw-beach.jpg` — man relaxing on beach, metallic AI figure floating above, chaos of apps/emails on one side, organized summaries on the other
- `content/visuals/reference/photorealistic-beach-research.jpg` — woman on beach with phone, holographic AI figure presenting floating dashboards
- `content/visuals/reference/split-panel-homework-bike.jpg` — kid doing homework (before) vs adults biking with AI hologram (after)

**Gemini prompt pattern:**
```
Semi-realistic illustration, NO TEXT OR CAPTIONS anywhere. Leave the top 20%
as empty dark gradient space for text overlay.

[Scene description: person in relaxed/normal situation, translucent AI figure
or floating holographic UI elements doing work. Warm lighting, sunset/golden
hour tones optional.]

Style: Semi-realistic with slight illustration quality. Warm color palette,
earth tones. The human looks relaxed/confident. The AI element is translucent,
ethereal, glowing softly. Floating UI elements show [dashboards/data/organized
info]. NO TEXT anywhere. 1200x630 pixels.
```

## Step-by-Step Execution

### Step 1: Analyze Article

Read the article and determine:

1. **Headline and subtitle extraction** — Do NOT just grab the first paragraph after H1 (that's often a greeting like "Hello, Sparklers!"). Use this priority order:
   - **Explicit arguments**: If the user passed `--orange` and `--white`, use those directly.
   - **SELECTED line**: Check for an HTML comment block at the top of the article with a `SELECTED:` line. Extract the subtitle after the `|` pipe character. Example: `SELECTED: One Prompt That Turns Meeting Chaos Into Action Items | Brain dump your mess...` → subtitle is "Brain dump your mess..."
   - **Fallback**: Only if neither source exists, use the first non-greeting paragraph after H1.
2. **Scene style** — `cartoon_panels` or `semi_realistic_human_ai`
3. **Scene description** — what the illustration should depict (characters, setting, action, emotion)
4. **Headline split** — which words are orange (hook/provocation) and which are white (resolution/promise). The editor chooses highlighting for maximum impact. Orange = the provocative or surprising part. White = the grounding or resolution.

### Step 2: Generate Scene via Gemini API

**Primary method** — Doppler CLI (reliable, always works):

```bash
GEMINI_API_KEY=$(doppler secrets get GEMINI_API_KEY_PAID --plain -p openclaw -c dev) \
node "$HOME/.claude/plugins/marketplaces/media-pipeline-marketplace/mcp-server/build/cli.bundle.js" \
  --prompt "<scene prompt — MUST include 'NO TEXT OR CAPTIONS anywhere'>" \
  --output "content/visuals/<slug>-scene.png" \
  --aspect-ratio "16:9"
```

**Fallback** — MCP tool `mcp__plugin_media-pipeline_media-pipeline__create_asset`. Note: this tool may return `API_KEY_INVALID` because it uses a separately configured key. If it fails, switch to the Doppler CLI method above.

Critical prompt rules:
- ALWAYS include "NO TEXT OR CAPTIONS anywhere in the image"
- ALWAYS include "Leave the top 20% of the image as empty dark gradient space"
- ALWAYS specify "1200x630 pixels"
- Reference the style patterns above for the chosen style
- Describe characters, setting, action, and emotion specifically

### Step 3: Crop to Exact Dimensions

Gemini outputs vary in size. Crop center and resize to exactly 1200x630:

```bash
python3 -c "
from PIL import Image
img = Image.open('content/visuals/<slug>-scene.png')
target_w, target_h = 1200, 630
target_ratio = target_w / target_h
orig_w, orig_h = img.size
orig_ratio = orig_w / orig_h
if orig_ratio < target_ratio:
    new_h = int(orig_w / target_ratio)
    top = (orig_h - new_h) // 2
    box = (0, top, orig_w, top + new_h)
else:
    new_w = int(orig_h * target_ratio)
    left = (orig_w - new_w) // 2
    box = (left, 0, left + new_w, orig_h)
cropped = img.crop(box)
resized = cropped.resize((target_w, target_h), Image.LANCZOS)
resized.save('content/visuals/<slug>-scene-cropped.png')
"
```

### Step 4: Create HTML Overlay + Render with Playwright

Write an HTML file that composites the Oswald headline over the cropped scene. The Oswald font file must be in the visuals directory:

```bash
cp /Users/travis/Library/Fonts/Oswald-VariableFont_wght.ttf content/visuals/ 2>/dev/null
```

**HTML template** — adjust headline text, orange/white split, and scene filename:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1200, height=630">
<style>
  @font-face {
    font-family: 'Oswald';
    src: url('Oswald-VariableFont_wght.ttf') format('truetype');
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 1200px;
    height: 630px;
    overflow: hidden;
    position: relative;
    font-family: 'Oswald', sans-serif;
    background: #000;
  }
  .bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 1200px;
    height: 630px;
  }
  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 155px;
    background: linear-gradient(180deg, rgba(0,0,0,0.95) 0%, rgba(0,0,0,0.9) 65%, rgba(0,0,0,0.0) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 12px 40px 30px;
    z-index: 2;
  }
  .headline {
    font-family: 'Oswald', Impact, sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    text-align: center;
    line-height: 1.1;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.9), 0 0 20px rgba(0,0,0,0.5);
  }
  /* 1.67x ratio for clear hierarchy */
  .orange { color: #FF6B00; font-size: 60px; }
  .white { color: #FFFFFF; font-size: 36px; }
  /* Arrow baseline fix: Oswald renders → too low. This nudges it up to visually center. */
  .arrow { position: relative; top: -6px; }
</style>
</head>
<body>
  <img class="bg" src="SCENE_CROPPED_FILENAME" alt="">
  <div class="overlay">
    <div class="headline">
      <span class="orange">ORANGE WORDS HERE</span><br>
      <span class="white">WHITE WORDS <span class="arrow">→</span> HERE</span>
    </div>
  </div>
</body>
</html>
```

**Rendering:**

The overlay HTML uses relative paths for the scene image and Oswald font, so the HTTP server must be started from the `content/visuals/` directory:

1. Start local HTTP server **from visuals dir**: `cd content/visuals && python3 -m http.server 8899 &`
2. Set Playwright viewport: `browser_resize` → 1200x630
3. Navigate: `browser_navigate` → `http://localhost:8899/<slug>-overlay.html` (root path, not nested)
4. Screenshot: `browser_take_screenshot` → `content/visuals/<slug>-final.png`
5. Kill server: `lsof -ti:8899 | xargs kill -9 2>/dev/null`

### Step 5: Validate with UX Knowledge

Run contrast checks:

| Check | Foreground | Background | Expected |
|-------|-----------|------------|----------|
| Orange headline on gradient | #FF6B00 | #000000 | 7.36:1 PASS |
| White subtitle on gradient | #FFFFFF | #000000 | 21:1 PASS |

Use `mcp__ux-knowledge__check_contrast` for both. If a check fails (scene has light area bleeding through gradient), increase gradient opacity or height.

Also consider asking UX Knowledge to `review_usability` on the overall composition — it caught the font hierarchy issue (1.27x too close → 1.67x better) in our first run.

### Step 6: Output

Final deliverables:
- `content/visuals/<slug>-scene.png` — raw Gemini output
- `content/visuals/<slug>-scene-cropped.png` — exact 1200x630
- `content/visuals/<slug>-overlay.html` — reusable for text tweaks
- `content/visuals/<slug>-final.png` — publication-ready hero

Report: dimensions confirmed 1200x630, contrast validation results, file paths.

## Headline Typography Rules

- **Font**: Oswald Bold 700, uppercase, letter-spacing 1px
- **Orange line** (#FF6B00): 60px — the hook, provocative statement, or surprising claim
- **White line** (#FFFFFF): 36px — the resolution, promise, or grounding statement
- **Ratio**: 1.67x between orange and white for clear visual hierarchy
- **Text shadow**: `2px 2px 8px rgba(0,0,0,0.9), 0 0 20px rgba(0,0,0,0.5)` for readability over any scene
- **Position**: Top of image, centered, inside dark gradient overlay
- **Gradient**: 155px tall, 95% opacity at top → transparent at bottom
- **No trailing periods**: Strip periods from the end of both orange and white text. "ONE PROMPT" not "ONE PROMPT."
- **Arrow baseline fix**: The → character in Oswald sits too low on the baseline. Wrap it in `<span class="arrow">` with `.arrow { position: relative; top: -6px; }` to visually center it between surrounding text.
- **Arrow is always inline**: The → arrow belongs inline within the white subtitle text (e.g., `MEETING CHAOS <span class="arrow">→</span> ACTION ITEMS`), never as its own separate row between orange and white lines.

The editor (you) decides which words go orange vs white. The orange words should be the part that makes someone stop scrolling. The white words complete the thought.

## Dimensions

| Platform | Width | Height | Aspect |
|----------|-------|--------|--------|
| Substack hero | 1200 | 630 | ~16:9 |
| LinkedIn hero | 1200 | 675 | 16:9 |
| Twitter card | 1200 | 628 | ~16:9 |

Default is Substack (1200x630). Adjust Playwright viewport height for other platforms.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Gemini API key not found | `doppler secrets get GEMINI_API_KEY_PAID --plain -p openclaw -c dev` |
| MCP tool returns API_KEY_INVALID | Use Doppler CLI method instead (see Step 2). The MCP tool uses a separate key that may be stale. |
| Black bars in final image | Scene dimensions don't match. Run Pillow crop step. |
| Font not rendering | Copy Oswald to visuals dir: `cp /Users/travis/Library/Fonts/Oswald-VariableFont_wght.ttf content/visuals/` |
| Playwright can't load file:// | Use local HTTP server (`python3 -m http.server 8899`), not file:// |
| Text baked into scene | Re-prompt with explicit "NO TEXT OR CAPTIONS anywhere in the image" |
| Scene too light at top | Increase gradient opacity or height in the HTML overlay |
| White diamond in corner | That's Gemini's watermark. Crop or ignore — it's on the generated scene, not the final composite |

## Usage Examples

```
QHERO content/articles/my-article.md
  --orange "Claude Code Can't Design"
  --white "Eight MCP Tools Fixed That"
  --style cartoon_panels
```

```
QHERO content/articles/competitive-research.md
  --orange "Stop Googling Your Competitors"
  --white "AI Does It in 30 Minutes"
  --style semi_realistic_human_ai
```

```
QHERO --scene "3 panels: robot wireframes → 3 robots argue → they rebuild together"
  --orange "My AI Tools Started Fighting"
  --white "The Designs Got Better"
```
