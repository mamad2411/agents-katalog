---
name: css-reset
description: Applies a modern CSS reset covering box-sizing, margin removal, text rendering, media defaults, and root stacking context. Use when starting a new web project, creating a global stylesheet, or when the codebase lacks sensible CSS defaults.
---

# css-reset

Include this reset at the top of your global stylesheet for every new web project. Each rule addresses a specific browser default that causes layout or rendering inconsistencies.

```css
/* 1. Use a more-intuitive box-sizing model */
*, *::before, *::after {
  box-sizing: border-box;
}

/* 2. Remove default margin */
*:not(dialog) {
  margin: 0;
}

/* 3. Enable keyword animations */
@media (prefers-reduced-motion: no-preference) {
  html {
    interpolate-size: allow-keywords;
  }
}

body {
  /* 4. Increase line-height */
  line-height: 1.5;
  /* 5. Improve text rendering */
  -webkit-font-smoothing: antialiased;
}

/* 6. Improve media defaults */
img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

/* 7. Inherit fonts for form controls */
input, button, textarea, select {
  font: inherit;
}

/* 8. Avoid text overflows */
p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}

/* 9. Improve line wrapping */
p {
  text-wrap: pretty;
}
h1, h2, h3, h4, h5, h6 {
  text-wrap: balance;
}

/* 10. Create a root stacking context */
#root, #__next {
  isolation: isolate;
}
```

## Notes

- Rule 3 (`interpolate-size: allow-keywords`) enables CSS transitions to/from keyword sizes like `auto` and `fit-content`. Broadly supported as of 2024; guarded by `prefers-reduced-motion` since it only matters for animations.
- Rule 9 (`text-wrap: pretty/balance`) is progressive enhancement — no effect in older browsers, no downside.
- Rule 10: `#root` targets React apps, `#__next` targets Next.js. Adjust the selector for other frameworks.
