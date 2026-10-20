---
description: "Use when editing the theme system, adding UI themes, introducing themed components, changing CSS custom-property naming, or modifying files under src/share/utils/theme, src/share/types/theme, src/assets/css/theme, or theme-aware form components."
applyTo: "src/share/utils/theme/**,src/share/types/theme/**,src/assets/css/theme/**,src/layouts/Layout.astro,src/components/form/InputField.astro,src/components/form/InputLabel.astro,src/components/form/InputText.astro,src/pages/index.astro"
---

# Theme System Guidelines

## Purpose

This project uses a typed component theme system that converts structured theme config into CSS custom properties injected globally by the layout.

The system must stay:

- typed while authoring themes
- reusable across shared field-shell components
- explicit about shared vs component-specific tokens
- easy to extend without turning one file into a dumping ground
- capable of supporting theming for any new reusable component

## Optional Custom Themes

Custom themes are optional in this project.

- Do not assume at least one named custom theme exists in `UI_THEMES`.
- Runtime behavior must remain valid when `UI_THEMES` is empty.
- Tests must not hardcode a required custom theme name (for example `warm`) unless the test is explicitly about that concrete sample theme.
- Prefer dynamic assertions based on discovered theme names where applicable.

## Source Of Truth

When editing the theme system, align with these files:

- `src/share/utils/theme/uiThemes.ts` — actual named theme data
- `src/share/types/theme/uiThemes.ts` — registry of themeable components
- `src/share/utils/theme/createComponentThemeCss.ts` — composition point for style-var generators
- `src/share/utils/theme/theme.ts` — theme resolution and runtime CSS creation
- `src/share/utils/theme/form/inputFieldConfig.ts` — shared field-shell style vars
- `src/share/utils/theme/form/inputTextConfig.ts` — InputText-only style vars and pass-through helpers
- `src/share/types/theme/form/inputField.ts` — shared field-shell config type
- `src/share/types/theme/form/inputText.ts` — InputText config and pass-through types
- `src/assets/css/theme/input-field.css` — default shared field-shell token values
- `src/assets/css/theme/base-input.css` — default text-control token values shared by text-like controls

## Architecture Rules

**Quick reference — key constraints:**

1. Separate shared field-shell tokens (`input-field-*`) from control-specific tokens (`input-control-*`).
2. `InputField` is the reusable shell for text-like controls; do not force checkbox/radio into it.
3. One type file per component; mirror the `src/components/<category>/` folder structure.
4. `*StyleConfig` must be a nested object keyed by `pt` slot names — never a flat object.
5. Every themed component must be registered in `UIThemeComponentsConfig`.
6. Use `as const satisfies Record<string, UIThemeConfig>` for typed theme authoring.
7. New reusable components must be theme-capable by design from the start.

### 1. Separate shared shell styling from control-specific styling

Use `input-field` tokens for styling that belongs to the reusable field shell:

- root spacing
- wrapper background, border, hover, focus, error, disabled
- label colors and background
- icon color and disabled opacity
- help and error text colors

Use `input-control` tokens only for text-control-specific styling:

- input text color
- input padding block
- placeholder colors
- disabled text color

Do not put shared field-shell styling under `input-text-*` names.

### 2. Treat InputField as the reusable shell for text-like controls

`InputField` is intended to support:

- InputText
- InputEmail
- InputPassword
- Textarea
- Select

Do not force checkbox or radio into this shell unless the structure is intentionally redesigned for them.

### 3. Keep type files narrow and component-specific

Do not reintroduce one catch-all `form.ts` for all themed controls.

Use this split:

- `form/shared.ts` for primitives like `ClassValue`, `StyleValue`, `PassThroughAttributes`
- `form/inputField.ts` for shared field-shell config
- `form/inputText.ts` for InputText-specific config and pass-through types
- future form components should get their own files such as `form/select.ts`, `form/textarea.ts`, `form/inputPassword.ts`

**Mirror the component folder structure for theme files.**

The folder layout under `src/share/types/theme/` and `src/share/utils/theme/` must mirror `src/components/`:

| Component location | Type file location | Config/utils location |
|---|---|---|
| `src/components/form/InputText.astro` | `src/share/types/theme/form/inputText.ts` | `src/share/utils/theme/form/inputTextConfig.ts` |
| `src/components/misc/Chips.astro` | `src/share/types/theme/misc/chips.ts` | `src/share/utils/theme/misc/chipsConfig.ts` |

Rule: **any new themed component under `src/components/<category>/` gets its type and config files under the matching `<category>/` subfolder** — never flat in the theme root.

### 4. Theme config shape must mirror the `pt` slot structure

When a component accepts a `pt` prop, its `*StyleConfig` type **must** be a nested object whose top-level keys are the `pt` slot names — never a flat object.

```ts
// ✅ Correct — one sub-config type per pt slot
export interface MyComponentStyleConfig {
  root?: MyComponentRootStyleConfig;       // pt.root → root element
  icon?: MyComponentIconStyleConfig;       // pt.icon → icon element
  label?: MyComponentLabelStyleConfig;     // pt.label → label element
  action?: MyComponentActionStyleConfig;   // pt.action → action element
}

// ❌ Wrong — flat config has no mapping to slots
export interface MyComponentStyleConfig {
  backgroundColor?: string;
  iconColor?: string;
  labelFontWeight?: string;
}
```

Rules:

- Every pt slot that can be styled gets its own dedicated sub-config type.
- Each sub-config type holds real visual properties (color, fontSize, fontWeight, borderRadius, etc.).
- Do not use an empty `interface` for a slot sub-config. Use a `type` alias with at minimum one property. Slots with no styleable properties yet may temporarily be `type XxxStyleConfig = Record<string, never>`, but prefer adding real properties immediately.
- The `create*StyleVars` generator must read `config.slotName?.property` paths matching this shape.
- In `UI_THEMES`, theme overrides use the same nested shape, giving authors direct alignment with the `pt` API.
- If an existing component has a flat `*StyleConfig`, restructure it to nested before adding new tokens.

### 5. Keep theme registration centralized

Every component that can appear inside `UI_THEMES` must be registered in `src/share/types/theme/uiThemes.ts`.

Autocomplete inside `UI_THEMES` depends on `UIThemeComponentsConfig`.

If a component is not registered there, theme authoring for that component is incomplete.

### 5. Keep theme authoring typed

Use the typed `as const satisfies Record<string, UIThemeConfig>` pattern in `src/share/utils/theme/uiThemes.ts`.

Do not replace it with an untyped object or broad `Record<string, unknown>` shape.

The authoring experience should provide autocomplete for nested theme config keys while editing theme objects.

Also keep token contracts aligned across these three places:

- generated declarations in `src/share/utils/theme/form/inputTextConfig.ts`
- consumed variables in `src/components/form/InputField.astro`
- default values in `src/assets/css/theme/base-input.css`

Do not rename one side of this contract without updating the others.

### 5.1 Prefer shared key/value helper aliases in theme type aliases

When deriving exported key or value aliases inside theme-system TypeScript files, prefer shared helpers from `src/share/types/index.ts`:

- use `Keyof<T>` instead of raw `keyof T`
- use `ValueOf<T>` instead of manual indexed unions like `T[keyof T]`

This keeps type alias style consistent across theme utilities and avoids mixed patterns in public theme typings.

### 6. New reusable components must be theme-capable by design

When creating a new reusable component, do not hardcode a styling model that blocks theming.

Required approach:

- ask whether the user wants theme wiring implemented now
- if yes, implement full theme support in the same task
- if not now, keep the component styling and API ready for future theme wiring with minimal refactor

Theme-ready means:

- styling surfaces are controlled by CSS custom properties
- config types can be added in `src/share/types/theme/...` without breaking component API
- style-var generation can be attached in `src/share/utils/theme/...`

## Naming Rules

### Shared field shell tokens

Use:

- `--input-field-root-gap`
- `--input-field-wrapper-*`
- `--input-field-label-*`
- `--input-field-icon-*`
- `--input-field-help-*`
- `--input-field-error-*`

### InputText-only tokens

Use text-control tokens:

- `--input-control-input-*`

### Future component-specific tokens

For new components, use the narrowest correct namespace:

- `--select-*`
- `--textarea-*`
- `--input-password-*`

Do not use a component-specific namespace for styling that belongs to the shared field shell.

## How To Add A New Theme Name

If you are only adding a new named theme and not a new component:

1. Edit `src/share/utils/theme/uiThemes.ts`
2. Add a new top-level theme entry next to existing themes
3. Override only the component values that differ from defaults
4. Preserve the existing typed shape
5. Run `pnpm run type:check`

Prefer sparse overrides. Do not duplicate all default values into every theme.

## How To Add A New Themed Component

**Summary — files to create or edit per step:**

| Step | File to create or edit |
|------|------------------------|
| 1 | Decide on shell reuse (no file) |
| 2 | Identify `src/components/<category>/` location (no file) |
| 3 | Create `src/share/types/theme/<category>/<componentName>.ts` |
| 4 | Edit `src/share/types/theme/uiThemes.ts` |
| 5 | Create `src/share/utils/theme/<category>/<componentName>Config.ts` |
| 6 | Add defaults to `src/assets/css/theme/<component>.css` |
| 7 | Edit `src/share/utils/theme/createComponentThemeCss.ts` |
| 8 | Edit component CSS to consume generated variables |
| 9 | Add or update tests |
| 10 | Run `pnpm run type:check` |
| 11 | Verify 100% coverage for modified theme logic |
| 12 | Update the component reference in `src/content/theme-guides/` |

Follow this sequence.

1. Decide whether the component reuses `InputField` or needs a unique structure.
2. Determine the component's category folder (e.g. `form`, `misc`) by looking at its location under `src/components/<category>/`.
3. Create a dedicated type file at `src/share/types/theme/<category>/<componentName>.ts`.
4. Register the component in `src/share/types/theme/uiThemes.ts`.
5. Create a style-var generator at `src/share/utils/theme/<category>/<componentName>Config.ts`.
6. Add default CSS variable values under `src/assets/css/theme/` if the component introduces new tokens.
7. Add the generator to `src/share/utils/theme/createComponentThemeCss.ts` if it participates in runtime theme output.
8. Use the generated CSS variables in the component CSS.
9. Add or update tests.
10. Run `pnpm run type:check`.
11. Ensure relevant tests pass and changed theme-related logic has 100% coverage in focused tests for the modified behavior.
12. Update the component reference doc in `src/content/theme-guides/` — bump `updatedAt`, reflect any new/changed keys in the Style Config Keys block and CSS Custom Properties block.

### Keep component reference docs in sync

Whenever you add, rename, or remove a key in a `*StyleConfig` type or a `--*` CSS custom property for a component that has a reference entry under `src/content/theme-guides/`, you **must** update that reference in the same change:

- **Style Config Keys block** — reflect the added/removed keys.
- **CSS Custom Properties block** — reflect the added/removed tokens.
- **Code examples** — update any snippets that use removed or renamed keys/tokens.
- **`updatedAt` frontmatter field** — bump to today's date.

Reference files by component:

| Component | Reference file |
|-----------|---------------|
| InputField / InputText | `src/content/theme-guides/input-field-reference.md` |
| InputText (control-specific) | `src/content/theme-guides/input-text-reference.md` |
| Chips | `src/content/theme-guides/chips-reference.md` |

Do not ship a config change without updating the corresponding reference.

## Composition Rules

`src/share/utils/theme/createComponentThemeCss.ts` is the place where style-var generators are composed.

Keep `src/share/utils/theme/theme.ts` orchestration-only.

### ComponentThemeCssMap is the single composition point

Every themed component must be registered as an entry in `componentThemeCssMap`. The map type is derived from `UIThemeComponentName` so TypeScript enforces that every registered component name has a creator — if you add a component to `UIThemeComponentsConfig` and forget to add it here, it is a compile error.

Do not use a single flat `createThemeCssFromStyleVars([...])` call that combines generators from different components. Each component has its own config type; mixing them into one array breaks type safety. Use one map entry per component instead:

```ts
export const componentThemeCssMap: ComponentThemeCssMap = {
  inputText: createThemeCssFromStyleVars([createInputFieldStyleVars, createInputTextStyleVars]),
  chips: createThemeCssFromStyleVars(createChipsStyleVars),
  // add new components here, one entry per component
};
```

Note: `inputText` uses an array because `InputTextStyleConfig` extends `InputFieldStyleConfig` — both generators share that same config type. Any other component with its own distinct config type always gets a single generator (or its own dedicated array if it has multiple generators of the same config type).

### No dead exports

Do not export aliases, wrappers, or backward-compatibility re-exports from `createComponentThemeCss.ts` unless they are actively imported by another file. Verify with usages before creating any new export from this file.

### No `any` and no `eslint-disable` comments

Do not use `any` or suppress lint/type errors with `// eslint-disable` or `// @ts-ignore` comments anywhere in the theme system.

When a generic cast seems necessary (for example, pairing `getThemeComponent` with `componentThemeCssMap`), capture the type parameter precisely instead. Use a small typed helper:

```ts
function createTypedComponentResolver<K extends UIThemeComponentName>(
  name: K,
  resolvedThemeName: UIThemeName,
) {
  return createComponentThemeResolver<UIThemeComponents[K], UIThemeName>({
    getThemeByName: (themeName: UIThemeName) => getThemeComponent(themeName, name),
    createThemeCss: componentThemeCssMap[name],
    selector: 'html:root',
  });
}
```

Capturing `K extends UIThemeComponentName` lets TypeScript prove `getThemeComponent(themeName, name)` and `componentThemeCssMap[name]` share the same `UIThemeComponents[K]` type without any cast.

If composition grows substantially, prefer extracting clearer named composition helpers instead of growing `theme.ts` with arrays and conditional logic.

## Runtime Flow

The runtime flow must stay:

1. Theme name is passed into `Layout.astro`
2. `getComponentsThemeCss(themeName)` resolves the theme
3. Each component config is converted into CSS declarations
4. CSS is injected globally by the layout

Do not introduce parallel theming paths unless there is a documented and approved project requirement.

The project intentionally removed `FormStyleProvider` to keep a single theming path.

## What Not To Do

- Do not put all future themed control types back into one file.
- Do not use `input-text-*` for shared field-shell tokens.
- Do not add a component to `UI_THEMES` without adding it to `UIThemeComponentsConfig`.
- Do not generate unused theme values that are never consumed by CSS.
- Do not add local wrapper-based theme systems when the global theme pipeline already solves the problem.
- Do not clone the full InputText theme stack for `InputEmail` or `InputPassword` if they can reuse `InputField`.
- Do not use a single flat `createThemeCssFromStyleVars([...])` array to combine generators from different components with different config types. Use `componentThemeCssMap` with one entry per component.
- Do not export aliases or backward-compatibility re-exports from `createComponentThemeCss.ts` unless they are actively used. No dead exports.

## Validation

After editing the theme system, run at minimum:

- `pnpm run type:check`

When changing theme utilities or token generation:

- run the relevant tests
- ensure those tests pass
- ensure changed theme-related logic is covered 100% in focused tests for the modified behavior
