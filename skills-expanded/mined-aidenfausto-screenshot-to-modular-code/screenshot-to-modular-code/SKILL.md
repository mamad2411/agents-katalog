---
name: screenshot-to-modular-code
description: Use when a user uploads a UI screenshot or mockup image and requests code implementation. Extract a structured UI spec first, then generate code module by module instead of dumping a whole page.
---

# Screenshot to Modular Code

Use this skill when a user provides a UI screenshot, mockup, or reference image and wants code.

Core rule: do not generate the whole page in one shot unless the user explicitly asks or the page is trivial. First extract a UI spec, then implement by modules.

## Workflow

### 0. Confirm implementation target

If working inside a repo, inspect existing stack, component library, style system, route/component conventions, and nearby pages first.

If no target is clear, ask one short question in the user's language: what is the target stack (e.g. Vue3, React, HTML, uni-app)?

If no stack context is available and the user does not specify, wait for one response before defaulting to plain HTML/CSS. User silence is not consent to proceed.

### 1. Extract UI spec from the image

Before writing code, output this structure:

```markdown
## UI Spec

### 1. Overall layout
- Layout type: grid / flex / absolute / mixed
- Page regions: header / sidebar / main / footer / modal / other
- Responsive clues: desktop / tablet / mobile / unknown

### 2. Color palette
| Role | HEX | Usage |
|---|---|---|
| Primary | #xxxxxx | ... |
| Secondary | #xxxxxx | ... |
| Background | #xxxxxx | ... |
| Text primary | #xxxxxx | ... |
| Text secondary | #xxxxxx | ... |
| Border/divider | #xxxxxx | ... |

### 3. Typography scale
| Level | Likely px/rem | Weight | Usage |
|---|---:|---:|---|
| Title | ... | ... | ... |
| Body | ... | ... | ... |
| Caption | ... | ... | ... |

### 4. Spacing system
- Base unit: 4px / 8px / other
- Outer padding: ...
- Component gap: ...
- Card padding: ...

### 5. Component inventory
List visible components from top to bottom, left to right:
1. `Header`: ...
2. `Sidebar`: ...
3. `Card`: ...
4. `Table/Form/Button/...`: ...

### 6. Interaction hints
- Clickable: ...
- Hoverable: ...
- Selectable/input: ...
- Navigation/action affordance: ...

### 7. Uncertainties
- ...
```

Use HEX values as close as possible. If exact extraction is impossible, mark values as approximate: `#1677ff approx`.

If the image is low-resolution, cropped, watermarked, or partially obscured, mark affected fields as `[unreadable]` and ask one targeted question before proceeding.

### 2. Split implementation plan

After the UI spec, split code into modules. Prefer this order:

1. Design tokens: colors, spacing, typography, radius, shadow. If working inside an existing project with design tokens already defined, skip this step and reuse existing variables.
2. Layout shell: `header / sidebar / main`.
3. Reusable primitives: button, card, tag, input, table row, icon wrapper.
4. Content modules: stats cards, charts, lists, forms, tables.
5. Page composition: assemble modules with mock data or real props.

For each module, state:

```markdown
### Module: Header
- Responsibility: ...
- Inputs/props: ...
- Output file: ...
- Depends on: tokens / primitives / project components
```

### 3. Generate code module by module

Implement one coherent module batch at a time. Good batches:

- `tokens + layout shell`
- `header + sidebar`
- `cards + metrics`
- `table/list/form`
- `final page composition`

Do not mix unrelated business logic into visual reconstruction. If data is needed, use a small local mock object and isolate it near the page entry.

## Code rules

- Match the screenshot first, but follow project conventions over generic examples.
- Reuse existing components, icons, CSS variables, utility classes, and layout primitives when present.
- Prefer semantic HTML and simple CSS Grid/Flexbox.
- Use CSS variables or project tokens for repeated colors, spacing, radius, and shadows.
- Avoid pixel-by-pixel absolute positioning except for decorative overlays that require it.
- Do not invent API calls, state machines, permissions, or routes.
- Do not add dependencies unless the user explicitly approves.
- Do not generate test files or Storybook stories unless explicitly requested.
- Keep components small and named by responsibility.
- Add standard block comments only where required by project/user rules; do not comment obvious markup.

## Verification

After implementation, verify at the nearest useful level:

- Static prototype: open/render and compare against the image. If rendering is not possible, list structural assumptions that could cause visual deviation.
- Existing app: run the relevant dev/build/lint command if available.
- UI fidelity: check layout regions, color tokens, spacing rhythm, component order, and interactive affordances.

Report only:

1. Changed files.
2. Implemented modules.
3. Verification result.
4. Known visual deviations.

## Anti-patterns

- Do not produce one giant component for a complex page.
- Do not skip the UI spec.
- Do not replace existing design system patterns with unrelated Tailwind/shadcn code.
- Do not overfit with random `top/left` values.
- Do not silently redesign colors, spacing, or component hierarchy.
