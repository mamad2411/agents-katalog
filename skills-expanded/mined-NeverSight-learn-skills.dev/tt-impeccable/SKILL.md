---
name: tt-impeccable
description: >
  Build, refine, or set up TikTok-native (TUX) interfaces with production-grade quality.
  Use this whenever building any TikTok/TUX UI component or screen, crafting a TikTok-native
  feature, setting up TUX project context, or aligning hard-coded values with official TUX v2
  tokens. Three modes: 'craft' (shape-then-build), 'teach' (project context setup),
  'extract' (token alignment). Trigger for any request involving TikTok design, TUX design
  system, TikTok-style mobile screens, or TT Style web/marketing surfaces — even if the user
  doesn't mention TUX or impeccable by name.
version: 1.1.0
user-invocable: true
argument-hint: "[craft|teach|extract]"
license: Apache 2.0. Based on Anthropic's impeccable skill. See NOTICE.md for attribution.
---

The quality bar is not "it looks mobile and clean." The bar is "a TikTok designer sees the screenshot and says 'that's TikTok' — not 'that's inspired by TikTok.'"

Your role is precise execution of a closed design system, not creative exploration.

---

## Context Gathering Protocol

Design work without TUX project context produces inconsistent output.

1. **Check current instructions** — if a **TUX Design Context** block is loaded, proceed immediately.
2. **Check `.tt-impeccable.md`** in project root — if it exists with required context, proceed.
3. **Run teach mode** — if neither source has context, follow [reference/teach.md](reference/teach.md) before doing any design work.

**Required minimum context**: product surface, fidelity intent (TUX-native or TT Style), primary user.

---

## Fidelity Tiers

| | Strict TUX-native | TT Style |
|---|---|---|
| **Surface** | Mobile product screens — feed, profile, settings, creator tools | Web / marketing / brand surfaces — landing pages, campaign sites, partner portals |
| **Canvas** | 390px mobile | Desktop-first, 1440px max-width |
| **Default theme** | Light (Dark via tokens) | Dark (`#000000`) as preferred canvas |
| **Typography** | 12-style TUX scale (10–32px), 400/600/700 only, letter-spacing: 0 | Display scale (48–96px+) allowed; 800/900 via TikTokVF for hero; negative tracking at 72px+ |
| **Spacing** | 4–32px grid, 16px horizontal padding fixed | Section-level spacing uncapped; responsive horizontal padding (80–120px desktop / 24px mobile) |
| **Motion** | ≤200ms UI feedback, ≤300ms entrance; transform + opacity only | Scroll-driven entrance up to 800ms; clip-path reveals; expressive easing |
| **Glassmorphism** | Banned | Opt-in only — confirm in Teach or Craft brief; never by default |
| **Multi-column grid** | Banned for mobile surfaces | Allowed |

**Universal bans (both tiers):** BAN 1 (side-stripe borders), BAN 2 (gradient text), BAN 3 (invented radius values), BAN 4 (custom shadow values), BAN 5 (unverified tux-web imports), BAN 7 (brand red as background). TikTok Sans / system-ui is the only permitted font family regardless of tier.

---

## Critical Rules

Always load reference files for the full spec. The rules below are the minimum that apply every time.

### Typography
- Font: always `'TikTok Sans', system-ui, -apple-system, sans-serif`. If TikTok Sans is unavailable in the project, `system-ui` is the only fallback — never pull in a substitute typeface.
- Scale: 12 fixed px sizes only: **32/24/20/17/16/15/14/13/12/11/10px**. No intermediate values, no `clamp()`.
- Weights: **400/600/700 only**. Large Title and H1 have no Regular variant; P1 and smaller have no Bold variant.
- **Letter-spacing: always 0.** No exceptions below 72px. (TT Style: negative tracking at 72px+ display text only.)
- Line heights are fixed per style — do not override.
- Max 3 distinct size tiers on one screen.

→ Full token tables, CSS classes, when-to-use guidance: [reference/typography.md](reference/typography.md)

### Color
- Always use `--tux-*` CSS variables. Never write raw hex or rgba in component code.
- **Neutral-first**: ~95% of all visual area is black, white, or gray. Color communicates function, not decoration.
- **Primary (brand red `#FE2C55`)**: at most one distinct interactive element type per screen. Canonical uses: CTA button, active tab pip, filled Like icon, notification badge. Never on non-interactive elements. Never at any opacity as a content area fill or background (BAN 7).
- **Secondary (teal `#20D5EC`)**: toggle ON track, verified badge, secondary accent text on designated surfaces only.
- Never use OKLCH or HSL to build or extend the palette.
- Image and video overlays: black-alpha (`rgba(0,0,0,0.15–0.8)`) or white-alpha only. Never colored tints.
- Dark mode: use official Dark token values only — never guess or invent them.

→ Complete color tables, shadows, spacing, radius, dark mode elevation, Brand Expression Palette: [reference/tokens.md](reference/tokens.md)

### Layout & Space
- **4px grid**: valid values 4/8/12/16/20/24/32px only. No off-grid values.
- **Page horizontal padding: always 16px** (TT Style: 80–120px desktop / 24px mobile).
- **Spacing ceiling: 32px** for TUX-native surfaces (TT Style: uncapped for section-level).
- Use `gap` for sibling spacing, not margins.
- **Surface-first separation**: separate content groups via background color changes (`UI/Page/*`, `UI/Shape/Neutral 4` fill). Borders and dividers are last resort — ask first whether a surface change would do the same job.
- Mobile canvas: 390px. Safe area: 44px status bar top, 34px home indicator bottom. Always account for both.

→ Spacing scale, radius system, touch targets, visual hierarchy rules: [reference/spatial-design.md](reference/spatial-design.md)

### Visual Details
- **Hover**: express via `background` or `opacity` changes only — never `border-color`.
- **Dark mode elevation**: use `UI/Page/Flat-*` brightness steps to signal layer height, not shadows (shadows recede surfaces in dark mode).
- **`overflow: hidden` on text containers**: verify `line-height ≥ 1.0em` to prevent descender clipping. If tight leading is needed, add `padding-bottom: 0.18em; margin-bottom: -0.18em` to the inner element.

→ Motion timing rules: [reference/motion-design.md](reference/motion-design.md)
→ Interactive states, touch targets, focus rings: [reference/interaction-design.md](reference/interaction-design.md)
→ Responsive patterns, safe area, breakpoints: [reference/responsive-design.md](reference/responsive-design.md)
→ UX writing, button labels, error templates: [reference/ux-writing.md](reference/ux-writing.md)
→ Production component templates: [reference/components.md](reference/components.md)

---

## Absolute Bans

These patterns are NEVER acceptable. Match-and-refuse: if you find yourself about to write any of these, stop and rewrite entirely.

**BAN 1** — Side-stripe borders on cards / list items / callouts / alerts
- Pattern: `border-left:` or `border-right:` with width > 1px as a colored accent
- Why: overused design tell; looks unintentional in any context
- Rewrite: use background tints, full borders, or leading icons/numbers instead

**BAN 2** — Gradient text fills
- Pattern: `background-clip: text` combined with a gradient background
- Why: decorative, not meaningful; is a top AI design tell
- Rewrite: solid color text only; use weight or size for emphasis

**BAN 3** — Invented radius values
- Pattern: any `border-radius` not in the TUX content radius table (4/6/8/10/12/9999px) or container radius table (8/10/14/16/26px); mixing content and container radius on the same element
- Rewrite: pick the correct table entry by element height (content) or nesting level (container)

**BAN 4** — Custom shadow values
- Pattern: any `box-shadow` not matching one of the 6 TUX shadow definitions
- Rewrite: choose the closest semantic level (Blocking/Notice/Floating/Attached/Subtle/Contrast)

**BAN 5** — Assumed @byted-tiktok/tux-web imports
- Pattern: importing a component from `@byted-tiktok/tux-web` without first verifying it exists in `package.json` and checking its actual API in the installed package
- Rewrite: verify first, then import; fall back to hand-built TUX-native if unavailable

**BAN 6** (Strict TUX-native only) — Glassmorphism
- Pattern: `backdrop-filter: blur()` used decoratively (not for a true system-blurred sheet)
- TT Style rule: glassmorphism is permitted only when the user has explicitly confirmed it in Teach or Craft Mode. If the context file is silent on glassmorphism, treat it as unconfirmed.

**BAN 7** — Brand red as background
- Pattern: `rgba(254,44,85,*)` at ANY alpha as a section background, card fill, blockquote fill, callout tint, or page background
- Why: brand red is reserved for CTA fills and primary action fills only — any opacity violation counts
- Rewrite: use `rgba(255,255,255,0.04–0.08)` for subtle fills on dark surfaces; `UI/Page/Grouped` or `UI/Page/Flat` tokens on light surfaces

---

## The TikTok Native Test

A production-quality TUX interface passes all three checks:

**1. Token fidelity** — Every color, spacing value, radius, and shadow maps to a TUX v2 token. No invented values.
- Contrast readability: temporarily override page background to `#000000` then `#FFFFFF`. Opacity-based text tokens must remain legible in both extremes.

**2. Hierarchy fidelity** — Content leads. Chrome (nav, tabs, borders) is secondary.
- Focal point check: can you identify the single most dominant element within 1 second? If two elements compete, reduce one.
- 3-tier max: more than 3 distinct visual weight levels means hierarchy is too flat or fragmented.
- Color restraint: Primary appears on at most one distinct interactive element type. Neither Primary nor Secondary on any non-interactive element. Rest of screen is neutral.

**3. Component fidelity** — Buttons at correct heights (52/44/32px). Inputs at 40px, radius 10px. Nav bar 44px. Tab bar 83px with 34px home indicator.

---

## Implementation Principles

Priority order for building blocks:
1. **Existing repository patterns** — extend what's already there first
2. **Verified `@byted-tiktok/tux-web` components** — only after confirming in the installed package
3. **Hand-built TUX-native** — from [reference/components.md](reference/components.md), with full TUX token compliance

Semantic tokens over hard-coded values. Accessible semantics, keyboard support, correct ARIA roles by default.

---

## Craft Mode

Invoke with `craft` (e.g., `/tt-impeccable craft [feature description]`):
→ Follow [reference/craft.md](reference/craft.md). Pass any additional arguments as the feature description.

## Teach Mode

Invoke with `teach` (e.g., `/tt-impeccable teach`):
→ Skip all design work and follow [reference/teach.md](reference/teach.md). One-time project context setup.

## Extract Mode

Invoke with `extract` (e.g., `/tt-impeccable extract [target]`):
→ Follow [reference/extract.md](reference/extract.md). Pass any additional arguments as the extraction target.
