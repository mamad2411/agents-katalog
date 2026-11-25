---
name: mynode
description: Mandatory Node.js, TypeScript, and pnpm project conventions — ESM, tsconfig, tooling, and code style. MUST be invoked before writing, modifying, or scaffolding any TypeScript code in a project with package.json and tsconfig.json. Contains binding rules that override default patterns for exports, imports, tooling choices, and configuration.
---

# Node.js / TypeScript / pnpm Conventions

These are opinionated defaults for Node.js projects using TypeScript and pnpm. Apply them when writing new code or making configuration decisions. In existing projects, read the current conventions first — if the project disagrees with a rule below, follow the project unless it is clearly legacy.

## Tooling

| Concern | Choice | Never |
|---------|--------|-------|
| Package manager | pnpm | npm, yarn |
| Module system | ESM (`"type": "module"`) | CommonJS (unless project already is) |
| Test runner | Vitest | Jest, mocha |
| TS execution (dev) | tsx | ts-node |
| Bundler (apps) | Vite | webpack, CRA |
| Bundler (libs) | tsup | raw tsc emit, rollup config |
| Lint | ESLint (flat config, `eslint.config.ts`) | .eslintrc legacy format |
| Format | Prettier | editor-only formatting |
| Node version | `packageManager` field + `.nvmrc` | unmanaged |

## pnpm rules

- Install with `pnpm add`, run with `pnpm run`, execute with `pnpm dlx` (not npx).
- Monorepo internal deps use `workspace:*`.
- Always commit `pnpm-lock.yaml`. Never edit it by hand.
- `.npmrc` defaults — `strict-peer-dependencies=false`, `auto-install-peers=true`.
- Never set `shamefully-hoist=true`. If a tool breaks, add a targeted `public-hoist-pattern[]=name`.
- Set `"packageManager": "pnpm@<version>"` in package.json.

## tsconfig stance

For new projects and new packages. See [references/tsconfig.md](references/tsconfig.md) for full snippets.

- `strict: true` — always.
- `moduleResolution: "bundler"` — no `.js` extensions in imports.
- `verbatimModuleSyntax: true` — forces explicit `import type`.
- `module: "ESNext"`, `target: "ES2022"`.
- `noUncheckedIndexedAccess: true` — new projects only, do not retrofit.
- `noEmit: true` for apps (Vite handles emit); `declaration: true` for libs.

## Code style

See [references/code-style.md](references/code-style.md) for examples.

- Named exports only. Default exports only when a framework mandates them (Next.js pages, etc.).
- `import type { Foo }` for type-only imports.
- Prefer `satisfies` over `as` for type narrowing.
- Use `as const` for literal config objects.
- `unknown` over `any`. Using `any` requires a justification comment.
- No `enum`. Use `as const` objects + union types.
- No barrel files (`index.ts` re-exports). Import from specific module paths.
- Arrow functions for callbacks; `function` declarations for exported public APIs.
- File naming — `kebab-case.ts` for modules, `PascalCase.tsx` for React components.

## Escape hatch

If the existing project uses CJS, Jest, npm, or any conflicting convention — match the project. Do not migrate or refactor existing patterns unless explicitly asked. These rules govern *new* decisions.
