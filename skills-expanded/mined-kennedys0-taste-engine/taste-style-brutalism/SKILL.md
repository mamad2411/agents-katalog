---
name: taste-style-brutalism
description: Apply Brutalism design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses brutalism or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as taste-engine instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Brutalism

**ID:** `brutalism`  
**Signature:** Raw structural honesty, exposed layout scaffolding, uncompromising monochrome contrast, and zero decorative camouflage.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. A chaotic, broken layout with arbitrary font sizes **does not qualify as architectural Brutalism**.

## Native layout variants

Brutalism provides two native layout variants sharing the same uncompromising material foundation:

```yaml
style:
  id: brutalism
  name: Brutalism
  category: visual-style
  default_variant: raw
  variants:
    raw:
      identity: raw-brutalism
      focus: linear-scaffolding
    bento:
      identity: brutalist-bento
      focus: modular-asymmetric-grid
```

### 1. Raw Brutalism (`variant: raw`, Default)

Preserves the original foundational aesthetic of raw structural honesty:
- **Exposed structural layout:** Section scaffolding and blueprint lines celebrated as primary visual elements.
- **Monumental typographic hierarchy:** Condensed grotesk headlines (`Anton`, `Space Grotesk 900`, `Impact`) with tight leading (0.88–1.05).
- **Intentionally raw composition:** High-contrast opaque planes, flush modular junctions, and deliberate visual tension.
- **No mandatory card containers:** Content lives inside flush cellular blueprint compartments and exposed linear frames rather than floating cards.
- **Strict 0px border radii:** Absolute square corners everywhere (`border-radius: 0px`).

### 2. Brutalist Bento (`variant: bento`)

Combines the compositional strengths of Bento Grid with the authentic visual principles of Brutalism:
- **Modular grid composition:** Asymmetric CSS Grid layout with intentional variation in panel sizes (dominant 2x2 hero bay, wide 2x1 modules, and compact 1x1 operational spec cells).
- **Grid-driven content prioritization:** Content drives panel spans rather than decorative filler.
- **Defined structural boundaries:** Every bento compartment is enclosed in solid black or white structural borders (`2px–3px solid`) with flush track alignment.
- **Zero cosmetic camouflage:** Flat opaque surfaces, 0px square corners, zero soft drop shadows, and zero pastel gradients.
- **Important:** Bento defines layout composition, not an independent visual style. A Brutalist Bento implementation remains unapologetically Brutalist and never degenerates into a generic rounded SaaS dashboard.

## Good fit / trade-offs

- **Works well for:** Avant-garde portfolios, activist platforms, architectural archives, independent publishing, art/culture institutions, developer tools seeking uncompromised structural authenticity, and modular feature overviews (Brutalist Bento).
- **Be careful with:** Conventional mass-market consumer applications where decorative familiarity and gentle aesthetics reduce initial user hesitation.
- **Reference directions:**
  - *Architectural Béton Brut (Raw):* Raw concrete gray (`#E8E8E8` to `#DCDCDC`), pure stark black lines (`#000000`), exposed structural grid divisions, and monospaced architectural metadata.
  - *Stark Monochrome Scaffolding (Raw):* Pure white background (`#FFFFFF`) with heavy black borders (`2.5px solid #000000`), stark black block actions, and zero cosmetic ornamentation.
  - *Brutalist Bento Grid (Bento):* Asymmetric multi-span modular compartments bounded by solid 2px borders, featuring prominent monospace indexes (`01`, `02`, `03`), bold condensed display headers, and high-voltage operational signal accents (`#FFDE00` / `#FF3B30`).

## Brutalist material fidelity gate — mandatory

**Before calling a brutalist page complete, the opening viewport must visibly read as a raw, honest structural composition.** If a user chose this style, a generic site that merely applies unstyled defaults, chaotic overlapping text, or generic soft rounded cards is a **FAIL**.

A successful brutalist implementation demonstrates **all** of the following:

1. **Exposed Structural Scaffolding:** Grid lines, section dividers, and content containers are formed by visible solid black borders (`2px–3px solid #000000`), celebrating the structural skeleton of the webpage.
2. **Zero Cosmetic Camouflage:** Absolutely no soft blurred drop shadows, no glossy reflections, no rounded bubble corners, and no translucent glass blurs. Surfaces are flat, opaque, and unapologetically direct.
3. **Hyper-Disciplined Alignment:** Despite its raw material honesty, alignment is razor-sharp. Columns, borders, and rows lock together seamlessly with zero erratic wandering.
4. **Stark High-Contrast Palette:** Uncompromising black-on-white or black-on-concrete monochrome contrast meeting WCAG AAA (7:1+). Color is used only as an operational alert signal (pure red `#FF0000` or raw warning yellow `#FFD700`).
5. **Immediate Interactive State Transitions:** Buttons and interactive elements flip instantly on `:hover` and `:active` (e.g. immediate color inversion from black-on-white to white-on-black) without delayed easing or artificial spring physics.
6. **Exposed Blueprint Gridlines & Cellular Enclosure:** Every section, compartment, and functional module must be enclosed in solid structural borders (`2px–3px solid`), aligning flush without awkward gaps like an architectural blueprint or constructivist formwork.
7. **Strict 0px Border Radii Mandate:** Absolute square corners everywhere (`border-radius: 0px`). Bubble corners, rounded buttons, and pill badges are strictly forbidden in architectural brutalism (both Raw and Bento variants).
8. **Monumental Heavyweight Condensed Typography:** Primary hero headlines must use heavyweight condensed grotesk typography (`Anton`, `Space Grotesk 900`, `Impact`, or heavy bold sans) with tight leading (0.88–1.05) and uppercase treatment.
9. **Controlled Operational Signal Colors:** The foundation is uncompromising black and white / concrete paper. Saturated color is strictly limited to high-voltage Warning Yellow (`#FFDE00`) and Signal Red (`#FF3B30`), used for operational status cells, active project rows, and primary conversion CTAs.
10. **Structured Architectural Indexing:** Compartments must feature explicit structural numbering (`01`, `02`, `03`, `04`), directional arrows (`↗`, `→`, `↓`), and technical metadata brackets.
11. **Single-Viewport Hero Composition ("1-Page Fit"):** The opening desktop hero must assemble the brand headline, architectural coordinate cell, status ticker, and primary action within a single view (`100svh`) before expanding into the project matrix and documentation.
12. **Cellular Blueprint Navigation Architecture:** Navigation bars must be composed of discrete, bounded rectangular cells divided by continuous vertical lines (`2px–3px solid`). Keep the main navigation track uncluttered by avoiding long code snippets or oversized command strings directly inside menu cells; place CLI installation pills or utility commands in the hero action group or a dedicated sub-bar. The brand cell features monumental condensed type, auxiliary role/taglines use compact uppercase stacked text (e.g. 2–3 vertical lines), navigation links sit in distinct rectangular bays, and the primary conversion CTA occupies the far right cell highlighted in a high-voltage operational color (such as Caution Yellow `#FFDE00`) with a directional corner arrow (`↗`).
13. **Hero Void Elimination & Architectural Spec Grid:** A brutalist hero composition avoids hollow, unpurposed whitespace between the primary headline and action row. When vertical space exists, structure it with dense, authentic architectural data relevant to the project: such as a multi-compartment numbered technical spec grid (`01`, `02`, `03` with prominent monospace index numbers and truthful functional specifications), an authentic circular stamp seal with running perimeter text, or technical metadata callouts.
14. **Monumental Headline Architecture:** Primary hero headlines must use monumental, tightly stacked condensed heavyweight grotesk typography (`Anton`, `Space Grotesk 900`, `Impact`, or heavy bold sans) with tight leading (`0.88–1.05`) and uppercase treatment, paired with a high-contrast bulleted micro-statement establishing the site's authentic purpose. The copy must directly reflect the user's specific product or project without generic template filler.

**First-viewport test:** In a desktop screenshot, identify the exposed structural border grid, the flat unornamented planes, and the stark monochrome authority **without reading the page title**. If it contains rounded cards or soft shadows, strip away the decorative camouflage immediately.

## Explicit brutalist structural exception — exposed grid borders are required

**Brutalism-specific override:** The universal anti-slop caution against *excessive borders or harsh contrast* MUST NOT be interpreted as a ban on thick black dividing lines (2px–3px solid) or exposed structural scaffolding here. In architectural brutalism, structural joints and honest materials are celebrated, not hidden behind cosmetic paint.

- **Allowed structural treatments:** Visible 2px–3px structural borders, raw rectangular containers, high-contrast monospace metadata, immediate color inversion states, and asymmetric modular bento grids with content-driven column and row spans.
- **Anti-slop boundary:** Do not deliberately break accessibility by overlapping body paragraphs, using unreadable neon clash colors, or making buttons impossible to locate. Authentic brutalism is hyper-functional, not randomly broken.
- **Anti-slop interpretation:** Evaluate brutalist layouts by **structural integrity, functional utility, and legibility**, not by trying to soften hard edges. Removing structural borders to satisfy a generic soft heuristic is a **design regression**.

## Typography and typewriting

Unyielding, heavyweight grotesk sans or technical monospace: Arial, Helvetica, IBM Plex Sans, IBM Plex Mono, Space Grotesk, or system sans. Headlines: 44–72 px desktop / 30–44 px mobile (weight 800–900, tight line-height 1.05–1.15). Body text: 16–18 px (weight 400, line-height 1.5). Monospace for metadata, timestamps, and section indexes.

In Brutalist Bento layouts, each panel features high-contrast typographic hierarchy with prominent monospace compartment markers (`[01 // CORE_SPEC]`, `[02 // MATRIX]`), scannable technical subheadings, and concise data labels.

## Color direction

- **Light Mode (Stark Paper):**
  - **Canvas Base:** Stark paper white (`#FFFFFF`) or architectural concrete (`#E5E5E5`).
  - **Structural Ink / Borders:** Pure black (`#000000`).
  - **Surface Blocks / Tiles:** High-contrast solid fills (`#000000` or `#FFFFFF`).
- **Dark Mode (Pitch Inverted):**
  - **Canvas Base:** Stark pitch black (`#000000`).
  - **Structural Ink / Borders:** Pure stark white (`#FFFFFF`).
  - **Surface Blocks / Tiles:** High-contrast solid dark fills (`#000000` or `#121212`).
- **Operational Signal Accent (Single Color Only):** Signal Red (`#FF0000` / `#FF3333`) or Warning Amber (`#FFCC00` / `#FFDE00`).
- **Theme Inversion Rule:** In brutalism, dark/light mode is an authoritative polarity flip. In dark mode, canvas is `#000000` and text/borders are `#FFFFFF`. Buttons invert cleanly on hover (light: white button flips to black fill + white text; dark: black button flips to white fill + black text). Black text on black background or white text on white background is strictly forbidden.

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicator dots, avatars, circular buttons with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent them from squishing into distorted ovals when viewport shrinks down to 320px.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns.
- **Corners:** Corners are strictly square (`border-radius: 0px`) across all elements and both variants. Bubble corners, rounded buttons, and pill badges are forbidden.
- **Structural borders:** `2px–3px solid #000000` in light mode, `2px–3px solid #ffffff` in dark mode.

### Layout structures by variant

```text
Raw Brutalism (Linear Scaffolding):
+------------------------------------+
| CELLULAR BLUEPRINT NAVIGATION      |
+------------------------------------+
| MONUMENTAL HERO MONOLITH           |
| [ARCHITECTURAL SPECIFICATION 01]   |
+------------------------------------+
| EXPOSED LINEAR COMPARTMENTS        |
+------------------------------------+

Brutalist Bento (Asymmetric Modular Grid):
+----------------------+-------------+
|                      |             |
| 01 PRIMARY HERO BAY  | 02 TELEMETRY|
| (COL SPAN 2)         | (COL SPAN 1)|
+-----------+----------+-------------+
|           |                        |
| 03 STATUS | 04 WORKSTREAM MATRIX   |
| (SPAN 1)  | (COL SPAN 2)           |
+-----------+------------------------+
| 05 FULL-WIDTH SPECIFICATION DOCK   |
+------------------------------------+
```

- **Raw Variant:** Content blocks lock flush against each other or maintain firm 16px/24px modular gaps with linear structural rhythm.
- **Bento Variant:** Uses CSS Grid (`grid-template-columns: repeat(3, 1fr)` or `repeat(4, 1fr)` on desktop, collapsing to 2 columns on tablet and 1 column on mobile) with 16px–24px gaps, varied row/column spans, and strictly square panel geometry.

## Surfaces, depth, texture

Surfaces are 100% flat, opaque, and structural. Zero shadows. Zero gradients. Depth is established purely by layering black blocks over white frames, crisp border grids, and immediate inversion of foreground and background colors.

In Brutalist Bento, modular panels are defined by solid structural borders and flat background fills (`#ffffff` / `#000000` / `#121212`) rather than drop shadows or blurry glow effects.

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, status indicators, or button prefixes across all UI elements. Use Lucide or clean vector SVGs (16px–24px) with consistent stroke weight (1.5px–2px) and currentColor.
- **Brutalist Button:** Heavy structural border (`2px solid currentColor`), solid background, bold uppercase text; on hover/active, immediately inverts foreground and background colors.
- **Structural Panel (Raw):** Rectangular container with heavy borders; dividers between internal sections.
- **Brutalist Bento Tile (Bento):** Modular grid cell bounded by solid 2px borders, 0px radius, monospace index header (`01 // PRIMARY`), distinct internal content anatomy, and optional directional corner link (`↗`).
- **Metadata Tag:** Monospace tag enclosed in square brackets: `[DOC_REF: 4092]`.
- **Form Controls:** Unadorned input fields with thick structural border and high-contrast solid focus ring (`outline: 3px solid currentColor; outline-offset: 2px;`).
- **Architectural Spec Cell:** A rectangular compartment bounded by 2px solid lines featuring a prominent monospace index number (`01`, `02`, `03`), an uppercase technical label, and brief, truthful functional specifications.
- **Circular Stamp Seal:** An authentic vector circular stamp badge with running perimeter text along an SVG circular textPath and a solid central graphic mark (such as an asterisk `*` or star `★`), celebrating verified structural fidelity without relying on soft decorative badges. Copy is user-defined.
- **Cellular Navigation Bar:** A full-width header divided into discrete architectural bays (brand cell, stacked multi-line role/tagline cell, individual link cells, theme polarity invert button, and high-visibility corner action cell).

## Motion

Immediate state flips by default (0 ms) or very brief linear transitions (60–100 ms). No bounce, no easing curves, no parallax, no decorative transitions.

For Brutalist Bento, tiles remain rock-solid in place. If hover feedback is desired, use an immediate border color flip or background fill inversion rather than floating card elevation or bouncy transforms.

## Optional Anime.js v4 recipe

- **Motion decision:** Immediate state flips by default; Anime.js generally unnecessary for authentic brutalism.
- **Starting duration:** 0ms (immediate); adjust only if a specific functional mechanical sliding shutter is requested (max 100ms linear).
- **Avoid:** springs, sliding reveals, theatrical scroll animations, continuous tile bounce.
- **Dependency:** CSS/native by default. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Direct, unapologetic, and factual. Examples: “INDEX”, “DOWNLOAD SPECIFICATION”, “TERMINAL ERROR: CONNECTION LOST”, “CONFIRM”. Avoid chatty conversational copy, hollow corporate jargon, or persuasive marketing fluff.

## Starter tokens (suggestions, not a complete theme)

| Token | Light mode default | Dark mode default | Role |
| --- | --- | --- | --- |
| `--taste-brutal-bg` | `#ffffff` | `#000000` | Canvas base |
| `--taste-brutal-ink` | `#000000` | `#ffffff` | Primary text and line ink |
| `--taste-brutal-surface` | `#ffffff` | `#121212` | Surface block fill |
| `--taste-brutal-border` | `2.5px solid #000000` | `2.5px solid #ffffff` | Structural blueprint border |
| `--taste-brutal-radius` | `0px` | `0px` | Strict square corners |
| `--taste-brutal-signal-yellow` | `#ffde00` | `#ffde00` | High-voltage operational warning |
| `--taste-brutal-signal-red` | `#ff3b30` | `#ff3b30` | Critical alert / primary CTA |
| `--taste-brutal-bento-gap` | `20px` | `20px` | Modular grid gutter spacing |
| `--taste-brutal-font-heading` | `'Arial Black', Arial, Helvetica, sans-serif` | `'Arial Black', Arial, Helvetica, sans-serif` | Heavy display grotesque |
| `--taste-brutal-font-body` | `Arial, Helvetica, sans-serif` | `Arial, Helvetica, sans-serif` | Functional sans body |
| `--taste-brutal-font-mono` | `'IBM Plex Mono', monospace` | `'IBM Plex Mono', monospace` | Technical spec monospace |
| `--taste-brutal-motion-duration` | `0ms` | `0ms` | Immediate state flips |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-brutal-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win.

- **Raw Variant:** Construct the first viewport as an unapologetic architectural monolith: massive display title locked inside structural scaffolding, stark black call-to-action blocks, cellular navigation, and zero cosmetic filler.
- **Bento Variant:** Structure the first viewport as an asymmetric modular bento grid where the dominant product story occupies the primary 2x2 panel and supporting specifications/metrics surround it in disciplined 0px square bays. Do not cram 8 tiny empty cards merely to fill height.

See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.

## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); verify stark monochrome contrast; ensure 2–3px structural borders are solid; verify sharp 0px square corners; confirm single-viewport hero fit on desktop; enforce monumental condensed typography; verify controlled caution yellow (`#ffde00`) and signal red (`#ff3b30`) operational roles; verify dark/light mode polarity inversion so text and background never clash (no black-on-black or white-on-white text); verify cellular navigation without long code clutter; ensure hero voids are structured with architectural spec grids or bento panels; confirm circular stamp seal or technical metadata.
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean vector SVGs with currentColor); do not add rounded corners, soft drop shadows, or smooth color gradients (strictly 0px radius across both Raw and Bento variants); avoid arbitrary font size chaos; never use pill buttons; avoid oversized padding that breaks the single-viewport hero fit; avoid decorative filler badges or chatty marketing copy; do not leave black ink or borders when switching to dark canvas; never leave cavernous empty whitespace between hero headlines and buttons; do not place long command code strings inside the main navigation bar; never turn Brutalist Bento into a generic rounded SaaS dashboard.
- Confirm desktop and mobile consistency; visible keyboard focus (`:focus-visible`); loading, empty, disabled, error and success states; reduced-motion behavior (`prefers-reduced-motion`).
- Do not inject style-specific assumptions into unrelated projects. When combining styles, explicitly name the primary style, layout variant, and borrowed features.

## Universal anti-slop gate (self-contained)

Every element must earn its place. **Content before decoration. Do not decorate uncertainty.** Do not invent balances, metrics, testimonials, users, logos, approval, verified/live/online status, fake activity, or success confirmations; use honest empty/loading/error states instead. Demo data is acceptable only if requested and visibly labeled.

Do not add decorative **card-inside-card** layers: a nested surface must represent a distinct interaction or information boundary. Avoid auto-generated 3-feature grids, 4-stat dashboards, fake hero claims, purposeless charts, badge/chip/icon spam, unrelated decorative art, and random loops merely to fill the viewport. Prefer grouping with typography, spacing, alignment and dividers. Equal peers need intentional visual balance.

**Anti-slop copywriting & zero emojis:** no generic "Unlock your potential", "Experience the future", "Supercharge your workflow", "seamless" claims, or translated equivalents. Headings must communicate actual content, CTAs must name the action, and empty/error/success text must describe real states and next steps. Avoid fake urgency, made-up counts, vague AI hype, and inaccessible all-caps walls. Emojis are strictly forbidden as UI icons, button prefixes, or badges across all styles; interface elements must exclusively use clean vector SVGs from Lucide, Radix, Feather, or Heroicons with currentColor inheritance. Adapt the wording to this style and the user's language without changing the truth.

**Theme and mode contrast integrity:** When a user requests dark mode or light mode (or builds a theme switcher), background and foreground colors MUST flip in synchronized pairs across all surfaces, text, borders, inputs, and semantic badges. Never leave black text on dark background, white text on white background, or unreadable low-contrast status pills. All states must meet WCAG AA contrast (minimum 4.5:1 for body/normal text, 3:1 for large headlines and interactive boundaries).

**Responsive 320px baseline and fluid typography:** compose mobile deliberately down to 320px minimum viewport width with zero horizontal blowout. Scale typography down smoothly while respecting readability minimums (body >= 1rem / 16px, secondary >= 0.875rem, code >= 0.8125rem). In top navigation bars, collapse navigation behind an accessible hamburger menu or disclosure with comfortable tap targets on mobile (< 768px). Circular geometry must enforce aspect-ratio: 1 / 1; flex-shrink: 0;. Static by default; use motion for meaningful interactions, respect reduced-motion preferences, avoid bounce/floating/pulsing decoration without a real state.

**Critical/High findings block completion:** fabricated status/data, broken actions, inaccessible/clipped controls, misleading copy, theme contrast collisions or significant mobile failure must be fixed. Report what was actually verified; do not claim tests that did not run.

**Not an aesthetics veto:** expressive colors, shadows, gradients, card layouts or decorative treatments are legitimate when they are intentional parts of the selected aesthetic and pass usability checks. Do not silently force minimalism.

## Anti-slop: style-specific

**Structural honesty and disciplined composition, not aesthetic playfulness or generic dashboard slop.**

- **Reject:** emojis used as UI icons or button stickers, rounded pill shapes, pastel accents, decorative shadow blurs, arbitrary font chaos, playful sticker illustrations, generic template cards, empty filler tiles added solely to balance a CSS grid, and theme collisions (such as black text remaining on a dark brutalist canvas).
- **Instead:** Expose layout grids with heavy structural borders, stark type hierarchy, immediate state flips, unambiguous contrast, and content-grounded panel modularity.
- **Copy check:** UI writing must be brief, direct, and functional without marketing jargon. Every Bento panel heading must communicate real functional utility.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `brutalism`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
