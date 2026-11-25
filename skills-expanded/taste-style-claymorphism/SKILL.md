---
name: taste-style-claymorphism
description: Apply Claymorphism design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses  or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as  instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Claymorphism

**ID:** `claymorphism`  
**Signature:** Molded, tactile, sculpted surfaces with dual inner-shadow volumetric depth, soft ambient drop shadows, and friendly physical presence.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. A flat card with rounded corners and a 1px border **does not qualify as Claymorphism**.

## Good fit / trade-offs

- **Works well for:** Playful consumer experiences, creative tools, personal dashboards, interactive widgets, tactile web apps, and modern educational or design platforms.
- **Be careful with:** Extremely dense tabular data, long-form legal reading, or low-power devices if excessive shadow calculations obstruct performance.
- **Reference directions:**
  - *Primary Saturated Clay:* Rich, vibrant violet/purple (`#813FFC`) molded surfaces with bright white inner highlights on the upper-left, deep tinted form shadows on the bottom-right, and crisp typography.
  - *Light Porcelain Clay:* Soft off-white (`#ECEBF5`) molded surfaces with pure white top-left inner highlights, soft gray-lavender bottom-right form shadows, and dark slate-purple typography.
  - *Sunken Inset Wells:* Recessed form inputs with a crisp white relief rim (`3px solid rgba(255, 255, 255, 0.85)`), inverted inset shadows, and accessible placeholder labels.

## Clay material fidelity gate — mandatory

**Before calling a claymorphism page complete, the opening viewport must visibly read as a sculpted clay composition.** If a user chose this style, a flat card with rounded corners and a 1px border is a **FAIL**, even if CSS variables are named `clay`.

A successful claymorphism implementation demonstrates **all** of the following:

1. **Volumetric Dual Inner Shadows (Highlight + Shadow):** A clay surface MUST feature opposing dual inner shadows: an upper-left inner highlight simulating incident light (`inset 3px 4px 6px rgba(255,255,255,...)`) and a lower-right inner form shadow simulating volumetric thickness (`inset -4px -6px 8px rgba(dark-tint,...)`). A single flat highlight line or generic bevel fails.
2. **Soft Tinted Ambient Drop Shadows:** Surfaces cast soft, directional, tinted drop shadows (`8px 16px 24px rgba(..., 0.20–0.35)`), creating the sensation of pliable material floating or resting above a tinted canvas, rather than harsh black drop shadows.
3. **Plush Squircle and Pill Geometry:** Generous curvature (`24px–32px` cards, `20px–26px` buttons, `9999px` pills or circles, `14px` squircle checkboxes). Sharp 90-degree corners fail.
4. **Sunken vs Raised Polarity:** Actionable components (buttons, badges, toggle thumbs, cards) are raised outward; containment wells (input fields, inactive switch channels) are recessed inward with reversed inset shadows and an optional white relief rim.
5. **Tactile Compression on Interaction:** On hover, focus, and click, controls respond physically with subtle scale down (`scale(0.97–0.98)` or `translateY(1–2px)`) and tightened shadows, feeling like real, pliable clay pressed by a finger.
6. **Multi-Surface Clay Composition Architecture:** Complex layouts (workspaces, dashboards, creative tools) must balance a saturated or pastel clay accent dock/panel (e.g. sidebar navigation with plush active white porcelain pills) with clean light porcelain card surfaces. This establishes visual hierarchy without burying the entire viewport in uniform monochrome candy.
7. **3D Cylindrical Bar & Donut Visualizations:** When data or charts are present, render metrics using tactile 3D rounded cylinders (pill-capped vertical bars with dual inner shadows inside recessed tracking grooves) or plump, segmented clay donut rings. Never use razor-thin 1px wireframe charts that conflict with the pliable clay physics.
8. **Plump Squircle Metric Compartments:** Metric cards must structure data with dedicated squircle icon bays (`12px–16px` border-radius with dual inner shadows and pastel color coding), prominent bold numeric typography, and soft tinted pill delta tags (`9999px` radius).
9. **Sunken Well Track & Extruded Pill Segmented Controls (Tabs / Filters):** Tab headers, segmented mode selectors, and filter strips must never be flat text with 1px border lines. They must use a continuous sunken well channel (`border-radius: 9999px; box-shadow: var(--taste-clay-inner-well);`) containing tactile pill buttons, where the active option is physically extruded outward as a raised 3D clay pill with dual inner highlights and soft ambient drop shadow.
10. **Pillow & Well Disclosure Architecture (Accordions / FAQs):** Expandable panels, disclosure widgets, and accordion items must pair a raised tactile clay pillow trigger (`24px–28px` radius) with an interior recessed sunken well channel (`18px–22px` radius) for the revealed body. The toggle indicator is a circular 3D clay sphere/button inside a sunken well bay that rotates smoothly upon opening.
11. **Sculpted Console & Code Pod Architecture:** Monospace code blocks, terminal previews, or telemetry boxes must not be rendered as flat black developer rectangles. They must be sculpted matte clay console pods (`24px–28px` radius) with recessed volumetric inset shadows (`inset 3px 4px 8px`), subtle relief borders, tactile 3D pastel control dots, and tactile clay pill action buttons.

**First-viewport test:** In a desktop screenshot, identify the raised sculpted buttons, the dual inner highlights/shadows, and the recessed input wells **without reading the page title**. If they appear flat or merely rounded, revise the shadow tokens before adding more content.

**Not a card-count rule:** A focused component showcase (e.g. primary "Submit" pill, secondary "Go Back" pill, circular action button, tactile toggle switch, checkbox, and sunken input field) is sufficient to establish authentic material fidelity without blanketing the entire screen in nested balloon cards.

## Explicit clay depth exception — clay is allowed to have volumetric depth

**Claymorphism-specific override:** The universal anti-slop caution against *excessive shadows, glossy effects, or neumorphic blur* MUST NOT be interpreted as a ban on dual inner shadows, soft ambient drop shadows, or white relief outlines here. These are **material-enabling properties**, essential for tactile physical presence.

- **Allowed material treatments:** Dual inner shadows (opposing light/dark), soft multi-stop tinted ambient shadows, white relief borders (`3px solid rgba(255,255,255,0.85)`), and tactile press transforms (`scale(0.97)`). These create essential tactile depth and physical presence. Static CSS delivers complete material fidelity with zero animation library overhead.
- **Color contrast discipline:** Saturated primary clay buttons require pure white text (`#FFFFFF`) with at least 4.5:1 contrast. Light porcelain clay surfaces require deep dark text (`#28233D` or `#1D1735`). Sunken wells require clear, accessible placeholder text (`#7C739E` or darker).
- **Anti-slop interpretation:** Evaluate clay depth by **material purpose, physical coherence, and readability**, not by counting CSS shadow declarations. Removing dual inner shadows to satisfy a generic minimal heuristic is a **design regression**.

See `examples/claymorphism/sculpted-surfaces.css` for starter implementation and `tests/claymorphism-visual.md` for visual acceptance criteria.

## Typography and typewriting

Friendly humanist or geometric sans: Manrope, Nunito Sans, or system sans. Weights 500/600/700 for labels, 700/800 for headings. Scale 14/16/20/26/34 px; line height 1.45–1.6. Prefer sentence case and concise, human labels. Avoid thin display fonts that look fragile over volumetric surfaces.

## Color direction

Choose a cohesive pastel-and-saturated palette:

- **Light Mode (Light Porcelain Clay):**
  - **Canvas Base:** Soft pastel lilac / lavender (`#D7D1F1` or `--taste-clay-bg: #d7d1f1`).
  - **Primary Saturated Clay:** Vibrant violet/purple (`#813FFC`) with white text (`#FFFFFF`), bright top-left white highlight, and deep purple bottom-right form shadow.
  - **Secondary Light Clay:** Soft off-white porcelain (`#ECEBF5` / `#F0EFF7`) with dark ink (`#28233D`), bright top-left highlight, and soft lavender bottom-right form shadow.
  - **Sunken Input Wells:** Canvas-tinted well (`#D7D1F1`) framed by a crisp white relief rim (`3px solid rgba(255, 255, 255, 0.85)`), recessed inset shadow, and legible placeholder (`#8F87B0`).
- **Dark Mode (Deep Night Sculpted Clay):**
  - **Canvas Base:** Moody obsidian-indigo (`#161326`).
  - **Primary Saturated Clay:** Vibrant violet/purple (`#813FFC`) with pure white text (`#FFFFFF`), top-left highlight, and dark violet form shadow.
  - **Secondary Clay Surface:** Rich sculpted plum/slate (`#26203D`) with crisp pale porcelain text (`#F3F0FA`), soft translucent top-left highlight (`rgba(255, 255, 255, 0.15)`), and deep black bottom-right form shadow (`rgba(10, 5, 25, 0.60)`).
  - **Sunken Input Wells:** Deep recessed well (`#1E1A33`) framed by a subtle relief rim (`3px solid rgba(255, 255, 255, 0.20)`), recessed inset shadow, and legible placeholder (`#A49BBF`).
- **Theme Contrast Coupling:** When switching to dark mode, text on secondary clay surfaces MUST flip from dark ink (`#28233D`) to pale porcelain (`#F3F0FA`). Leaving dark ink text on dark clay creates an immediate contrast failure. Saturated primary buttons retain pure white text (`#FFFFFF`) with 4.5:1+ contrast in both modes.

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicator dots, avatars, circular buttons with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent them from squishing into distorted ovals when viewport shrinks down to 320px.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns.
Radius 24–32 px cards, 20–26 px buttons, 9999px full pills or circles, 14–16 px squircle badges and checkboxes. Maintain consistent 8 px rhythm and comfortable gutters. Avoid random circles that have no semantic interaction.

## Surfaces, depth, texture

Surfaces must feel molded from physical matte clay:
- **Primary Clay (Raised):**
  `box-shadow: inset 3px 4px 6px rgba(255, 255, 255, 0.45), inset -4px -6px 8px rgba(40, 10, 110, 0.40), 8px 16px 24px rgba(100, 45, 210, 0.35), 2px 4px 8px rgba(70, 20, 150, 0.20);`
- **Light Porcelain Clay (Raised):**
  `box-shadow: inset 3px 4px 6px rgba(255, 255, 255, 0.95), inset -4px -6px 8px rgba(145, 135, 180, 0.35), 8px 16px 24px rgba(110, 95, 160, 0.20), 2px 4px 8px rgba(110, 95, 160, 0.12);`
- **Sunken Wells (Recessed):**
  `box-shadow: inset 3px 4px 8px rgba(110, 95, 165, 0.25), inset -2px -2px 6px rgba(255, 255, 255, 0.70);`
  Framed with `border: 3px solid rgba(255, 255, 255, 0.85);`

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, status indicators, or button prefixes across all UI elements. Use Lucide or clean vector SVGs (16px–24px) with consistent stroke weight (1.5px–2px) and currentColor.
- **Primary Button ("Submit >"):** Saturated purple pill, white bold text, directional chevron, tactile compression on click.
- **Secondary Button ("Go Back ↶"):** Light porcelain pill, dark ink text, return arrow icon, tactile compression on click.
- **Circular Action Button:** 50% border-radius round button (e.g. pause `❚❚`), saturated clay, centered icon.
- **Toggle Switch:** Pill-shaped track with smooth clay thumb sphere; toggles between light track/purple thumb and purple track/white thumb.
- **Checkbox:** Squircle container with dual inner shadow and vibrant purple checkmark (`✓`).
- **Input Field:** Sunken well with left icon, legible placeholder, and white relief rim border.
- **Cellular / Pill Navigation Bar:** Full-width header or sidebar dock divided into plush rounded pill bays (`9999px`), with the active route elevated as an extruded porcelain clay pill with soft dual inner shadows.
- **Sunken Well Tab Track:** Continuous pill-shaped inset channel (`border-radius: 9999px`) hosting tactile clay tabs, with the active route physically extruded outward as a raised 3D clay pill.
- **Tactile Clay Pillow Accordion:** Raised clay trigger capsule (`24px–28px` radius) paired with a circular 3D toggle sphere and an interior recessed sunken well channel for the revealed text.
- **Sculpted Console Pod:** Deep matte clay enclosure (`24px–28px` radius) with recessed inset shadows, 3D pastel window dots, and tactile copy pill.
- **3D Cylindrical Bar Chart:** Recessed sunken well tracks with vertical rounded 3D pill cylinders inside, featuring dual inner highlight and form shadow.
- **Tactile Segmented Donut Chart:** Plump, rounded circular arc segments with tactile drop shadow and soft pastel color coding.
- **3D Clay Color Pebble:** Squircle/pill-shaped swatch button demonstrating physical color with dual specular and form shadows.

## Motion

140–200 ms smooth ease-out. Tactile compression (`scale(0.97)` or `translateY(2px)`) with shadow tightening on press. Never bounce, overshoot, or run continuous floating loops.

## Optional Anime.js v4 recipe

- **Motion decision:** Pressed button with 1–2% compression and a brief return; keep existing sculpted shading.
- **Starting duration:** 180ms (0 = immediate); adjust to task and user preference.
- **Avoid:** bounce, overshoot, floating loops.
- **Dependency:** CSS/native by default. Use Anime.js v4 only if the requested interaction justifies it. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Warm and concrete. Examples: “Submit”, “Go Back”, “Enter your Username”, “Saved to drafts”. Avoid sugary AI slogans or fake marketing hype.

## Starter tokens (suggestions, not a complete theme)

| Token | Light mode default | Dark mode default |
| --- | --- | --- |
| `--taste-clay-bg` | `#d7d1f1` | `#161326` |
| `--taste-clay-primary` | `#813ffc` | `#813ffc` |
| `--taste-clay-light` | `#ecebf5` | `#26203d` |
| `--taste-clay-text` | `#28233d` | `#f3f0fa` |
| `--taste-clay-muted` | `#7c739e` | `#a49bbf` |
| `--taste-clay-shadow-primary` | `8px 16px 24px rgba(100, 45, 210, 0.35), 2px 4px 8px rgba(70, 20, 150, 0.20)` | `8px 16px 24px rgba(10, 5, 25, 0.50), 2px 4px 8px rgba(10, 5, 25, 0.30)` |
| `--taste-clay-inner-primary` | `inset 3px 4px 6px rgba(255, 255, 255, 0.45), inset -4px -6px 8px rgba(40, 10, 110, 0.40)` | `inset 3px 4px 6px rgba(255, 255, 255, 0.45), inset -4px -6px 8px rgba(40, 10, 110, 0.50)` |
| `--taste-clay-shadow-light` | `8px 16px 24px rgba(110, 95, 160, 0.20), 2px 4px 8px rgba(110, 95, 160, 0.12)` | `8px 16px 24px rgba(0, 0, 0, 0.45), 2px 4px 8px rgba(0, 0, 0, 0.25)` |
| `--taste-clay-inner-light` | `inset 3px 4px 6px rgba(255, 255, 255, 0.95), inset -4px -6px 8px rgba(145, 135, 180, 0.35)` | `inset 3px 4px 6px rgba(255, 255, 255, 0.15), inset -4px -6px 8px rgba(10, 5, 25, 0.60)` |
| `--taste-clay-inner-well` | `inset 3px 4px 8px rgba(110, 95, 165, 0.25), inset -2px -2px 6px rgba(255, 255, 255, 0.70)` | `inset 3px 4px 8px rgba(0, 0, 0, 0.50), inset -2px -2px 6px rgba(255, 255, 255, 0.15)` |
| `--taste-clay-well-rim` | `3px solid rgba(255, 255, 255, 0.85)` | `3px solid rgba(255, 255, 255, 0.20)` |
| `--taste-clay-radius-pill` | `9999px` | `9999px` |
| `--taste-clay-radius-btn` | `24px` | `24px` |
| `--taste-clay-radius-card` | `28px` | `28px` |
| `--taste-clay-radius-squircle` | `14px` | `14px` |
| `--taste-font-body` | `Manrope, system-ui, sans-serif` | `Manrope, system-ui, sans-serif` |
| `--taste-motion-duration` | `180ms` | `180ms` |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-clay-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win. **Style-specific direction:** Use one sculpted hero surface or a carefully balanced soft-material environment; place the true portfolio introduction and CTA in the first-screen composition. Do not nest puffy cards to fill 100svh. Clay depth should remain subtle and directional, with substantial flat space. See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.


## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally to prevent bloated UI; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); Ensure tactile dual inner shadows are visible; maintain consistent light direction (top-left to bottom-right); provide tactile active/press states; verify WCAG AA contrast on both primary and light clay; verify dark/light mode switching so text and surface colors adapt in coupled pairs (e.g. pale porcelain text on dark clay, dark ink text on light clay).
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean vector SVGs with currentColor); Do not treat simple rounded corners as clay; avoid balloon shadows, excessive glossy halos, unreadable light-on-light labels, ornamental badges, and dark/light mode collisions where dark text remains on dark clay.
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

**Soft material, not toy inflation.**

- **Reject:** emojis used as UI icons or button stickers, Reject puffy balloon cards, donut shadow halos, glow borders, nested elevated shells, repeating decorative status pills, and dark/light theme collisions (such as leaving dark purple text on dark plum clay surfaces); make flat/raised/inset states distinct and consistent with one light direction.
- **Instead:** Use one owning sculpted panel with spacing/dividers for internal content; reserve inset wells for real controls or containment.
- **Copy check:** Keep copy calm and concrete rather than cutesy AI encouragement.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `claymorphism`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
