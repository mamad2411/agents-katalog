---
name: taste-style-art-deco
description: Apply Art Deco design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses art-deco or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as taste-engine instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Art Deco

**ID:** `art-deco`  
**Signature:** Architectural geometric precision, stepped chevron forms, elegant symmetry, refined typography, and disciplined ornamentation.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. Art Deco is an architectural visual language, not a luxury color preset or a generic gold-and-black gradient template.

## Native expressions (variants)

Art Deco provides three distinctive expressions sharing the same foundation of geometric discipline, architectural framing, and intentional symmetry:

```yaml
style:
  id: art-deco
  name: Art Deco
  category: visual-style
  default_variant: modern
  variants:
    modern:
      identity: modern-deco
      focus: contemporary-architectural-whitespace
    classic:
      identity: classic-deco
      focus: rich-dramatic-symmetry-gold
    minimal:
      identity: minimal-deco
      focus: quiet-sophistication-bronze-burgundy
```

### 1. Modern Deco (`variant: modern`, Default)

Visual personality:
- **Contemporary, refined, architectural:** Generous intentional whitespace paired with rigorous geometric grid discipline.
- **Simplified geometric motifs:** Architectural line frames, subtle chevron separators, and restrained stepped corner accents.
- **Editorial typography:** Refined display headings paired with high-clarity functional sans for data and forms.
- **Balanced palette:** Forest Green (`#24453D`), Muted Brass (`#B69A68`), Warm Cream (`#F5F0E6`), Charcoal (`#292B29`).
- **Applications:** Creative agencies, editorial websites, premium SaaS, architecture studios, professional services, and modern portfolios.

### 2. Classic Deco (`variant: classic`)

Visual personality:
- **Rich, dramatic, sophisticated:** Unapologetic architectural drama inspired by 1920s–1930s monuments (Chrysler Building, Palais de Chaillot).
- **Strong symmetrical compositions:** Stepped ornamental borders, layered double-line framing, and prominent geometric medallions.
- **High-contrast typography:** Monumental decorative serif display headers with generous letter spacing, paired with warm ivory surfaces.
- **Restrained metallic finishes:** Flat and subtly layered Antique Gold finishes (`#B89B5E`), never chaotic glossy yellow gradients.
- **Dramatic palette:** Obsidian (`#171715`), Antique Gold (`#B89B5E`), Warm Ivory (`#F3ECDD`), Deep Emerald (`#183D36`).
- **Applications:** Luxury brands, high-end hospitality, fine dining, premium portfolios, cultural foundations, and heritage experiences.

### 3. Minimal Deco (`variant: minimal`)

Visual personality:
- **Quiet sophistication:** Subtle geometric accents applied with extreme restraint to a clean, spacious modern layout.
- **Architectural precision:** Hairline geometric dividers, discreet corner brackets, and crisp typographic balance.
- **Understated palette:** Ivory (`#F7F4ED`), Burgundy (`#693B43`), Bronze (`#A98462`), Ink (`#272625`).
- **Functional focus:** Uncompromising usability, high readability, and rapid scannability for content-heavy and operational views.
- **Applications:** Professional services, corporate documentation, modern consumer products, editorial interfaces, and minimal portfolios.

## Good fit / trade-offs

- **Works well for:** High-end architectural studios, cultural institutions, fine hospitality, luxury e-commerce, editorial magazines, premium SaaS platforms, and bespoke portfolios.
- **Be careful with:** High-frequency developer terminals or utilitarian bulk data consoles where decorative framing might reduce data density.
- **Reference directions:**
  - *Rockefeller / Streamline Moderne (Modern):* Deep forest greens, muted brass accents, crisp ivory canvas, and clean parallel line grids.
  - *Chrysler Heritage (Classic):* Obsidian black, geometric antique gold line art, stepped sunburst chevrons, and deep emerald jewel blocks.
  - *Atelier Burgundy & Bronze (Minimal):* Muted linen ivory, deep burgundy headers, brushed bronze dividers, and slate ink body text.

## Art Deco material fidelity gate — mandatory

**Before calling an Art Deco page complete, the opening viewport must visibly read as an architecturally composed, geometrically disciplined design system.** If a user chose this style, a generic black-and-gold card template with arbitrary yellow gradients and rounded SaaS cards is a **FAIL**.

A successful Art Deco implementation demonstrates **all** of the following:

1. **Architectural Geometric Framing:** Containers, headers, and hero modules feature structured stepped silhouettes, corner brackets, or paired parallel hairline rules (`1px–1.5px`) rather than generic rounded SaaS border radii.
2. **Intentional Symmetry & Grid Discipline:** Layouts celebrate deliberate axial alignment, balanced bilateral weight, and rhythmic geometric progression across columns.
3. **Multi-Tiered Typographic Hierarchy:** Display headlines use distinct geometric or high-contrast decorative typography with deliberate tracking (`letter-spacing: 0.05em–0.12em`), editorial headers use refined serifs, and body/data text uses crystal-clear functional sans.
4. **Flat / Layered Metallic Finishes (Zero Shiny Gradient Slop):** Metallic tones (Antique Gold, Muted Brass, Bronze) are applied as clean solid fills or restrained double hairlines, never as noisy multi-stop yellow-to-white diagonal gradients.
5. **Purposeful Ornamentation Engine:** Decorative motifs (chevrons, fan sunbursts, stepped corner brackets) are lightweight SVGs or CSS constructs that serve an explicit structural or hierarchy role, never floating randomly as decorative confetti.
6. **Accessible Contrast & Functional Integrity:** Text contrast meets WCAG AA (4.5:1+) in both light and dark themes. Interactive controls possess visible keyboard focus indicators (`outline: 2px solid var(--taste-deco-accent); outline-offset: 2px;`).
7. **Single-Viewport Hero Composition:** The desktop opening hero integrates navigation, brand title, architectural coordinates/creed, and primary action within a single viewport (`min-height: 100svh`) without awkward clipping or scroll-jacking.

## Explicit art deco ornamentation exception — structured geometry is required

**Art Deco-specific override:** The universal anti-slop caution against *excessive borders or unnecessary decoration* MUST NOT be interpreted as a ban on architectural double lines, stepped corner brackets, or geometric chevron dividers here. In Art Deco, structured geometry and architectural framing are essential design grammar, not cosmetic fluff.

- **Allowed decorative treatments:** Controlled double-line borders (`1px solid var(--taste-deco-border)` with `2px–4px` offset), stepped corner brackets, symmetrical header dividers with central diamond/star motifs, and stylized fan/sunburst SVGs.
- **Anti-slop boundary:** Every ornament must align to the grid, scale responsively, use `aria-hidden="true"`, and never occlude text, cause horizontal scrollbars, or delay user interaction.
- **Anti-slop interpretation:** Evaluate Art Deco layouts by **compositional balance, geometric elegance, and functional clarity**, not by stripping out architectural framing to simulate generic minimalism.

## Typography and typewriting

Typography balances historical grandeur with modern digital legibility across three distinct roles:

- **Display Typography (Headlines & Hero):** High-contrast geometric or decorative display fonts (`Cinzel`, `Playfair Display`, `Marcellus`, `Bodoni Moda`, or geometric grotesque with uppercase styling). Tracking: `0.06em–0.14em` for uppercase headlines; line-height: `1.05–1.2`.
- **Editorial Typography (Section Titles & Subheads):** Elegant serifs or balanced architectural sans (`Cormorant Garamond`, `Lora`, `Inter`, `Cinzel Decorative`). Line-height: `1.3–1.45`.
- **Functional Typography (Body, Forms, Tables, Navigation):** High-legibility modern sans-serif (`Inter`, `Plus Jakarta Sans`, system sans). Body text: `15px–17px`, line-height `1.55–1.65`. Monospace or tabular figures (`tabular-nums`) for timestamps, indexes, and metrics.

## Color direction

All three variants support paired light and dark modes with guaranteed WCAG AA contrast:

### Modern Deco (Default)
- **Light Theme:**
  - Canvas: `#F5F0E6` (Warm Cream)
  - Ink: `#292B29` (Deep Charcoal)
  - Surface: `#FFFFFF` (Crisp Studio)
  - Surface Elevated: `#ECE5D6` (Architectural Linen)
  - Primary Accent / Line: `#B69A68` (Muted Brass)
  - Secondary Accent: `#24453D` (Forest Green)
- **Dark Theme:**
  - Canvas: `#161B18` (Obsidian Pine)
  - Ink: `#F5F0E6` (Warm Cream)
  - Surface: `#1F2622` (Deep Forest Plate)
  - Surface Elevated: `#29332D` (Elevated Forest)
  - Primary Accent / Line: `#D8BC88` (Warm Polished Brass)
  - Secondary Accent: `#345C52` (Luminous Spruce)

### Classic Deco
- **Light Theme:**
  - Canvas: `#F3ECDD` (Warm Ivory)
  - Ink: `#171715` (Obsidian Black)
  - Surface: `#FCF9F2` (Pure Alabaster)
  - Surface Elevated: `#E7DDC8` (Stone Parchment)
  - Primary Accent / Line: `#9E8043` (Antique Gold Ink)
  - Secondary Accent: `#183D36` (Deep Emerald)
- **Dark Theme:**
  - Canvas: `#171715` (Obsidian Night)
  - Ink: `#F3ECDD` (Warm Ivory)
  - Surface: `#20201D` (Smoked Obsidian)
  - Surface Elevated: `#2B2B27` (Polished Basalt)
  - Primary Accent / Line: `#B89B5E` (Antique Gold)
  - Secondary Accent: `#1E4E45` (Emerald Jewel)

### Minimal Deco
- **Light Theme:**
  - Canvas: `#F7F4ED` (Linen Ivory)
  - Ink: `#272625` (Deep Slate Ink)
  - Surface: `#FFFFFF` (Pure Paper)
  - Surface Elevated: `#EBE6DB` (Muted Sand)
  - Primary Accent / Line: `#A98462` (Warm Bronze)
  - Secondary Accent: `#693B43` (Deep Burgundy)
- **Dark Theme:**
  - Canvas: `#1B1A19` (Smoked Charcoal)
  - Ink: `#F7F4ED` (Linen Ivory)
  - Surface: `#242321` (Basalt Plate)
  - Surface Elevated: `#2F2D2A` (Elevated Slate)
  - Primary Accent / Line: `#C5A281` (Luminous Bronze)
  - Secondary Accent: `#8A4E58` (Rose Burgundy)

## Layout and geometry

- **Stepped Silhouette Architecture:** Cards, buttons, and headers employ subtle stepped corner insets (`clip-path` or stepped corner SVGs) or clean `0px–2px` radius. Soft rounded bubble cards (`1.5rem–2rem`) are strictly prohibited in Art Deco.
- **Architectural Framing:** Content modules are bounded by hairline borders (`1px solid var(--taste-deco-border)`) and accented by decorative corner brackets or symmetrical top and bottom line caps.
- **Rhythmic Vertical Slices:** Grids balance full-width hero bays with disciplined 3-column and 4-column feature matrices.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid typography clamp, and mobile drawer navigation.
- **Strict 1:1 circle geometry (anti-oval):** Status indicator gems, circular medallion seals, and icon badges must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;`.

## Surfaces, depth, texture

Art Deco surfaces prioritize tactile architectural finishes over generic SaaS blurred shadows:
- **Fluted & Panelled Surfaces:** Flat, matte surfaces with subtle tonal steps between canvas, card, and elevated dialogs.
- **Restrained Geometric Layering:** Depth is created through contrasting hairline borders, inset stepped padding, and subtle dark-tinted or warm-tinted drop shadows (`0 4px 20px rgba(0, 0, 0, 0.08)`).
- **Hairline Double Rules:** Key divider rules utilize a double hairline pattern (`border-top: 1px solid var(--taste-deco-border); margin-top: 3px; border-bottom: 1px solid var(--taste-deco-border);`).
- **No Glossy Gradients:** Strictly avoid reflective bubble gradients, cheap chrome effects, or chaotic gold swirls.

## Component anatomy and interaction

- **Art Deco Button (Primary):** Stepped corner silhouette, solid accent background (Antique Gold / Muted Brass), high-contrast uppercase text with `0.08em` tracking; subtle lift and gold shimmer outline on hover.
- **Art Deco Button (Secondary / Outline):** 1px solid metallic border with double-line inner inset, transparent fill, uppercase text; fill inverts smoothly on hover.
- **Architectural Card:** Fine geometric border, stepped corner accents (`.art-deco-card-corner`), subtle inner framing hairline, and uppercase section index (`[BAY 01 // SALON]`).
- **Stepped Frame Divider:** Symmetrical horizontal line with central diamond or fan medallion motif (`.art-deco-divider`).
- **Form Controls:** Clean input fields with crisp 1px borders, subtle warm background fill, and high-visibility metallic gold focus ring (`outline: 2px solid var(--taste-deco-accent); outline-offset: 2px;`).
- **Data Table:** Disciplined hairline rows, uppercase tracked column headers, tabular numerals (`tabular-nums`), and subtle row hover highlighting.
- **Navigation Header:** Symmetrical layout with central or left brand monogram, 36px action buttons, theme toggle, and collapsible mobile drawer.

## Motion

Restrained, architectural, and graceful.
- **Default Duration:** 120ms–150ms linear or subtle ease-out for hover transitions.
- **Allowed:** Opacity transitions, subtle 1px–2px vertical translation on button hover, smooth disclosure expansion for accordions.
- **Prohibited:** Constantly spinning fan ornaments, continuous glitter particles, dramatic 3D card flips, bouncy elastic curves, or scroll-blocking reveals.
- **Reduced Motion:** Fully honors `@media (prefers-reduced-motion: reduce)` by disabling transforms and setting duration to 0ms.

## Optional Anime.js v4 recipe

- **Motion decision:** CSS/native browser transitions are preferred. Anime.js v4 is optional and reserved for coordinated architectural panel openings or delicate line reveals when requested.
- **Starting duration:** 150ms (restrained linear or `easeOutQuad`).
- **Avoid:** Endless particle loops, bouncing springs, theatrical golden sparkles.
- **Dependency:** Standalone use follows Taste Engine `references/motion-engine.md`.

## UI writing and microcopy

Cultivated, architectural, poised, and articulate.
- **Tone:** Confident, structured, and factual. Examples: “ARCHITECTURAL SPECIFICATION”, “EXPLORE THE ATELIER”, “VERIFIED MONOGRAPH”, “ESTABLISHED MDCCCCXXV”.
- **Anti-slop:** Avoid tacky luxury clichés (“Opulent Synergy for Disruptors”), artificial marketing hyperbole, or vacuous buzzwords. Every label must correspond to an actual product feature or verifiable metric.

## Starter tokens (suggestions, not a complete theme)

| Token | Modern Deco Default | Classic Deco Default | Minimal Deco Default | Role |
| --- | --- | --- | --- | --- |
| `--taste-deco-bg` | `#F5F0E6` | `#F3ECDD` | `#F7F4ED` | Canvas base surface |
| `--taste-deco-surface` | `#FFFFFF` | `#FCF9F2` | `#FFFFFF` | Primary card and module fill |
| `--taste-deco-surface-elevated` | `#ECE5D6` | `#E7DDC8` | `#EBE6DB` | Elevated dialogs and drawers |
| `--taste-deco-ink` | `#292B29` | `#171715` | `#272625` | Primary headline and body ink |
| `--taste-deco-ink-muted` | `#636662` | `#5C5A52` | `#68645E` | Secondary captions and metadata |
| `--taste-deco-accent` | `#B69A68` | `#9E8043` | `#A98462` | Primary metallic accent (brass/gold/bronze) |
| `--taste-deco-accent-secondary` | `#24453D` | `#183D36` | `#693B43` | Secondary jewel tone (forest/emerald/burgundy) |
| `--taste-deco-border` | `1px solid #D4C7B0` | `1px solid #D6C8A8` | `1px solid #D8CFC0` | Fine architectural hairline border |
| `--taste-deco-border-accent` | `1px solid #B69A68` | `1px solid #9E8043` | `1px solid #A98462` | Accent metallic border |
| `--taste-deco-radius` | `2px` | `0px` | `2px` | Architectural crisp radius |
| `--taste-deco-font-display` | `'Cinzel', serif` | `'Playfair Display', serif` | `'Cinzel', serif` | Geometric decorative display |
| `--taste-deco-font-body` | `'Plus Jakarta Sans', sans-serif` | `'Inter', sans-serif` | `'Inter', sans-serif` | Crisp functional sans body |
| `--taste-deco-motion-duration` | `150ms` | `120ms` | `150ms` | Graceful restrained transition |

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win.
- **Modern Deco:** Symmetrical balanced hero bay with geometric hairline frame, uppercase tracked statement, dual CTAs, and authentic project status telemetry strip.
- **Classic Deco:** Stepped architectural arch or chevron motif framing the monumental display title, flanked by paired coordinate markers and an antique gold action button.
- **Minimal Deco:** Architectural typography with disciplined white space, fine horizontal rules, and a focused conversion action.

See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.

## Style-specific quality gate

- **Do:** ensure circular elements maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;`; verify responsive integrity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales fluidly with `clamp()`; verify header navigation collapses into an accessible hamburger drawer on mobile (< 768px); enforce paired 36px action button heights; confirm crisp hairline geometric borders; ensure all text meets WCAG AA contrast (4.5:1+) against canvas and card surfaces; verify visible keyboard focus rings (`:focus-visible`); ensure decorative SVGs carry `aria-hidden="true"`; verify dark and light mode paired token inversion.
- **Don't:** never use garish diagonal yellow-to-white gradients simulating "gold shine"; avoid generic rounded SaaS cards (no `border-radius: 1.5rem`); never clutter the screen with random unaligned fan shapes; avoid low-contrast gold text on white backgrounds; never use emojis as functional UI icons; avoid fabricated customer metrics or fake awards; never allow decorative corner brackets to cause horizontal layout overflow; avoid heavy animation loops that delay interaction.
- Confirm desktop and mobile consistency; visible keyboard focus; loading, empty, disabled, error and success states; reduced-motion behavior (`prefers-reduced-motion`).

## Universal anti-slop gate (self-contained)

Every element must earn its place. **Content before decoration. Do not decorate uncertainty.** Do not invent balances, metrics, testimonials, users, logos, approval, verified/live/online status, fake activity, or success confirmations; use honest empty/loading/error states instead. Demo data is acceptable only if requested and visibly labeled.

Do not add decorative **card-inside-card** layers: a nested surface must represent a distinct interaction or information boundary. Avoid auto-generated 3-feature grids, 4-stat dashboards, fake hero claims, purposeless charts, badge/chip/icon spam, unrelated decorative art, and random loops merely to fill the viewport. Prefer grouping with typography, spacing, alignment and dividers. Equal peers need intentional visual balance.

**Anti-slop copywriting & zero emojis:** no generic "Unlock your potential", "Experience the future", "Supercharge your workflow", "seamless" claims, or translated equivalents. Headings must communicate actual content, CTAs must name the action, and empty/error/success text must describe real states and next steps. Avoid fake urgency, made-up counts, vague AI hype, and inaccessible all-caps walls. Emojis are strictly forbidden as UI icons, button prefixes, or badges across all styles; interface elements must exclusively use clean vector SVGs from Lucide, Radix, Feather, or Heroicons with currentColor inheritance. Adapt the wording to this style and the user's language without changing the truth.

**Theme and mode contrast integrity:** When a user requests dark mode or light mode (or builds a theme switcher), background and foreground colors MUST flip in synchronized pairs across all surfaces, text, borders, inputs, and semantic badges. Never leave black text on dark background, white text on white background, or unreadable low-contrast status pills. All states must meet WCAG AA contrast (minimum 4.5:1 for body/normal text, 3:1 for large headlines and interactive boundaries).

**Responsive 320px baseline and fluid typography:** compose mobile deliberately down to 320px minimum viewport width with zero horizontal blowout. Scale typography down smoothly while respecting readability minimums (body >= 1rem / 16px, secondary >= 0.875rem, code >= 0.8125rem). In top navigation bars, collapse navigation behind an accessible hamburger menu or disclosure with comfortable tap targets on mobile (< 768px). Circular geometry must enforce aspect-ratio: 1 / 1; flex-shrink: 0;. Static by default; use motion for meaningful interactions, respect reduced-motion preferences, avoid bounce/floating/pulsing decoration without a real state.

**Critical/High findings block completion:** fabricated status/data, broken actions, inaccessible/clipped controls, misleading copy, theme contrast collisions or significant mobile failure must be fixed. Report what was actually verified; do not claim tests that did not run.

**Not an aesthetics veto:** expressive colors, shadows, gradients, card layouts or decorative treatments are legitimate when they are intentional parts of the selected aesthetic and pass usability checks. Do not silently force minimalism.

## Anti-slop: style-specific

**Architectural discipline and purposeful geometry, not generic gold-and-black luxury slop.**

- **Reject:** cheap golden gradients, glowing yellow button shadows, decorative fan icons plastered randomly on every container, generic dark-mode crypto dashboard aesthetics pretending to be Art Deco, hollow luxury buzzwords, fake awards, and low-contrast metallic text.
- **Instead:** Expose clean geometric symmetry, stepped architectural silhouettes, authentic flat metallic finishes, refined multi-tiered typography, and crystal-clear data density.
- **Copy check:** UI writing must be direct, cultivated, and truthful. Replace vague puffery (*"Unmatched Elegance for Next-Gen Leaders"*) with real product capabilities and specifications.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility, and motion checks **in addition** to this style's quality gate. Do not penalize authentic, accessible geometric features characteristic of `art-deco`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
