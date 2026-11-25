---
name: taste-style-retro-pixel
description: Apply Retro Pixel design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses  or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as  instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Retro Pixel

**ID:** `retro-pixel`  
**Signature:** Nostalgic 8-bit and 16-bit personal computing culture with integer-aligned pixel art, classic desktop window chrome, stepped pixel borders, and arcade accents.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. A conventional modern interface with a pixel font **does not qualify as Retro Pixel**.

## Good fit / trade-offs

- **Works well for:** Gaming platforms and studios, indie creator portfolios, retro tech showcases, interactive developer tools, playful SaaS products, and digital culture magazines.
- **Be careful with:** Formal corporate enterprise environments or data-heavy compliance tools where nostalgic computer metaphors may contradict brand seriousness.
- **Reference directions:**
  - *Classic 16-bit Desktop:* Midnight blue grid canvas (`#10102B`) with desktop purple title bars (`#5B438E`), vintage cream content panels (`#F2DFB5`), arcade orange headlines (`#F27D36`), and retro teal accents (`#2CA7A3`).
  - *Warm Beige Workstation:* Vintage cream/parchment base (`#F2DFB5`) with warm gray window chrome (`#D8D2C2`), dark ink text (`#10102B`), stepped beveled panel borders, and arcade-colored status tags.
  - *Arcade Cyber Grid:* Deep indigo background with subtle geometric grid lines, chunky pixel badges, high-contrast button bevels, and crisp pixel-native icons.

## Retro pixel material fidelity gate — mandatory

**Before calling a retro-pixel page complete, the opening viewport must visibly read as a crafted retro graphical user interface and pixel-art environment.** If a user chose this style, a generic dark card layout with monospace text and an orange button is a **FAIL**, even if CSS classes contain `pixel`.

A successful retro-pixel implementation demonstrates **all** of the following:

1. **Pixel Precision & Integer Alignment:** Pixel art illustrations, icons, and decorative accents preserve hard pixel edges without accidental interpolation blur. Use `image-rendering: pixelated` specifically for raster pixel art assets and canvas sprites; never apply blur filters to pixel graphics. Do not force pixel rendering onto standard body text or smooth vector photographic imagery.
2. **Retro Window Surfaces & Desktop Chrome:** Rectangular panels (0–2px radius) feature distinct title bars, crisp separators, and stepped inset/outset beveled borders (`box-shadow: inset -2px -2px 0px #000, inset 2px 2px 0px rgba(255, 255, 255, 0.4)` or stepped multi-layer outlines) reminiscent of classic 1990s desktop operating systems.
3. **Tactile Stepped Button Affordance:** Buttons feature prominent pixel bevels or hard-edged offset drop shadows (`3px 3px 0px #000`). On `:active` or click, buttons physically shift by integer pixels (`transform: translate(2px, 2px); box-shadow: 1px 1px 0px #000;`), delivering unmistakable mechanical feedback.
4. **Structured Retro Visual Hierarchy:** Oversized arcade/pixel display headings pair with highly readable sans-serif or clean monospace body text. Information modules use framed content containers and retro control panel anatomy rather than generic floating card soup.
5. **Pixel-Native Illustration & Iconography:** Decorative elements employ authentic pixel art (such as vintage computer workstations, floppy disks, pixel folders, game controllers, or custom pixel icons) scaled consistently across the viewport. Sprites must communicate meaning or enhance page narrative, not serve as meaningless random stickers.

**First-viewport test:** In a desktop screenshot, identify the desktop window frames, stepped pixel borders, arcade headline typography, and pixel illustrations **without reading the page title**. If it looks like a generic web template with a pixel font, add the desktop window chrome and stepped border treatments.

## Explicit retro pixel exception — pixel graphics and stepped borders are allowed

**Retro-pixel-specific override:** The universal anti-slop caution against *decorative borders, grid patterns, screen ornamentation, or pixel textures* MUST NOT be interpreted as a ban on authentic pixel illustrations, stepped bevels, classic desktop title bars, window controls, or background grid lines here. These are **material-enabling properties**, essential to the Retro Pixel aesthetic.

- **Allowed material treatments:** Stepped pixel borders (`box-shadow` or border-image bevels), 0-blur hard offset shadows, subtle background grid lines, desktop window title bars with functional controls, dither patterns, limited-palette pixel illustrations, retro button press displacement, and pixel-style cursors where interactive affordances remain unambiguous.
- **Anti-slop boundary:** Every window control, tab, and button must perform a real action or clearly identified demo behavior. Do not flood interfaces with nonfunctional fake window controls, unreadable 8px microcopy, broken mobile layouts, or nested decorative windows without purpose.
- **Anti-slop interpretation:** Evaluate retro-pixel elements by **craft authenticity, layout clarity, and user utility**, not by banning nostalgic graphical GUI metaphors. Removing stepped borders and title bars to satisfy a generic flat heuristic is a **design regression**.

## Typography and typewriting

- **Display Typography (Headlines, badges, banner labels):** Blocky, arcade, or pixelated display fonts such as `Pixelify Sans`, `Press Start 2P`, `Silkscreen`, or chunky geometric monospace fallbacks (`'Courier New', monospace`). Headlines: 28–48 px desktop / 18–24 px tablet / 16–20 px mobile (`clamp(1.15rem, 5vw, 2.5rem)`); weight bold/700; line-height 1.25–1.35. Due to wide bitmap font metrics, always scale display headings down aggressively on mobile (`<= 480px`) and avoid long all-caps words that blowout 320px viewport containers.
- **Reading Typography (Body text, forms, tables, data):** Highly legible humanist sans-serif or clean monospace such as `Inter`, `IBM Plex Mono`, `JetBrains Mono`, or system sans (`system-ui, -apple-system, sans-serif`). Body text: 14–16 px; weight 400–500; line-height 1.5–1.6. Never force low-resolution pixel fonts into long multi-line paragraphs.
- **Window Title Bars & Navigation:** 12–14 px desktop / 10–12 px mobile with overflow ellipsis (`text-overflow: ellipsis; white-space: nowrap; overflow: hidden;`). On mobile navigation headers, collapse secondary actions and style galleries behind an accessible hamburger menu drawer to prevent header cramming.
- **Responsive type scale:** Follow the [responsive baseline](../references/responsive-baseline.md) with clamp-based fluid typography that scales headings down smoothly on mobile while preserving headline hierarchy and word wrapping down to 320px viewport width.

## Color direction

Define adaptable tokens rather than locking projects into one rigid palette.

- **Dark Mode (Midnight Arcade Grid):**
  - **Canvas Base:** Midnight navy canvas (`#10102B`).
  - **Window / Surface Panels:** Deep indigo slate (`#1B1B3A` or `#22224A`).
  - **Window Title Bars:** Desktop purple (`#5B438E`).
  - **Display Headline:** Arcade orange (`#F27D36`) or Retro teal (`#2CA7A3`).
  - **Body Text:** Vintage cream (`#F2DFB5`) or crisp ivory (`#EAE6DF`).
  - **Muted Text:** Soft slate lavender (`#9999C2`).
  - **Borders & Inset Bevels:** Hard dark ink (`#080816`) with top-left highlight (`rgba(255, 255, 255, 0.25)`).
  - **Background Grid:** Subtle midnight grid lines (`rgba(44, 167, 163, 0.08)` or `rgba(91, 67, 142, 0.15)`).
- **Light Mode (Vintage Parchment Workstation):**
  - **Canvas Base:** Warm vintage cream / parchment (`#F2DFB5` or `#EFE5CF`).
  - **Window / Surface Panels:** Warm retro beige-gray (`#E4DECE` or `#D8D2C2`).
  - **Window Title Bars:** Deep workstation purple (`#493475`) or muted teal (`#1D7D7A`).
  - **Display Headline:** Deep arcade rust-orange (`#C85718`) or dark teal (`#166B68`).
  - **Body Text:** Midnight ink (`#10102B`).
  - **Muted Text:** Deep slate olive (`#5A554A`).
  - **Borders & Inset Bevels:** Solid dark charcoal (`#1C1B24`) with top-left highlight (`#FFFFFF`).
  - **Background Grid:** Subtle warm grid lines (`rgba(16, 16, 43, 0.06)`).
- **Semantic Statuses:**
  - **Error:** Pixel Red (`#E03E3E` dark / `#B91C1C` light).
  - **Warning:** Arcade Amber (`#E69B00` dark / `#B45309` light).
  - **Success:** Pixel Mint (`#2BB673` dark / `#047857` light).
  - **Info:** Retro Teal (`#2CA7A3` dark / `#166B68` light).
- **Theme Coupling & Anti-Collision Rule:** When switching themes, borders, surfaces, title bars, and text colors flip in tandem. Never leave dark ink text on midnight canvas or light cream text on parchment. All text-to-background combinations must exceed WCAG AA contrast (minimum 4.5:1 for body copy, 3:1 for large display titles).

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicators, pixel avatar frames, circular control knobs with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent deformation into ovals under mobile flexbox compression.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns. Desktop multi-column window arrangements collapse into single-column modular panels on mobile. Top navigation links collapse behind an accessible hamburger menu on narrow screens (< 768px).
- **Pixel Grid & Alignments:** Borders, margins, and paddings align along a 4px/8px coordinate grid. Corners are square (`border-radius: 0px`) or minimally notched (`border-radius: 2px`). Avoid smooth modern rounded pill shapes (`border-radius: 9999px`) on core window frames and buttons.

## Surfaces, depth, texture

- **Raised Retro Window:** Flat panel with stepped 3D bevel (`box-shadow: inset 2px 2px 0px rgba(255, 255, 255, 0.35), inset -2px -2px 0px #000, 4px 4px 0px rgba(0, 0, 0, 0.8)`).
- **Retro Title Bar:** Full-width header banner in desktop purple (`#5B438E`) with white/cream title, optional pixel icon, and miniature action buttons (`_`, `□`, `×`).
- **Sunken Well / Inset Panel:** Inset content area (`box-shadow: inset 2px 2px 0px #000, inset -2px -2px 0px rgba(255, 255, 255, 0.25); background: var(--taste-pixel-well-bg)`).
- **Pixel Frame & Dither Border:** 2px solid border with alternating color dots or crisp corner notches.
- **Nested Sub-Panels (Card-in-Window):** Allowed when encapsulating distinct tool bays, inventory slots, command logs, or dialog sections inside a primary desktop window frame. Mindless decorative nesting without functional boundaries remains disallowed.

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, button prefixes, or status stickers across all UI elements. Use crisp pixel-native SVGs or custom pixel icons (16px, 20px, 24px) rendered with `image-rendering: pixelated` and consistent stroke weights.
- **Pixel Button:** Raised rectangular button with 2px solid outline and stepped shadow. Hover: slight border brighten or color shift. Active/Press: `transform: translate(2px, 2px); box-shadow: inset 2px 2px 0px #000;`.
- **Navigation Action Buttons & Paired Symmetry:** Action buttons in headers (Gallery link and Theme Toggle) must maintain strictly identical height (36px desktop / 38px mobile square), line-height (1), and vertical centering. Never use unconstrained emoji glyphs that distort button heights; wrap icons in 14×14px SVG containers so paired controls align on the integer grid.
- **Text Inputs & Form Controls:** Sunken inset wells with high-contrast text, 2px border, and prominent 2px solid accent focus ring (`:focus-visible`).
- **Checkboxes & Radios:** Chunky square checkboxes with pixel checkmarks (`✓`) and square radio buttons with centered pixel dot.
- **Desktop Window Component:** Complete with draggable/fixed header bar, window title, close/minimize buttons, content pane, and status bar.
- **Tab Bar:** Classic overlapping folder tabs with raised active tab connected directly to the content surface below.
- **Dialogs & Modals:** Stepped window frames centered over a subtle darkened/dithered backdrop overlay with working escape key and close button dismissal.

## Motion

Immediate or short stepped transitions by default (0–90 ms). Short 2px translations for button presses and window actions. Sprite frame animations (2–4 frames) when meaningful. Respect `prefers-reduced-motion` immediately by setting transition durations to 0 and disabling transforms.

## Optional Anime.js v4 recipe

- **Motion decision:** Discrete stepped button press (`translate(2px, 2px)`), window open/close scale-up (0.96 to 1.0), or tab flip; keep transitions snappy and integer-aligned.
- **Starting duration:** 90ms (0 = immediate); adjust to task and user preference.
- **Avoid:** elastic bounce, overshoot easing, perpetual jumping sprite loops, continuous screen glitching, and CRT flicker.
- **Dependency:** CSS/native by default. Use Anime.js v4 only if the requested interaction justifies it. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Playful, direct, nostalgic, and human. Grounded in genuine personal computing and arcade culture without condescending jargon or artificial hype. Examples: `Save Project`, `Ready`, `3 items selected`, `Disk 1 of 2`. Avoid generic AI filler like *"Revolutionize your workflow"* or *"Next-generation intelligence"*.

## Starter tokens (suggestions, not a complete theme)

| Token | Dark mode default | Light mode default |
| --- | --- | --- |
| `--taste-pixel-bg` | `#10102b` | `#f2dfb5` |
| `--taste-pixel-surface` | `#1b1b3a` | `#e4dece` |
| `--taste-pixel-window` | `#22224a` | `#d8d2c2` |
| `--taste-pixel-header` | `#5b438e` | `#493475` |
| `--taste-pixel-well-bg` | `#0d0d22` | `#ded6c4` |
| `--taste-pixel-teal` | `#2ca7a3` | `#166b68` |
| `--taste-pixel-orange` | `#f27d36` | `#c85718` |
| `--taste-pixel-purple` | `#5b438e` | `#493475` |
| `--taste-pixel-cream` | `#f2dfb5` | `#10102b` |
| `--taste-pixel-text` | `#f2dfb5` | `#10102b` |
| `--taste-pixel-text-muted` | `#9999c2` | `#5a554a` |
| `--taste-pixel-border` | `2px solid #080816` | `2px solid #1c1b24` |
| `--taste-pixel-bevel-light` | `rgba(255, 255, 255, 0.35)` | `#ffffff` |
| `--taste-pixel-bevel-dark` | `#000000` | `#000000` |
| `--taste-pixel-radius` | `0px` | `0px` |
| `--taste-pixel-font-display` | `'Pixelify Sans', 'Press Start 2P', monospace` | `'Pixelify Sans', 'Press Start 2P', monospace` |
| `--taste-pixel-font-body` | `'Inter', system-ui, sans-serif` | `'Inter', system-ui, sans-serif` |
| `--taste-pixel-motion-duration` | `90ms` | `90ms` |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-pixel-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win. **Style-specific direction:** Construct the first viewport as an expressive vintage workstation or retro gaming desktop: featured pixel artwork (e.g. vintage beige computer monitor with glowing display), bold arcade headline typography in orange/teal, a primary pixel CTA button with stepped press feedback, and desktop window chrome framing introductory content. Do not fill empty space with fake glitch loops or unreadable falling code. See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.

## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally to prevent bloated UI; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); verify high text contrast against canvas (WCAG AA); ensure pixel art graphics use integer scaling and `image-rendering: pixelated`; provide clear click fallbacks and keyboard focus rings (`:focus-visible`); test dark/light mode switching with coupled tokens; ensure all window action controls are functional or clearly identified demo interactions.
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean pixel vector SVGs with currentColor); do not apply pixel fonts to long body paragraphs; avoid blurred raster illustrations; do not present dead decorative window buttons that do nothing when clicked; avoid light-mode theme collisions such as white text on beige window panels.
- Confirm desktop and mobile consistency; visible keyboard focus (`:focus-visible`); loading, empty, disabled, error and success states; reduced-motion behavior (`prefers-reduced-motion`).
- Do not inject style-specific assumptions into unrelated projects. When combining styles, explicitly name the primary style and the borrowed features.

## Universal anti-slop gate (self-contained)

Every element must earn its place. **Content before decoration. Do not decorate uncertainty.** Do not invent balances, metrics, testimonials, users, logos, approval, verified/live/online status, fake activity, or success confirmations; use honest empty/loading/error states instead. Demo data is acceptable only if requested and visibly labeled.

Do not add decorative **card-inside-card** layers: a nested surface must represent a distinct interaction or information boundary. Avoid auto-generated 3-feature grids, 4-stat dashboards, fake hero claims, purposeless charts, badge/chip/icon spam, unrelated decorative art, and random loops merely to fill the viewport. Prefer grouping with typography, spacing, alignment and dividers. Equal peers need intentional visual balance.

**Anti-slop copywriting & zero emojis:** no generic "Unlock your potential", "Experience the future", "Supercharge your workflow", "seamless" claims, or translated equivalents. Headings must communicate actual content, CTAs must name the action, and empty/error/success text must describe real states and next steps. Avoid fake urgency, made-up counts, vague AI hype, and inaccessible all-caps walls. Emojis are strictly forbidden as UI icons, button prefixes, or badges across all styles; interface elements must exclusively use clean vector SVGs from Lucide, Radix, Feather, or Heroicons with currentColor inheritance. Adapt the wording to this style and the user's language without changing the truth.

**Theme and mode contrast integrity:** When a user requests dark mode or light mode (or builds a theme switcher), background and foreground colors MUST flip in synchronized pairs across all surfaces, text, borders, inputs, and semantic badges. Never leave black text on dark background, white text on white background, or unreadable low-contrast status pills. All states must meet WCAG AA contrast (minimum 4.5:1 for body/normal text, 3:1 for large headlines and interactive boundaries).

**Responsive 320px baseline and fluid typography:** compose mobile deliberately down to 320px minimum viewport width with zero horizontal blowout. Scale typography down smoothly while respecting readability minimums (body >= 1rem / 16px, secondary >= 0.875rem, code >= 0.8125rem). In top navigation bars, collapse navigation behind an accessible hamburger menu or disclosure with comfortable tap targets on mobile (< 768px). Circular geometry must enforce aspect-ratio: 1 / 1; flex-shrink: 0;. Static by default; use motion for meaningful interactions, respect reduced-motion preferences, avoid bounce/floating/pulsing decoration without a real state.

**Critical/High findings block completion:** fabricated status/data, broken actions, inaccessible/clipped controls, misleading copy, theme contrast collisions or significant mobile failure must be fixed. Report what was actually verified; do not claim tests that did not run.

**Not an aesthetics veto:** expressive colors, shadows, gradients, card layouts or decorative treatments are legitimate when they are intentional parts of the selected aesthetic and pass usability checks. Do not silently force minimalism.

## Anti-slop: style-specific

**Authentic retro computing environment, not pixel novelty wallpaper.**

- **Reject:** emojis used as UI icons or button stickers, generic modern cards with pixel icons pasted on top, unreadable tiny 8px microcopy, nonfunctional fake window controls, excessive screen flicker or CRT scanlines where Retro Terminal belongs, blurred pixel art assets, and endless nested windows without purpose.
- **Instead:** Provide real retro window anatomy, crisp stepped pixel borders, integer-scaled artwork, readable humanist body typography, functional desktop controls, and calibrated dark/light contrast.
- **Copy check:** Use clear, honest, grounded copy; eliminate vague AI marketing filler and fake telemetry statistics.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `retro-pixel`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
