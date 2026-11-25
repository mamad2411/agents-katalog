---
name: design-systems
description: Builds and maintains design systems and shared component libraries, covering design tokens, theming and dark mode, component API design, loading, empty, error and disabled states, built-in accessibility, documentation, visual regression tests and semver releases with deprecations. Use when creating or refactoring a UI component library, defining tokens or themes, reviewing a shared component's props, or planning a breaking change to shared UI. Not for styling a single page.
license: MIT
---

# Design Systems

A design system is a product whose users are other developers and designers. Its job is to make the accessible, on-brand choice the easiest one. Encode decisions in tokens, keep component APIs small and consistent, and never break consumers without a deprecation path.

## When to use

- Starting a shared component library or extracting one from an app.
- Defining or restructuring design tokens, themes, dark mode, or multiple brands.
- Designing or reviewing the props of a shared component.
- Planning a release with breaking changes, or migrating apps to a new version.

Not for: one-off page styling. For accessibility details use web-accessibility; for React specifics use react-patterns; for type design use typescript-patterns.

## Is a full design system warranted?

| Situation | Do this |
| --- | --- |
| One app, one team | A shared `components/` folder plus tokens as CSS custom properties. No separate package yet |
| Several apps or teams on one framework | A versioned package with docs, tests and a release process |
| Several frameworks (React, Vue, native mobile) | Shared tokens generated for every platform; components per framework, or Web Components where they fit |

Promote a component into the system after the same need shows up in about three places. Earlier abstraction usually guesses the API wrong.

## Workflow

1. **Inventory** the existing UI: repeated components, every distinct color, font size, spacing value, radius and shadow. Duplicates and near-duplicates show where tokens are missing.
2. **Define tokens first** (primitive, then semantic). Components come after.
3. **Build the most-used components first** (button, input, select, checkbox, dialog, layout primitives). Each one gets an API review, accessibility checks, docs and tests before release.
4. **Release with semver and a changelog.** Breaking changes ship with a migration guide and, for renames, a codemod where practical.
5. **Measure adoption** and remove what nobody uses.

## Tokens

| Tier | Example | Who uses it |
| --- | --- | --- |
| Primitive | `color.blue.600 = #2563eb`, `space.4 = 16px` | Only semantic tokens |
| Semantic | `color.text.primary`, `color.bg.danger`, `color.border.focus`, `space.inset.md` | Components and app code |
| Component (optional, sparingly) | `button.primary.bg` | One component |

Rules:

- Components consume **semantic tokens only**. A theme is a different mapping from semantic to primitive tokens; if a component uses a primitive directly, theming breaks.
- Name by purpose, not value: `color.text.muted`, never `color.grey5` or `blue-text`.
- Use a predictable pattern such as `category.property.variant.state` (`color.bg.surface.hover`).
- Cover color, typography (family, size, line height, weight), spacing scale, radius, elevation/shadow, motion (duration, easing), z-index layers, and breakpoints.
- Keep one source of truth (JSON) and generate platform outputs (CSS custom properties, JS, iOS, Android) with a build tool such as Style Dictionary. The W3C Design Tokens Community Group (DTCG) format, stable since version 2025.10, is the common interchange format; check which version your build tool supports.

Read [references/tokens.md](references/tokens.md) when creating or restructuring tokens; it has a naming scheme, a JSON example and a dark-theme mapping.

## Theming and dark mode

```css
:root {
  color-scheme: light;
  --color-bg-surface: #ffffff;
  --color-text-primary: #111827;
  --color-border-focus: #2563eb;
}
[data-theme="dark"] {
  color-scheme: dark;
  --color-bg-surface: #111827;
  --color-text-primary: #f9fafb;
  --color-border-focus: #60a5fa;
}
.card {
  background: var(--color-bg-surface);
  color: var(--color-text-primary);
}
```

- Dark mode is a second palette, not inverted colors. Re-check contrast for every text/background pair in every theme (WCAG 2.2 AA: 4.5:1 for normal text, 3:1 for large text and UI component boundaries).
- Respect the OS preference by default (`prefers-color-scheme`) and let users override it.
- Prevent a flash of the wrong theme: set `data-theme` before first paint (server-rendered from a cookie, or a tiny inline script in `<head>`).
- Multiple brands use the same semantic tokens with different primitive mappings.

## Component API rules

- **Consistent names across components**: `size`, `variant`, `disabled`, `value` / `defaultValue` / `onChange`, `open` / `defaultOpen` / `onOpenChange`.
- **Variants as one enum prop**, not booleans: `variant="primary" | "secondary" | "danger"` instead of `primary`, `secondary`, `danger` flags that allow impossible combinations.
- **Composition over configuration**: compound components or slots (`<Card><Card.Header/><Card.Body/></Card>`) instead of `headerTitle`, `headerIcon`, `headerActions` props.
- **Controlled and uncontrolled**: accept `value` + `onChange` for control, and `defaultValue` for simple use.
- **Pass through native attributes** to the root element (`...rest`), forward refs, and merge `className`/`style` instead of replacing them.
- **Polymorphism with care**: an `as` prop is flexible but complicates types and invites broken semantics (`<Button as="div">` loses keyboard behavior). Prefer an `asChild`/slot pattern or restrict the allowed elements.
- **No outer margins inside components.** Spacing between components belongs to the parent; provide layout primitives (Stack, Inline, Grid) that use spacing tokens.
- **Name events by intent** (`onSelect`, `onDismiss`), not by DOM detail.
- **Every new prop is a support commitment.** Ask for two real use cases before adding one.

## Accessibility built in

- Build on the correct native elements (`<button>`, `<input>`, `<dialog>`), or on a headless accessible primitives library (for example React Aria, Radix UI, Headless UI) for complex widgets such as combobox, menu, tabs and date picker. Hand-rolled ARIA for these is where most bugs come from.
- Every interactive component supports the keyboard, shows a visible focus indicator from a focus token, and respects `prefers-reduced-motion`.
- Make the accessible name impossible to forget: an icon-only button's type requires `aria-label` (or a `label` prop).
- Run automated accessibility checks (axe) on every story or component test, and do a keyboard pass on new components. See web-accessibility for the full checklist.

## Component states

Every component that shows data or accepts input must define each state below explicitly: in the API, in the design, in a story, and in a test. Undefined states are where products look broken.

| State | Visuals | ARIA and semantics | Focus | Copy |
| --- | --- | --- | --- | --- |
| Default | Uses semantic tokens only | Correct native element and accessible name | Visible focus indicator from the focus token | Clear label; no placeholder-as-label |
| Loading | Skeleton or spinner that keeps the final layout size (no layout shift); show it only after a short delay so fast responses don't flicker | `aria-busy="true"` on the region being updated; skeleton shapes `aria-hidden="true"`; announce long operations through a polite live region | Do not move focus; a loading button keeps focus and its width | Say what is happening ("Saving...") when it takes more than a moment |
| Empty | Distinct design, not a blank area | Plain text content, reachable by screen readers | Focus the primary action only if the user just triggered the empty result | Say why it is empty and what to do next; "no data yet" and "no results for these filters" are different messages |
| Error | Error token colors plus an icon or text (never color alone) | Field errors: `aria-invalid="true"` and `aria-describedby` pointing to the message. Async or page errors: `role="alert"` or a live region | After a failed submit, move focus to the first invalid field or an error summary | Say what went wrong and how to fix it; offer retry where it makes sense; no raw error codes alone |
| Disabled | Muted tokens (inactive controls are exempt from WCAG contrast minimums, but must still look disabled) | Native `disabled` removes the control from tab order and blocks events. Use `aria-disabled="true"` instead when users must still discover the control or a tooltip must explain why; then block activation in code | `disabled`: not focusable. `aria-disabled`: stays focusable | Explain why it is unavailable when the reason is not obvious |

Rules:

- A button in a loading or submitting state blocks repeat activation (use `aria-disabled="true"` plus an early return, so focus is not lost).
- Never show loading, empty and error at the same time; model the state as one value (`status: "idle" | "loading" | "success" | "empty" | "error"`), not separate booleans.
- Keep partial data visible while refreshing, and show an inline error for a failed refresh instead of wiping the content.
- Each state gets a story and a visual regression baseline, in every theme.

Read [references/component-states.md](references/component-states.md) when building data-driven components (tables, lists, forms, async buttons); it has per-component state checklists and markup examples.

## Documentation

For each component:

- Purpose, when to use it, and when to use something else.
- Live examples of every variant and state (default, hover, focus, disabled, loading, error, empty, long text).
- Props table generated from the types.
- Keyboard interactions and accessibility notes.
- Do / don't examples.

A workshop tool such as Storybook lets the same stories serve as documentation, interaction tests and visual regression fixtures.

## Testing

| Test | What it catches |
| --- | --- |
| Interaction tests (Testing Library, queries by role) | Broken behavior and semantics |
| Automated accessibility checks (axe) per story | Missing names, roles, contrast issues |
| Visual regression (screenshot comparison, for example Playwright `toHaveScreenshot` or a hosted service) | Unintended visual changes; run on every PR and review diffs |
| Theme and direction matrix | Each story in light, dark, and RTL |
| Type tests | Public prop types stay compatible |

## Versioning and deprecation

- Follow semver. Breaking: removing or renaming a prop, component or token; changing a default; changing DOM structure or class names consumers can target; visual changes that alter size or layout.
- Deprecate before removing: mark with `@deprecated` in types/JSDoc, log a development-only warning, keep it for at least one major version, and document the replacement.
- Provide codemods for mechanical renames.
- Generate changelogs from change descriptions (for example with Changesets).
- Declare framework libraries as `peerDependencies` so apps do not end up with two copies of React.

## Adoption and contribution

- Publish a contribution path: proposal, design review, API review, build, docs, release.
- Track adoption: imports of system components versus local look-alikes, and lint rules that flag raw hex colors or deprecated components (stylelint, ESLint custom rules).
- Hold regular office hours and help teams migrate. A system that lags behind product needs gets bypassed.

## Anti-patterns

- **Tokens named by value** (`blue500` used as "primary").
- **Components using primitive tokens or hard-coded colors**, so themes do not apply.
- **Boolean prop explosion** and props that conflict with each other.
- **Clickable `div`s** instead of buttons and links.
- **Margins baked into components.**
- **Breaking changes in a minor release**, or removals without a deprecation period.
- **Forking the library per app** instead of contributing back.
- **Shipping without docs and examples.** Undocumented components get reimplemented.
- **Building the system before there are real, repeated use cases.**

## Done when

- Tokens come from one source and generate every platform output; components use semantic tokens only.
- Every theme passes contrast checks for all semantic text and border pairs.
- Each released component has docs, stories for all states, interaction and axe tests, and a visual regression baseline.
- Every data or input component defines default, loading, empty, error and disabled states with the visuals, ARIA, focus behavior and copy from the state table.
- Releases follow semver with a changelog; every deprecation names its replacement and removal version.

## References

- [references/tokens.md](references/tokens.md) — read when defining, renaming or theming tokens.
- [references/component-states.md](references/component-states.md) — read when building tables, lists, forms or async buttons, to cover every state.
