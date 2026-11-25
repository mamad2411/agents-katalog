---
name: thumbnail
description: "Create premium YouTube thumbnails inspired by top French thumbnail agencies (thumbstudio.fr style) and proven high-performing YouTube thumbnails. Generates professional-grade thumbnails with multi-layered compositions, graphic design elements (banners, ribbons, icons, badges, arrows, product mockups), clean subject cutouts, bold 3D text on colored bands, and official brand logos. Uses Gemini API for AI image generation and ImageMagick for compositing. Use when the user asks to create, design, or make a YouTube thumbnail."
allowed-tools: Bash(python3 *), Bash(pip3 install *), Bash(curl *), Bash(magick *), Bash(convert *), Bash(composite *), Bash(identify *), Bash(ls *), Bash(mkdir *), Bash(cp *), Bash(open *), Bash(base64 *), Bash(yt-dlp *)
---

# Premium YouTube Thumbnail Generator

Create agency-quality YouTube thumbnails by combining thumbstudio.fr design principles with patterns from real high-performing YouTube thumbnails.

## Step 0: Study References BEFORE Every Generation

CRITICAL: Before generating ANY thumbnail, you MUST:

1. **Study `screen.png`** — thumbstudio.fr portfolio showing the target design quality level
2. **Study `references/`** — 15 real YouTube thumbnails from videos with 34K-600K views on "Claude Code"
3. **If the topic differs from Claude Code**, scrape new references first (see Step 0b below)

### What to Learn from Each Reference Source

**From thumbstudio.fr (`screen.png`) — DESIGN CRAFT:**
- Multi-layered graphic design compositions (5-7 layers)
- Text on colored banners/ribbons (NEVER floating)
- Flat vector icons inside colored circles with badge overlays
- Controlled 2-3 color palettes matched to topic
- Extreme contrast: bright subjects on dark backgrounds
- Professional subject cutouts with colored rim lighting

**From YouTube references (`references/`) — WHAT ACTUALLY GETS CLICKS:**
- Product screenshots/mockups are POWERFUL (terminal, app, phone)
- Curved arrows pointing to key elements appear in 40% of top thumbnails
- Yellow highlight bands on key words ("SYSTEM" on yellow = 306K views)
- Close-up faces (40-50% of frame) outperform distant shots
- The official brand logo/icon is a MUST (Claude starburst in every top performer)
- Simpler layouts with 3-4 strong elements beat cluttered 7-layer designs
- Whiteboard/educational style performs extremely well (600K views)
- Series numbering in colored circles creates binge triggers

### Key Insight: Blend Both Worlds

The BEST thumbnails combine thumbstudio.fr's **design craft** with YouTube's **click psychology**:
- Use thumbstudio.fr's banner/ribbon technique for text
- Use YouTube's arrow + product screenshot patterns
- Use thumbstudio.fr's color grading and rim lighting
- Use YouTube's close-up face + huge readable text approach
- Keep it to 4-5 intentional layers (not 7 cluttered ones)

## Step 0b: Scrape Topic-Specific References (if topic differs)

When creating thumbnails for a topic OTHER than Claude Code, scrape fresh references:

```bash
# Search YouTube for the topic, sorted by view count
yt-dlp --flat-playlist --print "%(id)s %(view_count)s %(title)s" \
  "ytsearch30:[TOPIC] tutorial" 2>/dev/null | sort -t' ' -k2 -nr | head -15

# Download thumbnails from top performers (>10K views)
mkdir -p references/
for VIDEO_ID in [ids_from_above]; do
  curl -s -o "references/${VIEW_COUNT}_${SLUG}.jpg" \
    "https://img.youtube.com/vi/${VIDEO_ID}/maxresdefault.jpg"
done
```

Study the downloaded thumbnails with the Read tool before generating.

## Reference Analysis: Patterns from 15 Top YouTube Thumbnails

### Pattern 1: "Whiteboard Educator" (600K views — HIGHEST performer)
- Subject on right (40% of frame), warm smile
- Whiteboard/flat surface with handwritten-style text and diagrams
- Numbered list showing video structure (1. Setup, 2. Subagents...)
- Brand logo prominently placed top-left
- Flowchart/diagram adds visual interest
- **When to use**: Tutorial/course content, structured educational videos

### Pattern 2: "Product Showcase + Big Text" (481K, 259K views)
- Dark/black background for maximum contrast
- HUGE bold white text: "CLAUDE CODE" (fills 50-60% of width)
- Brand logo (starburst) as standalone graphic element
- Key subtitle on YELLOW BANNER strip ("FOR BEGINNERS")
- Minimal design — only 3 elements but all MASSIVE
- **When to use**: Beginner tutorials, tool introductions, simple hooks

### Pattern 3: "Subject + Screenshot + Arrow" (306K, 215K views)
- Subject cutout on one side with glow/halo effect
- Product screenshot (terminal, app UI) on opposite side
- Curved arrow pointing from subject to screenshot (or to text)
- Yellow highlight band on ONE keyword for emphasis
- Multi-level text hierarchy: hero + smaller subtitle
- **When to use**: Guides, walkthroughs, "how I use X" videos

### Pattern 4: "Terminal ASCII Art Brand" (253K, 594K views)
- Claude Code ASCII art from terminal as graphic identity
- Subject with expressive gesture (open hand, pointing)
- Cursive or contrasting font for subtitle ("Pro Tips")
- Episode numbering in colored circle for series
- Dark background, minimal additional elements
- **When to use**: Tips, tricks, series content, advanced features

### Pattern 5: "Cinematic Product Demo" (115K, 110K views)
- Subject holding/presenting a device (laptop, phone)
- Multiple floating screens/dashboards in background
- Large curved arrow pointing to the product
- Bold text at bottom (often yellow/gold on dark)
- More complex composition, cinematic color grading
- **When to use**: Product reviews, "build X with Y", app demos

### Pattern 6: "Grid/Levels Comparison" (34K views)
- Multi-column layout showing progression
- Numbers prominently displayed (1, 2, 3, 4, 5, 6)
- Each column has different visual treatment
- "LEVEL" text repeated creates pattern
- Light/neutral background with brand color accents
- **When to use**: Comparison content, skill levels, tier lists

## Workflow

### Step 1: Gather Information

Ask the user for:
1. **Video topic** — What the video is about
2. **Text overlay** — Hero text + subtitle (suggest ALL CAPS, max 2-5 words). **ALL TEXT MUST BE IN FRENCH** unless the user explicitly requests another language.
3. **Subject photo(s)** — Path(s). Default: `assets/sophiene-muscle.jpg`
4. **Brand/Logo** — Any brand to feature? If yes, download OFFICIAL logo
5. **Mood/Color** — Dominant accent color (suggest based on topic)
6. **Layout pattern** — Which of the 6 patterns above fits best? (suggest one)

### Step 2: Fetch Official Logos (if needed)

**NEVER generate logos with AI. Always download official assets.**

1. Search: `"[brand name] official logo PNG transparent"`
2. Download from: official press kits, GitHub repos, Wikipedia SVG, brandfetch.com
3. Save: `curl -L -o /tmp/logo_[brand].png "[url]"`
4. Convert SVG if needed: `magick -background none /tmp/logo.svg -resize 300x300 /tmp/logo.png`
5. **Verify** by reading the file before using

### Step 3: Generate Thumbnail with Gemini API

**API Setup:**
```bash
magick [subject_photo] -resize 400x225 -quality 75 /tmp/subject_input.jpg
SUBJECT_B64=$(base64 -i /tmp/subject_input.jpg)
```

**API Call:**
```bash
curl -s -o /tmp/gemini_thumb_N.json \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"contents\": [{
      \"parts\": [
        {\"inlineData\": {\"mimeType\": \"image/jpeg\", \"data\": \"$SUBJECT_B64\"}},
        {\"text\": \"[USE PROMPT TEMPLATES BELOW]\"}
      ]
    }],
    \"generationConfig\": {\"responseModalities\": [\"IMAGE\", \"TEXT\"]}
  }"
```

**Extract image:**
```python
python3 << 'PYEOF'
import json, base64
with open("/tmp/gemini_thumb_N.json") as f:
    data = json.load(f)
parts = data["candidates"][0]["content"]["parts"]
for part in parts:
    if "inlineData" in part:
        img = base64.b64decode(part["inlineData"]["data"])
        with open("/tmp/thumbnail_raw_N.png", "wb") as f:
            f.write(img)
        print(f"Saved ({len(img)} bytes)")
PYEOF
```

**If generation fails (IMAGE_OTHER error):** Simplify the prompt — remove specific text requests, reduce layer count, and retry. Gemini sometimes refuses complex text-heavy prompts.

### Step 4: Post-Process with ImageMagick

```bash
magick /tmp/thumbnail_raw_N.png \
  -resize 1280x720^ -gravity center -extent 1280x720 \
  -unsharp 0x1+1.2+0 \
  -modulate 100,118,97 \
  -brightness-contrast 6x12 \
  /tmp/thumb_enhanced_N.png
```

**Composite official logo (with glow matching accent color):**
```bash
magick /tmp/thumb_enhanced_N.png \
  \( /tmp/logo_brand.png -resize 160x160 -background none \
     \( +clone -background "[ACCENT_COLOR]" -shadow 100x12+0+0 \) +swap \
     -background none -layers merge +repage \) \
  -gravity NorthWest -geometry +50+35 -composite \
  [OUTPUT_DIR]/variation_N.png
```

### Step 5: Present and Iterate

Show ALL variations to user. Offer: different pattern, bigger text, add/change logo, more dramatic, different layout, add arrow, add screenshot.

## Prompt Templates

### CRITICAL PROMPTING RULES

When prompting Gemini for agency-quality thumbnails:

1. **Reference a specific pattern** from the analysis above — don't generic-prompt
2. **Describe 4-5 intentional layers** — background, subject, text area, graphic elements, logo space
3. **Text on colored banners** — NEVER floating. Specify: "white text ON a [color] banner strip"
4. **Include at least ONE graphic element** — curved arrow, product screenshot, icon, badge
5. **Specify exact hex colors** — not "colorful" but "orange (#D4825A) banner with white bold text"
6. **Request yellow highlight on ONE keyword** — this is the #1 pattern in top performers
7. **Emphasize massive text** — "text fills 50% of thumbnail width, readable at 120px thumbnail size"
8. **Request depth** — "subject has subtle glow halo, background is blurred/dark, text pops forward"

### Template 1: Product Showcase + Big Text (Best for tutorials)
Based on Pattern 2 — 481K & 259K views

```
Create a premium YouTube thumbnail (16:9 wide) with an ultra-clean, high-impact design like the highest-performing YouTube tech tutorials.

BACKGROUND: Very dark [THEME] background (almost black, #0D0D0D to #1A1A1A gradient). Subtle [ACCENT COLOR] ambient glow in the center. Faint grid pattern or code texture barely visible for depth.

SUBJECT: This person as an ultra-sharp cutout on the RIGHT side, occupying 40-45% of frame. Extremely close crop — head and upper shoulders only, face fills the space. Strong [ACCENT COLOR] rim lighting on hair and shoulder edges. Professional studio-quality cutout with CLEAN edges. Bright, well-lit face against the dark background. Expression: [confident smile / excited / intense focus].

TEXT AREA (LEFT SIDE):
- HERO TEXT: "[MAIN TEXT]" in MASSIVE bold white letters with subtle drop shadow. This text must be ENORMOUS — filling 50% of thumbnail width. Clean modern sans-serif font, thick weight. Each word on its own line for maximum size.
- HIGHLIGHT WORD: "[KEY WORD]" on a bright [yellow #FFE033 / orange #FF6B35 / green #00D26A] banner/highlight strip. The banner extends slightly beyond the text edges. This colored highlight is CRITICAL for click appeal.
- SUBTITLE (optional): "[subtitle]" in smaller [COLOR] text below, clean and readable.

BRAND ELEMENT: [BRAND] logo/icon placed prominently — either top-left corner (medium size) or integrated near the text. The logo should have a subtle [ACCENT COLOR] glow behind it.

GRAPHIC ELEMENT: A curved white arrow pointing from the text toward the subject (or from the logo toward the text). The arrow should be bold and clean, adding visual flow.

OVERALL: Ultra high contrast. The thumbnail must be readable at 120px wide (YouTube mobile suggestion size). Maximum 4 visual elements total. Clean, bold, professional. NOT cluttered — every element is large and deliberate. This should look like a $500 professionally designed thumbnail.
```

### Template 2: Subject + Screenshot + Arrow (Best for guides)
Based on Pattern 3 — 306K & 215K views

```
Create a premium YouTube thumbnail (16:9 wide) combining a person with a product/app screenshot, connected by a visual arrow.

BACKGROUND: Dark gradient from [COLOR 1] to near-black. Subtle depth with very faint blurred elements.

LEFT SIDE - SUBJECT: This person as a sharp cutout, close crop of face and upper body. Confident or excited expression. Subtle white/[ACCENT COLOR] glow halo around the edges of the cutout (like a backlight effect). High contrast face.

RIGHT SIDE - PRODUCT SCREENSHOT: A [terminal window / app interface / code editor / phone mockup] showing [DESCRIPTION of what's on screen]. The screenshot should be in a clean device frame (macOS window with red/yellow/green dots, or phone bezel). Slightly angled for 3D perspective. Subtle shadow beneath.

CONNECTING ELEMENT: A bold curved arrow (white or [ACCENT COLOR]) flowing from the subject toward the screenshot. The arrow should be thick, clean, and prominent.

TEXT:
- "[HERO TEXT]" in massive bold white text at the TOP, spanning the full width. Thick black outline for readability.
- "[KEY WORD]" highlighted with a [yellow/orange] banner strip behind it.
- "wish I knew sooner" or "[SUBTITLE]" in smaller text below in [COLOR].

OVERALL: 4-layer composition. Dark cinematic background, bright subject, glowing screenshot, bold text. Every element large and readable at small sizes. Professional YouTube tech tutorial aesthetic.
```

### Template 3: Cinematic Multi-Element (Best for advanced content)
Based on Pattern 5 — 110K-115K views + thumbstudio.fr craft

```
Create a premium YouTube thumbnail (16:9 wide) that looks like it was designed by a top French thumbnail agency (thumbstudio.fr level quality). Multi-layered cinematic composition.

LAYER 1 - BACKGROUND: Dark moody [THEME] background with depth. [DESCRIPTION — floating blurred screens/dashboards, dark code, gradient, bokeh lights]. Very dark overall (almost black in corners) with [ACCENT COLOR] tint in center. Subtle vignette.

LAYER 2 - MID-GROUND: [Describe contextual elements — faint app icons, blurred UI panels, floating code snippets, or product imagery that adds depth. These should be 30-40% opacity, creating atmosphere].

LAYER 3 - SUBJECT: This person as a sharp, crisp cutout in [CENTER / RIGHT], holding or presenting [a laptop / phone / product]. Strong [ACCENT COLOR] rim lighting on edges. Ultra high contrast — face brightly lit. Clean sharp cutout edges.

LAYER 4 - TEXT ON BANNERS:
- A [COLOR] colored banner/ribbon strip in the [lower-left / bottom] area. Slight transparency and gradient.
- "[HERO TEXT]" in massive bold 3D white letters ON the banner. Thick black outline, [ACCENT COLOR] outer glow. ENORMOUS — filling 40-50% of width.
- "[SUBTITLE]" in [COLOR] smaller text, also on a thinner banner strip.

LAYER 5 - OVERLAYS: [Choose 1-2: curved arrow pointing to product, badge with checkmark, brand logo with glow, episode number in colored circle].

OVERALL: Ultra high contrast. Cinematic color grading with [ACCENT COLOR] dominant tones. Dark vignette. This must look like a $500 custom-designed thumbnail. 5 intentional layers, not 7 cluttered ones. Every element deliberately placed.
```

### Template 4: VS / Comparison
Based on thumbstudio.fr "OLD VS NEW" pattern + Pattern 6

```
Create a premium YouTube thumbnail (16:9 wide) showing a dramatic VERSUS comparison.

LAYOUT: Split composition with a bold [diagonal / vertical] divider in the center.

LEFT SIDE: [Subject/element 1] with [COLOR 1] accent tint and lighting. [COLOR 1] glow.
RIGHT SIDE: [Subject/element 2] with [COLOR 2] accent tint and lighting. [COLOR 2] glow.

CENTER DIVIDER: Bold dividing line with energy/lightning effect, OR large "VS" text in white with dramatic glow.

TEXT:
- Labels on each side: "[LABEL 1]" left, "[LABEL 2]" right — in large bold text
- Bottom banner strip: "[MAIN TEXT]" in massive bold white 3D letters on [COLOR] banner
- One keyword on [yellow] highlight strip

GRAPHIC ELEMENTS: Relevant icons or badges on each side (checkmark vs X, or numbered badges).

EFFECTS: High contrast, each side has its own distinct color temperature. Dark vignette. Dramatic cinematic feel.
```

### Template 5: Money / Numbers Callout
Based on thumbstudio.fr "€1 Million" and "+12500€/MOIS" patterns

```
Create a premium YouTube thumbnail (16:9 wide) focused on an impressive number/amount.

SUBJECT: Sharp crisp cutout on [SIDE], [EXPRESSION] expression (shocked or confident), [COLOR] rim lighting, ultra high contrast. Close crop — face fills their side of the frame.

BACKGROUND: Dark elegant gradient. Subtle money/success themed elements (faint euro signs, graph lines, sparkles) at very low opacity.

HERO NUMBER: "[€XX,XXX]" or "[AMOUNT]" in MASSIVE bold 3D [green #00D26A / yellow #FFD700] letters — this number should DOMINATE the thumbnail, filling 60% of the width. Thick black outline, strong glow, 3D depth extrusion. The number is THE main visual element.

TEXT BANNER: [Green/dark] semi-transparent banner strip behind the subtitle: "[SUBTITLE]" in medium white text. The word "[KEY WORD]" highlighted in [red/green] for emphasis.

GRAPHIC ELEMENTS: [1-2 of: upward arrow, sparkle effect, small money bag icon, trending graph line].

EFFECTS: Premium money/success aesthetic. Green and gold accents. Dark luxury feel. Ultra contrast. Subtle golden vignette.
```

### Template 6: Whiteboard / Educational
Based on Pattern 1 — 600K views (HIGHEST performer)

```
Create a premium YouTube thumbnail (16:9 wide) with a clean educational/whiteboard style.

SUBJECT: This person on the RIGHT side (35-40% of frame), warm confident smile, facing slightly left toward the content. High contrast, well-lit face. Clean sharp cutout.

BACKGROUND: Clean whiteboard or light surface taking up the left 60%. Warm lighting, slightly off-white (#F5F0EB).

WHITEBOARD CONTENT (LEFT SIDE):
- "[TITLE]" in large bold handwritten-style black text at the top
- A numbered list below: "1. [Item 1]", "2. [Item 2]", "3. [Item 3]" etc.
- A simple diagram/flowchart with boxes and arrows showing [CONCEPT]
- Small doodle-style icons next to list items

BRAND LOGO: [BRAND] logo placed top-left, medium size, clean.

DECORATIVE: Small hand-drawn style icons scattered around (brain, lightbulb, code brackets, etc.)

OVERALL: Clean, educational, organized. The numbered list creates a "value promise" — the viewer knows exactly what they'll learn. Warm, inviting, professional but approachable. High production value whiteboard aesthetic.
```

## Color Palettes by Theme

| Theme | Background | Banners/Highlights | Hero Text | Accents |
|-------|-----------|-------------------|-----------|---------|
| Tech/AI (Claude) | Dark navy #0D1117 | Orange #D4825A, Yellow #FFE033 | White, Orange | Orange glow |
| Money/Business | Dark navy/black | Green #00D26A semi-transparent | Green/Gold, White | Green glow |
| Tech/Developer | Dark blue-purple #1A0A2E | Blue #3B82F6, Cyan | White, Cyan | Blue-purple glow |
| Urgent/Drama | Dark red-black | Red #FF3333 banner | Red, Yellow, White | Red-orange glow |
| Growth/Success | Dark green-black | Green #10B981 banner | Green, White | Green accents |
| VS/Comparison | Split (color1 / color2) | Neutral dark | White, accent colors | Per-side coloring |
| Lifestyle/Brand | Dark warm #1A1412 | Orange/amber | Orange, White | Warm amber glow |

## Design Rules

### The 4-Element Rule (from YouTube analysis)
The highest-performing thumbnails have EXACTLY 4 strong elements:
1. **Subject** (close-up face with expression)
2. **Hero text** (massive, readable at 120px)
3. **Graphic element** (arrow, screenshot, icon, or logo)
4. **Color accent** (highlight band, glow, or banner)

More than 5 elements = clutter. Less than 3 = boring.

### Text Rules
- **ALL TEXT IN FRENCH** by default (unless user specifies otherwise)
- MAX 2-5 words for hero text
- ALWAYS ALL CAPS
- Hero text fills 40-60% of thumbnail width
- Always has: thick outline + shadow (3D depth optional)
- ONE keyword on a different-colored highlight/banner strip
- Must be readable at 120px wide (YouTube mobile suggestion size)
- 2 text hierarchy levels minimum (hero + subtitle)

### Subject Rules
- Ultra-sharp cutout with CLEAN edges
- CLOSE CROP — head and upper shoulders fill their area
- Strong rim lighting matching accent color
- High contrast — bright face on dark background
- Expression must convey emotion (confidence, shock, excitement)
- Subtle glow halo behind subject separates from background

### Arrow Rules (found in 40% of top performers)
- Bold, curved, white or accent-colored
- Points FROM the subject/logo TOWARD the key element
- Clean and smooth, not sketchy
- Creates visual flow guiding the eye

### Banner/Highlight Rules (from thumbstudio.fr)
- Text sits ON colored banner strips, NEVER floats on background
- Yellow (#FFE033) is the most effective highlight color
- Banner extends slightly beyond text edges
- Semi-transparent with subtle gradient
- This ONE technique separates amateur from professional

### Logo Rules
- NEVER generate logos with AI — always download official assets
- Transparent PNG or SVG format
- Add glow matching the thumbnail's accent color
- Prominent but not dominating (120-160px)
- **NEVER overlap text or subject** — place in a clear empty area (corner or margin)
- Default position: top-left corner with 45px margin, but ONLY if that area is empty
- If top-left has text/content, move to: top-right, bottom-left, or bottom-right
- Before compositing, check the thumbnail visually to find a clear spot

## Technical Specs

- **Dimensions**: 1280x720 px (16:9)
- **File size**: Under 2MB
- **Format**: PNG
- **Model**: `gemini-3-pro-image-preview` (DEFAULT — best text accuracy and prompt adherence). Fallback: `gemini-2.5-flash-image` (faster but makes spelling errors)
- **Input images**: Resize to ~400x225, quality 75 (keep under 500KB)
- **API key**: `$GEMINI_API_KEY`
- **Font fallback**: `/System/Library/Fonts/HelveticaNeue.ttc`

## Multiple Variations

ALWAYS generate 3-4 variations per request using DIFFERENT patterns:
- Variation 1: Pattern 1 or 2 — Clean big text (dark bg, massive text, arrow)
- Variation 2: Pattern 3 — Subject + screenshot + arrow
- Variation 3: Pattern 5 or 3 — Cinematic multi-element OR thumbstudio.fr style
- Variation 4: Pattern 6 — Whiteboard/educational (if topic fits)

Run API calls in PARALLEL for speed. Save all to user-specified output directory.

## Output

Save to user-specified directory or `~/Documents/thumbnail/` by default.
Naming: Use a slugified French video title proposition for each file, e.g. `claude_code_automatiser_tout.png`, `guide_complet_claude_code.png`. Each variation gets a unique title suggestion that could work as the actual YouTube video title.
Always show ALL results to user using Read tool.

## Assets

- `assets/sophiene-muscle.jpg` — Default subject photo
- `screen.png` — Reference portfolio from thumbstudio.fr (STUDY BEFORE EVERY GENERATION)
- `references/` — 15 real YouTube thumbnails from Claude Code videos with 34K-600K views:
  - `600K_claude_code_full_course.jpg` — Whiteboard educator style (HIGHEST performer)
  - `594K_claude_code_intro_setup.jpg` — Series episode with terminal + branding
  - `481K_claude_code_beginners.jpg` — Minimal: dark bg + huge text + logo
  - `306K_claude_code_explained.jpg` — Yellow highlight band + arrow + app icon
  - `259K_claude_code_full_tutorial.jpg` — Dark bg + huge text + yellow "FOR BEGINNERS" banner
  - `253K_meta_engineer_tips.jpg` — ASCII art branding + expressive gesture
  - `215K_master_95_percent.jpg` — Subject + screenshot + arrow + "Full Guide" text
  - `206K_real_engineering.jpg` — Terminal window + arrow + white banner subtitle
  - `115K_build_app_with_ai.jpg` — Light bg + phone mockup + close-up face
  - `110K_ultimate_tutorial_de.jpg` — Cinematic floating screens + laptop + yellow text
  - `59K_claude_code_beginners2.jpg` — Code background + ASCII art + banner subtitle
  - `55K_full_course_beginners.jpg` — Code background + ASCII art + series branding
  - `53K_only_tutorial_needed.jpg` — "ZERO TO HERO" + crown icon + app showcase
  - `34K_6_levels_explained.jpg` — Grid/levels comparison layout
  - `34K_absolute_beginners.jpg` — Orange bg + code screenshot + logo + subject
