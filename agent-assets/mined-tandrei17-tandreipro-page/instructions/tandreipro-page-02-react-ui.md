---
name: React UI
description: 'Use when implementing or changing React components, page UI, JSX, or CSS styles.'
applyTo: "src/**/*.tsx, src/**/*.css"
---

# React UI

- Before adding a component or hook, search `src/` for existing implementations to reuse or extend. Follow nearby component, import, naming, and CSS organization patterns.
- Preserve existing responsive behavior. Keep styles in the project's CSS files; do not add CSS-in-JS or Tailwind.
- Give each form control an associated visible label or accessible name. Add descriptive `alt` text to meaningful images and `alt=""` to decorative images.
- Keep TypeScript types precise and avoid introducing `any`. Use English camelCase for variables/functions and PascalCase for React components.
- For user-facing text, follow `04-localization.instructions.md`.
- Treat user input and API-provided content as untrusted. Do not use `dangerouslySetInnerHTML`; if rendering HTML is essential, sanitize it with an established sanitizer before it reaches the DOM.
- Use the existing Formik/Yup validation patterns for client-side usability, but rely on the server to validate input and enforce authorization; client validation is not a security boundary.
- Never store authentication tokens or sensitive session data in `localStorage` or `sessionStorage`. Do not introduce client-side secrets; all `VITE_*` values are public.
