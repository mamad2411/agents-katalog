---
name: pptx-dotnet
description: "Create, edit, and analyze PowerPoint presentations (.pptx) using C# and .NET 8. Use when the user requests PPTX work AND specifies C#/.NET, or when the project context is .NET/C#. Supports: (1) Creating presentations from scratch via HtmlBuild (write HTML/CSS, Playwright extracts layout, OpenXml SDK generates native PPTX), (2) Editing existing presentations via template inventory/replace workflow, (3) Slide rearrangement and duplication."
---

# PPTX (.NET)

Create beautiful presentations using HTML/CSS and .NET. The LLM writes HTML slides, Playwright renders them in headless Chromium to extract precise layout, and the OpenXml SDK generates native PPTX with editable text and shapes. No visual validation loop needed — what you write in HTML is what you get in PowerPoint.

## Workflow Decision Tree

- **Create from scratch** → HtmlBuild workflow (Section A) — write HTML/CSS slides
- **Create from template** → Inventory/Replace workflow (Section B)
- **Rearrange/duplicate slides** → Rearrange tool (Section C)

---

## A. Create from Scratch — HtmlBuild

Write one HTML file per slide. Playwright renders it in headless Chromium, extracts element positions and computed styles from the DOM, and converts them to native OpenXml shapes. The output is a real PPTX with editable text — not screenshots.

### A1. Choose a theme

Select from [references/themes.json](references/themes.json). Preview at [assets/theme-previews.png](assets/theme-previews.png).

| Theme | Style | Best for |
|-------|-------|----------|
| **midnight** | Dark blue, cyan accents | Tech, corporate, data |
| **ocean** | Teal/marine | Healthcare, biotech, science |
| **arctic** | Clean white/ice blue | Clinical, minimal, regulatory |
| **ember** | Dark with red/orange | Energy, urgency, alerts |
| **forest** | Deep green | Sustainability, growth |
| **slate** | Professional gray | Corporate, finance |
| **ivory** | Warm cream/gold | Academic, classical |
| **aurora** | Purple/violet | Innovation, creative |
| **copper** | Earth tones | Consulting, strategy |
| **glacier** | Ice blue/silver | Analytics, data science |
| **obsidian** | Near-black, neon accents | Technical, dev |
| **sandstone** | Warm neutral | Community, education |

Load the theme colors and use them consistently across all slides.

### A2. Write HTML slides

Each slide is a standalone HTML file. The `<body>` dimensions must match the aspect ratio:

| Aspect | Body style |
|--------|-----------|
| **16:9** | `width: 720pt; height: 405pt` |
| **4:3** | `width: 720pt; height: 540pt` |
| **16:10** | `width: 720pt; height: 450pt` |

#### Slide template

```html
<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="width: 720pt; height: 405pt; margin: 0; padding: 0; font-family: Arial, sans-serif; background: #F8FAFC;">
  <!-- Top accent bar -->
  <div style="position: absolute; top: 0; left: 0; right: 0; height: 4pt; background: #0369A1;"></div>

  <!-- Title -->
  <h1 style="position: absolute; top: 22pt; left: 45pt; width: 400pt; font-size: 22pt; color: #0F172A; margin: 0;">
    Slide Title Here
  </h1>
  <div style="position: absolute; top: 50pt; left: 45pt; width: 50pt; height: 3pt; background: #0EA5E9;"></div>

  <!-- Content goes here -->

</body>
</html>
```

### A3. HTML-to-PPTX element mapping

| HTML | PPTX result | Notes |
|------|-------------|-------|
| `<p>`, `<h1>`–`<h6>` | Text shape | **ALL text must be in these tags** |
| `<ul>`, `<ol>` with `<li>` | Bulleted/numbered list | Never use manual bullet symbols (•, -, *) |
| `<b>`, `<i>`, `<u>`, `<span>` | Rich text runs | Inline formatting within a text element |
| `<div>` with `background` | Filled rectangle | Supports border-radius, box-shadow |
| `<div>` with `border` | Rectangle with outline, or line shapes for partial borders |
| `<img>` | Embedded image | Use absolute file paths |
| `<div class="placeholder">` | Reserved position | Returns `{id, x, y, w, h}` for charts |

#### What does NOT convert

- ❌ CSS gradients (`linear-gradient`, `radial-gradient`) — rasterize as PNG first
- ❌ Text directly in `<div>` — **will silently disappear**. Always wrap in `<p>` or heading
- ❌ Backgrounds/borders on text elements (`<p>`, `<h1>`, `<ul>`) — only `<div>` supports these
- ❌ Margins on inline `<span>`, `<b>`, `<i>` — not supported in PowerPoint text runs
- ❌ Inset box-shadows — only outer shadows convert
- ❌ Custom fonts — use web-safe only: Arial, Georgia, Verdana, Tahoma, Trebuchet MS, Times New Roman, Impact, Courier New

### A4. Critical design rules

These rules prevent the layout problems that occur when browser rendering differs from PowerPoint text rendering. **Follow them strictly.**

#### Typography

| Element | Max font size | Notes |
|---------|--------------|-------|
| Slide title | **22pt** | Bold, one line preferred |
| Section header | 14–16pt | Bold |
| Body text / bullets | 9–12pt | Regular weight |
| Stat numbers | 26–30pt | Bold, inside cards |
| Stat labels | 9–10pt | Below the number |
| Footnotes / sources | 8–9pt | Muted color |
| Card headers | 12pt | Bold, colored |

**Never use titles larger than 22pt on content slides.** Title slides may use up to 30pt.

#### Layout

- **Margins**: Minimum 45pt from all edges for content
- **Title area**: Top 22pt to 55pt (title + underline accent)
- **Content area**: 65pt to 290pt — this is the safe working zone
- **Bottom 30%**: Keep clear or use only for footnotes/source text
- **Card spacing**: Minimum 15pt gap between cards
- **Card rows**: Maximum 2 rows of cards per slide

#### Shapes and text — the critical rule

**Never nest absolute-positioned text inside absolute-positioned divs for cards.**

Instead, place the background shape and the text as **separate sibling elements** at the body level:

```html
<!-- ✅ CORRECT: Shape and text as siblings -->
<div style="position: absolute; top: 65pt; left: 45pt; width: 200pt; height: 70pt;
            background: #FFFFFF; border-radius: 5pt; border-left: 4pt solid #DC2626;
            box-shadow: 1px 2px 4px rgba(0,0,0,0.08);"></div>
<p style="position: absolute; top: 73pt; left: 62pt; width: 170pt;
          font-size: 26pt; color: #DC2626; margin: 0; font-weight: bold;">1,420</p>
<p style="position: absolute; top: 105pt; left: 62pt; width: 170pt;
          font-size: 10pt; color: #64748B; margin: 0;">Missed visits per year</p>
```

```html
<!-- ❌ WRONG: Text nested inside the card div — causes overlap in PowerPoint -->
<div style="position: absolute; top: 65pt; left: 45pt; width: 200pt; height: 70pt;
            background: #FFFFFF; border-radius: 5pt;">
  <p style="position: absolute; top: 10pt; left: 15pt; font-size: 26pt;">1,420</p>
  <p style="position: absolute; top: 45pt; left: 15pt; font-size: 10pt;">Missed visits</p>
</div>
```

#### Callout boxes

```html
<!-- Insight/callout box -->
<div style="position: absolute; top: 210pt; left: 45pt; width: 630pt; height: 55pt;
            background: #EFF6FF; border-radius: 5pt; border-left: 4pt solid #0369A1;"></div>
<p style="position: absolute; top: 220pt; left: 62pt; width: 598pt;
          font-size: 11pt; color: #1E293B; margin: 0; line-height: 1.5;">
  <b>Key finding:</b> Your insight text here.
</p>
```

#### Stat cards (3-across)

```html
<!-- Three stat cards -->
<div style="position: absolute; top: 65pt; left: 45pt; width: 200pt; height: 75pt;
            background: #0369A1; border-radius: 5pt;"></div>
<p style="position: absolute; top: 72pt; left: 60pt; width: 170pt;
          font-size: 28pt; color: #FFFFFF; margin: 0; font-weight: bold;">10%</p>
<p style="position: absolute; top: 106pt; left: 60pt; width: 170pt;
          font-size: 9pt; color: #BAE6FD; margin: 0;">Target no-show rate</p>

<div style="position: absolute; top: 65pt; left: 260pt; width: 200pt; height: 75pt;
            background: #0369A1; border-radius: 5pt;"></div>
<p style="position: absolute; top: 72pt; left: 275pt; width: 170pt;
          font-size: 28pt; color: #FFFFFF; margin: 0; font-weight: bold;">640</p>
<p style="position: absolute; top: 106pt; left: 275pt; width: 170pt;
          font-size: 9pt; color: #BAE6FD; margin: 0;">Appointments recovered</p>

<div style="position: absolute; top: 65pt; left: 475pt; width: 200pt; height: 75pt;
            background: #0369A1; border-radius: 5pt;"></div>
<p style="position: absolute; top: 72pt; left: 490pt; width: 170pt;
          font-size: 28pt; color: #FFFFFF; margin: 0; font-weight: bold;">$170K</p>
<p style="position: absolute; top: 106pt; left: 490pt; width: 170pt;
          font-size: 9pt; color: #BAE6FD; margin: 0;">Revenue recovered</p>
```

#### Two-column content cards (2×2 grid)

```html
<!-- Row 1 -->
<div style="position: absolute; top: 65pt; left: 45pt; width: 310pt; height: 100pt;
            background: #FFFFFF; border-radius: 5pt;
            box-shadow: 1px 2px 4px rgba(0,0,0,0.06);"></div>
<p style="position: absolute; top: 72pt; left: 58pt; width: 280pt;
          font-size: 12pt; color: #0369A1; margin: 0; font-weight: bold;">1. Card Title</p>
<ul style="position: absolute; top: 90pt; left: 58pt; width: 280pt;
           font-size: 9pt; color: #334155; line-height: 1.8; padding-left: 10pt;">
  <li>Point one</li>
  <li>Point two</li>
  <li>Point three</li>
</ul>

<div style="position: absolute; top: 65pt; left: 370pt; width: 310pt; height: 100pt;
            background: #FFFFFF; border-radius: 5pt;
            box-shadow: 1px 2px 4px rgba(0,0,0,0.06);"></div>
<p style="position: absolute; top: 72pt; left: 383pt; width: 280pt;
          font-size: 12pt; color: #0369A1; margin: 0; font-weight: bold;">2. Card Title</p>
<ul style="position: absolute; top: 90pt; left: 383pt; width: 280pt;
           font-size: 9pt; color: #334155; line-height: 1.8; padding-left: 10pt;">
  <li>Point one</li>
  <li>Point two</li>
  <li>Point three</li>
</ul>

<!-- Row 2: same pattern at top: 180pt -->
```

### A5. Build the PPTX

**Docker (recommended)** — all dependencies baked in, nothing to install:

```bash
docker run --rm -v /path/to/slides:/data ghcr.io/drpedapati/htmlbuild \
  slide1.html slide2.html slide3.html output.pptx [--aspect 16:9|4:3|16:10]
```

**Local** (requires .NET 8 SDK):

```bash
cd $SKILL_DIR/scripts/HtmlBuild
dotnet run -- slide1.html slide2.html slide3.html output.pptx [--aspect 16:9|4:3|16:10]
```

The builder:
1. Renders each HTML in headless Chromium via Playwright
2. Extracts all element positions and computed styles from the DOM
3. Validates: overflow, unsupported CSS, unwrapped text, manual bullets
4. Generates native PPTX with editable text shapes — not rasterized images

**No visual validation loop.** The HTML is the source of truth.

### A6. Slide dimensions reference

| Aspect | Width | Height | Body style |
|--------|-------|--------|-----------|
| 16:9 | 10" | 5.625" | `720pt × 405pt` |
| 4:3 | 10" | 7.5" | `720pt × 540pt` |
| 16:10 | 10" | 6.25" | `720pt × 450pt` |

---

## B. Create from Template

Use an existing .pptx as a design template. Extract its structure, rearrange slides, replace text.

### B1. Analyze template

```bash
# Extract text inventory
cd $SKILL_DIR/scripts/Inventory
dotnet run -- template.pptx template-inventory.json

# Render slides to PNG for reference
cd $SKILL_DIR/scripts/Validate
dotnet run -- template.pptx --outdir /tmp/template-slides
```

Read each PNG. Map every slide to its purpose.

### B2. Rearrange slides

```bash
cd $SKILL_DIR/scripts/Rearrange
dotnet run -- template.pptx working.pptx 0,3,3,7,12,12,15
```

Comma-separated 0-based indices. Duplicates allowed. Unlisted slides deleted.

### B3. Extract and replace text

```bash
# Get current text inventory
cd $SKILL_DIR/scripts/Inventory
dotnet run -- working.pptx text-inventory.json

# Apply replacements
cd $SKILL_DIR/scripts/Replace
dotnet run -- working.pptx replacement-text.json output.pptx
```

Replacement JSON matches the inventory structure. See B5 below for format.

### B4. Inventory JSON structure

```json
{
  "slide-0": {
    "shape-0": {
      "position": {"left_in": 0.5, "top_in": 0.5, "width_in": 9.0, "height_in": 1.0},
      "paragraphs": [
        {"text": "Original Title", "font_size": 36, "bold": true, "color": "000000"}
      ]
    }
  }
}
```

### B5. Replacement JSON

```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        {"text": "New Title", "font_size": 36, "bold": true, "color": "1a1a2e",
         "alignment": "CENTER", "font_name": "Arial"}
      ]
    }
  }
}
```

Paragraph properties: `text`, `bullet` (bool), `level`, `alignment` (CENTER/RIGHT/JUSTIFY), `space_before`/`space_after` (pt), `font_name`, `font_size`, `bold`, `italic`, `underline`, `color` (hex without #), `theme_color`.

---

## C. Rearrange Slides

```bash
cd $SKILL_DIR/scripts/Rearrange
dotnet run -- input.pptx output.pptx 0,1,1,3,5
```

- Comma-separated 0-based slide indices
- Repeated indices = duplicated slides
- Unlisted slides are deleted

---

## Tools Reference

| Tool | Purpose | Usage |
|------|---------|-------|
| **HtmlBuild** | HTML → PPTX | `docker run --rm -v .:/data ghcr.io/drpedapati/htmlbuild slide1.html output.pptx` |
| **Inventory** | Extract text map | `dotnet run -- input.pptx output.json [--issues-only]` |
| **Replace** | Swap text content | `dotnet run -- input.pptx replacements.json output.pptx` |
| **Rearrange** | Reorder slides | `dotnet run -- input.pptx output.pptx 0,3,3,7` |
| **Validate** | Render to PNG | `dotnet run -- input.pptx [--outdir dir] [--width N]` |
| **DirectBuild** | JSON → PPTX (legacy) | `dotnet run -- slides.json output.pptx [--aspect 16:9]` |

## Docker

The `ghcr.io/drpedapati/htmlbuild` image packages everything — .NET 8 runtime, headless Chromium, OpenXml SDK, scaffold templates. No local dependencies needed.

```bash
# Build a presentation
docker run --rm -v /path/to/slides:/data ghcr.io/drpedapati/htmlbuild \
  slide1.html slide2.html slide3.html output.pptx

# Build the image locally
cd skills/pptx-dotnet
docker build -t htmlbuild .
```

## Dependencies (local dev only)

**.NET SDK** 8.0 or later. Headless Chromium (auto-installed by Playwright on first run).

NuGet packages (all signed, restored automatically):
- `DocumentFormat.OpenXml` — Microsoft Open XML SDK
- `Microsoft.Playwright` — headless browser for HTML rendering (HtmlBuild only)
- `SkiaSharp` — cross-platform 2D graphics (Validate only)
