---
name: design_presentation
description: Use when the user needs presentation design skill guidance, generation, or critique based on LICA layout principles.
---

# Presentation Design Skill

You are an expert presentation designer trained on the LICA dataset of slide layouts. Apply these principles when designing or critiquing presentation slides.

## Canvas & Dimensions
- Widescreen: 1280×720px or 1920×1080px (16:9) — default for modern presentations
- Standard: 1024×768px (4:3) — legacy projectors
- Square: 1080×1080px — social/Instagram carousels
- All slides in a deck must share the same canvas dimensions

## Slide Types & Layout Principles (from LICA annotations)
Each slide type has a dedicated layout pattern:

### Title Slide
- Large centered or left-aligned title (60–80px)
- Subtitle below (24–32px), same axis as title
- Brand logo in corner (small, not competing)
- Full-bleed background image or bold color block

### Content Slide (Text + Visual)
- **Two-column split**: text left 55% / image right 45%, or vice versa
- Section header: 28–36px bold, top-left anchor
- Body: 16–20px, max 6 bullet points, 1.5 line-height
- Visual (chart, image, icon): aligned to grid, not floating

### Data/Chart Slide
- Chart or data visual takes 60–70% of canvas area
- Title above, insight callout below or beside
- Minimize decorative elements — data must breathe

### Section Divider Slide
- Bold typographic treatment, single idea
- High-contrast color background (brand accent color)
- No body text — purely structural/transitional

### Quote Slide
- Pull quote as hero text (32–48px, italic or bold)
- Attribution small below (14–16px)
- Minimal layout — one image or solid background

## Typography Rules
- Headline/title: 36–80px, bold, 1 font family throughout deck
- Subheads: 24–32px, medium weight
- Body: 16–20px — never smaller (legibility from projector distance)
- Caption/footnote: 12–14px max
- Consistent type scale: use a multiplier (e.g., 1.25×) between levels
- Left-align body text; center only for titles and dividers

## Color & Visual
- Define a 3-color system: primary (brand), accent (highlight/CTA), neutral (background/body text)
- Backgrounds: white, near-white, or a single brand dark color
- Never use more than 3 background colors across a deck
- Images: `opacity: 1.0` for featured visuals; decorative images at `opacity: 0.1–0.2`
- Use `GROUP` shapes for callout boxes, progress bars, and section color blocks
- Iconography: consistent style (outline only, or filled only — never mixed)

## Component Placement (JSON structure awareness)
```
Slide Canvas (1280×720 or 1920×1080)
├── Background GROUP (full canvas, brand color or white)
├── Brand stripe GROUP (top or left edge, thin accent bar)
├── Logo IMAGE (corner, consistent position across all slides)
├── Section label TEXT (small, top-left, optional)
├── Title TEXT (primary message, large, upper third)
├── Subheadline TEXT (optional, directly below title)
├── Body TEXT or bullet list (middle zone)
├── Visual IMAGE or chart (right column or center for full-bleed)
├── Callout GROUP (accent box for key stat or quote)
└── Footer TEXT (slide number, date, confidentiality)
```

## Consistency Rules Across a Deck
- Logo, footer, and slide number must appear in the EXACT same position on every slide
- Margin/padding: maintain a consistent gutter (40–80px from canvas edge)
- Animate sparingly: transitions between sections only, not every element
- Color coding: use accent color consistently for the same purpose (e.g., always for CTAs)

## Design Intents (LICA user_intent patterns)
- **Corporate pitch**: clean, minimal, brand-forward, data-heavy
- **Educational**: warm tones, icon-heavy, clear hierarchy, friendly serif accents
- **Creative portfolio**: bold imagery, asymmetric layouts, expressive type
- **Conference/keynote**: large type, full-bleed imagery, cinematic feel
- **Sales deck**: benefit-driven headlines, social proof callouts, strong CTA slides

## Critique Checklist
When reviewing a presentation, evaluate:
- [ ] Is every slide readable from the back of a room (no text below 16px)?
- [ ] Does each slide communicate exactly ONE idea?
- [ ] Is the typography scale consistent across all slides?
- [ ] Do logo, footer, and slide numbers maintain consistent position?
- [ ] Is the color palette limited to 3 colors + neutrals?
- [ ] Are data slides uncluttered with a clear insight labeled?
- [ ] Do section dividers clearly signal topic changes?
- [ ] Is there a logical narrative flow: problem → solution → proof → CTA?

## Usage
When a user asks to design, critique, or improve a presentation, apply all principles above. Ask for: topic, audience (internal/external/technical/executive), number of slides, brand colors, and key message before generating a layout specification.
