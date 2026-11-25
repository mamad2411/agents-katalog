# UI Guidelines — Printable Maze Generator

These guidelines define **intentional UI behavior**, not generic "modern UI" defaults.  
They exist to keep the interface calm, printable-first, parent-friendly, and reviewer-clean.

---

## 1) Layout Philosophy — Asymmetrical, Calm

- Use an **asymmetrical layout**, balanced but not centered.
- Control panel on the **left** (reading order: controls → action → result).
- Panel width: ≈30–35% of viewport.
- The remaining space is reserved for preview and background context.
- In v0, the preview area is intentional white space. No live maze preview.
- Avoid card-heavy or dashboard-style layouts.
- White space is intentional; nothing should feel dense or "app-like."

### Responsive Behavior
- On narrow viewports (<768px), stack vertically: controls above preview area.

**Intent:** feel like a worksheet tool, not a game or SaaS product.

---

## 2) Typography — Parent Assisting a Child

### Header / Display Font
**Fraunces (variable serif)**

- Friendly, human, slightly playful
- Signals "this is for kids, but adults are in control"
- Use for:
  - Page title
  - Section headers
  - Primary call-to-action text

---

### Body / UI Font
**Inter**

- Highly legible
- Neutral and modern
- Use for:
  - All form controls
  - Labels and helper text
  - Footer and attribution

### Font Loading
- Fonts should be self-hosted or bundled.
- No runtime dependency on Google Fonts CDN.
- Provide system font fallbacks for offline resilience.

**Rule:** use only these two fonts.

---

## 3) Background Treatment — Maze as Context

- Full-screen background with a **faint maze illustration**
- Very low contrast (5–10% opacity)
- Static in v0 (no motion or parallax)

### Constraints
- Background must never reduce readability
- Foreground panels must have solid or softly translucent backing
- No animation in v0

**Intent:** establish mood without competing for attention.

---

## 4) Controls — Interactive but Obvious

Controls must be **discoverable without instruction**.

### Core Principles
- Every control has:
  - a visible label
  - a visible current state
- No hidden gestures
- No icon-only controls

### Control Patterns
- **Age Range:** segmented buttons (not a dropdown)
- **Maze Style / Theme:** toggle groups with text-first labels
- **Quantity:** stepper or slider with numeric feedback
- **Primary Action:** one dominant button only

### Primary Action Button
- Label: **Generate Printable PDF**
- Visually dominant
- One per screen
- No competing secondary actions

---

## 5) Color, Borders, and Line Language

### Color Palette (Muted, Print-Aware)

| Role | Color | Hex |
|------|-------|-----|
| Background | warm off-white | `#FAFAF8` |
| Primary | slate-900 (deep navy/charcoal) | `#1E293B` |
| Accent | slate-600 (muted blue-gray) | `#475569` |
| Border | slate-200 | `#E2E8F0` |
| Text muted | slate-500 | `#64748B` |

- Avoid saturated or playful colors.
- All colors must translate cleanly to grayscale.

---

### Borders & Shape Language
- Rounded corners used sparingly to imply friendliness
- Small, consistent border radius (4–8px)
- Minimal or no shadows
- Prefer outlines over elevation

**Rule:** if it would not print well, it does not belong in the UI.

---

## 6) Accessibility Baseline

- Maintain WCAG AA contrast (4.5:1 for body text, 3:1 for large text).
- Visible focus states on all interactive elements.
- Controls must be keyboard-navigable.
- Labels must be associated with their inputs.

---

## 7) Overall Tone Check

The UI should feel:
- Calm
- Trustworthy
- Slightly playful, never loud
- Closer to an educational worksheet than a game

If a design choice feels:
- like a toy → too far
- like enterprise software → too far

Pull it back.

---

## Non-Goals (UI)

- No gamification
- No animations in v0
- No personalization
- No visual complexity that does not survive printing

These constraints are intentional and enforced.
