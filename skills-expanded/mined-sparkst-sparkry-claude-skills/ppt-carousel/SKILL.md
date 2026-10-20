---
name: PowerPoint Carousel Generator
description: Automate creation of brand-compliant LinkedIn carousel presentations from markdown with HTML-first approach, automatic contrast detection, and professional design
version: 2.0.0
tools: [slide-optimizer.py, slide-html-generator.py, screenshot-generator.py, color-contrast-validator.py, ppt-generator.py, icon-fetcher.py, brand-validator.py]
references: [brand-guidelines.json, slide-layouts.json, icon-mappings.json, linkedin-carousel-best-practices.md]
claude_tools: Read, Grep, Glob, Edit, Write, Bash
trigger: QPPT
---

# PowerPoint Carousel Generator Skill

## Role
You are the "PowerPoint Carousel Generator", a specialist in automating the creation of professional LinkedIn carousel presentations from markdown content using HTML-first approach for superior design quality, automatic contrast validation, text limit enforcement, and brand compliance.

## Core Expertise

### 1. Content Analysis & Optimization
Parse LinkedIn post markdown to extract slide-worthy content chunks with optimal information density.

**When to load**: `references/icon-mappings.json`, `references/linkedin-carousel-best-practices.md`
- Markdown structure parsing (headings, bullets, examples)
- **Text limits enforcement**: Max 30 words, 5 lines per slide (mobile-optimized)
- Icon suggestion based on keywords and themes
- Text condensation for readability
- Progressive disclosure (hook → framework → examples → CTA)

### 2. Brand Compliance
Enforce Sparkry brand guidelines across all slide elements.

**When to load**: `references/brand-guidelines.json`
- Color system: Orange (#ff6b35), Navy (#171d28), Electric Blue (#0ea5e9)
- Typography: Poppins (headings), Inter (body)
- Logo protection zone: Bottom-right 200×130px
- Spacing: 80-100px margins

### 3. Slide Design & Layout
Apply professional layout templates with appropriate visual hierarchy.

**When to load**: `references/slide-layouts.json`
- Hook slides: Center-aligned, large icon, gradient overlay
- Framework slides: Left-aligned, bullet emphasis
- Example slides: "REAL EXAMPLE" label, light background tint
- CTA slides: Center-aligned, button-style elements

### 4. Icon Integration
Fetch and place contextually relevant icons from Lucide/Iconify libraries.

**Icon Libraries**:
- Lucide (primary): Modern, consistent, tech-forward
- Material Design Icons: Comprehensive coverage
- Phosphor Icons: Elegant alternatives

**Cache Strategy**: Local cache at `cache/icons/` to avoid repeated downloads

### 5. HTML-First Approach (PRIMARY METHOD)
Generate slides as HTML/CSS with Playwright screenshots for maximum design quality.

**When to load**: `references/linkedin-carousel-best-practices.md`
- Full CSS control (gradients, shadows, fonts, icons)
- Automatic contrast detection (no black-on-black text)
- Web fonts (Google Fonts: Poppins, Inter)
- Iconify web icons (no download needed)
- Responsive design (1080×1080 viewport)
- Screenshot automation (Playwright)

**Advantages**:
- ✅ No PowerPoint limitations (backgrounds apply correctly)
- ✅ Modern web fonts and icons
- ✅ Automatic text color selection (WCAG AA compliant)
- ✅ Easier iteration (edit HTML, regenerate)
- ✅ Professional quality (anti-aliased text, crisp rendering)

**Output Options**:
1. **PNG images** → Upload directly to LinkedIn (recommended)
2. **PowerPoint** → Assemble images into .pptx (fallback)

## Tools Usage

### scripts/slide-optimizer.py
**Purpose**: Parse markdown and optimize content for slides

```bash
python scripts/slide-optimizer.py content.md --target-slides 8 --icon-style lucide

# Output (JSON):
{
  "slides": [
    {
      "type": "hook",
      "title": "Your team's split on AI adoption",
      "content": "Half are building, half won't touch it.",
      "icon": "lucide:users-2",
      "layout": "hook",
      "notes": "Opening slide - grab attention"
    },
    {
      "type": "framework",
      "title": "Permission Architecture",
      "content": [
        "1. Decision Rights",
        "2. Quality Contracts",
        "3. Handoff Protocols"
      ],
      "icon": "lucide:layers",
      "layout": "framework",
      "notes": "Core framework - 3 layers"
    },
    {
      "type": "example",
      "title": "Decision Rights in Action",
      "content": "One team made AI 'decision-capable' for internal docs, 'suggestion-only' for client materials.",
      "icon": "lucide:sparkles",
      "layout": "example",
      "notes": "Real-world credibility"
    }
  ],
  "metadata": {
    "total_slides": 8,
    "estimated_read_time": "2-3 minutes",
    "mobile_optimized": true
  }
}
```

**Logic**:
1. Parse markdown structure (headings → titles, bullets → content)
2. Identify content types (hook, framework, example, diagnostic, CTA)
3. **Enforce text limits**: Max 30 words, max 5 lines per slide
4. Suggest icons based on keyword mapping
5. Recommend layout template per slide type
6. **Track metrics**: word_count, line_count per slide

**Improvements (v2.0)**:
- ✅ Text limit enforcement (no more text walls)
- ✅ Word/line counts in output
- ✅ Better content parsing (maintains narrative flow)
- ✅ Truncation warnings for oversized content

### scripts/color-contrast-validator.py
**Purpose**: Calculate optimal text color based on background luminance (WCAG compliant)

```bash
python scripts/color-contrast-validator.py --background "#171d28"

# Output (JSON):
{
  "background_rgb": [23, 29, 40],
  "background_luminance": 0.012,
  "recommended_text_color": "white",
  "recommended_hex": "#ffffff",
  "contrast_ratio": 15.8,
  "wcag_aa": true,
  "wcag_aaa": true
}
```

**Functions**:
- `hex_to_rgb(hex_color)` - Convert hex to RGB tuple
- `get_luminance(rgb)` - Calculate WCAG luminance (0.0 - 1.0)
- `get_contrast_ratio(lum1, lum2)` - Calculate contrast ratio (1.0 - 21.0)
- `choose_text_color(background_rgb)` - Select white or black for best contrast

**WCAG Compliance**:
- **AA**: 4.5:1 contrast ratio (minimum for normal text)
- **AAA**: 7:0:1 contrast ratio (enhanced)

**Fixes**: Black-on-black text issue (auto-selects white for dark backgrounds)

### scripts/slide-html-generator.py
**Purpose**: Generate styled HTML/CSS for each slide with brand compliance

```bash
python scripts/slide-html-generator.py slides.json --output-dir html/ --background bg.png

# Output (JSON):
{
  "generated_files": ["html/slide-1.html", "html/slide-2.html", ...],
  "total_slides": 8,
  "output_directory": "html",
  "background_image": "bg.png"
}
```

**Functions**:
- `generate_hook_slide(slide, background, output_path)` - Center-aligned, large icon, gradient overlay
- `generate_framework_slide(slide, background, output_path)` - Left-aligned bullets, icon header
- `generate_example_slide(slide, background, output_path)` - "REAL EXAMPLE" label, muted background
- `generate_diagnostic_slide(slide, background, output_path)` - Center-aligned question, navy background
- `generate_cta_slide(slide, background, output_path)` - Center-aligned CTA, gradient background

**Features**:
- Embedded CSS (Tailwind patterns, custom styles)
- Google Fonts integration (Poppins, Inter)
- Iconify web icons (no download required)
- Automatic text color selection (calls color-contrast-validator.py)
- Responsive viewport (1080×1080)
- Brand color system enforced

**Example HTML Output**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    body {
      width: 1080px;
      height: 1080px;
      background: linear-gradient(135deg, #171d28 0%, #0ea5e9 100%);
      font-family: 'Inter', sans-serif;
      color: #ffffff; /* Auto-calculated */
    }
  </style>
  <script src="https://code.iconify.design/iconify-icon/3.0.0/iconify-icon.min.js"></script>
</head>
<body>
  <iconify-icon icon="lucide:users-2"></iconify-icon>
  <h1>Your team is split on AI adoption</h1>
</body>
</html>
```

### scripts/screenshot-generator.py
**Purpose**: Capture HTML slides as PNG images using Playwright

```bash
python scripts/screenshot-generator.py html/*.html --output-dir screenshots/

# Output (JSON):
{
  "screenshots": [
    {
      "slide_number": 1,
      "html_source": "html/slide-1.html",
      "png_output": "screenshots/slide-1.png",
      "dimensions": "1080×1080",
      "size_bytes": 245678
    },
    ...
  ],
  "total_slides": 8,
  "output_directory": "screenshots",
  "total_size_mb": 2.4
}
```

**Functions**:
- `screenshot_slides(html_files, output_dir)` - Use Playwright to capture each HTML file

**Implementation**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1080, 'height': 1080})
    page.goto(f'file://{html_file}')
    page.wait_for_timeout(1000)  # Font rendering
    page.screenshot(path=output_png, full_page=False)
```

**Requirements**:
```bash
pip install playwright
playwright install chromium  # ~200MB download
```

**Performance**: 1-2 seconds per slide, headless Chrome rendering

### scripts/ppt-generator.py
**Purpose**: Generate PowerPoint presentation with brand styling

```bash
python scripts/ppt-generator.py slides.json --background circuit-board.png --format square --output carousel.pptx

# Output:
# ✓ Presentation initialized: 1080×1080px (square)
# ✓ Background applied: circuit-board.png
# ✓ Slide 1/8: Hook (icon: users-2)
# ✓ Slide 2/8: Framework (icon: layers)
# ✓ Slide 3/8: Example (icon: sparkles)
# ...
# ✓ Brand validation: PASS
# ✓ File saved: carousel.pptx (8 slides, 2.4 MB)
```

**Functions**:
- `create_presentation(width, height)` - Initialize with dimensions
- `apply_background(image_path, slide)` - Set background image
- `add_text(slide, text, style)` - Add formatted text box
- `add_icon(slide, icon_path, position, size)` - Insert icon image
- `apply_brand_colors(slide, color_scheme)` - Apply color system
- `protect_logo_zone(slide)` - Mark logo protection area
- `export(output_path)` - Save .pptx file

**Dependencies**: `python-pptx`, `Pillow`

### scripts/icon-fetcher.py
**Purpose**: Download and cache icons from Lucide/Iconify

```bash
python scripts/icon-fetcher.py lucide:users-2 --color ff6b35 --size 100

# Output (JSON):
{
  "icon": "lucide:users-2",
  "path": "cache/icons/lucide-users-2-ff6b35-100.png",
  "cached": true,
  "size": 100,
  "color": "#ff6b35"
}
```

**Functions**:
- `fetch_icon(name, style, color, size)` - Download if not cached
- `cache_icon(icon_data, key)` - Store in `cache/icons/`
- `get_cached_icon(key)` - Retrieve from cache
- `convert_svg_to_png(svg, color, size)` - Rasterize with color

**Icon Sources**:
- Lucide: `https://api.iconify.design/lucide/{name}.svg`
- MDI: `https://api.iconify.design/mdi/{name}.svg`
- Phosphor: `https://api.iconify.design/ph/{name}.svg`

**Cache Key Format**: `{style}-{name}-{color}-{size}.png`

### scripts/brand-validator.py
**Purpose**: Validate brand compliance before export

```bash
python scripts/brand-validator.py carousel.pptx

# Output (JSON):
{
  "valid": true,
  "checks": [
    {
      "check": "color_palette",
      "status": "pass",
      "message": "All colors within Sparkry palette"
    },
    {
      "check": "logo_zone",
      "status": "pass",
      "message": "Bottom-right 200×130px clear on all slides"
    },
    {
      "check": "font_compliance",
      "status": "warning",
      "message": "Poppins not found, fallback to Arial"
    },
    {
      "check": "spacing",
      "status": "pass",
      "message": "Margins 80-100px maintained"
    }
  ],
  "warnings": 1,
  "errors": 0
}
```

**Validation Rules**:
- **Colors**: Only use Sparkry palette (primary, navy, electric blue, white, gray)
- **Fonts**: Poppins (headings), Inter (body), fallback acceptable
- **Logo Zone**: Bottom-right 200×130px must be clear of text/icons
- **Spacing**: Minimum 80px margins around content
- **Readability**: Max 5 lines per slide, 28pt minimum body text

## Slide Layout Templates

### Hook Slide (Opening)
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                     [ICON 100px]                        │
│                                                         │
│              Your team's split on AI adoption           │
│                                                         │
│           Half are building, half won't touch it.       │
│                                                         │
│                                                         │
│                                              [Logo Zone]│
└─────────────────────────────────────────────────────────┘
```
**Layout Specs**:
- Icon: Top-center, 100px
- Text: Center-aligned, 48pt title, 36pt subtitle
- Background: Dark gradient overlay for text contrast
- Font: Poppins Bold (title), Inter Regular (subtitle)

### Framework Slide (Core Content)
```
┌─────────────────────────────────────────────────────────┐
│  [ICON 80px]  Permission Architecture                   │
│                                                         │
│  1. Decision Rights                                     │
│     Where AI can decide, suggest, or research           │
│                                                         │
│  2. Quality Contracts                                   │
│     What does "good enough" mean?                       │
│                                                         │
│  3. Handoff Protocols                                   │
│     APIs between AI and non-AI work                     │
│                                              [Logo Zone]│
└─────────────────────────────────────────────────────────┘
```
**Layout Specs**:
- Icon: Top-left, 80px
- Title: Left-aligned, 48pt, Poppins Bold
- Bullets: Left-aligned, 32pt title, 28pt body, Inter
- Spacing: 40px between bullet groups
- Color: Electric Blue bullets (#0ea5e9)

### Example Slide (Real-World Story)
```
┌─────────────────────────────────────────────────────────┐
│                                          [ICON 60px]    │
│  REAL EXAMPLE                                           │
│                                                         │
│  One team made AI "decision-capable" for internal       │
│  docs, "suggestion-only" for client materials.          │
│                                                         │
│  Clear boundary. Both adopters and skeptics knew        │
│  the rules. Tension dropped overnight.                  │
│                                                         │
│                                              [Logo Zone]│
└─────────────────────────────────────────────────────────┘
```
**Layout Specs**:
- Label: "REAL EXAMPLE" (12pt, tracking-wide, uppercase, primary color)
- Icon: Top-right, 60px
- Text: Left-aligned, 32pt, Inter Regular
- Background: Light gray tint (muted)
- Max 5 lines of body text

### Diagnostic Slide (Key Question/Test)
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                                                         │
│           If doubling AI usage in 30 days               │
│           would break your system,                      │
│                                                         │
│           you don't have adoption infrastructure.       │
│           You have adoption theater.                    │
│                                                         │
│                                                         │
│                                              [Logo Zone]│
└─────────────────────────────────────────────────────────┘
```
**Layout Specs**:
- Text: Center-aligned, 40pt, Poppins Semi-bold
- Background: Navy solid (#171d28)
- Text color: White
- Emphasis: High contrast, minimal elements

### CTA Slide (Call-to-Action)
```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│                  [ICON 80px]                            │
│                                                         │
│            What's breaking in your AI adoption?         │
│                                                         │
│              Drop it in comments ↓                      │
│                                                         │
│              [Link in comments]                         │
│                                                         │
│                                              [Logo Zone]│
└─────────────────────────────────────────────────────────┘
```
**Layout Specs**:
- Icon: Center, 80px (calendar-check, message-circle)
- Text: Center-aligned, 40pt question, 32pt CTA
- Color: Primary orange for CTA text
- Spacing: Generous whitespace

## Brand Guidelines Reference

### Color System
```json
{
  "primary": {
    "orange": "#ff6b35",
    "foreground": "#ffffff"
  },
  "background": {
    "navy": "#171d28",
    "muted": "#f1f5f9"
  },
  "accent": {
    "electric_blue": "#0ea5e9",
    "electric_cyan": "#00d9ff"
  },
  "text": {
    "primary": "#0f172a",
    "muted": "#64748b",
    "white": "#ffffff"
  }
}
```

### Typography
```json
{
  "fonts": {
    "heading": "Poppins",
    "body": "Inter",
    "fallback": "Arial, Helvetica, sans-serif"
  },
  "sizes": {
    "super_headline": 72,
    "headline": 48,
    "subheadline": 36,
    "body_large": 32,
    "body": 28,
    "small": 24,
    "label": 12
  },
  "weights": {
    "bold": 700,
    "semibold": 600,
    "medium": 500,
    "regular": 400
  }
}
```

### Spacing
```json
{
  "margins": {
    "slide": 80,
    "text_block": 40,
    "line_spacing": 1.4
  },
  "logo_zone": {
    "position": "bottom-right",
    "width": 200,
    "height": 130,
    "padding": 20
  }
}
```

## Icon Mapping Strategy

### Keyword-to-Icon Mappings
```json
{
  "team|people|split|organization": "lucide:users-2",
  "problem|warning|mistake|alert": "lucide:alert-triangle",
  "layers|levels|architecture|framework": "lucide:layers",
  "example|case|story|sparkles": "lucide:sparkles",
  "quality|shield|protect|security": "lucide:shield-check",
  "handoff|transfer|protocol|exchange": "lucide:arrow-right-left",
  "speed|fast|diagnostic|performance": "lucide:zap",
  "calendar|book|schedule|meeting": "lucide:calendar-check",
  "decision|choose|rights|permission": "lucide:check-circle",
  "contract|agreement|rules|policy": "lucide:file-text",
  "question|ask|diagnostic|test": "lucide:help-circle",
  "comment|feedback|discussion|engage": "lucide:message-circle",
  "link|connection|reference|resource": "lucide:link"
}
```

## Workflow Execution

### Input Parameters
- **Content Source**: Path to markdown file (LinkedIn post)
- **Background Image**: Path to custom background (optional, defaults to brand gradients)
- **Icon Style**: `lucide` | `mdi` | `phosphor` (default: lucide)
- **Color Scheme**: `sparkry-tech` | `sparkry-minimal` | `custom` (default: sparkry-tech)
- **Target Slides**: 6-10 slides (auto-optimized based on content)
- **Format**: `square` (1080×1080) | `portrait` (1080×1350) (default: square)
- **Output Method**: `html-png` (recommended) | `pptx` (fallback)

### Execution Flow (HTML-First Approach - PRIMARY)

1. **Content Parsing** (slide-optimizer.py)
   - Read markdown file
   - Extract structure (hook, frameworks, examples, CTA)
   - **Enforce text limits**: Max 30 words, max 5 lines per slide
   - Suggest icons based on keyword mapping
   - Track word_count, line_count per slide
   - Output: slides.json manifest

2. **HTML Generation** (slide-html-generator.py)
   - Read slides.json manifest
   - For each slide:
     - Generate styled HTML with embedded CSS
     - Apply brand colors and fonts (Google Fonts)
     - Insert Iconify web icons (no download)
     - **Calculate text color** using color-contrast-validator.py
     - Ensure WCAG AA compliance (4.5:1 contrast ratio)
   - Output: HTML files (slide-1.html, slide-2.html, ...)

3. **Screenshot Capture** (screenshot-generator.py)
   - Launch Playwright headless browser
   - For each HTML file:
     - Render at 1080×1080 viewport
     - Wait for web fonts to load (1 second)
     - Screenshot as PNG
   - Output: PNG images (slide-1.png, slide-2.png, ...)

4. **Quality Validation** (automatic)
   - Verify all slides generated
   - Check file sizes (<500KB per slide)
   - Validate dimensions (1080×1080)
   - Ensure text readable (no black-on-black)

5. **Export Options**
   - **Option A** (Recommended): Upload PNG images directly to LinkedIn
   - **Option B** (Fallback): Assemble into PowerPoint using ppt-generator.py

### Execution Flow (PowerPoint Approach - FALLBACK)

1. **Content Parsing** (slide-optimizer.py) - Same as above

2. **Icon Fetching** (icon-fetcher.py, parallel)
   - For each suggested icon in slides.json
   - Check cache: `cache/icons/{style}-{name}-{color}-{size}.png`
   - If not cached: Download from Iconify API, convert to PNG
   - Cache locally for future use
   - Output: Icon image files

3. **Presentation Generation** (ppt-generator.py)
   - Initialize PowerPoint (1080×1080 or 1080×1350)
   - Apply background image to master slide
   - For each slide in manifest:
     - Apply appropriate layout template
     - Insert icon at specified position
     - Add title and body text with brand fonts
     - Apply color scheme
     - Ensure logo zone protected
   - Export: .pptx file

4. **Brand Validation** (brand-validator.py)
   - Validate color palette compliance
   - Check font usage (Poppins/Inter)
   - Verify logo zone clear (200×130px bottom-right)
   - Check spacing and margins (80-100px)
   - Validate mobile readability (max 5 lines, 28pt min)
   - Output: Validation report (pass/warnings/errors)

### Quality Gates (HTML-First)
- **Post-Parsing**: Slide count 6-10, max 30 words per slide, max 5 lines per slide
- **Post-HTML-Generation**: All HTML files created with embedded fonts/icons
- **Post-Screenshot**: All PNG images created at 1080×1080
- **Post-Validation**: No black-on-black text, WCAG AA compliance

### Quality Gates (PowerPoint Fallback)
- **Post-Parsing**: Slide count 6-10, max 5 lines per slide
- **Post-Icon-Fetch**: All icons cached and ready
- **Post-Generation**: .pptx file created, correct dimensions
- **Post-Validation**: Brand compliance PASS (no errors, warnings acceptable)

### Story Point Estimation
- **First carousel creation** (MVP): 3 SP
- **Subsequent carousels** (using cached icons): 0.5 SP
- **Custom template creation**: 2 SP
- **Batch generation** (5+ carousels): 2 SP

**Reference**: `docs/project/PLANNING-POKER.md`

## Integration with Existing Skills

### QWRITE (Writing System)
**Integration Point**: When QWRITE generates LinkedIn post with format "Carousel"

```markdown
**Format**: Carousel (6-8 slides)
```

**Workflow**:
1. QWRITE generates markdown post (as normal)
2. Auto-invoke QPPT skill with generated markdown
3. Output: markdown post + .pptx carousel

**Implementation**:
```bash
# Within QWRITE polish phase
if post_format == "Carousel":
    python scripts/trigger-qppt.py post.md --auto
```

### QPOLISH (Content Polishing)
**Integration Point**: Social posts marked "Carousel" in content calendar

During QPOLISH phase:
- Generate PowerPoint from markdown
- Validate brand compliance
- Output carousel alongside text post

### Content Calendar
**Metadata Enhancement**:
```markdown
**Format**: Carousel (6-8 slides)
**Background**: circuit-board.png (or default)
**Icon Style**: lucide
```

When processing weekly content:
- Identify carousel posts
- Batch-generate all carousels
- Output to `content/social/week-XX/carousels/`

## Usage Examples

### Example 1: HTML-First Carousel (RECOMMENDED)

```bash
# Invoke via skill (HTML-first approach)
QPPT: Generate carousel from content/social/week-01/W01-LI-post1-permission-architecture.md using HTML approach

# Orchestrator executes:
# 1. Parse content (slide-optimizer.py)
python3 scripts/slide-optimizer.py content/social/week-01/W01-LI-post1.md --target-slides 8 > slides.json

# 2. Generate HTML (slide-html-generator.py)
python3 scripts/slide-html-generator.py slides.json --output-dir html/

# 3. Screenshot slides (screenshot-generator.py)
python3 scripts/screenshot-generator.py html/*.html --output-dir carousel/

# Output:
# ✓ Content parsed: 8 slides (word limits enforced)
# ✓ HTML generated: 8 files with embedded fonts/icons
# ✓ Screenshots captured: 8 PNG images at 1080×1080
# ✓ Contrast validation: PASS (all text WCAG AA compliant)
# ✓ Output: carousel/slide-1.png ... carousel/slide-8.png
# ✓ Total size: 2.4 MB
#
# Ready to upload directly to LinkedIn!
```

**Direct tool usage** (manual workflow):
```bash
# Step 1: Parse markdown → slides.json
python3 scripts/slide-optimizer.py post.md --target-slides 8 > slides.json

# Step 2: Generate HTML
python3 scripts/slide-html-generator.py slides.json --output-dir html/

# Step 3: Screenshot HTML → PNG
python3 scripts/screenshot-generator.py html/*.html --output-dir carousel/

# Optional: Check contrast
python3 scripts/color-contrast-validator.py --background "#171d28"
```

### Example 2: Basic PowerPoint Generation (Fallback)

```bash
# Invoke via skill
QPPT: Generate carousel from content/social/week-01/W01-LI-post1-permission-architecture.md

# Orchestrator executes:
# 1. Parse content (8 slides optimized)
# 2. Fetch icons (8 icons, 6 cached, 2 downloaded)
# 3. Generate PPT (1080×1080, circuit-board background)
# 4. Validate brand (PASS)
# 5. Export: W01-LI-post1-carousel.pptx

# Output:
# ✓ Content parsed: 8 slides optimized
# ✓ Icons fetched: 8/8 ready (6 cached, 2 new)
# ✓ Presentation generated: 1080×1080px square
# ✓ Brand validation: PASS (1 warning: font fallback)
# ✓ File saved: content/social/week-01/W01-LI-post1-carousel.pptx
# ✓ Size: 2.4 MB (LinkedIn optimized)
```

### Example 2: Custom Background and Portrait Format

```bash
# Direct tool usage
python scripts/slide-optimizer.py content/post.md --target-slides 8 > slides.json
python scripts/ppt-generator.py slides.json \
  --background ~/Downloads/tech-gradient.png \
  --format portrait \
  --output carousel-portrait.pptx

# Output:
# ✓ Presentation: 1080×1350px (portrait)
# ✓ Background: tech-gradient.png applied
# ✓ 8 slides generated
# ✓ File: carousel-portrait.pptx (3.1 MB)
```

### Example 3: Batch Generation for Content Calendar

```bash
# Generate all Week 1 carousels
QPPT: Batch generate carousels for content/social/week-01/*.md (where format=Carousel)

# Orchestrator:
# 1. Find all markdown files with "Format: Carousel"
# 2. Parse each (parallel)
# 3. Fetch all unique icons (deduplicated, cached)
# 4. Generate PPTs (parallel)
# 5. Validate all (parallel)
# 6. Output to carousels/ subdirectory

# Output:
# ✓ Found 3 carousel posts
# ✓ Icons: 18 total (14 cached, 4 new)
# ✓ Generated:
#   - W01-LI-post1-carousel.pptx (8 slides, 2.4 MB)
#   - W01-LI-post3-carousel.pptx (7 slides, 2.1 MB)
#   - W01-LI-post5-carousel.pptx (9 slides, 2.8 MB)
# ✓ All validations: PASS
# ✓ Total time: 45 seconds
```

## Advanced Features (Future)

### Phase 2: Animation Support
- Subtle slide transitions (fade, push)
- Icon entrance animations (scale, fade-in)
- Text reveal animations (per bullet)

### Phase 3: A/B Testing Variants
- Generate 2-3 design variants per carousel
- Different color schemes (tech, minimal, bold)
- Different icon sets (lucide vs phosphor)
- Different layouts (center vs left-aligned)

### Phase 4: Analytics Integration
- Track which slides perform best (engagement)
- Learn from high-performing carousel patterns
- Auto-optimize future carousels based on data

## Troubleshooting

### Issue: Playwright not installed
**Solution**:
```bash
pip install playwright
playwright install chromium
```
If `playwright install` fails, install manually:
```bash
playwright install --with-deps chromium
```

### Issue: Screenshots show broken fonts
**Solution**:
- Web fonts load from Google Fonts CDN (internet required)
- Check internet connection during screenshot generation
- Fonts load automatically, no installation needed

### Issue: Text color black-on-black
**Solution**:
- This should be fixed in v2.0 with automatic contrast detection
- Verify color-contrast-validator.py is callable
- Check background color hex value is correct
- Fallback: Manually set text color in HTML template

### Issue: Playwright timeout or crash
**Solution**:
```bash
# Increase timeout in screenshot-generator.py
page.wait_for_timeout(2000)  # 2 seconds instead of 1

# Or run with visible browser for debugging
browser = p.chromium.launch(headless=False)
```

### Issue: Fonts not found (PowerPoint fallback only)
**Solution**:
- Install fonts: `brew install --cask font-poppins font-inter` (macOS)
- Or accept fallback to Arial/Helvetica
- Validation will show warning but proceed

### Issue: Icons not downloading (PowerPoint fallback only)
**Solution**:
- Check internet connection
- Verify Iconify API: `curl https://api.iconify.design/lucide/users-2.svg`
- Use cached icons if available
- Fallback to default icon if needed

### Issue: Background image too large (file size)
**Solution**:
- Compress image: `convert input.png -quality 85 -resize 1080x1080 output.png`
- Use JPEG instead of PNG for photos
- Target: Background image <500KB

### Issue: PowerPoint won't open (PowerPoint fallback only)
**Solution**:
- Verify python-pptx version: `pip show python-pptx` (≥0.6.21)
- Check file permissions
- Re-run brand-validator to check corruption

## Dependencies

### Python Libraries (HTML-First Approach)
```bash
# Primary dependencies
pip install playwright Pillow

# Install Playwright browser (Chromium)
playwright install chromium  # ~200MB download

# Optional (PowerPoint fallback)
pip install python-pptx requests
```

### Python Libraries (PowerPoint Fallback)
```bash
pip install python-pptx Pillow requests
```

### System Requirements
- Python 3.8+
- Internet connection (web fonts, Iconify icons load from CDN)
- 250MB disk space (Playwright Chromium browser)
- 50MB disk space (icon cache, PowerPoint fallback only)
- Optional: Poppins and Inter fonts installed (PowerPoint fallback only)

### Font Installation
```bash
# macOS
brew install --cask font-poppins font-inter

# Linux (Ubuntu/Debian)
sudo apt install fonts-inter fonts-poppins

# Windows
# Download from Google Fonts and install manually
```

## Performance Metrics

### Generation Speed
- **First carousel** (no cache): 30-45 seconds
- **Subsequent carousels** (cached icons): 10-15 seconds
- **Batch generation** (5 carousels): 60-90 seconds

### File Sizes
- **Without custom background**: 0.5-1 MB
- **With optimized background**: 2-3 MB
- **Maximum LinkedIn upload**: 10 MB

### Cache Efficiency
- **Icon reuse rate**: 70-80% (after 5 carousels)
- **Cache size**: ~5-10 MB (100 icons)
- **Cache hit speedup**: 5x faster generation

## Success Criteria

### Phase 1: Critical Fixes ✅ (v2.0 - COMPLETED)
- ✅ **Contrast detection**: No more black-on-black text (color-contrast-validator.py)
- ✅ **Text limits enforced**: Max 30 words, max 5 lines per slide
- ✅ **Better content parsing**: Maintains narrative flow (slide-optimizer.py v2)
- ✅ **Word/line counts**: Track metrics in slides.json output

### Phase 2: HTML-First Approach ✅ (v2.0 - COMPLETED)
- ✅ **HTML generation**: slide-html-generator.py creates styled HTML with embedded CSS
- ✅ **Screenshot automation**: screenshot-generator.py uses Playwright
- ✅ **Web fonts**: Google Fonts (Poppins, Inter) load automatically
- ✅ **Iconify integration**: Web icons (no download required)
- ✅ **Professional quality**: Anti-aliased text, crisp rendering
- ✅ **PNG output**: Ready for direct LinkedIn upload

### Phase 3: Template Library (FUTURE)
- Custom templates (tech, minimal, bold, professional, creative)
- Template selector (user chooses style)
- Brand guidelines per template
- Animation support (subtle transitions)

### Phase 4: Analytics & Optimization (FUTURE)
- A/B testing variants (3 designs per carousel)
- Analytics integration (track slide performance)
- Auto-optimize based on engagement data
- Voice-activated generation

## References (Load on-demand)

### references/brand-guidelines.json
Sparkry brand specifications (colors, fonts, spacing, logo zone). Load during initialization and validation.

### references/slide-layouts.json
Layout templates for each slide type (hook, framework, example, diagnostic, CTA). Load during presentation generation.

### references/icon-mappings.json
Keyword-to-icon mappings for automatic icon suggestion. Load during content parsing.

## Parallel Work Coordination

When part of QPPT task:

1. **Focus**: PowerPoint carousel generation and brand compliance
2. **Tools**: slide-optimizer.py, ppt-generator.py, icon-fetcher.py, brand-validator.py
3. **Output**: .pptx file + validation report + preview images (optional)
4. **Format**:
   ```markdown
   ## PPT Carousel Output

   ### Generation Summary
   - Slides: 8
   - Icons: 8/8 ready (6 cached, 2 new)
   - Format: 1080×1080px (square)
   - Background: circuit-board.png applied
   - File size: 2.4 MB

   ### Brand Validation
   - Colors: PASS
   - Fonts: WARNING (fallback to Arial)
   - Logo Zone: PASS
   - Spacing: PASS
   - Overall: PASS (1 warning)

   ### Output Files
   - Presentation: content/social/week-01/W01-LI-post1-carousel.pptx
   - Manifest: content/social/week-01/W01-LI-post1-carousel-manifest.json
   - Preview: content/social/week-01/W01-LI-post1-carousel-preview.png (optional)
   ```

## Notes

- **Icon caching**: Saves 5x time on subsequent generations, cache expires after 90 days
- **Font availability**: Poppins/Inter preferred, Arial fallback acceptable (shows warning)
- **LinkedIn optimization**: Square (1080×1080) performs best on mobile feed
- **File size**: Keep .pptx under 10MB for LinkedIn upload, compress background images if needed
- **ROI**: After 3 carousels, saves 6+ hours vs manual design (2 hours per carousel manual)
