---
name: react-component
description: Generates complete, production-ready React/TypeScript components using Tailwind CSS. Use when building UI components in a React or Next.js project that requires TypeScript, Tailwind styling, and accessible interactions.
---

# react-component

Generates self-contained React/TypeScript components — plan first, confirm, then produce complete code with no placeholders.

## Workflow

1. **Plan**: Present a concise pseudocode implementation plan covering structure, state, and key logic.
2. **Confirm**: Verify requirements and constraints with the user before writing code.
3. **Code**: Write the full implementation. Leave no TODOs, placeholders, or missing pieces.

## Code Rules

- **Tailwind only** — no CSS files, no inline styles. All styling via Tailwind classes.
- **Conditional classes** — use `clsx` or concise template literals; avoid complex nested ternaries.
- **Handler naming** — prefix all event handlers with `handle`: `handleClick`, `handleKeyDown`.
- **Early returns** — use them wherever they improve readability.
- **Accessibility** — non-native interactive elements (e.g., `<div>`, `<span>`) must have `tabIndex={0}`, `aria-label`, `onClick`, and `onKeyDown`.
- **Types** — define prop types explicitly; avoid `any`.
- **Naming** — descriptive variable and function names throughout.

## Output Format

- One self-contained `.tsx` file with a default export
- All imports included, component properly named
- No prose outside the code block in the final answer
- Must compile in a standard React/Next.js project without modification
