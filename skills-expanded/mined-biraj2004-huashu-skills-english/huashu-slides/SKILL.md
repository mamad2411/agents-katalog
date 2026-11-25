---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |

    param($m)
    $inner = $m.Groups[1].Value
    # Split by | and fix each cell separator
    $cells = $inner -split '\|'
    $fixedCells = $cells | ForEach-Object {
      $cell = ---
name: huashu-slides
description: End-to-end presentation creation from content to finished PPTX, with AI illustration generation and 18 design styles. Use when the user mentions "make a PPT", "create slides", "presentation", "Keynote", or "slides".
---

# AI Presentation Workflow

Create professional presentations: Content → Design → Build → Assembly → Polish.

## Step 0: Choose Workflow Settings

**At the start of every presentation task, ask the user TWO choices:**

### 0-A. Collaboration Mode

| Mode | Description | Checkpoints |
|------|-------------|-------------|
| **Full Auto** | Minimal interaction. Confirm topic only, deliver final PPTX. | 1 checkpoint |
| **Guided** (recommended) | Confirm outline, pick design, preview before assembly. | 3 checkpoints |
| **Collaborative** | Review every slide, approve every illustration, full control. | Per-slide |

If the user doesn't specify, default to **Guided** mode.

### 0-B. Assembly Method

| Method | How it works | Best for |
|--------|-------------|----------|
| **Editable HTML** (Path A) | HTML slides + selective AI illustrations → html2pptx → editable PPTX | Need to edit text later, precise layout, corporate decks |
| **Full AI Visual** (Path B) | Every slide as a complete AI-generated image → image PPTX | Maximum visual impact, artistic presentations |

**Trade-offs:**

| | Path A: Editable HTML | Path B: Full AI Visual |
|---|---|---|
| Text | Editable in PPT | Baked into image (not editable) |
| Visual quality | Good with illustrations | Excellent — cohesive design |
| Chinese text | Perfect (font rendering) | Usually good (AI may occasionally misrender) |
| Speed | Faster | Slower (image per slide) |

If the user doesn't specify, default to **Path A** (Editable HTML).

---

## Step 1: Content Structuring

Turn raw material into a slide-by-slide outline.

**Per slide, define:**

- **Title** — a complete assertion sentence (not a topic word)
- **Key points** — 3–4 maximum
- **Visual type** — illustration / chart / diagram / icon / quote
- **Path A:** Illustration needed? — Yes/No. If yes, one-line description.
- **Path B:** Visual scene description — one paragraph describing the complete slide visual.

**Assertion-Evidence rule:**

| Bad title | Good title |
|-----------|------------|
| Q3 Sales | Q3 Sales Grew 23% — New Users Are the Main Driver |
| Methodology | We Validated This Conclusion via Double-Blind Testing |

**Language rule**: Slide content in the user's primary language. Only keep necessary English terms (names, brand names, technical proper nouns). Section labels (INSIGHT, TAKEAWAY) may use English as a design element.

### ✅ Checkpoint 1 (Guided + Collaborative)

Present the outline as a table. Ask the user:

- Approve / adjust slide count
- Approve / adjust which slides get illustrations (Path A) or visual scene descriptions (Path B)
- Any content to add or remove

---

## Step 2: Design System

**Present 3 design system options for the user to choose from.** Each is a complete visual language — not just a colour palette.

**CRITICAL: A design system is NOT just colours.** It defines visual philosophy, typography ratios, composition rules, and emotional intent.

### Style Discussion (Optional)

If the user references a specific design movement (Bauhaus, Swiss Style, etc.), consult `references/design-movements.md` to translate their aesthetic language into actionable presets.

---

### Design System Presets

**⚠️ Key insight: Illustration/comic styles generate far better AI results than "professional minimalist" styles.** Comic styles have clear visual language (lines, characters, colour blocks); minimalist styles (dark bg + glowing text + whitespace) produce flat, empty results.

**Topic Recommendation Table:**

| Topic Type | 1st Choice | 2nd Choice | 3rd Choice |
|-----------|-----------|-----------|-----------|
| Brand / product intro | Warm Comic Strip | Neo-Pop Magazine | Eastern-style (Dunhuang) |
| Education / training | Neo-Brutalism | Manga Educational | Warm Comic Strip |
| Tech sharing | Whiteboard Sketch | Neo-Brutalism | Ligne Claire |
| Data reports | Pentagram Editorial | Fathom Data | Ligne Claire |
| Young audience | Neo-Pop | Pixel Art | Risograph |
| Creative / artistic | Dada Collage | Risograph | The Oatmeal |
| Eastern / traditional | Dunhuang | Ukiyo-e | Takram Speculative |
| Formal business | Pentagram Editorial | Müller-Brockmann Grid | Build Luxury Minimal |
| Product launch | Soviet Constructivism | Neo-Pop | Pentagram Editorial |
| Internal sharing | Neo-Brutalism | The Oatmeal | Whiteboard Sketch |
| Industry analysis | Fathom Data | Pentagram Editorial | Müller-Brockmann Grid |
| Training materials | Takram Speculative | Warm Narrative | Manga Educational |
| Investor pitch | Build Luxury Minimal | Pentagram Editorial | Soviet Constructivism |

**Full 18-style reference:** `references/proven-styles-gallery.md`
**Style sample images:** `assets/style-samples/` directory

---

**Tier 1 (Highly recommended — excellent results):**

**1. Warm Comic Strip** — Snoopy/Peanuts style

- Philosophy: The warmth and wisdom of Peanuts comics — simple characters saying profound things in everyday scenes
- Visual world: Round-headed kids, a lovable dog, a small yellow bird. Extremely simple backgrounds (grass, sky, kennel, trees). Tone like yellowed newspaper comics.
- ⚠️ Key lesson: Don't over-constrain visual details in the prompt. Only describe mood and content; let the AI improvise.

**2. Manga Educational** — Learning manga style

- Philosophy: Japanese educational manga — a character guides you through the concept with reactions and drama
- Colours: Bright warm palette, white bg with selective colour panels, screen-tone grey for emphasis
- Composition: Dynamic manga panel layouts (3–5 panels per slide), character reactions drive emphasis

**3. Ligne Claire Comics** — Clean-line comic style

- Philosophy: Hergé's Tintin tradition — maximum information clarity through visual restraint
- Colours: White/cream (#FFFDF7) bg, black outlines, flat saturated fills (3–5 solid colours, no gradients)
- Composition: Panel-based layouts (2–4 panels), sequential left-to-right reading flow

**4. Neo-Pop Magazine** — New pop art magazine style

- Philosophy: Youth media / streetwear brand aesthetic, bold and playful
- Colours: Cream (#FFF8E7) bg, black text, colour-blocking with hot pink + cyan + yellow
- Typography: Headlines occupy 40–50% of slide area (typography AS the visual)

**Tier 2 (Recommended for specific scenarios):**

**5. Whiteboard Sketch** — xkcd whiteboard style

- Philosophy: xkcd meets a professor's whiteboard — extreme minimalism forces focus on the idea itself
- Colours: White bg, black ink, ONE accent colour (red or blue)
- Visual language: Stick figures, hand-drawn charts, wobbly lines, annotation arrows

**6. Soviet Constructivism** — Constructivist propaganda poster style

- Philosophy: Revolutionary propaganda poster — power through geometry and limited colour
- Colours: Revolutionary red (#CC0000) 40% + black 25% + cream white 30%
- Composition: Diagonal wedge from bottom-left to top-right, geometric shapes

**7. Warm Narrative** — Warm storytelling style

- Philosophy: Friendly storytelling, like a TED talk visual or Airbnb pitch deck
- Colours: Warm cream (#FDF6EC) bg, charcoal text, coral accent
- Visual language: Flat vector illustrations with warm palette, people-centric imagery

More styles (Tier 2 & 3) — see `references/proven-styles-gallery.md`: The Oatmeal, Dunhuang, Ukiyo-e, Risograph, Isometric, Bauhaus, Blueprint, Vintage Ad, Dada Collage, Pixel Art

---

**Tier 4: Professional / Editorial Design Systems (Path A only)**

> ⚠️ The following styles **strongly recommend Path A (HTML→PPTX)**. They depend on precise typography, data visualisation, and grid systems — AI image generation cannot achieve the required precision.

**8. Pentagram Editorial** — Editorial magazine style

- Philosophy: Pentagram/Michael Bierut — typography as language, grid as thought. Let data speak through extreme restraint.
- Colours: Cream white (#FFFDF7) bg, near-black (#1A1A1A) text, ONE accent colour (e.g., orange-red #D4480B)
- Composition: Swiss grid system, 2px black border cards, precise horizontal dividers, embedded data visualisation
- Reference: "Like a McKinsey insight report meets Monocle magazine"
- **Execution path: Path A only**

**9. Fathom Data Narrative** — Data storytelling style

- Philosophy: Fathom Information Design — every pixel must carry information
- Colours: White bg, dark grey text, navy (#1A365D) primary + one highlight
- Composition: High information density but not crowded; annotation system embedded in layout; small multiples chart arrays
- Reference: "Like a Nature paper's data supplement meets a Bloomberg data feature"
- **Execution path: Path A only**

**10. Müller-Brockmann Grid** — Swiss Grid style

- Philosophy: Josef Müller-Brockmann — objectivity is beauty. Mathematical grid makes any chaotic information orderly.
- Colours: White bg, black text, maximum one accent colour
- Composition: 8-column mathematical grid; all elements aligned to grid lines; zero decorative elements
- **Execution path: Path A only**

**11. Build Luxury Minimal** — Luxury minimalist style

- Philosophy: Build Studio — refined simplicity is harder than complexity
- Colours: Pure white bg, dark grey (#2D2D2D) text, single brand accent used sparingly
- Typography: Very subtle weight variation (200–600); giant titles (48pt+) but light; spacious tracking
- **Execution path: Path A**

**12. Takram Speculative** — Japanese speculative design style

- Philosophy: Takram — technology as a medium for thinking
- Colours: Warm grey (#F5F3EF) bg, dark grey text, sage green (#8B9D77) accent
- Composition: Soft shadows (20px+ blur), rounded corners (16px+), concept diagrams as core visuals
- **Execution path: Path A**

### Typography Rules (All Presets)

- Max 2 font families (1 heading + 1 body)
- Heading: bold, personality — ≥36pt
- Body: clean, readable — ≥18pt
- Key principle: Typography is a DESIGN ELEMENT, not just an information container

### ✅ Checkpoint 2 (Guided + Collaborative)

Ask the user to pick one of the 3 proposed design systems.

---

## Step 3: Build Slides

### Step 3-A: HTML + Selective Illustrations (Path A)

Generate AI illustrations for key slides, then create HTML slide files.

**Which slides need illustrations?** Prioritise:

1. **Cover slide** — always. Sets the visual tone.
2. **Key insight slides** — the "aha moment" slides benefit most.
3. **Closing slide** — optional but impactful.
4. **Data-heavy slides** — charts/diagrams instead of AI art.

**Illustration Generation:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[description]" \
  --filename "[timestamp]-slide-[N]-[name].png" \
  --resolution 2K
```

**Base Style Prompt** — define ONE style suffix, append to every illustration:

```text
[Base Style]: flat vector illustration, [palette background color] background,
[accent color] highlight elements, clean minimalist aesthetic,
professional presentation style, no text in image
```

**Per-slide prompt = [specific content] + [Base Style]**

**Key rules:**

- Always include "no text in image" — text will be added as editable elements
- Use descriptive paragraphs, not keyword lists
- Specify hex colours explicitly

**Embedding in HTML slides:**

```html
<!-- Side illustration (recommended) -->
<div class="left"><!-- text content --></div>
<div class="right"><img src="illustration.png" style="width: 280pt; height: 280pt;"></div>
```

**✅ Checkpoint 3-A** — Show generated illustrations. Ask: Approve / regenerate / style consistent?

---

### Step 3-B: Full AI Slide Generation (Path B)

Generate EVERY slide as a complete AI image — layout, text, visuals, all in one.

**⚠️ THE #1 MISTAKE: Over-constraining the prompt with layout details.**
More constraints = LESS creativity. Give mood + reference + content, NOT specific positions, colour ratios, or character restrictions.

#### The Golden Rule of AI Image Prompts

**SHORT prompts > LONG prompts.** A 3-sentence prompt describing mood and content beats a 30-line spec.

| DON'T (kills diversity) | DO (enables creativity) |
|---|---|
| Specify colour ratios (60%/25%/15%) | Describe the mood ("warm like a Sunday comic page") |
| Dictate layout positions | Reference a specific aesthetic ("Peanuts comic strip") |
| Restrict characters | Let AI interpret the style naturally |
| List every visual element | Describe what the viewer should FEEL |

#### Base Style Prompt — Keep it SHORT

Define once, append to every slide. **Under 5 lines.**

```text
[Base Style]:
VISUAL REFERENCE: [Specific art/design aesthetic in one sentence]
CANVAS: 16:9 aspect ratio, 2048x1152 pixels, high quality rendering.
COLOR SYSTEM: [Describe the mood/feel of colours, not exact ratios]
```

#### Per-Slide Prompt Structure

```text
Create a [style] slide about [topic].

[Base Style]

DESIGN INTENT: [1 sentence — what the viewer should FEEL]

TEXT TO RENDER:
- Title: "[exact text]"
- Body: "[exact text]"

[Optional: 1–2 sentences describing mood or scene. Let AI decide composition.]
```

**Prompt Quality Checklist (verify before every generation):**

1. Does the prompt name a specific art style or publication?
2. Does the prompt describe what the viewer should FEEL, not where elements should be placed?
3. Are all texts to render listed clearly and accurately?
4. Is the prompt concise? (Long prompts with detailed specs REDUCE diversity)
5. No micro-management — no hex colour ratios, no typography sizes, no pose instructions

**Technical Rules:**

- Always specify resolution: `2048x1152` (2K, 16:9)
- Include ALL text verbatim
- Keep titles short (≤8 characters for best Chinese rendering)
- Generate in parallel: run 3–5 slide generations concurrently

**Generation command:**

```bash
export $(grep GEMINI_API_KEY ~/.claude/.env) && \
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "[full slide prompt]" \
  --filename "slide-[NN]-[name].png" \
  --resolution 2K
```

**✅ Checkpoint 3-B** — Show ALL generated slide images. Ask: Text accurate? Style consistent? Any slides to regenerate?

---

## Step 4: PPTX Assembly

### 4-A: html2pptx Workflow (Path A)

```javascript
const pptxgen = require('pptxgenjs');
const html2pptx = require(process.env.HOME + '/.agents/skills/pptx/scripts/html2pptx.js');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
await html2pptx('slide1.html', pptx);
await html2pptx('slide2.html', pptx);
await pptx.writeFile({ fileName: 'output.pptx' });
```

**HTML rules:**

- Body dimensions: `width: 720pt; height: 405pt` (16:9)
- ALL text must be in `<p>`, `<h1>`–`<h6>`, `<ul>`, `<ol>` tags
- Backgrounds/borders only on `<div>` elements
- No CSS gradients — pre-render as PNG
- Use web-safe fonts only (Arial, Helvetica, Georgia, etc.)

**Known issue:** Non-ASCII characters in file paths can break image loading. Use symlinks to ASCII paths if needed.

### 4-B: Image Assembly (Path B)

```bash
uv run ~/.claude/skills/image-to-slides/scripts/create_slides.py \
  slide-01-cover.png slide-02-intro.png ... \
  --layout fullscreen \
  --bg-color 000000 \
  -o output.pptx
```

| Layout | Use case |
|--------|----------|
| `fullscreen` | AI-generated full-page slides (Path B default) |
| `title_above` | Image + editable title (hybrid approach) |
| `title_left` | Split: text + visual |
| `center` | Centred image with padding |
| `grid` | Multiple images per slide |

---

## Step 5: Preview & Polish

**Path A:** Screenshot key HTML slides with Playwright:

```bash
npx playwright screenshot "file:///path/to/slide.html" preview.png \
  --viewport-size=960,540 --wait-for-timeout=1000
```

**Path B:** Show the generated slide images directly using the Read tool.

### ✅ Checkpoint 4 (All modes)

Show preview to the user. Ask:

- Any slides to adjust?
- Ready to open in Keynote / PowerPoint?

### Final Polish (in Keynote/PowerPoint)

- Transitions and animations
- Speaker notes
- Brand logo placement
- Path A: Final text adjustments (editable)
- Path B: Text NOT editable — regenerate the slide image if text errors are found

---

## Design Quick Reference

**5/5/5 rule:** ≤5 words/line, ≤5 bullets/slide, ≤5 text-heavy slides in a row

**Cognitive load:** One idea per slide. ~1 min per slide. Slides complement speech, never duplicate it.

**Visual hierarchy:** F/Z-pattern reading flow. Title:body size ≈ 3:1. Every slide should have a visual element.

**Detailed references:**

- `references/proven-styles-gallery.md` — 18 tested visual styles with tiered recommendations
- `references/proven-styles-snoopy.md` — Snoopy/Peanuts style detailed per-slide templates
- `references/prompt-templates.md` — Content generation and image prompts
- `references/design-principles.md` — Full design framework, colour palettes, typography
- `references/design-movements.md` — Design movement and style reference library

## Related Skills

| Skill | Role |
|-------|------|
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
.Trim()
      if ($cell -match '^:?-+:?
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

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
  
| `pptx` | Advanced PPTX creation/editing (html2pptx, templates) |
| `nano-banana-pro` | AI illustration generation |
| `design-philosophy` | 20 design philosophies — detailed style DNA, scene templates, review criteria |

## Output

- `.pptx` files compatible with PowerPoint, Keynote, Google Slides
- Web-safe fonts for cross-platform compatibility
- AI illustrations as separate PNG files (reusable)

---

> **By Huashu** | AI Native Coder · Independent Developer
> WeChat Official Account "Huashu" | 300k+ followers | AI Tools & Productivity
> Flagship products: Kitty Catchlight (AppStore Paid Rankings Top 1) · *Play DeepSeek with One Book*
