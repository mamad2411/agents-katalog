---
name: taste-style-retro-terminal
description: Apply Retro Terminal design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses  or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as  instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Retro Terminal

**ID:** `retro-terminal`  
**Signature:** Authentic CRT developer-console visual language, phosphor glow, monospace tabular structure, and modern keyboard-driven utility.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. A plain black page with unstyled green text **does not qualify as Retro Terminal**.

## Good fit / trade-offs

- **Works well for:** Developer portfolios, CLI cloud dashboards, cybersecurity and devops tools, system monitoring consoles, and creative coding experiences.
- **Be careful with:** Non-technical consumer audiences who may find strict monospace data layouts or terminal metaphors unfamiliar.
- **Reference directions:**
  - *Classic Amber CRT:* Obsidian black background (`#0C0D0E`) with warm phosphor amber (`#FFB000`), subtle raster scanlines, and high-contrast cream labels.
  - *Phosphor Matrix Green:* Deep graphite canvas (`#0A0F0D`) with electric phosphor green (`#33FF33`), bracketed window titles, and crisp log streams.
  - *Cyberdeck Cyan:* High-tech terminal with luminous cyan (`#00F0FF`), crisp box-drawing borders (`┌─┐`), and keyboard shortcut tags (`[ESC]`).

## Retro terminal fidelity gate — mandatory

**Before calling a retro-terminal page complete, the opening viewport must visibly read as a real, working terminal console or command deck.** If a user chose this style, an ordinary dark website with monospace font is a **FAIL**, even if CSS classes contain `terminal`.

A successful retro-terminal implementation demonstrates **all** of the following:

1. **Phosphor Glow & High-Contrast Luminance:** Text and active indicators exhibit subtle phosphor radiation (`text-shadow: 0 0 6px currentColor`), with primary output passing WCAG AA contrast against obsidian grounds.
2. **Subtle CRT Raster Scanline Overlay:** Surfaces feature a controlled, static horizontal scanline pattern (`repeating-linear-gradient(0deg, rgba(0,0,0,0.15) 0px, transparent 2px)`) that adds genuine display depth without impairing character legibility.
3. **Structured ASCII / Bracketed Layout Framing:** Window headers, panel frames, and status bars use crisp 1px rules, ASCII box characters (`┌─┐`), or bracketed badges (`[SYS_OK]`, `[MODE: CLI]`).
4. **Authentic Command Prompt & Caret:** Interfaces feature an active shell prompt line (`visitor@terminal:~$`) with a solid block caret (`█`) and distinct command history styling.
5. **Monospace Tabular Alignment:** Content aligns strictly along monospace character columns for timestamps, status codes, process IDs, and data readouts.

**First-viewport test:** In a desktop screenshot, identify the terminal prompt, phosphor glow, scanline raster, and bracketed console frames **without reading the page title**. If it looks like a generic dark blog, add the scanline overlay and terminal prompt structure.

## Explicit retro-terminal scanline exception — phosphor glow is allowed

**Retro-terminal-specific override:** The universal anti-slop caution against *decorative overlays or screen textures* MUST NOT be interpreted as a ban on subtle scanlines, phosphor glow, or shell prompt lines here. These are **material-enabling properties**, essential to the CRT console aesthetic.

- **Allowed material treatments:** Monospace box-drawing borders, phosphor text glow (`0 0 6px`), static scanline raster overlays, bracketed status pills, and blinking/solid block carets.
- **Anti-slop boundary:** Every command line or action must be usable. Do not flood screens with unreadable falling matrix characters, fake terminal boot errors, or static decorative code snippets masquerading as a functional UI.
- **Anti-slop interpretation:** Evaluate terminal elements by **command clarity, legibility, and developer productivity**, not by banning monospace frames. Removing scanlines and prompt lines to satisfy a generic flat heuristic is a **design regression**.

## Typography and typewriting

High-legibility monospace: JetBrains Mono, IBM Plex Mono, Fira Code, or system monospace (`ui-monospace, monospace`). Primary body: 14–15 px; headings: 20–32 px with bold weight (700) and uppercase bracketed styling (`### [SYSTEM_OVERVIEW]`). Maintain strict character grid alignment.

## Color direction

- **Dark Mode (Obsidian CRT Phosphor):**
  - **Canvas Base:** Obsidian black (`#0C0D0E` or `#080A08`).
  - **Surface Panels:** Deep slate-charcoal (`#14171A` or `#111613`).
  - **Phosphor Accent (Choose One):**
    - Classic Amber: `#FFB000` (glow: `rgba(255, 176, 0, 0.45)`)
    - Phosphor Green: `#33FF33` (glow: `rgba(51, 255, 51, 0.45)`)
    - Cyber Cyan: `#00F0FF` (glow: `rgba(0, 240, 255, 0.45)`)
  - **Borders:** `1px solid rgba(255, 176, 0, 0.25)` or `#2A2F35`.
  - **Scanlines:** Translucent dark raster lines (`repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0px, transparent 2px)`).
- **Light Mode (Vintage Parchment Teletype):**
  - **Canvas Base:** Warm paper ivory (`#F4F1EA`).
  - **Surface Panels:** Warm oatmeal (`#E8E4DA`).
  - **Phosphor Inversion (Choose One):**
    - Dark Burnt Amber: `#5C3A00`
    - Deep Terminal Green: `#0F4D19`
    - Carbon Ink: `#111613`
  - **Borders:** `1px solid #D5D0C3`.
  - **Scanlines:** Subdued or turned off (`none` or subtle paper texture).
- **Semantic Statuses:** Error Red (`#FF5555` dark / `#B91C1C` light), Warning Yellow (`#FFCC00` dark / `#B45309` light), Success Mint (`#50FA7B` dark / `#047857` light).
- **Theme Coupling & Anti-Collision Rule:** In light mode, bright phosphor accents MUST invert to high-contrast carbon/dark amber ink (`#111613` or `#5C3A00`). Putting bright amber `#FFB000` or neon green `#33FF33` on light paper canvas is an immediate contrast collision and strictly prohibited.

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicator dots, avatars, circular buttons with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent them from squishing into distorted ovals when viewport shrinks down to 320px.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns.
Corners are sharp or minimal (`0px–4px`); 1px solid terminal panel borders; tight vertical rhythm (4px/8px monospace line grid). Panels model modular terminal multiplexers (tmux/screen style).

## Surfaces, depth, texture

- **Terminal Screen:** Deep black background with static scanline raster overlay.
- **Console Panel:** 1px solid border (`1px solid rgba(255, 176, 0, 0.3)` or `#2A2F35`) with subtle inset shadow.
- **Nested Sub-Panels / Action Wells (Card-in-Card):** Permissible when encapsulating distinct terminal multiplexer panes, process monitoring wells, or code execution containers (e.g. `background: var(--taste-term-well-bg, #080A0B); border: 1px dashed var(--taste-term-border);`). Mindless decorative nesting without distinct command boundaries remains disallowed.
- **Active Cursor:** Block caret with 1s pulse or solid active state.

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, status indicators, or button prefixes across all UI elements. Use Lucide or clean vector SVGs (16px–24px) with consistent stroke weight (1.5px–2px) and currentColor.
- **Command Line Prompt:** `user@system:~$ command --flag` with functional input and clear return results.
- **Terminal Button / Action:** Outlined bracket button (`[ EXECUTE ]` or `[ CANCEL ]`) with hover color inversion (`background: currentColor; color: #000;`).
- **Data Log Stream:** Tabular rows with timestamp, log level tag, and message.
- **Keyboard Shortcuts:** Bracketed key indicators (`[⌘+K]`, `[ENTER]`) with clear pointer click fallbacks.

## Motion

Immediate state changes by default (0–80 ms). Optional skippable character typing effect for hero intros only. Respect `prefers-reduced-motion` immediately.

## Optional Anime.js v4 recipe

- **Motion decision:** Monospace character typing reveal or terminal scan bar sweep; keep frame rate stable.
- **Starting duration:** 100ms per token block (0 = immediate); adjust to task and user preference.
- **Avoid:** screen jitter, artificial distortion waves, perpetual flickering loops.
- **Dependency:** CSS/native by default. Use Anime.js v4 only if the requested interaction justifies it. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Precise, technical, and command-driven. Examples: `deploy --prod`, `status: healthy`, `4 processes running`. Avoid patronizing marketing chatter.

## Starter tokens (suggestions, not a complete theme)

| Token | Dark mode default | Light mode default |
| --- | --- | --- |
| `--taste-term-bg` | `#0c0d0e` | `#f4f1ea` |
| `--taste-term-surface` | `#14171a` | `#e8e4da` |
| `--taste-term-well-bg` | `#080a0b` | `#ded9cd` |
| `--taste-term-text` | `#ffb000` | `#5c3a00` |
| `--taste-term-text-muted` | `#8a7030` | `#7d6945` |
| `--taste-term-amber` | `#ffb000` | `#5c3a00` |
| `--taste-term-glow` | `0 0 6px rgba(255, 176, 0, 0.45)` | `none` |
| `--taste-term-border` | `1px solid rgba(255, 176, 0, 0.25)` | `1px solid #d5d0c3` |
| `--taste-term-scanline` | `repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0px, transparent 2px)` | `none` |
| `--taste-term-radius` | `2px` | `2px` |
| `--taste-term-font-mono` | `JetBrains Mono, IBM Plex Mono, monospace` | `JetBrains Mono, IBM Plex Mono, monospace` |
| `--taste-term-motion-duration` | `80ms` | `80ms` |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-term-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win. **Style-specific direction:** Construct the first viewport as an authentic interactive console session with welcome ASCII banner, system status summary, and a working prompt line. Do not simulate fake matrix rain or unreadable glitch loops. See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.


## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally to prevent bloated UI; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); Verify high text contrast against canvas (WCAG AA); ensure monospace alignment is preserved; provide click fallbacks for all keyboard shortcuts; test scanline readability; verify dark/light mode switching so phosphor colors invert to high-contrast dark ink on light grounds.
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean vector SVGs with currentColor); Do not treat a plain dark theme as retro-terminal; avoid illegible glitch animations; do not present fake non-interactive console prompts that confuse users; avoid light-mode theme collisions such as neon green or light amber text on parchment.
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

**Authentic CLI environment, not hacker wallpaper.**

- **Reject:** emojis used as UI icons or button stickers, Generic dark cards disguised as terminal, decorative non-functional console prompts, blinding scanline overlays, neon text on light paper backgrounds, and illegible matrix rain loops.
- **Instead:** Provide real monospace hierarchy, working command lines or tabs, structured tabular log readouts, and calibrated dark/light contrast.
- **Copy check:** Use precise technical commands and status descriptors.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `retro-terminal`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
