---
name: tooling-eslint-prettier
description: Use when configuring ESLint flat config + Prettier (or Biome as alternative) — rules for React/TS, plugin selection, prettier integration, monorepo.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: tooling
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [typescript, react, ts-vitest, pnpm-essentials, bun-essentials, tooling-git-advanced]
---

# ESLint + Prettier (and Biome, as the escape hatch)

**Iron Law: ESLint catches bugs; Prettier owns formatting. Don't let them fight — `eslint-config-prettier` strips conflict rules, and you NEVER enable `eslint-plugin-prettier`. One tool per concern.**

**Versions:** Current `eslint 9.x` (flat config only — legacy `.eslintrc` removed) · Current `prettier 3.x` · Current `biome 2.x` — _No LTS series. ESLint 9 dropped `.eslintrc._`formats; if`eslint.config.{js,mjs,ts}`isn't present, the install is broken. Prettier 3 made trailing-comma`all`the default and removed`jsx-bracket-line`. Biome 2 added monorepo configs and is now production-grade for TS/JS but still lacks an `eslint-plugin-react-hooks` equivalent for full rules-of-hooks coverage.\*

## Flat config — the only supported style

`eslint.config.mjs` at the repo root:

```js
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";
import prettier from "eslint-config-prettier";

export default tseslint.config(
  { ignores: ["dist", "build", "coverage", "**/*.generated.*"] },
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parserOptions: {
        projectService: true, // typescript-eslint 8+ — replaces `project: true`
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: { react, "react-hooks": reactHooks, "jsx-a11y": jsxA11y },
    settings: { react: { version: "detect" } },
    rules: {
      ...react.configs.flat.recommended.rules,
      ...react.configs.flat["jsx-runtime"].rules, // no `import React` needed since 17
      ...reactHooks.configs.recommended.rules,
      ...jsxA11y.configs.recommended.rules,
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/consistent-type-imports": ["error", { fixStyle: "inline-type-imports" }],
      "react/prop-types": "off", // TS handles props
    },
  },
  prettier, // MUST be last — strips formatting rules from everything above
);
```

### Why these plugins, in this order

| Plugin                      | Job                                                                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `@eslint/js`                | Recommended JS rules (`no-undef`, `no-unused-vars`, etc.)                                                                     |
| `typescript-eslint`         | TS parser + recommended TS rules. `recommendedTypeChecked` enables rules that need type info (the expensive but valuable set) |
| `eslint-plugin-react`       | JSX rules, exhaustive-deps-adjacent rules. Use the `flat` configs in v7+                                                      |
| `eslint-plugin-react-hooks` | Rules of Hooks + exhaustive-deps — non-negotiable for any React codebase                                                      |
| `eslint-plugin-jsx-a11y`    | Accessibility rules. Catches missing `alt`, bad ARIA, label issues                                                            |
| `eslint-config-prettier`    | Disables every formatting rule. Always last in the array, no exceptions                                                       |

### Why NOT `eslint-plugin-prettier`

It runs Prettier as a lint rule. Two problems: every formatting diff shows up as an "ESLint error" (noisy in editor squiggles), and ESLint reruns Prettier on every file change — measurably slower than running Prettier directly. The correct pipeline:

```
Prettier (on save / pre-commit)  →  formats the file
ESLint   (on save / pre-commit)  →  reports bugs only (formatting rules disabled)
```

## Prettier baseline

`.prettierrc` (or `prettier.config.mjs` if you need conditional logic):

```json
{
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "semi": true,
  "singleQuote": false,
  "trailingComma": "all",
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

`.prettierignore`:

```
dist
build
coverage
pnpm-lock.yaml
*.generated.*
```

Two non-obvious choices:

- **`printWidth: 100`** is opinionated. Some teams pick 80, some 120. Pick once and never argue about it again — that IS the point of Prettier.
- **`endOfLine: lf`** + a `.gitattributes` with `* text=auto eol=lf` prevents Windows checkouts from flipping every line.

## Monorepo layout (pnpm workspaces)

```
repo/
├── eslint.config.mjs    # root — base rules, applies everywhere
├── .prettierrc          # root — ONE config, do not override per-package
└── packages/<pkg>/eslint.config.mjs  # imports root, adds local overrides
```

```js
// packages/ui/eslint.config.mjs
import root from "../../eslint.config.mjs";
export default [...root, { files: ["src/**/*.tsx"], rules: { "react/no-unescaped-entities": "off" } }];
```

**Don't fragment Prettier config across packages.** Format consistency at the repo level is the point.

## Editor + pre-commit

`.editorconfig` (`indent_style = space`, `indent_size = 2`, `end_of_line = lf`, `insert_final_newline = true`) keeps non-Prettier files (`.py`, `.yaml`) consistent.

`.vscode/settings.json` (commit it — onboarding is friction reduction):

```json
{
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": { "source.fixAll.eslint": "explicit" },
  "eslint.useFlatConfig": true
}
```

Pre-commit: `lefthook.yml` (preferred over husky — single binary, no postinstall) runs `eslint --fix` then `prettier --write` on **staged files only**, then re-stages:

```yaml
pre-commit:
  parallel: true
  commands:
    eslint: { glob: "*.{js,jsx,ts,tsx,mjs,cjs}", run: "pnpm exec eslint --fix {staged_files}", stage_fixed: true }
    prettier:
      {
        glob: "*.{js,jsx,ts,tsx,json,md,yml,yaml,css}",
        run: "pnpm exec prettier --write {staged_files}",
        stage_fixed: true,
      }
```

CI still runs `eslint .` + `prettier --check .` over the whole tree as a safety net. Never run repo-wide lint in a hook.

## Biome — when to consider it

Biome is a single Rust binary that does both linting and formatting. Trade-offs:

| Pro                                                     | Con                                                                                                                           |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| ~10-20× faster than ESLint + Prettier combined          | Smaller rule set; some `typescript-eslint` rules have no equivalent yet                                                       |
| One config (`biome.json`), one binary, no plugin matrix | No first-party `react-hooks` rules-of-hooks coverage as of 2.x (use `eslint-plugin-react-hooks` alongside, or accept the gap) |
| Built-in monorepo support via `extends`                 | Auto-fixes are sometimes too aggressive; review more carefully than Prettier                                                  |
| Formatter output is near-Prettier-identical             | Migrations from large ESLint configs lose rules — audit, don't assume parity                                                  |

**Adopt Biome when:** the project is greenfield, the lint config is small, and CI feedback latency matters. **Stay on ESLint when:** you depend on niche plugins (`@tanstack/eslint-plugin-query`, `eslint-plugin-import-x`, library-specific rule packs), or the existing config is heavily tuned.

Hybrid pattern that works: Biome for format + the obvious lint wins; ESLint with a trimmed rule set for the rules Biome lacks. Run both in CI; only Biome on save.

`biome.json` baseline:

```json
{
  "$schema": "https://biomejs.dev/schemas/2.0.0/schema.json",
  "files": { "ignore": ["dist", "build", "coverage"] },
  "formatter": { "indentStyle": "space", "indentWidth": 2, "lineWidth": 100 },
  "linter": { "rules": { "recommended": true } },
  "javascript": { "formatter": { "quoteStyle": "double", "trailingCommas": "all" } }
}
```

## Anti-patterns

- `eslint-plugin-prettier` — slow, noisy, fights the editor. See above.
- ESLint formatting rules (`indent`, `quotes`, `semi`) enabled with Prettier — turn them off via `eslint-config-prettier`.
- `eslintConfig` in `package.json` — flat config is a file, not a property.
- `.eslintrc.*` in 2026 — ESLint 9 ignores them. If `eslint --print-config` reports nothing, you're on the legacy path.
- Per-package `.prettierrc` overrides with different print widths — formatting will flap on every cross-package edit.
- Running lint over `node_modules` because `ignores` was misconfigured — flat config `ignores` is global only as the first config-object entry; per-block `ignores` works differently.
- `--fix` in CI — CI verifies, doesn't mutate. Use `--fix` locally and in pre-commit, never in the verify pipeline.
- Adopting Biome by deleting the ESLint config the same day — run them in parallel for a sprint, compare findings, then cut.
- Disabling `react-hooks/exhaustive-deps` because it's "annoying" — every disabled instance is a future stale-closure bug. Fix the dep array or extract a `useCallback`.

## Hand-off

For the TypeScript rules these configs enforce (strict-mode flags, `import type`, `unknown` in `catch`): `Skill(typescript)`. For React patterns the hooks/jsx-a11y plugins are catching: `Skill(react)`. For wiring lint into the test runner (Vitest reporters, `vitest --typecheck`): `Skill(ts-vitest)`. For workspace package manager mechanics: `Skill(pnpm-essentials)`, `Skill(bun-essentials)`. For pre-commit hook plumbing and tagged-release workflows: `Skill(tooling-git-advanced)`.
