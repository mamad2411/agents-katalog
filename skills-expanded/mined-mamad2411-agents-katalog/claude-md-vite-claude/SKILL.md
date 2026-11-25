# CLAUDE.md

## Project

Vite + TypeScript + Bootstrap 5 frontend. No framework (no React/Vue). Components are plain TypeScript functions that return/manipulate DOM elements.

## Stack

- **Bundler**: Vite
- **Language**: TypeScript
- **UI**: Bootstrap 5 (utility-first; minimize custom CSS)
- **Components**: vanilla TS — functions that return `HTMLElement`

## Structure

```
src/
  components/    # One file per component
  style.css      # Only what Bootstrap can't do
  main.ts        # Entry point
```

## Component Model

Components are TypeScript functions, not classes. They accept props as function parameters and return `HTMLElement`.

```ts
// Good
export function Header(productName: string): HTMLElement { ... }

// Bad — no classes, no globals
```

Props come from function params. No hardcoded strings inside components.

## Bootstrap-First Rule

Use Bootstrap utilities before writing any CSS. Custom CSS in `style.css` is a last resort and must be justified. If you're about to write CSS, ask: "Can a Bootstrap utility class do this?"

The goal is near-zero custom CSS. When custom CSS is needed (e.g. making sidebar truly full-height in a dynamic layout), document why Bootstrap alone isn't sufficient.

## Layout Patterns

Design layouts using Bootstrap's flex and grid utilities. Before writing any layout CSS, check if `d-flex`, `flex-grow-1`, `align-items-stretch`, `h-100`, `min-vh-100`, or grid columns cover it.

Common pitfalls to document in the project when they arise:
- Full-height columns: the parent row needs `align-items-stretch` and the child needs `h-100`
- Scroll breaking height: a `min-vh-100` on the root container is often the fix — comment why if added
- Background color inconsistency: set it via `bg-*` class on the element, not via CSS on a parent

Layout structure is project-specific. Document the chosen skeleton in the project README or an `agent_docs/layout.md` file.

## Theme

Theme is project-specific. Document the chosen theme (light/dark/custom) and any intentional per-component exceptions in `agent_docs/theme.md` when the project has one.

## Event Handling

Click listeners belong on the component that owns the element. If a menu item triggers content rendering, the listener is on the menu component and it calls a render function passed in as a callback param.

## Component Decomposition

Avoid God components. If a component handles multiple tabs, each tab's content is its own component. Rule of thumb: one responsibility per file.

When a component will later need API integration, design the UI layer so data flows in via params — don't hardcode API calls into the component. This makes swapping in real data painless.

**Tab/form components:** each tab is a component; each form is a component. Field definitions are typed objects (array of field descriptors), not hardcoded HTML blocks.

## Forms

Use Bootstrap form classes (`form-label`, `form-control`, `form-select`, etc.). Define fields as data:

```ts
const fields = [
  { id: "name", label: "Name", type: "text" },
  { id: "rate", label: "Rate", type: "number" },
]
// then render from this array — don't repeat HTML per field
```

## What to check if something looks wrong

- White background not applying → check parent has `bg-white` or `bg-light`, not just `main`
- Sidebar not full height → check row has `align-items-stretch` and sidebar col has `h-100`
- Width mismatch between sidebar and content → confirm both are inside the same flex row with no conflicting widths
- Dark component when everything else is light → check for `data-bs-theme="dark"` on that element
