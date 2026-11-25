---
name: one-vue-component
description: 'Create new Vue components for the ONE.Vue design system library. Use when: creating a new component, adding a component to ONE.Vue, scaffolding component files, generating component boilerplate, adding sub-components. Covers: props, emits, SCSS theme, tests, docs, playground, resolver registration, and global exports.'
argument-hint: 'Component name in kebab-case (e.g. product-card, step-b2c)'
---

# ONE.Vue Component Creation Skill

Create fully integrated components for the ONE.Vue design system library following all project conventions, registrations, and quality checks.

## When to Use

- Creating a brand new component from scratch
- Adding a component with sub-components (parent + children)
- Scaffolding all required files for a new ONE.Vue component
- Whenever the user says "crear componente", "new component", "añadir componente"

## Conventions

| Concept         | Format                        | Example                        |
| --------------- | ----------------------------- | ------------------------------ |
| Folder          | kebab-case                    | `product-card/`                |
| Registered name | PascalCase with `One` prefix  | `OneProductCard`               |
| CSS classes     | kebab-case with `one-` prefix | `one-product-card`             |
| Namespace       | kebab-case (no prefix)        | `useNamespace('product-card')` |

> **Prefix is `One`, NOT `El`.**

## Procedure

Follow every step sequentially. Do NOT skip any step — missing a registration causes silent failures.

### Step 0 — Create Feature Branch

Before writing any code, create a dedicated branch from `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/<name>
```

See [git workflow reference](./references/git-workflow.md) for the full branching strategy, commit conventions, and MR process.

### Step 1 — Gather Requirements

Before writing code, determine:

- **Component name** (kebab-case): e.g. `my-component`
- **Props and their types**: strings, booleans, enums, complex objects
- **Events (emits)**: click, change, select, etc.
- **Slots**: default, named slots
- **Sub-components**: Does it need child components? (e.g. menu + menu-item)
- **Visual variants**: colors, sizes, states
- **Design reference**: Figma URL or design spec if available

### Step 2 — Create Component Source Files

Create files under `packages/components/<name>/`:

```
packages/components/<name>/
├── index.ts                    # Public exports
├── src/
│   ├── <name>.ts               # Props, emits, types
│   ├── <name>.vue              # Main component
│   ├── instance.ts             # TS instance type
│   ├── constants.ts            # Constants (optional)
│   └── use-<name>.ts           # Composable (optional)
├── style/
│   ├── index.ts                # SCSS import
│   └── css.ts                  # CSS import
└── __tests__/
    └── <name>.test.tsx         # Tests
```

Use the [templates reference](./references/templates.md) for the exact boilerplate of each file.

### Step 3 — Create Theme SCSS

1. **Define variables** in `packages/theme/src/common/var.scss` — see [SCSS variables reference](./references/scss-guide.md#variables)
2. **Create SCSS file** at `packages/theme/src/<name>.scss` — see [SCSS component reference](./references/scss-guide.md#component-scss)
3. **Register** in `packages/theme/src/index.scss`: add `@use './<name>.scss';`

### Step 4 — Global Registration (3 files)

See [registration reference](./references/registration.md) for details.

1. **`packages/components/index.ts`** — add `export * from './<name>'`
2. **`packages/one-vue/component.ts`** — add import and entry in the Plugin[] array
3. **`packages/theme/src/index.scss`** — add `@use './<name>.scss';` (if not done in Step 3)

### Step 5 — Resolvers (4 files) ⚠️ CRITICAL

Without this step, the component won't render in play/ or docs/. Add component names to `probedComponents` in:

1. `play/unplugin-vue-components/dist/resolvers.mjs`
2. `play/unplugin-vue-components/dist/resolvers.js`
3. `docs/unplugin-vue-components/dist/resolvers.mjs`
4. `docs/unplugin-vue-components/dist/resolvers.js`

See [resolver registration reference](./references/resolvers.md) for details.

### Step 6 — Tests

Create `__tests__/<name>.test.tsx` using Vitest + TSX. See [test reference](./references/templates.md#tests).

Run: `npx vitest run packages/components/<name>`

### Step 7 — Documentation

1. Create `docs/en-US/component/<name>.md` and `docs/es-ES/component/<name>.md`
2. Create example files in `docs/examples/<name>/`
3. **Add to sidebar navigation** — insert an entry `{ "link": "/<name>", "text": "<DisplayName>" }` in alphabetical order in:
   - `docs/.vitepress/crowdin/en-US/pages/component.json` → inside `basic.children`
   - `docs/.vitepress/crowdin/es-ES/pages/component.json` → inside `basic.children`
4. Run `pnpm docs:gen-locale` to regenerate the i18n files (this reads the crowdin JSONs and builds `docs/.vitepress/i18n/`)

See [documentation reference](./references/docs-guide.md).

### Step 8 — Playground

1. Create view: `play/src/views/<PascalName>.vue`
2. Create examples: `play/src/examples/<name>/`
3. Register route in `play/src/router/index.js`

### Step 9 — Validation

```bash
npx eslint --fix packages/components/<name>/
npx eslint packages/components/<name>/
npx vitest run packages/components/<name>
pnpm docs:gen-locale
pnpm dev  # Visual check at /#/<name>
```

### Step 10 — Commit, CHANGELOG and Merge Request

1. **Commit** following the conventional commit format: `feat(components): [<name>] description`
2. **Update CHANGELOG.md** — add an undated entry with the next version number
3. **Push** the branch and create a **Merge Request** targeting `main`
4. Request review from a maintainer (@ilainac, @rguerrerog, or @rarrieta)

See [git workflow reference](./references/git-workflow.md) for commit types, MR checklist, and detailed instructions.

## Known Issues

See [known issues reference](./references/known-issues.md) for common errors and workarounds (ESLint import order, useLicense in tests, mediaMd undefined mixin, etc.).

## Files Summary

| Action | File                                                   |
| ------ | ------------------------------------------------------ |
| Create | `packages/components/<name>/index.ts`                  |
| Create | `packages/components/<name>/src/<name>.ts`             |
| Create | `packages/components/<name>/src/<name>.vue`            |
| Create | `packages/components/<name>/src/instance.ts`           |
| Create | `packages/components/<name>/style/index.ts`            |
| Create | `packages/components/<name>/style/css.ts`              |
| Create | `packages/components/<name>/__tests__/<name>.test.tsx` |
| Create | `packages/theme/src/<name>.scss`                       |
| Modify | `packages/theme/src/common/var.scss`                   |
| Modify | `packages/theme/src/index.scss`                        |
| Modify | `packages/components/index.ts`                         |
| Modify | `packages/one-vue/component.ts`                        |
| Modify | `play/unplugin-vue-components/dist/resolvers.mjs`      |
| Modify | `play/unplugin-vue-components/dist/resolvers.js`       |
| Modify | `docs/unplugin-vue-components/dist/resolvers.mjs`      |
| Modify | `docs/unplugin-vue-components/dist/resolvers.js`       |
| Create | `docs/en-US/component/<name>.md`                       |
| Create | `docs/es-ES/component/<name>.md`                       |
| Create | `docs/examples/<name>/*.vue`                           |
| Create | `play/src/views/<PascalName>.vue`                      |
| Create | `play/src/examples/<name>/*.vue`                       |
| Modify | `play/src/router/index.js`                             |
