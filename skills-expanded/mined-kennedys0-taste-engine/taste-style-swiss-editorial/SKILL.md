---
name: taste-style-swiss-editorial
description: Apply Swiss / Editorial design style to user-selected frontend and UI work. Use only when the user explicitly chooses this style. Provides typography, color, layout, components, interactions, motion, copy and quality gates. Do not impose on unrelated work.
license: MIT
metadata:
  version: "0.13.1"
---

Use this skill only after a user explicitly chooses  or a confirmed project configuration specifies it. For unexplained new UI requests, use a style selector such as  instead of deciding the user's taste here. Existing brand, accessibility and user overrides outrank all examples below. The following style guide is not permission to start UI coding before style selection.

# Style pack: Swiss / Editorial

**ID:** `swiss-editorial`  
**Signature:** Rigorous grid-driven typographic hierarchy, stark scale contrast, structural hairline rules, numbered indexes, and intentional negative space.

> This is a **style pack, not a mandatory default**. Load it only after explicit selection or confirmed applicable project style. Project instructions can override individual choices. Preserve accessibility, utility, and brand constraints. Fonts are suggestions, not required dependencies. A plain page with black sans-serif text **does not qualify as Swiss Editorial**.

## Good fit / trade-offs

- **Works well for:** High-end design agencies, architectural publications, editorial portfolios, cultural magazines, annual reports, and luxury product narratives.
- **Be careful with:** Fast-paced transactional operational tools where massive display typography slows down repetitive data entry.
- **Reference directions:**
  - *Classic Zurich International Style:* Crisp paper white background (`#FFFFFF` or `#F7F7F7`), stark jet black typography (`#111111`), 1px structural dividing rules, numbered indexes (`01`, `02`), and a single strike of Swiss Red (`#E3000F` light / `#EF4444` dark).
  - *Modern Editorial Klein Blue:* Ultra-clean monochrome canvas with International Klein Blue (`#002FA7` light / `#3B82F6` dark) as a high-precision focal accent on navigation and primary actions.
  - *Basel Forest Green:* Deep, disciplined Basel Forest Green (`#007A3D` light / `#10B981` dark) for architectural, environmental, or institutional publications.
  - *Monochrome Obsidian / Paper Inversion:* Pure grayscale editorial canvas (`#111111` light / `#F5F5F5` dark) with zero chromatic hue, relying exclusively on structural weight and stark typographic value contrast.

## Swiss editorial fidelity gate — mandatory

**Before calling a swiss-editorial page complete, the opening viewport must visibly read as a rigorous, grid-aligned typographic editorial work.** If a user chose this style, a generic minimal page lacking dramatic scale contrast and structural rules is a **FAIL**.

A successful swiss-editorial implementation demonstrates **all** of the following:

1. **Extreme Typographic Scale Contrast:** A decisive, uncompromised contrast between massive grotesk display headlines (48px–72px desktop / 32px–44px mobile, tight tracking) and disciplined body copy (16px, line-height 1.55), with tracked uppercase section labels (`letter-spacing: 0.08em`).
2. **Structural Horizontal Hairline Rules:** Content sections, column boundaries, and metadata headers are demarcated by clean 1px solid rules (`border-top: 1px solid #111111`), establishing clear visual shelves.
3. **Numbered Section Hierarchy:** Distinct editorial index numbering (`01`, `02`, `03`) placed above or beside primary article blocks, creating scannable visual anchors.
4. **Rigorous Multi-Column Grid Alignment:** Layout conforms strictly to a 12-column desktop grid with generous asymmetrical gutters and margins. Content never floats loosely without grid anchoring.
5. **Monochrome Base + 1 High-Impact Signal Accent:** The layout remains strictly monochrome (black, off-white, paper gray) with exactly one deliberate signal accent (Swiss Red `#E3000F` or Klein Blue `#002FA7`) applied sparingly to active links, index tags, or primary CTAs.

**First-viewport test:** In a desktop screenshot, identify the massive headline scale, the 1px structural dividing rules, the numbered section markers, and the deliberate asymmetric grid **without reading the page title**. If it looks like a standard blog template, elevate the typography scale and grid rules.

## Explicit swiss editorial typographic exception — dramatic scale is required

**Swiss-editorial-specific override:** The universal anti-slop caution against *excessive font sizes or empty space* MUST NOT be interpreted as a ban on large display headlines (48px–72px) or generous whitespace here. In Swiss Typography (Josef Müller-Brockmann, Max Bill), active negative space and bold scale contrast are the primary structural materials, replacing decorative graphics or shadows.

- **Allowed typographic treatments:** Massive display scale (up to 72px), numbered index typography, hairline structural borders, uppercase tracked metadata, and high-impact single-accent links.
- **Anti-slop boundary:** Do not paste random floating pull-quotes without editorial context, fake publication issue numbers, or oversized headlines that crowd out actual readable content.
- **Anti-slop interpretation:** Evaluate swiss layouts by **grid discipline, typographic rhythm, and information clarity**, not by trying to fill every square inch with cards. White space that directs focus is authentic design.

## Typography and typewriting

Objective grotesk sans: Helvetica Neue, Neue Haas Grotesk, Arial, Inter, or system sans. Headlines: clamp(2rem, 6vw, 4.5rem) (32px mobile up to 72px desktop, weight 700–800, `letter-spacing: -0.03em`); subheadings: 24–32 px; body: 16–18 px (line-height 1.55–1.65); index numerals and captions: 12–14 px uppercase (`letter-spacing: 0.08em`).

## Color direction

- **Light Mode (Crisp Gallery White Paper):**
  - **Canvas Base:** Paper white (`#FFFFFF` or warm gallery white `#FBFBFA`).
  - **Ink / Typography:** Deep obsidian black (`#111111`).
  - **Dividing Rules:** Solid hairline stroke (`#111111` or `#D1D5DB`).
  - **Secondary Gray:** Editorial neutral (`#6B7280`).
- **Dark Mode (Dramatic Dark Monolith):**
  - **Canvas Base:** Pitch obsidian canvas (`#0D0D0D`).
  - **Ink / Typography:** Bone-white display typography (`#F5F5F5`).
  - **Dividing Rules:** Translucent white hairline rule (`rgba(255, 255, 255, 0.20)` or `#2A2A2A`).
  - **Secondary Gray:** Stone gray (`#9CA3AF`).
- **Singular Signal Accent:** Exactly one calibrated focal accent chosen from Zurich Signal Red (`#E3000F` / `#EF4444`), International Klein Blue (`#002FA7` / `#3B82F6`), Basel Forest Green (`#007A3D` / `#10B981`), or Monochrome Obsidian (`#111111` / `#F5F5F5`). Applied sparingly to active links, index tags, or primary CTAs.
- **Theme Inversion Rule:** In swiss editorial, dark/light mode is an authoritative typographic polarity flip. In dark mode, canvas is `#0D0D0D` and typography is `#F5F5F5`. Primary buttons invert cleanly (light mode: solid black block with white text; dark mode: solid white block with black text). Black text on dark canvas or white text on white canvas is strictly prohibited.

## Layout and geometry

- **Strict 1:1 circle geometry (anti-oval):** Any circular UI element (status indicator dots, avatars, circular buttons with `border-radius: 50%`) must enforce `aspect-ratio: 1 / 1; flex-shrink: 0;` to prevent them from squishing into distorted ovals when viewport shrinks down to 320px.
- **Responsive baseline:** Adhere to the [responsive baseline](../references/responsive-baseline.md) for 320px minimum viewport safety, fluid mobile typography defaults, and small-viewport navigation patterns.
Corners are razor-sharp (`0px` border-radius by default, up to `2px` max); generous outer margins; strict 12-column grid alignment. Structural 1px horizontal rules frame content blocks.

## Surfaces, depth, texture

Surfaces are completely flat, single-plane, unornamented, and ink-sharp. Zero card-on-card nesting: avoid stacked card containers; structure editorial content directly using grid gutters, typography, and 1px hairline rules. Zero drop shadows (`box-shadow: none`), zero background gradients, zero blur. Depth is communicated purely through typographic scale, weight, and spatial juxtaposition.

## Component anatomy and interaction

- **Iconography — zero emojis:** Emojis are strictly banned as interface icons, status indicators, or button prefixes across all UI elements. Use Lucide or clean vector SVGs (16px–24px) with consistent stroke weight (1.5px–2px) and currentColor.
- **Editorial Primary CTA:** Crisp solid black block with white typography, or clean underlined text link with 2px stroke offset.
- **Numbered Index Tag:** Small uppercase tag: `[ 01 / ARCHITECTURE ]`.
- **Dividing Rule:** `border-top: 1px solid #111111; padding-top: 1.5rem; margin-top: 2rem;`.
- **Tabular Metadata:** Two-column key-value pairs separated by hairline dividers.

## Motion

Minimal, instantaneous, or 120–160 ms clean linear transitions. No spring bounce, no floating parallax. Focus on crisp state changes.

## Optional Anime.js v4 recipe

- **Motion decision:** Clean text opacity fade or horizontal rule expansion on scroll.
- **Starting duration:** 140ms (0 = immediate); adjust to task and user preference.
- **Avoid:** elastic motion, 3D rotations, playful wobbles.
- **Dependency:** CSS/native by default. Use Anime.js v4 only if the requested interaction justifies it. Follow Taste Engine `references/motion-engine.md` when available; standalone skill follows the reduced-motion and no-decorative-loop principles above.

## UI writing and microcopy

Cultured, concise, and articulate. Examples: “Selected Works 2026”, “Index”, “Read Documentation”, “01 / Overview”. Avoid colloquial slang or enthusiastic sales hype.

## Starter tokens (suggestions, not a complete theme)

| Token | Light mode default | Dark mode default |
| --- | --- | --- |
| `--taste-swiss-bg` | `#ffffff` | `#0d0d0d` |
| `--taste-swiss-ink` | `#111111` | `#f5f5f5` |
| `--taste-swiss-accent` | `#e3000f` | `#ef4444` |
| `--taste-swiss-muted` | `#6b7280` | `#9ca3af` |
| `--taste-swiss-rule` | `1px solid #111111` | `1px solid rgba(255, 255, 255, 0.20)` |
| `--taste-swiss-radius` | `0px` | `0px` |
| `--taste-swiss-shadow` | `none` | `none` |
| `--taste-swiss-border` | `1px solid #111111` | `1px solid rgba(255, 255, 255, 0.20)` |
| `--taste-swiss-font-heading` | `'Helvetica Neue', Inter, system-ui, sans-serif` | `'Helvetica Neue', Inter, system-ui, sans-serif` |
| `--taste-swiss-font-body` | `'Helvetica Neue', Inter, system-ui, sans-serif` | `'Helvetica Neue', Inter, system-ui, sans-serif` |
| `--taste-swiss-motion-duration` | `120ms` | `120ms` |

Tokens represent a **direction** and are not copy-paste guaranteed for every palette/platform. Define `--taste-swiss-*` at project level, ensure color contrast, and adapt via theme tokens rather than scattering literal values.

## Hero composition (full first viewport)

**When a public-facing portfolio/landing/homepage has a hero:** use a one-visible-screen header+hero composition. Base height on `min-height: 100svh` with `100vh` fallback, subtracting the **real** header only when it is in normal flow; let the hero expand for accessibility and short mobile screens. Do not apply this to private dashboards or other task screens; direct user overrides win. **Style-specific direction:** Anchor the opening screen with an authoritative, massive display title, clear section numbering, and an asymmetrical grid split between hero narrative and key navigation. Whitespace must feel deliberate and composed, not empty. See the router `references/hero-layout.md` when present. Standalone use follows the same responsive and anti-slop principles.


## Style-specific quality gate

- **Do:** ensure circular elements (status dots, icon badges, round buttons) maintain strict 1:1 aspect ratio with `aspect-ratio: 1 / 1; flex-shrink: 0;` without squishing into ovals; verify responsive fidelity down to 320px viewport with zero horizontal scroll blowout; ensure mobile typography scales down proportionally to prevent bloated UI; verify header navigation collapses into an accessible hamburger menu on narrow screens (< 768px); Verify strict 12-column grid alignment; maintain dramatic headline-to-body scale ratio; ensure 1px hairline rules cleanly separate sections; keep accent color strictly singular; verify dark/light mode switching so typography, canvas, hairline rules, and primary actions flip cleanly without color collisions (minimum 4.5:1 contrast).
- **Don't:** never let circular elements deform into ovals under flexbox compression; never force crowded horizontal navigation links on mobile headers (always use a hamburger menu); avoid bloated mobile font sizes that crowd small screens; never use emojis as UI icons or button prefixes (always use Lucide or clean vector SVGs with currentColor); Do not add drop shadows (`box-shadow: none` strictly required), rounded bubbles, card-on-card container stacking, or decorative gradients; do not clutter whitespace with meaningless badge chips; avoid low-contrast gray text on small labels; do not leave black typography on dark obsidian canvas.
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

**Typographic authority, not generic minimalism.**

- **Reject:** emojis used as UI icons or button stickers, Weak headlines, decorative card wrappers around text, multiple competing accent colors, low-contrast small captions, and theme collisions (such as black typography remaining on a dark editorial canvas).
- **Instead:** Rely on scale contrast, precise column alignment, singular accent signal, and synchronized dark/light polarity inversion.
- **Copy check:** Text must read like an editorial publication—articulate, structured, and intentional.
- **Audit:** Run universal anti-slop purpose, truth, nested-surface, copywriting, responsiveness, accessibility and motion checks **in addition** to this style's quality gate. Do not penalize deliberate, accessible features characteristic of `swiss-editorial`.

## Quality tiers (standalone)

**FLOOR (must pass):** correct and truthful data/state, working critical actions, accessible focus/labels/contrast, usable responsive UI and reduced-motion support. **REFLEX (explain or fix):** generic feature grids, purposeless nested cards, decorative labels/icons, default marketing hype or constant motion. A reflex is allowed when it clearly expresses the chosen style and serves the task. **FINISH:** refinement of alignment, typography rhythm and edge cases. Never treat the selected style itself as a violation. Do not claim browser testing unless actually performed.
