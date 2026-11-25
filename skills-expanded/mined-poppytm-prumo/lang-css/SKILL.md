---
name: lang-css
description: CSS modern architecture, design token binding, cascade layers (@layer), container queries, zero unreviewed !important, and layout performance.
---

# CSS Modern Architecture & Performance Contract

## 1. Cascade Architecture & Layers
- Organize all global and component styles using CSS cascade layers (\`@layer reset, base, components, utilities\`).
- Prohibit \`!important\` in production stylesheets. If overriding third-party styles, encapsulate in an explicit \`@layer override\`.
- Leverage native CSS nesting with single-level or maximum two-level depth to prevent specificity explosion.

## 2. Design Tokens & Maintainability
- Bind all colors, spacing, typography, and motion to CSS custom properties (variables) defined at \`:root\` or token scope.
- Use logical properties (\`margin-inline\`, \`padding-block\`, \`inset-inline-start\`) to support internationalization and bi-directional text natively.

## 3. Layout Performance & Responsiveness
- Prohibit layout thrashing: animate only compositor-friendly properties (\`transform\`, \`opacity\`).
- Utilize \`contain: layout paint\` or \`content-visibility: auto\` for large off-screen list items.
- Implement responsive interfaces with fluid typography (\`clamp()\`) and container queries (\`@container\`).\n