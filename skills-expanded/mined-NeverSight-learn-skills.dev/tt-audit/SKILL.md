---
name: tt-audit
description: >
  Run technical quality checks against TUX v2 standards and generate a scored
  report. Checks accessibility, performance, TUX token fidelity, component
  compliance, and TikTok native test. Produces P0-P3 findings with actionable
  recommendations. Does NOT fix — use /tt-impeccable extract or /tt-impeccable
  craft to act on findings.
version: 1.0.0
user-invocable: true
argument-hint: "[area (feature, page, component...)]"
license: Apache 2.0. Based on Anthropic's impeccable skill ecosystem. See NOTICE.md.
---

## Mandatory Preparation

Invoke `/tt-impeccable` — it contains TUX design principles, token tables, and the **Context Gathering Protocol**. Follow the protocol before proceeding. If no TUX design context exists yet, run `/tt-impeccable teach` first.

---

## Fidelity Tier

Before running any checks, determine which tier this project operates under:

1. Read `.tt-impeccable.md` from the project root → check `### Fidelity Intent`
2. If absent, check loaded instructions for a `## TUX Design Context` block
3. If neither exists, ask: "Is this a **Strict TUX-native** (mobile product screen) or **TT Style** (web / marketing surface)?"

Rules below marked **(TUX-native only)** are skipped for TT Style projects — they are not violations. Rules marked **(TT Style only)** are skipped for TUX-native. **Universal** rules apply to both tiers.

---

Run systematic **technical** quality checks against TUX v2 standards and generate a comprehensive report. **Do not fix issues** — document them for `/tt-impeccable extract` or `/tt-impeccable craft` to address.

This is a code-level audit, not a design critique. Check what is measurable and verifiable in the implementation.

---

## Diagnostic Scan

Score each of the 5 dimensions 0–4 using the criteria below.

---

### 1. Accessibility (A11y)

**Check for**:
- **Contrast**: Text contrast < 4.5:1 (normal) or < 3:1 (large text / UI components)
- **Touch targets**: Interactive elements with tap area < 44×44px
- **Missing ARIA**: Interactive elements without role, label, or state attributes
- **Keyboard navigation**: Missing `:focus-visible`, illogical tab order, keyboard traps
- **Semantic HTML**: `<div>` used as button, missing `<main>`/`<nav>` landmarks, broken heading hierarchy
- **Form issues**: `<input>` without `<label>`, errors not associated via `aria-describedby`, missing `required`

**Score 0–4**: 0 = Inaccessible (fails WCAG A) · 1 = Major gaps · 2 = Partial effort · 3 = WCAG AA mostly met · 4 = WCAG AA fully met

---

### 2. Performance

**Check for**:
- **Expensive animations**: `width`, `height`, `top`, `left`, `padding`, `margin` being animated instead of `transform`/`opacity` **(universal)**
- **Animation duration** **(TUX-native only)**: UI feedback transitions exceeding 200ms or entrance transitions exceeding 300ms — flag as P2. (TT Style: scroll-driven hero entrances up to 800ms are acceptable; looping/idle animations remain banned.)
- **Layout thrashing**: Reading and writing layout properties in the same loop **(universal)**
- **Missing lazy loading**: Off-screen images or content loaded eagerly
- **Excessive re-renders**: Missing memoization, state causing full subtree re-render
- **Unused imports**: Dependencies imported but not used; heavy libraries for trivial tasks

**Score 0–4**: 0 = Severe · 1 = Major problems · 2 = Partial · 3 = Mostly optimized · 4 = Fast and lean

---

### 3. TUX Token Fidelity

The core TUX-specific dimension. Check every color, spacing, radius, shadow, and typography declaration against `reference/tokens.md` and `reference/typography.md`.

**Colors**:
- Raw hex or rgba values not going through `var(--tux-*)` CSS variables
- OKLCH, HSL, or custom color functions
- Brand red (`#FE2C55`) used as section background or decorative fill
- Neutral-first violation: `UI/Shape/Primary` or `UI/Shape/Secondary` appearing on more than one distinct element type per screen (TUX-native only; flag as P2)
- Colored overlay (red or teal tint) applied over image or video content — Image Overlay tokens must be black-alpha or white-alpha only (universal)
- Colored skeleton/placeholder on image or video loading states — must use `UI/Shape/Neutral 4` (universal)
- Invented dark mode values not from the official token table

**Borders & Dividers**:
- Border overuse: `border`, `border-top`, or `border-bottom` used to separate content groups where a background color change (`UI/Page/Flat 2`, `UI/Page/Grouped 1/2`, `UI/Shape/Neutral 4` fill) would achieve the same separation. Flag as P2 — borders add visual noise TUX avoids by design.
- `border-left` or `border-right` > 1px as a colored accent stripe — flag as P0 (hard ban, universal)
- Divider weight: prefer `0.5px` hairline over `1px` on retina screens
- **Hover via border-color**: any `:hover` rule that changes `border-color` or adds a new `border` — flag as P2. Hover state must be expressed through `background` or `opacity` changes, not border changes. Ghost/outline buttons are the only exception, and even then only the `background` should change on hover, not the `border-color`.
- **Border compensating for insufficient surface contrast**: if a `border` appears on a dark surface element (e.g., a code block or panel) whose background is nearly identical to the page background, flag as P2 — the root cause is a wrong background color, not a missing border. The fix is to use the correct `UI/Page/Flat 2` (`#1E1E1E`) or `UI/Page/Flat 3` (`#2C2C2C`) token, not to add an outline.

**Brand Red Opacity Violations**:
- `rgba(254,44,85,*)` at ANY alpha value used as a content area fill, section background, blockquote tint, or card background — flag as P1 regardless of opacity. A tint of `0.06` is as much a BAN 7 violation as full opacity. Legitimate sub-full-opacity uses are interactive state fills only (pressed row, selected background).
- Check for `--red-dim`, `var(--tux-shape-primary-4)`, `var(--tux-shape-primary-5)` on non-interactive elements — flag as P1.

**Neutral-first (expanded)**:
- Primary/Secondary on non-interactive elements is a violation even if it appears only once — the "one element per screen" rule is a ceiling, not a floor. A decorative arrow, separator, bullet, or background tint in brand red or teal fails the neutral-first check regardless of count. Verify interactivity: does the element have `onClick`, `href`, `role="button"`, or equivalent? If not, it must be neutral.

**Spacing**:
- Any pixel value not in the TUX 4px grid: 4 / 8 / 12 / 16 / 20 / 24 / 32 **(universal)**
- Values exceeding 32px **(TUX-native only)** — TT Style allows uncapped section spacing
- Page horizontal padding deviating from 16px **(TUX-native only)** — TT Style uses responsive padding (80–120px desktop / 24px mobile)

**Radius**:
- Values not from content radius table: 4 / 6 / 8 / 10 / 12 / 9999px
- Values not from container radius table: 8 / 10 / 14 / 16 / 26px
- Content and container radius mixed on the same element

**Shadow**:
- Custom `box-shadow` values not matching the 6 TUX levels
- Drop shadows used in dark mode for elevation (should be brightness overlays)

**Typography**:
- Font family other than `'TikTok Sans', system-ui, -apple-system, sans-serif` **(universal)**
- Font sizes not in the 12-step scale: 32 / 24 / 20 / 17 / 16 / 15 / 14 / 13 / 12 / 11 / 10px **(TUX-native only)** — TT Style allows display scale (48 / 72 / 96px+) for hero text
- Font weight above 700 **(TUX-native only)** — TT Style allows 800/900 via TikTokVF for hero display text
- Non-zero `letter-spacing` on text below 72px **(universal)** — TT Style allows negative tracking at 72px+ display text only
- Line-heights not matching the fixed per-style values from the type scale **(TUX-native only)**
- More than 3 distinct size tiers visible on one screen **(universal)**

**Score 0–4**: 0 = No tokens (hard-coded everything) · 1 = Occasional tokens · 2 = Partial · 3 = Good, minor hard-coded values · 4 = Full compliance

---

### 4. TUX Component Compliance

Check that TUX components match their specified dimensions, states, and structure.

| Component | Spec | ✓/✗ |
|---|---|---|
| Full-width CTA button | height 52px, pill radius (9999px) | |
| Mid-page button | height 44px, pill radius | |
| Inline button | height 32px, pill radius | |
| Text input / search bar | height 40px, radius 10px, `rgba(0,0,0,0.05)` bg | |
| Toggle | 52×32px track, teal ON / neutral OFF | |
| Navigation bar | height 44px, horizontal padding 16px | |
| Tab bar | 83px total (49px visible + 34px home indicator inset) | |
| Status bar spacer | 44px top | |
| Safe area bottom | 34px | |

**Also check for bans** (mark tier where applicable):
1. Side-stripe borders (border-left/right > 1px as accent) **(universal)**
2. Gradient text (`background-clip: text` + gradient) **(universal)**
3. Invented radius values (outside the two official tables) **(universal)**
4. Custom shadow values (outside the 6 TUX levels) **(universal)**
5. Assumed `@byted-tiktok/tux-web` imports (without package.json verification) **(universal)**
6. Glassmorphism (`backdrop-filter: blur()` decoratively) **(TUX-native: hard ban. TT Style: flag as P2 if `.tt-impeccable.md` Glassmorphism field is absent or "No" — it requires explicit user confirmation, not assumed from the fidelity tier)**
7. Brand red as large-area background **(universal)**

**Score 0–4**: 0 = Multiple spec violations + banned patterns · 1 = Several wrong dimensions · 2 = Some violations · 3 = Minor deviations · 4 = Full compliance

---

### 5. TikTok Native Test

> "If you sent a screenshot to a TikTok designer, would they say 'that's TikTok' or 'that's a clone'?"

Apply the criteria matching the declared fidelity tier:

**Strict TUX-native** — "Does this feel like it belongs inside the TikTok app?":
- Is content the most visually dominant element — not chrome, not decoration?
- Is there a single clear focal point (primary CTA or main content) identifiable in 1 second?
- Are there more than 3 distinct visual weight tiers on screen?
- Do same-level elements use consistent size and weight?
- Are accent colors (brand red, teal) only on interactive elements of the appropriate type?
- Does Primary (brand red) appear on more than one distinct interactive element type per screen? If so, the color restraint rule is broken — one of them should be neutral.
- Do any image or video surfaces have colored overlays or colored placeholder backgrounds? They must not.
- Does content at the viewport bottom clip slightly (signals scrollability without a label)?
- On lists with section separators, is the first cell's top gap 8px larger than cell-to-cell gap?

**TT Style** — "Does this feel like tiktokbrandhub.com — or a generic dark web page?":
- Is the dark canvas (#000000) used as the primary background?
- Do Blaze (red) and Glint (teal) appear only in their correct semantic roles (CTA / secondary accent)?
- Does the hero typography have presence — bold weight, clear scale hierarchy?
- Is negative space used intentionally, not just left empty?
- Does motion feel purposeful and brand-forward, not generic (no CSS default easings, no bounce)?
- Is the pill button shape present on primary actions?
- Would someone recognize this as TikTok brand — not a TikTok-adjacent third party?

**Score 0–4**: 0 = Clearly third-party · 1 = Significant divergence · 2 = Recognizable but rough · 3 = Close, minor tells · 4 = Indistinguishable from authentic TikTok (native app or Brand Hub depending on tier)

---

## Generate Report

### Audit Health Score

| # | Dimension | Score | Key Finding |
|---|---|---|---|
| 1 | Accessibility | ? /4 | [most critical issue or —] |
| 2 | Performance | ? /4 | |
| 3 | TUX Token Fidelity | ? /4 | |
| 4 | TUX Component Compliance | ? /4 | |
| 5 | TikTok Native Test | ? /4 | |
| **Total** | | **??/20** | **[rating]** |

**Rating bands**: 18–20 Excellent · 14–17 Good · 10–13 Acceptable · 6–9 Poor · 0–5 Critical

---

### TUX Token Verdict

**Start here.** Pass/fail: does the implementation use TUX tokens throughout, or are there hard-coded values? List specific violations with file and line locations. Be specific — "rgba(254,44,85,1) hardcoded in Button.tsx line 34" not "some colors are hardcoded".

---

### Executive Summary

- Audit Health Score: **??/20** ([rating band])
- Issues by severity: P0 __ · P1 __ · P2 __ · P3 __
- Top 3–5 critical issues
- Recommended next steps

---

### Detailed Findings by Severity

Tag every issue with **P0–P3**:
- **P0 Blocking** — prevents task completion or causes WCAG failure; fix before any release
- **P1 Major** — significant user impact or TUX fidelity gap; fix before release
- **P2 Minor** — visible deviation, workaround exists; fix in next pass
- **P3 Polish** — subtle; fix if time permits

For each issue:
- **[P?] Issue name**
- **Location**: component / file / line number
- **Category**: Accessibility · Performance · Token Fidelity · Component · TikTok Native
- **Impact**: how it affects users or TUX compliance
- **Recommendation**: exactly what to change and to what value
- **Suggested command**: `/tt-impeccable extract` for token/component fixes; `/tt-impeccable craft [feature]` for structural rebuilds

---

### Systemic Issues

Identify patterns that indicate a systemic gap:
- "Hard-coded colors appear in 12+ components — needs a shared tokens CSS file"
- "Touch targets consistently under 44px — interaction patterns need a sweep"

---

### Positive Findings

Note what is correct and should be preserved. Good practices are as important to document as violations.

---

## Recommended Actions

List in priority order (P0 first):

1. **[P?] `/tt-impeccable extract`** — [specific tokens / components to align]
2. **[P?] `/tt-impeccable craft [feature]`** — [what to rebuild and why]

After presenting the report:

> You can ask me to run these one at a time, all at once, or in any order you prefer.
>
> Re-run `/tt-audit` after fixes to track score improvement.

---

## Never

- Report issues without explaining user impact
- Give generic recommendations — cite specific files, lines, and values
- Skip positive findings
- Mark everything P0 — prioritization is the point
- Report false positives without verifying in the actual code
- Fix anything during audit — this is a read-only diagnostic pass
