---
name: resume-website
description: Build a stunning personal website from a resume PDF. Use this skill whenever the user wants to create a personal website, portfolio site, or online resume from a PDF resume/CV. Also trigger when the user mentions converting a resume to a website, building a portfolio from their CV, or wants a personal landing page based on their professional background.
---

# Resume Website Builder

Build a distinctive, production-grade personal website from a resume PDF. The website should reflect the user's profession, personality, and design preferences — not look like a generic template.

---

## Design Aesthetics Mandate

Before writing a single line of code, internalize this: the biggest failure mode in AI-generated websites is aesthetic convergence — every site ends up looking vaguely the same. Avoid this at all costs. Your job is to make something that feels genuinely, specifically designed for *this* person.

### Typography

Choose fonts that are beautiful, unusual, and appropriate to the person's field. The goal is a pairing that someone would notice and comment on — not a safe fallback.

**Banned fonts** (overused to the point of invisibility): Inter, Roboto, Arial, Helvetica, system-ui, -apple-system, Space Grotesk, Poppins. These are defaults, not choices.

**Distinctive Google Fonts to draw from** (pick the right ones for the profession and aesthetic — don't use all of them):

*Editorial / Expressive Serifs:*
- Cormorant Garamond — romantic, literary, fashion editorial luxury
- Playfair Display — classic print editorial, high contrast strokes
- Fraunces — quirky optical serif, surprising personality
- Instrument Serif — refined and contemporary, quiet confidence
- DM Serif Display — modern serif with punch
- Abril Fatface — ultra-high contrast, statement headlines
- Yeseva One — art deco warmth, approachable authority
- Cinzel — classical Roman gravitas

*Clean but Distinctive Sans-Serifs:*
- Syne — geometric, design-forward, contemporary
- Unbounded — bold, grid-perfect, web-native
- Plus Jakarta Sans — warm and modern, distinct from Inter
- Outfit — fresh geometric with personality
- DM Sans — clean but not sterile
- Josefin Sans — elegant geometric minimalism

*For Body Text (readable, distinctive):*
- Lora — warm serif, literary, readable at length
- Source Serif 4 — editorial trustworthiness
- Spectral — elegant digital serif
- Literata — precision-engineered for reading

*For Technical / Developer Aesthetic:*
- JetBrains Mono — developer credibility
- IBM Plex Mono — corporate-tech, structured
- Space Mono — retro-digital, character
- Fira Code — ligatures, hacker aesthetic

*For Expressive / Niche Aesthetics:*
- Exo 2 — sci-fi precision
- Orbitron — space-age (use sparingly — for the right person it's perfect)
- Rajdhani — angular, technical energy

**Pairing principle:** Pick one display/headline font and one body font. They should contrast — a high-drama serif headline with a clean sans body, or a precise monospace headline with a warm serif body. Boring pairings are pairings where both fonts feel the same weight.

### Color & Theme

Commit to a strong, cohesive palette. Timid palettes that spread color evenly feel amateur. One dominant color + one sharp accent + careful neutrals is almost always stronger than three equally-weighted colors.

**Banned color combinations** (clichéd, expected):
- Purple/violet gradients on white (the default "AI aesthetic")
- Teal + coral on white (overused startup palette)
- Generic dark mode: #1a1a1a background + white text + blue accent
- Flat pastels with no contrast or tension

**Distinctive palette archetypes to draw from** (adapt, don't copy exactly):
- Deep forest `#1a2e1a` + warm gold `#c9a84c` + cream `#f5f0e8` — organic authority
- Midnight navy `#0d1b2a` + electric cyan `#00d4ff` + white — technical precision
- Warm black `#1a1208` + amber `#f59e0b` + ivory — editorial warmth
- Charcoal `#2a2a2a` + rust `#c0392b` + off-white `#fafaf7` — bold confidence
- Deep burgundy `#3d0c02` + champagne `#e8d5b7` + ivory — academic luxury
- Near-black `#0e0e0e` + acid lime `#a8d729` + white — technical edge
- Slate `#2c3e50` + deep coral `#ff6b4a` + cream — warm modernism
- Off-white `#fafaf8` + ink `#1a1a2e` + terracotta `#c4602a` — grounded warmth
- Dark violet `#1a0533` + hot pink `#ff6b9d` + white — creative maximalism

**Actively vary between light and dark themes** across different users. Don't default to dark because it "looks more technical" — a light site with a strong editorial palette can be just as striking.

Use CSS custom properties for every color:
```css
:root {
  --color-bg: #1a2e1a;
  --color-surface: #243824;
  --color-accent: #c9a84c;
  --color-text: #f5f0e8;
  --color-muted: #8a9e8a;
}
```

### Motion

One well-orchestrated entrance sequence creates more delight than ten scattered micro-interactions. Think of the page load as a single choreographed moment.

**Effective patterns:**
```css
/* Staggered reveal on load — apply with increasing animation-delay */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.hero-name    { animation: fadeUp 0.6s ease forwards; animation-delay: 0.1s; }
.hero-title   { animation: fadeUp 0.6s ease forwards; animation-delay: 0.25s; }
.hero-tagline { animation: fadeUp 0.6s ease forwards; animation-delay: 0.4s; }
.hero-cta     { animation: fadeUp 0.6s ease forwards; animation-delay: 0.55s; }
```

- Use `opacity: 0` as default and animate to `opacity: 1` — clean, compositable
- Hover states should use `transition: all 0.2s ease` — fast enough to feel responsive
- Scroll-triggered reveals: use `IntersectionObserver` + a CSS class toggle for sections entering the viewport
- For borders, underlines, and highlights: animated `width` or `clip-path` transforms feel precise and intentional

**Avoid:** particle.js / canvas particle effects, excessive bouncing, parallax that fights the content, animations that delay content visibility for more than ~1 second total.

### Backgrounds

Solid colors are the lazy default. Every background should have at least one layer of depth or texture.

**Techniques:**
```css
/* Mesh gradient — multiple radial gradients layered */
background:
  radial-gradient(ellipse at 20% 50%, rgba(201,168,76,0.15) 0%, transparent 60%),
  radial-gradient(ellipse at 80% 20%, rgba(0,212,255,0.08) 0%, transparent 50%),
  #0d1b2a;

/* Subtle grid pattern */
background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                  linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
background-size: 48px 48px;

/* Grain texture via SVG filter */
filter: url(#grain); /* define SVG feTurbulence filter */

/* Diagonal stripe accent */
background: repeating-linear-gradient(
  -45deg,
  transparent,
  transparent 8px,
  rgba(201,168,76,0.05) 8px,
  rgba(201,168,76,0.05) 9px
);
```

Match the background technique to the overall aesthetic — a terminal-aesthetic dev site might use a subtle scanline effect; a luxury finance site might use a very faint linen texture.

---

## Workflow

### Step 1: Extract the Resume PDF

Use the following approach in order — try the script first, fall back to the MCP only if it fails.

#### Option A: uv script (preferred)

Run the extraction script using `uv`. It handles dependencies automatically with no setup beyond having `uv` installed.

```bash
uv run .claude/skills/resume-website/scripts/pdf-extract.py <path-to-resume.pdf>
```

If `uv` is not installed, instruct the user to install it first:

- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Windows (PowerShell):**
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

After installing, re-run the script command above.

#### Option B: pdf-reader MCP (fallback)

If the script fails for any reason, fall back to the pdf-reader MCP. Verify it is installed — if not, install it:

```bash
claude mcp add pdf-reader -- npx @sylphx/pdf-reader-mcp
```

After installing, **restart Claude Code** for the MCP to become available. Then use the MCP's `read_pdf` tool to extract the resume content.

### Step 2: Read and Analyze the Resume

Use the pdf-reader MCP to read the user's resume PDF. Extract and organize:

- **Name and contact info** (email, phone, location, LinkedIn, GitHub, portfolio links)
- **Professional title / headline**
- **Work experience** (companies, roles, dates, achievements)
- **Education** (degrees, institutions, dates)
- **Skills** (technical, soft, languages)
- **Projects** (if any)
- **Certifications, awards, publications** (if any)
- **Summary / objective** (if any)

### Step 3: Analyze the User's Profession

The user's job determines the website's aesthetic direction. Match the design to their professional identity — but go beyond surface-level categorization. A "software engineer" at a hedge fund has different aesthetics than one at a design agency.

| Profession Category | Aesthetic Direction | Font Starting Point | Color Direction |
|---|---|---|---|
| Software Engineer / Developer | Terminal-inspired, precise, dark-preferred | JetBrains Mono or IBM Plex Mono + clean sans | Dark bg + electric accent (cyan, green, amber) |
| Designer / Creative Director | Bold, experimental, strong typographic presence | Expressive display serif + geometric sans | High contrast, unexpected pairings |
| Data Scientist / Analyst | Structured, analytical, data-viz inspired | Precise sans + readable serif body | Deep navy/slate + sharp single accent |
| Marketing / Business | Editorial magazine feel, confident, CTA-driven | High-contrast serif headline + warm sans | Warm dominant + bold accent |
| Academic / Researcher | Scholarly, serif-heavy, intellectual minimalism | Cormorant or Spectral + Lora body | Cream/ivory + ink + one warm accent |
| Healthcare / Medical | Clean, trustworthy, calm authority | DM Sans or Plus Jakarta Sans + readable body | Calming neutral + trustworthy accent |
| Finance / Consulting | Luxury, authority, refined | Cinzel or Yeseva One + elegant body serif | Dark + gold/champagne or deep navy + silver |
| Artist / Photographer | Gallery-like, image-forward, dramatic | Abril Fatface or Syne + minimal body | Depends on their work — often near-black + one bold color |
| Product Manager | Modern, organized, metric-forward | Instrument Serif + clean sans | Confident mid-tone + crisp accent |
| Teacher / Educator | Warm, approachable, readable | Fraunces or DM Serif + warm sans body | Warm palette, higher brightness |
| Legal | Authoritative, traditional, structured | Cinzel or Playfair Display + serif body | Dark navy or charcoal + gold |
| Freelancer / Generalist | Personal brand expression — use resume details to decide | Depends on their personality | Depends on their personality |

Use this as a starting point, then adapt based on what the specific resume reveals about their personality, seniority, and industry context.

### Step 4: Ask the User's Design Preferences

Use the `AskUserQuestion` tool to gather design preferences. Ask questions in a friendly, non-technical way since users may not know design terminology.

**The key principle: each question must adapt to what the user already answered.** Don't batch all questions upfront and present pre-generated options — the choices in later questions depend on what the user chose earlier. If you ask about typography before knowing whether they want light or dark, you'll suggest the wrong fonts.

#### Round 1 — The anchor decision: vibe + tone

Ask about overall vibe and light/dark direction together, since these are the two axes that everything else branches from. Generate 3-4 aesthetic directions tailored to their profession (e.g. a software engineer sees "terminal/precision", a designer sees "editorial/expressive"). Lead with your top recommendation and explain why it suits them specifically. Include a "Surprise me" option.

Once you have their answer, **hold it as the anchor for everything that follows.**

#### Round 2 — Color + visual style (adapted to Round 1)

Now generate color palette options that actually work within the theme they chose. If they picked light, show light palettes — not "here are 5 options, 3 of which are dark". Same for visual style — show styles that are coherent with the vibe they chose. Use the Design Aesthetics Mandate's palette archetypes as a starting point and adapt them.

**Showing colors visually:** Before asking the color question, generate a temporary `color_preview.html` file and open it in the browser so the user can see real swatches. Then ask them to pick by name/number.

Generate 3–4 palette options. Each palette should have: background, surface, accent, and text colors. Write the HTML like this:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Pick your palette</title>
<style>
  body { font-family: sans-serif; padding: 32px; background: #f5f5f5; }
  .palettes { display: flex; flex-wrap: wrap; gap: 24px; }
  .palette { border-radius: 12px; overflow: hidden; width: 260px; box-shadow: 0 2px 12px rgba(0,0,0,0.12); }
  .swatch { height: 56px; display: flex; align-items: center; padding: 0 16px; font-size: 13px; font-weight: 500; }
  .label { padding: 14px 16px; background: white; }
  .label h3 { margin: 0 0 4px; font-size: 15px; }
  .label p { margin: 0; font-size: 12px; color: #666; }
</style>
</head>
<body>
<h2>Choose a color palette</h2>
<div class="palettes">
  <!-- Repeat this block for each palette option -->
  <div class="palette">
    <div class="swatch" style="background:#1a2e1a; color:#f5f0e8;">Background</div>
    <div class="swatch" style="background:#243824; color:#f5f0e8;">Surface</div>
    <div class="swatch" style="background:#c9a84c; color:#1a2e1a;">Accent</div>
    <div class="swatch" style="background:#f5f0e8; color:#1a2e1a;">Text</div>
    <div class="label">
      <h3>1. Forest &amp; Gold</h3>
      <p>Organic authority — deep green, warm gold, cream</p>
    </div>
  </div>
</div>
</body>
</html>
```

Save it as `color_preview.html` in the current directory, then run `open color_preview.html`. Tell the user: "I've opened a color preview in your browser — take a look and tell me which palette number you like."

After they pick, delete `color_preview.html` and continue with `AskUserQuestion` for the remaining visual style choices (no need to re-show colors there).

#### Round 3 — Typography + animation + background (adapted to Rounds 1–2)

Typography options should match both their field and the color/style they chose. A dark, terminal-aesthetic site should see monospace headline options; a light, editorial site should see high-contrast serifs. Animation and background texture should similarly be generated to feel at home within the choices already locked in — not pulled from a generic menu.

**Showing typography + background visually:** Generate a `design_preview.html` and open it before asking Round 3 questions. This file should show 3–4 typography pairings AND background texture options, all rendered using the palette the user already chose.

Each typography option should show:
- The headline font rendering a sample name (use the user's actual name from the resume)
- The body font rendering a short sample bio sentence
- The font pairing name and mood

Each background option should show the actual CSS technique (mesh gradient, grid lines, grain, etc.) applied as a live preview panel.

Structure the HTML like this:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Typography & Background Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<!-- Load all candidate Google Fonts here -->
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;600&family=DM+Sans:wght@400;500&family=JetBrains+Mono:wght@400;700&family=Lora&display=swap" rel="stylesheet">
<style>
  body { margin: 0; padding: 32px; background: #111; color: #eee; font-family: sans-serif; }
  h2 { margin-bottom: 8px; font-size: 16px; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.5; }
  .section { margin-bottom: 48px; }
  .options { display: flex; flex-wrap: wrap; gap: 20px; }

  /* Typography cards — use the chosen palette colors */
  .type-card {
    width: 320px; border-radius: 12px; overflow: hidden;
    padding: 28px; cursor: pointer;
    background: var(--color-surface);
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.15s;
  }
  .type-card:hover { transform: translateY(-3px); }
  .type-card .headline { font-size: 28px; margin: 0 0 8px; color: var(--color-text); }
  .type-card .body-sample { font-size: 14px; line-height: 1.6; opacity: 0.7; color: var(--color-text); }
  .type-card .meta { margin-top: 16px; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--color-accent); }

  /* Background preview panels */
  .bg-card {
    width: 320px; height: 160px; border-radius: 12px; cursor: pointer;
    display: flex; align-items: flex-end; padding: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    transition: transform 0.15s;
  }
  .bg-card:hover { transform: translateY(-3px); }
  .bg-card .bg-label {
    background: rgba(0,0,0,0.5); backdrop-filter: blur(8px);
    padding: 6px 12px; border-radius: 6px; font-size: 13px;
  }
</style>
</head>
<body>
<!-- Set palette CSS vars from the user's chosen palette -->
<style>
  :root {
    --color-bg: #0d1b2a;
    --color-surface: #1a2e42;
    --color-accent: #00d4ff;
    --color-text: #e0f0ff;
  }
  body { background: var(--color-bg); }
</style>

<div class="section">
  <h2>Typography Pairings</h2>
  <div class="options">
    <div class="type-card">
      <div class="headline" style="font-family:'Cormorant Garamond',serif; font-weight:600;">Alex Johnson</div>
      <div class="body-sample" style="font-family:'DM Sans',sans-serif;">Senior software engineer with 8 years building distributed systems at scale.</div>
      <div class="meta">1. Cormorant + DM Sans — editorial contrast</div>
    </div>
    <!-- Add more type-card blocks for each pairing option -->
  </div>
</div>

<div class="section">
  <h2>Background Textures</h2>
  <div class="options">
    <div class="bg-card" style="background: radial-gradient(ellipse at 20% 50%, rgba(0,212,255,0.15) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(0,100,200,0.1) 0%, transparent 50%), var(--color-bg);">
      <div class="bg-label">1. Mesh gradient</div>
    </div>
    <!-- Add more bg-card blocks for each texture option -->
  </div>
</div>

</body>
</html>
```

Save as `design_preview.html`, run `open design_preview.html`, and tell the user: "Here's a preview of font and background options — all shown in your chosen colors. Let me know which typography number and background number you like."

After they pick, delete `design_preview.html` and use `AskUserQuestion` only for animation level (which can't be previewed statically).

#### Round 4 — Content layout + assets + special features

Ask about single vs. multi-page (informed by their resume length), what media assets they have, and which special features they want. **Explicitly prompt them to drop any photos, project screenshots, or videos into the repo now**, before building — e.g., "If you have a profile photo or any project screenshots, drag them into the repo and let me know the filenames."

Curate special features that are relevant to their profession. A developer might see "GitHub contribution graph widget" and "live project demo embeds"; a consultant might see "client logo carousel" and "case study cards". Always include basics like "downloadable PDF resume" and "contact section".

**Required coverage checklist — confirm all are answered before moving to Step 5:**
- [ ] Overall vibe
- [ ] Light vs. dark (or specific tone)
- [ ] Color palette
- [ ] Visual style
- [ ] Typography feel
- [ ] Animation & interaction level
- [ ] Background & texture
- [ ] Content layout
- [ ] Photos/media (and prompt to provide files)
- [ ] Special features

#### After all rounds: coherence check

Before moving to Step 5, review all the choices together as a set. Ask yourself: do these work as a unified design language? Common incompatibilities to watch for:

- Light background chosen, but color palette is dark-dominant → adjust palette to light variant
- Minimalist visual style chosen, but heavy animation level chosen → flag the tension and either ask the user or default to subtle motion
- "Surprise me" on vibe but very specific color constraints → make sure the surprise stays within their color constraint
- Bold/expressive typography chosen but "clean and simple" visual style → reconcile toward one direction

If you spot a conflict, **resolve it before building** — either by making a sensible judgment call (and telling the user what you decided), or by asking a quick follow-up question. Don't silently apply incompatible choices and hope it works out.

### Step 5: Generate the Design System

Based on the user's profession and their answers from Step 4, define a concrete design system before writing any HTML. This prevents design decisions from drifting mid-build.

Write out (internally — you don't need to show this to the user):

```
Typography:
  - Headline font: [specific font name] — [why it fits]
  - Body font: [specific font name] — [why it fits]
  - Accent font (if any): [specific font name or "none"]

Palette:
  --color-bg: [hex]
  --color-surface: [hex]
  --color-accent: [hex]
  --color-accent-2: [hex if needed]
  --color-text: [hex]
  --color-muted: [hex]

Background treatment: [technique from Design Aesthetics Mandate]
Animation approach: [one entrance sequence + hover states, or more — describe]
Layout type: [single page / multi-page]
```

This design system must be genuinely derived from the user's profession and stated preferences — not a safe default. If you find yourself writing "Inter" or "#6366f1" here, stop and reconsider.

### Step 6: Build the Website

Create the static HTML website in the current working directory.

**Technical Requirements:**
- Pure static HTML + CSS + JS (no build tools, no frameworks)
- All styles inline or in `<style>` tags (single file preferred, but can split into multiple pages)
- Use Google Fonts via CDN link for typography
- Use SVG icons (Heroicons, Lucide, or custom) — NEVER use emojis as icons
- Responsive design — must look great on mobile, tablet, and desktop
- Accessible — proper semantic HTML, alt text, contrast ratios, keyboard navigation

**Content Mapping from Resume:**
- Hero section with name, title, and a compelling one-liner
- About section with professional summary
- Experience section with timeline or cards — if displaying company logos, use the `logo-search` skill to fetch them via logo.dev CDN (e.g. `<img src="https://img.logo.dev/stripe.com?token=pk_...">`)
- Skills section with visual representation (bars, tags, or grouped categories)
- Education section — same as above, use `logo-search` for university/institution logos if desired
- Projects section (if applicable)
- Contact section with links and optional form
- Footer with social links

**Logo integration:** If the user's resume includes companies, clients, or institutions and their design calls for visual logos (e.g. a client logo carousel, company timeline with logos), invoke the `logo-search` skill. It supports both direct domain lookup and brand name search, and returns a ready-to-use CDN image URL. The `pk_` publishable key goes in the `.env` file.

**Design Execution:**
Apply the design system from Step 5. Then go further:

- **Typography in code:** Load the exact Google Fonts you specified. Set `font-family` explicitly at each level — don't let anything fall back to system fonts.
- **Background:** Implement the background technique from the Design Aesthetics Mandate, not a solid color.
- **Color:** Use CSS custom properties for every color. Apply the dominant color boldly — it should feel *committed to*, not timid.
- **Animation:** Implement one choreographed entrance sequence using staggered `animation-delay`. Add `IntersectionObserver` for scroll-triggered section reveals. Keep hover states fast (`0.2s`).
- **Layout:** Use CSS Grid for major layout structure. Avoid cookie-cutter card grids — think about what layout *this person's content* actually calls for.

**File Structure:**
- Save the main file as `index.html` in the current directory
- If multi-page: create additional HTML files (e.g., `about.html`, `projects.html`)
- If user provides assets: save them in an `assets/` subdirectory
- Add a `style.css` only if styles are too large for inline

### Step 7: Review and Iterate

After building, tell the user:
- What you built and the design decisions you made
- How to view it (open `index.html` in a browser)
- Ask if they want any changes — colors, layout, content, animations, etc.

Be ready to iterate based on feedback.
