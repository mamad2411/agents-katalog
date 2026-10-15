---
name: revealjs-presentation
description: >
  Generate stunning, production-quality Reveal.js presentations as single self-contained HTML files.
  Use this skill whenever the user asks to create a "Reveal.js presentation", "slide deck", "HTML presentation",
  "web-based slides", "interactive presentation", "animated slide deck", or mentions Reveal.js by name.
  Also trigger when the user wants a presentation exported as a single HTML file rather than PowerPoint.
  Do NOT use this skill for PowerPoint (.pptx) or Google Slides requests.
---

# Reveal.js Presentation Skill

Generate visually striking, self-contained Reveal.js presentations that look like they were designed by a professional — not like default conference slides.

## Output

A single `.html` file the user can open directly in any browser. No build step, no local server, no npm install. The file is fully self-contained except for CDN links (Reveal.js, Google Fonts, optionally Font Awesome).

Save the file to the user's preferred location, or to a sensible default in their working directory.

## Architecture of the HTML File

The output file follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Presentation Title]</title>

  <!-- Reveal.js core CSS from CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/reveal.min.css">
  <!-- Reveal.js theme (used as a base, heavily overridden) -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/theme/black.min.css">
  <!-- Syntax highlighting theme for code slides -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/plugin/highlight/monokai.min.css">
  <!-- Google Fonts -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=...&display=swap">

  <style>
    /* ALL custom styling goes here — this is where the magic happens */
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Slides go here -->
    </div>
  </div>

  <!-- Reveal.js core + plugins from CDN -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/reveal.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/plugin/highlight/highlight.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/plugin/notes/notes.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/plugin/zoom/zoom.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/reveal.js/5.2.1/plugin/search/search.min.js"></script>

  <script>
    Reveal.initialize({
      hash: true,
      plugins: [RevealHighlight, RevealNotes, RevealZoom, RevealSearch],
      // Additional config...
    });
  </script>
</body>
</html>
```

## Visual Design

This is what separates a great presentation from a generic one. The inline `<style>` block is the heart of the design.

### Typography

Load two complementary Google Fonts — a bold display font for headings and a clean sans-serif for body text. Good pairings:

| Heading Font      | Body Font        | Vibe               |
|-------------------|------------------|---------------------|
| Space Grotesk     | Inter            | Modern tech         |
| Playfair Display  | Source Sans 3    | Elegant editorial   |
| Outfit            | DM Sans          | Friendly startup    |
| Sora              | Plus Jakarta Sans| Clean SaaS          |
| Bebas Neue        | Work Sans        | Bold cinematic      |
| Bricolage Grotesque | Geist Sans     | Contemporary dev    |

Choose a pairing that matches the content's tone. A pitch deck wants "clean SaaS," a history talk wants "elegant editorial," a tech tutorial wants "modern tech."

Set up clear typographic hierarchy:

```css
.reveal h1 { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.8em; letter-spacing: -0.02em; }
.reveal h2 { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 2em; }
.reveal h3 { font-family: 'Space Grotesk', sans-serif; font-weight: 500; font-size: 1.4em; }
.reveal p, .reveal li { font-family: 'Inter', sans-serif; font-weight: 400; font-size: 0.95em; line-height: 1.7; }
```

### Color Themes

Default to dark themes unless the user says otherwise. Define your palette as CSS custom properties on `.reveal`:

**Dark Cinematic** (default):
```css
.reveal {
  --bg-primary: #0a0a0f;
  --bg-secondary: #12121a;
  --text-primary: #e8e8ed;
  --text-secondary: #9898a6;
  --accent: #6366f1;
  --accent-glow: rgba(99, 102, 241, 0.3);
  --highlight: #f472b6;
  --gradient-start: #1e1b4b;
  --gradient-end: #0f172a;
}
```

**Light Minimal**:
```css
.reveal {
  --bg-primary: #e7e5e4;
  --bg-secondary: #d6d3d1;
  --text-primary: #1c1917;
  --text-secondary: #44403c;
  --accent: #2563eb;
  --accent-glow: rgba(37, 99, 235, 0.15);
  --highlight: #dc2626;
  --gradient-start: #c7d2fe;
  --gradient-end: #e7e5e4;
}
```

**Vibrant Bold**:
```css
.reveal {
  --bg-primary: #0f0720;
  --bg-secondary: #1a0e35;
  --text-primary: #f8fafc;
  --text-secondary: #c4b5fd;
  --accent: #a855f7;
  --accent-glow: rgba(168, 85, 247, 0.4);
  --highlight: #facc15;
  --gradient-start: #4c1d95;
  --gradient-end: #0f0720;
}
```

**Corporate Clean**:
```css
.reveal {
  --bg-primary: #e2e8f0;
  --bg-secondary: #cbd5e1;
  --text-primary: #0f172a;
  --text-secondary: #334155;
  --accent: #0369a1;
  --accent-glow: rgba(3, 105, 161, 0.15);
  --highlight: #047857;
  --gradient-start: #bfdbfe;
  --gradient-end: #e2e8f0;
}
```

Avoid light backgrounds brighter than ~#e2e8f0 — anything closer to white is harsh on screens and tiring to look at. Light themes should feel like paper, not like staring at a lightbulb.

Then reference these variables everywhere in your CSS instead of hard-coding colors. This keeps the theme consistent and makes it easy to swap.

### Color Emphasis in Body Text

On dark backgrounds, body text tends to look like a wall of white-on-gray. Break this up by using your accent and highlight colors for key inline elements — dates, names, numbers, and important terms. This adds visual interest and makes content scannable.

```css
/* Use these classes for inline emphasis */
.accent { color: var(--accent); }
.highlight-text { color: var(--highlight); }
.date { color: var(--accent); font-weight: 600; }
```

```html
<li><span class="date">1969</span> — Apollo 11 lands on the Moon</li>
<li><span class="accent">SpaceX</span> launches its first orbital mission</li>
<li>Market size: <span class="highlight-text">$380 billion</span></li>
```

This is essential on dark themes where everything defaults to white/gray. Dates, numbers, names, and key terms should pop in the accent color — it makes the content feel designed rather than dumped onto the slide.

### Backgrounds

Reveal.js handles slide backgrounds through its own system. The correct approach is to use `data-background-color` and `data-background-gradient` attributes on `<section>` elements — this ensures the background fills the entire viewport, not just the slide content area. Setting `background` via CSS on `.reveal .slides section` creates a visible rectangle floating on a grey page, which looks broken.

```css
/* Set the overall page background to match the theme — this fills any gaps */
body {
  background: var(--bg-primary);
}
.reveal {
  background: var(--bg-primary);
}
```

Then use Reveal.js's native data attributes for per-slide backgrounds:

```html
<!-- Default dark slide -->
<section data-background-color="#0a0a0f">

<!-- Gradient for section dividers -->
<section data-background-gradient="linear-gradient(135deg, #1e1b4b, #0f172a)">

<!-- Radial glow for emphasis slides -->
<section data-background-gradient="radial-gradient(ellipse at center, rgba(99, 102, 241, 0.3), #0a0a0f 70%)">
```

Do NOT use `::before` pseudo-elements or `position: relative/absolute` on `<section>` elements for texture overlays or decorative backgrounds. These interfere with Reveal.js's vertical centering mechanism and cause content to render bottom-aligned or glitched. Rely solely on `data-background-*` attributes for all background effects.

Vary backgrounds across the deck for visual rhythm — but always use the `data-background-*` attributes, not CSS `background` on sections.

### Transitions

Use `fade` as the default and `slide` for section breaks. Do not use `zoom` or `convex` — they distort card layouts, grids, and stat elements, making them look broken during the transition animation.

```js
Reveal.initialize({
  transition: 'fade',        // default for content slides
  transitionSpeed: 'default',
  backgroundTransition: 'fade',
  // ...
});
```

Override per-slide sparingly:
- **Section dividers**: `data-transition="slide"` — gives a clear sense of moving to a new chapter
- **Everything else**: `data-transition="fade"` — keeps attention on content, not motion

The goal is subtlety. One or two transition types across the entire deck is ideal.

### Fragment Animations

Fragments reveal content progressively on click. However, they interact badly with Reveal.js's vertical centering — hidden fragments aren't counted in the layout height, so content starts off-center and shifts downward as fragments appear. Because of this, use fragments only in specific situations:

**Where fragments work well:**
- A single supplementary element below the main content — e.g., a source attribution, a callout box, or a "key takeaway" that appears after the audience has absorbed the main content
- A quote attribution appearing after the quote text

```html
<section>
  <h2>Slide Title</h2>
  <div class="accent-line"></div>
  <ul>
    <li>First point — visible immediately</li>
    <li>Second point — visible immediately</li>
    <li>Third point — visible immediately</li>
  </ul>
  <div class="glow-box fragment fade-up" style="margin-top: 1em;">
    <p>Key takeaway that appears on click</p>
  </div>
</section>
```

**Do NOT fragment:**
- Individual bullet points in a list — breaks vertical centering
- Individual cards or items in a grid layout — tedious clicking
- Multiple elements on the same slide — causes layout shift

Fragment styles to use (when appropriate):
- `fade-up` — good for a supplementary element appearing below
- `fade-in` — subtle, for secondary content

Do not use `grow` — it causes layout shifts and looks glitchy.

### Visual Elements

Use CSS to create visual richness without external images:

**Accent lines and dividers**:
```css
.accent-line {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, var(--accent), var(--highlight));
  border-radius: 2px;
  margin: 0.8em 0;
}
```

**Stat callout cards**:
```css
.stat-card {
  display: inline-block;
  padding: 1.5em 2em 1.2em;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  text-align: center;
  box-sizing: border-box;
  overflow: hidden;
}
.stat-card .number {
  font-size: 2.8em;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--highlight));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.2;
}
.stat-card .label {
  color: var(--text-secondary);
  margin-top: 0.4em;
  font-size: 0.8em;
}
```

When placing stat cards in a grid, make sure each card stays within bounds. Use `box-sizing: border-box` on all cards and grids, and keep `.number` font sizes moderate (2.5-3em) so text doesn't overflow on smaller viewports.

**Quote styling**:
```css
.styled-quote {
  position: relative;
  font-style: italic;
  font-size: 1.3em;
  padding-left: 1.5em;
  border-left: 3px solid var(--accent);
  color: var(--text-secondary);
}
```

**Glowing highlight boxes**:
```css
.glow-box {
  padding: 1.2em 1.8em;
  background: rgba(99, 102, 241, 0.08);
  border: 1px solid var(--accent);
  border-radius: 12px;
  box-shadow: 0 0 30px var(--accent-glow);
  box-sizing: border-box;
  overflow: hidden;
}
```

**Grid layouts for multi-column content**:
```css
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 2em; align-items: start; box-sizing: border-box; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1.5em; align-items: start; box-sizing: border-box; }
.grid-2 > *, .grid-3 > * { box-sizing: border-box; }
```

Content density is the #1 cause of broken slides — content that exceeds the available slide height (~900px effective) pushes everything to the bottom and breaks vertical centering. Follow these hard limits:

- **grid-3**: Use only for short content — stat cards (number + 3-5 word label), icons with a title, or single-line items. Never put paragraphs or multi-line descriptions in a 3-column grid.
- **grid-2**: Use for moderate content. **Each card/cell must contain at most 20-25 words** (a title + 1-2 short sentences). If you need more detail, move it to speaker notes or split across slides.
- **If content has more than 4 items with descriptions**: Split across multiple slides rather than cramming into one grid. Two clean slides beat one overflowing slide.
- **Cards with text content** (feature cards, team bios, era descriptions): Use grid-2, never grid-3. Each card should have at most a title + 1-2 short sentences (max 25 words in the description). Do NOT list multiple sub-items inside a single card.
- **Stat cards in grid-3**: Keep the `.number` at 2.5em max and the `.label` to 5 words or fewer.
- **Bullet lists in grid-2 cells**: Max 3 bullets, each under 10 words. If bullets need descriptions, don't put them in a grid — use a full-width list instead.

When in doubt, use fewer columns and more slides.

Never stack multiple grids vertically on one slide (e.g., two grid-2 blocks one after another). This overflows the slide height and breaks vertical centering. If you need 4+ cards, either use a single grid-2 with 2 items (and put the rest on the next slide), or use a simple bulleted list instead of cards.

### Code Slides

When the presentation involves code, configure the highlight plugin properly:

```html
<section>
  <h2>Function Example</h2>
  <pre><code class="language-python" data-trim data-noescape data-line-numbers="1-3|5-7|9-11">
def greet(name):
    """Greet someone by name."""
    message = f"Hello, {name}!"

    # Add some flair
    stars = "★" * len(name)
    decorated = f"{stars} {message} {stars}"

    # Return the result
    print(decorated)
    return decorated
  </code></pre>
  <aside class="notes">Walk through line by line: definition, decoration, output.</aside>
</section>
```

The `data-line-numbers="1-3|5-7|9-11"` attribute creates a step-through walkthrough — lines highlight in groups as you advance. This is much more engaging than showing all code at once. Always use `data-trim` to strip leading/trailing whitespace.

Match the syntax theme to your color palette:
- Dark themes → `monokai.min.css`
- Light themes → `github.min.css`

Do not use solarized themes — they have low contrast and make line-by-line highlighting nearly invisible.

Style the code container to match your slide design. For line-by-line highlighting (`data-line-numbers`), Reveal.js already dims non-active lines — do not override this with extra opacity rules, as it makes the dimmed lines unreadably dark. Instead, add a subtle background color to the highlighted lines so they stand out through color contrast, not just brightness:

```css
.reveal pre {
  background: rgba(0, 0, 0, 0.5);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  padding: 1em;
  font-size: 0.55em;
}
.reveal code {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
}

/* Add a colored background to highlighted lines so the active step is obvious */
.reveal .hljs-ln-line.highlight-line,
.reveal tr.highlight-line td {
  background: rgba(99, 102, 241, 0.15);
}
```

The key thing: when a viewer presses the right arrow to step through code, it should be immediately obvious which lines are now active. Use a colored background tint (matching your accent color at ~15% opacity) rather than aggressive dimming of inactive lines.

## Slide Structure

A well-structured deck follows a narrative arc. Here's how to think about each slide type:

### Title Slide
The first impression. Make it visually bold.

```html
<section data-background-color="#0a0a0f" data-transition="fade">
  <div style="margin-bottom: 0.5em;">
    <h1 style="font-size: 3.2em; line-height: 1.1; margin-bottom: 0.2em;">
      Presentation Title
    </h1>
    <div class="accent-line" style="margin: 0 auto;"></div>
    <p style="font-size: 1.2em; color: var(--text-secondary); margin-top: 0.8em;">
      Subtitle or tagline goes here
    </p>
  </div>
  <p style="font-size: 0.7em; color: var(--text-secondary); margin-top: 2em;">
    Presenter Name &bull; Date &bull; Context
  </p>
  <aside class="notes">Welcome the audience. Set the stage for what's coming.</aside>
</section>
```

### Section Dividers
Full-screen slides that mark transitions between topics. Use a distinct background class.

```html
<section data-background-gradient="linear-gradient(135deg, #1e1b4b, #0f172a)" data-transition="slide">
  <h2 style="font-size: 2.8em;">Chapter Title</h2>
  <p style="color: var(--text-secondary);">Brief context for this section</p>
  <aside class="notes">Transition to the next major topic.</aside>
</section>
```

### Slide Count

Unless the user specifies a slide count, aim for **10-15 slides** total (including title, section dividers, and closing). This is enough for a 10-20 minute presentation. Going beyond 20 slides usually means content is too granular — combine related points, cut less essential material, or suggest the user split into multiple presentations. More slides means more chances for layout issues and a longer, less focused deck.

### Content Slides
The core of the deck. Keep text minimal — 3-5 bullet points max, phrased as short statements, not sentences.

```html
<section>
  <h2>Slide Title</h2>
  <div class="accent-line"></div>
  <ul>
    <li>Key point one — concise and impactful</li>
    <li>Key point two — with a concrete detail</li>
    <li>Key point three — the takeaway</li>
  </ul>
  <aside class="notes">Expand on each bullet point with context and examples.</aside>
</section>
```

### Stat / Callout Slides
For impressive numbers or bold statements. Center a single striking element.

```html
<section data-background-gradient="radial-gradient(ellipse at center, rgba(99, 102, 241, 0.2), #0a0a0f 70%)">
  <div class="stat-card fragment fade-in">
    <div class="number">42%</div>
    <div class="label">Increase in user engagement</div>
  </div>
  <p class="fragment fade-up" style="margin-top: 1.5em; color: var(--text-secondary);">
    Source: Internal analytics, Q4 2025
  </p>
  <aside class="notes">This number is the hook — let it land before explaining.</aside>
</section>
```

### Quote Slides

```html
<section>
  <div class="styled-quote">
    "The best way to predict the future is to invent it."
  </div>
  <p style="margin-top: 1em; color: var(--text-secondary);">— Alan Kay</p>
  <aside class="notes">Use this quote to bridge into the next section about innovation.</aside>
</section>
```

### Closing Slide
Summarize or give a call to action.

```html
<section data-transition="fade">
  <h2>Thank You</h2>
  <div class="accent-line" style="margin: 0 auto;"></div>
  <div style="margin-top: 1.5em;">
    <p>Key takeaway or call to action</p>
    <p style="color: var(--text-secondary); font-size: 0.8em; margin-top: 1em;">
      email@example.com &bull; @handle &bull; website.com
    </p>
  </div>
  <aside class="notes">Thank the audience and invite questions.</aside>
</section>
```

### Speaker Notes

Every slide gets `<aside class="notes">` with substantive talking points — not just "discuss this slide" but actual content the presenter can use. The presenter presses **S** to open the speaker notes view.

## Reveal.js Configuration

```js
Reveal.initialize({
  hash: true,
  slideNumber: 'c/t',
  showSlideNumber: 'speaker',
  transition: 'fade',
  transitionSpeed: 'default',
  backgroundTransition: 'fade',
  center: true,
  width: 1920,
  height: 1080,
  margin: 0.08,
  plugins: [RevealHighlight, RevealNotes, RevealZoom, RevealSearch]
});
```

- `hash: true` — enables URL hash navigation so slides are linkable
- `slideNumber: 'c/t'` — shows "current/total" in speaker view
- `width/height: 1920/1080` — targets HD aspect ratio; Reveal.js scales it responsively
- `margin: 0.08` — provides comfortable padding around content

## Responsive Considerations

The 1920x1080 base resolution scales down automatically via Reveal.js. But also add a few responsive tweaks:

```css
@media (max-width: 768px) {
  .reveal h1 { font-size: 2em; }
  .reveal h2 { font-size: 1.5em; }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
  .stat-card .number { font-size: 2em; }
}
```

## Common Pitfalls

These are things that easily go wrong — check them carefully:

- **Background as grey rectangle**: If you set `background` via CSS on `.reveal .slides section`, Reveal.js shows the slide as a small rectangle on a grey page. Always use `data-background-color` or `data-background-gradient` on each `<section>` instead, and set `body` and `.reveal` backgrounds as fallback.
- **Content overflow**: Cards, stat numbers, and glow-boxes can overflow the slide area. Use `box-sizing: border-box` and `overflow: hidden` on all card-like elements. Keep stat `.number` font sizes at 2.5em max. Never put 6 feature cards in a 2x3 grid — they will overflow the bottom. Split across slides instead.
- **Columns too narrow**: A 3-column grid with paragraphs or multi-line text will truncate or overflow. Use grid-3 only for very short content (stat numbers + short labels). Use grid-2 for anything with descriptions.
- **White-on-gray monotony**: On dark themes, all text defaults to white or gray, making slides look flat and hard to scan. Use `var(--accent)` and `var(--highlight)` colors for dates, key terms, numbers, and names. Every content slide should have at least some colored text to break the monotony.
- **Zoom/convex transitions**: These distort grid layouts, cards, and multi-element slides during animation. Stick to `fade` and `slide` only.
- **`grow` fragment**: Causes layout reflow and visual glitches. Use `fade-in` or `fade-up` instead.
- **Fragments break vertical centering**: Do not fragment bullet points or grid items. Hidden fragments aren't counted in layout height, so content starts off-center and shifts as fragments appear. Only use fragments for a single supplementary element (callout box, attribution) below the main content.
- **Stacked grids break vertical centering**: Never put two grids on top of each other on one slide (e.g., two grid-2 blocks stacked vertically to show 4 cards). The combined height overflows the slide area and content won't be vertically centered. Strict rule: one grid per slide, max 2 cards in that grid. If you need 4 items, split across 2 slides.
- **Invisible code highlighting steps**: Solarized and low-contrast syntax themes make `data-line-numbers` stepping hard to see. Use monokai for dark themes and add a subtle accent-colored background tint on highlighted lines. Do NOT add extra opacity rules to dim non-highlighted lines — Reveal.js already handles dimming, and overriding it makes the code unreadable.
- **Pattern-bg / position tricks break centering**: Never use `position: relative` or `position: absolute` on `<section>` elements or pseudo-elements (`::before`, `::after`). These interfere with Reveal.js's vertical centering calculations, causing content to render at the bottom of the slide. Use only `data-background-*` attributes for backgrounds.
- **Content too tall for centering**: If slide content exceeds ~900px effective height, Reveal.js centering breaks and content gets pushed to the bottom. Grid slides with feature cards are the most common offender — each card description must be kept to 20-25 words max. When in doubt, reduce text and put detail in speaker notes.

## Checklist Before Delivering

1. Does the file open in a browser without errors? (CDN links are correct and current)
2. Do backgrounds fill the full viewport on every slide? (No grey borders or floating rectangles)
3. Are all slides visually distinct — not a wall of identical layouts?
4. Do fragments animate smoothly? (Not too fast, not too many per slide)
5. Are transitions subtle? (Only `fade` and `slide` — no `zoom` or `convex`)
6. Does every slide have meaningful speaker notes?
7. Is the typography hierarchy clear — can you tell headings from body at a glance?
8. Is the color palette consistent throughout?
9. Do all cards, stat boxes, and glow elements fit within their slide bounds? (No text cut off, no overflow past slide edges)
10. Are grids using the right column count? (grid-3 only for short stat cards, grid-2 for content with descriptions)
11. Is there color variety in body text? (Dates, names, and key terms in accent/highlight colors — not all white/gray)
12. For code slides: is the line stepping clearly visible? (Highlighted lines bright, non-highlighted lines dimmed to ~0.25 opacity)
13. Does the content follow a logical narrative arc?
14. Would you be proud to present this?
