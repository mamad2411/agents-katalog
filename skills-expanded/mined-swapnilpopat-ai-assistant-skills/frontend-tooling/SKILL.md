---
name: frontend-tooling
description: Expert Vite 6+, pnpm 9+, and Vitest 2+ guidance for frontend build, package, and test tooling. Use when configuring Vite, managing pnpm workspaces, setting up Vitest, or auditing toolchain health.
source: https://github.com/JetBrains/skills/tree/main/vite
---

# Frontend Tooling

Production toolchain for modern frontend repos: Vite 6+ (Rolldown-bundled prod builds incoming), pnpm 9+ workspaces with catalogs, Vitest 2/3 with browser mode and Testcontainers-style container tests, plus deterministic CI.

## Stack Baseline (2026)

| Component | Default | Notes |
| --- | --- | --- |
| Node | 22 LTS (or 24 LTS) | `engines.node` pinned in `package.json`. Use Volta or Corepack. |
| Package manager | pnpm 9.x | Catalogs (`pnpm-workspace.yaml`), workspace protocol, content-addressable store. Enable via Corepack. |
| Build | Vite 6.x (Rolldown coming in Vite 7) | `defineConfig`, ESM config, environments API. |
| Test | Vitest 2/3 | Browser mode (Playwright provider), `vi.mock`, `expect.extend`, type tests. |
| Linter | ESLint 9 (flat config) + `typescript-eslint` 8 | `eslint.config.ts`. |
| Formatter | Prettier 3 or Biome 1.9 | Pick one; Biome is faster, smaller plugin ecosystem. |
| Type checking | TypeScript 5.6+, `strict: true` | Run `tsc --noEmit` in CI even if Vite transpiles. |
| Git hooks | `lefthook` or `husky` + `lint-staged` | Pre-commit: lint, format, type-check changed files. |

## When to Use

- Bootstrapping or reconfiguring a Vite project.
- Setting up a pnpm monorepo with catalogs.
- Wiring or debugging Vitest (jsdom vs browser mode, mocks, coverage).
- Reviewing or fixing CI install caching.
- Migrating from Webpack/CRA/Yarn/npm to Vite + pnpm.

## Instructions

### 1. Vite Configuration: One Config, Explicit Aliases, Layered Env

```ts
// vite.config.ts
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react-swc";
import tsconfigPaths from "vite-tsconfig-paths";
import { fileURLToPath, URL } from "node:url";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "VITE_");
  return {
    plugins: [react(), tsconfigPaths()],
    resolve: {
      alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
    },
    server: {
      port: 5173,
      strictPort: true,
      proxy: {
        "/api": { target: env.VITE_API_URL, changeOrigin: true },
      },
    },
    build: {
      target: "es2022",                                     // align with browserslist
      sourcemap: true,                                       // upload to error tracker, then strip from CDN
      rollupOptions: {
        output: {
          manualChunks: {
            react: ["react", "react-dom"],
            tanstack: ["@tanstack/react-query", "@tanstack/react-router"],
          },
        },
      },
    },
    define: {
      __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
    },
    test: {                                                  // Vitest config inline (one source of truth)
      environment: "jsdom",
      setupFiles: ["./src/test/setup.ts"],
      globals: false,
      coverage: {
        provider: "v8",
        reporter: ["text", "lcov"],
        thresholds: { lines: 80, functions: 80, branches: 75, statements: 80 },
      },
    },
  };
});
```

Key rules:

- Only `VITE_*` env vars are exposed to client code (`import.meta.env.VITE_*`). Anything else stays server-side.
- Don't put secrets in `.env` files committed to git. Document each `.env.example` key.
- Use `tsconfig-paths` so a single `tsconfig.json` `paths` map drives both TS resolution and Vite resolution.
- Prefer `import.meta.glob` for many similar imports (routes, MDX) over hand-written index files.
- Pin browser targets in one place: `package.json` `browserslist` or `build.target`.

### 2. Library Mode (Publishing a Package)

```ts
// vite.config.ts (library)
import { defineConfig } from "vite";
import dts from "vite-plugin-dts";

export default defineConfig({
  plugins: [dts({ rollupTypes: true })],
  build: {
    lib: {
      entry: "src/index.ts",
      formats: ["es"],                                      // ESM only by default in 2026
      fileName: "index",
    },
    sourcemap: true,
    rollupOptions: {
      external: ["react", "react-dom", /^@tanstack\//],     // peer deps stay external
      output: { exports: "named" },
    },
  },
});
```

`package.json`:

```jsonc
{
  "type": "module",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "import": "./dist/index.js" }
  },
  "files": ["dist"],
  "sideEffects": false,
  "publishConfig": { "access": "public", "provenance": true }
}
```

Always set `sideEffects: false` (or list the specific side-effecting files) so consumers can tree-shake.

### 3. pnpm Workspaces with Catalogs

`pnpm-workspace.yaml`:

```yaml
packages:
  - "apps/*"
  - "packages/*"
catalog:
  react: ^19.0.0
  react-dom: ^19.0.0
  typescript: ^5.6.3
  vite: ^6.0.0
  vitest: ^2.1.0
catalogs:
  test:
    "@testing-library/react": ^16.0.0
    "@playwright/test": ^1.48.0
```

Consume in a package:

```jsonc
{
  "name": "@acme/web",
  "dependencies": {
    "react": "catalog:",
    "react-dom": "catalog:",
    "@acme/ui": "workspace:*"
  },
  "devDependencies": {
    "@testing-library/react": "catalog:test",
    "vite": "catalog:",
    "vitest": "catalog:"
  }
}
```

Why catalogs: one place to bump `react` for the whole repo; no version drift; `pnpm update -r react` Just Works.

`.npmrc` essentials:

```ini
auto-install-peers=true
strict-peer-dependencies=false
shamefully-hoist=false              # keep node_modules clean; force explicit deps
prefer-frozen-lockfile=true         # CI behavior: fail on drift
```

Common workspace commands:

```bash
pnpm i                              # install (uses lockfile)
pnpm i --frozen-lockfile            # CI install
pnpm -r build                       # build everything
pnpm --filter @acme/web test        # filter by package
pnpm --filter "...{packages/ui}"... # everything that depends on ui
pnpm dlx <tool>                     # one-off; like npx
pnpm -r exec tsc --noEmit           # type-check all packages
pnpm update -r --latest             # bump versions
```

### 4. Vitest: Fast, Vite-Native Testing

`src/test/setup.ts`:

```ts
import "@testing-library/jest-dom/vitest";
import { afterEach } from "vitest";
import { cleanup } from "@testing-library/react";

afterEach(() => cleanup());
```

Patterns:

```ts
import { describe, expect, it, vi, beforeEach } from "vitest";

vi.mock("./api", () => ({ getUser: vi.fn().mockResolvedValue({ id: "1", name: "Ada" }) }));

describe("UserBadge", () => {
  beforeEach(() => vi.clearAllMocks());
  it("renders the user name", async () => {
    // ...
  });
});

it.concurrent("a", async () => { /* parallel within file */ });
it.each([["a", 1], ["b", 2]])("%s -> %i", (input, expected) => { /* ... */ });
```

Browser mode (Vitest 2+) for components that need a real DOM, layout, or visual snapshots:

```ts
// vitest.config.ts
import { defineConfig } from "vitest/config";
export default defineConfig({
  test: {
    browser: {
      enabled: true,
      provider: "playwright",
      instances: [{ browser: "chromium" }],
    },
  },
});
```

Coverage with v8 (default in Vitest 2). Set thresholds; treat them as smoke alarms, not goals. MSW + Vitest is the default for HTTP mocking.

### 5. Lint, Format, Type-Check (ESLint Flat Config)

```ts
// eslint.config.ts
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import react from "eslint-plugin-react";
import hooks from "eslint-plugin-react-hooks";
import jsxA11y from "eslint-plugin-jsx-a11y";

export default tseslint.config(
  { ignores: ["dist", "coverage", ".turbo"] },
  js.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: { parserOptions: { project: "./tsconfig.json" } },
    plugins: { react, "react-hooks": hooks, "jsx-a11y": jsxA11y },
    rules: {
      ...react.configs.recommended.rules,
      ...hooks.configs.recommended.rules,
      ...jsxA11y.configs.recommended.rules,
      "react/react-in-jsx-scope": "off",
    },
    settings: { react: { version: "detect" } },
  }
);
```

Run in CI:

```bash
pnpm lint
pnpm exec tsc --noEmit -p .
pnpm test --coverage
pnpm build
```

Use `lint-staged` to scope lint/format to changed files on pre-commit.

### 6. Bundle Hygiene

- Inspect with `vite-bundle-visualizer` or `rollup-plugin-visualizer`.
- Budgets in CI (`size-limit` or `bundlesize`):
  - JS first-load: <= 170KB gzip for typical apps; lower for marketing pages.
  - CSS first-load: <= 50KB gzip.
- Code-split per route + per heavy widget (`React.lazy` / `defineAsyncComponent`).
- Avoid barrel re-exports in hot paths - they defeat tree-shaking. Import `lodash-es/debounce` not `lodash`.
- Use modern alternatives: `date-fns` v3 (ESM, tree-shakable) over `moment`; `valibot` over `zod` if bundle is critical.
- Strip dev-only code with `import.meta.env.PROD`.

### 7. Determinism in CI

- Always `--frozen-lockfile` install.
- Cache pnpm store between runs:
  ```yaml
  - uses: pnpm/action-setup@v4
    with: { version: 9 }
  - uses: actions/setup-node@v4
    with: { node-version: 22, cache: "pnpm" }
  - run: pnpm install --frozen-lockfile
  ```
- Run `pnpm dedupe --check` to fail on lockfile drift after manual edits.
- Pin OS images (`ubuntu-24.04`, not `ubuntu-latest`) for repeatable Playwright + Vitest browser runs.
- Use Turborepo or Nx caching for monorepos when build time matters.

### 8. Security

- `pnpm audit --prod` in CI; auto-PRs via Dependabot/Renovate.
- Verify package provenance (`pnpm install --frozen-lockfile --strict-peer-dependencies` + npm provenance attestations).
- SCA (Snyk, Socket.dev) to catch typo-squatting and supply-chain risk.
- Lock down `pnpm` allow-scripts: `--ignore-scripts` for untrusted deps; review which packages run install scripts.
- Don't commit `.env` files; commit `.env.example` only.

### 9. Migration Notes

- **Webpack -> Vite**: replace loaders with Vite plugins; rewrite `process.env.X` to `import.meta.env.VITE_X`; replace `require.context` with `import.meta.glob`.
- **CRA -> Vite**: `create-react-app` is unmaintained; migrate. Public assets move to `/public`; `react-scripts` script entries are replaced with `vite`/`vite build`/`vite preview`.
- **npm/Yarn -> pnpm**: delete `node_modules` + `package-lock.json`/`yarn.lock`; `pnpm import` to convert lockfile; verify no phantom deps surface (modules previously hoisted that you imported without declaring).
- **Jest -> Vitest**: APIs are nearly identical. Replace `jest.mock` with `vi.mock`, `jest.fn` with `vi.fn`. Update `tsconfig` `types` to include `vitest/globals` only if `globals: true`.

## Common Pitfalls

| Anti-pattern | Why it hurts | Fix |
| --- | --- | --- |
| Mixing npm/yarn/pnpm in one repo | Lockfile chaos, hoisting differs | Pick one (pnpm); commit only its lockfile |
| `process.env.X` in client code with Vite | Undefined at runtime | `import.meta.env.VITE_X` |
| `shamefully-hoist=true` to "fix" missing deps | Hides phantom deps | Declare them properly |
| Two configs: `vite.config.ts` + `vitest.config.ts` for the same project | Drift between dev and tests | One config with `test` block |
| `coverage: 100%` as the goal | Junk tests for coverage | Threshold + risk-based testing |
| Building with `vite build` but skipping `tsc --noEmit` | Type errors slip into prod | Always type-check in CI |
| Importing CommonJS-only packages in pure ESM | Subtle interop bugs | `import * as cjs from "pkg"` or upgrade |
| Wildcard `manualChunks: () => 'vendor'` | Defeats per-route splitting | Group only stable shared chunks |
| Committing `pnpm-lock.yaml` conflicts resolved by hand | Broken installs | Resolve via `pnpm install` and recommit |
| Using `pnpm i --no-frozen-lockfile` in CI | Silent dep drift | Always `--frozen-lockfile` |

## Output Format

When applying this skill, deliver:

1. Toolchain decision matrix (PM, build, test, lint, format).
2. `vite.config.ts` (or `vitest.config.ts`) with annotated decisions.
3. `pnpm-workspace.yaml` + per-package `package.json` snippet using catalogs.
4. CI install + cache snippet.
5. Lint/type-check/test/build commands documented in `package.json` `scripts`.
6. Bundle budget + monitoring plan.
7. Migration steps if relevant.

## Authoritative References

- Vite docs: https://vite.dev/
- Vite config reference: https://vite.dev/config/
- Vite Environment API: https://vite.dev/guide/api-environment
- pnpm docs: https://pnpm.io/
- pnpm catalogs: https://pnpm.io/catalogs
- pnpm workspaces: https://pnpm.io/workspaces
- Vitest docs: https://vitest.dev/
- Vitest browser mode: https://vitest.dev/guide/browser/
- Testing Library: https://testing-library.com/
- ESLint flat config: https://eslint.org/docs/latest/use/configure/configuration-files
- typescript-eslint: https://typescript-eslint.io/
- Biome: https://biomejs.dev/
- Turborepo: https://turbo.build/repo/docs
- Rolldown (future Vite bundler): https://rolldown.rs/
- Browserslist: https://browsersl.ist/