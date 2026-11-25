---
name: taste-style-neo-brutalism
description: Apply Neo-brutalism design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses  or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as  instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Neo-brutalism

**ID:** `neo-brutalism`  
**Signature:** Playful bold colors, high-contrast black borders, hard unblurred offset shadows, and tactile mechanical press feedback.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. A flat card with rounded corners and a soft blurred drop shadow **does not qualify as Neo-brutalism**.

## Good fit / trade-offs

- **Works well for:** Creator tools, playful B2B SaaS, modern developer portals, hackathon/event platforms, indie product websites, and marketing pages demanding unmistakable personality.
- **Be careful with:** Formal financial reporting or enterprise legal workflows unless specifically branded for an energetic, non-traditional audience.
- **Reference directions:**
  - *Light Pop Canvas:* Crisp cream or warm paper base (`#FFFDF7` / `#F4F0EA`) with high-contrast black strokes (`#121212`), electric accent fills (vivid yellow `#FFDE59`, punchy cyan `#4DEEEA`, coral `#FF5E5B`), and crisp unblurred drop shadows (`5px 5px 0 #121212`).
  - *Dark Pop Contrast:* Deep ink canvas (`#18181B`) with stark white borders (`2.5px solid #FAFAFA`), vivid lime/violet accents, and white/accent offset shadows (`4px 4px 0 #FAFAFA`).

## Neo-brutalist material fidelity gate — mandatory

**Before calling a neo-brutalist page complete, the opening viewport must visibly read as an authentic neo-brutalist composition.** If a user chose this style, a generic card with subtle border-radius and standard blurred shadow is a **FAIL**, even if CSS classes contain `neo`.

A successful neo-brutalist implementation demonstrates **all** of the following:

1. **High-Contrast Solid Outlines:** Core containers, actionable buttons, inputs, and badges feature crisp solid borders (`2px–3px solid #121212`). No faint gray hairline strokes.
2. **Hard Unblurred Offset Shadows:** Surfaces cast sharp, 0-blur directional drop shadows (`4px 4px 0 #121212` for controls, `6px 6px 0 #121212` to `8px 8px 0 #121212` for cards). A soft blurred shadow is a direct failure.
3. **Mechanical Press Collapse:** On `:active` or click, interactive buttons physically depress along the shadow axis (`transform: translate(2px, 2px); box-shadow: 2px 2px 0 #121212;`), providing unmistakable tactile mechanical feedback.
4. **Vibrant Intentional Color Blocking:** A balanced high-contrast palette: 1 canvas base + 1 stark ink color + 1–2 purposeful saturated accents used for primary actions and semantic grouping.
5. **Bold Asymmetric Typographic Structure:** Confident grotesk or geometric typography with tight line heights and clear contrast between massive display headlines and readable body text.

**First-viewport test:** In a desktop screenshot, identify the thick black outlines, the hard 0-blur offset shadows, and the tactile button states **without reading the page title**. If it looks like a standard flat SaaS layout, revise the border and shadow tokens before proceeding.

## Explicit neo-brutalist hard-shadow exception — shadows are allowed to be sharp

**Neo-brutalism-specific override:** The universal anti-slop caution against *excessive decoration or distracting shadows* MUST NOT be interpreted as a ban on hard offset shadows or black outlines here. These are **material-enabling properties**, essential to neo-brutalist physics and visual clarity.

- **Allowed material treatments:** Solid 0-blur offset shadows (`4px 4px 0 #000`), 2–3px black borders, badge rotations (between -2° and +2° for badges only), and high-contrast color pills.
- **Color contrast discipline:** All text placed on vibrant accent backgrounds (yellow, cyan, lime, coral) must be tested against black ink (`#121212`) to exceed WCAG AA (4.5:1). Pure white text is strictly reserved for dark ink fills.
- **Anti-slop interpretation:** Evaluate neo-brutalist elements by **affordance, layout structure, and readability**, not by counting hard shadows. Removing hard offset shadows to satisfy a generic minimal heuristic is a **design regression**.

## Typography and typewriting

Expressive, confident grotesk sans: Space Grotesk, Archivo, Syne, or system sans. Headlines 36–56 px desktop / 28–40 px mobile; weight 700–800. Body text 15–17 px, weight 400–500; line-height 1.45–1.55. Section indexes and metadata can use uppercase tracking (`letter-spacing: 0.05em`). Punchy, human microcopy without hollow slogans.

## Color direction

- **Light Mode (Punchy Pop Light):**
  - **Canvas Base:** Off-white / light cream (`#FFFDF7` or `#F7F5F0`).
  - **Card Background:** Pure white (`#FFFFFF`) or light tinted block.
  - **Ink / Stroke:** Jet black (`#121212`).
  - **Offset Shadows:** Solid black (`4px 4px 0 #121212`).
- **Dark Mode (Dark Pop Contrast):**
  - **Canvas Base:** Deep ink canvas (`#18181B`).
  - **Card Background:** Elevated dark charcoal (`#222227`) or deep slate (`#27272A`).
  - **Ink / Stroke:** Stark white / cream (`#FAFAFA`).
  - **Offset Shadows:** Stark white or vivid accent (`4px 4px 0 #FAFAFA` or `4px 4px 0 var(--taste-neo-accent-primary)`).
- **Primary Accent:** Vivid pop color (e.g. Electric Yellow `#FFE600`, Hot Coral `#FF5757`, or Royal Cobalt `#3B5BFF`).
- **Secondary Accent:** Complementary contrast (e.g. Crisp Mint `#00F0A8` or Lilac Pop `#D8B4FE`).
- **Theme Coupling & Anti-Collision Rule:** In dark mode, borders and offset shadows MUST flip to light/white or bright accents. Leaving black borders and black shadows on a dark canvas causes complete loss of depth and contrast (black on black). All text on vibrant accent backgrounds (yellow, cyan, lime, coral) must be tested against black ink (`#121212`) to exceed WCAG AA (4.5:1). Pure white text is strictly reserved for dark ink fills.

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicator dots, avatars, circular buttons with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent them from squishing into distorted ovals when viewport shrinks down to 320px.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns.
Corners are square or subtly rounded (`0px–8px` max); generous padding (20px–32px on cards); 2px–3px solid borders; 4px–8px hard offset shadows. Spacing uses a firm 8px grid. Layout should feel grounded, punchy, and confident.

## Surfaces, depth, texture

Surfaces are clean, opaque, and solid:
- **Buttons (Raised):** `background: var(--taste-neo-accent); border: 2.5px solid #121212; box-shadow: 4px 4px 0 #121212;`
- **Buttons (Active/Pressed):** `transform: translate(2px, 2px); box-shadow: 2px 2px 0 #121212;`
- **Cards & Panels:** `background: #FFFFFF; border: 2.5px solid #121212; box-shadow: 6px 6px 0 #121212;`
- **Nested Cards / Action Wells (Card-in-Card):** Permissible when encapsulating a distinct semantic boundary, elevated parameter well, or code container (e.g. `background: var(--taste-neo-card-elevated, #FFF9E6); border: 2px solid #121212; box-shadow: 4px 4px 0 #121212;`). Mindless decorative nesting without purpose remains disallowed.
- **Input Fields:** `background: #FFFFFF; border: 2.5px solid #121212; box-shadow: 3px 3px 0 #121212;` (tightens on focus).

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, status indicators, or button prefixes across all UI elements. Use Lucide or clean vector SVGs (16px–24px) with consistent stroke weight (1.5px–2px) and currentColor.
- **Primary Action (CTA):** Bold colored pill/rectangle with hard offset shadow, thick stroke, and tactile click depression.
- **Secondary Action:** White or transparent fill with black border, inverted hover effect (`background: #121212; color: #FFFFFF;`).
- **Form Controls:** Outlined input box with crisp label, distinct focus state with colored offset glow or deepened stroke.
- **Status Badges / Tags:** High-contrast pill with 2px stroke, subtle 2px offset shadow, and short concrete label.
- **Cards & Nested Wells:** Crisp divider lines (`border-bottom: 2px solid #121212`) separating card header, body, and action footer. Nested wells provide distinct contrast boundaries for inner workflows.

## Motion

100–160 ms crisp linear or ease-out transitions. Direct 1–2px displacement on press. Never use long bouncy springs, float loops, or cartoon oscillations.

## Optional Anime.js v4 recipe

- **Motion decision:** Short direct 1–2px button shift with a matching hard-shadow response; never animate giant shadows.
- **Starting duration:** 130ms (0 = immediate); adjust to task and user preference.
- **Avoid:** bounce and endlessly moving stickers.
- **Dependency:** CSS/native by default. Use Anime.js v4 only if the requested interaction justifies it. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Energetic, plainspoken, and direct. Examples: “Start building”, “Get code”, “Copied to clipboard”. Avoid corporate jargon or cutesy meme text in production tools.

## Starter tokens (suggestions, not a complete theme)

| Token | Light mode default | Dark mode default |
| --- | --- | --- |
| `--taste-neo-bg` | `#fffdf7` | `#18181b` |
| `--taste-neo-card-bg` | `#ffffff` | `#222227` |
| `--taste-neo-card-elevated` | `#fff9e6` | `#2b2b32` |
| `--taste-neo-ink` | `#121212` | `#fafafa` |
| `--taste-neo-ink-muted` | `#4b4b4b` | `#a1a1aa` |
| `--taste-neo-border` | `2.5px solid #121212` | `2.5px solid #fafafa` |
| `--taste-neo-shadow-sm` | `3px 3px 0 #121212` | `3px 3px 0 #fafafa` |
| `--taste-neo-shadow-md` | `5px 5px 0 #121212` | `5px 5px 0 #fafafa` |
| `--taste-neo-shadow-lg` | `8px 8px 0 #121212` | `8px 8px 0 #fafafa` |
| `--taste-neo-accent-primary` | `#ffe600` | `#ffe600` |
| `--taste-neo-accent-secondary` | `#ff5757` | `#ff5757` |
| `--taste-neo-radius` | `6px` | `6px` |
| `--taste-neo-font-body` | `Space Grotesk, Archivo, system-ui, sans-serif` | `Space Grotesk, Archivo, system-ui, sans-serif` |
| `--taste-neo-motion-duration` | `130ms` | `130ms` |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-neo-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win. **Style-specific direction:** Make the full viewport energetic through bold asymmetric blocks, well-grounded display typography and one high-contrast primary action. Thick borders and offset shadows remain intentional; do not stack stickers, extra outlined boxes or spinning ornaments to fill the screen. See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.


## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally to prevent bloated UI; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); Verify hard unblurred offset shadows; maintain 2–3px solid borders; test tactile press displacement; verify text contrast against saturated accents (black ink on yellow/cyan/mint); verify dark/light mode switching so borders, offset shadows, and ink invert properly and never disappear into dark grounds.
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean vector SVGs with currentColor); Do not add blur or spread to neo-brutalist shadows; avoid muted low-contrast pastels; do not place pure white text on yellow or mint buttons; do not leave black borders/shadows on dark canvas.
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

**Confident graphic pop, not messy chaos.**

- **Reject:** emojis used as UI icons or button stickers, Blurry shadows, gradient borders, cartoon sticker spam, illegible white text on bright yellow pills, and dark mode theme collisions where black borders disappear against dark canvas.
- **Instead:** Pair crisp solid borders with grounded unblurred offset shadows, clear typographic hierarchy, and intentional theme adaptation.
- **Copy check:** Punchy, human microcopy without hollow corporate slogans.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `neo-brutalism`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
