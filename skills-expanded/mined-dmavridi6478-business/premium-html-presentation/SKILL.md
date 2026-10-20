---
name: premium-html-presentation
description: >
  Create premium, cinematic, dark-mode HTML presentation decks with atmospheric lighting, smooth
  animations, and a professional monochromatic + accent color system. Use this skill whenever the
  user asks to build an HTML presentation, slide deck, pitch deck, or multi-slide web-based
  presentation — especially when they want it to look polished, premium, or "Apple-style." Also
  trigger when the user mentions "presentation deck," "HTML slides," "slide deck," "dark mode
  presentation," "cinematic presentation," "animated slides," "web presentation," "reveal.js-style,"
  "pitch deck," "executive presentation," or asks for slides with smooth transitions and visual
  storytelling. Use even if the user only says "make me a deck" or "create slides for X topic" —
  this skill defines the full design system to follow.
---

# Premium HTML Presentation – Design System Skill

A complete design system for building **cinematic, dark-mode HTML presentation decks** with atmospheric depth, smooth transitions, and professional visual hierarchy. This is the standard to follow whenever producing any HTML-based slide presentation.

---

## Core Design Principles

### 1. Atmospheric Lighting (Soft-Focus Aesthetic)
- **Background base:** Deep charcoal `#0f0f0f` — never pure black, never gray.
- **Depth layer:** Each slide uses a `radial-gradient` ambient glow positioned behind the primary content container. This creates a "floating content" illusion reminiscent of premium Apple and Linear product pages.
- **Rule:** The glow must be subtle. Opacity range: `0.08–0.18`. It adds depth, not distraction.

```css
/* Example ambient glow for a slide */
background: radial-gradient(ellipse 80% 60% at 50% 40%, rgba(99, 102, 241, 0.12) 0%, transparent 70%);
```

### 2. Color Palette — Monochromatic + One Accent
Use **neutral grays and whites** for all body text and supporting elements. Reserve the single accent color exclusively for:
- Call-to-action elements
- Highlighted data points or focal statistics
- Active progress indicators
- Key underlines or border accents on section headers

**Default accent options (pick one per deck, never mix):**
| Name | Hex | Use Case |
|---|---|---|
| Electric Indigo | `#6366f1` | Technology, strategy, innovation |
| Soft Amber | `#f59e0b` | Healthcare, warmth, commercial |
| Emerald | `#10b981` | Sustainability, growth, ESG |
| Sky Blue | `#38bdf8` | Data, analytics, clinical |

**Typography colors:**
- Primary headings: `#ffffff`
- Subheadings: `#e5e7eb`
- Body / supporting text: `#9ca3af`
- Captions / metadata: `#6b7280`

### 3. Typographic Hierarchy
- **Font family:** `Inter` (Google Fonts) as primary. Fallback: `system-ui, -apple-system, sans-serif`.
- **Heading scale:**
  - H1 (Title slide): `clamp(2.5rem, 5vw, 4rem)`, `font-weight: 700`, `letter-spacing: -0.03em`, `line-height: 1.1`
  - H2 (Section header): `clamp(1.8rem, 3.5vw, 2.8rem)`, `font-weight: 600`, `letter-spacing: -0.02em`
  - H3 (Sub-header): `1.25rem`, `font-weight: 500`
- **Body text:** `1rem–1.125rem`, `line-height: 1.75`, `font-weight: 400`
- **Never use more than 3 font sizes per slide.**

### 4. Flow & Motion
All slide transitions and element entrances use:
```css
transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
```

**Stagger pattern for element entrance** (elements appear sequentially, not all at once):
```css
.slide-element:nth-child(1) { animation-delay: 0.1s; }
.slide-element:nth-child(2) { animation-delay: 0.25s; }
.slide-element:nth-child(3) { animation-delay: 0.4s; }
```

**Entrance animation standard:**
```css
@keyframes fadeSlideIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

---

## Technical Architecture

### Slide Structure
Each deck is a **single self-contained HTML file**. No external dependencies except Google Fonts (via `<link>`).

```
index.html
├── <head>          → Google Fonts import, CSS variables, base styles
├── <style>         → All CSS inline or in <style> block
├── .deck-wrapper   → Full viewport container, overflow hidden
│   ├── .slide      → Each slide: position absolute, full viewport
│   │   ├── .slide-bg     → Radial gradient ambient layer (z-index: 0)
│   │   ├── .slide-content → Primary content container (z-index: 1)
│   │   └── .slide-*      → Content elements (text, stats, lists, etc.)
│   └── .progress-bar     → Thin top-line progress indicator
└── <script>        → Navigation logic only (keyboard + click)
```

### CSS Variables (Define Once, Use Everywhere)
```css
:root {
  --bg-base:       #0f0f0f;
  --bg-surface:    #1a1a1a;
  --accent:        #6366f1;        /* Swap this for different decks */
  --accent-muted:  rgba(99, 102, 241, 0.15);
  --text-primary:  #ffffff;
  --text-secondary:#9ca3af;
  --text-muted:    #6b7280;
  --border:        rgba(255,255,255,0.08);
  --radius:        12px;
  --transition:    0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Progress Indicator
A **thin horizontal top-line** that fills as slides progress. Never use bulky dots or visible step counters — minimal and discrete only:
```css
.progress-bar {
  position: fixed;
  top: 0; left: 0;
  height: 2px;
  background: var(--accent);
  transition: width var(--transition);
  z-index: 100;
}
```

### Navigation Logic
Support both keyboard (← →, Space, PageUp/Down) and click-based navigation. Include touch swipe support for mobile:
```javascript
// Minimal navigation — keyboard + optional click zones
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ')  nextSlide();
  if (e.key === 'ArrowLeft')                     prevSlide();
});
```

---

## Slide Layout Templates

### Template A — Title Slide
**Purpose:** Opening or section divider  
**Layout:** Centered, minimal — logo or brand mark optional top-left, large title center, subtitle below, CTA or date bottom-right.

### Template B — Headline + Body
**Purpose:** Key message slides  
**Layout:** Large left-aligned H2, body text right or below, optional accent stat or pull quote in a bordered card.

### Template C — Data/Stats Slide
**Purpose:** Metrics, KPIs, benchmark data  
**Layout:** 2–3 large stat numbers with labels, separated by subtle vertical dividers. Use accent color exclusively on the key metric.

### Template D — Comparison / Two-Column
**Purpose:** Competitive comparison, before/after, pros/cons  
**Layout:** Two equal columns with a vertical divider. Accent color marks the "winner" or preferred column.

### Template E — Closing / CTA Slide
**Purpose:** Summary, call to action, contact  
**Layout:** Centered, sparse. One bold closing statement, one accent-colored CTA button or highlighted element.

---

## Content Placeholders (Modular Pattern)

When generating the deck, wrap all user-editable content in clearly labeled placeholder comments:

```html
<!-- SLIDE 1: TITLE -->
<!-- [EDIT] Deck title -->
<h1 class="slide-title">Your Title Here</h1>
<!-- [EDIT] Subtitle or tagline -->
<p class="slide-subtitle">Supporting context or date</p>
```

This ensures the user can find and replace content without touching the design logic.

---

## Accessibility & Readability Rules

- Minimum contrast ratio: **4.5:1** for body text (WCAG AA).
- Never place text directly over a complex gradient without a semi-transparent overlay.
- Font size floor: `0.875rem` (14px) for any visible text element.
- Line length: max `65ch` for body paragraphs — never full-width text on wide slides.

---

## Quality Checklist Before Delivering Any Deck

Before presenting the final HTML to the user, mentally verify:

- [ ] Single accent color used consistently — not mixed with other colors
- [ ] All slides use `#0f0f0f` base background
- [ ] Ambient radial gradient present but opacity ≤ 0.18
- [ ] Entrance animations staggered, not simultaneous
- [ ] Progress bar functional and minimal
- [ ] All content wrapped in `<!-- [EDIT] -->` placeholder comments
- [ ] CSS variables defined in `:root` — no hardcoded hex values in component styles
- [ ] Font is Inter (loaded from Google Fonts or system fallback)
- [ ] Responsive: deck readable on both 1920×1080 and 1366×768 viewports
- [ ] Navigation works via keyboard arrow keys

---

## Common Mistakes to Avoid

| Mistake | Why It Fails | Correct Approach |
|---|---|---|
| Using multiple accent colors | Destroys visual hierarchy | One accent, used sparingly |
| Full-brightness gradient backgrounds | Creates visual noise, fatigues audience | Opacity ≤ 0.18 on all glows |
| All elements animating simultaneously | Overwhelms the viewer | Stagger delays: 0.1s, 0.25s, 0.4s |
| Hardcoding hex values in components | Makes theming painful | Always use CSS variables |
| Oversized body text blocks | Slides ≠ documents | Max 3–5 lines per text block |
| Missing placeholder comments | User can't edit content | Every editable string gets `[EDIT]` tag |

---

## Accent Color Selection Guide for MedTech / Healthcare Context

Given the primary use context (MedTech, cardiology, clinical sales enablement):

| Deck Purpose | Recommended Accent | Rationale |
|---|---|---|
| Competitive intelligence / CI report | `#6366f1` Electric Indigo | Strategic, analytical, premium |
| Clinical / surgical training | `#38bdf8` Sky Blue | Clean, clinical, trustworthy |
| Commercial / sales enablement | `#f59e0b` Soft Amber | Warm, persuasive, human |
| ESG / sustainability | `#10b981` Emerald | Growth-oriented, responsible |
| Executive / C-suite briefing | `#6366f1` Electric Indigo | Authority, precision |

## Related skills in this repo

- **sales-enablement**: Source content (positioning, objections, ROI narrative) for a pitch deck built with this skill.
- **business-intelligence-report** / **ceo-reporting-skill** / **quarterly-okr-architect**: Good content sources for an executive-briefing deck in this style.
- **the-design-system-prompt**: Overlapping cinematic-HTML-deck skill — prefer this one (it's the more complete, MedTech-tuned version with a full QA checklist); use `the-design-system-prompt` only if its specific prompt framing is explicitly requested.
- **theme-factory**: Pull a ready-made visual theme instead of picking colors manually.
- **pptx**: Use instead when the deliverable must be an actual editable `.pptx` file rather than an HTML/web deck.
