---
name: ng-lib
description: |
  Angular library generator for Nx monorepo. This skill should be used when creating new Angular libraries
  with @nx/angular:library generator. Handles feature libs (landing/feature-*), shared libs (landing/shared/*),
  and global shared libs (shared/*). Auto-prefills tags, directory, prefix, importPath based on project conventions.
  Triggers: "create lib", "new library", "generate library", "ng-lib", "/ng-lib"
---

# Angular Library Generator

Generate Angular libraries following project conventions with proper scoping and module boundaries.

## Quick Reference

| Scope           | Directory Pattern             | Tags                                  | Import Path                         |
| --------------- | ----------------------------- | ------------------------------------- | ----------------------------------- |
| Global shared   | `libs/shared/{name}`          | `scope:shared`, `type:{name}`         | `@portfolio/shared/{name}`          |
| Landing shared  | `libs/landing/shared/{type}`  | `scope:landing`, `type:shared-{type}` | `@portfolio/landing/shared/{type}`  |
| Landing feature | `libs/landing/feature-{name}` | `scope:landing`, `type:feature`       | `@portfolio/landing/feature-{name}` |

## Workflow

1. **Gather input** - Ask user for library name and purpose
2. **Classify** - Determine scope (global-shared, landing-shared, landing-feature)
3. **Prefill** - Auto-generate all options based on classification
4. **Confirm** - Show user the command before execution
5. **Execute** - Run nx generate command

## Interactive Questions

Ask user:

1. "What is the library name?" (e.g., `projects`, `data-access`, `ui`)
2. "What is the library's purpose?" (helps classify scope)
3. "Which scope?" - Offer options based on purpose:
   - **Feature** - Landing page section (projects, skills, experience, hero)
   - **Landing Shared** - Shared within landing app (data-access, ui, util, types)
   - **Global Shared** - Shared across FE+BE (types, utils, testing)

## Generator Options

Reference: `references/generator-options.md`

### Project Defaults (from nx.json)

```
linter: eslint
unitTestRunner: jest
style: scss (for components)
standalone: true
```

### Computed Options by Scope

**Global Shared** (`libs/shared/{name}`):

```bash
nx g @nx/angular:library {name} \
  --directory=libs/shared/{name} \
  --importPath=@portfolio/shared/{name} \
  --tags="scope:shared,type:{name}" \
  --prefix=shared \
  --standalone \
  --style=scss
```

**Landing Shared** (`libs/landing/shared/{type}`):

```bash
nx g @nx/angular:library {type} \
  --directory=libs/landing/shared/{type} \
  --importPath=@portfolio/landing/shared/{type} \
  --tags="scope:landing,type:shared-{type}" \
  --prefix=landing \
  --standalone \
  --style=scss
```

**Landing Feature** (`libs/landing/feature-{name}`):

```bash
nx g @nx/angular:library feature-{name} \
  --directory=libs/landing/feature-{name} \
  --importPath=@portfolio/landing/feature-{name} \
  --tags="scope:landing,type:feature" \
  --prefix=landing \
  --standalone \
  --style=scss
```

## Post-Generation

After generating, do the following:

1. Update `tsconfig.base.json` paths if not auto-added
2. Verify tags in `project.json`
3. **Fix `tsconfig.spec.json`** — The Nx generator defaults to `"module": "commonjs"` and `"moduleResolution": "node10"`, which breaks Angular package resolution (e.g., `@angular/core/testing`). Update to:
   ```json
   "module": "es2015",
   "moduleResolution": "bundler"
   ```
   This only applies to Angular/frontend libs. Pure backend or non-Angular shared libs (types, utils, errors) can keep `node10`.
4. Run `pnpm lint` to verify module boundaries

## File & Component Naming

All generated files/folders must follow the grammar in **`.context/patterns-file-structure.md`**
(`<entity>.[variant].<role|kind>.[spec].<ext>`, dot = structural boundary, dash = word-joiner). It is
lint-enforced (`fe-naming/filename-grammar` + `fe-naming/decorator-name-agreement`, **error** level for
landing + console).

- **Components:** the `@nx/angular:component` generator is pre-set in `nx.json` to emit the new shape —
  no `.component` suffix (`type: ""`), `OnPush`, `scss`, folder-per-component. Pass a grammar-correct
  **path** so the file lands dot-named in the right place, e.g.:
  ```bash
  nx g @nx/angular:component --path=libs/console/feature-project/src/lib/project.delete-dialog/project.delete-dialog
  # → project.delete-dialog.ts (class ProjectDeleteDialog, selector console-project-delete-dialog)
  ```
  Role/variant must come from the controlled vocab in §5 (console is allowlist-enforced; landing section
  names are open). Single-file artifacts (`*.types.ts`, `*.service.ts`, `*.tokens.ts`) sit flat at `src/`
  / `src/lib/` root — no folder, no `components/` bucket.
- **Class ↔ file ↔ selector** must agree (§6): file `x.y.ts` → class `XY` → selector `<prefix>-x-y`.
  The lint rule fails the build otherwise.

## Module Boundary Rules

Reference: `references/module-boundaries.md` for ESLint enforce-module-boundaries configuration.
