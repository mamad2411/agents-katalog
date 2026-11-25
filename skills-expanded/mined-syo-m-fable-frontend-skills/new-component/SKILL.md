---
name: new-component
description: Scaffolds a new UI component the repo-standard way — component + styles + Storybook story with play function (+ unit test only for extracted pure logic), wired to design tokens and a11y checks. Use when creating a new component from scratch or implementing one from a Figma design. 日本語の依頼例:「新しいコンポーネント作って」「◯◯コンポーネント追加」「Figmaのこれ実装して」。
---

# New component pipeline

Produce the full set in one pass — a component without its story is not done. Load `react-patterns` + the project's styling skill (the "Styles, design tokens, responsive" row in the CLAUDE.md index; if no such row exists — minimal profile — follow the Stack section's styling line: the project's existing approach, consistently) (+ `design-system` for shared components, `a11y` for custom widgets); this file is the order of operations.

## Steps

1. **Locate & name** — follow the repo's existing component directory convention (check siblings first — repo convention beats this file). One directory: `Component.tsx`, `Component.stories.tsx`, plus the styling file the active styling skill prescribes (e.g. `Component.module.css` under CSS Modules; none under Tailwind).
2. **Contract first** — write the props type: required props minimal, variants as unions (not booleans that multiply), events named `onX`. No `any`; state stays out unless the component owns it.
3. **Markup** — semantic element first (`button`, not `div onClick`). Custom widget? Full keyboard contract + roles/states per `a11y` before any styling.
4. **Styles** — per the active styling skill: consume design tokens (never raw values), variants via `data-*`/`aria-*` attributes, responsive per that skill's rules. No inline styles.
5. **Story** — CSF3, one story per meaningful state (default, each variant, error/disabled, loading, empty). Interactive behavior gets a play function — that IS the component test. Include a keyboard-path assertion for interactive components.
6. **Unit tests** — only for pure logic extracted out of the component (formatting, reducers). Do not duplicate what the play function covers.
7. **Verify** — typecheck, lint, run the story tests. Check the story renders every state without console errors.

## Definition of done

Component + module CSS + stories with play function all exist, all gates in step 7 pass, tokens used throughout, keyboard path covered. If asked for "just the component, quickly" — still deliver the story; drop only the optional extras and say so.
