# Skill: Visual Brief + Image Generation

## Trigger
- After generating a post (especially Angle 2: Framework/Mental Model)
- User says "Create a visual for this post"
- Any post containing a framework, matrix, comparison, or tiered concept

## Visual Signature (AllAboutPMM Brand)

The visual must match Sourav's established style from `data/user/visuals/`. Key characteristics:

### Layout Patterns (pick the one that fits the post's content)
| Pattern | When to Use | Example |
|---------|------------|---------|
| **Matrix / Quadrant** | Comparing 2 dimensions (e.g., "Two ways of positioning agentic AI") | 2-column layout with headers, pros/cons, examples |
| **Tiered Progression** | Levels, hierarchy, or good/better/best (e.g., "Six Levels of Problem-Solving") | Stacked horizontal bars, ascending left-to-right or bottom-to-top |
| **Concentric Circles** | Nested concepts, zooming in/out (e.g., "Positioning as concentric dials") | Bullseye diagram with labels at each ring |
| **Decision Tree / Branch** | Choices, paths, or "what approach?" (e.g., "What's the right category approach?") | Central question branching to 2-3 options with color-coded backgrounds |
| **Stacked Cards** | Sequential progression (e.g., "Clear → Compelling → Unique") | Vertical stack of labeled boxes with directional arrows |
| **Checklist Infographic** | Lists with structure (e.g., corporate trajectory steps) | Left-aligned labels with right-aligned descriptions, color-coded rows |
| **Quote Card** | One powerful insight, punchy line (e.g., "As ideas get cheaper, decisions get more expensive") | Large bold text on solid color background with keyword highlights |

### Color Palette
- **Primary backgrounds:** Warm muted pastels — sage green (#C5E1A5), dusty rose/pink (#F8BBD0), cream/off-white (#FFF8E1), golden yellow (#FFF59D), soft teal
- **Accent backgrounds:** Soft lavender, light blue (#BBDEFB), lime green (#DCEDC8)
- **Bold accents (sparingly):** Deep blue/indigo (#3F51B5), vibrant purple (#7C4DFF) — for emphasis bars or headers
- **Text:** Black or very dark gray on light backgrounds. White on dark accent bars.
- **Each row/section in a tiered layout gets a DIFFERENT pastel color** — this is a signature trait

### Typography
- **Headers:** Bold display font, large (the main concept in 3-6 words)
- **Sub-headers/labels:** Bold sans-serif, medium, often inside tag-shaped or pill-shaped containers
- **Body text:** Clean sans-serif, regular weight, smaller
- **Keyword emphasis:** Highlighted words in contrasting pill/tag backgrounds (pink highlight on yellow, blue highlight on cream)

### Brand Mark
- **"AllAboutPMM"** logo/text in bottom-right corner
- Clean, professional — not decorative

### Design Principles
1. **Generous white space** — never cramped
2. **One concept per image** — if the post has 3 ideas, pick the ONE most visual
3. **Information hierarchy is crystal clear** — viewer gets the main point in 2 seconds
4. **Framework structure is visible** — the layout itself communicates the relationship between concepts
5. **No decorative illustrations, icons, or stock imagery** — pure information design

## Process

### Step 1: Analyze the Post
Read the post and identify:
- The core concept that would benefit from visualization
- The structural relationship (hierarchy? comparison? progression? branching?)
- The key labels/terms that need to appear
- Any data points that should be visualized

### Step 2: Select Layout Pattern
Match the concept to one of the 7 layout patterns above. Pick the BEST fit, not the most complex.

### Step 3: Generate the Visual Brief
Produce a structured brief with:

```
VISUAL BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Layout: [Pattern name]
Title: [Main header text — 3-6 words, bold]
Subtitle: [Optional — one line of context]

Sections:
  1. [Label] — [Description] — [Color: e.g., dusty rose]
  2. [Label] — [Description] — [Color: e.g., sage green]
  3. [Label] — [Description] — [Color: e.g., golden yellow]

Emphasis: [Which word/phrase gets a highlight pill]
Brand: AllAboutPMM — bottom right
Dimensions: 1200x1200 (square, LinkedIn optimized)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 4: Generate the Image
Use the visual brief to generate an image. The prompt to the image generation tool should:

1. **Reference the specific layout pattern** with spatial instructions
2. **Specify exact colors** using the palette above
3. **Include all text content** that should appear in the image
4. **Mandate the style:** clean infographic, no illustrations, no icons, no stock art, generous white space, bold typography, pastel color blocks
5. **Include "AllAboutPMM" branding** in bottom-right corner
6. **Specify 1200x1200** square format for LinkedIn

### Image Generation Prompt Template
```
Create a clean, modern infographic for LinkedIn (1200x1200 square).

LAYOUT: [Pattern — e.g., "tiered horizontal bars ascending left-to-right"]
TITLE: "[Header text]" in large bold black sans-serif font at the top
[Describe each section with exact text, colors, and spatial positioning]

STYLE: Warm muted pastels (sage green, dusty rose, cream, golden yellow).
Each section uses a different pastel color block. Bold sans-serif typography.
Generous white space. No icons, no illustrations, no decorative elements.
Pure information design. "AllAboutPMM" in small text, bottom-right corner.
```

### Step 5: Present to User
Show:
- The visual brief (text)
- The generated image
- Ask: "Want me to adjust the layout, colors, or content?"

## When NOT to Generate a Visual
- Pure opinion posts with no structural concept
- Story-led posts (Angle 3) that rely on narrative, not frameworks
- Short posts under 500 characters
- Posts where the insight is in the LANGUAGE, not the STRUCTURE

## Reference Images
Always check `data/user/visuals/` for style calibration before generating. Key references:
- Tiered progression: `1730213731219.jpeg` (corporate trajectory), `1763223928066.jpeg` (problem-solving levels)
- Comparison matrix: `1737731539582.jpeg` (positioning agentic AI)
- Concentric circles: `1722370634418.jpeg` (positioning dials)
- Stacked cards: `1724334040925.jpeg` (clear → compelling → unique)
- Decision tree: `1741523397761.jpeg` (category approach)
- Quote card: `1752959305250.jpeg` (ideas cheaper, decisions expensive)
