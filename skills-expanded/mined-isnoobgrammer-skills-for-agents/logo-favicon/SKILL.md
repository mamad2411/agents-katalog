---
name: logo-favicon
description: >
  Find, generate, or create logos, favicons, and SVGs for any project. Cascading
  strategy: search the web for existing assets first, scrape free logo sites, generate
  SVGs programmatically with Python, and only use AI image generation as a last resort.
  Triggers on: "logo", "favicon", "icon", "brand kit", "SVG", "app icon", "og image",
  "make me a logo", "need a favicon", "brand identity", "project icon", "website icon".
  Even triggers when the user mentions "new project" or "deploying" — every project needs a logo.
domain: craft
composable: true
yields_to: [process]
---

# Logo & Favicon Hunter

> Every project deserves a face. This skill finds or builds one — by any means necessary.

You are a logo/favicon acquisition engine. You don't ask the user what style they want
until you've already exhausted every free resource on the internet. You are aggressive,
resourceful, and you never stop at the first result.

---

## The Cascading Strategy (MANDATORY ORDER)

Execute these levels sequentially. Each level MUST be attempted before moving to the next.
Report results at each level. The user decides when to stop.

```
Level 1: WEB SCAVENGE     → Search for existing logos/icons for the project
Level 2: FREE TOOLS        → Use favicon.io, IconForge, RealFaviconGenerator
Level 3: PROGRAMMATIC SVG  → Generate SVG with Python (svgwrite + Pillow)
Level 4: BRAND KIT EXPORT  → Convert to all formats (ICO, PNG, WebP, OG)
Level 5: AI GENERATION     → Last resort: ChatGPT/Gemini prompts or image_generate
```

**The philosophy:** AI generation is the LAST resort, not the first. A well-chosen
existing icon beats a generic AI-generated one every time. Search first, generate last.

---

## Level 1: Web Scavenge

Before creating anything, search for what already exists. Run these searches:

1. **Project name + "logo"** — does the project already have branding somewhere?
2. **Project name + "icon" OR "favicon"** — maybe someone already made one
3. **Project topic/niche + "free icon" OR "free logo"** — related assets
4. **Search icon libraries**: Flaticon, Icons8, The Noun Project, Font Awesome
5. **Search SVG repos**: SVG Repo, OpenMoji, Twemoji (for emoji-based logos)

Use `scripts/logo_hunter.py` to automate this search:

```bash
python scripts/logo_hunter.py --name "ProjectName" --topic "description" --output ./brand/
```

The script searches multiple sources and downloads candidate logos/icons.

---

## Level 2: Free Online Tools

If Level 1 finds nothing satisfactory, use these free tools (in order of preference):

### Text-Based Logo (fastest)
1. **favicon.io** — https://favicon.io
   - Input: text initials + background color + font
   - Output: favicon.ico, apple-touch-icon.png, android-chrome-512x512.png
   - Use the browser to generate, or use the API endpoint:
     `https://favicon.io/favicon-generator/?text=AB&background_color=000000&font_color=ffffff&font=segoe-ui-bold`

2. **Logomaker** — https://logomaker.lol
   - Input: text + font + effects
   - Output: PNG, SVG, animated frames
   - Zero dependencies, client-side

3. **IconForge** — https://www.iconforge.dev
   - 8 free tools: favicon generator, SVG optimizer, app icon maker, logo designer
   - All browser-based, no upload needed

### Image-Based Logo
4. **RealFaviconGenerator** — https://realfavicongenerator.net
   - Upload a source image (260x260+ or SVG)
   - Generates ALL sizes for ALL platforms
   - Has developer API: https://realfavicongenerator.net/developers

5. **FaviconGenerator.io** — https://favicongenerator.io
   - SVG → ICO + PNG + Apple Touch + PWA icons
   - Dark mode support

6. **Snappicon** — https://www.snappicon.com
   - One logo upload → favicons, Apple Touch, PWA, OG images, HTML snippets

### Monogram/Initial Logo
7. **Logogram.io** — https://www.logogram.io
   - AI monogram generator with SVG/PNG export + built-in SVG editor

8. **Zawa Monogram** — https://zawa.ai/monogram-maker
   - Free 3-initial monogram creator

9. **Icons8 Monogram** — https://icons8.com/make/3-initial-monogram-generator-free
   - Three-letter monogram with various styles

---

## Level 3: Programmatic SVG Generation

If no existing logo works, generate one with Python. Use `scripts/svg_generator.py`:

```bash
python scripts/svg_generator.py --name "ProjectName" --style modern --output ./brand/logo.svg
```

### Styles Available
- **modern** — clean geometric, sans-serif, minimal
- **tech** — dark background, neon accent, monospace feel
- **playful** — rounded shapes, bright colors, friendly
- **elegant** — serif font, thin lines, sophisticated
- **monogram** — initials in a circle/shield/hexagon
- **icon** — simple geometric symbol (no text)

### How It Works
1. Generates SVG using `svgwrite` (pure Python, no dependencies)
2. Creates multiple variants: full logo, icon only, wordmark only
3. Exports light/dark/mono versions
4. Converts to PNG using Pillow (multiple sizes)
5. Generates favicon.ico from the PNG set

### The SVG Generator Creates
```
brand/
├── logo-full-light.svg
├── logo-full-dark.svg
├── icon-light.svg
├── icon-dark.svg
├── icon-mono-black.svg
├── icon-mono-white.svg
├── favicon.ico
├── favicon-16.png
├── favicon-32.png
├── favicon-48.png
├── favicon-96.png
├── apple-touch-icon.png (180x180)
├── android-chrome-192.png
├── android-chrome-512.png
├── og-image.png (1200x630)
└── BRAND.md
```

---

## Level 4: Brand Kit Export

After obtaining a logo (from any level), generate the full brand kit:

```bash
python scripts/favicon_generator.py --input ./brand/logo-full-light.svg --output ./brand/
```

This converts any SVG/PNG into:
- All favicon sizes (16, 32, 48, 96, 180, 192, 512)
- ICO file (multi-size)
- Apple Touch Icon
- Android Chrome icons
- PWA manifest icons
- OG image (1200x630 with padding)
- WebP optimized versions

---

## Level 5: AI Generation (LAST RESORT)

Only proceed here if Levels 1-4 produced nothing satisfactory.

### Option A: Generate with image_generate tool
Use the built-in `image_generate` tool with a crafted prompt:

```
image_generate(
  prompt="[project name] logo, [style] design, clean vector style,
          minimalist, suitable for favicon and app icon, white background,
          centered composition, professional branding",
  aspect_ratio="square"
)
```

Then run Level 4 on the output to get all formats.

### Option B: Give the user prompts for ChatGPT/Gemini

See `references/ai-prompts.md` for ready-to-use prompts optimized for:
- ChatGPT (DALL-E 3) — best for detailed, realistic logos
- Gemini (Imagen) — best for clean, simple icons
- Midjourney — best for artistic, unique designs

Present these prompts to the user so they can generate in their preferred tool.

### Option C: LogoLoom MCP Server
If the user has Node.js 18+, suggest LogoLoom:

```bash
npx @mcpware/logoloom
```

This is an MCP server that:
- Reads your codebase to understand the brand
- Generates clean SVG code (not auto-traced paths)
- Exports 31-file brand kit automatically
- Zero cost, runs locally

---

## The Output: Brand Kit Structure

Every investigation ends with this structure:

```
brand/
├── LOGO.md                    # Manifest: source, license, generation method
├── logo-full-light.svg        # Primary logo (light bg)
├── logo-full-dark.svg         # Dark mode variant
├── icon-only.svg              # Icon without text
├── icon-mono.svg              # Single color version
├── favicon.ico                # Multi-size ICO
├── favicon-{16,32,48,96}.png  # Individual favicon sizes
├── apple-touch-icon.png       # 180x180
├── android-chrome-{192,512}.png
├── og-image.png               # 1200x630
├── twitter-card.png           # 1200x600
└── BRAND.md                   # Colors, typography, usage guidelines
```

---

## Decision Tree

```
START
  │
  ├─ Does the project already have a logo somewhere?
  │   YES → Download it → Level 4 (brand kit) → DONE
  │   NO ↓
  │
  ├─ Can we find a suitable free icon/logo online?
  │   YES → Download + customize → Level 4 → DONE
  │   NO ↓
  │
  ├─ Can we generate a text-based logo? (initials, name)
  │   YES → favicon.io or svg_generator.py → Level 4 → DONE
  │   NO ↓
  │
  ├─ Can we generate a geometric SVG logo?
  │   YES → svg_generator.py → Level 4 → DONE
  │   NO ↓
  │
  ├─ Does the user have a source image to convert?
  │   YES → RealFaviconGenerator or favicon_generator.py → DONE
  │   NO ↓
  │
  └─ AI GENERATION (last resort)
      ├─ image_generate tool → Level 4 → DONE
      ├─ ChatGPT/Gemini prompts → user generates → Level 4 → DONE
      └─ LogoLoom MCP → DONE
```

---

## Quick Start Examples

### "I need a favicon for my project called NightOwl"
1. Search: "NightOwl logo" "NightOwl icon" "owl favicon free"
2. Check Flaticon, Icons8 for owl icons
3. If nothing: `python scripts/svg_generator.py --name "NightOwl" --style modern --symbol owl`
4. Generate brand kit: `python scripts/favicon_generator.py --input brand/icon-light.svg --output brand/`

### "Make me a logo for my GitHub repo"
1. Search the repo for existing assets (README images, docs/, assets/)
2. Check if the org/user has existing branding
3. Generate monogram from initials
4. Export brand kit including GitHub preview (1280x640)

### "I need a complete brand identity"
1. Scavenge web for the project name
2. Generate SVG logo with svg_generator.py
3. Export full brand kit
4. Provide AI prompts for refinement if needed
5. Generate BRAND.md with color codes and usage guidelines

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/logo_hunter.py` | Search web for existing logos/icons | `--name "X" --topic "Y"` |
| `scripts/svg_generator.py` | Generate SVG logos programmatically | `--name "X" --style modern` |
| `scripts/favicon_generator.py` | Convert any image to full favicon set | `--input logo.svg --output brand/` |

---

## Boundaries

- Does NOT hire designers or manage design contracts
- Does NOT guarantee uniqueness — advise user to check trademark databases
- Does NOT create photorealistic logos (use AI image tools for that)
- DOES produce clean, scalable SVG as primary output
- DOES work offline for Levels 3-4 (no API needed)
- DOES respect copyright — always check licenses on downloaded assets

---

## Composability — Working With Other Skills

> **See `PROTOCOL.md` (SIP) at skills root for full interop contract.**

### Domain Declaration

```yaml
domain: craft
composable: true
yields_to: [process]
```

Logo-favicon owns **craft** — visual identity assets for projects.

### When Logo-Favicon Leads

- Any request for a logo, favicon, icon, or brand kit
- When a new project is created and needs visual identity
- When deploying a website/app and need favicon set

### When Logo-Favicon Defers

| Other Skill's Domain | What Logo-Favicon Does |
|---------------------|------------------------|
| **Process** (e.g. planner) | Logo-favicon generates assets on demand. Process decides when in the workflow to create them. |
| **Content** (e.g. blogger) | Logo-favicon provides the visual assets. Content handles where they appear. |

### Conflict Signal

> `⚠️ Craft conflict: logo-favicon generates visual assets, but another skill wants to control visual style. Logo-favicon defers to process for timing, but owns the asset generation itself.`
