---
name: Visual Content Generator
description: Generate eye-catching hero images and framework/diagram visuals from article content using HTML-to-image conversion for maximum design quality
version: 1.0.0
tools: [generate-hero-image.py, convert-ascii-to-visual.py, detect-visual-opportunities.py, render-html-to-image.py]
references: [templates/hero-image.html, templates/framework-diagram.html, examples/ascii-patterns.md, brand-guidelines.json]
claude_tools: Read, Grep, Glob, Edit, Write, Bash
trigger: QVISUAL
---

# Visual Content Generator Skill

## Role
You are the "Visual Content Generator", a specialist in generating eye-catching hero images and framework/diagram visuals from article content using HTML-to-image conversion (same approach as LinkedIn carousel generation) for maximum design quality.

## Core Expertise

### 1. Hero Image Generation
Create branded hero images from article metadata (title + key insight).

**When to load**: `references/templates/hero-image.html`
- Extract title from markdown H1
- Extract subtitle from first paragraph or hook
- Render HTML template with brand styling (Sparkry colors, fonts)
- Output PNG optimized for social media (1200×630)

### 2. ASCII Art Conversion
Transform ASCII diagrams into professional visuals.

**When to load**: `references/examples/ascii-patterns.md`
- Parse ASCII structure (boxes, arrows, connections)
- Map to HTML/CSS visual representation
- Preserve relationships and flow
- Render as PNG with brand styling

### 3. Framework Visualization
Generate structured diagrams for frameworks mentioned in articles.

**When to load**: `references/templates/framework-diagram.html`
- Detect framework descriptions (lists, steps, processes)
- Create visual hierarchy
- Apply brand colors and typography
- Output scannable diagram

### 4. Automatic Detection
Scan articles for visualizable content opportunities.

**Detection patterns**:
- ASCII art sections (box-drawing characters: ┌─┐│└┘)
- Multi-line frameworks (numbered lists, process flows)
- System architectures
- Decision trees

### 5. HTML-First Approach
Generate visuals as HTML/CSS with Playwright screenshots for maximum design quality.

**Advantages**:
- Full CSS control (gradients, shadows, fonts, icons)
- Automatic contrast detection (WCAG AA compliant)
- Web fonts (Google Fonts: Poppins, Inter)
- Iconify web icons (no download needed)
- Responsive design
- Professional quality (anti-aliased text, crisp rendering)

## Tools Usage

### tools/generate-hero-image.py
**Purpose**: Create hero image from article title and key insight

```bash
python tools/generate-hero-image.py --file content.md --output hero.png

# Output (JSON):
{
  "success": true,
  "visual_path": "content/visuals/week-02/W02-THU-article-hero.png",
  "title": "Article Title",
  "subtitle": "Key insight from first paragraph",
  "size": {
    "width": 1200,
    "height": 630
  },
  "render_time_ms": 342
}
```

**Arguments**:
- `--file PATH`: Path to markdown article (required)
- `--output PATH`: Output PNG path (optional, auto-generated if not provided)
- `--style {bold,minimal,gradient}`: Visual style (default: gradient)
- `--width INT`: Image width (default: 1200)
- `--height INT`: Image height (default: 630)

**Logic**:
1. Parse markdown to extract H1 title
2. Extract first paragraph or hook as subtitle
3. Load HTML template (`references/templates/hero-image.html`)
4. Inject title and subtitle with variable substitution
5. Call `render-html-to-image.py` to generate PNG
6. Save to `content/visuals/week-##/` directory

### tools/convert-ascii-to-visual.py
**Purpose**: Transform ASCII art into professional diagram

```bash
python tools/convert-ascii-to-visual.py --ascii-input "ASCII content" --output diagram.png --title "Framework Name"

# Output (JSON):
{
  "success": true,
  "visual_path": "content/visuals/diagram.png",
  "detected_type": "flowchart",
  "nodes": 4,
  "connections": 3,
  "render_time_ms": 520
}
```

**Arguments**:
- `--ascii-input TEXT`: ASCII art content (required)
- `--output PATH`: Output PNG path (required)
- `--style {framework,flowchart,tree}`: Diagram style (default: framework)
- `--title TEXT`: Optional title above diagram

**Logic**:
1. Parse ASCII structure:
   - Detect boxes (┌─┐│└┘├┤┬┴┼)
   - Detect arrows (→ ← ↑ ↓)
   - Detect connections and relationships
2. Map ASCII structure to HTML/CSS:
   - Boxes → `<div>` with borders
   - Arrows → CSS pseudo-elements or SVG
   - Layout → Flexbox or Grid
3. Load framework diagram template
4. Inject diagram HTML and title
5. Render to PNG using Playwright

### tools/detect-visual-opportunities.py
**Purpose**: Scan article for visualizable content

```bash
python tools/detect-visual-opportunities.py --file content.md

# Output (JSON):
{
  "success": true,
  "article": "content/articles/week-02/W02-THU-article.md",
  "opportunities": [
    {
      "type": "hero",
      "suggested": true,
      "content": {
        "title": "Article Title",
        "subtitle": "Key insight..."
      }
    },
    {
      "type": "ascii_diagram",
      "location": "Line 145-160",
      "content": "┌─────┐\n│ Box │\n└─────┘",
      "suggested_style": "flowchart"
    },
    {
      "type": "framework",
      "location": "Section: The Three Pillars",
      "content": "1. Pillar A\n2. Pillar B\n3. Pillar C",
      "suggested_style": "framework"
    }
  ],
  "total_opportunities": 3
}
```

**Arguments**:
- `--file PATH`: Path to markdown article (required)
- `--suggest-only`: Only suggest, don't generate (default: false)

**Detection Logic**:
1. **Hero image** (always suggest): Extract H1 + first paragraph
2. **ASCII art sections**:
   - Scan for code blocks with box-drawing characters
   - Scan for indented text with ASCII borders
   - Detect flowchart-style text with arrows
3. **Framework descriptions**:
   - Detect numbered lists (3+ items)
   - Detect section headers like "The X Framework"
   - Detect process flows ("Step 1", "Step 2", etc.)

### tools/render-html-to-image.py
**Purpose**: Core rendering engine (HTML → PNG via Playwright)

```bash
python tools/render-html-to-image.py --html-file template.html --output image.png --width 1200 --height 630

# Output (JSON):
{
  "success": true,
  "output_path": "image.png",
  "render_time_ms": 342,
  "size": {
    "width": 1200,
    "height": 630
  }
}
```

**Arguments**:
- `--html-file PATH`: HTML template file (required)
- `--output PATH`: Output PNG path (required)
- `--width INT`: Viewport width (default: 1200)
- `--height INT`: Viewport height (default: 630)
- `--scale FLOAT`: DPI scale factor (default: 2)
- `--variables JSON`: Template variables as JSON (optional)

**Implementation**:
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': width, 'height': height})
    page.goto(f'file://{html_file}')
    page.wait_for_timeout(1000)  # Font rendering
    page.screenshot(path=output_png, full_page=False)
```

**Requirements**:
- Playwright installed: `pip install playwright`
- Chromium browser: `playwright install chromium` (~200MB)

## HTML Template System

All visuals rendered from HTML templates with embedded CSS.

### Hero Image Template
**File**: `references/templates/hero-image.html`

**Variables**:
- `{{ title }}`: Article title (H1)
- `{{ subtitle }}`: Key insight or first paragraph

**Styling**:
- Size: 1200×630px (OpenGraph standard)
- Background: Gradient (Sparkry navy → electric blue)
- Typography: Poppins Bold (title), Inter Regular (subtitle)
- Colors: White text on dark gradient
- Layout: Center-aligned, generous whitespace

### Framework Diagram Template
**File**: `references/templates/framework-diagram.html`

**Variables**:
- `{{ title }}`: Diagram title
- `{{ diagram_html }}`: Injected HTML structure from ASCII conversion

**Styling**:
- Size: 1200×800px (4:3 ratio)
- Background: White
- Typography: Poppins (headers), Inter (body)
- Colors: Sparkry palette (navy, orange, electric blue)
- Layout: Title top, diagram center

## ASCII Art Detection Patterns

**Load from**: `references/examples/ascii-patterns.md`

### Pattern 1: Box-Drawing Characters
```
┌─────────────┐
│   Process   │
└─────────────┘
      ↓
┌─────────────┐
│   Outcome   │
└─────────────┘
```

### Pattern 2: ASCII Borders
```
+-------------------+
|   Component A     |
+-------------------+
         |
         v
+-------------------+
|   Component B     |
+-------------------+
```

### Pattern 3: Tree Structures
```
Root
├── Branch 1
│   ├── Leaf 1
│   └── Leaf 2
└── Branch 2
    └── Leaf 3
```

### Pattern 4: Flowcharts
```
[Start] → [Process] → [Decision]
                         ↓ Yes
                      [Action]
```

## Output Directory Structure

```
content/visuals/
├── week-01/
│   ├── W01-TUE-article-hero.png
│   ├── W01-TUE-article-diagram-1.png
│   └── ...
├── week-02/
│   ├── W02-THU-ai-internationalization-hero.png
│   ├── W02-THU-ai-internationalization-diagram-1.png
│   └── ...
```

**Naming convention**: `W##-DAY-slug-{hero|diagram-N}.png`

## Integration with Writing Skill

### Polish Phase Enhancement

**AFTER existing validations in writing skill polish phase, ADD**:

```markdown
6. **Visual Content Generation** (articles only, not social posts)
   - Detect visual opportunities: `python tools/detect-visual-opportunities.py --file <article_path>`
   - Generate hero image (always): `python tools/generate-hero-image.py --file <article_path>`
   - Convert ASCII diagrams (if detected): `python tools/convert-ascii-to-visual.py`
   - Generate framework visuals (if detected)
   - Save to `content/visuals/week-##/`
   - Log visual paths in output
```

### Writing System Output Format Enhancement

**ADD to writing system output**:

```markdown
### Visual Content
- **Hero Image**: content/visuals/week-02/W02-THU-article-hero.png
- **Diagrams**:
  - content/visuals/week-02/W02-THU-article-diagram-1.png (ASCII flowchart)
  - content/visuals/week-02/W02-THU-article-diagram-2.png (Framework: The Three Pillars)
- **Opportunities Detected**: 3 (1 hero, 2 diagrams)
- **Generation Time**: 4.2 seconds
```

### Quality Gates

**Add to Post-Polish quality gates**:

- **VISUAL CONTENT GENERATED** (articles only):
  - Hero image created ✅
  - ASCII diagrams converted (if present) ✅
  - Framework visuals generated (if detected) ✅
  - Visual paths logged ✅
  - All files <500KB ✅
  - All dimensions correct ✅

## Manual Invocation

### Via QVISUAL Shortcut

**Usage examples**:

```bash
# Generate all visuals for article
QVISUAL: Generate visuals for content/articles/week-02/W02-THU-article.md

# Convert specific ASCII art
QVISUAL: Convert this ASCII to diagram:
┌─────────┐
│ Process │
└─────────┘
     ↓
┌─────────┐
│ Outcome │
└─────────┘

# Generate hero image only
QVISUAL: Generate hero image for content/articles/week-02/W02-THU-article.md
```

### Direct Tool Usage

```bash
# Detect opportunities
python .claude/skills/content/visual-content-generator/tools/detect-visual-opportunities.py \
  --file content/articles/week-02/W02-THU-article.md

# Generate hero image
python .claude/skills/content/visual-content-generator/tools/generate-hero-image.py \
  --file content/articles/week-02/W02-THU-article.md \
  --output content/visuals/week-02/W02-THU-hero.png

# Convert ASCII art
python .claude/skills/content/visual-content-generator/tools/convert-ascii-to-visual.py \
  --ascii-input "$(cat ascii-diagram.txt)" \
  --output diagram.png \
  --title "Permission Architecture"
```

## Performance Metrics

### Target Latency
- **Hero image**: <3 seconds
- **ASCII diagram**: <5 seconds
- **Framework visual**: <5 seconds
- **Full article scan + generation**: <10 seconds

### File Sizes
- **Hero images**: 200-400KB (target <500KB)
- **Diagrams**: 150-350KB (target <500KB)
- **Total per article**: <2MB

### Quality
- **Resolution**: 2x DPI scaling (retina-ready)
- **Contrast**: WCAG AA compliant (4.5:1 minimum)
- **Typography**: Web fonts loaded from Google Fonts
- **Brand compliance**: Sparkry color palette enforced

## Error Handling

### Missing Dependencies
- **Playwright not installed**: Warn user, provide install command, skip generation
- **Chromium not installed**: Provide `playwright install chromium` command

### Rendering Failures
- **HTML template not found**: Use minimal fallback template
- **Font loading fails**: Fallback to system fonts
- **Screenshot timeout**: Increase wait time, retry once

### Content Issues
- **No ASCII art detected**: Generate hero only (expected behavior)
- **Empty title/subtitle**: Use generic placeholder, warn user
- **Malformed ASCII**: Skip conversion, log warning

### File System
- **Output directory missing**: Create automatically
- **Permission denied**: Log error, suggest chmod
- **Disk full**: Log error, skip generation

## Story Point Estimation

- **Generate hero image for article**: 0.1 SP
- **Convert ASCII diagram**: 0.2 SP
- **Generate framework visual**: 0.3 SP
- **Full article processing (hero + 2-3 diagrams)**: 0.5 SP
- **Batch processing (5 articles)**: 1 SP

**Reference**: `docs/project/PLANNING-POKER.md`

## Integration with Existing Agents

### QWRITE (Writing System)
**Integration Point**: Polish phase (after link validation, before Google Docs publishing)

**Workflow**:
1. QWRITE completes draft and editorial passes
2. Polish phase invokes visual content generator
3. Detect visual opportunities
4. Generate hero + diagrams
5. Log visual paths in output
6. Proceed with Google Docs publishing

### QPPT (PowerPoint Carousel)
**Potential Synergy**: Share HTML rendering engine and brand templates

**Future Enhancement**: Convert article visuals to carousel slides automatically

## Parallel Work Coordination

When part of QVISUAL task:

1. **Focus**: Visual content generation from articles
2. **Tools**: generate-hero-image.py, detect-visual-opportunities.py, render-html-to-image.py
3. **Output**: PNG images in `content/visuals/week-##/` + generation summary
4. **Format**:
   ```markdown
   ## Visual Content Generator Output

   ### Article Processed
   - **File**: content/articles/week-02/W02-THU-article.md
   - **Title**: "AI Internationalization Challenges"

   ### Opportunities Detected
   - Hero image: Yes (always)
   - ASCII diagrams: 2 found
   - Framework visuals: 1 suggested

   ### Generated Visuals
   1. **Hero Image**: content/visuals/week-02/W02-THU-article-hero.png
      - Size: 1200×630px
      - File size: 287KB
      - Render time: 2.8s

   2. **Diagram 1**: content/visuals/week-02/W02-THU-article-diagram-1.png
      - Type: Flowchart (ASCII conversion)
      - Size: 1200×800px
      - File size: 194KB
      - Render time: 4.2s

   3. **Diagram 2**: content/visuals/week-02/W02-THU-article-diagram-2.png
      - Type: Framework (The Three Layers)
      - Size: 1200×800px
      - File size: 218KB
      - Render time: 3.9s

   ### Summary
   - **Total visuals**: 3
   - **Total size**: 699KB
   - **Total time**: 10.9 seconds
   - **Status**: ✅ All generated successfully
   ```

## Dependencies

### Python Libraries
```bash
# Required
pip install playwright Pillow

# Install Playwright browser
playwright install chromium  # ~200MB download
```

### System Requirements
- Python 3.8+
- Internet connection (Google Fonts load from CDN)
- 250MB disk space (Playwright Chromium)
- 50MB disk space (visual outputs)

## Troubleshooting

### Issue: Playwright not installed
**Solution**:
```bash
pip install playwright
playwright install chromium
```

### Issue: Screenshots show broken fonts
**Solution**:
- Web fonts load from Google Fonts CDN (internet required)
- Check internet connection during generation
- Fonts load automatically, no local installation needed

### Issue: Playwright timeout
**Solution**:
```bash
# Increase timeout in render-html-to-image.py
page.wait_for_timeout(2000)  # 2 seconds instead of 1

# Or run with visible browser for debugging
browser = p.chromium.launch(headless=False)
```

### Issue: File size too large
**Solution**:
- Reduce image dimensions
- Use PNG compression
- Target: <500KB per image

## Success Criteria

### MVP (Phase 1)
- ✅ Generate hero images from article metadata
- ✅ Detect ASCII art in articles
- ✅ Convert simple ASCII diagrams to visuals
- ✅ Integrate with QWRITE polish phase
- ✅ Manual invocation via QVISUAL

### Phase 2 (Future)
- Advanced ASCII parsing (complex flowcharts, trees)
- Framework auto-generation from numbered lists
- Interactive diagram editing
- Batch processing optimization
- A/B testing visual styles

### Phase 3 (Future)
- Animation support (subtle transitions)
- Video generation from articles
- Social media size optimization
- Analytics integration (track visual engagement)

## References (Load on-demand)

### references/templates/hero-image.html
HTML/CSS template for hero images with Sparkry branding. Load during hero image generation.

### references/templates/framework-diagram.html
HTML/CSS template for framework diagrams. Load during ASCII conversion and framework visualization.

### references/examples/ascii-patterns.md
Common ASCII art patterns and detection rules. Load during opportunity detection.

### references/brand-guidelines.json
Sparkry brand specifications (symlinked from ppt-carousel skill). Load during rendering for color/font enforcement.

## Notes

- **Reuses carousel infrastructure**: Leverages existing HTML-to-image approach from ppt-carousel skill
- **Playwright dependency**: Same as carousel, ~200MB Chromium download
- **Brand consistency**: Uses identical color palette and typography as carousel slides
- **Performance**: <10 seconds per article (hero + 2-3 diagrams)
- **File organization**: Organized by week matching content calendar structure
- **Integration**: Automatic in QWRITE polish phase for articles (not social posts)
