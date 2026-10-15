---
name: vis-reverse-ui
description: Reverse engineer web UIs and design mockups into pixel-accurate CSS design tokens, computed style specs, and atomic CSS properties. Use when extracting design systems from existing websites, replicating frontend components, or converting rendered UI into clean CSS variables and Tailwind tokens.
---

# UI Visual Reverse Engineering & Atomic Token Extraction

Extract pixel-accurate computed styles, design tokens, and W3C atomic CSS specifications from rendered web pages or UI mockups using automated tool inspection, adversarial cross-verification, and first-principles CSS decomposition.

## Core Rules & Guardrails

- **Zero Guesswork / Real Computed Styles**: All measurements (px, rem, hex/rgba) must originate from real computed browser styles. Approximate descriptions ("about 16px", "bluish") are strictly prohibited.
- **First-Principles Atomic Decomposition (4 Steps)**:
  1. *Identify Compound Properties*: Detect all compound CSS rules (`background`, `border`, `padding`, `margin`, `flex`, `grid`, `font`, `box-shadow`).
  2. *Decompose to Minimal W3C Units*: Break compound properties down to indivisible W3C sub-properties (e.g. `border` $\rightarrow$ `border-top-width`, `border-top-style`, `border-top-color`).
  3. *Verify Decomposition Depth*: Recursively verify that no compound properties remain.
  4. *Dual Output*: Provide both the human-readable compound shorthand and the development-ready atomic breakdown.
- **High Cohesion & Low Coupling**:
  - *Cohesion*: Each design token must serve exactly one semantic category (Color, Size, Spacing, Font, Shadow, Radius, Motion).
  - *Coupling*: Token references must not exceed 1 layer of indirect reference (e.g. `--btn-bg: var(--color-primary-500)` is 1 layer; no multi-hop chaining).

---

## 3-Step Adversarial Style Verification (Ultracode Method)

```
[Step 1: Specificity & Inheritance Trace] ➔ [Step 2: Dual-Tool Cross Verification] ➔ [Step 3: Confidence Tiering (L1/L2/L3)]
```

1. **Specificity & Origin Trace**: Trace CSS rule origin, selector specificity, and parent inheritance to ensure captured values are the actual winning computed styles.
2. **Cross-Tool Tolerance**: Compare measurements across browser tools. Numerical deviation $\le 1\text{px}$ and color difference $\Delta E \le 1$ pass.
3. **Confidence Level**:
   - `L1 (High)`: Clear origin rule, verified computed style with zero inheritance interference.
   - `L2 (Medium)`: Verified with explainable cascade override.
   - `L3 (Low)`: Discrepancy observed or dynamic computed style depending on viewport state.

---

## Output Token & Component Specification Template

```markdown
# Reverse Engineered UI Specification: <Component / Page Name>

## 1. Design Token Dictionary (CSS Variables)

```css
:root {
  /* Color Palette (Semantic) */
  --color-brand-primary: #2563eb;
  --color-surface-card: #ffffff;
  --color-text-primary: #0f172a;
  --color-text-secondary: #64748b;
  --color-border-subtle: #e2e8f0;

  /* Spacing Scale (4px System) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;

  /* Typography */
  --font-family-base: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --line-height-normal: 1.5;
  --font-weight-medium: 500;
  --font-weight-bold: 700;

  /* Elevation & Borders */
  --radius-md: 8px;
  --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
}
```

## 2. Component Atomic Breakdown: `<target-component>`

### State: Default
- **Shorthand CSS**:
  ```css
  padding: 12px 24px;
  background-color: var(--color-brand-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-card);
  ```
- **Atomic Decomposed Properties**:
  - `padding-top`: `12px` [L1]
  - `padding-right`: `24px` [L1]
  - `padding-bottom`: `12px` [L1]
  - `padding-left`: `24px` [L1]
  - `background-color`: `rgb(37, 99, 235)` (`#2563eb`) [L1]
  - `border-top-left-radius`: `8px` [L1]
  - `border-top-right-radius`: `8px` [L1]

### State: Hover / Focus
- `background-color`: `#1d4ed8` (transition: `background-color 150ms cubic-bezier(0.4, 0, 0.2, 1)`)

## 3. Responsive Breakpoints
- `sm`: `640px` (padding: 16px)
- `md`: `768px` (2-column layout)
- `lg`: `1024px` (max-width: 1200px container)
```

---

## Checkable Completion Criteria

- [ ] All colors formatted as exact HEX or RGBA values (no generic color names).
- [ ] Compound properties decomposed to indivisible W3C atomic units.
- [ ] Cohesion and coupling verified for all generated design tokens.
- [ ] Hover, focus, active, and disabled interactive states fully covered.
