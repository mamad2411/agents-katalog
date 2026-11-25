---
name: taste-style-minimalism
description: Apply Minimalism design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses  or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as  instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Minimalism

**ID:** `minimalism`  
**Signature:** Purposeful restraint, active intentional negative space, mathematical typography, hairline divider architecture, and high-density operational data cockpits.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. An empty page with low-contrast gray text or an unaligned consumer card template **does not qualify as Minimalism**.

## Good fit / trade-offs

- **Works well for:** High-focus productivity tools, developer consoles, B2B SaaS platforms, operational admin dashboards, cloud infrastructure monitors, fintech/trading portals, focused e-commerce storefronts, personal portfolios, documentation hubs, and form-intensive applications.
- **Be careful with:** Highly ornamental spectacle sites or playful carnival campaign landing pages where visual noise and decorative chaos are the primary objective.
- **Reference directions:**
  - *Calm Industrial White (Studio & Clean Desk):* Warm neutral paper base (`#FAFAF9` or `#FFFFFF`), deep slate typography (`#18181B`), hairline dividers (`rgba(0, 0, 0, 0.08)` or `#E4E4E7`), compact 36px/32px table rows with tabular numbers, and single purposeful primary action.
  - *Disciplined Studio Dark (Cloud Operations Cockpit):* Muted obsidian canvas (`#121214` or `#0F1117`) with crisp porcelain/slate typography (`#F4F4F5`), quiet borders (`rgba(255, 255, 255, 0.09)` or `#232733`), calibrated semantic status tokens (WCAG AA), and high-velocity keyboard affordances (`⌘K`).

## Minimalist material fidelity gate — mandatory

**Before calling a minimalist page complete, the opening viewport must visibly read as a masterclass in purposeful restraint, alignment, and information clarity.** If a user chose this style, "lazy minimalism" (faint gray text, missing labels, hidden controls, or an empty screen with one centered sentence) or consumer dashboard slop (fake KPI cards with zero tabular density) is a direct **FAIL**.

A successful minimalist implementation demonstrates **all** of the following:

1. **Active Proportional Negative Space:** Whitespace is deliberate and calibrated, not accidental empty voids. It frames content purposefully and directs the user's eye directly to key tasks without needing boxes, badges, or arrows.
2. **Mathematically Calibrated Typographic Scale:** Clear contrast between display titles (32px–44px, weight 600–700), section anchors (18px–22px, weight 600), body text (15px–16px, weight 400, line-height 1.6), and metadata/table cells (12px–13px, weight 500 tabular figures).
3. **Razor-Sharp Spatial Alignment & Hairline Dividers:** Grouping is achieved through alignment, proximity, and subtle hairline dividers (`1px solid rgba(0, 0, 0, 0.08)` or `rgba(255, 255, 255, 0.10)`), completely eliminating unnecessary nested floating cards.
4. **Information-Dense Tabular Architecture:** When displaying records or entities, present them in structured, scannable data tables or compact master-detail lists with consistent row heights (32px–40px) and explicit column headers.
5. **Tabular Numerals & Flush Alignment:** All numbers, financial amounts, metrics, and timestamps enforce `font-variant-numeric: tabular-nums`. Numerical columns align strictly flush-right; text columns align flush-left.
6. **Semantic Status Tokens with Legible Contrast:** Status indicators (Healthy, Degraded, Failed, Pending) use calibrated semantic token pills with dark accessible text on soft tinted backgrounds (e.g. Success: `#ECFDF5` background with `#065F46` text, passing WCAG AA 4.5:1).
7. **Productivity Affordances & Shortcuts:** Search bars feature keyboard trigger hints (`⌘K` or `/`), table headers feature sort indicators (`▲/▼`), and multi-select checkboxes trigger contextual batch docks.
8. **Accessible High Contrast (WCAG AA/AAA):** Text, icons, and interactive elements maintain strong contrast against neutral surfaces. Faint unreadable `#999999` text on white is strictly prohibited.
9. **Clear Action Affordances:** Primary interactive controls are immediately discoverable, featuring high-contrast fills, distinct hover states, and visible keyboard focus indicators (`:focus-visible`).

**First-viewport test:** In a desktop screenshot, identify the calm typographic rhythm, effortless reading flow, hairline structural discipline, and unambiguous primary action **without reading the page title**. If essential labels are hidden, text is washed out, or data tables look like bloated consumer cards, restore contrast and structural hierarchy immediately.

## Explicit minimalist restraint & enterprise density exceptions

**Minimalism-specific overrides:**
1. **Restraint override:** The universal anti-slop caution against *empty canvases or under-designed viewports* MUST NOT be interpreted as a mandate to inject decorative badges, floating cards, or illustrations here. In authentic minimalist design (Dieter Rams, Massimo Vignelli), removing non-essential decoration elevates clarity and reduces cognitive load.
2. **Enterprise density override:** The universal anti-slop caution against *dashboard clutter or multiple metric boxes* MUST NOT be interpreted as a mandate to hide data tables, filter toolbars, or operational status indicators. In authentic software (Stripe, Linear, Datadog), dense scannable tabular data is the primary interface requirement.

- **Allowed treatments:** Generous active negative space, subtle hairline dividers, unembellished typography, single-accent links, compact data tables (32px–40px rows), filter toolbars, search bars with keyboard shortcut badges, batch action bars, and semantic status pills.
- **Anti-slop boundary:** Never hide core navigation, delete labels, or sacrifice accessibility in the name of "clean aesthetics". Never invent fake revenue metrics, decorative mini-sparklines without axis scales, or animated pie charts that convey zero operational data.
- **Anti-slop interpretation:** Evaluate layouts by **clarity of task, ease of reading, and information density**, not by demanding ornamental fills. Purposeful white space paired with dense tabular utility is authentic design.

## Typography and typewriting

Pure, neutral UI sans: Inter, Source Sans 3, SF Pro, or system sans paired with JetBrains Mono for code, identifiers, and tabular figures. Headlines: 32–44 px (weight 600–700, `letter-spacing: -0.025em`); section titles: 18–22 px (weight 600); body: 15–16 px (weight 400, line-height 1.6); table cells: 13–14 px (line-height 1.45); captions/metadata: 12–13 px (weight 500 monospace, tabular numbers). Calm, scannable type scale with golden-ratio line heights.

## Color direction

- **Light Mode (Clean Studio Light & Console):**
  - **Canvas Base:** Soft paper white (`#FAFAF9` or `#FFFFFF`).
  - **Surface / Table:** Pure white (`#FFFFFF`).
  - **Primary Ink / Typography:** Deep slate black (`#18181B`).
  - **Secondary Text:** Balanced neutral slate (`#52525B` — passes 4.5:1 WCAG AA).
  - **Hairline Divider:** Translucent gray (`rgba(0, 0, 0, 0.08)` or `#E4E4E7`).
  - **Hover Row Highlight:** `#F8FAFC`.
- **Dark Mode (Disciplined Studio Dark & Cloud Cockpit):**
  - **Canvas Base:** Muted obsidian canvas (`#121214` or `#0F1117`).
  - **Surface / Table:** Dense slate obsidian (`#18181B` / `#161922`).
  - **Primary Ink / Typography:** Crisp porcelain (`#F4F4F5` / `#F9FAFB`).
  - **Secondary Text:** Balanced slate (`#A1A1AA` — passes 4.5:1 WCAG AA).
  - **Hairline Divider:** Translucent white (`rgba(255, 255, 255, 0.09)` or `#232733`).
  - **Hover Row Highlight:** `#1F2430`.
- **Brand Accent:** Singular functional accent (e.g. high-contrast ink anchor `#18181B` light / `#F4F4F5` dark, or calibrated Enterprise Cobalt `#2563EB` light / `#3B82F6` dark).
- **Semantic Status Tokens (WCAG AA Calibrated for Both Modes):**
  - **Success (Healthy / Active):** Light: `#065F46` on `#ECFDF5` (border `#A7F3D0`); Dark: `#34D399` on `rgba(16, 185, 129, 0.15)` (border `rgba(16, 185, 129, 0.35)`).
  - **Warning (Degraded):** Light: `#92400E` on `#FEF3C7` (border `#FDE68A`); Dark: `#FBBF24` on `rgba(245, 158, 11, 0.15)` (border `rgba(245, 158, 11, 0.35)`).
  - **Error (Failed):** Light: `#991B1B` on `#FEE2E2` (border `#FECACA`); Dark: `#F87171` on `rgba(239, 68, 68, 0.15)` (border `rgba(239, 68, 68, 0.35)`).
  - **Neutral (Pending / Inactive):** Light: `#374151` on `#F3F4F6` (border `#E5E7EB`); Dark: `#9CA3AF` on `rgba(156, 163, 175, 0.12)` (border `rgba(156, 163, 175, 0.25)`).
- **Theme Coupling Rule:** Canvas, typography, secondary text, table rows, and status badges MUST flip synchronously. When user requests dark mode, text must turn light (`#F4F4F5`); when light mode, text must turn dark (`#18181B`). Never leave dark text on dark canvas.

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicator dots, avatars, circular buttons with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent them from squishing into distorted ovals when viewport shrinks down to 320px.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns.
- Consistent 4px/8px spacing grid; gentle, unified corner radii (`6px–8px`); consistent table row heights (36px default, 32px compact); subtle hairline borders where structural separation is necessary. Negative space groups related information naturally.

## Surfaces, depth, texture

Surfaces are quiet, flat, and matte. Minimal or zero box-shadows (`0 1px 3px rgba(0, 0, 0, 0.05)` max for elevated dropdowns). Depth is communicated via contrast, spacing, hairline borders, and typographic weight.

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, status indicators, or button prefixes across all UI elements. Use Lucide or clean vector SVGs (16px–24px) with consistent stroke weight (1.5px–2px) and currentColor.
- **Hairline Navigation Header:** Fixed or sticky top bar with subtle hairline dividing stroke (`1px solid rgba(0, 0, 0, 0.08)`), brand mark, horizontal link row on desktop, and symmetric 36px action controls. On mobile viewports (< 768px), links collapse into an accessible hamburger button with 44px+ tap target drawer.
- **Primary Action (CTA):** Solid dark pill or rounded rectangle (`border-radius: 6px`) with high contrast fill, distinct hover state, and zero visual blur noise.
- **Secondary Action:** Unadorned text link or subtle outline button with hairline border (`1px solid var(--pow-border)`).
- **Restrained Form Input:** Clean input field with visible hairline border, clear placeholder, and high-contrast focus ring (`outline: 2px solid var(--pow-accent); outline-offset: 2px;`).
- **Dense Data Table:** Sticky header row, hover row highlighting (`#F8FAFC` light / `#1F2430` dark), flush-right numerical columns with `font-variant-numeric: tabular-nums`, flush-left text, and multi-select row checkboxes.
- **HUD Telemetry Strip:** Compact operational metric headers pairing high-contrast tabular values with subtle progress or health ratios. Every KPI or meter must display an explicit operational denominator, time horizon, or threshold baseline (e.g. `84.2% (101/120 Nodes Active)`, `1.42M ops/sec`). Zero giant consumer vanity cards.
- **Floating Batch Action Dock:** Contextual bottom action bar triggered dynamically when 1 or more rows are selected via checkboxes, allowing high-velocity batch interventions without losing filter context.
- **Slide-Over Detail Inspector Drawer:** Lateral drawer or master-detail split pane for deep telemetry inspection, node diagnostics, and raw JSON configurations without losing table scroll position or active search filters.
- **Minimalist Toggle Switch:** Pill-shaped track with smooth sliding circular knob enforcing `aspect-ratio: 1 / 1; flex-shrink: 0;` (never deforms into an oval).
- **Segmented Control Tabs:** Flush inline segmented pill bar (`border-radius: 4px`) for density, scale, or view switching.
- **Mathematical 4-Metric Grid:** Box grid separated by 1px hairline rules without individual floating card shadows.

## Motion

100–140 ms quiet ease-out transitions for opacity, background color, or subtle border color. Zero gratuitous movement; animations should be felt, not watched. Prioritize rock-solid stability during data refreshing or table filtering.

## Optional Anime.js v4 recipe

- **Motion decision:** Subtle opacity fade or gentle micro-transition on active state; keep motion minimal.
- **Starting duration:** 120ms (0 = immediate); adjust to task and user preference.
- **Avoid:** bouncing, sliding reveals, floating loops, staggered table rows.
- **Dependency:** CSS/native by default. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Calm, concise, and helpful. Examples: “Save changes”, “Account settings”, “3 files selected”, “12 nodes healthy”. Avoid marketing superlatives or enthusiastic exclamation marks.

## Starter tokens (suggestions, not a complete theme)

| Token | Light mode default | Dark mode default | Architectural Role |
| --- | --- | --- | --- |
| `--taste-mini-bg` | `#fafaf9` | `#121214` | Base canvas backdrop base |
| `--taste-mini-surface` | `#ffffff` | `#18181b` | Elevated surface / table fill |
| `--taste-mini-ink` | `#18181b` | `#f4f4f5` | Primary typography & vector icons (WCAG AAA) |
| `--taste-mini-muted` | `#52525b` | `#a1a1aa` | Secondary metadata text (4.5:1+) |
| `--taste-mini-border` | `1px solid rgba(0, 0, 0, 0.08)` | `1px solid rgba(255, 255, 255, 0.09)` | Subtle structural hairline dividing rule |
| `--taste-mini-accent` | `#18181b` | `#f4f4f5` | Primary functional action fill |
| `--taste-mini-blue` | `#2563eb` | `#3b82f6` | Operational focus & interactive links |
| `--taste-mini-radius` | `6px` | `6px` | Gentle unified corner radius |
| `--taste-mini-font-sans` | `Inter, system-ui, sans-serif` | `Inter, system-ui, sans-serif` | Pure unembellished typography stack |
| `--taste-mini-font-mono` | `JetBrains Mono, monospace` | `JetBrains Mono, monospace` | Tabular metadata and monospace code font |
| `--taste-mini-space-unit` | `4px / 8px` | `4px / 8px` | Mathematical grid rhythm base |
| `--taste-mini-motion-duration` | `120ms` | `120ms` | Subtle ease-out micro-transition timing |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-mini-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win. **Style-specific direction:** Compose the first viewport around a crystal-clear headline, one primary action, and generous, intentional white space or a high-density operational telemetry monitor. Do not invent filler cards, fake testimonials, or decorative badges to clutter the canvas. See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.

## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally to prevent bloated UI; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); verify high text contrast (WCAG AA 4.5:1) in both light and dark modes; ensure interactive controls have clear hit targets and visible focus indicators; group content through spacing and hairline dividers; verify that mode switching flips canvas, ink, muted text, and borders in paired synchronization; ensure data tables use `tabular-nums` and flush right numeric alignment.
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean vector SVGs with currentColor); do not treat washed-out gray text or missing labels as minimalism; avoid hiding core actions behind obscure icons; do not create vast empty voids that confuse navigation; avoid dark/light theme collisions where text remains dark on dark canvas; never display fake consumer metrics without denominators.
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

**Clarity through restraint and truthful data density, not lazy emptiness or dashboard slop.**

- **Reject:** emojis used as UI icons or button stickers, faint low-contrast gray text, unlabelled icon-only controls, ghost buttons that look disabled, empty viewports that communicate zero product information, consumer dashboard templates with decorative mini-sparklines or fake KPI cards lacking denominators, and theme collisions where text is unreadable against the canvas.
- **Instead:** Combine ample breathing room with high-contrast type hierarchy, structured hairline data tables with tabular numerals, clear semantic status badges, and robust dark/light theme support.
- **Copy check:** Every word must serve a clear purpose; remove filler and marketing hype copy.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `minimalism`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
