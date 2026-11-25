---
name: color-contrast
description: Meet WCAG 2.2 AA contrast ratios; never use color as the only visual signal
---

# Color Contrast

WCAG 2.2 SC 1.4.3 (Contrast — Minimum, Level AA) and SC 1.4.11 (Non-text Contrast, Level AA) set the baseline. Color blindness affects roughly 8% of men and 0.5% of women; insufficient contrast degrades readability for everyone in bright environments.

## Contrast ratio requirements (WCAG 2.2 AA)

| Content type | Minimum ratio |
|---|---|
| Normal text (< 18pt / < 14pt bold) | 4.5:1 |
| Large text (≥ 18pt / ≥ 14pt bold) | 3:1 |
| UI components (borders, icons, focus indicators) | 3:1 against adjacent color |
| Disabled elements | Exempt (but prefer 3:1 where possible) |
| Decorative elements | Exempt |
| Logotypes | Exempt |

## Rules

- **Never use color as the only way to convey information.** Error states, required fields, active tabs, and graph series must also be distinguishable by text label, icon, pattern, or shape. WCAG 1.4.1 (Use of Color, Level A).
- **Verify contrast with computed colors, not design tokens.** A token named `--color-muted` may pass in light mode and fail in dark mode. Check both.
- **Placeholder text must meet 4.5:1.** Browsers default to ~3.5:1 for `::placeholder`; override it explicitly.
- **Hover and focus states must also meet minimum contrast.** A blue button that turns light-grey on hover may drop below 3:1.
- **Semi-transparent colors are measured against the actual rendered background**, not the base color. `rgba(0,0,0,0.5)` on white = `#808080`, which fails at 3.95:1 against white.

## Examples

```css
/* BAD — #767676 on white is exactly 4.48:1, just below the 4.5:1 threshold */
.body-text {
  color: #767676;
}

/* GOOD — #595959 on white is 7.0:1, comfortably AA */
.body-text {
  color: #595959;
}

/* BAD — placeholder is too light */
::placeholder {
  color: #aaaaaa; /* ~2.3:1 on white */
}

/* GOOD */
::placeholder {
  color: #767676; /* 4.48:1 — just sufficient; #595959 preferred */
}
```

```tsx
// BAD — only color differentiates error from success
<span style={{ color: isError ? 'red' : 'green' }}>
  {message}
</span>

// GOOD — icon + color + text label
<span className={isError ? 'text-red-700' : 'text-green-700'}>
  {isError ? <ErrorIcon aria-hidden="true" /> : <CheckIcon aria-hidden="true" />}
  <span>{message}</span>
</span>
```

## Gotchas

- WCAG AA is the minimum; AAA (7:1 normal, 4.5:1 large) is aspirational for body text and worth the effort on critical information.
- Background images under text make contrast unpredictable. Add a solid background or overlay behind text on images.
- CSS `mix-blend-mode` and filters change rendered colors; measure in the browser's color picker, not the source stylesheet.
- Tools: browser DevTools accessibility panel, [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/), Figma's built-in contrast indicator, `axe-core` in CI.
