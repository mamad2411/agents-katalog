---
name: typography-system
description: Typography system rules, font pairings, typographic hierarchy, editorial layout, variable fonts, tracking, responsive scaling, vertical rhythm, reading width, and optical balance. Use when configuring typography systems, font scales, and editorial layouts.
---

# ✍️ 03 - Typography System Engine

## 🎯 Purpose
Establish an uncompromising, editorial-grade typography system for premium digital experiences. Typography is the architectural backbone of visual communication. Every typographic choice must directly express the project's bespoke brand personality rather than defaulting to generic or overused font stacks.

---

## 🛠️ Core Responsibilities & Principles

### 1. Intentional Font Pairing (Brand-Driven Selection)
> ⚠️ **RULE**: Never select fonts because they are popular or trending. Every font pairing MUST reinforce the project's emotional tone and visual narrative.

- **Monochromatic Tech / Developer Luxury**:
  - *Display*: `Geist Display`, `Space Grotesk`, or `Söhne Breit`
  - *Body*: `Geist Sans` or `Inter`
  - *Mono / Code*: `Geist Mono` or `JetBrains Mono`
- **Editorial High Fashion / Architectural**:
  - *Display*: `Instrument Serif`, `Syne`, or `PP Editorial New`
  - *Body*: `Switzer` or `General Sans`
  - *Mono*: `Space Mono`
- **Modern Minimalist Product**:
  - *Display*: `General Sans` or `Plus Jakarta Sans`
  - *Body*: `Inter` or `System UI`
  - *Mono*: `Fira Code`

---

### 2. Typographic Scale & Fluid Responsive Scaling
Use CSS `clamp()` for continuous, fluid typography that scales smoothly between mobile viewports (`375px`) and desktop viewports (`1440px+`) without discrete breakpoint jumps.

| Scale Token | Fluid Clamp Definition | Desktop Size | Tracking (Letter Spacing) | Line Height (Leading) | Weight |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `display-xl` | `clamp(3.5rem, 8vw, 7rem)` | `112px` | `-0.04em` | `1.02` | `700` / `Variable` |
| `display-lg` | `clamp(2.75rem, 6vw, 5rem)` | `80px` | `-0.035em` | `1.05` | `600` / `700` |
| `h1` | `clamp(2.25rem, 4.5vw, 3.75rem)`| `60px` | `-0.03em` | `1.1` | `600` |
| `h2` | `clamp(1.75rem, 3.5vw, 2.75rem)`| `44px` | `-0.025em` | `1.15` | `600` |
| `h3` | `clamp(1.35rem, 2.5vw, 2rem)` | `32px` | `-0.02em` | `1.25` | `500` / `600` |
| `h4` | `clamp(1.1rem, 1.8vw, 1.5rem)` | `24px` | `-0.01em` | `1.3` | `500` |
| `body-lg` | `clamp(1.125rem, 1.3vw, 1.25rem)`| `20px` | `-0.01em` | `1.6` | `400` |
| `body-base` | `clamp(0.938rem, 1vw, 1rem)` | `16px` | `0em` | `1.6` | `400` |
| `body-sm` | `clamp(0.813rem, 0.9vw, 0.875rem)`| `14px` | `+0.01em` | `1.5` | `400` / `500` |
| `caption` | `0.75rem` | `12px` | `+0.03em` | `1.4` | `500` (Uppercase) |

---

### 3. Variable Font Optimization
Leverage variable font axes (`wght`, `slnt`, `wdth`, `opsz`) for high-performance optical sizing and continuous weight interpolation during hover/scroll transitions.

```css
/* Variable Font Optical Sizing & Weight Interpolation */
.headline-variable {
  font-family: 'Geist Variable', sans-serif;
  font-variation-settings: 'wght' 650, 'opsz' 36;
  transition: font-variation-settings 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.headline-variable:hover {
  font-variation-settings: 'wght' 750, 'opsz' 48;
}
```

---

### 4. Reading Width & Ergonomics
- **Optimal Line Length**: Restrict paragraph text containers strictly between **45 to 75 characters per line** (`max-width: 65ch`).
- **Short Copy**: Subheaders and lead paragraphs should target `40ch` to `50ch` for instantaneous scanning.

---

### 5. Vertical Rhythm & Baseline Alignment
- All line heights and vertical paragraph margins MUST align to multiples of `4px` or `8px`.
- Use `margin-trim` or explicit utility margins (`mb-4`, `mb-6`, `mb-8`) to maintain consistent baseline cadence across column blocks.

---

### 6. Optical Alignment & Editorial Details
- **Hanging Punctuation**: Enable `hanging-punctuation: first last;` for editorial quote blocks and headers.
- **Font Feature Settings**: Always enable advanced OpenType features for high-end rendering:
  ```css
  .text-editorial {
    font-feature-settings: 'kern' 1, 'liga' 1, 'calt' 1, 'cv05' 1;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  ```
- **Optical Margin Trim**: Adjust display header negative left margins (`margin-left: -0.04em`) so characters like `T`, `W`, `V`, `O`, or quote marks optically align flush with the grid edge.
