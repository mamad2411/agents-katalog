---
name: css-micro-fx
description: >
  Pure CSS functional feedback effects for form inputs, buttons, loading
  states and text links. Triggered by :focus, :active, and state changes —
  not hover. Auto-matches intensity to the existing design style.
  Zero JS, zero dependencies, no SSR issues. Sourced from cssfx (6.1k ★).
triggers:
  - "input focus"
  - "form animation"
  - "form effect"
  - "loading state"
  - "loading animation"
  - "button click effect"
  - "button feedback"
  - "micro interaction"
  - "micro animation"
  - "form feedback"
  - "focus effect"
  - "active state"
  - "submit button"
  - "input highlight"
  - "spinner"
  - "progress indicator"
  - "polished form"
  - "form feels flat"
license: MIT
attribution: "Pattern library derived from cssfx by jolaleye (MIT) — modernized and extended"
upstream: "https://github.com/jolaleye/cssfx"
---

# CSS Micro-FX

Functional feedback effects: inputs, buttons, loaders, text links.
These respond to **:focus / :active / state changes** — not hover.

---

## Step 1 — Detect Context & Style

Read the existing UI before applying anything.

### What to read
```
Form density
  few fields, large padding  → marketing / signup page → Shine, Bubble
  many fields, tight layout  → app / dashboard        → Bars, subtle Highlight

Button prominence
  large CTA (full-width or hero)  → Shine or Slide
  small inline button             → Jelly or Pulse

Color palette
  monochrome / muted  → MINIMAL → Bars, Highlight only
  vivid accent color  → BOLD    → all effects

Existing focus styles
  outline: none (reset)  → must add visible focus → use Bars or Glow
  outline present        → enhance, don't replace
  
Dark background
  yes → use lighter glow variants
  no  → standard effects
```

### Style Classification (same as css-hover-effects)

| Style | Key Signal | Intensity |
|-------|-----------|-----------|
| MINIMAL | muted palette, large radius | Bars, Highlight only |
| BOLD | vivid accent, strong shadows | Shine, Slide, Bubble |
| PLAYFUL | rounded, colorful | Jelly, Bubble, Pulse |
| CORPORATE | tight layout, muted | Bars, subtle Glow |
| DARK-PREMIUM | dark bg, glowing accents | Glow, Bars with accent |

---

## Step 2 — Compatibility Matrix

| Effect | MINIMAL | BOLD | PLAYFUL | CORPORATE | DARK-PREMIUM |
|--------|---------|------|---------|-----------|--------------|
| Bars (input) | ✅ ★ | ✅ | ✅ | ✅ ★ | ✅ |
| Highlight (input) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Glow (input) | ❌ | ✅ | ✅ | ❌ | ✅ ★ |
| Bubble (button) | ❌ | ✅ | ✅ ★ | ❌ | ❌ |
| Jelly (button) | ❌ | ✅ | ✅ ★ | ❌ | ❌ |
| Shine (button) | ❌ | ✅ ★ | ✅ | ❌ | ✅ |
| Slide (button) | ✅ | ✅ ★ | ✅ | ✅ | ✅ |
| Pulse (button) | ❌ | ✅ | ✅ | ❌ | ❌ |
| Pillars (loader) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Overline (loader) | ✅ ★ | ✅ | ✅ | ✅ ★ | ✅ |
| Strikethrough (done) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Underline (link) | ✅ ★ | ✅ | ✅ | ✅ | ✅ |

---

## Step 3 — Effect Library

---

### CATEGORY: Input Focus Effects

Apply to `<input>`, `<textarea>`, `<select>`.
Always pair with a visible focus ring or replacement for accessibility.

#### Bars
Bottom border slides in from center. Clean, universal.
Best for: any style. Default choice when unsure.
```css
.fx-input-bars {
  --accent: #6366f1;
  border: none;
  border-bottom: 2px solid #e4e4e7;
  border-radius: 0;
  padding: 10px 4px;
  outline: none;
  background: transparent;
  width: 100%;
  font-size: 14px;
  transition: border-color 0.25s ease;
  position: relative;
}
.fx-input-bars:focus {
  border-bottom-color: var(--accent);
}
/* Optional: animated line variant */
.fx-input-bars-animated {
  border: none;
  border-bottom: 2px solid #e4e4e7;
  outline: none;
  padding: 10px 4px;
  width: 100%;
  font-size: 14px;
  background: transparent;
}
.fx-input-bars-animated + .bar-line {
  display: block;
  height: 2px;
  background: var(--accent, #6366f1);
  width: 0;
  transition: width 0.3s ease;
  margin-top: -2px;
}
.fx-input-bars-animated:focus + .bar-line {
  width: 100%;
}
```
*HTML for animated variant:*
```html
<input class="fx-input-bars-animated" type="text" placeholder="Name">
<span class="bar-line"></span>
```

---

#### Highlight
Soft background tint on focus. Rounded inputs, card forms.
```css
.fx-input-highlight {
  --accent: #6366f1;
  --highlight: rgba(99, 102, 241, 0.08);
  border: 1.5px solid #e4e4e7;
  border-radius: 8px;
  padding: 10px 14px;
  outline: none;
  width: 100%;
  font-size: 14px;
  background: white;
  transition: border-color 0.25s ease, background-color 0.25s ease;
}
.fx-input-highlight:focus {
  border-color: var(--accent);
  background-color: var(--highlight);
}
```

---

#### Glow
Focus ring glow. DARK-PREMIUM and BOLD styles.
```css
.fx-input-glow {
  --accent: #6366f1;
  --glow: rgba(99, 102, 241, 0.25);
  border: 1.5px solid #e4e4e7;
  border-radius: 8px;
  padding: 10px 14px;
  outline: none;
  width: 100%;
  font-size: 14px;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
.fx-input-glow:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 4px var(--glow);
}
```

---

#### Label Float
Label animates up when input is focused or filled.
For forms where the label sits inside the input.
```css
.fx-field-float {
  position: relative;
  padding-top: 16px;
}
.fx-field-float input {
  border: 1.5px solid #e4e4e7;
  border-radius: 8px;
  padding: 14px 14px 6px;
  outline: none;
  width: 100%;
  font-size: 14px;
  transition: border-color 0.25s ease;
}
.fx-field-float label {
  position: absolute;
  left: 14px;
  top: 26px;
  font-size: 14px;
  color: #a1a1aa;
  pointer-events: none;
  transition: top 0.2s ease, font-size 0.2s ease, color 0.2s ease;
}
.fx-field-float input:focus,
.fx-field-float input:not(:placeholder-shown) {
  border-color: #6366f1;
}
.fx-field-float input:focus + label,
.fx-field-float input:not(:placeholder-shown) + label {
  top: 6px;
  font-size: 11px;
  color: #6366f1;
}
```
*HTML:*
```html
<div class="fx-field-float">
  <input type="text" id="name" placeholder=" ">
  <label for="name">Full name</label>
</div>
```

---

### CATEGORY: Button Click Effects

Apply to `<button>` elements. Triggered on `:active` or via JS class.

#### Bubble
Ripple circle expands from click point on `:active`.
```css
.fx-btn-bubble {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.fx-btn-bubble::after {
  content: '';
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%) scale(0);
  width: 120%;
  padding-top: 120%;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  opacity: 0;
  transition: transform 0.5s ease, opacity 0.4s ease;
}
.fx-btn-bubble:active::after {
  transform: translate(-50%, -50%) scale(1);
  opacity: 1;
  transition: 0s;
}
```

---

#### Jelly
Elastic squish on click. PLAYFUL and BOLD only.
```css
.fx-btn-jelly {
  cursor: pointer;
  transition: transform 0.1s ease;
}
.fx-btn-jelly:active {
  animation: fx-jelly 0.4s ease;
}
@keyframes fx-jelly {
  0%  { transform: scale(1, 1); }
  25% { transform: scale(0.9, 1.12); }
  50% { transform: scale(1.1, 0.9); }
  75% { transform: scale(0.96, 1.04); }
  100% { transform: scale(1, 1); }
}
```

---

#### Shine
Light sweep diagonally across button on hover. Premium CTA feel.
```css
.fx-btn-shine {
  position: relative;
  overflow: hidden;
  cursor: pointer;
}
.fx-btn-shine::after {
  content: '';
  position: absolute;
  top: -60%;
  left: -100%;
  width: 60%;
  height: 220%;
  background: rgba(255, 255, 255, 0.22);
  transform: skewX(-20deg);
  transition: left 0.45s ease;
  pointer-events: none;
}
.fx-btn-shine:hover::after {
  left: 140%;
}
```

---

#### Slide
Background color slides in from left on hover. Versatile.
```css
.fx-btn-slide {
  --slide-color: var(--accent, #6366f1);
  --text-hover: white;
  position: relative;
  z-index: 1;
  overflow: hidden;
  cursor: pointer;
  transition: color 0.3s ease;
}
.fx-btn-slide::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--slide-color);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  z-index: -1;
}
.fx-btn-slide:hover::before {
  transform: translateX(0);
}
.fx-btn-slide:hover {
  color: var(--text-hover);
}
```

---

#### Pulse
Persistent pulsing ring. Draws attention to a single action button.
Use on ONE element maximum per page.
```css
.fx-btn-pulse {
  --pulse-color: rgba(99, 102, 241, 0.4);
  position: relative;
  cursor: pointer;
}
.fx-btn-pulse::before {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: inherit;
  border: 2px solid var(--pulse-color);
  animation: fx-pulse-ring 1.5s ease infinite;
}
@keyframes fx-pulse-ring {
  0%   { transform: scale(1); opacity: 1; }
  100% { transform: scale(1.15); opacity: 0; }
}
```

---

#### Press
Subtle depth press on click. Tactile "button pushes in" feel.
Works on any style — most conservative option.
```css
.fx-btn-press {
  transition: transform 0.08s ease, box-shadow 0.08s ease;
  box-shadow: 0 4px 0 rgba(0,0,0,0.15);
}
.fx-btn-press:active {
  transform: translateY(3px);
  box-shadow: 0 1px 0 rgba(0,0,0,0.15);
}
```

---

### CATEGORY: Loading States

Use when an async operation is in progress.
Swap loading class in via JS when needed.

#### Pillars
5 bars wave in sequence. Compact, fits inside buttons.
```css
.fx-loader-pillars {
  display: inline-flex;
  gap: 3px;
  align-items: flex-end;
  height: 18px;
  vertical-align: middle;
}
.fx-loader-pillars span {
  display: block;
  width: 3px;
  border-radius: 2px;
  background: currentColor;
  animation: fx-pillars 0.9s ease infinite;
}
.fx-loader-pillars span:nth-child(1) { height: 6px;  animation-delay: 0s; }
.fx-loader-pillars span:nth-child(2) { height: 12px; animation-delay: 0.12s; }
.fx-loader-pillars span:nth-child(3) { height: 18px; animation-delay: 0.24s; }
.fx-loader-pillars span:nth-child(4) { height: 12px; animation-delay: 0.36s; }
.fx-loader-pillars span:nth-child(5) { height: 6px;  animation-delay: 0.48s; }
@keyframes fx-pillars {
  0%, 100% { opacity: 0.3; transform: scaleY(0.6); }
  50%       { opacity: 1;   transform: scaleY(1); }
}
```
*HTML:*
```html
<div class="fx-loader-pillars">
  <span></span><span></span><span></span><span></span><span></span>
</div>
```

---

#### Overline
Progress bar sweeps across full width. Page-level or section loading.
```css
.fx-loader-overline {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: rgba(99, 102, 241, 0.15);
  z-index: 9999;
  overflow: hidden;
}
.fx-loader-overline::after {
  content: '';
  position: absolute;
  left: -40%;
  top: 0;
  width: 40%;
  height: 100%;
  background: var(--accent, #6366f1);
  border-radius: 0 2px 2px 0;
  animation: fx-overline 1.1s ease infinite;
}
@keyframes fx-overline {
  to { left: 100%; }
}
```
*Usage: add/remove `.fx-loader-overline` div on route change or fetch.*

---

#### Spinner Dot
Three dots pulse in sequence. Inline "typing" / "thinking" state.
```css
.fx-loader-dots {
  display: inline-flex;
  gap: 5px;
  align-items: center;
}
.fx-loader-dots span {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: fx-dot-pulse 1.2s ease infinite;
}
.fx-loader-dots span:nth-child(2) { animation-delay: 0.2s; }
.fx-loader-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes fx-dot-pulse {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40%            { transform: scale(1);   opacity: 1; }
}
```

---

#### Spinner Ring
Classic circular spinner. Buttons and inline loaders.
```css
.fx-spinner-ring {
  --size: 18px;
  --thickness: 2px;
  --color: currentColor;
  width: var(--size);
  height: var(--size);
  border: var(--thickness) solid rgba(255,255,255,0.25);
  border-top-color: var(--color);
  border-radius: 50%;
  animation: fx-spin 0.7s linear infinite;
  display: inline-block;
}
@keyframes fx-spin { to { transform: rotate(360deg); } }
```

---

#### Strikethrough
Line draws through text when task is complete.
```css
.fx-done {
  position: relative;
  display: inline-block;
  color: #a1a1aa;
}
.fx-done::after {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  height: 1.5px;
  width: 0;
  background: var(--accent, #22c55e);
  animation: fx-strike 0.4s ease forwards;
}
@keyframes fx-strike {
  to { width: 100%; }
}
```
*Apply `.fx-done` class via JS when the task is marked complete.*

---

### CATEGORY: Text Link Effects

Apply to `<a>` tags within body copy.

#### Underline Draw
Line draws in on hover from left. Replaces static underline.
```css
.fx-link-draw {
  --accent: #6366f1;
  text-decoration: none;
  position: relative;
  color: var(--accent);
}
.fx-link-draw::after {
  content: '';
  position: absolute;
  bottom: -1px; left: 0;
  height: 1.5px;
  width: 0;
  background: var(--accent);
  transition: width 0.25s ease;
}
.fx-link-draw:hover::after { width: 100%; }
```

---

#### Underline Slide Out
Line is always visible, slides out and back in — surprise reversal.
```css
.fx-link-slide {
  --accent: #6366f1;
  text-decoration: none;
  color: var(--accent);
  background-image: linear-gradient(var(--accent), var(--accent));
  background-position: bottom left;
  background-repeat: no-repeat;
  background-size: 100% 1.5px;
  transition: background-size 0.25s ease;
}
.fx-link-slide:hover {
  background-size: 0% 1.5px;
}
```

---

#### Color Shift
Text color transitions to accent on hover. Simple, safe.
```css
.fx-link-color {
  --accent: #6366f1;
  color: inherit;
  text-decoration: none;
  transition: color 0.2s ease;
}
.fx-link-color:hover { color: var(--accent); }
```

---

## Step 4 — Combining with css-hover-effects

These two skills are designed to work together:

```
css-hover-effects    →  :hover state (mouse enter)
css-micro-fx         →  :focus / :active / state change
```

**Example: polished button**
```css
/* hover-effects handles the hover state */
.btn { /* hvr-shine applied */ }

/* micro-fx handles the click */
.btn { /* fx-btn-jelly applied */ }

/* Together: shine on hover, jelly on click */
```

**Example: polished input**
```css
/* micro-fx handles focus */
.input { /* fx-input-bars applied */ }

/* hover-effects adds a subtle border hint on hover */
.input:hover { border-color: #c4b5fd; }
```

---

## Step 5 — Application Checklist

- [ ] Identified form context (marketing vs app) and adjusted intensity
- [ ] Chosen input effect (Bars for minimal/corporate, Glow for dark/bold)
- [ ] Applied `prefers-reduced-motion` block (once per stylesheet)
- [ ] Pulse used on ≤ 1 button per page
- [ ] Overline loader attached to route/fetch lifecycle
- [ ] Strikethrough triggered by JS class, not CSS-only
- [ ] All effects use `var(--accent)` pointing to existing palette

```css
/* Always include — paste once at the top of any stylesheet using these effects */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Quick Reference

| Need | Effect | Class |
|------|--------|-------|
| Input focus, minimal style | Bars animated | `fx-input-bars-animated` |
| Input focus, any style | Highlight | `fx-input-highlight` |
| Input focus, dark/bold | Glow | `fx-input-glow` |
| Float label | Label Float | `fx-field-float` |
| Button click, playful | Jelly | `fx-btn-jelly` |
| Button click, premium | Bubble | `fx-btn-bubble` |
| Button hover shine | Shine | `fx-btn-shine` |
| Button hover slide | Slide | `fx-btn-slide` |
| Draw attention to CTA | Pulse | `fx-btn-pulse` |
| Tactile press feel | Press | `fx-btn-press` |
| Loading in button | Pillars | `fx-loader-pillars` |
| Page-level loading | Overline | `fx-loader-overline` |
| Chat / AI thinking | Dots | `fx-loader-dots` |
| General spinner | Ring | `fx-spinner-ring` |
| Task complete | Strikethrough | `fx-done` |
| Body copy links | Underline Draw | `fx-link-draw` |
